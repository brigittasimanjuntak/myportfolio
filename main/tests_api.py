import uuid
from django.contrib.auth.models import Group, User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from main.models import CreativeSpace

class CreativeSpaceAPITest(APITestCase):
    def setUp(self):
        # 1. Bikin User
        self.owner = User.objects.create_superuser(
            username="owner", password="test-password", email="owner@example.com"
        )
        self.visitor = User.objects.create_user(username="visitor", password="test-password")
        
        # Bikin user Editor dan masukin ke group 'Editor'
        self.editor = User.objects.create_user(username="editor", password="test-password")
        editor_group = Group.objects.create(name="Editor")
        self.editor.groups.add(editor_group)

        # 2. Bikin Data Artwork
        self.artwork = CreativeSpace.objects.create(
            title="Sunset Doodle",
            description="A soft pastel drawing.",
            artist="Brigitta",
            medium="digital-art",
            image="https://example.com/sunset.jpg",
        )

        # 3. URL Endpoint
        self.list_url = reverse("api:creativespace-list")
        self.detail_url = reverse("api:creativespace-detail", args=[self.artwork.id])
        self.star_url = reverse("api:creativespace-star", args=[self.artwork.id])
        
        # 4. Payload Buat Nambah Data
        self.payload = {
            "title": "New Artwork",
            "description": "A cool sketch.",
            "artist": "Brigitta",
            "medium": "sketch",
            "image": "https://example.com/sketch.jpg",
        }

    def test_public_can_read(self):
        """Pengunjung bisa melihat list dan detail"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], str(self.artwork.id))
        
        response_detail = self.client.get(self.detail_url)
        self.assertEqual(response_detail.status_code, status.HTTP_200_OK)

    def test_visitor_and_guest_cannot_write(self):
        """Pengunjung dan user biasa gak bisa nambah/ngedit/hapus"""
        for user in (None, self.visitor, self.editor): # Editor juga gak bisa nambah/hapus!
            self.client.force_authenticate(user=user)
            
            # Gak bisa nambah (Create)
            self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, status.HTTP_403_FORBIDDEN)
            # Gak bisa hapus (Delete)
            self.assertEqual(self.client.delete(self.detail_url).status_code, status.HTTP_403_FORBIDDEN)

    def test_editor_can_update_but_not_delete(self):
        """Editor cuma bisa ngedit (PATCH/PUT)"""
        self.client.force_authenticate(user=self.editor)
        
        # Bisa PATCH
        response = self.client.patch(self.detail_url, {"title": "Updated by Editor"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.artwork.refresh_from_db()
        self.assertEqual(self.artwork.title, "Updated by Editor")
        
        # Gak bisa delete
        self.assertEqual(self.client.delete(self.detail_url).status_code, status.HTTP_403_FORBIDDEN)

    def test_owner_can_create_update_delete(self):
        """Superuser bisa semuanya"""
        self.client.force_authenticate(user=self.owner)
        
        # Create
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CreativeSpace.objects.count(), 2)
        
        # Update (PUT)
        response = self.client.put(self.detail_url, {
            "title": "Updated by Owner",
            "description": "New desc",
            "artist": "Me",
            "medium": "digital-art",
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Delete
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_validation_xss(self):
        """Cek proteksi XSS di title"""
        self.client.force_authenticate(user=self.owner)
        bad_payload = self.payload.copy()
        bad_payload["title"] = "<script>alert('hack')</script>"
        
        response = self.client.post(self.list_url, bad_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", response.data)

    def test_star_requires_login_and_toggles(self):
        """Star harus login, dan beneran nge-toggle"""
        # Belom login
        self.assertEqual(self.client.post(self.star_url).status_code, status.HTTP_403_FORBIDDEN)
        
        # Login sebagai visitor
        self.client.force_authenticate(user=self.visitor)
        response = self.client.post(self.star_url)
        self.assertTrue(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)
        
        # Klik lagi buat unstar
        response = self.client.post(self.star_url)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 0)

    def test_search_works(self):
        """Cek fitur pencarian (?title=...)"""
        response = self.client.get(self.list_url, {"title": "Sunset"})
        self.assertEqual(len(response.data), 1)
        
        response_empty = self.client.get(self.list_url, {"title": "TidakAda"})
        self.assertEqual(len(response_empty.data), 0)