import threading
import time
from serial_messages import SerialMessagesHandler

class ParsedMidiSerialPlayer:
    def __init__(self):
        self.serial_messages_handler = SerialMessagesHandler()
        self.init_lock = threading.Lock()
        self.bpm = 120
    
    def ticksMs2Seconds(self, ticks):
        return ticks/1000

    def play(self, midi_messages):
        print('player scheduling messages play')
        start_time = time.time()

        for message in midi_messages:
            # Unused variable, consider removing if not needed
            time_label = self.ticksMs2Seconds(round(message['time']))
            serial_note = message['serialNote']
            velocity = message['velocity']
            # print(round(message['time']), '-', time_label)

            elapsed_time = time.time() - start_time
            time_to_wait = max(0, time_label/1000 - elapsed_time)
            time.sleep(time_to_wait)
            self.play_serial_message(serial_note, velocity)

    def play_serial_message(self, serial_note, velocity):
        with self.init_lock:
            if self.serial_messages_handler is not None:
                print(f"Play: SerialNote {serial_note}, Velocity {velocity}")
                # self.serial_messages_handler.send_message(serial_note)  # TODO: uncomment this! to send serial messages
                pass
            else:
                print("Serial Messages Handler is not initialized.")
