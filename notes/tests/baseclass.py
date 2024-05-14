from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note


User = get_user_model()


class BaseClass(TestCase):
    HOME = reverse('notes:home')
    LOGIN = reverse('users:login')
    LOGOUT = reverse('users:logout')
    SIGNUP = reverse('users:signup')
    LIST = reverse('notes:list')
    ADD = reverse('notes:add')
    SUCCESS = reverse('notes:success')

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
        }
        cls.DETAIL = reverse('notes:detail', args=(cls.note.slug,))
        cls.EDIT = reverse('notes:edit', args=(cls.note.slug,))
        cls.DELETE = reverse('notes:delete', args=(cls.note.slug,))
