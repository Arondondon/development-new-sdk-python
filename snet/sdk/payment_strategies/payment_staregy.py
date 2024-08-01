import abc


class PaymentStrategy(abc.ABC):

    @abc.abstractmethod
    def get_payment_metadata(self,service_client):
        pass

    @abc.abstractmethod
    def get_price(self,service_client):
        pass
