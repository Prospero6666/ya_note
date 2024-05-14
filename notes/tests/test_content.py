from notes.forms import NoteForm
from notes.tests.baseclass import BaseClass


class TestContent(BaseClass):

    def test_notes_list_for_author_client(self):
        response = self.author_client.get(self.LIST)
        notes_list = response.context['object_list']
        self.assertTrue(self.note in notes_list)
        for note in notes_list:
            self.assertEqual(note.title, self.note.title)
            self.assertEqual(note.text, self.note.text)
            self.assertEqual(note.slug, self.note.slug)
            self.assertEqual(note.author, self.note.author)

    def test_notes_list_for_reader_client(self):
        response = self.reader_client.get(self.LIST)
        notes_list = response.context['object_list']
        self.assertFalse(self.note in notes_list)

    def test_pages_contains_form(self):
        urls = (self.ADD, self.EDIT)
        for url in urls:
            with self.subTest():
                try:
                    response = self.author_client.get(url)
                    self.assertIn('form', response.context)
                    self.assertIsInstance(response.context['form'], NoteForm)
                except AssertionError:
                    self.fail(f"Ошибка для URL '{url}': {AssertionError}")
