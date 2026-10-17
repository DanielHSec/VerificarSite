import unittest

from url_validation import normalize_public_url


class URLValidationTests(unittest.TestCase):
    def test_domain_gets_https(self):
        self.assertEqual(normalize_public_url("  exemplo.com.br "), "https://exemplo.com.br")

    def test_preserves_public_url(self):
        self.assertEqual(
            normalize_public_url("http://example.org/path?q=1#frag"),
            "http://example.org/path?q=1",
        )

    def test_rejects_unsafe_schemes(self):
        for value in ("javascript:alert(1)", "file:///etc/passwd", "ftp://example.com"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                normalize_public_url(value)

    def test_rejects_private_urls(self):
        for value in (
            "http://localhost:3000",
            "http://127.0.0.1",
            "http://192.168.1.1",
            "http://10.0.0.2",
            "http://[::1]/",
            "http://server.local",
            "http://host.internal",
            "http://169.254.169.254",
        ):
            with self.subTest(value=value), self.assertRaises(ValueError):
                normalize_public_url(value)

    def test_rejects_embedded_credentials(self):
        with self.assertRaises(ValueError):
            normalize_public_url("https://user:secret@example.com")

    def test_rejects_blank_and_malformed(self):
        for value in ("", "https://", "not-a-domain", "https://a..com", "https://example.com:abc"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                normalize_public_url(value)

    def test_rejects_controls(self):
        with self.assertRaises(ValueError):
            normalize_public_url("https://example.com/\nmalicious")


if __name__ == "__main__":
    unittest.main()
