from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

def success_response(message:str = "success", data = None):
    content = {
        "code": 200,
        "message": message,
        "data": data
    }
    # 目标：把任何的FastAPI、Pydantic、ORM对象都要正常响应→code、message、data
    return JSONResponse(content=jsonable_encoder(content))

def fail_response(code=500, msg="error", data=None):
    content = {
        "code": code,
        "message": msg,
        "data": data
    }
    return JSONResponse(content=jsonable_encoder(content))
