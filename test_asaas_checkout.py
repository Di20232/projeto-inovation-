import unittest
from decimal import Decimal

from python.python import build_asaas_checkout_payload


class AsaasCheckoutPayloadTests(unittest.TestCase):
    def test_builds_single_charge_without_card_details(self):
        payload = build_asaas_checkout_payload(
            total=Decimal("123.45"),
            external_reference="NF-test",
            callback_base_url="http://localhost:3000",
            customer_name="Cliente de Teste",
            customer_email="cliente@example.com",
        )

        self.assertEqual(payload["billingTypes"], ["CREDIT_CARD"])
        self.assertEqual(payload["chargeTypes"], ["DETACHED"])
        self.assertEqual(payload["externalReference"], "NF-test")
        self.assertEqual(payload["items"][0]["value"], 123.45)
        self.assertEqual(
            payload["callback"]["successUrl"],
            "http://localhost:3000/pagamento?asaas=success",
        )
        self.assertEqual(
            payload["customerData"],
            {"name": "Cliente de Teste", "email": "cliente@example.com"},
        )
        self.assertNotIn("creditCard", payload)
        self.assertNotIn("ccv", payload)


if __name__ == "__main__":
    unittest.main()
