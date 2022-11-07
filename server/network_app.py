import datetime
import decimal
import json

from flask import Flask, request
from database import FurnitureDatabase
import database
import pickle
import itertools
import os
from datetime import datetime as dt


def full_check(json_data, stand_comand: dir, name_db):
    my_db = FurnitureDatabase(name_db=name_db)
    ch_headline = check_headline(json_data, stand_comand)
    if ch_headline != True:
        return ch_headline

    list_tables = my_db.get_tables()
    ch_table = check_table(json_data, list_tables)
    tables = json_data['tables']
    tables_list = tables.keys()
    if ch_table == False:
        return 'Check table False'

    for name_table in tables_list:
        list_column = my_db.get_name_column(name_table, format_result='names')
        data_table = tables[name_table]
        ch_name_column = check_column(list_column, data_table)
        if ch_name_column != 'ok':
            return f'column named {ch_name_column} does not exist in table {name_table}'
        type_columns = my_db.get_type(name_table)

        ch_type = check_type(data_table, name_table, type_columns)
        if ch_type != True:
            return 'Type error:' + ch_type
    return 'ok'


def check_headline(data, stand_comand: dict):
    flag_check = True

    if data['comand'] != stand_comand['comand']:
        print(f"command {data['comand']} does not match the execute command")
        return f"command {data['comand']} does not match the execute command"

    if data['user'] != stand_comand['user']:
        print(f"users {data['user']} does not have permission to perform the operation")
        return f"users {data['user']} does not have permission to perform the operation"

    if data['db_comand'] != stand_comand['db_comand']:
        print(f"command {data['db_comand']} does not allow adding data")
        return f"command {data['db_comand']} does not allow adding data"
    return flag_check


def check_column(get_columns, rows):
    for row in rows:
        json_columns = list(row.keys())
        for json_column in json_columns:
            if (json_column in get_columns) == False:
                return json_column
    return 'ok'


def check_type(data, name_table, type_columns):
    check_flag = True

    for row_table in data:
        # if type(row_table) != list:
        #     row_table=[row_table]
        for name_column in row_table:
            if not isinstance(row_table[name_column], type_columns[name_column]):
                check_flag = f'ERROR WRITE:type the data types of the row "{name_column}" to the table "{name_table}' \
                             f' do not match with the database'

                print(f'ERROR WRITE:type the data types of the row "{name_column}" to the table "{name_table}" '
                      f'do not match with the database')
                return check_flag
    return check_flag


def check_table(data, list_tables):
    send_tables = set(data['tables'].keys())
    list_tables = set(list_tables)
    check = send_tables <= list_tables
    return check


app = Flask(__name__)


# db=FurnitureDtabase


# _<int:comand>comand, data

@app.route('/furniture/connect_server/', methods=['POST'])
def connect_server():
    stand_comand = {'comand': 6666,
                    'user': 'admin',
                    'db_comand': 6666}
    a = request.data
    j = json.loads(a.decode('utf-8'))
    check_error = check_headline(j, stand_comand)
    if not check_error:
        return check_error
    if j['password'] == database.BD_password:
        return 'ok'


@app.route('/furniture/create_company_<name_db>/', methods=['POST'])
def create_company(name_db):
    name_criterions = []
    stand_comand = {'comand': 5000,
                    'user': 'admin',
                    'db_comand': 1}
    a = request.data
    j = json.loads(a.decode('utf-8'))
    check_error = full_check(json_data=j, stand_comand=stand_comand, name_db=name_db)
    if check_error != 'ok':
        return check_error
    my_db = FurnitureDatabase(name_db=name_db)
    ### Отправляться в метод add_row только в конструкции списка множектва (столбец 1, столбец 2)
    ###                                                                     данные 1    данные 2

    list_tables = j['tables']
    for name_table in list_tables:
        my_db.clear_table(name_table)
        list_rows = list_tables[name_table]
        for row in list_rows:
            title = list(row.keys())
            value = [row[i] for i in title]
            my_db.add_row(name_table, tuple(title), tuple(value))
    return 'ok'


