from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class Home(Resource):
    def get(self):
        return "Incognito analytic is running"


api.add_resource(Home, '/')

if __name__ == '__main__':
    app.run(debug=True)
