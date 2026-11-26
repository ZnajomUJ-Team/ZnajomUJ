from django.test import TestCase
from django.urls import reverse


class HomePageTests(TestCase):
    def test_home_page_returns_200(self):
        response = self.client.get(reverse("core:home"))
        self.assertEqual(response.status_code, 200)

    def test_home_page_extends_base_template(self):
        response = self.client.get(reverse("core:home"))
        self.assertTemplateUsed(response, "base.html")
        self.assertContains(response, '<html lang="pl">')
