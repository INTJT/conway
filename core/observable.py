class Observable:

    def _set_events(self, events):
        self._observers = {event: set() for event in events}

    def add_observer(self, event, observer):
        self._observers[event].add(observer)

    def remove_observer(self, event, observer):
        self._observers[event].remove(observer)

    def notify(self, event):
        for observer in self._observers[event]:
            observer()
