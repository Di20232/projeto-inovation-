import unittest
from decimal import Decimal

from python.python import (
    build_asaas_credit_card_payment_payload,
    normalize_asaas_credit_card_form,
)


class AsaasCreditCardPaymentTests(unittest.TestCase):
    def setUp(self):
        self.form_data = {
            "holder_name": "Cliente de Teste",
            "holder_email": "cliente@example.com",
            "cpf_cnpj": "529.982.247-25",
            "postal_code": "01001-000",
            "address_number": "100",
            "phone": "(11) 99999-9999",
            "card_number": "4539 6560 4839 2220",
            "expiration": "2099-12",
            "ccv": "123",
        }

    def test_builds_sandbox_payment_payload_without_card_formatting(self):
        form_data = normalize_asaas_credit_card_form(self.form_data)
        payload = build_asaas_credit_card_payment_payload(
            total=Decimal("123.45"),
            external_reference="NF-test",
            customer_id="cus_test",
            remote_ip="127.0.0.1",
            form_data=form_data,
        )

        self.assertEqual(payload["customer"], "cus_test")
        self.assertEqual(payload["billingType"], "CREDIT_CARD")
        self.assertEqual(payload["value"], 123.45)
        self.assertEqual(payload["externalReference"], "NF-test")
        self.assertEqual(payload["remoteIp"], "127.0.0.1")
        self.assertEqual(
            payload["creditCard"],
            {
                "holderName": "Cliente de Teste",
                "number": "4539656048392220",
                "expiryMonth": "12",
                "expiryYear": "2099",
                "ccv": "123",
            },
        )
        self.assertEqual(
            payload["creditCardHolderInfo"],
            {
                "name": "Cliente de Teste",
                "email": "cliente@example.com",
                "cpfCnpj": "52998224725",
                "postalCode": "01001000",
                "addressNumber": "100",
                "phone": "11999999999",
            },
        )

    def test_rejects_expired_test_card(self):
        self.form_data["expiration"] = "2020-01"

        with self.assertRaisesRegex(ValueError, "validade do cartão precisa ser futura"):
            normalize_asaas_credit_card_form(self.form_data)

    def test_rejects_invalid_cpf(self):
        self.form_data["cpf_cnpj"] = "111.111.111-11"

        with self.assertRaisesRegex(ValueError, "CPF válido"):
            normalize_asaas_credit_card_form(self.form_data)


if __name__ == "__main__":
    unittest.main()
