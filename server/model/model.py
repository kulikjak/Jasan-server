class Model(object):

    def __init__(self, db):
        from server.model.feedbacks import Feedbacks
        from server.model.screams import Screams
        from server.model.users import Users

        self.feedbacks = Feedbacks(model=self, db=db)
        self.screams = Screams(model=self, db=db)
        self.users = Users(model=self, db=db)
