import socket


class SocketHelper:
    def __init__(self):
        self.local_ip = self.get_local_ip_address()

    def get_local_ip_address(self):
        try:
            # Create a temporary socket
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as temp_socket:
                temp_socket.connect(
                    ("192.168.100.27", 6000)
                )  # Connect to a known address
                local_ip_address = temp_socket.getsockname()[0]  # Get local IP address
                print(local_ip_address)
                return local_ip_address
        except socket.error as e:
            print("Error occurred while retrieving local IP address:", e)
            return None

    def UDPSend(self, cmd, targetIP, targetPort):
        try:
            with socket.socket(socket.AF_INET, type=socket.SOCK_DGRAM) as udp:
                print(self.local_ip)
                udp.connect((targetIP, targetPort))

                udp.sendto(str.encode(cmd), (targetIP, targetPort))
                print(udp.sendto(str.encode(cmd), (targetIP, targetPort)))
            print("sent")
        except:
            pass

    def UDPReceive(self, IP=None, PORT=None):
        if IP is None:
            IP = self.local_ip
            if PORT is None:
                PORT = 6000

        try:
            with socket.socket(socket.AF_INET, type=socket.SOCK_DGRAM) as udp:
                udp.bind((IP, PORT))
                udp.settimeout(1)
                data, addr = udp.recvfrom(1024)
                return data.decode(), addr[0], addr[1]
        except:
            pass

    def return_ip(self):
        ip = self.get_local_ip_address()
        return ip
