import easypost
import config


easypost.api_key = config.EASYPOST_API


class Shipping_Utilities():
    def validate_address(self, req):
        # Create and verify an address.
        sender_address = easypost.Address.create(
            verify= ['delivery'],
            street1= req["sender_address_1"],
            street2= req["sender_address_2"],
            city= req["sender_city"],
            state= req["sender_state"],
            zip= req["sender_zip_code"],
            country= req["sender_country"],
        )
        recipient_address = easypost.Address.create(
            verify=['delivery'],
            street1=req["recipient_address_1"],
            street2=req["recipient_address_2"],
            city=req["recipient_city"],
            state=req["recipient_state"],
            zip=req["recipient_zip_code"],
            country=req["recipient_country"],
        )
        return {"sender":
                     [sender_address["verifications"]["delivery"]["success"],
                    sender_address["verifications"]["delivery"]["errors"]],
                "recipient":
                     [recipient_address["verifications"]["delivery"]["success"],
                    recipient_address["verifications"]["delivery"]["errors"]]}

    def get_rates(self, req):
        customs_info = {}
        if req["recipient_country"] != req["sender_country"]:
            customs_info = easypost.CustomsInfo.create(
                eel_pfc='NOEEI 30.37(a)',
                customs_certify=True,
                customs_signer='Steve Brule',
                contents_type='merchandise',
                contents_explanation='',
                restriction_type='none',
                restriction_comments='',
                non_delivery_option='abandon',
                customs_items=[{
                    'description': 'Sweet shirts',
                    'quantity': 1,
                    'hs_tariff_number': '654321',
                    'origin_country': 'US'
                }]
            )
        shipment = easypost.Shipment.create(
            to_address={
                "street1": req["recipient_address_1"],
                "street2": req["recipient_address_2"],
                "city": req["recipient_city"],
                "state": req["recipient_state"],
                "zip": req["recipient_zip_code"],
                "country": req["recipient_country"],
            },
            from_address={
                "street1": req["sender_address_1"],
                "street2": req["sender_address_2"],
                "city": req["sender_city"],
                "state": req["sender_state"],
                "zip": req["sender_zip_code"],
                "country": req["sender_country"],
                "residential": req["recipient_resident"],
            },
            parcel={
                "length": req["length"],
                "width": req["width"],
                "height": req["height"],
                "weight": int(req["weight"])
            },
            customs_info=customs_info
        )
        ret = {}
        rates = shipment.get_rates()["rates"]
        #print(rates)
        for rate in rates:
            # print(rate)
            if rate["carrier"] not in ret:
                ret[rate["carrier"]] = [{
                    rate["service"] : {"Listed": [rate["list_currency"],rate["list_rate"]],
                                       "Regular": [rate["currency"],rate["rate"]],
                                       "Retail": [rate["retail_currency"],rate["retail_rate"]]}
                }]
            else:
                ret[rate["carrier"]].append({
                    rate["service"]: {"Listed": [rate["list_currency"], rate["list_rate"]],
                                      "Regular": [rate["currency"], rate["rate"]],
                                      "Retail": [rate["retail_currency"], rate["retail_rate"]]}
                })
        print(ret)
        return ret
