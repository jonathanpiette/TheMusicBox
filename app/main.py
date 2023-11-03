from gpio_manager import GPIOManager
from audio_manager import AudioManager
from nfc_manager import NFCManager
from volume_controller import VolumeController
from display_manager import DisplayManager
import config

def main():
    # Setup managers
    gpio_manager = GPIOManager(config.PIN_CONFIG)
    audio_manager = AudioManager()
    nfc_manager = NFCManager()
    display_manager = DisplayManager()

    # Volume controller setup
    volume_controller = VolumeController(gpio_manager, audio_manager)
    volume_controller.setup(config.CLK_PIN, config.DT_PIN, config.SW_PIN)

    # Add volume control event callbacks
    gpio_manager.add_event_callback(config.CLK_PIN, volume_controller.volume_control_callback)
    
    def display_nfc_read_message(message):
        display_manager.display_message(message)

    try:
        # Main loop
        while True:
            tag_id = nfc_manager.read_nfc_tag(display_callback=display_nfc_read_message)
            if tag_id:
                audio_manager.play_audio(f"audio/{tag_id}.mp3")
            
            # Other main application logic here

    except KeyboardInterrupt:
        print("Program stopped by user")
    finally:
        gpio_manager.cleanup()

if __name__ == "__main__":
    main()
