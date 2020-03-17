
class ResponseJSON(object):

    def __init__(self, data, status):
        self.data = data
        self.status = status



    def getResponseJSON(self):

        if self.status:
            self.code = "0"
        else:
            self.code = "404"

        return {'status':self.status,'code':self.code,'data':self.data}

class Error_ResponseJSON(object):

    def __init__(self, message, status):
        self.message = message
        self.status = status



    def getResponseJSON(self):

        if self.status:
            self.code = "0"
        else:
            self.code = "404"

        return {'status':self.status,'code':self.code,'data':None,"message":self.message}