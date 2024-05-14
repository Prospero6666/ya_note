from notes.forms import NoteForm
from notes.models import Note
from notes.tests.baseclass import BaseClass


class TestContent(BaseClass):

    def test_notes_list_for_author_client(self):
        response = self.author_client.get(self.LIST)
        notes_list = response.context['object_list']
        self.assertIn(self.note, notes_list)
        notes_counts = Note.objects.count()
        self.assertEqual(notes_counts, 1)
        author_client_note = Note.objects.get()
        self.assertEqual(author_client_note.title, self.note.title)
        self.assertEqual(author_client_note.text, self.note.text)
        self.assertEqual(author_client_note.slug, self.note.slug)
        self.assertEqual(author_client_note.author, self.note.author)

    def test_notes_list_for_reader_client(self):
        self.assertNotIn(
            self.note, self.reader_client.get(self.LIST).context['object_list']
        )

    def test_pages_contains_form(self):
        urls = (self.ADD, self.EDIT)
        for url in urls:
            for url in urls:
                with self.subTest(msg=f"Ошибка для URL '{url}'"):
                    response = self.author_client.get(url)
                    self.assertIn(
                        'form', response.context,
                        msg="Форма отсутствует в контексте страницы"
                    )
                    self.assertIsInstance(
                        response.context['form'], NoteForm,
                        msg="Неверный тип формы"
                    )
