import clickhouse_connect
from os import getenv

db_admin_password = getenv("ROOT_PASSWORD")

def db_connect(namedb, namespace):
    """
    Подключение к БД clickhouse
    """
    host_db = namedb + "." + namespace
    client = clickhouse_connect.get_client(host=host_db,
                                       user='default',
                                       password=db_admin_password,
                                       port=8123,
                                       database='default',
                                       connect_timeout=15)
    return client

def list_users(namedb, namespace, user_db):
    """
    Поиск пользователя из arg user_db в заданной БД
    """
    query = 'SHOW USERS'
    with db_connect(namedb, namespace) as client: 
        result = client.command(query)
    result_user = result.find(user_db)
    return result_user

# TODO: обрааботка ошибок

def create_user_db(namedb, namespace, user_db, password_user):
    """
    Создания пользователя из arg user_db в заданной БД
    """
    check_exists_user = list_users(namedb, namespace, user_db)
    if check_exists_user != -1:
        message = f"Пользователь {user_db} уже есть в {namedb}"
    else:
        parameters = {'user': user_db, 'password': password_user}
        query = 'CREATE USER %(user)s HOST ANY IDENTIFIED WITH sha256_password BY %(password)s'
        query_1 = 'GRANT SELECT,SHOW,OPTIMIZE ON default.* TO %(user)s WITH GRANT OPTION'
        with db_connect(namedb, namespace) as client: 
            client.query(query, parameters=parameters)
            client.query(query_1, parameters=parameters)
        message = f"Пользователь {user_db} создан в {namedb}"

    return message
 
def update_password_user_db(namedb, namespace, user_db, password_user):
    """
    Обновления пароля пользователя из arg user_db и password_user в заданной БД
    """
    check_exists_user = list_users(namedb, namespace, user_db)

    if check_exists_user != -1:
        parameters = {'user': user_db, 'password': password_user}
        query = 'ALTER USER %(user)s IDENTIFIED BY %(password)s'
        with db_connect(namedb, namespace) as client:
            client.query(query, parameters=parameters)
        message = f"У Пользователя {user_db} изменен пароль."
    else:
        message = f"Такого пользователя {user_db} уже нет в БД {namedb}, пожайлуста создайте его"

    return message

def delete_user_db(namedb, namespace, user_db):
    """
    Удаление пользователя из БД
    """
    client = db_connect(namedb, namespace)
    
    check_exists_user = list_users(namedb, namespace, user_db)

    if check_exists_user != -1:
        parameters = {'user': user_db}
        query = 'DROP USER %(user)s'
        with db_connect(namedb, namespace) as client:
            client.query(query, parameters=parameters)
        message = f"Пользователь {user_db} удален в {namedb}"
    else:
        message = f"Такого пользователя {user_db} уже нет в БД {namedb}"
    return message