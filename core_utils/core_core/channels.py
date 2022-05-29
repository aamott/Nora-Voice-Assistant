#################################################
# Channels
# This class manages channels that allow skills to communicate with each other.
# A similar concept is used in ROS.
# A channel class contains two methods:
#   - publish(message, channel_name)
#   - subscribe(callback, channel_name)
#################################################
from inspect import signature

class Channels:
    def __init__(self):
        self.channels = {}

    def publish(self, message, channel_name: str):
        """ Publish a message to a channel.
            Before calling a callback, the message is checked to see if it matches the signature of the callback.
            If it does not, the callback is not called and execution continues.

        Args:
            message: The message to be published. Can be a string, a list, a number, etc.
            channel_name (str): The name of the channel to publish to.
        """
        channel = self.channels.get(channel_name)
        if channel:
            for callback in channel:
                # Check if message is of the same type as the callback's first parameter
                sig = signature(callback)
                if sig.parameters[0].annotation == type(message):
                    callback(message)


    def subscribe(self, callback: callable, channel_name: str) -> bool:
        """ Subscribe to a channel.

        Args:
            callback (callable): The callback to be called when a message is published to the channel.
                                        Must have only one parameter, which is the message.
            channel_name (str): The name of the channel to subscribe to.
        Returns:
            bool: True if the callback was successfully subscribed to the channel, False otherwise.
        """
        if channel_name not in self.channels:
            self.channels[channel_name] = []
        
        # Check that the callback has only one parameter
        sig = signature(callback)
        if len(sig.parameters) != 1:
            return False
        else:
            self.channels[channel_name].append(callback)
            return True


    def unsubscribe(self, callback: callable, channel_name: str) -> bool:
        """ Unsubscribe from a channel.

        Args:
            callback (callable): The callback to be removed from the channel.
            channel_name (str): The name of the channel to unsubscribe from.

        Returns:
            bool: True if the callback was unsubscribed from the channel, False if the callback was not subscribed to the channel.
        """
        if channel_name in self.channels:
            self.channels[channel_name].remove(callback)
            return True
        else:
            return False


    def get_channels(self):
        """ Get names of all the channels."""
        return self.channels.keys()



################
# Test
if __name__ == "__main__":
    channel = Channels()
    def callback(message):
        print(message)
    channel.subscribe(callback, "test")
    channel.publish("Hello", "test")