

class QsonException(Exception):
    def __init__(self, msg):
        self.message = msg

    def __repr__(self):
        return "<QsonException '{}'>".format(self.message)


class ParseError(QsonException):
    def __init__(self, msg):
        super().__init__(msg)

    def __repr__(self):
        return "<ParseError '{}'>".format(self.message)

