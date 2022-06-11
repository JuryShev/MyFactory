import mysql.connector
BD_password='1234'
def create_database(name_db, path_script):
    with mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='1234',
            port='3306'
            # database='fur_database'

    ) as connection:
        sql_file = open(path_script)
        sql_as_string = sql_file.read()
        sql_as_string = sql_as_string.replace('*', name_db)
        mycursor = connection.cursor()
        print(f"sql_as_string={sql_as_string}")
        mycursor.execute(sql_as_string)

def create_tables_factory(name_db, path_script):
    with mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='1234',
            port='3306',
            database=name_db

    ) as connection:
        sql_file = open(path_script)
        sql_as_string = sql_file.read()
        mycursor = connection.cursor()
        mycursor.execute(sql_as_string)

def get_databases():
    with mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='1234',
            port='3306'
            # database='fur_database'

    ) as connection:

        sql_command = 'SHOW SCHEMAS'
        mycursor = connection.cursor()
        mycursor.execute(sql_command)
        tuple_databases = mycursor.fetchall()
        list_databases = []
        forbidden_set = {'sys', 'performance_schema', 'information_schema', 'mysql'}
        for i in tuple_databases:
            if i[0] not in forbidden_set:
                list_databases.append(i[0])
        return list_databases



class FurnitureDtabase:
    def __init__(self, name_db):
        self.host='127.0.0.1'
        self.user='root'
        self.password = '1234'
        self.port = '3306'
        self.database = name_db



    def get_last_row(self, name_table, name_column='*'):
        print("start")
        with mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            port=self.port,
            database=self.database

        ) as connection:
            mycursor = connection.cursor()
            name_id='id_'+name_table
            mysql_comand = f'SELECT {name_column} FROM {name_table} ORDER BY {name_id} DESC LIMIT 1'
            mycursor.execute(mysql_comand)
            last_row = mycursor.fetchall()
        return last_row

    def open_dir_associated_file(self, row, name_table, names_column_file):
        id_column= list(row.keys())[0]
        id=row[id_column]
        with mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            port=self.port,
            database=self.database

        ) as connection:
            mycursor = connection.cursor()
            mysql_comand=f'SELECT {names_column_file} FROM {name_table} WHERE {id_column}={id} '
            mycursor.execute(mysql_comand)
            dir_file=mycursor.fetchall()
            return dir_file[0][0]
        #SELECT id_personal FROM with_photo.personal ORDER BY id_personal DESC LIMIT 1

    def add_column(self, name_table, name_column, type_data):
        print("start")
        with mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            port=self.port,
            database=self.database

        ) as connection:
            mysql_comand='{0}{1}{2}{3}{4}{5}'.format('ALTER TABLE ', name_table, ' ADD ', name_column, ' ', type_data)
            mycursor = connection.cursor()
            mycursor.execute(mysql_comand)

    def add_row(self, name_table, name_columns, data):
        print("start")
        with mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            port=self.port,
            database=self.database

        ) as connection:
            value='VALUES ('
            insert='INSERT INTO '+name_table+'('
            if len(name_columns)==len(data[:]):
                d_type=','.join('%s' for _ in range(len(data)))
                name_columns=','.join(name_columns)
                value=value+d_type+')'
                insert=insert+name_columns+') '
                mysql_comand=(insert+value)
                mycursor = connection.cursor()
                # for i in range(len(data)):
                #     d=tuple(data[:][i])
                mycursor.execute(mysql_comand, data)
                connection.commit()

    def del_row(self, name_table, title_id :tuple, value_id:tuple):
        with mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                port=self.port,
                database=self.database

        ) as connection:
            mycursor = connection.cursor()
            for n in range(len(title_id)):
                mysql_comand = f"DELETE FROM {name_table} WHERE {title_id[n]} = {value_id[n]}"
                mycursor.execute(mysql_comand)
                connection.commit()

    def get_type(self, name_table, orig_t=1):
        with mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                port=self.port,
                database=self.database

        ) as connection:
            mycursor = connection.cursor()
            mysql_comand = (f'SHOW COLUMNS FROM {self.database}.{name_table}')
            mycursor.execute(mysql_comand)
            show_columns=mycursor.fetchall()
            column=[]
            column_type=[]
            for i in enumerate(show_columns):
                column.append(i[1][0])
                column_type.append(i[1][1])
                column_type[i[0]]=column_type[i[0]].decode("utf-8")

            if orig_t==0:
                type_columns = dict(zip(column, column_type))
                return  type_columns
            else:
                for i in enumerate(column_type):
                    if i[1].startswith('varchar'):
                        column_type[i[0]]=str
                    elif i[1].startswith('int'):
                        column_type[i[0]] = int
                    elif i[1].startswith('decimal'):
                        column_type[i[0]] = float

                type_columns = dict(zip(column, column_type))


                return type_columns

    def get_tables(self):
        with mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                port=self.port,
                database=self.database

        ) as connection:
            list_table_=[]
            mycursor = connection.cursor()
            mysql_comand = (f'SHOW TABLES FROM {self.database}')
            mycursor.execute(mysql_comand)
            list_table = mycursor.fetchall()
            for i in list_table:
                list_table_.append(i[0])

            print(list_table_)
        return list_table_

    def check_value(self, name_table, name_column, data):
        """
        Проверяет значение на схожесть.
        MySQL запрос: SELECT column FROM table WHERE column LIKE "%text%"
        (для полной схожести название значения отправлять полностью)

        :param name_table: str
        :param name_columns: str
        :param data: str
        :return: True or result str
        """

        with mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                port=self.port,
                database=self.database

        ) as connection:
            mycursor = connection.cursor()
            if data == str :

                mysql_comand_full='{0}{1}{2}{3}{4}{5}{6}{7}'.format('SELECT ', name_column, ' FROM ',
                                                         name_table, ' WHERE ', name_column, ' LIKE ', f' "%{data}%" ')
                mysql_comand_partial = '{0}{1}{2}{3}{4}{5}{6}{7}'.format('SELECT ', name_column, ' FROM ',
                                                           name_table, ' WHERE ', name_column, ' LIKE ',
                                                           f' "%{data[:-1]}%" ')
                mycursor.execute(mysql_comand_full)
                full_match = mycursor.fetchall()
                mycursor.execute(mysql_comand_partial)
                partial_match = mycursor.fetchall()
            else:
                pass
            if len(full_match)>0:
                return full_match[0][0]+'$'
            elif len(partial_match)>0:
                return full_match + '%'

        return 'True'

    def count_row(self, name_table):
        """
        :param name_table str:
        :return count row:
        Comand MySQL:SELECT COUNT(1) FROM name_table
        """
        with mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                port=self.port,
                database=self.database

        ) as connection:
            mycursor = connection.cursor()
            mysql_comand = 'SELECT COUNT(1) FROM '+name_table
            mycursor.execute(mysql_comand)
            count = mycursor.fetchall()
        return count
    def clear_table(self, name_table):
        """

        :param name_table:
        :return: None
        """
        with mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                port=self.port,
                database=self.database

        ) as connection:
            mycursor = connection.cursor()
            on_update = 'SET SQL_SAFE_UPDATES = 0'
            cl_table=f'DELETE FROM {name_table}'
            off_update='SET SQL_SAFE_UPDATES = 1'
            mycursor.execute(on_update)
            mycursor.execute(cl_table)
            mycursor.execute(off_update)
            connection.commit()

        return None

    def get_data_all(self, name_table):
        with mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                port=self.port,
                database=self.database

        ) as connection:
            mycursor = connection.cursor()
            mysql_comand= f'SELECT * from {name_table}'
            mycursor.execute(mysql_comand)
            data=mycursor.fetchall()

        return data

    def get_name_column(self, name_table, format_result='all'):
        with mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                port=self.port,
                database=self.database

        ) as connection:
            field_names=None
            mycursor = connection.cursor()
            mysql_comand= f'SHOW COLUMNS from {name_table}'
            mycursor.execute(mysql_comand)
            name_column=mycursor.fetchall()

            if format_result=='all':
                field_names=name_column
            elif format_result=='names':
                field_names = [i[0] for i in name_column]

        return field_names

