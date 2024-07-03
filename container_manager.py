import docker
import hashlib

class ContainerManager:
    def __init__(self):
        self.client = docker.from_env()
        self.image_cache = {}

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
        self.image_cache[image_name] = image
        return image

    def run_container(self, image):
        container = self.client.containers.run(image.id, detach=True)
        return container
