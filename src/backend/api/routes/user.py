from flask_restful import Resource
from flask_pydantic import validate
from flask import make_response, request
from flask_jwt_extended import jwt_required, get_jwt_identity


from api.models.user import User,  Phone
from api.models.requests import ResponseModel,ErrorResponseModel
from api.database import pdb
from api.utils import remove_null_keys

import json, random, string, re


class CRUDUser(Resource):

    @jwt_required()
    @validate()
    def post(self, body: User):
        body = json.loads(body.json())
        print(body)
        if body.get('phone') == get_jwt_identity():
            username = generate_unique_link_from_name(body.get("name"))
            body["username"] = username
            new_user = pdb["users"].insert_one(body)
            created_user = pdb["users"].find_one({"_id": new_user.inserted_id})
            created_user.pop("id")
            created_user.pop("_id")
            return make_response({"status": "success", "data": created_user}, 201)
        return make_response({"status": "error", "message": "You are not authorized to create a user"}, 401)

    @jwt_required()
    @validate()
    def get(self, query: Phone):
        # print(request.args)
        query = json.loads(query.json())
        user = pdb["users"].find_one({"phone": query.get("phone")})
        if user:
            user.pop("_id")
            user.pop("id")
            if query.get("category"):
                print("not all")
                user = user.get(query.get("category","not found"))
            print(user)
            return make_response(ResponseModel({"status":"Ok", "user": user },"User found"), 200)
        return make_response(ErrorResponseModel({"status":"Error"},404,"User not found"), 404)




def generate_unique_link_from_name(name):
    
    p = re.compile("[^a-zA-Z0-9 -]")
    ul = "-".join(p.sub(" ",name.lower()).split())
    if pdb["users"].count_documents({"username":ul}):
        str = string.ascii_uppercase
        flux = ''.join(random.choice(str) for i in range(5))
        ul = ul + "-" + flux
    return ul