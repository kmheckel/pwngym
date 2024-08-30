<p align="center">
  <img src="pwngym_welcome.jpg" alt="PwnGym Welcome Banner" width="50%">
</p>

# PwnGym

PwnGym is a minimalistic library for interfacing foundation models with the command line. It permits the model to work with a TTY connection and allows for the use of interactive tools; this is notably different than most other LLM-CLI interfaces which wait for EOFs.

## Features

- **Flexible Backend**: Choose between local Docker setup or connect to external cyber ranges.
- **Interactive TTY Interface**: Seamlessly connect AI models to command-line interfaces.
- **Customizable Configurations**: Easily set up and manage different testing environments.
- **Transformation Utilities**: Handle special cases like Windows path escaping.

## Getting Started

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/pwngym.git
   cd pwngym
   ```

2. Install the pwngym as a local package (be sure to install the top level pwngym folder.):
   ```
   pip install -e ./pwngym
   ```


## Usage

PwnGym provides a Python API for interacting with the simulated environments. Simply create a backend and start it to launch a Docker environment, then connect in using an Env object; from there, call step or reset as you please.

The Env.step() method can be built into tools provided to an LLM agent to allow it to interact with the environment.

For example, here is how you could use pwngym as a LangChain tool:

```
def build_terminal_tool(env: pwngym.Env) -> Callable:
    @tool
    def terminal(command: str) -> str:
        """Execute a Linux terminal command."""
        return env.step(command)
    return terminal
```

Alternatively, you can drop the @tool decorator and pass the wrapped `env.step()` function to the API endpoint if it supports function calling.

## Environments:

You can use PwnGym to either connect to a remote/privately hosted cyber range, test locally against other docker containers, or a mix of the two. For example, you can replace the `example.ovpn` file with a connection pack from HackTheBox and have your agent work on HTB machines while executing from a local container.

For full details of the Docker environments, check the Docker compose files; you can also feel free to use your own!

## Honeypots:

PwnGym also supports honeypots for countering offensive cyber agents. These rely on prompt injection attacks and deceving the offensive agent into executing defender-specified code, allowing for defenders to gather more information, impede, or defeat the attacker.