@app.route('/furniture/add_personal_<name_db>/', methods=['POST'])
def add_personal(name_db):
    name_avatar = ''
    path_save_avatar = f'C:/Users/{os.getlogin()}/Documents/avatar/{name_db}/'
    if not os.path.exists(path_save_avatar):
        os.makedirs(path_save_avatar)

    stand_comand = {'comand': 2000,
                    'user': 'admin',
                    'db_comand': 1}
    a = request.data
    j = json.loads(a.decode('utf-8'))
    check_error = full_check(json_data=j, stand_comand=stand_comand, name_db=name_db)
    if check_error != 'ok':
        return check_error
    my_db = FurnitureDatabase(name_db=name_db)
    list_tables = j['tables']
    for name_table in list_tables:
        # my_db.clear_table(name_table)
        list_rows = list_tables[name_table]
        for row in list_rows:
            last_id = my_db.get_last_row(name_table, 'id_personal')
            if len(last_id) == 0:
                name_avatar = 'avatar_1'
            else:
                name_avatar = 'avatar_' + str(last_id[0][0] + 1)
            avatar = row['dir_avatar']
            name_save = path_save_avatar + name_avatar + '.pickle'
            with open(name_save, "wb") as outfile:
                # "wb" argument opens the file in binary mode
                pickle.dump(avatar, outfile)
            row['dir_avatar'] = name_save
            title = list(row.keys())
            value = [row[i] for i in title]
            my_db.add_row(name_table, tuple(title), tuple(value))

    return 'ok'


@app.route('/furniture/get_personal_<name_db>/', methods=['POST'])
def get_personal(name_db):
    result = None
    stand_comand = {'comand': 2001,
                    'user': 'admin',
                    'db_comand': 1}
    a = request.data
    j = json.loads(a.decode('utf-8'))
    check_error = full_check(json_data=j, stand_comand=stand_comand, name_db=name_db)
    if check_error != 'ok':
        return check_error
    my_db = FurnitureDatabase(name_db=name_db)
    list_tables = j['tables']
    for name_table in list_tables:
        # my_db.clear_table(name_table)
        list_rows = list_tables[name_table]
        for row in list_rows:
            for comb in itertools.permutations(row["name"].split(" ")):
                result = my_db.search_personal(name_db, comb)
                if len(result) > 0:
                    for pers in result:
                        dir_avatar = pers['dir_avatar']
                        with open(dir_avatar, "rb") as openfile:
                            avatar = pickle.load(openfile)
                            pers['dir_avatar'] = avatar
                    json_send = json.dumps(result, default=str)
                    return json_send
                else:
                    result = {"error": "Сотрудник с таким именем не найден"}
    json_send = json.dumps(result)
    return json_send


@app.route('/furniture/add_db/', methods=['POST'])
def add_factory(comand=1111):
    stand_comand = {'comand': comand,
                    'user': 'admin',
                    'db_comand': 1}
    path_cr_db = "./mysql_scripts/create_database.sql"
    path_cr_tb = "./mysql_scripts/create_table_factory_ed.sql"

    a = request.data
    j = json.loads(a.decode('utf-8'))
    check_error = check_headline(j, stand_comand)
    if check_error != True:
        return check_error
    database.create_database(j['name_db'], path_cr_db)
    database.create_tables_factory(j['name_db'], path_cr_tb)

    return "ok"


@app.route('/furniture/get_inside_struct_<name_db>/', methods=['POST'])
def get_inside_struct(name_db):
    table_list = {"tables": {"conf_criterion": [],
                             "department": [],
                             "bonus_koeficient": [],
                             "posts": []
                             }}
    temp_data = {}
    stand_comand = {'comand': 1100,
                    'user': 'admin',
                    'db_comand': 1,
                    }
    my_db = FurnitureDatabase(name_db=name_db)
    a = request.data
    j = json.loads(a.decode('utf-8'))
    check_error = check_headline(j, stand_comand)
    if check_error != True:
        return check_error

    for name_table in table_list["tables"]:
        data_table = my_db.get_data_all(name_table)
        column_table = my_db.get_name_column(name_table)
        for h in data_table:
            for i in range(len(h)):
                if type(h[i]) == decimal.Decimal:
                    temp_data[column_table[i][0]] = float(h[i])
                else:
                    temp_data[column_table[i][0]] = h[i]
            table_list["tables"][name_table].append(temp_data.copy())
        temp_data.clear()
    print("json")
    json_send = json.dumps(table_list)
    return json_send


