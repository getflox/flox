class ServiceContainer:
    def __init__(self, flox):
        self.services = {}
        self.flox = flox

    def registry(self, service, tags: list, priority=0):
        for tag in tags:
            if tag not in self.services:
                self.services[tag] = []

            self.services[tag].insert(priority, service)

        return service

    def find(self, tag, name=None):
        services = self.services.get(tag, {})
        if not name:
            return services

        return next(filter(lambda x: x.name == name, services)) or None

    def get(self, tag):
        return next(iter(self.find(tag))) or None


