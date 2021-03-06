from app import db
from flask.ext.restful import reqparse, Resource, fields, marshal_with
from app.models import Poll
from sqlalchemy.exc import IntegrityError
from .res_errors import not_found
pollparser = reqparse.RequestParser()
pollparser.add_argument('name', type=str, required=True)
resource_fields = {
    'id': fields.String,
    'name': fields.String,
    'timestamp': fields.DateTime(dt_format='rfc822')
}


class PollList(Resource):
    """
    This resource represents the collection of all Polls
    """

    @marshal_with(resource_fields)
    def get(self):
        polls = Poll.query.all()
        return [poll.as_dict() for poll in polls]

    @marshal_with(resource_fields)
    def post(self):
        args = pollparser.parse_args()
        poll = Poll(name=args['name'])

        try:
            db.session.add(poll)
            db.session.commit()
        except IntegrityError, exc:
            return {"error": exc.message}, 500
        return poll.as_dict(), 201


class PollView(Resource):
    """
    This resource represents a single Poll
    """
    @marshal_with(resource_fields)
    def get(self, poll_id):
        poll = Poll.query.get(poll_id)
        if poll is not None:
            return poll.as_dict()
        else:
            return not_found("Poll %d" % poll_id), 404

    def put(self, poll_id):
        """
        TODO: don't require the entire object, only the field being changed
        """
        args = pollparser.parse_args()
        poll = Poll.query.get(poll_id)
        if poll is not None:
            poll.name = args['name']
            db.session.commit()
        else:
            return not_found("Poll %d" % poll_id), 404

    def delete(self, poll_id):
        poll = Poll.query.get(poll_id)
        if poll is not None:
            db.session.delete(poll)
            db.session.commit()
            return {}, 200
        else:
            return not_found("Poll %d" % poll_id), 404
