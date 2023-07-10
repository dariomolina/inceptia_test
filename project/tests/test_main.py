import unittest
from unittest import mock

from project.main import GeoAPI, Product, Discount
from project.tests.constants import GEO_API_MOCK


class MockResponse:
    def __init__(self, status_code, json_data):
        self.status_code = status_code
        self.json_data = json_data

    def json(self):
        return self.json_data

    def raise_for_status(self):
        pass


class TestMain(unittest.TestCase):

    @mock.patch('requests.get')
    def test_geo_api(self, mock_response):
        geo_api_json_is_hot = GEO_API_MOCK.copy()
        geo_api_json_is_hot["main"]["temp"] = 40
        mock_response.return_value = MockResponse(status_code=200, json_data=geo_api_json_is_hot)
        is_hot = GeoAPI.is_hot_in_pehuajo()

        geo_api_json_is_cold = GEO_API_MOCK.copy()
        geo_api_json_is_cold["main"]["temp"] = 4
        mock_response.return_value = MockResponse(status_code=200, json_data=geo_api_json_is_cold)
        is_cold = GeoAPI.is_hot_in_pehuajo()

        self.assertTrue(is_hot)
        self.assertFalse(is_cold)

    def test_is_product_available(self):
        is_available_true = Product.is_product_available("Chocolate", 3)
        is_available_true_2 = Product.is_product_available("Dulce de Leche", 0)
        is_available_false = Product.is_product_available("Chocolate", 100)
        is_available_false_3 = Product.is_product_available("chicle", 50)

        self.assertTrue(is_available_true)
        self.assertFalse(is_available_false)
        self.assertTrue(is_available_true_2)
        self.assertFalse(is_available_false_3)

    def test_validate_discount_code(self):
        is_valid_code = Discount.validate_discount_code("primavera2021")
        is_invalid_code = Discount.validate_discount_code("priMaveRa2021")
        self.assertTrue(is_valid_code)
        self.assertFalse(is_invalid_code)
