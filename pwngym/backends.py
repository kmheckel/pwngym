import subprocess
import time
import yaml
import os

from abc import ABC, abstractmethod

class Backend(ABC):
    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

class DockerBackend(Backend):
    """This class executes a local Docker Compose command and can set up one or more containers for use."""
    def __init__(self, compose_path, startup_time=10, service_name="kali-rolling"):
        self.compose_path = compose_path
        self.startup_time = startup_time
        self.service_name = service_name
        
    def start(self):
        subprocess.run(['sudo', 'docker', 'compose', '-f', self.compose_path, 'up', '-d'])
        time.sleep(self.startup_time)

    def stop(self):
        subprocess.run(['sudo', 'docker', 'compose', '-f', self.compose_path, 'down'])


class ExternalBackend(Backend):
    """This class is in case you want to substitute a remote cyber range into an eval and don't want to have to change calls for starting or shutting down the environment."""
    def __init__(self, verbose=True):
        self.verbose = verbose

    def start(self):
        if self.verbose:
            print("External Backend, you must start it up yourself.")

    def stop(self):
        if self.verbose:
            print("External Backend, you must shut it down yourself.")
