import docker
import hashlib
import os
import json

class ContainerManager:
    def __init__(self):
        self.client = docker.from_env()
        self.image_cache = self.load_image_cache()

    def generate_image_name(self, command):
        return "cmd_" + hashlib.sha256(command.encode()).hexdigest()

    def create_or_get_image(self, command):
        image_name = self.generate_image_name(command)
        if image_name in self.image_cache:
            return self.image_cache[image_name]
        
        dockerfile_content = f"""
        FROM ubuntu:latest
        RUN apt-get update && apt-get install -y procps
        CMD {command}
        """
        
        with open("Dockerfile", "w") as f:
            f.write(dockerfile_content)
        
        image, _ = self.client.images.build(path=".", tag=image_name)
        self.image_cache[image_name] = image_name  # Guardamos solo el nombre de la imagen
        self.save_image_cache()
        return image_name

    def run_container(self, image_name):
        self.client.containers.run(image_name, detach=True)

    def load_image_cache(self):
        if os.path.exists('data/image_cache.json'):
            with open('data/image_cache.json', 'r') as f:
                return json.load(f)
        return {}

    def save_image_cache(self):
        with open('data/image_cache.json', 'w') as f:
            json.dump(self.image_cache, f, indent=4)
