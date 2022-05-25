# Nora-Voice-Assistant
Nora is a voice assistant built on the concept of modularity, ease of design and development, and a flexible and extensible architecture. Its original intent was to explore the concept of a web UI that allows for a user to edit routines (and even skills themselves) through the user of a block programming language. Now, this Web UI is planned to take over settings as well, and in the future may include a text-based way to interact with the voice assistant. 


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

## Background
Nora is built off of modular components. Each piece (i.e. speech recognition, text to speech, etc.) should be able to be replaced by another module accepting and receiving the same data and continue to function without any changes to the outside code. 
Skills are the core concept of a voice assistant. Each skill is a set of related functions a user can call on. For example, a music player skill might allow the user to say, “play Party in the USA” as well as “pause the music.” Skills should be developable by almost anyone with a basic knowledge of coding.



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
- [ ] Web Server 🚀
- [ ] Skill Editor 📝
- [ ] Settings Manager Frontend 🔧