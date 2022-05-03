from flask_restful import Resource
from flask_pydantic import validate
from flask import make_response, request
from flask_jwt_extended import jwt_required, get_jwt_identity


from api.models.task import Task, UpdateTask, Phone
from api.models.requests import ResponseModel,ErrorResponseModel
from api.database import pdb
from api.utils import remove_null_keys

import json, random, string, re



class CRUDTask(Resource):

    @jwt_required()
    @validate()
    def post(self, body: Task):
        body = json.loads(body.json())
        print(body)
        if body.get('phone') == get_jwt_identity():
            uniquelink = generate_unique_link_from_name(body.get("name"))
            body["uniquelink"] = uniquelink
            new_task = pdb["task"].insert_one(body)
            created_task = pdb["task"].find_one({"_id": new_task.inserted_id})
            created_task.pop("id")
            created_task.pop("_id")
            return make_response({"status": "success", "data": created_task}, 201)
        return make_response({"status": "error", "message": "You are not authorized to create a task"}, 401)


    @jwt_required()
    @validate()
    def get(self, query: Phone):
        query = json.loads(query.json())
        task = pdb["task"].find_one({"phone": query.get("phone")})
        if task:
            task.pop("_id")
            task.pop("id")
            return make_response(ResponseModel({"status":"Ok", "task": task },"Task found"), 200)
        return make_response(ErrorResponseModel({"status":"Error"},404,"Task not found"), 404)

    @jwt_required()
    @validate()
    def put(self, body: UpdateTask):
        body = remove_null_keys(json.loads(body.json()))
        task = pdb["task"].find_one({"uniquelink": body.get("uniquelink")})
        if task:
            if task.get("phone") == get_jwt_identity():
                task.pop("_id")
                task.update(body)
                pdb["task"].update_one({"phone": body.get("phone")}, {"$set": task})
                return make_response(ResponseModel({"status":"Ok", "task": task },"Task updated"), 200)
            return make_response(ErrorResponseModel({"status":"Error"},401,"You are not authorized to update this task"), 401)
        return make_response(ErrorResponseModel({"status":"Error"},404,"Task not found"), 404)






def generate_unique_link_from_name(name):
    
    p = re.compile("[^a-zA-Z0-9 -]")
    ul = "-".join(p.sub(" ",name.lower()).split())
    if pdb["tasks"].count_documents({"uniquelink":ul}):
        str = string.ascii_uppercase
        flux = ''.join(random.choice(str) for i in range(5))
        ul = ul + "-" + flux
    return ul