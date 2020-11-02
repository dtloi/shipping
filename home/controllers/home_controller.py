from ..network.Shipping_Utilities import Shipping_Utilities

class HomeController():
    def validate_data(self, req):
        ship_utils = Shipping_Utilities()
        validate_ret = ship_utils.validate_address(req)
        #print(validate_ret)
        return validate_ret
    def get_all_rates(self, req):
        ship_utils = Shipping_Utilities()
        return ship_utils.get_rates(req)