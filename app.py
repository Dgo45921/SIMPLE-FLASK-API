from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection
uri = "mongodb+srv://admin:admin@clusterace2.z3slk1n.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
db = client['sensor_data']
collection = db['readings']

bulbcollection = db['bulb_status']  # Use 'status' bulbcollection to store light bulb status
aircollection = db['air_status']  # Use 'status' bulbcollection to store light bulb status
notificationcollection = db['notifications']


# Error response
def error_response(message, status_code):
    return jsonify({'error': message}), status_code


# Update light air status (toggle from false to true)
@app.route('/update_air_status', methods=['GET'])
def update_air_status():
    try:
        # Fetch the current status document
        current_status = aircollection.find_one({}, {'_id': 0, 'status': 1})

        if current_status:
            # Get the current status value
            current_status_value = current_status['status']

            new_status_value = not current_status_value

            # Update the existing status document with the new status value
            aircollection.update_one({}, {'$set': {'status': new_status_value}})

            return jsonify({'status': new_status_value})
        else:
            return jsonify({'message': 'No status available'}), 404
    except Exception as e:
        return error_response(str(e), 500)


@app.route('/get_air_status', methods=['GET'])
def get_air_status():
    try:
        latest_status = aircollection.find_one({}, {'_id': 0, 'status': 1})
        if latest_status:
            return jsonify({'status': latest_status['status']})
        else:
            return jsonify({'message': 'No status available'}), 404
    except Exception as e:
        return error_response(str(e), 500)


# Update light bulb status (toggle from false to true)
@app.route('/update_bulb_status', methods=['GET'])
def update_bulb_status():
    try:
        # Fetch the current status document
        current_status = bulbcollection.find_one({}, {'_id': 0, 'status': 1})

        if current_status:
            # Get the current status value
            current_status_value = current_status['status']

            new_status_value = not current_status_value

            # Update the existing status document with the new status value
            bulbcollection.update_one({}, {'$set': {'status': new_status_value}})

            return jsonify({'status': new_status_value})
        else:
            return jsonify({'message': 'No status available'}), 404
    except Exception as e:
        return error_response(str(e), 500)


@app.route('/get_bulb_status', methods=['GET'])
def get_bulb_status():
    try:
        latest_status = bulbcollection.find_one({}, {'_id': 0, 'status': 1})
        if latest_status:
            return jsonify({'status': latest_status['status']})
        else:
            return jsonify({'message': 'No status available'}), 404
    except Exception as e:
        return error_response(str(e), 500)


@app.route('/add_reading', methods=['POST'])
def add_reading():
    try:

        print(request)
        data = request.get_json()
        print(data)

        aqi = data.get('ppm')
        lumen = data.get('lumen')
        temp = data.get('temp')
        humidity = data.get('humedad')
        proximity = data.get('proximidad')
        notificacion_luz_encendida = data.get('notificacion_luz_encendida')
        notificacion_luz_apagada = data.get('notificacion_luz_apagada')
        notificacion_aire_sucio = data.get('notificacion_aire_sucio')
        notificacion_aire_limpio = data.get('notificacion_aire_limpio')

        new_reading = {
            'ppm': aqi,
            'lumen': lumen,
            'temp': temp,
            'humedad': humidity,
            'proximidad': proximity,
            'notificacion_luz_encendida': notificacion_luz_encendida,
            'notificacion_luz_apagada': notificacion_luz_apagada,
            'notificacion_aire_sucio': notificacion_aire_sucio,
            'notificacion_aire_limpio': notificacion_aire_limpio

        }

        print(new_reading)

        if notificacion_luz_encendida:
            newnoti = {
                'message': 'La luz fue encendida'
            }

            notificationcollection.insert_one(newnoti)

        if notificacion_luz_apagada:
            newnoti = {
                'message': 'La luz fue apagada'
            }

            notificationcollection.insert_one(newnoti)

        if notificacion_aire_sucio:
            newnoti = {
                'message': 'La calidad del aire es mala!'
            }

            notificationcollection.insert_one(newnoti)

        if notificacion_aire_limpio:
            newnoti = {
                'message': 'El aire esta limpio'
            }

            notificationcollection.insert_one(newnoti)

        result = collection.insert_one(new_reading)

        return jsonify({'message': 'Reading added successfully', 'inserted_id': str(result.inserted_id)})
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500


@app.route('/get_last_notifications', methods=['GET'])
def get_last_notifications():
    try:
        readings = list(notificationcollection.find({}, {'_id': 0}))
        last_4_readings = readings[-4:]  # Using slicing to get the last 4 elements
        return jsonify(last_4_readings)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/get_readings', methods=['GET'])
def get_last_reading():
    try:
        readings = list(collection.find({}, {'_id': 0}))
        return jsonify({'readings': readings})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/get_last_reading', methods=['GET'])
def get_readings():
    try:
        readings = list(collection.find({}, {'_id': 0}))
        return jsonify(readings[len(readings) - 1])
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
