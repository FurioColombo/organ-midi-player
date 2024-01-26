from flask import Flask, jsonify, request
from flask_cors import CORS
from serial_messages import SerialMessagesHandler
from server_state import ServerState
from player import ParsedMidiSerialPlayer

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})
server_state = ServerState()
serial_message_handler = SerialMessagesHandler(server_state.get_com_port())

@app.route('/')
def index():
    return jsonify('Welcome to the Flask server!')

@app.route('/receive-parsed-midi', methods=['POST'])
def receive_data():
    try:
        data = request.get_json()
        server_state.set_parsed_midi_channels(data)
        for i in range(5):
            print("Received parsed midi data:", server_state.get_parsed_midi_channels()[0][i])
        return jsonify({'message': 'Data received successfully'})
    
    except Exception as e:
        print("Error while receiving data:", e)
        return jsonify({'message': 'Error receiving data'}), 500

@app.route('/play', methods=['POST'])
def play():
    print('Starting the music')
    print(type(server_state.get_parsed_midi_channels()))
    parsed_midi_serial_player = ParsedMidiSerialPlayer()
    parsed_midi_serial_player.play(server_state.get_parsed_midi_channels()[0])
    # for i in range(5):
    #     print(server_state.get_parsed_midi_channels()[0][i])
    # for i in range(2):
    #     serial_message_handler.send_message(b'Auguriiii!!')
    return jsonify({'message': 'Play route triggered'})

@app.route('/change-com-port', methods=['POST'])
def set_com_port():
    try:
        data = request.get_json()
        server_state.set_com_port(data['new_com_port'])
        serial_message_handler.change_COM_port(server_state.get_com_port())
        return jsonify({'message': 'COM port changed successfully'})
    
    except Exception as e:
        print("Error while setting a new com port:", e)
        return jsonify({'message': 'Error while setting a new com port'}), 500
