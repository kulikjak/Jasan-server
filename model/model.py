class Model(object):

    def __init__(self, db):
        from model.feedbacks import Feedbacks
        from model.polls import Polls
        from model.responses import Responses
        from model.screams import Screams

        self.polls = Polls(model=self, db=db)
        self.responses = Responses(model=self, db=db)
        self.screams = Screams(model=self, db=db)
        self.feedbacks = Feedbacks(model=self, db=db)
