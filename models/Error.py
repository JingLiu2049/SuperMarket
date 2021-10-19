class CustError(Exception):
    def __init__(self, msg: object='') -> None:
        super().__init__(msg)
        self.msg = msg
    def __str__(self):
        return self.msg


class ItemError(Exception):
    def __init__(self, msg: object='') -> None:
        super().__init__(msg)
        self.msg = msg
    def __str__(self):
        return self.msg
        
class CartError(Exception):
    def __init__(self, msg: object='') -> None:
        super().__init__(msg)
        self.msg = msg
    def __str__(self):
        return self.msg

class ControllerError(Exception):
    def __init__(self, msg: object='') -> None:
        super().__init__(msg)
        self.msg = msg
    def __str__(self):
        return self.msg

