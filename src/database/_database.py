from ._engine import async_session_maker


class Database:
    def __init__(self):
        self.session_maker = async_session_maker
