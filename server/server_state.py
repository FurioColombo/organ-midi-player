
class ServerState:
    def __init__(self):
        self.parsed_midi_channels = None
        self.com_port = 'COM3'

    def set_parsed_midi_channels(self, data):
        self.parsed_midi_channels = data

    def get_parsed_midi_channels(self):
        return self.parsed_midi_channels

    def set_com_port(self, new_com_port):
        self.com_port = new_com_port

    def get_com_port(self):
        return self.com_port
