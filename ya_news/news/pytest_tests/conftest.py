from datetime import datetime, timedelta
from django.test.client import Client
from django.urls import reverse
import pytest

from news.models import Comment, News
from yanews.settings import NEWS_COUNT_ON_HOME_PAGE


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def anonymous_client():
    client = Client()
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def new():
    new = News.objects.create(
        title='Заголовок',
        text='Текст заметки',
    )
    return new


@pytest.fixture
def news():
    today = datetime.today()
    news = News.objects.bulk_create(
        News(title=f'Новость {index}', text='Просто текст.',
             date=today - timedelta(days=index))
        for index in range(NEWS_COUNT_ON_HOME_PAGE + 1)
    )
    return news


@pytest.fixture
def comment(author, new):
    comment = Comment.objects.create(
        news=new,
        author=author,
        text='Текст',
    )
    return comment


@pytest.fixture
def comments(author, new):
    today = datetime.today()
    comments = Comment.objects.bulk_create(
        Comment(news=new, author=author, text=f'Текст {index}',
                created=today - timedelta(days=index))
        for index in range(10)
    )
    return comments


@pytest.fixture
def form_data():
    return {
        'text': 'Новый текст'
    }


@pytest.fixture
def url_home():
    return reverse('news:home')


@pytest.fixture
def url_detail(new):
    return reverse('news:detail', args=[new.id])


@pytest.fixture
def url_login():
    return reverse('users:login')


@pytest.fixture
def url_logout():
    return reverse('users:logout')


@pytest.fixture
def url_signup():
    return reverse('users:signup')


@pytest.fixture
def url_edit(comment):
    return reverse('news:edit', args=[comment.id])


@pytest.fixture
def url_delete(comment):
    return reverse('news:delete', args=[comment.id])
