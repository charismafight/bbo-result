class Lin(object):
    """
    a lin object relate to a *.lin file now
    and the content of the file should have and only have 1 line.
    """

    # proxies = {
    #     "http": "http://221.202.248.52:80",
    #     "http": "http://1.0.189.67：8080",
    #     "http": "http://1.175.137.45:3128",
    #     "http": "http://1.179.146.153:8080",
    #     "http": "http://1.196.161.162:9999",
    #     "http": "http://1.25.234.114:3128",
    #     "http": "http://101.109.198.183:3128",
    #     "http": "http://101.109.252.92:8081",
    #     "http": "http://101.128.68.113:8080",
    #     "http": "http://101.128.68.123:8080",
    #     "http": "http://101.128.68.137:8080",
    #     "http": "http://101.200.89.170:8888",
    #     "http": "http://101.201.79.172:808",
    #     "http": "http://101.248.64.68:80",
    #     "http": "http://101.248.64.68:8080",
    #     "http": "http://101.255.51.222:8080",
    #     "http": "http://101.37.79.125:3128",
    #     "http": "http://101.4.136.34:8080",
    #     "http": "http://101.4.136.34:81",
    #     "http": "http://101.51.123.240:8080",
    # }

    def __init__(self, file_url, result):
        self.file_url = file_url
        self.__content = None
        self._contact = None
        self.fetch_retry_times = 0
        self.fetch_status = 0
        self._result = result

    @property
    def result(self):
        return self._result

    @result.setter
    def result(self, value):
        self._result = value

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
        data = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
        }

        req = conn.get(self.file_url, data=data, verify=False, stream=True)
        if req.status_code != 200:
            print(
                'error when getting ', self.file_url, ' http_error_code:', str(req.status_code),
                str(self.fetch_retry_times) + ',retries')

            if self.fetch_retry_times >= 10:
                print("download failed 10 times")
                # fail
                self.fetch_status = 2
                return
            self.fetch_retry_times += 1
            self.fetch_file(conn)
            return
        # ok
        self.fetch_status = 1
        self.content = req.content.decode()
        print(self.file_url + ' fetched.')

    def __str__(self):
        return self.content
