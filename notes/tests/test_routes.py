from http import HTTPStatus

from notes.tests.baseclass import BaseClass
from notes.tests.baseclass import (
    HOME, LOGIN, LOGOUT, SIGNUP,
    LIST, ADD, SUCCESS, DETAIL,
    EDIT, DELETE, DETAIL_REDIRECT,
    EDIT_REDIRECT, DELETE_REDIRECT,
    ADD_REDIRECT, SUCCESS_REDIRECT,
    LIST_REDIRECT
)


class TestRoutes(BaseClass):

    def test_pages_availability(self):
        test_urls = (
            (HOME, self.client, HTTPStatus.OK),
            (LOGIN, self.client, HTTPStatus.OK),
            (LOGOUT, self.client, HTTPStatus.OK),
            (SIGNUP, self.client, HTTPStatus.OK),
            (LIST, self.author_client, HTTPStatus.OK),
            (ADD, self.author_client, HTTPStatus.OK),
            (SUCCESS, self.author_client, HTTPStatus.OK),
            (DETAIL, self.author_client, HTTPStatus.OK),
            (EDIT, self.author_client, HTTPStatus.OK),
            (DELETE, self.author_client, HTTPStatus.OK),
            (DETAIL, self.reader_client, HTTPStatus.NOT_FOUND),
            (EDIT, self.reader_client, HTTPStatus.NOT_FOUND),
            (DELETE, self.reader_client, HTTPStatus.NOT_FOUND),
            (ADD, self.reader_client, HTTPStatus.OK),
            (SUCCESS, self.reader_client, HTTPStatus.OK),
            (LIST, self.reader_client, HTTPStatus.OK),
            (LIST, self.client, HTTPStatus.FOUND),
            (ADD, self.client, HTTPStatus.FOUND),
            (SUCCESS, self.client, HTTPStatus.FOUND),
            (DETAIL, self.client, HTTPStatus.FOUND),
            (EDIT, self.client, HTTPStatus.FOUND),
            (DELETE, self.client, HTTPStatus.FOUND),
        )
        for url, client, expected_status in test_urls:
            with self.subTest(
                url=url, client=client, expected_status=expected_status
            ):
                self.assertEqual(
                    client.get(url).status_code, expected_status
                )

    def test_redirect(self):
        urls = (
            (DETAIL, self.client, DETAIL_REDIRECT),
            (EDIT, self.client, EDIT_REDIRECT),
            (DELETE, self.client, DELETE_REDIRECT),
            (ADD, self.client, ADD_REDIRECT),
            (SUCCESS, self.client, SUCCESS_REDIRECT),
            (LIST, self.client, LIST_REDIRECT)
        )
        for url, anonym, expected_url in urls:
            with self.subTest(
                url=url, anonym=anonym, expected_url=expected_url
            ):
                self.assertRedirects(anonym.get(url), expected_url)
