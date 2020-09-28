import logging
import pickle
import uuid

from django.core.cache import cache


class BaseConverter:
    INITIATED_STATUS = 'initiated'
    INSERTING_STATUS = 'inserting'
    PENDING_STATUS = 'pending'
    FINISHED = 'finished'
    WITH_ERRORS = 'finished with errors'


class ConverterResultDetail:
    unit = None
    original_value = 0
    date = None
    conversion_rate = 0
    converted_value = 0

    def __init__(self, unit: str, original_value: float, date: date, conversion_rate: float, converted_value: float):
        self.unit = unit
        self.original_value = original_value
        self.date = date
        self.conversion_rate = conversion_rate
        self.converted_value = converted_value


class ConverterResultError:
    unit = None
    original_value = None
    date = None
    error = None

    def __init__(self, unit: str, original_value: float, date: date, error: str):
        self.unit = unit
        self.original_value = original_value
        self.date = date
        self.error = error


class ConverterResult:
    id = None
    target = None
    detail = []
    sum = 0
    status = None
    errors = []

    def __init__(self, id: str = None, target: str = None, detail: [ConverterResultDetail] = None,
                 sum: float = 0, status: str = BaseConverter.INITIATED_STATUS, errors: [ConverterResultError] = None):
        self.id = id
        self.target = target
        self.detail = detail or []
        self.sum = sum
        self.status = status
        self.errors = errors or []

    def increment_sum(self, value):
        try:
            float(value)
            self.sum += value
        except ValueError:
            logging.error("invalid value, will not increment result sum", value)

    def end_batch(self):
        if self.errors:
            self.status = BaseConverter.WITH_ERRORS
        else:
            self.status = BaseConverter.FINISHED
        return self.status


class BaseConverter:
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
        self.id = id or uuid.uuid4()
        self.data = []

    @classmethod
    def load(cls, id: str) -> BaseConverter:
        obj = cache.get(id)
        if obj:
            return pickle.loads(obj)
        raise KeyError(f"Converter with id {id} not found in cache")

    def save(self):
        cache.set(self.id, pickle.dumps(self))

    def add_data(self, data: []) -> []:
        """
        Check data and add it to the dataset
        Return list of errors
        """
        if not data:
            return [{'data': 'Empty data set', }]
        if errors := self.check_data(data):
            return errors
        self.status = self.INSERTING_STATUS
        self.save()
        return []

    def end_batch(self, status):
        self.status = status

    def check_data(self, data):
        """
        Validates data
        """
        raise NotImplementedError

    def convert(self) -> ConverterResult:
        """
        Converts data to base currency
        """
        raise NotImplementedError


class Batch:
    id = None
    status = None

    def __init__(self, id, status):
        self.id = id
        self.status = status
