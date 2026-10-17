"""Smoke tests offline da interface Flask."""

import unittest
from unittest.mock import patch

from app import app


class AppTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_homepage(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"VerificarSite", response.data)

    def test_invalid_url_stays_local(self):
        with patch("app.consultar_site") as consult:
            response = self.client.post("/", data={"url": "http://localhost:8000"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("endereços internos".encode(), response.data)
        consult.assert_not_called()

    def test_valid_url_normalizes_and_displays_results(self):
        with patch("app.consultar_site", return_value="Dados demonstrativos") as consult:
            response = self.client.post("/", data={"url": "example.org"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Dados demonstrativos".encode(), response.data)
        consult.assert_called_once_with("https://example.org")

    def test_provider_error_does_not_leak_traceback(self):
        with patch("app.consultar_site", side_effect=RuntimeError("Falha temporária")):
            response = self.client.post("/", data={"url": "https://example.org"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Falha temporária".encode(), response.data)
        self.assertNotIn(b"Traceback", response.data)

    def test_provider_results_are_escaped(self):
        with patch("app.consultar_site", return_value="<script>alert(1)</script>"):
            response = self.client.post("/", data={"url": "https://example.org"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"&lt;script&gt;", response.data)
        self.assertNotIn(b"<script>", response.data)


if __name__ == "__main__":
    unittest.main()
