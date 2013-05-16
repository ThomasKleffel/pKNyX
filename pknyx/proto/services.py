"""
Renommer en ServicesManager
"""


class Services(object):
    """
    """
    def __init__(self):
        """
        """
        self._configFile = None

        self.configServer = None
        self.persistentStorage = None
        self.timers = None
        self.smsGateway = None
        self.emailGateway = None
        self.knxConnection = None
        self.exceptionDays = None
        self.locationInfo = None

    def loadconfig(self):
        """
        """

    def saveConfig(self):
        """
        """

    def start():
        """
        """
        print("TRACE::Services.start()")
        self.timers.startManager()
        self.knxConnection.startConnection()  # -> start()

    def stop():
        """
        """
        print("TRACE::Services.stop()")
        self._timers.stopManager()
        self._knxConnection.stopConnection()