@app.route('/furniture/edit_tables_<name_db>/', methods=['POST'])
def set_edit_tables(name_db):
    stand_comand = {'comand': 1110,
                    'user': 'admin',
                    'db_comand': 1,
                    }

    my_db = FurnitureDatabase(name_db=name_db)
    a = request.data
    j = json.loads(a.decode('utf-8'))
    check_error = full_check(json_data=j, stand_comand=stand_comand, name_db=name_db)
    if check_error != 'ok':
        return check_error
    list_tables = j['tables']
    for name_table in list_tables:
        list_rows = list_tables[name_table]
        for row in list_rows:
            title = list(row.keys())
            value = [row[i] for i in title]
            my_db.edit_row(name_table, tuple(title), tuple(value))
    return "ok"


@app.route('/furniture/edit_column_tables_<name_db>/', methods=['POST'])
def edit_column_tables(name_db):
    stand_comand = {'comand': 1336,
                    'user': 'admin',
                    'db_comand': 1,
                    }

    my_db = FurnitureDatabase(name_db=name_db)
    a = request.data
    j = json.loads(a.decode('utf-8'))
    check_error = check_headline(j, stand_comand)
    if check_error != True:
        return check_error
    list_tables = j['tables']
    ch_table = check_table(j, list_tables)
    if ch_table == False:
        return 'Check table False'
    for name_table in list_tables:
        list_rows = list_tables[name_table]
        list_column = my_db.get_name_column(name_table, format_result='names')
        for row in list_rows:
            old_name = row['old_name']
            if old_name in list_column:
                new_name = row['new_name']
                my_db.edit_column(name_table, old_name, new_name)
            else:
                return f"Невозможно отредактировать колонку {old_name}"

    return 'ok'


@app.route('/furniture/delete_row_<name_db>/', methods=['POST'])
def del_row_tables(name_db):
    stand_comand = {'comand': 1110,
                    'user': 'admin',
                    'db_comand': 1,
                    }
    my_db = FurnitureDatabase(name_db=name_db)
    a = request.data
    j = json.loads(a.decode('utf-8'))
    check_error = full_check(json_data=j, stand_comand=stand_comand, name_db=name_db)
    if check_error != 'ok':
        return check_error
    list_tables = j['tables']
    for name_table in list_tables:
        list_rows = list_tables[name_table]
        for row in list_rows:
            title = list(row.keys())
            value = [row[i] for i in title]
            if name_table == 'conf_criterion':
                list_column_criterion = my_db.get_name_column(name_table, format_result='names')
                for id_drop_criterion in value:
                    if len(my_db.check_value('personal_assessment', 'id_progress_now', 'id_criterion',
                                             id_drop_criterion)) > 0:
                        row_drop_criterion = my_db.check_value(name_table, '*', 'id_conf_criterion', id_drop_criterion)
                        my_db.add_row('drop_criterion', list_column_criterion[1:], row_drop_criterion[0][1:])
                        last_id_drop_criterion = my_db.get_last_row(name_table='drop_criterion',
                                                                    name_column='id_drop_criterion'
                                                                    )
                        my_db.edit_row('personal_assessment', ('id_criterion', 'id_drop_criterion'),
                                       (id_drop_criterion, last_id_drop_criterion[0][0]))

            my_db.del_row(name_table, tuple(title), tuple(value))
    return 'ok'


@app.route('/furniture/delete_column_<name_db>/', methods=['POST'])
def del_column_table(name_db):
    stand_comand = {'comand': 1503,
                    'user': 'admin',
                    'db_comand': 1,
                    }

    my_db = FurnitureDatabase(name_db=name_db)
    a = request.data
    j = json.loads(a.decode('utf-8'))
    check_error = check_headline(j, stand_comand)
    if check_error != True:
        return check_error
    list_tables = j['tables']
    ch_table = check_table(j, list_tables)
    if ch_table == False:
        return 'Check table False'

    for name_table in list_tables:
        list_column = my_db.get_name_column(name_table, format_result='names')
        list_rows = list_tables[name_table]
        for row in list_rows:
            name_column = row['name_column']
            if name_column in list_column:
                my_db.del_column(name_table, name_column)
            else:
                return f'невозможно удалить колонку {name_column}'

    return 'ok'


