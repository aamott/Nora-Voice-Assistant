#################################################
# Channels
# This class manages channels that allow skills to communicate with each other.
# A similar concept is used in ROS.
# A channel class contains two methods:
#   - publish(message, channel_name)
#   - subscribe(callback, channel_name)
#################################################
import inspect


class Channels:
    def __init__(self):
        self.channels = {}

    def publish(self, message: str, channel_name: str):
        """ Publish a message to a channel.

        Args:
            message (str): The message to be published.
            channel_name (str): The name of the channel to publish to.
        """
        if channel_name in self.channels:
            for callback in self.channels[channel_name]:
                callback(message)


    def subscribe(self, callback: callable, channel_name: str):
        """ Subscribe to a channel.

        Args:
            callback (callable): The function be called when a message is published to the channel.
                                    The function must take one argument, the message.
            channel_name (str): The name of the channel to subscribe to.
        """
        # check that the callback signature includes an argument for the message
        callback_args = inspect.signature(callback).parameters
        if len(callback_args) == 0:
            raise ValueError("Callback function must take one argument, the message.")
        # if there are any other agruments, see if they have default values.
        if len(callback_args) > 1:
            if callback_args[1].default == inspect.Parameter.empty:
                raise ValueError("Callback function must take one argument, the message.")

        # check if the callback is already subscribed to the channel
        if channel_name not in self.channels:
            self.channels[channel_name] = []
        self.channels[channel_name].append(callback)


    def unsubscribe(self, callback: callable, channel_name: str):
        """ Unsubscribe from a channel.

        Args:
            callback (callable): The callback callable to be removed from the channel.
            channel_name (str): The name of the channel to unsubscribe from.
        """
        if channel_name in self.channels:
            self.channels[channel_name].remove(callback)


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