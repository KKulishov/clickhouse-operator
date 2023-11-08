import kopf
from src.lib import create_user_db, delete_user_db, update_password_user_db

RESOURCE_GROUP = "devops.org"
RESOURCE_VERSION = "v1"
RESOURCE_TYPE = "clickhouse-devops"

# TODO: add variables all for type/user/namedb/password

@kopf.on.create(RESOURCE_GROUP, RESOURCE_VERSION, RESOURCE_TYPE)
def create_fn(spec, logger, **kwargs):
    type = spec.get('namespace', None)
    user = spec.get('User', None)
    namedb = spec.get('namedb', None)
    password = spec.get('password', None)

    create_users = create_user_db(namedb, type, user, password)
    logger.info(create_users)
    return create_users

#  TODO: update password 
@kopf.on.update(RESOURCE_GROUP, RESOURCE_VERSION, RESOURCE_TYPE)
def update_password(spec, logger, **kwargs):
    type = spec.get('namespace', None)
    user = spec.get('User', None)
    namedb = spec.get('namedb', None)
    password = spec.get('password', None)
    update_password = update_password_user_db(namedb, type, user, password)
    
    if type is not None:
        print(f"type in spec: {type}")
    if user is not None:
        print(f"user in spec: {user}")
    else:
        print("No 'spec' field in the Custom Resource.")
    logger.info(update_password)
    return update_password

@kopf.on.delete(RESOURCE_GROUP, RESOURCE_VERSION, RESOURCE_TYPE)
def delete_custom_resource(body, spec, logger, **kwargs):
    type = spec.get('namespace', None)
    user = spec.get('User', None)
    namedb = spec.get('namedb', None)
    delete_user = delete_user_db(namedb, type, user)
    logger.info(delete_user)
    return delete_user