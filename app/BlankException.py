class BlankException(Exception):
    def __init__(self, message, code=400):
        self.message = str(message).replace('"',"'")
        self.code = code
        super().__init__(self.message)

