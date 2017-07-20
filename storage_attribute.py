from abc import ABC, abstractmethod
from ipaddress import ip_address


class StorageAttribute(ABC):
    def __init__(self, server, storage_ip, lower, upper):
        if lower > upper or lower < 0 or upper < 0:
            raise ValueError('Invalid lower and upper value')
        try:
            ip_address(storage_ip)
        except:
            raise ValueError('Invalid IP address')
        self.lower = lower
        self.upper = upper
        self.server = server
        self.storage_ip = storage_ip
        super(StorageAttribute, self).__init__()

    @classmethod
    @abstractmethod
    def remove(self):
        pass
