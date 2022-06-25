from dummy.utils import *
from datetime import datetime, date


class Form:
    direct_date = None
    return_date = None
    delta_in_seconds = 86399

    def __init__(self, request_data):
        self.iata_from = request_data.get('iata_from')
        self.iata_to = request_data.get('iata_to')
        self.direct_date_str = request_data.get('direct_date')
        self.return_date_str = request_data.get('return_date')
        self.adults_count_str = request_data.get('adults_count', 0)
        self.children_count_str = request_data.get('children_count', 0)
        self.baby_count_str = request_data.get('baby_count', 0)
        self.flight_class = request_data.get('flight_class')

    def process(self):
        errors = {}
        # Аэропорты
        if not self.iata_from:
            errors["iata_from"] = "Укажите аэропорт вылета"
        else:
            self.airport_from = get_airport_by_iata(self.iata_from)
            if self.airport_from is None:
                errors["iata_from"] = "Неверно указан аэропорт вылета"
        if not self.iata_to:
            errors["iata_to"] = "Укажите аэропорт назначения"
        else:
            self.airport_to = get_airport_by_iata(self.iata_to)
            if self.airport_to is None:
                errors["iata_to"] = "Неверно указан аэропорт назначения"

        # Пассажиры
        self.adults_count, self.children_count, self.baby_count = 0, 0, 0
        try:
            self.adults_count = int(self.adults_count_str)
            if not 0 < self.adults_count < 10:
                raise ValueError
        except(TypeError, ValueError):
            errors["adults_count"] = "Укажите число от 0 до 9"

        try:
            if self.children_count_str:
                self.children_count = int(self.children_count_str)
                if not 0 <= self.children_count < 9 - self.adults_count:
                    raise ValueError
        except(TypeError, ValueError):
            errors["children_count"] = f"Укажите число от 0 до {9 - min(self.adults_count, 9)}"

        try:
            if self.baby_count_str:
                self.baby_count = int(self.baby_count_str)
                if not 0 <= self.baby_count <= self.adults_count:
                    raise ValueError
        except(TypeError, ValueError):
            errors["baby_count"] = f"Укажите число от 0 до {self.adults_count}"

        if (self.adults_count + self.children_count + self.baby_count > 9
                and "adults_count" not in errors):
            errors["adults_count"] = "Суммарно не может быть больше 9 пассажиров"

        # Класс
        if self.flight_class and self.flight_class not in "YWCF":
            errors["flight_class"] = "Неверно указан код класса"

        # Даты
        try:
            self.direct_date = datetime.strptime(self.direct_date_str, "%Y-%m-%d")
            if self.direct_date.date() < date.today():
                errors["direct_date"] = "Дата вылета не может быть в прошлом"
        except(TypeError, ValueError):
            errors["direct_date"] = "Неверный формат даты"

        if self.return_date_str:
            try:
                self.return_date = datetime.strptime(self.return_date_str, "%Y-%m-%d")
                if self.return_date < self.direct_date:
                    errors["return_date"] = "Дата обратного вылета не может быть раньше даты прямого"
            except(TypeError, ValueError):
                errors["return_date"] = "Неверный формат даты"

        if self.direct_date.date() == date.today():
            self.direct_date, self.delta_in_seconds = get_departure_date_and_delta(self.direct_date)

        return errors
