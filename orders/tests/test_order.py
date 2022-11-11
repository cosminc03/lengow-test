from django.test import TestCase
from django.urls import reverse
from orders.models import Order


def create_order(order_id: str, marketplace: str, currency: str):
    order = Order.objects.create(
        id=order_id, marketplace=marketplace, currency=currency
    )

    return order


class OrderListTests(TestCase):
    def test_when_orders_not_available(self):
        response = self.client.get(reverse("order_list"))
        self.assertJSONEqual(response.content, [])

    def test_when_multiple_orders_available(self):
        create_order(order_id="test-1", marketplace="amazon", currency="EUR")
        create_order(order_id="test-2", marketplace="ebay", currency="EUR")
        response = self.client.get(reverse("order_list"))

        self.assertJSONEqual(
            response.content,
            [
                {
                    "id": "test-1",
                    "marketplace": "amazon",
                    "currency": "EUR",
                    "purchase_date": None,
                },
                {
                    "id": "test-2",
                    "marketplace": "ebay",
                    "currency": "EUR",
                    "purchase_date": None,
                },
            ],
        )


class OrderDetailViewTests(TestCase):
    def test_when_order_is_missing(self):
        response = self.client.get(reverse("order_detail", kwargs={"pk": "1"}))
        self.assertJSONEqual(response.content, {"detail": "Not found."})

    def test_when_order_is_available(self):
        create_order(order_id="test-123", marketplace="amazon", currency="EUR")
        response = self.client.get(reverse("order_detail", kwargs={"pk": "test-123"}))

        self.assertJSONEqual(
            response.content,
            {
                "id": "test-123",
                "marketplace": "amazon",
                "currency": "EUR",
                "purchase_date": None,
            },
        )
