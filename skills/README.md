# Skills
This folder contains all the skills. Here, we'll go over the development of a skill. 

# Creating a Basic Skill
A really basic skill only has to do two things: activate when a user says something specific (their 'intent') and respond. 

### Create a file
The skill can reside in a single file with the name of the skill (like the hello world skill) or in a folder where the name of the entry file is either `__init__.py` or the same as the folder name. 


### Write the Skill class
To start, we need to declare a `Skill` class that inherits from `base_sill.BaseSkill` class.
```python
...
class Skill(base_skill.BaseSkill):
    name = "Hello World Skill"
    ...
```


Next, we set up the skill with some basic tools. The setup function expects a skill to have these parameters, and if it doesn't, it will fail to import. 
```python
from skills import base_skill
from core_utils.core_core.channels import Channels
from core_utils.settings_tool import SettingsTool
from core_utils.audio_utils import AudioUtils

class Skill(base_skill.BaseSkill):
    name = "Hello World Skill"


    def __init__(self, settings_tool: SettingsTool, channels: Channels, audio_utils: AudioUtils):
        """ Initialize the skill. 
         """
        self.settings_tool = settings_tool
        self.channels = channels
        self.audio_utils = audio_utils
```
This will give us access to the 3 main tools: `audio_utils` (for interacting with the user and audio), `settings_tool` (for managing your skill's settings), and `channels` (for inter-skill communication).  
For now, let's focus on `audio_utils`. 

### The `intent_creator` Function
Next, we need a way to add our skill's intents. To do this, we create a function called `create_intents` that accepts a function as input. 

```python
 def intent_creator(self, register_intent: callable):
        """ This function registers intents
            Parameters: 
                register_intent (callable): a function that
                can add an intent to Nora. 
            """
        ...
```

To add an intent, we call this function with 3 inputs: 
- `intent_callback`: The function to call when the intent is detected.
- `intent_phrases`: The phrase(s) that will activate the function. See [How to Write an Intent Phrase](#how-to-write-an-intent-phrase) below.
- `intent_name`: A name to keep track of your intent.

```python
        ...
        register_intent(
            intent_callback=self.hello_world_intent,
            # This hrase will match 'hello world' or 'hello'.
            intent_phrases=["Hello (world | )"],
            intent_name="say_hello")

        ...
```

### The Intent Callback
Finally, when your intent is detected, the function you specified above will be called. The function has to accept 2 inputs: 
- `self` - This is a class, after all.
- `intent_data` - A dictionary containing data about what the user said. It looks like this (but the entity names will be what you put in).
```python
# intent_data
{'name': str, 'original_phrase': str 'entities': {<entity name>: str, <other entity name>: str}}
```
Your callback function can use any of the tools initialized in the `__init__` function.
```python
    ...

    def hello_world_intent(self, intent_data):
        """This function is called when the
        intent is detected."""
        self.audio_utils.say("Hello World!")
```

### All together now
```python
from skills import base_skill
from core_utils.core_core.channels import Channels
from core_utils.settings_tool import SettingsTool
from core_utils.audio_utils import AudioUtils

class Skill(base_skill.BaseSkill):
    name = "Hello World Skill"


    def __init__(self, settings_tool: SettingsTool, channels: Channels, audio_utils: AudioUtils):
        """ Initialize the skill. 
         """
        self.settings_tool = settings_tool
        self.channels = channels
        self.audio_utils = audio_utils


     def intent_creator(self, register_intent: callable):
        """ This function registers intents
            Parameters: 
                register_intent (callable): a function that
                can add an intent to Nora. 
            """
            register_intent(
                intent_callback=self.hello_world_intent,
                # This hrase will match 'hello world' or 'hello'.
                intent_phrases=["Hello (world | )"],
                intent_name="say_hello")


    def hello_world_intent(self, intent_data):
        """This function is called when the
        intent is detected."""
        self.audio_utils.say("Hello World!")
```

# How to Write an Intent Phrase
There are two important parts to writing a phrase you need to understand. One, if I want to get user input, I have to include it as an entity in the intent phrase. Two, if I want an intent phrase to match, it needs to be as flexible as possible. 
There is a syntax to writing intent phrases to follow. 
1. Words written without extra syntax will be matched.
If I wrote `intent_phrases = ["Hello world"]`
then it would only match the phrase "Hello world". 
2. The or operator looks like this: `\`. If I wrote, `["Hello (world | planet)"]`, then it would match the phrases "hello world" *and* "hello planet".
3. The or operator works with empty space. `["Hello (world | )"]` then it would match "hello world" and "hello". 
4. Entities can be used to get a specific part of a phrase. `["Hello {name}"]` would match "hello Paul" as well as "hello world". The power behind this is that later, we can get `name` out of the `intent_data`. Let's go into detail below.

### `intent_data`
```python
# intent_data
{'name': str, 'original_phrase': str 'entities': {<entity name>: str, <other entity name>: str}}
```
If I said, "add potatoes to my shopping list" then the intent phrase would be written 
```python
"add {item} to my {list_name} list" 
```
and `intent_data` would be
```python
intent_data = {
    'name': 'add_item',
     'entities': {
        'item': 'potatoes',
         'list_name': 'shopping'
        }
    }
```

You can access it like this: 
```python
item = intent_data['entities'].get("item")
print(item)
# prints "potatoes"
```