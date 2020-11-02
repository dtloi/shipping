import json
import os

from fedex.config import FedexConfig
from fedex.services.address_validation_service import FedexAddressValidationRequest
from fedex.services.country_service import FedexValidatePostalRequest
from fedex.services.rate_service import FedexRateServiceRequest
from fedex.tools.conversion import sobject_to_json

CONFIG_OBJ = FedexConfig(key=os.getenv("FEDEX_KEY"),
                         password=os.getenv("FEDEX_PASSWORD"),
                         account_number=os.getenv("FEDEX_ACC_NUM"),
                         meter_number=os.getenv("FEDEX_METER_NUM"))

class Fedex():
    service_types = ["EUROPE_FIRST_INTERNATIONAL_PRIORITY",
                    "INTERNATIONAL_PRIORITY",
                    "INTERNATIONAL_ECONOMY",
                    "FEDEX_2_DAY",
                    "FEDEX_2_DAY_AM",
                    "STANDARD_OVERNIGHT",
                    "FIRST_OVERNIGHT",
                    "PRIORITY_OVERNIGHT",
                    ]
    residential_service_types = ["GROUND_HOME_DELIVERY", ]

    packaging_types = ["YOUR_PACKAGING",
                      "FEDEX_10KG_BOX",
                      "FEDEX_25KG_BOX",
                      "FEDEX_BOX",
                      "FEDEX_ENVELOPE",
                      "FEDEX_EXTRA_LARGE_BOX",
                      "FEDEX_LARGE_BOX",
                      "FEDEX_MEDIUM_BOX",
                      "FEDEX_PAK",
                      "FEDEX_SMALL_BOX",
                      "FEDEX_TUBE",
                      ]
    def get_rates(self, req):
        rate = FedexRateServiceRequest(CONFIG_OBJ)

        rate.RequestedShipment.Shipper.Address.StreetLines = req["sender_address"]#["3035 Baronscourt Way"]
        rate.RequestedShipment.Shipper.Address.City = req["sender_city"]#"San Jose"
        rate.RequestedShipment.Shipper.Address.StateOrProvinceCode = req["sender_state"]#'CA'
        rate.RequestedShipment.Shipper.Address.PostalCode = req["sender_zip_code"]#'95132'
        rate.RequestedShipment.Shipper.Address.CountryCode = req["sender_country"]#'US'

        rate.RequestedShipment.Recipient.Address.StreetLines = req["recipient_address"]  # ["3035 Baronscourt Way"]
        rate.RequestedShipment.Recipient.Address.City = req["recipient_city"]  # "San Jose"
        rate.RequestedShipment.Recipient.Address.StateOrProvinceCode = req["recipient_state"] #'NC'
        rate.RequestedShipment.Recipient.Address.PostalCode = req["recipient_zip_code"]#'27577'
        rate.RequestedShipment.Recipient.Address.CountryCode = req["recipient_country"]#'US'

        rate.RequestedShipment.EdtRequestType = 'NONE'
        rate.RequestedShipment.ShippingChargesPayment.PaymentType = 'SENDER'

        rate.RequestedShipment.EdtRequestType = "NONE"
        rate.RequestedShipment.DropoffType = 'REGULAR_PICKUP'
        rate.RequestedShipment.PackagingType = 'YOUR_PACKAGING'

        package1_weight = rate.create_wsdl_object_of_type('Weight')
        package1_weight.Value = float(req["weight"])#1.0
        package1_weight.Units = req["unit"]#"LB"
        package1 = rate.create_wsdl_object_of_type('RequestedPackageLineItem')
        package1.Weight = package1_weight
        package1.PhysicalPackaging = 'BOX'
        package1.GroupPackageCount = 1
        rate.add_package(package1)

        available_service_types = {}
        for service in self.service_types:
            try:
                rate.RequestedShipment.ServiceType = service
                rate.send_request()
                response_json = json.loads(sobject_to_json(rate.response))
                # print(response_json["RateReplyDetails"][0]["RatedShipmentDetails"][0]["ShipmentRateDetail"]["TotalNetChargeWithDutiesAndTaxes"])
                available_service_types[service] = response_json["RateReplyDetails"][0]["RatedShipmentDetails"][0]["ShipmentRateDetail"][
                    "TotalNetChargeWithDutiesAndTaxes"]
            except:
                print(str(service))
                continue

        return available_service_types
    def validate_address(self):
        avs_request = FedexAddressValidationRequest(CONFIG_OBJ)
        address1 = avs_request.create_wsdl_object_of_type('AddressToValidate')
        address1.Address.StreetLines = ['155 Old Greenville Hwy', 'Suite 103']
        address1.Address.City = 'Clemson'
        address1.Address.StateOrProvinceCode = 'SC'
        address1.Address.PostalCode = 29631
        address1.Address.CountryCode = 'US'
        address1.Address.Residential = False
        avs_request.add_address(address1)

        avs_request.send_request()
        return avs_request.response


#test = Fedex()
#ret = test.get_rates()
#print(ret)
#ret = test.validate_address()
#print(ret)
#response_json = sobject_to_json(ret)
#print(response_json)
#print(test.validatePostalCode())