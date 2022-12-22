import requests
import json
import argon2
from base64 import b64decode
from itsdangerous import base64_decode
from flask import Markup
import zlib
from werkzeug.http import parse_date
import uuid
def hash_password(salt_user, password):
    salt_user=bytes(salt_user, 'utf-8')
    password = argon2.hash_password_raw(time_cost=16, memory_cost=2 ** 15,
                                        parallelism=2, hash_len=32,
                                        password=bytes(password, 'utf-8'),
                                        salt=salt_user,
                                        type=argon2.low_level.Type.ID).hex()
    return salt_user.decode(), password

def decode(cookie):
    """Decode a Flask cookie."""
    try:
        compressed = False
        payload = cookie

        if payload.startswith('.'):
            compressed = True
            payload = payload[1:]

        data = payload.split(".")[0]

        data = base64_decode(data)
        if compressed:
            data = zlib.decompress(data)

        return data.decode("utf-8")
    except Exception as e:
        return "[Decoding error: are you sure this was a Flask session cookie? {}]".format(e)

def flask_loads(value):
    """Flask uses a custom JSON serializer so they can encode other data types.
    This code is based on theirs, but we cast everything to strings because we
    don't need them to survive a roundtrip if we're just decoding them."""
    def object_hook(obj):
        if len(obj) != 1:
            return obj
        the_key, the_value = next(obj.iteritems())
        if the_key == ' t':
            return str(tuple(the_value))
        elif the_key == ' u':
            return str(uuid.UUID(the_value))
        elif the_key == ' b':
            return str(b64decode(the_value))
        elif the_key == ' m':
            return str(Markup(the_value))
        elif the_key == ' d':
            return str(parse_date(the_value))
        return obj
    return json.loads(value, object_hook=object_hook)

