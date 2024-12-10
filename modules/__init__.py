class BaseModule:
    def __init__(self, params):
        self.params = params

    def process(self, ssh_client):
        raise NotImplementedError("This method should be overridden in child modules.")
