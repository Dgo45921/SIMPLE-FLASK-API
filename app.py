from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection
uri = "mongodb+srv://admin:admin@clusterace2.z3slk1n.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
db = client['sensor_data']
collection = db['readings']

bulbcollection = db['status']  # Use 'status' bulbcollection to store light bulb status


# Error response
def error_response(message, status_code):
    return jsonify({'error': message}), status_code


# Update light bulb status (toggle from false to true)
@app.route('/update_status', methods=['POST'])
def update_status():
    try:
        # Fetch the current status document
        current_status = bulbcollection.find_one({}, {'_id': 0, 'status': 1})

        if current_status:
            # Get the current status value
            current_status_value = current_status['status']

            new_status_value = not current_status_value

            # Update the existing status document with the new status value
            bulbcollection.update_one({}, {'$set': {'status': new_status_value}})

            return jsonify({'message': 'Status updated successfully'})
        else:
            return jsonify({'message': 'No status available'}), 404
    except Exception as e:
        return error_response(str(e), 500)


@app.route('/get_status', methods=['GET'])
def get_status():
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
        data = request.get_json()

        aqi = data.get('ppm')
        lumen = data.get('lumen')
        temp = data.get('temp')
        humidity = data.get('humedad')
        proximity = data.get('proximidad')
        notificacion_luz_encendida = data.get('notificacion_luz_encendida')
        notificacion_luz_apagada = data.get('notificacion_luz_apagada')
        notificacion_aire_sucio = data.get('notificacion_aire_sucio')
        notificacion_aire_limpio = data.get('notificacion_aire_limpio')

        if temp is None or aqi is None or lumen is None or humidity is None or proximity is None \
                or notificacion_luz_encendida is None or notificacion_luz_apagada is None \
                or notificacion_aire_sucio is None or notificacion_aire_limpio is None:
            return jsonify({'error': 'Missing data'}), 400

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

        result = collection.insert_one(new_reading)

        return jsonify({'message': 'Reading added successfully', 'inserted_id': str(result.inserted_id)})
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
        return jsonify( readings[len(readings) - 1])
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
