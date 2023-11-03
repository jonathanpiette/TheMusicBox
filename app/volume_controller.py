class VolumeController:
    def __init__(self, gpio_manager, audio_manager):
        self.gpio_manager = gpio_manager
        self.audio_manager = audio_manager
        self.last_state = None

    def setup(self, clk_pin, dt_pin, sw_pin):
        self.clk_pin = clk_pin
        self.dt_pin = dt_pin
        self.sw_pin = sw_pin
        self.last_state = self.gpio_manager.read_pin(self.clk_pin)

    def volume_control_callback(self, channel):
        clk_state = self.gpio_manager.read_pin(self.clk_pin)
        dt_state = self.gpio_manager.read_pin(self.dt_pin)
        if clk_state != self.last_state:
            if dt_state != clk_state:
                self.audio_manager.set_volume(min(self.audio_manager.get_volume() + 0.05, 1.0))
            else:
                self.audio_manager.set_volume(max(self.audio_manager.get_volume() - 0.05, 0.0))
            self.last_state = clk_state
