class Model(object):

    def __init__(self, db):
        from model.feedbacks import Feedbacks
        from model.screams import Screams

        self.screams = Screams(model=self, db=db)
        self.feedbacks = Feedbacks(model=self, db=db)
