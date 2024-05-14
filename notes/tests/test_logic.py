from http import HTTPStatus

from pytils.translit import slugify

from notes.forms import WARNING
from notes.models import Note
from notes.tests.baseclass import BaseClass


class TestNoteCreation(BaseClass):

    def create_note(self):
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
        return Note.objects.get()

    def test_author_can_create_note(self):
        new_note = self.create_note()
        self.assertEqual(new_note.title, self.form_data['title'])
        self.assertEqual(new_note.text, self.form_data['text'])
        self.assertEqual(new_note.slug, self.form_data['slug'])
        self.assertEqual(new_note.author, self.author)

    def test_anonymous_user_cant_create_note(self):
        notes_count_before = Note.objects.count()
        self.assertEqual(notes_count_before, 1)
        response = self.client.post(self.ADD, data=self.form_data)
        self.assertRedirects(response, f'{self.LOGIN}?next={self.ADD}')
        notes_count_after = Note.objects.count()
        self.assertEqual(notes_count_after, 1)

    def test_not_unique_slug(self):
        notes_count_before = Note.objects.count()
        self.assertEqual(notes_count_before, 1)
        self.form_data['slug'] = self.note.slug
        response = self.author_client.post(
            self.ADD,
            data=self.form_data
        )
        self.assertFormError(
            response,
            'form',
            'slug',
            errors=(self.note.slug + WARNING)
        )
        notes_count_after = Note.objects.count()
        self.assertEqual(notes_count_after, 1)

    def test_empty_slug(self):
        form_data = self.form_data
        form_data.pop('slug')
        new_note = self.create_note()
        expected_slug = slugify(form_data['title'])
        self.assertEqual(new_note.title, form_data['title'])
        self.assertEqual(new_note.text, form_data['text'])
        self.assertEqual(new_note.slug, expected_slug)
        self.assertEqual(new_note.author, self.author)

    def test_author_can_edit_note(self):
        notes_count_before = Note.objects.count()
        self.assertEqual(notes_count_before, 1)
        response = self.author_client.post(
            self.EDIT,
            data=self.form_data
        )
        self.assertRedirects(response, self.SUCCESS)
        notes_count_after = Note.objects.count()
        self.assertEqual(notes_count_after, 1)
        edited_note = Note.objects.get(id=self.note.id)
        self.assertEqual(edited_note.title, self.form_data['title'])
        self.assertEqual(edited_note.text, self.form_data['text'])
        self.assertEqual(edited_note.slug, self.form_data['slug'])
        self.assertEqual(edited_note.author, self.author)

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
        self.assertEqual(notes_count_before, 1)
        response = self.reader_client.post(self.DELETE)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        notes_count_after = Note.objects.count()
        self.assertEqual(notes_count_after, 1)
