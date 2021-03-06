from app import db
from flask.ext.restful import reqparse, Resource
from app.models import Question, Poll
from sqlalchemy.exc import IntegrityError
from .res_errors import not_found
questionparser = reqparse.RequestParser()
questionparser.add_argument('text', type=str, required=True)
questionparser.add_argument('poll_id', type=int, required=True)


class QuestionList(Resource):
    """
    This resource represents the collection of Questions
    """
    def get(self):
        questions = Question.query.all()
        return [question.as_dict() for question in questions]


class QuestionPollList(Resource):
    """
    This resource represents the collection of Questions for a specific Poll
    """
    def get(self, poll_id):
        poll = Poll.query.get(poll_id)
        if poll is not None:
            questions = poll.questions.all()
            return [question.as_dict() for question in questions]
        else:
            return not_found("Poll %d" % poll_id), 404

    def post(self, poll_id):
        args = questionparser.parse_args()
        question = Question(
            text=args['text'],
            poll_id=args['poll_id']
        )
        try:
            db.session.add(question)
            db.session.commit()
        except IntegrityError, exc:
            return {"error": exc.message}, 500
        return question.as_dict(), 201


class QuestionView(Resource):
    """
    This resource represents a single Question
    """
    def get(self, question_id):
        question = Question.query.get(question_id)
        if question is not None:
            return question.as_dict()
        else:
            return not_found("Question %d" % question_id), 404

    def put(self, question_id):
        args = questionparser.parse_args()
        question = Question.query.get(question_id)
        if question is not None:
            question.text = args['text']
            question.poll_id = args['poll_id']
            db.session.commit()
            return question.as_dict(), 200
        else:
            return not_found("Question %d" % question_id), 404

    def delete(self, question_id):
        question = Question.query.get(question_id)
        if question is not None:
            db.session.delete(question)
            db.session.commit()
            return {}, 200
        else:
            return not_found("Question %d" % question_id), 404
