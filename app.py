from flask import Flask, jsonify, request
from flask_cors import CORS
import subprocess

app = Flask(__name__)
CORS(app)  # Enable CORS

def docker_launch(docker_image, container_name):
    cmd = f"docker run -i -d -t --name {container_name} {docker_image}"
    cid = subprocess.getoutput(cmd)
    return f"Docker launched with container ID: {cid}"

@app.route('/launch', methods=['POST'])
def launch_container():
    data = request.get_json()
    docker_image = data.get('docker_image')
    container_name = data.get('container_name')

    if not docker_image:
        return jsonify({"error": "No Docker image provided"}), 400
    if not container_name:
        return jsonify({"error": "No container name provided"}), 400

    container_id = docker_launch(docker_image, container_name)
    return jsonify({"message": container_id}), 200

@app.route('/pull', methods=['POST'])
def pull_docker_image():
    data = request.get_json()
    docker_image = data.get('docker_image')

    if not docker_image:
        return jsonify({"error": "No Docker image provided"}), 400

    cmd = f"docker pull {docker_image}"
    result = subprocess.getoutput(cmd)

    if "Error" in result:
        return jsonify({"error": result}), 400

    return jsonify({"message": f"Docker image '{docker_image}' pulled successfully."}), 200

@app.route('/images', methods=['GET'])
def list_docker_images():
    cmd = "docker images --format '{{.Repository}}:{{.Tag}}'"
    images = subprocess.getoutput(cmd).splitlines()
    return jsonify({"images": images}), 200

@app.route('/containers', methods=['GET'])
def list_docker_containers():
    cmd = "docker ps --format '{{.ID}}: {{.Image}} ({{.Status}})'"
    containers = subprocess.getoutput(cmd).splitlines()
    return jsonify({"containers": containers}), 200

@app.route('/volumes', methods=['GET'])
def list_docker_volumes():
    cmd = "docker volume ls --format '{{.Name}}'"
    volumes = subprocess.getoutput(cmd).splitlines()
    return jsonify({"volumes": volumes}), 200

@app.route('/networks', methods=['GET'])
def list_docker_networks():
    cmd = "docker network ls --format '{{.Name}}'"
    networks = subprocess.getoutput(cmd).splitlines()
    return jsonify({"networks": networks}), 200

@app.route('/stop', methods=['POST'])
def stop_container():
    data = request.get_json()
    container_name = data.get('container_name')
    if not container_name:
        return jsonify({"error": "No container name provided"}), 400
    
    cmd = f"docker stop {container_name}"
    result = subprocess.getoutput(cmd)
    
    if result.startswith("Error"):
        return jsonify({"error": result}), 400
    
    return jsonify({"message": f"Container '{container_name}' stopped successfully."}), 200

@app.route('/remove', methods=['POST'])
def remove_container():
    data = request.get_json()
    container_name = data.get('container_name')
    if not container_name:
        return jsonify({"error": "No container name provided"}), 400
    
    cmd = f"docker rm {container_name}"
    result = subprocess.getoutput(cmd)
    
    if result.startswith("Error"):
        return jsonify({"error": result}), 400
    
    return jsonify({"message": f"Container '{container_name}' removed successfully."}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
