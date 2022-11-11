from io import StringIO

from django.core.management import call_command
from django.test import TestCase
from unittest.mock import patch

from orders.models import Order
from orders.serializers import OrderSerializer
from orders.management.commands.import_orders import Command


def mocked_xml(cls):
    return """<?xml version="1.0" encoding="ISO-8859-1"?>
        <data>
            <orders>
                <order>
                    <order_id><![CDATA[test-123]]></order_id>
                    <marketplace><![CDATA[amazon]]></marketplace>
                    <order_currency><![CDATA[EUR]]></order_currency>
                    <order_purchase_date><![CDATA[]]></order_purchase_date>
                </order>
            </orders>
        </data>
    """


class ImportOrdersCommandTests(TestCase):
    def call_command(self, *args, **kwargs):
        out = StringIO()
        call_command("import_orders", *args, stdout=out, stderr=StringIO(), **kwargs)
        return out.getvalue()

    @patch("orders.management.commands.import_orders.Command._fetch_xml", mocked_xml)
    def test_when_reading_xml_file(self):
        command = Command()
        result = command._read_xml()
        self.assertEqual(
            result,
            [
                {
                    "order_id": "test-123",
                    "marketplace": "amazon",
                    "currency": "EUR",
                    "order_purchase_date": None,
                }
            ],
        )

    @patch("orders.management.commands.import_orders.Command._fetch_xml", mocked_xml)
    def test_when_new_order_is_added(self):
        out = self.call_command()
        order = Order.objects.get(pk="test-123")
        serializer = OrderSerializer(order)

        self.assertEqual(out, "Orders succesfully imported!\n")
        self.assertEqual(
            serializer.data,
            {
                "id": "test-123",
                "marketplace": "amazon",
                "currency": "EUR",
                "purchase_date": None,
            },
        )

    @patch("orders.management.commands.import_orders.Command._fetch_xml", mocked_xml)
    def test_when_existent_order_is_updated(self):
        order = Order.objects.create(id="test-123", marketplace="ebay", currency="USD")
        out = self.call_command()
        order = Order.objects.get(pk="test-123")
        serializer = OrderSerializer(order)

        self.assertEqual(out, "Orders succesfully imported!\n")
        self.assertEqual(
            serializer.data,
            {
                "id": "test-123",
                "marketplace": "amazon",
                "currency": "EUR",
                "purchase_date": None,
            },
        )