@app.route('/furniture/del_associated_file_<name_db>/', methods=['POST'])
def del_associated_file(name_db):
    stand_comand = {'comand': 1110,
                    'user': 'admin',
                    'db_comand': 1,
                    }
    my_db = FurnitureDatabase(name_db=name_db)
    a = request.data
    j = json.loads(a.decode('utf-8'))
    check_error = full_check(json_data=j, stand_comand=stand_comand, name_db=name_db)
    if check_error != 'ok':
        return check_error
    names_column_file = j['names_column_file']
    list_tables = j['tables']
    for name_table in list_tables:
        list_rows = list_tables[name_table]
        for row in list_rows:
            dir_associated_file = my_db.open_dir_associated_file(row, name_table, names_column_file[name_table])
            os.remove(dir_associated_file)

    return 'ok'


@app.route('/furniture/edit_associated_file_<name_db>/', methods=['POST'])
def edit_associated_file(name_db):
    stand_comand = {'comand': 1110,
                    'user': 'admin',
                    'db_comand': 1,
                    }
    my_db = FurnitureDatabase(name_db=name_db)
    a = request.data
    j = json.loads(a.decode('utf-8'))
    check_error = full_check(json_data=j, stand_comand=stand_comand, name_db=name_db)
    if check_error != 'ok':
        return check_error
    names_column_file = j['names_column_file']
    list_tables = j['tables']
    for name_table in list_tables:
        list_rows = list_tables[name_table]
        for row in list_rows:
            dir_associated_file = my_db.open_dir_associated_file(row, name_table, names_column_file[name_table])
            with open(dir_associated_file, "wb") as outfile:
                # "wb" argument opens the file in binary mode
                pickle.dump(row[names_column_file[name_table]], outfile)

    return 'ok'


@app.route('/furniture/add_row_<name_db>/', methods=['POST'])
def add_row_tables(name_db):
    stand_comand = {'comand': 1110,
                    'user': 'admin',
                    'db_comand': 1,
                    }
    my_db = FurnitureDatabase(name_db=name_db)
    a = request.data
    j = json.loads(a.decode('utf-8'))
    check_error = full_check(json_data=j, stand_comand=stand_comand, name_db=name_db)
    if check_error != 'ok':
        return check_error
    list_tables = j['tables']
    for name_table in list_tables:
        list_rows = list_tables[name_table]
        for row in list_rows:
            title = list(row.keys())
            value = [row[i] for i in title]
            my_db.add_row(name_table, tuple(title), tuple(value))
    return 'ok'


@app.route('/furniture/add_column_<name_db>/', methods=['POST'])
def add_column_table(name_db):
    stand_comand = {'comand': 2569,
                    'user': 'admin',
                    'db_comand': 1,
                    }

    my_db = FurnitureDatabase(name_db=name_db)
    a = request.data
    j = json.loads(a.decode('utf-8'))
    check_error = check_headline(j, stand_comand)
    if check_error != True:
        return check_error
    list_tables = j['tables']
    ch_table = check_table(j, list_tables)
    if ch_table == False:
        return 'Check table False'
    for name_table in list_tables:
        list_rows = list_tables[name_table]
        for row in list_rows:
            name_column = row['name_column']
            type_data = row['type_data']
            my_db.add_column(name_table, name_column, type_data)
    return 'ok'


#############доработать(не понятно как собирать если по result["tables"] если по одной таблице идет несколько условий)
@app.route('/furniture/get_row_<name_db>_<column_condition>/', methods=['POST'])
def get_row_tables(name_db, column_condition):
    stand_comand = {'comand': 2001,
                    'user': 'admin',
                    'db_comand': 1,
                    }
    result = {"tables": {}}
    my_db = FurnitureDatabase(name_db=name_db)
    a = request.data
    j = json.loads(a.decode('utf-8'))
    check_error = full_check(json_data=j, stand_comand=stand_comand, name_db=name_db)
    if check_error != 'ok':
        return check_error
    list_tables = j['tables']
    for name_table in list_tables:
        list_rows = list_tables[name_table]
        result["tables"][name_table] = []
        for row in list_rows:
            result_row = my_db.get_row(name_db, name_table, column_condition, row[column_condition])
            result["tables"][name_table] = result_row


