class HeaderAuth(object):

    def __init__(self, header, user):
        self.header = header
        self.user = user

    def authorize(self):

        contentType = header["Content-Type"]