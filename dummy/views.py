from django.http import JsonResponse
from django.views.generic import DetailView
from dummy.utils import *
from dummy.validators import Form


class Aviatickets(DetailView):
    def get(self, request):
        form = Form(request.GET)
        errors = form.process()
        if errors:
            return JsonResponse({"error": "Ошибка заполнения формы", "fields_errors": errors}, status=400)

        base_duration = random.randint(40, 350)

        tickets = []
        for count in range(form.delta_in_seconds // 1000):
            carrier = random.choice(carriers)

            # Случайная длительность перелета
            direct_duration = base_duration + random.randint(-5, 15)
            return_duration = base_duration + random.randint(-5, 15)
            # Случайная цена, зависит от длительности
            price = random.randint(50, 100) * direct_duration * (form.adults_count + form.children_count)

            # Время вылета зависит от выбранной даты вылета и текущей даты
            direct_departure_time = generate_departure_date(form.direct_date, form.delta_in_seconds)
            # Время прилета зависит только от длительности
            direct_arrival_time = direct_departure_time + timedelta(minutes=direct_duration)

            direct_way = {
                "airport_from": form.iata_from,
                "airport_to": form.iata_to,
                "departure_datetime": datetime.strftime(direct_departure_time, "%Y-%m-%d %H:%M"),
                "arrival_datetime": datetime.strftime(direct_arrival_time, "%Y-%m-%d %H:%M"),
                "duration": direct_duration,
                "carrier_id": carrier["id"],
            }
            ticket = {
                "direct": direct_way,
                "price": price,
                "buy_link": "https://loftschool.com/"
            }
            if form.return_date:
                return_departure_time = generate_departure_date(max(direct_arrival_time, form.return_date))
                # Время прилета зависит только от длительности
                return_arrival_time = return_departure_time + timedelta(minutes=return_duration)
                return_way = {
                    "airport_from": form.iata_to,
                    "airport_to": form.iata_from,
                    "departure_datetime": datetime.strftime(return_departure_time, "%Y-%m-%d %H:%M"),
                    "arrival_datetime": datetime.strftime(return_arrival_time, "%Y-%m-%d %H:%M"),
                    "duration": return_duration,
                    "carrier_id": carrier["id"],
                }
                ticket["return"] = return_way

            tickets.append(ticket)

        result = {
            "airports": [form.airport_from, form.airport_to],
            "carriers": carriers,
            "tickets": tickets
        }
        return JsonResponse(result)


class Airports(DetailView):
    def get(self, request):
        return JsonResponse({'airports': airpotr_list})
