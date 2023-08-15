from .json_f import load_config


def where_(query_builder):
    def wrapper(*args, **kwargs):
        operations = {"<", ">", "=", "<=", ">=", "!=", "BETWEEN", "LIKE", "IN"}
        ind_operation = []
        json_where={}
        for f in kwargs["where"].keys():
            split_req = kwargs["where"][f].split(" ")
            include_operations = operations & set(split_req)
            for ch in include_operations:
                ind_operation+=[i for i, ltr in enumerate(split_req) if ltr == ch]
            condition=''.join(split_req[i] for i in ind_operation )
            ind_operation.append(min(ind_operation)+1)
            value=[a for i, a in enumerate(split_req) if i not in ind_operation]
            json_where[f] = {"condition": condition,
                             "value": value}
        kwargs["where"]=json_where

        templ_load_table = query_builder(*args, **kwargs)
        return templ_load_table

    return wrapper


@where_
def build_command_get_table(name_table, columns, join, where, input_lang, output_lang, distinct=False):
    templ_load_table = load_config("./json_data/config_load/load_table.json")
    templ_load_table["columns"] = columns
    templ_load_table["JOIN"] = join
    templ_load_table["WHERE"] = where
    templ_load_table["input_lang"] = input_lang
    templ_load_table["output_lang"] = output_lang
    templ_load_table["distinct"] = distinct
    return templ_load_table



