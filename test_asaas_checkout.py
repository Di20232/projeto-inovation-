import unittest
from decimal import Decimal

from python.python import (
    build_asaas_credit_card_form_data,
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
            "card_number": "4539656048392220",
            "expiration": "2099-12",
            "ccv": "123",
        }

    def test_builds_card_form_from_visible_fields_and_server_profile(self):
        card_form = build_asaas_credit_card_form_data(
            {
                "holder_name": "Cliente de Teste",
                "holder_email": "forged@example.com",
                "cpf_cnpj": "111.111.111-11",
                "card_number": "4539656048392220",
                "expiration": "2099-12",
                "ccv": "123",
            },
            holder_email=" CLIENTE@example.com ",
            cpf_cnpj="529.982.247-25",
            phone="(11) 99999-9999",
            postal_code="01001-000",
            address_number=" 100 ",
        )

        self.assertEqual(card_form["holder_email"], "cliente@example.com")
        self.assertEqual(card_form["cpf_cnpj"], "52998224725")
        self.assertEqual(card_form["phone"], "11999999999")
        self.assertEqual(card_form["postal_code"], "01001000")
        self.assertEqual(card_form["address_number"], "100")
        self.assertEqual(card_form["card_number"], "4539656048392220")

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

    def test_rejects_card_number_outside_conventional_length(self):
        for card_number in ("123456789012", "12345678901234567890"):
            with self.subTest(card_number_length=len(card_number)):
                self.form_data["card_number"] = card_number
                with self.assertRaisesRegex(
                    ValueError,
                    "número do cartão deve conter entre 13 e 19 dígitos",
                ):
                    normalize_asaas_credit_card_form(self.form_data)

    def test_rejects_non_digit_card_number(self):
        self.form_data["card_number"] = "453965604839222x"

        with self.assertRaisesRegex(ValueError, "cartão deve conter apenas dígitos"):
            normalize_asaas_credit_card_form(self.form_data)

    def test_normalizes_common_card_number_separators(self):
        self.form_data["card_number"] = "4539 6560-4839 2220"

        card_form = normalize_asaas_credit_card_form(self.form_data)

        self.assertEqual(card_form["card_number"], "4539656048392220")

    def test_rejects_missing_card_number_with_specific_message(self):
        self.form_data["card_number"] = ""

        with self.assertRaisesRegex(ValueError, "Informe o número do cartão"):
            normalize_asaas_credit_card_form(self.form_data)

    def test_rejects_cvv_outside_conventional_length(self):
        for ccv in ("12", "1234"):
            with self.subTest(cvv_length=len(ccv)):
                self.form_data["ccv"] = ccv
                with self.assertRaisesRegex(
                    ValueError,
                    "CVV deve conter exatamente 3 dígitos",
                ):
                    normalize_asaas_credit_card_form(self.form_data)

    def test_rejects_non_digit_cvv(self):
        self.form_data["ccv"] = "12a"

        with self.assertRaisesRegex(ValueError, "CVV deve conter apenas números"):
            normalize_asaas_credit_card_form(self.form_data)

    def test_rejects_invalid_cpf(self):
        self.form_data["cpf_cnpj"] = "111.111.111-11"

        with self.assertRaisesRegex(ValueError, "CPF válido"):
            normalize_asaas_credit_card_form(self.form_data)


if __name__ == "__main__":
    unittest.main()
