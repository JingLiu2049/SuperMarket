class MyResponse:
    def __init__(self,status:int,msg:str='',data:object = '') -> None:
        self.status = status
        self.data = data
        self.msg = msg