@app.route('/furniture/get_databases/', methods=['POST'])
def get_databases():
    stand_comand = {'comand': 1110,
                    'user': 'admin',
                    'db_comand': 1,
                    }
    a = request.data
    j = json.loads(a.decode('utf-8'))
    check_error = check_headline(j, stand_comand)
    if check_error != True:
        return check_error
    list_databases = database.get_databases()

    json_send = json.dumps(list_databases)
    return json_send


def is_all_employers_rated(db, prev_date: dt, id_department):
    count_assessments = db.mysql_custom_command(
        f'''SELECT COUNT(*) FROM personal_assessment 
                INNER JOIN personal ON personal_assessment.id_name_personal=personal.id_personal
                 WHERE personal.id_department={id_department} AND personal_assessment.date = '{prev_date}' ''')[0][0]
    count_personal = db.mysql_custom_command(f'''SELECT COUNT(*) FROM personal 
                                                WHERE id_department = {id_department} ''')[0][0]
    count_criteria = db.mysql_custom_command("SELECT COUNT(*) FROM conf_criterion")[0][0]

    return count_personal * count_criteria == count_assessments


def is_date_avaible(db, date):
    count_exist_rows = db.mysql_custom_command(f'''SELECT COUNT(date) FROM personal_assessment 
                                                       WHERE date = '{date}' ''')[0][0]
    count_rows_next_dates = db.mysql_custom_command(f'''SELECT COUNT(date) FROM personal_assessment
                                                   WHERE date > '{date}' ''')[0][0]
    return not (count_exist_rows == 0 and count_rows_next_dates > 0)


@app.route('/furniture/get_persons_for_assessment/', methods=['POST'])
def get_persons_for_assessment():
    db = database.FurnitureDatabase("new_factory_6")
    data = json.loads(request.data.decode('utf-8'))
    department = data["tables"]["department"]
    id_department = db.mysql_custom_command(f'''SELECT id_department 
                                                FROM department WHERE title = '{department}' ''')[0][0]

    cur_date = dt(*reversed(list(map(int, data['date'].split('-')))))
    # print('cur_date', cur_date)
    if not is_date_avaible(db, cur_date):
        result = {"error": "Bad date"}
        json_send = json.dumps(result)
        return json_send

    prev_date = db.mysql_custom_command(f'''SELECT date FROM personal_assessment 
                                            WHERE date < '{cur_date}' ORDER BY date DESC LIMIT 1 ''')
    print('prev_date', prev_date)

    if len(prev_date) != 0 and not is_all_employers_rated(db, prev_date[0][0], id_department):
        result = {"error": "Не все сотрудники были оценены в прошлый раз"}
        json_send = json.dumps(result)
        return json_send

    # pprint(data)
    assessment_list = {"tables": {"personal": []}}
    persons = db.mysql_custom_command(f'''SELECT id_personal, name, dir_avatar FROM personal 
                                        WHERE id_department = (SELECT id_department FROM department
                                                                                    WHERE title = '{department}')''')
    # print(persons)
    for i in range(len(persons)):
        assessment_list["tables"]["personal"].append({
            "name": persons[i][1],
            "id_person": persons[i][0],
            "id_assessment": {},
            "assessment": {},
            "comments": {},
            "edit_data": {},
            "add_data": {},
            "average_value": {}
        })
        person = assessment_list["tables"]["personal"][i]
        for criterion in db.mysql_custom_command("SELECT id_conf_criterion, title_criterion FROM conf_criterion"):
            person["id_assessment"][criterion[1]] = [0, 0]
            exist_assessment = db.mysql_custom_command(f'''SELECT * FROM personal_assessment
                                                            WHERE date = '{cur_date}' AND id_name_personal = '{persons[i][0]}' 
                                                            AND id_criterion = {criterion[0]} ''')
            # print('exist_assessment', exist_assessment)
            person["id_assessment"][criterion[1]][0] = exist_assessment[0][0] if len(exist_assessment) != 0 else 0
            person["assessment"][criterion[1]] = exist_assessment[0][9] if len(exist_assessment) != 0 else 0
            person["comments"][criterion[1]] = exist_assessment[0][4] if len(exist_assessment) != 0 else ""
            person["add_data"][criterion[1]] = "admin" if len(exist_assessment) != 0 else ""
            person["edit_data"][criterion[1]] = "admin" if len(exist_assessment) != 0 else ""
            person["average_value"][criterion[1]] = db.get_average_value(cur_date, data["period_mean"],
                                                                         person["id_person"], criterion[0])
        # with open(persons[i][2], "rb") as open_file:
        #     assessment_list["tables"]["personal"][i]["avatar"] = pickle.load(open_file)
    # pprint(assessment_list)
    return assessment_list


