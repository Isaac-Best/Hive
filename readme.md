

Socket Programming Project 3 - Transient Services 

Step 1. Open 4 terminals and execute the main script with the following commands (one in each terminal).
    python .\app_main.py -ip 127.0.0.1 -port 54321 -friendly_name LosAngeles
    python .\app_main.py -ip 127.0.0.1 -port 54322 -friendly_name London
    python .\app_main.py -ip 127.0.0.1 -port 54323 -friendly_name Brisbane
    python .\app_main.py -ip 127.0.0.1 -port 54324 -friendly_name NewYork

Step 2. Once the app starts, type the following from London, Brisbane, and NewYork:
    connect 127.0.0.1 54321

Step 3. In any terminal run the command (give a few seconds for everything to connect)
    propogate_config 

    this will load the hardcoded network configuration file from initial_configuration.json assign it to a config_network_manager
    data member and then propagate it to the currently connected live nodes. 

Step 4 In any terminal you wish to run service checks type 
    run_service_checks

    in order to start the network monitoring threads 

Step 5 In any terminal run 
    list_network_configuration -> to view the netowork configuration of all nodes
    list_current_network_status -> to view the network configuration of the current node as well as some data (in a terminal running service checks)

