import datetime

from django.test import TestCase
from django.utils import timezone

from .network.Shipping_Utilities import Shipping_Utilities

class QuestionModelTests(TestCase):

    def test_domestic_shipment(self):
        ship = Shipping_Utilities()
        req = {'sender_address_1': '1165 St. John Street',
               'sender_address_2': '',
               'sender_city': 'Drake ',
               'sender_zip_code': 'S4P3Y2 ',
               'sender_country': 'CA',
               'sender_state': 'Saskatchewan ',
               'recipient_address_1': '3386 Nelson Street',
               'recipient_address_2': '',
               'recipient_city': 'Connaught',
               'recipient_zip_code': 'Ontario',
               'recipient_country': 'US',
               'recipient_state': 'CA',
               'recipient_resident': 'on',
               'height': '1', 'width': '3', 'length': '4', 'weight': '2', 'unit': 'LB'}
        errors = ship.validate_address(req)

        #time = timezone.now() + datetime.timedelta(days=30)
        #future_question = Question(pub_date=time)
        #self.assertIs(future_question.was_published_recently(), False)