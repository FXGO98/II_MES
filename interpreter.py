from pymodbus.client.sync import ModbusTcpClient
import socketserver
import opcua
import order

#CODE = "DESKTOP-G84C5PG"
CODE = "FXGO"
PORT = "4840"


class Interpreter:
    def __init__(self):
        self.transmitter = None
        pass

    def check_recv(self):
        raise Exception

    def send(self, Message):
        raise Exception

    def shutdown(self):
        pass


class ModbusInterpreter(Interpreter):
    def __init__(self):
        self.transmitter = ModbusTcpClient("127.0.0.1", 5502)

        if self.transmitter.connect():
            print("Connected to server!")
        else:
            print("Could not connect to server!")

    def shutdown(self):
        self.transmitter.close()


class OPC_UA_Interpreter(Interpreter):
    def __init__(self):
        self.transmitter = opcua.Client("opc.tcp://{}:{}".format(CODE, PORT))
        try:
            self.transmitter.connect()
            self.root = self.transmitter.get_root_node()
            # print("Object node is: {}".format(self.root))
            print('OPC-UA Interpreter initialized successfully!')
        except Exception as e:
            print(e)

    def shutdown(self):
        self.transmitter.disconnect()


class UDPServerEx(socketserver.UDPServer):
    def handle_timeout(self):
        # print('Timed out!')
        return None

    # Override in order to return the request itself
    def _handle_request_noblock(self):
        request = None
        try:
            request, client_address = self.get_request()
        except OSError:
            return None

        if self.verify_request(request, client_address):
            try:
                self.process_request(request, client_address)
            except Exception:
                self.handle_error(request, client_address)
                self.shutdown_request(request)
                return None
        else:
            self.shutdown_request(request)
            return None

        return request


class UDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        pass
        # self.request = ET.fromstring(self.request[0])
        # print('handle(): got "{}"'.format(type(self.request)))


class XMLInterpreter(Interpreter):
    def __init__(self):
        self.handler = UDPHandler
        self.transmitter = UDPServerEx(("127.0.0.1", 54321), self.handler)
        self.transmitter.timeout = 0.05
        print('XML Interpreter initialized successfully!')

    def recv(self):
        try:
            request = self.transmitter.handle_request()
            if request is None:
                return None
            print("request received!")
            return order.from_XML(request[0])
        except Exception as e:
            print(e)
            return None

    def shutdown(self):
        self.transmitter.server_close()
