import unittest
from dungeonjournal.post import *

class TestPost(unittest.TestCase):

    def test_convert_post(self):
        self.assert_post({"title": "Article", "link": "article", "created_date": "05/07/2017", "content": "Hello", "preview_content": "World"},
            convert_post({"title": "Article", "link": "article", "created_datetime": "2017-07-05 00:00:00+00:00", "content": "Hello", "preview_content": "World"}))

    def test_convert_post_empty_values(self):
        self.assert_post({"title": "", "link": "", "created_date": "", "content": "", "preview_content": ""},
            convert_post({"title": "", "link": "", "created_date": "", "content": "", "preview_content": ""}))

    def test_convert_post_null_values(self):
        """Testing no exception is thrown"""
        convert_post({"title": None, "link": None, "created_date": None, "content": None, "preview_content": None})

    def test_convert_post_no_values(self):
        # Testing no exception is thrown.
        convert_posts({})

    def test_convert_posts(self):
        converted_posts = convert_posts([
            {"title": "Article One", "link": "article_one", "created_datetime": "2017-07-05 00:00:00+00:00", "content": "Content of Article One"},
            {"title": "Article X", "link": "article_x", "created_datetime": "9999-01-01 00:00:00+00:00", "preview_content": "Preview Content of Article X"},
        ])
        self.assert_post({"title": "Article One", "link": "article_one", "created_date": "05/07/2017", "content": "Content of Article One"}, converted_posts[0])
        self.assert_post({"title": "Article X", "link": "article_x", "created_date": "01/01/9999", "preview_content": "Preview Content of Article X"}, converted_posts[1])

    def test_convert_archive_posts(self):
        archive = convert_archive_posts([
            {"title": "Article Two", "link": "article_two", "created_year": "2017", "created_month": "July"},
            {"title": "Article One", "link": "article_one", "created_year": "2017", "created_month": "July"},
            {"title": "Older Article", "link": "old_article", "created_year": "2017", "created_month": "January"},
            {"title": "Ancient Article", "link": "ancient_article", "created_year": "2015", "created_month": "November"},
        ])

        self.assertEqual(2, len(archive))
        # 2017
        year = archive[0]
        self.assertEqual("2017", year["year"])
        self.assertEqual(2, len(year["months"]))
        # July
        month = year["months"][0]
        self.assertEqual("July", month["month"])
        self.assertEqual(2, len(month["posts"]))
        self.assert_post({"title": "Article Two", "link": "article_two"}, month["posts"][0])
        self.assert_post({"title": "Article One", "link": "article_one"}, month["posts"][1])
        # January
        month = year["months"][1]
        self.assertEqual("January", month["month"])
        self.assertEqual(1, len(month["posts"]))
        self.assert_post({"title": "Older Article", "link": "old_article"}, month["posts"][0])
        # 2015
        year = archive[1]
        self.assertEqual("2015", year["year"])
        self.assertEqual(1, len(year["months"]))
        # November
        month = year["months"][0]
        self.assertEqual("November", month["month"])
        self.assertEqual(1, len(month["posts"]))
        self.assert_post({"title": "Ancient Article", "link": "ancient_article"}, month["posts"][0])

    def test_convert_archive_posts_empty_list(self):
        # Testing no exception is thrown.
        convert_archive_posts(())

    def assert_post(self, expected_post, actual_post):
        self.assert_post_value("title", expected_post, actual_post)
        self.assert_post_value("link", expected_post, actual_post)
        self.assert_post_value("created_date", expected_post, actual_post)
        self.assert_post_value("content", expected_post, actual_post)
        self.assert_post_value("preview_content", expected_post, actual_post)

    def assert_post_value(self, value_name, expected_post, actual_post):
        if value_name in expected_post:
            self.assertEqual(expected_post[value_name], actual_post[value_name])
        else:
            self.assertFalse(value_name in actual_post)