class ServerConnector():
    def __init__(self, id_user, password, adress, port):
        self.id_user = id_user
        self.adress=adress
        self.command = 0
        self.db_command = 0
        self.name_db=''
        self.url = f"http://{self.adress}:{port}"
        self.password=password
        self.coockies=None

    def get_nick_user(self):
        result = requests.post(f"{self.url}/furniture/get_nick_user/",
                               cookies=self.coockies
                               ).content.decode("utf-8")

        return result

    def change_log_pass(self,json_send):

        if json_send["change"]=='pass':
            result = requests.post(f"{self.url}/furniture/get_salt/",
                                   cookies=self.coockies)

            if len(json.loads(result.content.decode('utf-8'))['error']) == 0:
                result = json.loads(result.content.decode('utf-8'))
                _, password = hash_password(result['salt'], json_send['tables']['users']['password'])
                json_send['tables']['users']['password'] = password

                result = requests.post(f"{self.url}/furniture/change_log_pass_{self.name_db}/",
                                       cookies=self.coockies,
                                       json=json_send)
            return result
        elif json_send["change"]=='login':
            result = requests.post(f"{self.url}/furniture/change_log_pass_{self.name_db}/",
                                   cookies=self.coockies,
                                   json=json_send)
            self.coockies = result.cookies
            return result


    def connect_server(self, json_send):

        result=requests.post(f"{self.url}/furniture/get_salt/",
                                    cookies=self.coockies,
                                   json=json_send)

        if len(json.loads(result.content.decode('utf-8'))['error'])==0:
            result = json.loads(result.content.decode('utf-8'))
            _,password=hash_password(result['salt'], json_send['tables']['user']['password'])
            json_send['tables']['user']['password']=password
            json_send['tables']['user']['right']=result['right']
            result=requests.post(f"{self.url}/furniture/connect_server/",
                                        cookies=self.coockies,
                                       json=json_send)

            self.coockies=result.cookies
        return result
    def get_id_user(self):
        result = requests.post(f"{self.url}/furniture/get_id_user_{self.name_db}/",
                               cookies=self.coockies,
                               )
        self.coockies=result.cookies
        return result.content

    def add_db(self, command, db_command):
        result = requests.post(f"{self.url}/furniture/add_db",
                               cookies=self.coockies,
                               json={
                                   "comand": command,
                                   "user": self.id_user,
                                   "db_comand": db_command,
                                   "name_db": self.name_db})
        return result

    def add_criterion(self, data_send):
        result = requests.post(f"{self.url}/furniture/create_company_{self.name_db}/",
                               cookies=self.coockies,
                               json=data_send)
        return result

    def add_personal(self, data_send):
        result = requests.post(f"{self.url}/furniture/add_personal_{self.name_db}/",
                               cookies=self.coockies,
                               json=data_send)
        return result

    def edit_table(self, data_send):
        result = requests.post(f"{self.url}/furniture/edit_tables_{self.name_db}/",
                               cookies=self.coockies,
                               json=data_send)
        return result

    def edit_column_table(self, data_send):
        result = requests.post(f"{self.url}/furniture/edit_column_tables_{self.name_db}/",
                               cookies=self.coockies,
                               json=data_send)
        return result

    def del_associated_file(self, data_send):
        result = requests.post(f"{self.url}/furniture/del_associated_file_{self.name_db}/",
                               cookies=self.coockies,
                               json=data_send)
        return result

    def del_row_table(self, data_send):
        result = requests.post(f"{self.url}/furniture/delete_row_{self.name_db}/",
                               cookies=self.coockies,
                               json=data_send)
        return result
    def del_row_struct(self, data_send):
        result = requests.post(f"{self.url}/furniture/delete_row_struct_{self.name_db}/",
                               cookies=self.coockies,
                               json=data_send)
        return result

    def del_column_table(self, data_send):
        result = requests.post(f"{self.url}/furniture/delete_column_{self.name_db}/",
                               cookies=self.coockies,
                               json=data_send)
        return result

    def edit_associated_file(self, data_send):
        result = requests.post(f"{self.url}/furniture/edit_associated_file_{self.name_db}/",
                               cookies=self.coockies,
                               json=data_send)
        return result
    def edit_person(self, data_send, name_column_file):
        name_keys=list(data_send["tables"]["personal"][0].keys())[1:]
        result=''
        flag_edit_avtar=0
        if 'dir_avatar' in name_keys:
            data_send['names_column_file']=name_column_file
            result=self.edit_associated_file(data_send).content
            result = result.decode('utf-8')
            flag_edit_avtar=1
            data_send["tables"]["personal"][0].pop(name_column_file['personal'])
            if result!='ok':
                return result

        if flag_edit_avtar==1 and len(name_keys)==1:
            return result
        elif (flag_edit_avtar==1 and len(name_keys)>1) or flag_edit_avtar==0:
            result=self.edit_table(data_send).content
        return result.decode('utf-8')



    def del_person(self, data_send ):

        result = requests.post(f"{self.url}/furniture/del_person_{self.name_db}/",
                               cookies=self.coockies,
                               json=data_send)
        return result

    def get_row_table(self, data_send, name_row_condition):
        result = requests.post(f"{self.url}/furniture/get_row_{self.name_db}_{name_row_condition}/",
                               cookies=self.coockies,
                               json=data_send)
        return result

    def add_row_table(self, data_send):
        result = requests.post(f"{self.url}/furniture/add_row_{self.name_db}/",
                               cookies=self.coockies,
                               json=data_send)
        return result
    def add_column_table(self, data_send):
        result = requests.post(f"{self.url}/furniture/add_column_{self.name_db}/",
                               cookies=self.coockies,
                               json=data_send)
        return result

    def get_struct(self):
        result = requests.post(f"{self.url}/furniture/get_inside_struct_{self.name_db}/",
                               cookies=self.coockies,
                               json={
                                   "comand": 1100,
                                   "user": self.id_user,
                                   "db_comand": 1})
        return result

    def assessment_personal(self, data_send, mode='get'):
        if mode=='get':
            result = requests.post(f"{self.url}/furniture/get_persons_for_assessment_{self.name_db}/",
                                   cookies=self.coockies,
                                   json=data_send)
        elif mode=='send':
            result = requests.post(f"{self.url}/furniture/send_assessment_{self.name_db}/",
                                   cookies=self.coockies,
                                   json=data_send)
        else:
            result=f'команды {mode} не существует'

        return result

    def load_data_all(self,  name_table):
        db_cond = f"select * {name_table}"
        command_server = 1100
        json_ = {"comand": command_server,
                 "user": self.id_user,
                 "db_comand": 1,
                 "db_cond":db_cond
                 }
        self.load_data(json_)


    def load_data_cond(self):
        pass

    def load_databases(self):
        result = requests.post(f"{self.url}/furniture/get_databases/",
                               cookies=self.coockies,
                               json={
                                   "comand": 1110,
                                   "user": self.id_user,
                                   "db_comand": 1})
        return result

    def get_personal(self, data_send):
        result=requests.post(f"{self.url}/furniture/get_personal_{self.name_db}/",
                             cookies=self.coockies,
                      json=data_send)

        return result

    def register(self, data_send):
        if data_send['status']=='del_user':
            result = requests.post(f"{self.url}/furniture/del_user_{self.name_db}/",
                                   cookies=self.coockies,
                                   json=data_send)
        elif data_send['status']=='change' or data_send['status']=='register':
            result = requests.post(f"{self.url}/furniture/register_{self.name_db}/",
                                   cookies=self.coockies,
                                   json=data_send)
        else:
            result=None
        return result

    def activate_user(self, data_send):
        result = requests.post(f"{self.url}/furniture/activate_user/",
                               cookies=self.coockies,
                               json=data_send)
        return result

    def appoint_admin(self, data_send):
        result = requests.post(f"{self.url}/furniture/appoint_admin_{self.name_db}/",
                               cookies=self.coockies,
                               json=data_send)
        return result

    def clear_cookies(self):
        self.coockies=None
        print('ok')


