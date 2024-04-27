from http import HTTPStatus
import pytest
from pytest_django.asserts import assertRedirects


URL_NEWS_HOME = pytest.lazy_fixture('url_home')
URL_NEWS_DETAIL = pytest.lazy_fixture('url_detail')
URL_NEWS_LOGIN = pytest.lazy_fixture('url_login')
URL_NEWS_LOGOUT = pytest.lazy_fixture('url_logout')
URL_NEWS_SIGNUP = pytest.lazy_fixture('url_signup')
URL_NEWS_EDIT = pytest.lazy_fixture('url_edit')
URL_NEWS_DELETE = pytest.lazy_fixture('url_delete')


ANONYMOUS_CLIENT = pytest.lazy_fixture('anonymous_client')
USER_CLIENT = pytest.lazy_fixture('not_author_client')
AUTHOR_CLIENT = pytest.lazy_fixture('author_client')


@pytest.mark.django_db
@pytest.mark.parametrize(
    ('url', 'parametrized_client', 'expected_status'),
    (
        (URL_NEWS_HOME, ANONYMOUS_CLIENT, HTTPStatus.OK),
        (URL_NEWS_DETAIL, ANONYMOUS_CLIENT, HTTPStatus.OK),
        (URL_NEWS_SIGNUP, ANONYMOUS_CLIENT, HTTPStatus.OK),
        (URL_NEWS_LOGIN, ANONYMOUS_CLIENT, HTTPStatus.OK),
        (URL_NEWS_LOGOUT, ANONYMOUS_CLIENT, HTTPStatus.OK),
        (URL_NEWS_DELETE, AUTHOR_CLIENT, HTTPStatus.OK),
        (URL_NEWS_EDIT, AUTHOR_CLIENT, HTTPStatus.OK),
        (URL_NEWS_DELETE, USER_CLIENT, HTTPStatus.NOT_FOUND),
        (URL_NEWS_EDIT, USER_CLIENT, HTTPStatus.NOT_FOUND),
    )
)
def test_pages(url, parametrized_client, expected_status):
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    ('login_url', 'url', 'parametrized_client'),
    (
        (URL_NEWS_LOGIN, URL_NEWS_DELETE, ANONYMOUS_CLIENT),
        (URL_NEWS_LOGIN, URL_NEWS_EDIT, ANONYMOUS_CLIENT),
    )
)
def test_redirects(login_url, url, parametrized_client):
    expected_url = f'{login_url}?next={url}'
    response = parametrized_client.get(url)
    assertRedirects(response, expected_url)
