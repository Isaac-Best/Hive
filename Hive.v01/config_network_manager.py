

from logger import Logger
from hive_node_manager import HiveNodeManager
from message_queue import MessageQueue
from service_script import ServiceMonitor
from config_message import ConfigMessage
from hive_message import HiveMessage
from app_settings import AppSettings

class ConfigNetworkManager:
    """
    ConfigNetworkManager manages the network services and configurations for the Hive network.

    Attributes:
    ----------
    logger : Logger
        An instance of the Logger class for logging messages.
    hive_node_manager : HiveNodeManager
        Manages the nodes in the Hive network.
    outbound_message_queue : MessageQueue
        A queue for outbound messages.
    service_monitor : ServiceMonitor
        Monitors the network services.
    """

    def __init__(self, hive_node_manager: HiveNodeManager, outbound_message_queue: MessageQueue):
        """
        Initializes a new instance of ConfigProtocolCommandManager.

        Parameters:
        ----------
        hive_node_manager : HiveNodeManager
            Manages the nodes in the Hive network.
        outbound_message_queue : MessageQueue
            A queue for outbound messages.
        network_config : dict
            The configuration for ALL the network services.
        service_monitor : ServiceMonitor
            Monitors the network services.
        threads : list
            A list of threads for running the service checks. Easier to close out and restart access when changes are made
        """
        self.logger: Logger = Logger()
        self.hive_node_manager: HiveNodeManager = hive_node_manager
        self.outbound_message_queue: MessageQueue = outbound_message_queue

        self.network_config = None
        self.service_monitor = ServiceMonitor()
        self.threads = []

        self.logger.debug("ConfigProtocolCommandManager", "ConfigProtocolCommandManager initialized...")

    def set_config(self, config: dict) -> None:
        """
        Sets the configuration for the network services. If there are any current service checks running -> join and close the threads to clear current configuration.

        Parameters:
        ----------
        config : dict
            The configuration for the network services.
        """
        if self.threads:
            for thread in self.threads:
                thread.join()

        self.network_config = config
    
    def get_config(self) -> dict:
        """
        Gets the configuration for the network services.

        Returns:
        ----------
        config : dict
            The configuration for the network services.
        """
        return self.network_config
    
    
    def run_service_checks(self) -> None:
        """
        Starts the service checks for the network services that matches the local node name.
        """
        # self.logger.info("ConfigProtocolCommandManager", f"local node name: {self.hive_node_manager.local_node.friendly_name}")
        # self.logger.info("ConfigProtocolCommandManager", f"network config: {self.network_config}")

        self.threads = self.service_monitor.initialize_monitoring(self.network_config[self.hive_node_manager.local_node.friendly_name])

    def propogate_config(self) -> None:
        """
        Propogates the configuration to all nodes in the network.
        """
        self.logger.info("ConfigProtocolCommandManager", "Propogating configuration to all nodes in the network...")

        for node in self.hive_node_manager.get_all_live_nodes():        
            if node.friendly_name != self.hive_node_manager.local_node.friendly_name:
                self.logger.info("ConfigProtocolCommandManager", f"Propogating configuration to {node.friendly_name}...")
                config_message = ConfigMessage(
                    sender=self.hive_node_manager.local_node,
                    recipient=node,
                    message=self.network_config
                )
                new_hive_message = HiveMessage(config_message)
                self.outbound_message_queue.enqueue(new_hive_message)
    
    def list_network_configuration(self) -> None:
        """
        Logs the network configuration.
        """
        self.logger.info("ConfigProtocolCommandManager", "-" * AppSettings.LOG_LINE_WIDTH)
        self.logger.info("ConfigProtocolCommandManager", "Network Configuration")
        self.logger.info("ConfigProtocolCommandManager", "-" * AppSettings.LOG_LINE_WIDTH)
        for node_name, node_config in self.network_config.items():
            self.logger.info("ConfigProtocolCommandManager", f"Node: {node_name}")
            self.logger.info("ConfigProtocolCommandManager", f"Services: {node_config}")
        self.logger.info("ConfigProtocolCommandManager", "-" * AppSettings.LOG_LINE_WIDTH)


    def list_current_network_status(self) -> None:
        """
        Logs the current status of the network services.
        """
        self.logger.info("ConfigProtocolCommandManager", "-" * AppSettings.LOG_LINE_WIDTH)
        self.logger.info("ConfigProtocolCommandManager", "Current Network Status")
        self.logger.info("ConfigProtocolCommandManager", "-" * AppSettings.LOG_LINE_WIDTH)
        current_status = self.service_monitor.get_status()
        for key, info in current_status.items():
            service_type, identifier = key.split('&')
            self.logger.info("ConfigProtocolCommandManager", f"{service_type} ({identifier}): Last Run at {info['last_run']}, Result: {info['result']}")
        self.logger.info("ConfigProtocolCommandManager", "-" * AppSettings.LOG_LINE_WIDTH)

