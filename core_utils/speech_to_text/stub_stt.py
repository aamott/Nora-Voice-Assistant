#######################################
# Stub Speech to Text
#  Acts as a stand-in for the real STT module
#######################################


class STT:
    # The id of the object as it will appear in the json
    name = "Stub_STT"

    def __init__(self):
        # Initialize stuff for speech recognition
        pass

    def listen(self):
        text = "Hello, world!"
        return text
