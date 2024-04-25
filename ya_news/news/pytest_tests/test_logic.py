from django.urls import reverse
import pytest

from news.forms import BAD_WORDS, WARNING
from news.models import Comment


@pytest.mark.django_db
@pytest.mark.parametrize(
    'parametrized_client, comment_create',
    (
        (pytest.lazy_fixture('author_client'), 1),
        (pytest.lazy_fixture('client'), 0),
    )
)
def test__users__create_comment(parametrized_client, comment_create, form_data,
                                new):
    url = reverse('news:detail', args=(new.id,))
    parametrized_client.post(url, data=form_data)
    comments_count = Comment.objects.count()
    assert comments_count == comment_create


@pytest.mark.parametrize(
    'parametrized_client, comments_status',
    (
        (pytest.lazy_fixture('author_client'), True),
        (pytest.lazy_fixture('not_author_client'), False),
    )
)
def test__users__edit_delete_comment(parametrized_client, comments_status,
                                     form_data, new, comment):
    url = reverse('news:edit', args=(comment.id,))
    parametrized_client.post(url, data=form_data)
    comment.refresh_from_db()
    assert (comment.text == form_data['text']) == comments_status
    parametrized_client.delete(reverse('news:delete', args=(comment.id,)))
    comment_count = Comment.objects.count()
    assert (comment_count == 0) == comments_status


def test_user_cant_use_bad_words(author_client, new):
    url = reverse('news:detail', args=(new.id,))
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    response = author_client.post(url, data=bad_words_data)
    assert response.context['form'].errors['text'][0] == WARNING
