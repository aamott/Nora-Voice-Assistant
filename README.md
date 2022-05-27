# Nora-Voice-Assistant
Nora is a voice assistant built on the concept of modularity, ease of design and development, and a flexible and extensible architecture. Its original intent was to explore the concept of a web UI that allows for a user to edit routines (and even skills themselves) through the user of a block programming language. Now, this Web UI is planned to take over settings as well, and in the future may include a text-based way to interact with the voice assistant. 


## Background
Nora is built off of modular components. Each piece (i.e. speech recognition, text to speech, etc.) should be able to be replaced by another module accepting and receiving the same data and continue to function without any changes to the outside code. 
Skills are the core concept of a voice assistant. Each skill is a set of related functions a user can call on. For example, a music player skill might allow the user to say, “play Party in the USA” as well as “pause the music.” Skills should be developable by almost anyone with a basic knowledge of coding.


## Installation
1. Install Python 3.8 or higher (might work with older versions)

2. clone the repository and enter the directory
``` bash
git clone https://github.com/aamott/Nora-Voice-Assistant.git

cd Nora-Voice-Assistant
```

3. Install dependencies
``` bash
pip3 install -r requirements.txt
```

4. Run the server
``` bash
python3 nora.py
```

5. To get updates, run `git pull` from the root directory.


# Development
The most helpful development right now is in the skill department. Skills are lacking right now as this is a beginning project, but it has a lot of room to grow. For a quick example, see the `hello_world` skill inside the `skills` folder. It's a single-file, very basic skill. 
There are a few requirements all skills follow:
1. A skill must inherit from the `BaseSkill` class. For example:
``` python
from skills import base_skill

class Skill(base_skill.BaseSkill):
    ...
```

2. A skill must accept 3 parameters: `settings_tool` of type `SettingsTool`, channels of type `Channels`, and `audio_utils` of type `AudioUtils`. For example:
``` python
...
from core_utils.core_core.channels import Channels
from core_utils.settings_tool import SettingsTool
from core_utils.audio_utils import AudioUtils

class Skill(base_skill.BaseSkill):

    def __init__(self, settings_tool: SettingsTool, channels: Channels, audio_utils: AudioUtils):
        ...
```
In case you don't know, `audio_utils: AudioUtils` simply means that audio_utils has to be an AudioUtils object. 

3. The skill class must implement `BaseSkill`'s methods. One is the `__init__` function as mentioned above. The other is the `intent_creator`, which allows the skill to register intents. 
``` python
    ...

    def intent_creator(self, register_intent: callable):
            """ registers intents using register_intent """
            ...
```
It passes in a `register_intent` callback, which registers one intent at a time. It requires 3 arguments:  
    `intent_callback`: The function that will be called when the intent is triggered  
    `intent_phrases`:  The phrase(s) that will trigger the intent. These must be formatted as given in Mycroft's documentation for Padatious. 
    `intent_name`: The name of the intent. There must be no duplicate names in any given skill.  
Example of using register_intent (continuing at the ellipsis):

``` python
            ...
            register_intent(intent_callback=self.hello_world_intent, # this is a reference to the function below
                            intent_phrases=["hello (world | )"], # this will match "hello world" and "hello"
                            intent_name="say_hello") # There is no other intent in this skill named "say_hello"


    # The function to be registered as an intent
    def hello_world_intent(self, intent_data):
        print("Hello World!")
        self.audio_utils.say("Hello World!")
```


4.  Skills may use the provided `settings_tool` of type `SettingsTool`, channels of type `Channels`, and `audio_utils` of type `AudioUtils`. 

It is important to note that classes must be imported as though they are being viewed from `nora.py` and not relative to the skill doing the importing. Otherwise, we couldn't have access to many of the core elements used in a skill, like those described next. 


## SettingsTool
Passed in as  `settings_tool: SettingsTool` and imported with `from core_utils.settings_tool import SettingsTool`. SettingsTool manages settings for whatever class it is set up for. Skills receive a SettingsTool with the path set to `skills.<skill_name>` replacing `<skill_name>` with the skill's actual name. For example, `skills.hello_world`. Settings saved here will show up in the settings.yaml file as follows:  
``` yaml
skills:
    hello_world:
        # Settings set in the hello world skill will show up here 
        world_shape: round
        foods:
            ice_creams:
                vanilla: good
                strawberry: better
                chocolate: best
```
Settings paths are written in dot notation. For example, `setting_path = "foods.ice_creams.strawberry"`.  
SettingsTool implements 2 core methods:  
1. `get_setting(setting_path)` - Gets a setting by its path.
2. `set_setting(setting_path, value)` - Sets the setting under setting_path to the value. If the path does not exist, it will be created. For example:
``` python
    ...
    setting_path = "foods.ice_creams.strawberry"
    value = "bestest"
    self.settings_tool.set_setting(setting_path, value)
    ...
```
Now, the settings.yaml file has changed.  
``` yaml
                ...
                strawberry: bestest
                chocolate: best
```


## Channels
Channels allow skills to communicate with each other and the core system. If one skill wants to receive messages from another skill, it must `subscribe` to a channel the other skill is `publishing` to. For example, two functions could use Channels as follows:
``` python
from core_utils.core_core.channels import Channels

channels = Channels()

# the function that will publish
def say_hello():
    print("hello, world!")
    channels.publish(message ="hello, world!", channel = "hello_channel")

# the function that will be subscribed
def say_hello_louder(message):
    print( message.upper() )

# subscribe the say_hello_louder function to the "hello_channel" channel
channels.subscribe(callback=say_hello_louder, "hello_channel")

say_hello()
```

Running this prints the following:  
``` bash
hello, world!
HELLO, WORLD!
```
A function can also unsubscribe and it will no longer receive messages:
``` python
...
channels.unsubscribe(callback = say_hello_louder)
```

## AudioUtils
The AudioUtils object is used for any audio control and interaction, including speaking, listening, recording, and playing sounds. Its main methods include:

- `say(text)`
- `listen()` -> str - returns text of what the user said. If no speech was detected, returns  `None`
- `play(filename:str = None, audio_data:ndarray = None)` - Plays filename or audio in a numpy array
- `pause()` - pauses any playback
- `resume()` - resumes any playback
- `stop()` - ends any playback. Running resume() after stop() has no effect.
- `play_sound(filename:str = None, audio_data:ndarray = None)` - Like play, but targeted to shorter sounds, like sound effects for a game.
- `stop_sound()` - Ends all sound effect playback. 

## TODO: 
### Essentials
- [x] Speech to Text engines 🗣️
    - [X] Audio Recording class 🎤
- [X] Text to Speech engines 👂
    - [ ] Use Audio Playback class  🎧
- [X] Intent Parser -  [Padaos](https://github.com/MycroftAI/padaos) 🤔
- [X] Wakeword - [Porcupine](https://pypi.org/project/pvporcupine/) ⏰

### Basic Skills 🤹🏻‍♀️
- [X] Hello World 👋
- [ ] Music Player 🎵
- [ ] Weather 🌍
- [ ] News 📰
- [ ] Calculator 📈
- [ ] To Do List 📋
- [ ] Calendar, Time, and Reminder 📅
- [ ] Notes 📝

### Next step
- [X] Settings Manager 🔧
- [X] Channels class📡
- [ ] Routine Manager 📦

### Web Interface 🌐
- [ ] Web Server Backend - [FastAPI](https://fastapi.tiangolo.com/)🚀
- [ ] Settings Control 🔧
- [ ] Routine Manager 📦
- [ ] Skill Editor 📝