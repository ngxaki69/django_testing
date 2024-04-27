from django.contrib.auth import get_user_model
from common import BaseTestCase
from django.urls import reverse
from http import HTTPStatus
from pytils.translit import slugify

from notes.forms import WARNING
from notes.models import Note


User = get_user_model()


class TestRoutes(BaseTestCase):

    def test_user_can_create_note(self):
        self.client.force_login(self.author)
        url = reverse('notes:add')
        old_count = Note.objects.count()
        response = self.client.post(url, data=self.note_form)
        self.assertRedirects(response, reverse('notes:success'))
        self.assertEqual(Note.objects.count(), old_count + 1)
        new_note = Note.objects.last()
        self.assertEqual(new_note.title, self.note_form['title'])
        self.assertEqual(new_note.text, self.note_form['text'])
        self.assertEqual(new_note.slug, self.note_form['slug'])

    def test_anonymous_user_cant_create_note(self):
        url = reverse('notes:add')
        old_count = Note.objects.count()
        response = self.client.post(url, self.note_form)
        login_url = reverse('users:login')
        expected_url = f'{login_url}?next={url}'
        self.assertRedirects(response, expected_url)
        self.assertEqual(Note.objects.count(), old_count)

    def test_not_unique_slug(self):
        self.client.force_login(self.author)
        url = reverse('notes:add')
        self.note_form['slug'] = self.note.slug
        response = self.client.post(url, data=self.note_form)
        self.assertFormError(
            response,
            'form',
            'slug',
            errors=(self.note.slug + WARNING)
        )
        self.assertEqual(Note.objects.count(), 1)

    def test_empty_slug(self):
        self.client.force_login(self.author)
        url = reverse('notes:add')
        self.note_form.pop('slug')
        response = self.client.post(url, data=self.note_form)
        self.assertRedirects(response, reverse('notes:success'))
        new_note = Note.objects.last()
        expected_slug = slugify(self.note_form['title'])
        self.assertEqual(new_note.slug, expected_slug)

    def test_author_can_edit_note(self):
        self.client.force_login(self.author)
        url_edit = reverse('notes:edit', args=(self.note.slug,))
        response = self.client.post(url_edit, self.note_form)
        self.assertRedirects(response, reverse('notes:success'))
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, self.note_form['title'])
        self.assertEqual(self.note.text, self.note_form['text'])
        self.assertEqual(self.note.slug, self.note_form['slug'])
        url_delete = reverse('notes:delete', args=(self.note.slug,))
        old_count = Note.objects.count()
        response = self.client.delete(url_delete)
        self.assertRedirects(response, reverse('notes:success'))
        self.assertEqual(Note.objects.count(), old_count - 1)

    def test_author_can_delete_note(self):
        self.client.force_login(self.author)
        url_delete = reverse('notes:delete', args=(self.note.slug,))
        old_count = Note.objects.count()
        response = self.client.delete(url_delete)
        self.assertRedirects(response, reverse('notes:success'))
        self.assertEqual(Note.objects.count(), old_count - 1)

    def test_not_author_cant_edit_note(self):
        self.client.force_login(self.not_author)
        url_edit = reverse('notes:edit', args=(self.note.slug,))
        response = self.client.post(url_edit, self.note_form)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note_from_db = Note.objects.get(id=self.note.id)
        self.assertEqual(self.note.title, note_from_db.title)
        self.assertEqual(self.note.text, note_from_db.text)
        self.assertEqual(self.note.slug, note_from_db.slug)

    def test_not_author_cant_delete_note(self):
        self.client.force_login(self.not_author)
        url_delete = reverse('notes:delete', args=(self.note.slug,))
        old_count = Note.objects.count()
        response = self.client.delete(url_delete)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(Note.objects.count(), old_count)
