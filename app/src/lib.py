import clickhouse_connect
from os import getenv

db_admin_password = getenv("ROOT_PASSWORD")

def db_connect(namedb, namespace):
    host_db = namedb + "." + namespace
    client = clickhouse_connect.get_client(host=host_db,
                                       user='default',
                                       password=db_admin_password,
                                       port=8123,
                                       database='default',
                                       connect_timeout=15)
    return client

def list_users(namedb, namespace, user_db):
    client = db_connect(namedb, namespace)
    query = 'SHOW USERS'
    result = client.command(query)
    result_user = result.find(user_db)
    return result_user

# TODO: обрааботка ошибок

def create_user_db(namedb, namespace, user_db, password_user):
    client = db_connect(namedb, namespace)

    check_exists_user = list_users(namedb, namespace, user_db)
    if check_exists_user != -1:
        message = f"Пользователь {user_db} уже есть в {namedb}"
    else:
        query = 'CREATE USER ' + user_db + ' HOST ANY IDENTIFIED WITH sha256_password BY ' + '\'' + password_user + '\''
        query_1 = 'GRANT SELECT,SHOW,OPTIMIZE ON default.* TO ' + user_db + ' WITH GRANT OPTION' 
        client.command(query)
        client.command(query_1)
        message = f"Пользователь {user_db} создан в {namedb}"

    return message
 
def update_password_user_db(namedb, namespace, user_db, password_user):
    client = db_connect(namedb, namespace)
    
    check_exists_user = list_users(namedb, namespace, user_db)

    if check_exists_user != -1:
        query = 'ALTER USER ' + user_db + ' SET PASSWORD ' + '\'' + password_user + '\''
        client.command(query)
        message = f"У Пользователя {user_db} изменен пароль."
    else:
        message = f"Такого пользователя {user_db} уже нет в БД {namedb}, пожайлуста создайте его"

    return message

def delete_user_db(namedb, namespace, user_db):
    client = db_connect(namedb, namespace)
    
    check_exists_user = list_users(namedb, namespace, user_db)

    if check_exists_user != -1:
        query = 'DROP USER ' + user_db
        client.command(query)
        message = f"Пользователь {user_db} удален в {namedb}"
    else:
        message = f"Такого пользователя {user_db} уже нет в БД {namedb}"
    return message