from http import HTTPStatus

from notes.tests.baseclass import BaseClass


class TestRoutes(BaseClass):

    def test_pages_availability(self):
        test_urls = (
            (self.HOME, self.client, HTTPStatus.OK),
            (self.LOGIN, self.client, HTTPStatus.OK),
            (self.LOGOUT, self.client, HTTPStatus.OK),
            (self.SIGNUP, self.client, HTTPStatus.OK),
            (self.LIST, self.author_client, HTTPStatus.OK),
            (self.ADD, self.author_client, HTTPStatus.OK),
            (self.SUCCESS, self.author_client, HTTPStatus.OK),
            (self.DETAIL, self.author_client, HTTPStatus.OK),
            (self.EDIT, self.author_client, HTTPStatus.OK),
            (self.DELETE, self.author_client, HTTPStatus.OK),
            (self.DETAIL, self.reader_client, HTTPStatus.NOT_FOUND),
            (self.EDIT, self.reader_client, HTTPStatus.NOT_FOUND),
            (self.DELETE, self.reader_client, HTTPStatus.NOT_FOUND),
            (self.ADD, self.reader_client, HTTPStatus.OK),
            (self.SUCCESS, self.reader_client, HTTPStatus.OK),
            (self.LIST, self.reader_client, HTTPStatus.OK),
        )
        for url, client, expected_status in test_urls:
            with self.subTest():
                try:
                    self.assertEqual(
                        client.get(url).status_code, expected_status
                    )
                except AssertionError:
                    self.fail(f"Ошибка для URL '{url}': {AssertionError}")

    def test_redirect(self):
        urls = (
            self.DETAIL,
            self.EDIT,
            self.DELETE,
            self.ADD,
            self.SUCCESS,
            self.LIST,
        )
        for url in urls:
            with self.subTest():
                try:
                    self.assertRedirects(
                        self.client.get(url), f'{self.LOGIN}?next={url}'
                    )
                except AssertionError:
                    self.fail(f"Ошибка для URL '{url}': {AssertionError}")
