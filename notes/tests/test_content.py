from notes.forms import NoteForm
from notes.models import Note
from notes.tests.baseclass import BaseClass
from notes.tests.baseclass import LIST, ADD, EDIT


class TestContent(BaseClass):

    def test_notes_list_for_author_client(self):
        response = self.author_client.get(LIST)
        notes_list = response.context['object_list']
        self.assertIn(self.note, notes_list)
        self.assertEqual(Note.objects.count(), 1)
        author_client_note = notes_list[0]
        self.assertEqual(author_client_note.title, self.note.title)
        self.assertEqual(author_client_note.text, self.note.text)
        self.assertEqual(author_client_note.slug, self.note.slug)
        self.assertEqual(author_client_note.author, self.note.author)

    def test_notes_list_for_reader_client(self):
        self.assertNotIn(
            self.note, self.reader_client.get(LIST).context['object_list']
        )

    def test_pages_contains_form(self):
        urls = (ADD, EDIT)
        for url in urls:
            with self.subTest(url=url, msg=f"Ошибка для URL '{url}'"):
                self.assertIsInstance(
                    self.author_client.get(url).context['form'], NoteForm
                )
