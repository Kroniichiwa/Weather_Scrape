from flask import Flask
from flask_restful import Api, Resource, abort, marshal_with ,fields, reqparse
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
db = SQLAlchemy(app)
api = Api(app)

class WeatherModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable = False)
    temp = db.Column(db.String(100), nullable = False)
    unit = db.Column(db.String(100), nullable = False)
    date = db.Column(db.String(100), nullable = False)
    desc = db.Column(db.String(100), nullable = False)

    def __repr__(self) :
        return f"Weather(name:{name},temp:{temp} ,unit:{unit}, date:{date}, desc:{desc})"

#Requesr Parser
weather_add_args=reqparse.RequestParser()
weather_add_args.add_argument("name",required=True,type=str,help="Name is required!")
weather_add_args.add_argument("temp",required=True,type=str,help="Temperature is required!")
weather_add_args.add_argument("unit",required=True,type=str,help="Degree Celsius is required!")
weather_add_args.add_argument("date",required=True,type=str,help="Date is required!")
weather_add_args.add_argument("desc",required=True,type=str,help="Description is required!")

resource_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "temp": fields.String,
    "unit": fields.String,
    "date": fields.String,
    "desc": fields.String,
}

#use line 40, For only the first time you're running this code
#db.create_all()

class Weather(Resource):
    @marshal_with(resource_fields)
    def get(self, weather_name):
        if weather_name == "All" :
            data = WeatherModel.query.all()
            return data, 200
        weather = WeatherModel.query.filter_by(name=weather_name).first() 
        if not weather :
            abort(404,message="Name not found...")
        return weather, 200
    
    @marshal_with(resource_fields)
    def post(self, weather_name) :
        weather = WeatherModel.query.filter_by(name=weather_name).first() 
        if weather :
            abort(403,message="This Country or this city is taken!")
        args=weather_add_args.parse_args()
        new_weather = WeatherModel(name=weather_name,temp=args["temp"],unit=args["unit"],date=args["date"],desc=args["desc"])
        db.session.add(new_weather)
        db.session.commit()
        return new_weather, 201
    
    @marshal_with(resource_fields)
    def delete(self, weather_name):
        result = WeatherModel.query.filter_by(name=weather_name).first()
        if not result:
            abort(404, message="Name not found...")
        db.session.delete(result)
        db.session.commit()
        return '', 204
    

api.add_resource(Weather,"/Weather/<string:weather_name>")

if __name__ == "__main__" :
    app.run(debug=True)