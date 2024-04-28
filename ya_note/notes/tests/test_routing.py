from common import BaseTestCase
from django.urls import reverse
from http import HTTPStatus

from common import URL_NOTES_HOME, URL_NOTES_LOGIN, URL_NOTES_LOGOUT
from common import URL_NOTES_SIGNUP, URL_NOTES_DETAIL, URL_NOTES_EDIT
from common import URL_NOTES_DELETE, URL_NOTES_LIST, URL_NOTES_ADD
from common import URL_NOTES_SUCCESS


class TestRoutes(BaseTestCase):

    def test_pages(self):
        urls = (
            (URL_NOTES_HOME, self.client, HTTPStatus.OK),
            (URL_NOTES_LOGIN, self.client, HTTPStatus.OK),
            (URL_NOTES_LOGOUT, self.client, HTTPStatus.OK),
            (URL_NOTES_SIGNUP, self.client, HTTPStatus.OK),
            (URL_NOTES_DETAIL, self.not_author_client, HTTPStatus.NOT_FOUND),
            (URL_NOTES_EDIT, self.not_author_client, HTTPStatus.NOT_FOUND),
            (URL_NOTES_DELETE, self.not_author_client, HTTPStatus.NOT_FOUND),
            (URL_NOTES_DETAIL, self.author_client, HTTPStatus.OK),
            (URL_NOTES_EDIT, self.author_client, HTTPStatus.OK),
            (URL_NOTES_DELETE, self.author_client, HTTPStatus.OK),
            (URL_NOTES_LIST, self.author_client, HTTPStatus.OK),
            (URL_NOTES_ADD, self.author_client, HTTPStatus.OK),
            (URL_NOTES_SUCCESS, self.author_client, HTTPStatus.OK),
        )
        for url, user, status in urls:
            with self.subTest(name=url):
                response = user.get(url)
                self.assertEqual(response.status_code, status)

    def test_redirects(self):
        urls = (
            (URL_NOTES_DETAIL),
            (URL_NOTES_EDIT),
            (URL_NOTES_DELETE),
            (URL_NOTES_ADD),
            (URL_NOTES_SUCCESS),
            (URL_NOTES_LIST),

        )
        for url in urls:
            with self.subTest(name=url):
                login_url = reverse('users:login')
                expected_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, expected_url)
