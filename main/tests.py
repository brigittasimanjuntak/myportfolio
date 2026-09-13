from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Experience, CreativeSpace


class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="PBP Teaching Assistant",
            description="Help students understand web development.",
            category="part-time",
        )

        self.artwork = CreativeSpace.objects.create(
            title="Sunset Doodle",
            description="A soft pastel sunset drawing.",
            medium="digital-art",
            image="https://example.com/sunset.jpg",
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/a-page-that-does-not-exist/")

        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "PBP Teaching Assistant")
        self.assertEqual(self.experience.category, "part-time")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.description)
        self.assertContains(response, "Part-Time")
        self.assertContains(response, "Ongoing")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "No experience has been added yet.")

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("main:show_experience"))

        self.assertFalse(self.experience.is_ongoing)
        self.assertContains(response, "Completed")
        self.assertNotContains(response, "Ongoing")

class CreativeSpaceTest(TestCase):
    def setUp(self):
        self.artwork = CreativeSpace.objects.create(
            title="Sunset Doodle",
            description="A soft pastel sunset drawing.",
            medium="digital-art",
            image="https://example.com/sunset.jpg",
        )

    def test_creative_space_url_is_accessible(self):
        """Test 1: URL bisa diakses dan pake template yang tepat."""
        response = self.client.get(reverse("main:show_creative_space"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "creativespace.html")

    def test_artwork_appears_on_page(self):
        """Test 2: Data model muncul di HTML ketika ada data."""
        response = self.client.get(reverse("main:show_creative_space"))
        self.assertContains(response, self.artwork.title)
        self.assertContains(response, self.artwork.description)
        self.assertContains(response, "Digital Art")

    def test_empty_creative_space_page(self):
        """Test 3: Halaman nampilin pesan kosong ketika belum ada data."""
        CreativeSpace.objects.all().delete()
        response = self.client.get(reverse("main:show_creative_space"))
        self.assertContains(response, "No artwork has been added yet")