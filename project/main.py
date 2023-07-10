import os

import pandas as pd
import requests
from requests import HTTPError

from decorators import ValidateRequests


class GeoAPI:
    url = os.environ.get('OPEN_WEATHER_MAP_URL', '')
    params_openweathermap = {
        "appid": os.environ.get('API_KEY', ''),
        "lat": "-35.836948753554054",
        "lon": "-61.870523905384076",
        "units": "metric",
    }

    @classmethod
    def is_hot_in_pehuajo(cls):
        """
        Method to obtain the temperature of Pehuajó.
        :return: (bool) Returns true if the temperature is higher than 28 degrees Celsius.
        """
        is_hot = False
        response = requests.get(url=cls.url, params=cls.params_openweathermap)
        try:
            response.raise_for_status()
            temperature = response.json()["main"]["temp"]
            if temperature > 28:
                is_hot = True
        except HTTPError:
            pass
        return is_hot


class Product:
    _PRODUCT_DF = {
        "product_name": [
            "Chocolate",
            "Granizado",
            "Limon",
            "Dulce de Leche"
        ],
        "quantity": [3, 10, 0, 5]
    }
    df = pd.DataFrame(_PRODUCT_DF)

    incorrect_requests = 0

    @classmethod
    @ValidateRequests(incorrect_requests=incorrect_requests)
    def is_product_available(cls, product_name, quantity):
        """
        Method to verify if a product is available.
        In the case of an infinite loop, you can count the
        number of incorrect requests up to a maximum of 3.
        :param product_name: (str) product name to filter
        :param quantity: (int) quantity of the product to filter
        :return: (bool) Return True if the product exists and also has stock
        """
        has_product_available = True
        filtered_df = cls.df[cls.df['product_name'] == product_name]
        if filtered_df.empty or filtered_df['quantity'].values[0] < quantity:
            cls.incorrect_requests += 1
            has_product_available = False
        return has_product_available


class Discount:
    _AVAILABLE_DISCOUNT_CODES = [
        "Primavera2021",
        "Verano2021",
        "Navidad2x1",
        "heladoFrozen"
    ]

    @classmethod
    def validate_discount_code(cls, discount_code):
        """
        :param discount_code: (str) discount code to validate
        :return: (bool) Returns True if the difference between the
        discount code and the valid codes is less than three characters,
        in at least one of the valid codes.
        """
        validation = False
        for available_code in cls._AVAILABLE_DISCOUNT_CODES:
            series_1 = pd.Series(list(discount_code))
            series_2 = pd.Series(list(available_code))
            difference1 = series_1[~series_1.isin(series_2)].to_list()
            difference2 = series_2[~series_2.isin(series_1)].to_list()
            difference_chars = set(difference1 + difference2)
            if difference_chars and len(difference_chars) < 3:
                validation = True
                break
        return validation


if __name__ == '__main__':
    print("\n", GeoAPI.is_hot_in_pehuajo())
    print("\n", Product.is_product_available("Chocolate", 3))
    print("\n", Discount.validate_discount_code("primavera2021"))
