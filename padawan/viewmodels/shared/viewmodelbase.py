import flask


class ViewModelBase:
    def __init__(self):
        self.request: flask.Request = flask.request
        self.grogu = "Baby Yoda"
        # TODO manage authenticated user
        # self.__user: Optional[User] = None
        # self.__user_set: bool = False
        # self.request_dict = request_dict.create('')
        #
        # self.error: Optional[str] = None
        # self.user_id: Optional[int] = cookie_auth.get_user_id_via_auth_cookie(self.request)

    def to_dict(self):
        data = dict(self.__dict__)
        data['user'] = self.user
        return data

    @property
    def user(self):
        # TODO return User from DB or None if anonymous
        return None