##############доделать###############################################
    def get_row(self, name_db,name_table, name_row, name_condition):
        with mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                port=self.port,
                database=self.database

        ) as connection:
            mycursor = connection.cursor()
            mysql_comand = "SELECT * "\
                           f" FROM {name_db}.{name_table}" \
                           f" WHERE {name_table}.{name_row} = '{name_condition}'"

            mycursor.execute(mysql_comand)
            count = mycursor.fetchall()
            if len(count)>0:
                field_names = [i[0] for i in mycursor.description]
                for i  in range(len(count)):
                    count[i]=dict(zip(field_names, list(count[i])))
            return count
#############################################################################

    def edit_row(self, name_table, title: tuple, value : tuple):
        with mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                port=self.port,
                database=self.database

        ) as connection:
            mycursor = connection.cursor()
            for n in range(1,len(title)):
                if type(value[n])==str:
                    mysql_comand=f"UPDATE {name_table} SET {title[n]} = '{value[n]}' WHERE {title[0]} = {value[0]}"
                else:
                    mysql_comand = f"UPDATE {name_table} SET {title[n]} = {value[n]} WHERE {title[0]} = {value[0]}"
                mycursor.execute(mysql_comand)
                connection.commit()

    def search_personal(self, name_table, name_personal):
        with mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                port=self.port,
                database=self.database

        ) as connection:
            mycursor = connection.cursor()
            name_personal_compile=''
            for n in name_personal:
                name_personal_compile=name_personal_compile+" "+n
            name_personal_compile=name_personal_compile[1:]

            mysql_comand="SELECT id_personal, name, education, number, certification, salaryl, bonus, birthday, created_pers, dir_avatar, " \
                    " title as 'id_department', label_post as 'id_posts'"\
                    f" FROM {name_table}.personal" \
                    f" INNER JOIN {name_table}.department ON department.id_department = personal.id_department"\
                    f" INNER JOIN {name_table}.posts ON posts.id_posts = personal.id_posts"\
                    f" WHERE personal.name LIKE '%{name_personal_compile}%' or '{name_personal_compile}%'"

            mycursor.execute(mysql_comand)
            count = mycursor.fetchall()
            if len(count)>0:
                field_names = [i[0] for i in mycursor.description]
                for i  in range(len(count)):
                    count[i]=dict(zip(field_names, list(count[i])))
            return count





