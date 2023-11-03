import board
from adafruit_pn532.i2c import PN532_I2C

class NFCManager:
    def __init__(self):
        i2c = board.I2C()
        self.nfc = PN532_I2C(i2c)
        self.nfc.SAM_configuration()

    def read_nfc_tag(self, display_callback=None):
        try:
            tag_id = self.nfc.read_passive_target(timeout=0.5)
            if tag_id:
                tag_id_hex = bytes(tag_id).hex()
                if display_callback:
                    display_callback(f"Tag {tag_id_hex} read")
                return tag_id_hex
        except RuntimeError as e:
            print(f"Error reading NFC tag: {e}")
        return None