@app.route('/furniture/send_assessment/', methods=['POST'])
def send_assessments():
    # print(type(request.data)) # <class 'bytes'>
    data = json.loads(request.data.decode('utf-8'))
    db = database.FurnitureDatabase("new_factory_6")
    for person in data['tables']['personal']:
        for criterion, value in dict(person['id_assessment']).items():
            id_row, command = value
            if command == 0:  # ничего не делаем
                pass
            elif command == 1:
                if id_row == 0:  # добавляем новую оценку
                    # print('add')
                    id_criterion = db.mysql_custom_command(
                        f"SELECT id_conf_criterion FROM conf_criterion WHERE title_criterion = '{criterion}'")[0][0]
                    db.add_row_v2('personal_assessment',
                                  ('date', 'id_name_personal', 'id_title_project', 'comments',
                                   'id_criterion', 'id_drop_criterion', 'user_add', 'user_edit', 'assessment'),
                                  (dt.today(), person['id_person'], 'NULL', person['comments'][criterion],
                                   id_criterion, 'NULL', 'admin', 'NULL', person['assessment'][criterion]
                                   ))
                    #  таблицы проекты и персонал будут связаны через битрикс
                else:  # редактируем
                    # print('edit')
                    db.mysql_custom_command(f'''UPDATE personal_assessment
                                                    SET
                                                        assessment = {person['assessment'][criterion]},
                                                        comments = '{person['comments'][criterion]}',
                                                        user_edit = '{person['edit_data'][criterion]}'
                                                    WHERE id_assessment = {id_row};''', 0)

                    print(db.mysql_custom_command(
                        f'''SELECT * FROM personal_assessment WHERE id_assessment = {id_row}'''))

            elif command == -1:  # удаляем
                print('delete')
                db.mysql_custom_command(f"DELETE FROM personal_assessment WHERE id_assessment = {id_row}", 0)

    return "200"


# list_tables = db.get_tables()
# stand_comand={ 'comand': 1000,
#                 'user': 'admin',
#                 'db_comand': 1}
# if not check_headline(data, stand_comand=stand_comand):
#         raise Exception('Incorrect entry of header keys')
# set_unk_tables=check_table(data, list_tables)
# if  set_unk_tables!=None:
#     raise Exception(f'unknown table named{set_unk_tables}')
#     pass

#     return "get_data_personal"
# @app.route('/personal', methods=['GET'])
# def get_data_personal():
#     return "get_data_personal"
#
# @app.route('/personal', methods=['POST'])
# def add_data_personal():
#
#     return db.add_new_personal(name, adress, number, certification)
#
# @app.route('/personal', methods=['GET'])
# def get_alldata_personal():
#     return "get_data_personal"

"""**********Check value***************"""
# for name_table in list_tables:
#     if '#' in name_table:
#         sep_name, limit = name_table.split('#')
#         count = db.count_row(sep_name)
#         if count >= limit:
#             return 'jj'
#
#     list_rows = list_tables[name_table]
#     for row in list_rows:
#         title = list(row.keys())[0]
#         value = row[title]
#         check_value = my_db.check_value(name_table, title, value)
#         if check_value[-1] == '$':
#             return f'department named {check_value[:-1]} already exists'
#         elif check_value[-1] == '%':
#             return f'department named {check_value[:-1]} already exists'
"""***********************************************"""
if __name__ == '__main__':
    # app.debug=True
    app.run(host="0.0.0.0", port=5000)
