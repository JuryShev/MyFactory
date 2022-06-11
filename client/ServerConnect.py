import requests
import json

class ServerConnector():
    def __init__(self, id_user, password, adress, port):
        self.id_user = id_user
        self.adress=adress
        self.command = 0
        self.db_command = 0
        self.name_db=''
        self.url = f"http://{self.adress}:{port}"
        self.password=password

    def connect_server(self, command, db_command):
        result = requests.post(f"{self.url}/furniture/connect_server/",
                               json={
                                   "comand": command,
                                   "user": self.id_user,
                                   "db_comand": db_command,
                                   "password": self.password},
                                )
        return result

    def add_db(self, command, db_command):
        result = requests.post(f"{self.url}/furniture/add_db",
                               json={
                                   "comand": command,
                                   "user": self.id_user,
                                   "db_comand": db_command,
                                   "name_db": self.name_db})
        return result

    def add_criterion(self, data_send):
        result = requests.post(f"{self.url}/furniture/create_company_{self.name_db}/",
                               json=data_send)
        return result

    def add_personal(self, data_send):
        result = requests.post(f"{self.url}/furniture/add_personal_{self.name_db}/",
                               json=data_send)
        return result

    def edit_table(self, data_send):
        result = requests.post(f"{self.url}/furniture/edit_tables_{self.name_db}/",
                               json=data_send)
        return result

    def del_associated_file(self, data_send):
        result = requests.post(f"{self.url}/furniture/del_associated_file_{self.name_db}/",
                               json=data_send)
        return result

    def del_row_table(self, data_send):
        result = requests.post(f"{self.url}/furniture/delete_row_{self.name_db}/",
                               json=data_send)
        return result

    def edit_associated_file(self, data_send):
        result = requests.post(f"{self.url}/furniture/edit_associated_file_{self.name_db}/",
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



    def del_person(self, data_send, names_column_file:dir ):

        data_send['names_column_file']=names_column_file
        result=self.del_associated_file( data_send).content
        result = result.decode('utf-8')
        if result=='ok':
            data_send.pop('names_column_file')
            result=self.del_row_table(data_send)
        return result

    def get_row_table(self, data_send, name_row_condition):
        result = requests.post(f"{self.url}/furniture/get_row_{self.name_db}_{name_row_condition}/",
                               json=data_send)
        return result

    def add_row_table(self, data_send):
        result = requests.post(f"{self.url}/furniture/add_row_{self.name_db}/",
                               json=data_send)
        return result

    def get_struct(self):
        result = requests.post(f"{self.url}/furniture/get_inside_struct_{self.name_db}/",json={
                                   "comand": 1100,
                                   "user": self.id_user,
                                   "db_comand": 1})
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
                               json={
                                   "comand": 1110,
                                   "user": self.id_user,
                                   "db_comand": 1})
        return result

    def get_personal(self, data_send):
        result=requests.post(f"{self.url}/furniture/get_personal_{self.name_db}/",
                      json=data_send)

        return result


