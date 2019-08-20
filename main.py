from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask_jsonpify import jsonify  # works even when hashed out?!

db_connect = create_engine('sqlite:///chinook.db')

app = Flask(__name__)  # What are we doing to the Flask function?

# Attempt 1 to get jsonify working - failed!
# (https://flask.palletsprojects.com/en/1.1.x/api/#flask.json.jsonify)

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# Attempt 2 to get jsonify working - failed!
# app.config['DEBUG'] = True

api = Api(app)


class Employees(Resource):  # What is 'Resource here?'

    def get(self):  # Is self, just a reflection that this is a method?

        # connect to database
        conn = db_connect.connect()
        # The following line performs query and returns json result
        query = conn.execute(
                             """
                             select
                                *
                             from employees
                             """
                             )
        # Fetches first column (Employee ID) from each row
        # Not sure what cursor adds..
        return {
                'employees': [i[0]
                              for i in query.cursor.fetchall()]
                }


class Tracks(Resource):

    def get(self):
        conn = db_connect.connect()
        query = conn.execute(
                             """
                             select
                             trackid
                             , name
                             , composer
                             , unitprice

                             from tracks;
                             """
                            )

        # For each row in our query, we grab the table columns (query.keys())
        # and zip these column headers against our row values; we then create a
        # dictionary object from these pairings; then once all rows are
        # processed we put in a another dictionary object, with the output as
        # the value and 'data' as the key; we then return this as a JSON
        result = {
                  'data': [dict(zip(tuple(query.keys()), i))
                           for i in query.cursor]
                  }
        return jsonify(result)  # jsonify not working?


class Employees_Name(Resource):

    def get(self, employee_id):
        conn = db_connect.connect()

        # Select * from table where employee_id = pre-defined
        # value - no idea how we're pulling this in?!

        query = conn.execute(
                             """
                             select
                                *
                             from employees
                             where EmployeeId =%d
                             """
                             % int(employee_id)
                             )
        # Same as previous - zip column headers into k/v pairs and dict result
        result = {
                  'data': [dict(zip(tuple(query.keys()), i))
                           for i in query.cursor]
                  }
        return jsonify(result)  # jsonify not working?


# So here it looks like we call each class, and we also definine the string,
# to set the output against? i.e. web address + '/employees' returns our
# Employees class

api.add_resource(Employees, '/employees')  # Route_1
api.add_resource(Tracks, '/tracks')  # Route_2
api.add_resource(Employees_Name, '/employees/<employee_id>')  # Route_3

if __name__ == '__main__':
    app.run(port='5002')
