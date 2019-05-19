from flask_restplus import Resource, Namespace

api = Namespace("auditories")

@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}