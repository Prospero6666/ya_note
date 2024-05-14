from http import HTTPStatus

from pytils.translit import slugify

from notes.forms import WARNING
from notes.models import Note
from notes.tests.baseclass import BaseClass


class TestNoteCreation(BaseClass):

    def test_author_can_create_note(self):
        Note.objects.all().delete()
        notes_count_before = Note.objects.count()
        self.assertEqual(notes_count_before, 0)
        response = self.author_client.post(
            self.ADD,
            data=self.form_data
        )
        self.assertRedirects(response, self.SUCCESS)
        notes_count_after = Note.objects.count()
        self.assertEqual(notes_count_after, 1)
        new_note = Note.objects.get()
        self.assertEqual(new_note.title, self.form_data['title'])
        self.assertEqual(new_note.text, self.form_data['text'])
        self.assertEqual(new_note.slug, self.form_data['slug'])
        self.assertEqual(new_note.author, self.form_data['author'])

    def test_anonymous_user_cant_create_note(self):
        notes_count_before = Note.objects.count()
        response = self.client.post(self.ADD, data=self.form_data)
        notes_count_after = Note.objects.count()
        self.assertRedirects(response, self.REDIRECT + self.ADD)
        self.assertEqual(notes_count_before, notes_count_after)

    def test_not_unique_slug(self):
        notes_count_before = Note.objects.count()
        self.form_data['slug'] = self.note.slug
        response = self.author_client.post(
            self.ADD,
            data=self.form_data
        )
        notes_count_after = Note.objects.count()
        self.assertFormError(
            response,
            'form',
            'slug',
            errors=(self.note.slug + WARNING)
        )
        self.assertEqual(notes_count_before, notes_count_after)

    def test_empty_slug(self):
        Note.objects.all().delete()
        notes_count_before = Note.objects.count()
        self.assertEqual(notes_count_before, 0)
        self.form_data.pop('slug')
        response = self.author_client.post(
            self.ADD,
            data=self.form_data
        )
        self.assertRedirects(response, self.SUCCESS)
        notes_count_after = Note.objects.count()
        self.assertEqual(notes_count_after, 1)
        new_note = Note.objects.get()
        expected_slug = slugify(self.form_data['title'])
        self.assertEqual(new_note.title, self.form_data['title'])
        self.assertEqual(new_note.text, self.form_data['text'])
        self.assertEqual(new_note.slug, expected_slug)
        self.assertEqual(new_note.author, self.form_data['author'])

    def test_author_can_edit_note(self):
        Note.objects.all()
        notes_count_before = Note.objects.count()
        self.assertEqual(notes_count_before, 1)
        response = self.author_client.post(
            self.EDIT,
            data=self.form_data
        )
        self.assertRedirects(response, self.SUCCESS)
        notes_count_after = Note.objects.count()
        self.assertEqual(notes_count_after, 1)
        new_note = Note.objects.get()
        self.assertEqual(new_note.title, self.form_data['title'])
        self.assertEqual(new_note.text, self.form_data['text'])
        self.assertEqual(new_note.slug, self.form_data['slug'])
        self.assertEqual(new_note.author, self.form_data['author'])

    def test_not_author_cant_edit_note(self):
        response = self.reader_client.post(
            self.EDIT,
            data=self.form_data
        )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note_from_db = Note.objects.get(id=self.note.id)
        self.assertEqual(self.note.title, note_from_db.title)
        self.assertEqual(self.note.text, note_from_db.text)
        self.assertEqual(self.note.slug, note_from_db.slug)
        self.assertEqual(self.note.author, note_from_db.author)

    def test_author_can_delete_note(self):
        Note.objects.all()
        notes_count_before = Note.objects.count()
        self.assertEqual(notes_count_before, 1)
        response = self.author_client.post(self.DELETE)
        self.assertRedirects(response, self.SUCCESS)
        notes_count_after = Note.objects.count()
        self.assertEqual(notes_count_after, 0)

    def test_not_author_cant_delete_note(self):
        notes_count_before = Note.objects.count()
        response = self.reader_client.post(self.DELETE)
        notes_count_after = Note.objects.count()
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(notes_count_before, notes_count_after)
