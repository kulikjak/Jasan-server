class Model(object):

    def __init__(self, db):
        from model.polls import Polls
        from model.responses import Responses

        self.polls = Polls(model=self, db=db)
        self.responses = Responses(model=self, db=db)
