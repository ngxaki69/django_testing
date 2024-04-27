from django.contrib.auth import get_user_model
from common import BaseTestCase
from django.urls import reverse

from notes.forms import NoteForm

User = get_user_model()


class TestRoutes(BaseTestCase):

    def test_notes_list_for_different_users(self):
        users_objects_status = (
            (self.author, True),
            (self.not_author, False),
        )
        for user, expected_status in users_objects_status:
            self.client.force_login(user)
            url = reverse('notes:list')
            response = self.client.get(url)
            object_list = response.context['object_list']
            actual_status = self.note in object_list
            self.assertEqual(actual_status, expected_status)

    def test_pages_contains_form(self):
        urls = (
            ('notes:add', None),
            ('notes:edit', (self.note.slug,)),
        )
        for name, args in urls:
            with self.subTest(name=name):
                self.client.force_login(self.author)
                url = reverse(name, args=args)
                response = self.client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
