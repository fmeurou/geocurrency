"""
Standard classes for the Converter module
"""

import logging
import pickle
import uuid

from django.core.cache import cache


class ConverterLoadError(Exception):
    """
    Exception when loading a converter from its redis pickle
    """
    msg = 'Error while loading converter'


class BaseConverter:
    """
    Base class for conversion
    Mock up for usage in type hinting
    """
    INITIATED_STATUS = 'initiated'
    INSERTING_STATUS = 'inserting'
    PENDING_STATUS = 'pending'
    FINISHED = 'finished'
    WITH_ERRORS = 'finished with errors'


class ConverterResultDetail:
    """
    Details of a conversion
    """
    unit = None
    original_value = 0
    date = None
    conversion_rate = 0
    converted_value = 0

    def __init__(self, unit: str, original_value: float,
                 date: date, conversion_rate: float,
                 converted_value: float):
        """
        Initialize details
        :param unit: dimension as a string
        :param original_value: value before conversion
        :param date: date of conversion
        :param conversion_rate: rate of conversion
        :param converted_value: resulting value
        """
        self.unit = unit
        self.original_value = original_value
        self.date = date
        self.conversion_rate = conversion_rate
        self.converted_value = converted_value


class ConverterResultError:
    """
    Error from a conversion
    """
    unit = None
    original_value = None
    date = None
    error = None

    def __init__(self, unit: str, original_value: float,
                 date: date, error: str):
        """
        Initialize error
        :param unit: string of the dimension
        :param original_value: value before conversion
        :param date: date of conversion
        :param error: description of the error
        """
        self.unit = unit
        self.original_value = original_value
        self.date = date
        self.error = error


class ConverterResult:
    """
    Result of a batch of conversions
    """
    id = None
    target = None
    detail = []
    sum = 0
    status = None
    errors = []

    def __init__(self, id: str = None, target: str = None,
                 detail: [ConverterResultDetail] = None,
                 sum: float = 0, status: str = BaseConverter.INITIATED_STATUS,
                 errors: [ConverterResultError] = None):
        """
        Initialize result
        :param id: ID of the batch
        :param target: target currency
        :param detail: List of ConverterResultDetail
        :param sum: sum of all detailed conversions
        :param status: status of the batch
        :param errors: List of conversion errors
        """
        self.id = id
        self.target = target
        self.detail = detail or []
        self.sum = sum
        self.status = status
        self.errors = errors or []

    def increment_sum(self, value):
        """
        Sum individual conversion results
        They are all in the target currency
        :param value: result of a conversion
        """
        try:
            float(value)
            self.sum += value
        except ValueError:
            logging.error("invalid value, "
                          "will not increment result sum", value)

    def end_batch(self):
        """
        Puts a final status on the batch
        """
        if self.errors:
            self.status = BaseConverter.WITH_ERRORS
        else:
            self.status = BaseConverter.FINISHED
        return self.status


class BaseConverter:
    """
    Base conversion class
    """
    INITIATED_STATUS = 'initiated'
    INSERTING_STATUS = 'inserting'
    PENDING_STATUS = 'pending'
    FINISHED = 'finished'
    WITH_ERRORS = 'finished with errors'
    id = None
    status = INITIATED_STATUS
    data = []
    converted_lines = []
    aggregated_result = {}

    def __init__(self, id: str = None):
        """
        Initialize BaseConverter
        :param id: ID of the batch
        """
        self.id = id or uuid.uuid4()
        self.data = []

    @classmethod
    def load(cls, id: str) -> BaseConverter:
        """
        Load Converter from cache
        :param id: ID of the batch
        """
        obj = cache.get(id)
        if obj:
            return pickle.loads(obj)
        raise KeyError(f"Converter with id {id} not found in cache")

    def save(self):
        """
        Save Converter to cache
        """
        cache.set(self.id, pickle.dumps(self))

    def add_data(self, data: []) -> []:
        """
        Check data and add it to the dataset
        Return list of errors
        :param data: list of items to convert
        """
        if not data:
            return [{'data': 'Empty data set', }]
        errors = self.check_data(data)
        if errors:
            return errors
        self.status = self.INSERTING_STATUS
        self.save()
        return []

    def end_batch(self, status: str):
        """
        set status of the batch
        :param status: status from statuses
        """
        self.status = status

    def check_data(self, data):
        """
        Validates data
        Not implementd
        :param data: list of items to convert
        """
        raise NotImplementedError

    def convert(self) -> ConverterResult:
        """
        Converts data to base currency
        Not implemented
        """
        raise NotImplementedError


class Batch:
    """
    Batch class
    """
    id = None
    status = None

    def __init__(self, id: str, status: str):
        """
        Initialize the batch
        :param id: ID of the batch
        :param status: status of the batch
        """
        self.id = id
        self.status = status
