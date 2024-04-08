import datanode_pb2
import datanode_pb2_grpc
import grpc
from flask import Flask, jsonify, request
from google.protobuf.empty_pb2 import Empty

app = Flask(__name__)

dataNodes = {}
database = {}

# Funciones auxiliares

def send_request(name) -> list[str]:
    datanodes = []
    for key in dataNodes.keys():
        if key != name:
            info = dataNodes[key]
            ports = "localhost:" + str(info['port'])
            channel = grpc.insecure_channel(f"{ports}")
            client = datanode_pb2_grpc.dataNodeStub(channel)
            try:
                response = client.CheckStatus(Empty())
                if response.status:
                    datanodes = dataNodes[key]
                    print(f"This node is available {key}")
                else:
                    print(f"This node is available but there was an error {key}")
            except grpc.RpcError as e:
                print(f"This node isn't available {key}")
    return datanodes

# REST server

@app.route('/login', methods=['POST'])
def login():
    global dataNodes
    data = request.json
    datanode = data['name']
    port = data["port"]
    dataNodes[datanode] = {"name": datanode, "port": port}
    return jsonify({'message': 'DataNode Register successful', 'Name': datanode, 'Port': port}), 200

@app.route('/signal', methods=['GET'])
def signal():
    data = request.json
    name = data['name']
    if len(dataNodes) > 1:
        nodes = send_request(name)
        return jsonify({'message': 'Available DataNodes successful', 'nodes': nodes}), 200
    else:
        return jsonify({'error': 'There are 0 or just 1 DataNodes available'}), 404

@app.route('/save_data', methods=['POST'])
def save_data():
    global database
    data = request.json
    name = data['name']
    filename = data['filename']
    port = data['port']
    copy = data['copy']
    port_copy = data['port_copy']
    if filename not in database:
        database[filename] = [{'Filename': filename, 'Datanode Name': name, 'Port': port, 'Copy': copy, 'Port Copy': port_copy}]
    else:
        database[filename].append({'Filename': filename, 'Datanode Name': name, 'Port': port, 'Copy': copy, 'Port Copy': port_copy})
    return jsonify({'message': 'File Register successful', 'Name': filename, 'Port': port}), 200

@app.route('/search', methods=['GET'])
def search():
    try:
        return jsonify({'message': 'Search successful these are the available datanodes', 'dataNodes': dataNodes}), 200
    except Exception as e:
        return jsonify({'error': 'We cannot find any available datanode'}), 404
    

@app.route('/index', methods=['GET'])
def index():
    try:
        return jsonify({'message': 'Indexing successful these are the available files', 'dataBase': database}), 200
    except Exception as e:
        return jsonify({'error': 'We cannot find any file'}), 404

if __name__ == '__main__':
    app.run(debug=True)