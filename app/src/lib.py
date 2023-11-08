import clickhouse_connect
from os import getenv

db_admin_password = getenv("ROOT_PASSWORD")

# TODO: вынести подключение clickhouse в отдельную func
# TODO: обрааботка ошибок

def create_user_db(namedb, namespace, user_db, password_user):
    
    host_db = namedb + "." + namespace

    client = clickhouse_connect.get_client(host=host_db,
                                       user='default',
                                       password=db_admin_password,
                                       port=8123,
                                       database='default',
                                       connect_timeout=15)
    
    # TODO: check user exists 

    query = 'CREATE USER ' + user_db + ' HOST ANY IDENTIFIED WITH sha256_password BY ' + '\'' + password_user + '\''
    query_1 = 'GRANT SELECT,SHOW,OPTIMIZE ON default.* TO ' + user_db + ' WITH GRANT OPTION' 
    client.command(query)
    client.command(query_1)

    message = f"Пользователь {user_db} создан в {namedb}"

    return message

# TODO: add func update CRD if password changes     
def update_password_user_db(namedb, namespace, user_db, password_user):
    return None

def delete_user_db(namedb, namespace, user_db):
    host_db = namedb + "." + namespace
    client = clickhouse_connect.get_client(host=host_db,
                                       user='default',
                                       password=db_admin_password,
                                       port=8123,
                                       database='default',
                                       connect_timeout=15)

    # TODO: check user exists                                    
    
    query = 'DROP USER ' + user_db
    client.command(query)
    message = f"Пользователь {user_db} удален в {namedb}"
    return message