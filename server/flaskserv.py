import requests
import hashlib
import logging

from flask import Flask, request
from flask_pymongo import PyMongo
from flask_restful import reqparse
from celery import Celery

from send_mail import send_mail

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost/MD5_db'
celery = Celery(app.name, broker='redis://localhost')
mongo = PyMongo(app)

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(filename= "service.log", level=logging.INFO, format=FORMAT)

#Получение статуса задачи по идентификатору (API GET)
@app.route('/check', methods=['GET'])
def get():
    id = str(request.args.get('id'))
    logging.info(f'Поступил запрос по задаче с id = {id}')
    try:
        task_info = mongo.db.task_info.find({'id': f'{id}'},{'_id': 0})
        response = response_preparation(task_info)
        return response
    except Exception:
        return {'message':'identifier not found'}

#Создание задачи с идентификатором (API POST)
@app.route('/submit', methods=['POST'])
def post():
    parser = reqparse.RequestParser()
    parser.add_argument('email')
    parser.add_argument('url',required=True)
    args = parser.parse_args()
    logging.info(f'''Поступил запрос на создание задачи, параметры: email = {args['email']}, url = {args['url']}''')
    task_id = create_task_with_id(args['url'],args['email'])
    mongo.db.task_info.insert({'id':f'{task_id}','md5':'','status':'100','url': args['url']})
    return {'id': f'{task_id}'}

#Создание асинхронного процесса
def create_task_with_id(url,mail):
    task = calc_hash_sum.delay(url,mail)
    return task.task_id

#Подсчёт MD5-хеш суммы, отправка результатов на почту
@celery.task(name='flaskserv.calc_hash_sum',bind=True)
def calc_hash_sum(self,url,mail=''):
    file = requests.get(url)
    if file.status_code == 200: 
        hash_sum = hashlib.md5()
        hash_sum.update(file.content)
        hash_sum = hash_sum.hexdigest()
        mongo.db.task_info.update({'id': self.request.id},{'$set':{'md5':f'{hash_sum}', 'status':f'{file.status_code}'}})
        if mail is not None:
            try:
                send_mail(mail,url,hash_sum)
            except Exception as e:
                logging.info(f"Не удалось отправить письмо на почту! Ошибка:{e}")
    else:
        mongo.db.task_info.update({'id': self.request.id},{'$set':{'status':f'{file.status_code}'}})

#Подготовка ответа по запросу пользователя
def response_preparation(cursor):
    dict_list = list()
    for dictionary in cursor:
        dict_list.append(dictionary)
    response = dict_list[0]
    if response['status'] == '200':
        prepared_response = {'md5': response['md5'],
        'status': 'done',
        'url': response['url']
        }
        return prepared_response
    elif response['status'] == '100':
        prepared_response = {'status':'running'}
        return prepared_response
    elif response['status'] == '404':
        prepared_response = {'status':'not found'}
        return prepared_response
    elif response['status'] == '500':
        prepared_response = {'status':'task failure'}
        return prepared_response

if __name__=='__main__':
    app.run(debug=True)
    
