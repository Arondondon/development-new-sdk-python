from snet.sdk.contract.contract import *


class RegistryContract(EthContract):
    def __init__(self, w3: web3.Web3, address: str = None):
        super().__init__(w3, "Registry", address)

    def get_org_by_id(self, org_id: str): # -> dict:
        return self.contract.functions.getOrganizationById(org_id).call()

    def get_service_registration_by_id(self, org_id: str, service_id: str): # -> dict:
        return self.contract.functions.getServiceRegistrationById(org_id, service_id).call()

    def list_organizations(self): # -> list[dict]:
        return self.contract.functions.listOrganizations().call()

    def list_services_by_organization(self, org_id: str): # -> list[dict]:
        return self.contract.functions.listServices(org_id).call()

    def supports_interface(self, interface_id: str): # -> bool:
        return self.contract.functions.supportsInterface(interface_id).call()

    # TODO: implement write methods

