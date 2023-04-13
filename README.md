# AI Pal

AI Pal is a REST API first framework designed to simplify the integration of language models with data sources and other applications. With AI Pal, you can easily deploy language models as RESTful services, making it simple to integrate them into your application architecture.

## Features

- RESTful API
- Easy configuration and extensibility
- Integrates with data sources and other applications
- Memory management
- Support for multiple language models (in progress)
- Easy deployment and management

## Requirements

- Python 3.9 or later
- [OpenAI API Key](https://platform.openai.com/account/api-keys)

## Installation

1. Clone this repo

```
git clone https://github.com/vilelaml/aipal.git
```

2. Change to the AI Pal directory

```
cd aipal
```

3. Install dependencies

```
pip install -r requirements.txt
```

4. Configure the server 

Edit the `src/server/aipal.yml` file with your preferred text editor

```
vi src/server/aipal.yml
```

By default, it uses LocalCache memory, benefits from a better memory management.

You can enable or disable plugins by adding or removing them from the list

```
# src/server/aipal.yml
memory:
  class: LocalCache
  file_name: memory.json
plugin:
  base_path: plugins
  plugins:
    - confluence
```

5. Configure your api keys

Set the OpenAI Api Key, you can obtain it from https://platform.openai.com/account/api-keys.

```
export OPENAI_API_KEY=<your api key>
```

## Run

### Start the server

First you want to make sure your AI Pal server is running.

Set you PYTHONPATH. Make sure you are on the aipal directory

```
export PYTHONPATH=$PYTHONPATH:`pwd`
```

Run the server

```
cd src/server
python app.py
```

### Start the client

You can use any client that connects with an API, this example will use the console client.

Set you PYTHONPATH. Make sure you are on the aipal directory. You don't need to do it if you already did on the server setup.

```
export PYTHONPATH=$PYTHONPATH:`pwd`
```

Execute the console app

```
python src/client/console/aipal_client.py
```

## Usage

The API has only two endpoints:

### GET /commands

Will list of commands, including the core commands and the plugins. To test it you can use curl:

```
curl 'http://127.0.0.1:5000/command'
```

### POST /commands

Will execute the command with the following parameters:
- command: the command you want to execute
- args: the arguments in a json string

Example curl request, which will trigger a chat conversation with a LLM.

```
curl -X POST 'http://127.0.0.1:5000/command' --form 'command="chat"' --form 'args="{\"message\": \"Hello\"}"' 
```

## Contributing

All contributions are welcomed.

AI Pal intents to be configurable and extensible.

### Plugins

To create a new plugin you will need at least two files:
-  the plugin source code, which should be in the `src/server/plugins/<you_plugin>/` directory
- A configuration file `config.yaml`, on the same directory

#### Plugin python script

AI Pal is designed to be extended by plugins as a class. Most plugins methods will want to add the results into the memory, so you can use it to pass to the language model.

Make sure to:
- Get the memory from the config (it's a singleton)
- Make sure you add the return to the memory

_TODO_: wrap thing on a parent class and/or decorators to make it easier to create new plugins.

```
class MyPlugin:
    api_token = os.getenv("MYPLUGIN_API_KEY")

    @property
    def memory(self):
        return Config().memory

    def my_method(self, arg_1):
        result = do_my_thing
        self.memory.add(result)
        return 'Added to my knowledge base'
   
```


#### Configuration file

The `config.yaml` follows the structure

```
package: src.server.plugins.<your_plugin_directory>.<your_plugin_entrypoint>
class: <your_plugin_class>
commands:
  - name: <command_1_used_on_the_command_parameter_in_the_api_call>
    function: <command_1_the_method_it_will_call_on_your_class>
    args:
      - <arg_name>
  - name: <command_2_used_on_the_command_parameter_in_the_api_call>
    function: <command_2_the_method_it_will_call_on_your_class>
    args:
      - <arg_name>

```