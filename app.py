from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection
uri = "mongodb+srv://admin:admin@clusterace2.z3slk1n.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
db = client['sensor_data']
collection = db['readings']


@app.route('/add_reading', methods=['POST'])
def add_reading():
    try:
        data = request.get_json()

        temperature = data.get('temperature')
        aqi = data.get('aqi')
        co2 = data.get('co2')
        light = data.get('light')

        if temperature is None or aqi is None or co2 is None or light is None:
            return jsonify({'error': 'Missing data'}), 400

        new_reading = {
            'temperature': temperature,
            'aqi': aqi,
            'co2': co2,
            'light': light
        }

        result = collection.insert_one(new_reading)

        return jsonify({'message': 'Reading added successfully', 'inserted_id': str(result.inserted_id)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/get_readings', methods=['GET'])
def get_readings():
    try:
        readings = list(collection.find({}, {'_id': 0}))  # Exclude '_id' field from results
        return jsonify({'readings': readings})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
