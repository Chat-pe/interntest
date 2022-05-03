from flask_restful import Resource
from flask_pydantic import validate
from flask import make_response
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token

from api.models.register import Register, Verify
from api.models.requests import ResponseModel,ErrorResponseModel
from api.utils.send_otp import send_otp, verify_otp

import json


class Verification(Resource):

    @validate()
    def get(self, query: Register):
        query = json.loads(query.json())
        print(query)
        if query.get("phone"):
            if send_otp(query.get("phone"), query.get("signature")):
                
                return make_response(ResponseModel({"status":"Ok" },"Phone number verified"), 200)
            else:
                return make_response(ErrorResponseModel({"status":"Error"},400,"OTP not sent"), 400)
        return {"message": "success"}

    @validate()
    def post(self, body: Verify):
        body = json.loads(body.json())
        print(body)
        if body.get("phone") and body.get("code"):
            if verify_otp(body.get("phone"), body.get("code")):
                access_token = create_access_token(identity=body.get("phone"),expires_delta=False)
                return make_response(ResponseModel({"status":"Ok","token":access_token},"OTP verified"), 200)
            else:
                return make_response(ErrorResponseModel({"status":"Error"},400,"OTP not verified"), 400)
        return {"message": "success"}