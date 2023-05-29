import socket
#import netifaces

class MyIP:
    """
    A class for retrieving the IP address of the local machine.
    """

    def get():
        """
        Retrieves the IP address of the local machine.

        Returns:
            A string containing the IP address of the local machine.
        """
        hostname = socket.gethostname()   
        return socket.gethostbyname(hostname)

        # The code below uses the netifaces library to retrieve the IP address
        # of the local machine for each network interface. However, this code
        # is currently unreachable because of the return statement above.

        # Get a list of all network interfaces
        interfaces = netifaces.interfaces()

        # Iterate over each interface
        for iface in interfaces:
            # Get the IP addresses for this interface
            addrs = netifaces.ifaddresses(iface)
            ip_addrs = addrs.get(netifaces.AF_INET)
            if ip_addrs:
                # Print the first IP address found for this interface
                return ip_addrs[0]['addr']
