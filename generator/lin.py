class Lin(object):
    """
    a lin object relate to a *.lin file now
    and the content of the file should have and only have 1 line.
    """

    def __init__(self, file_url):
        self.file_url = file_url

    @property
    def content(self):
        """
        :return: a string including file content
        """
        if self.__content:
            return self.__content
        else:
            # TODO
            pass
        pass

    def init_data(self):
        """
        initiate data from a string,and set object's attr
        :return: void
        """
