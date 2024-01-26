import serial

class SerialMessagesHandler:
    def __init__(self, com_port=None):
        self.COM = com_port or 'COM3'
        self.ser = None
        self.init_connection()

    def init_connection(self):
        try:
            print('Initializing connection on', self.COM)
            self.ser = serial.Serial(self.COM, 9600)  # Adjust baudrate as needed
        except Exception as e:
            print("Error opening serial connection:", e)

    def send_message(self, message):
        try:
            if self.ser is None:
                self.init_connection()
            if self.ser.isOpen():
                self.ser.write(message)
            else:
                raise Exception('Serial connection not initialized or closed')
        except Exception as e:
            print("Error sending serial message:", e)

    def close_connection(self):
        try:
            if self.ser is not None and self.ser.isOpen():
                self.ser.close()
        except Exception as e:
            print("Error closing serial connection:", e)

    def change_COM_port(self, com_port):
        self.COM = com_port
        self.close_connection()
        self.init_connection()
