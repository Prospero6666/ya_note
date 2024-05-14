from http import HTTPStatus

from pytils.translit import slugify

from notes.forms import WARNING
from notes.models import Note
from notes.tests.baseclass import BaseClass
from notes.tests.baseclass import LOGIN, ADD, SUCCESS, EDIT, DELETE


class TestNoteCreation(BaseClass):

    def create_note(self):
        Note.objects.all().delete()
        response = self.author_client.post(
            ADD,
            data=self.form_data
        )
        self.assertRedirects(response, SUCCESS)
        self.assertEqual(Note.objects.count(), 1)
        new_note = Note.objects.get()
        self.assertEqual(new_note.title, self.form_data['title'])
        self.assertEqual(new_note.text, self.form_data['text'])
        self.assertEqual(new_note.slug, self.form_data['slug'])
        self.assertEqual(new_note.author, self.author)

    def test_author_can_create_note(self):
        self.create_note()

    def test_anonymous_user_cant_create_note(self):
        Note.objects.all().delete()
        response = self.client.post(ADD, data=self.form_data)
        self.assertRedirects(response, f'{LOGIN}?next={ADD}')
        self.assertEqual(Note.objects.count(), 0)

    def test_not_unique_slug(self):
        self.assertEqual(Note.objects.count(), 1)
        note_from_db = Note.objects.get()
        self.form_data['slug'] = self.note.slug
        response = self.author_client.post(
            ADD,
            data=self.form_data
        )
        self.assertFormError(
            response,
            'form',
            'slug',
            errors=(self.note.slug + WARNING)
        )
        self.assertEqual(Note.objects.count(), 1)
        self.assertEqual(note_from_db.text, self.note.text)
        self.assertEqual(note_from_db.title, self.note.title)
        self.assertEqual(note_from_db.slug, self.note.slug)
        self.assertEqual(note_from_db.author, self.note.author)

    def test_empty_slug(self):
        self.form_data.pop('slug')
        self.form_data['slug'] = slugify(self.form_data['title'])
        self.create_note()

    def test_author_can_edit_note(self):
        self.assertEqual(Note.objects.count(), 1)
        response = self.author_client.post(
            EDIT,
            data=self.form_data
        )
        self.assertRedirects(response, SUCCESS)
        self.assertEqual(Note.objects.count(), 1)
        edited_note = Note.objects.get(id=self.note.id)
        self.assertEqual(edited_note.title, self.form_data['title'])
        self.assertEqual(edited_note.text, self.form_data['text'])
        self.assertEqual(edited_note.slug, self.form_data['slug'])
        self.assertEqual(edited_note.author, self.note.author)

    def test_not_author_cant_edit_note(self):
        response = self.reader_client.post(
            EDIT,
            data=self.form_data
        )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note_from_db = Note.objects.get(id=self.note.id)
        self.assertEqual(self.note.title, note_from_db.title)
        self.assertEqual(self.note.text, note_from_db.text)
        self.assertEqual(self.note.slug, note_from_db.slug)
        self.assertEqual(self.note.author, note_from_db.author)

    def test_author_can_delete_note(self):
        response = self.author_client.post(
            ADD,
            data=self.form_data
        )
        self.assertEqual(Note.objects.count(), 2)
        response = self.author_client.post(DELETE)
        self.assertRedirects(response, SUCCESS)
        self.assertEqual(Note.objects.count(), 1)

    def test_not_author_cant_delete_note(self):
        note_from_db = Note.objects.get(id=self.note.id)
        self.assertEqual(Note.objects.count(), 1)
        response = self.reader_client.post(DELETE)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(Note.objects.count(), 1)
        self.assertEqual(note_from_db.text, self.note.text)
        self.assertEqual(note_from_db.title, self.note.title)
        self.assertEqual(note_from_db.slug, self.note.slug)
        self.assertEqual(note_from_db.author, self.note.author)
