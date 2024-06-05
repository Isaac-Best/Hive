from base_message import BaseMessage
from hive_node import HiveNode
from typing import Dict

class ConfigMessage(BaseMessage):
    """
    ConfigMessage represents a message for config protocol in the Hive network.

    Attributes:
    ----------
    sender : HiveNode
        The sender node of the message.
    recipient : HiveNode
        The recipient node of the message.
    """

    def __init__(self, sender: HiveNode, recipient: HiveNode, message: str):
        """
        Initializes a new instance of ConfigMessage.

        Parameters:
        ----------
        sender : HiveNode
            The sender node of the message.
        recipient : HiveNode
            The recipient node of the message.
        message : json config info for the network service 
        """
        super().__init__(sender, recipient, 'config')
        self.message: str = message

    def to_dict(self) -> Dict[str, dict]:
        """
        Converts the ConfigMessage instance to a dictionary representation.

        Returns:
        -------
        Dict[str, dict]
            A dictionary representing the ConfigMessage instance.
        """
        base_dict: Dict[str, dict] = super().to_dict()
        base_dict.update({'message': self.message})
        return base_dict