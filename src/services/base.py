from abc import ABC, abstractmethod


class Repository(ABC):
    @abstractmethod
    def get(self, *args, **kwargs):
        raise NotImplementedError
    
    @abstractmethod
    def get_multy(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def create(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def update(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def delete(self, *args, **kwargs):
        raise NotImplementedError
