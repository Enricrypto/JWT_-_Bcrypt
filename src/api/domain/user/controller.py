import api.domain.user.repository as Repository
import bcrypt
from flask_jwt_extended import create_access_token

def verify_user_email_and_pass(user):
    if user['email'] is None or user['email'] == "":
        return {"msg": "Bad request", "error": True, "status": 400}
    if user['password'] is None or user['password'] == "":
        return {"msg": "Bad request", "error": True, "status": 400}
    return user

def create_user(new_user):
    
    user_verify = verify_user_email_and_pass(new_user)
    if user_verify.get('error') is not None:
        return user_verify 

    hashed = bcrypt.hashpw(new_user['password'].encode(), bcrypt.gensalt(14))

    return Repository.create_user(new_user['email'], hashed.decode()) 

def login(body): 
    user_verify = verify_user_email_and_pass(body)
    if user_verify.get('error') is not None:
        return user_verify 

    user = Repository.get_user_by_email(body['email'])

    if user is None:
        return {"msg": "User not found", "error": True, "status": 404}

    if bcrypt.checkpw(body['password'].encode(), user.password.encode()):
        new_token = create_access_token(identity=user.serialize())
        return {"token": new_token}

    return {"msg": "User not found", "error": True, "status": 404}

def get_user(user):
    user = Repository.get_user_by_email(user['email'])
    if user is None:
        return {"msg": "User not found", "error": True, "status": 404}
    return user
