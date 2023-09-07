from controllers.controller import Controller


class OthersController(Controller):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def load_config(self):
        self.config.load()

        self.gui.spin_volume.setValue(self.config.volume)
