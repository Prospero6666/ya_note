from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note


User = get_user_model()


class BaseClass(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.reader = User.objects.create(username='Не автор')
        cls.author_client = Client()
        cls.reader_client = Client()
        cls.author_client.force_login(cls.author)
        cls.reader_client.force_login(cls.reader)
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст заметки',
            slug='note-slug',
            author=cls.author,
        )
        cls.form_data = {
            'title': 'Новый заголовок',
            'text': 'Новый текст',
            'slug': 'new-slug',
            'author': cls.author
        }
        cls.HOME = reverse('notes:home')
        cls.LOGIN = reverse('users:login')
        cls.LOGOUT = reverse('users:logout')
        cls.SIGNUP = reverse('users:signup')
        cls.LIST = reverse('notes:list')
        cls.ADD = reverse('notes:add')
        cls.SUCCESS = reverse('notes:success')
        cls.DETAIL = reverse('notes:detail', args=(cls.note.slug,))
        cls.EDIT = reverse('notes:edit', args=(cls.note.slug,))
        cls.DELETE = reverse('notes:delete', args=(cls.note.slug,))
        cls.REDIRECT = f'{cls.LOGIN}?next='
