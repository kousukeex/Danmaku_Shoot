class ScoreData(object):
    score = 0
    @classmethod
    def add_score(cls,score):
        cls.score += score