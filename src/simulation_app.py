"""
This module was made to replace the singleton used previously,
creating another layer of communication, this one between the API and the simulation.

To go back to the previous version, one must import the listeners and the simulation singleton in this file
making the appropriate changes to the file to create a socket server
Also, one file to start the app is needed, check previous versions of the repo looking after the file
"start_simulation.py"
"""
import json
import sys
from flask import request, jsonify
from flask import Flask
from flask_cors import CORS
from src.simulation.simulation import Simulation

config_path, base_url, port = sys.argv[1:]


def start_instance(path):
    with open(path, 'r') as simulation_config:
        json_config = json.loads(simulation_config.read())
        return Simulation(json_config)


app = Flask(__name__)
simulation = start_instance(config_path)
initial_percepts = simulation.start()


@app.route('/register_agent', methods=['POST'])
def register_agent():
    if request.remote_addr != base_url:
        return jsonify(message='This endpoint can not be accessed.')

    token = request.get_json(force=True)
    if token is not None:
        result = simulation.create_agent(token)
        return jsonify({'results': result.__dict__, 'initial_percepts': initial_percepts})
    return 'NoneType'


@app.route('/do_actions', methods=['POST'])
def do_actions():
    if request.remote_addr != base_url:
        return jsonify(message='This endpoint can not be accessed.')

    actions = request.get_json(force=True)
    if actions is not None:
        result = simulation.do_step(actions)

        current = result['events']['current_event']
        json_events = {'current_event': None, 'pending_events': []}
        if current is not None:
            json_events['current_event'] = current.json()

        for idx, event_list in enumerate(result['events']['pending_events']):
            json_events['pending_events'].append([])
            for event in event_list:
                json_events['pending_events'][idx].append(event.json())

        result['events'] = json_events

        return jsonify(result)
    return 'NoneType'


if __name__ == '__main__':
    app.debug = False
    app.config['SECRET_KEY'] = 'gjr39dkjn344_!67#'
    CORS(app)
    app.run(port=port)