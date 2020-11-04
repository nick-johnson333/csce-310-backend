class DatabaseException(Exception):
    code = 400
    def __init__(self,message, error_type=None):
        self.message = str(message).replace('"',"'")
        if error_type is None:
            self.error_type = type(message).__name__
        else:
            self.error_type = error_type
        super().__init__(self.message)
