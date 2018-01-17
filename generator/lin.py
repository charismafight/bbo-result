class Lin(object):
    """
    a lin object relate to a *.lin file now
    and the content of the file should have and only have 1 line.
    """

    def __init__(self, file_url):
        self.file_url = file_url
        self.__content = None
        self.fetch_retry_times = 0

    @property
    def content(self):
        """
        :return: a string including file content
        """
        return self.__content

    @content.setter
    def content(self, value):
        self.__content = value

    def init_data(self):
        """
        initiate data from a string,and set object's attr
        :return: void
        """
        pass

    def fetch_file(self, conn):
        """
        fetch file by url
        eg:http://www.bridgebase.com/myhands/fetchlin.php?id=1535437396&when_played=1514118898
        :return: void
        """
        req = conn.get(self.file_url, verify=False, stream=True)
        if req.status_code != 200 and self.fetch_retry_times <= 10:
            print(
                'error when getting ', self.file_url, ' http_error_code:', str(req.status_code),
                str(self.fetch_retry_times) + ',retries')
            self.fetch_retry_times += 1
            self.fetch_file(conn)
            return
        print(req.content)
