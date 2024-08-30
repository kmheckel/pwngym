# pwngym

<p align="center">
  <img src="pwngym_welcome.jpg" alt="PwnGym Welcome Banner" width="100%">
</p>

# PwnGym

PwnGym is a minimalistic library for interfacing foundation models with the command line. It permits the model to work with a TTY connection and allows for the use of interactive tools; this is notably different than most other LLM-CLI interfaces which wait for EOFs.

## Features

- **Realistic Environments**: Simulate real-world scenarios using Docker containers.
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

2. Install the pwngym package:
   ```
   pip install pwngym
   ```


## Usage

PwnGym provides a Python API for interacting with the simulated environments. Simply create a backend and start it to launch a Docker environment, then connect in using an Env object; from there, call step or reset as you please.

The Env.step() method can be built into tools provided to an LLM agent to allow it to interact with the environment.
