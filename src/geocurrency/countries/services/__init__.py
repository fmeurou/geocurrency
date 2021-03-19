"""
Country services
"""
from timezonefinder import TimezoneFinder

from geocurrency.countries.models import Country, CountryNotFoundError

tf = TimezoneFinder(in_memory=True)


class Geocoder:
    """
    Geocoder services
    """

    def search(self, address, language=None, bounds=None, region=None, components=""):
        """
        Search an address
        :params text: address to search for
        :params language: optional, language of result
        :params bounds: optional, limit results to bounds
        :params region: optional, limit results to region
        :params components: optional, a components filter with elements separated by a pipe (|)
        :returns: Country
        """
        raise NotImplementedError("Use specific implementation")

    def reverse(self, lat, lng):
        """
        Search from GPS coordinates
        :params lat: latitude
        :params lng: longitude
        """
        raise NotImplementedError("Use specific implementation")

    def parse_countries(self, data):
        """
        Parse countries from result
        :params data: geocoding / reverse geocoding result
        :returns: Country instance
        """
        raise NotImplementedError("Use specific implementation")

    def countries(self, data):
        """
        List countries
        :params data: json response from geocoding / reverse geocoding service
        """
        countries = []
        alphas = self.parse_countries(data=data)
        for alpha in set(alphas):
            try:
                if len(alpha) == 2:
                    country = Country(alpha)
                elif len(alpha) == 3:
                    country = Country(alpha[0:2])
                else:
                    country = Country(alpha)
            except CountryNotFoundError:
                continue
            countries.append(country)
        return sorted(countries, key=lambda x: x.name)
