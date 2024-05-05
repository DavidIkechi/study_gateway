# response handler code.
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder

# for errorsS
class Exceptions:
    def __init__(self):
        pass
    
    def generic_error(self, status_code, detail="An error occurred", data=[]):
        return JSONResponse(
            status_code= status_code,
            content=jsonable_encoder({"detail": detail,
                                      "data": data,
                                      "status": 0}),
        )
    
    def bad_request_error(self, detail="An error occurred", data = []):
        return self.generic_error(status_code=400, detail=detail, data=data)
    
    def not_found_error(self, detail="Not seen", data=[]):
        return self.generic_error(404, detail=detail, data=data)
        
    def forbidden_error(self, detail="password change is required", data=[]):
        return self.generic_error(status_code=403, detail=detail, data=data)    
    
    def unauthorized_error(self, detail="Client is Unanthorized"):
        raise HTTPException(status_code = 401, detail=detail)
         
    def server_error(self, detail = ""):
        return self.generic_error(status_code=500, detail=detail)

# for success message.       
class Success:
    def __init__(self):
        pass
    
    def success_message(self, data=[], detail="Success", status_code=200):
        return JSONResponse(
            status_code= status_code,
            content=jsonable_encoder({"detail": detail,
                                      "data": data,
                                      "status": 1}),
        )
    
    
error_response = Exceptions()
success_response = Success()