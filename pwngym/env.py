import re
from typing import Callable
from .utils import *
from .transformations import *

from pwnlib.tubes.ssh import ssh

from pydantic import BaseModel
from pydantic.networks import IPvAnyAddress


class EnvConfig(BaseModel):
    name: str
    ip_address: IPvAnyAddress
    username: str
    password: str
    max_output_chars: int = 65536 # set to at most the context length of your model unless you want to do multistage summarization/extraction.
    timeout: int = 5
    patient_keywords: list[str] = []
    patience_factor: int = 3
    verbose: bool = False
    instrumentation: Callable = print
    transformations: list[Callable] = [escape_windows_paths]

class Env:
    """An interactive TTY interface for connecting Foundation Models to the CLI."""
    def __init__(self, config: EnvConfig):
        self.name = config.name
        self.ip = config.ip_address
        self.username = config.username
        self.password = config.password # TODO: support SSH keyfiles for more secure login. pwntools already supports this, so just need an arg.
        self.max_output_chars = config.max_output_chars # how many characters before truncating the message.
        self.timeout = config.timeout # how long to wait since last received bytes before returning.
        self.patient_keywords = config.patient_keywords # commands to use a longer timeout for
        self.patience_factor = config.patience_factor # timeout multiplier for longer commands to ensure full output capture.
        self.verbose = False # Whether to print/log the received commands and corresponding output.
        self.callback = config.instrumentation # printing/logging function to use if verbose mode enabled.
        self.transformations = config.transformations

        self.reset()
        self.step("PS1='$(whoami)@kali:$(pwd)# '") # add CWD and user/host information to shell prompt.
        self.verbose = config.verbose

    def reset(self):
        """Reset the ssh connection to the Linux environment."""
        self.conn = ssh(self.username, self.ip, password=self.password)
        self.shell = self.conn.system("/bin/sh") # use a vanilla shell since extra features in bash make it tougher to parse.
        if self.verbose:
            self.callback(f"Connection to {self.ip} reset.")


    def step(self, command: str):
        """Execute a terminal command in the environment. This command will truncate the feedback after so many characters to save token costs."""
        output = b""

        if self.verbose:
            self.callback(f"### Sending Command ###\n{command}\n### End Command ###")

        self.shell.sendline(bytes(command, "utf-8"))

        recv_timeout = self.timeout
        if check_keywords(self.patient_keywords, command):
            recv_timeout *= self.patience_factor

        output += f"### Feedback from executing command '{command}': ###\n".encode('utf-8')
        output += self.shell.recvrepeat(recv_timeout)
        output = clean_byte_string(output).decode('utf-8')

        trimmed_output = output[:self.max_output_chars]
        if len(output) > self.max_output_chars:
            trimmed_output += "### Message Truncated ###"
        
        for transform in self.transformations:
            trimmed_output = transform(trimmed_output)

        if self.verbose:
            self.callback(f"### Output Received ###\n{trimmed_output}\n### End Output ###")

        return trimmed_output



