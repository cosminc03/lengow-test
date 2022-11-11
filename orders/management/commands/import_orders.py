import requests
import xml.etree.ElementTree as ET

from django.core.management.base import BaseCommand, CommandParser
from orders.models import Order


class Command(BaseCommand):
    def _fetch_xml(self):
        response = requests.get("http://test.lengow.io/orders-test.xml")
        return response.content

    def _read_xml(self):
        orders = list()
        data = self._fetch_xml()
        tree_root = ET.fromstring(data)

        for child in tree_root.find("orders"):
            orders.append(
                {
                    "order_id": child.find("order_id").text,
                    "marketplace": child.find("marketplace").text,
                    "currency": child.find("order_currency").text,
                    "order_purchase_date": child.find("order_purchase_date").text,
                }
            )

        return orders

    def add_arguments(self, parser: CommandParser) -> None:
        pass

    def handle(self, *args, **options):
        orders = self._read_xml()
        for order_xml in orders:
            try:
                order = Order.objects.get(id=order_xml["order_id"])
            except Order.DoesNotExist:
                order = Order()

            order.id = order_xml["order_id"]
            order.marketplace = order_xml["marketplace"]
            order.currency = order_xml["currency"]
            order.purchase_date = order_xml["order_purchase_date"]
            order.save()

        self.stdout.write("Orders succesfully imported!")
