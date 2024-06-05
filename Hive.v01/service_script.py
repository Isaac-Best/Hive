import network_monitoring_functions
import threading 
import time
from logger import Logger


# Map the service type to the corresponding monitoring function
monitoring_functions_map = {
    "HTTP": network_monitoring_functions.check_server_http,
    "HTTPS": network_monitoring_functions.check_server_https,
    "ICMP": network_monitoring_functions.ping,
    "DNS": network_monitoring_functions.check_dns_server_status,
    "NTP": network_monitoring_functions.check_ntp_server,
    "TCP": network_monitoring_functions.check_tcp_port,
    "UDP": network_monitoring_functions.check_udp_port
}

# Map the service type to the required arguments
monitoring_functions_args_map = {
    "HTTP": ["url"],
    "HTTPS": ["url"],
    "ICMP": ["hostname"],
    "DNS": ["dns_server", "dns_query", "dns_record_type"],
    "NTP": ["hostname"],
    "TCP": ["server_address", "port_number"],
    "UDP": ["server_address", "port_number"]
}


class ServiceMonitor:
    """
    ServiceMonitor is a class that runs the service checks for the network services.

    Attributes:
    ----------
    logger : Logger
        An instance of the Logger class for logging messages.
    """
    def __init__(self):
        self.logger = Logger()
        self.statuses = {}
        self.status_lock = threading.Lock()

    def service_wrapper(self, service_type, monitoring_function, frequency, *args):
        arg_names = monitoring_functions_args_map[service_type]
        arg_dict = {arg_name: arg for arg_name, arg in zip(arg_names, args)}
        identifier = arg_dict.get('url') or arg_dict.get('hostname') or arg_dict.get('server_address') or arg_dict.get('dns_server')

        while True:
            result = monitoring_function(*args)
            self.update_status(service_type, identifier, result[0])
            if service_type == "HTTP":
                self.logger.info("ServiceMonitor", f"URL: {arg_dict.get('url')} - HTTP server status: {result[0]}, HTTP response code: {result[1]}")
            elif service_type == "HTTPS":
                self.logger.info("ServiceMonitor", f"URL: {arg_dict.get('url')} - HTTPS server status: {result[0]}, HTTPS response code: {result[1]}, Description: {result[2]}")
            elif service_type == "ICMP":
                self.logger.info("ServiceMonitor", f"Hostname: {arg_dict.get('hostname')} - Ping address: {result[0]}, Ping time: {result[1]}")
            elif service_type == "DNS":
                self.logger.info("ServiceMonitor", f"DNS Server: {arg_dict.get('dns_server')} - DNS server status: {result[0]}, DNS query results: {result[1]}")
            elif service_type == "NTP":
                self.logger.info("ServiceMonitor", f"Hostname: {arg_dict.get('hostname')} - NTP server status: {result[0]}, NTP server time: {result[1]}")
            elif service_type == "TCP":
                self.logger.info("ServiceMonitor", f"Server Address: {arg_dict.get('server_address')} - TCP port status: {result[0]}, TCP port description: {result[1]}")
            elif service_type == "UDP":
                self.logger.info("ServiceMonitor", f" Server Address: {arg_dict.get('server_address')} - UDP port status: {result[0]}, UDP port description: {result[1]}")
            
            time.sleep(frequency)


    def initialize_monitoring(self, service_configs: dict) -> list[threading.Thread]:
        threads = []
        for service in service_configs:
            if service["type"] in monitoring_functions_map:
                monitoring_function = monitoring_functions_map[service["type"]]
                # maps assigned parameters to the function
                args = tuple(service[param] for param in monitoring_functions_args_map[service["type"]])
                thread = threading.Thread(target=self.service_wrapper, args=(service["type"], monitoring_function, service["frequency"], *args), daemon=True)
                thread.start()
                threads.append(thread)
            else:
                print(f"Unsupported service type: {service['type']}")
                continue

        return threads

    def update_status(self, service_type, identifier, result):
        key = f"{service_type}&{identifier}"
        with self.status_lock:
            self.statuses[key] = {
                'last_run': time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
                'result': result
            }


    def get_status(self):
        with self.status_lock:
            return self.statuses
