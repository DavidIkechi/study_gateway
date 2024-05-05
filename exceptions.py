from fastapi import HTTPException

class BadExceptions(HTTPException):
    def __init__(self, detail: str, status_code: int = 400, data=[]):
        super().__init__(status_code=status_code, detail=detail)
        self.data = data

class NotFoundException(HTTPException):
    def __init__(self, detail: str, status_code: int = 404, data=[]):
        super().__init__(status_code=status_code, detail=detail)
        self.data = data

class NotAuthorizedException(HTTPException):
    def __init__(self, detail: str, status_code: int = 401, data=[]):
        super().__init__(status_code=status_code, detail=detail)
        self.data = data
        
class ForbiddenException(HTTPException):
    def __init__(self, detail: str, status_code: int = 403, data=[]):
        super().__init__(status_code=status_code, detail=detail)
        self.data = data

class ServerErrorException(HTTPException):
    def __init__(self, detail: str, status_code: int = 500):
        super().__init__(status_code=status_code, detail=detail)