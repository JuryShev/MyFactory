

def eng_to_rus_column(config, table_name, name_column, lang="en_ru"):
    column_rus = config[lang][table_name]
    for id, name in enumerate(name_column):
        if " as " in name:
            name = name.split(" as ")[-1]
        elif '.' in name:
            name = name.split(".")[-1]
        try:
            name_column[id] = column_rus[name]
        except KeyError:
            continue


def eng_to_rus_table(config, table_name, lang="en_ru"):
    column_rus = config[lang][table_name]
    return column_rus[table_name]

