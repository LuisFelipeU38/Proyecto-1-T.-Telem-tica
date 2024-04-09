import datanode_pb2
import datanode_pb2_grpc
import grpc
import requests
from google.protobuf.empty_pb2 import Empty

# Configuraciones
options = [
    ('grpc.max_receive_message_length', 50 * 1024 * 1024),
]

file  = []
name = ""

def upload_file(datanodes, file_name, file_address):

    with open(file_address, "rb") as file:
        block_size = 1024 * 1024 
        datanode_keys = list(datanodes.keys()) 
        datanode_count = len(datanode_keys)
        block_index = 0
        arr_nodes = set()
        while True:
            block_data = file.read(block_size)
            if not block_data:
                break
            else:
                if len(block_data) < block_size:
                    block_data += b'\0' * (block_size - len(block_data))
                
                selected_datanode_key = datanode_keys[block_index % datanode_count]
                selected_datanode_info = datanodes[selected_datanode_key]
                arr_nodes.add(selected_datanode_key)
                channel = grpc.insecure_channel("localhost:" + str(selected_datanode_info['port']))
                stub = datanode_pb2_grpc.dataNodeStub(channel)
                try:
                    response = stub.WriteBlock(datanode_pb2.WriteBlockRequest(name=file_name, data=block_data))
                    if not response.success:
                        print(f"Error sending the block {selected_datanode_key}")
                        break
                    else:
                        print(f"Block successfully sended {selected_datanode_key}")
                except grpc.RpcError as e:
                    print(f"Error on the connection with the datanode {selected_datanode_key}: {e}")
                    break
                
                block_index += 1
        for node in arr_nodes:
            node_info = datanodes[node]
            channel = grpc.insecure_channel("localhost:" + str(node_info['port']))
            stub = datanode_pb2_grpc.dataNodeStub(channel)
            response = stub.SendIndex(datanode_pb2.SendIndexRequest(filename=file_name))



def download_blocks():
    blocks = []
    for node in file:
        if node['leader_available']:
            channel = grpc.insecure_channel("localhost:" + str(node['Port']), options=options)
        else:
            channel = grpc.insecure_channel("localhost:" + str(node['Port Copy']), options=options)
        stub = datanode_pb2_grpc.dataNodeStub(channel)
        data = stub.ReadBlock(datanode_pb2.ReadBlockRequest(name=node['Filename']))
        blocks.append(data.data)
    with open(name, 'wb') as final_file:
        for node_block in blocks:
            for block in node_block:
                final_file.write(block)
        
        print(f"Archivo {name} descargado y reconstruido correctamente.")

def index(base_url):
    """
    Función para obtener los nodos de datos disponibles.
    """
    try:
        response = requests.get(f"{base_url}/index")
        if response.status_code == 200:
            print("Indexing successful. Available data nodes:")
            print(response.json())
        else:
            print("Failed to index data nodes.")
    except Exception as e:
        print(f"Error during indexing: {e}")

def search(base_url):
    try:
        response = requests.get(f"{base_url}/search")
        if response.status_code == 200:
            print("Search successful. Available files:")
            data = response.json() 
            print(data)
            return data['dataNodes']
        else:
            print("File not found or error during search.")
            return {}
    except Exception as e:
        print(f"Error during search: {e}")
        return {}

def get_file(base_url, filename):
    global file, name
    try:
        response = requests.get(f"{base_url}/get_file", json=filename)
        if response.status_code == 200:
            print("Search successful. Available files:")
            data = response.json() 
            file = data['Nodes']
            name = filename
            download_blocks()
            print(data)
        else:
            print("File not found or error during search.")
    except Exception as e:
        print(f"Error during search: {e}")


def run():
    # Establecer conexión con el servidor DFS para gRPC
    channel = grpc.insecure_channel('localhost:50051', options=options)
    stub = datanode_pb2_grpc.dataNodeStub(channel)

    base_url = "http://localhost:5000"  # Asegúrate de ajustar esto a la URL de tu servidor Flask
    
    option = menu()
    
    if option == "1":
        file_name = "luis.jpg"
        file_address = "C:/Users/admin/Downloads/luis.jpg"
        datanode = search(base_url)
        upload_file(datanode, file_name, file_address)
    elif option == "2":
        index(base_url)
    elif option == "3":
        file_name = input("What is the name of the file to download?")
        get_file(base_url, file_name)
    else:
        print("Opción no válida.")

def menu():
    print("Bienvenido al Cliente del Sistema DFS")
    print("1. Subir archivo al servidor")
    print("2. Indexar nodos de datos disponibles")
    print("3. Buscar un archivo específico")
    return input("Seleccione una opción: ")

if __name__ == '__main__':
    run()
