from __future__ import absolute_import

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.template import TemplateSyntaxError
from twitter import models as twitter_models
from wagtail.tests.utils import WagtailTestUtils
from twitter_feed.templatetags import twitter_tags


class TestTwitterFeedCreateView(TestCase, WagtailTestUtils):
    def setUp(self):
        self.login()

    def get(self, params={}):
        return self.client.get(reverse('wagtailsnippets_create',
                                       args=('twitter', 'user')),
                               params)

    def post(self, post_data={}):
        return self.client.post(reverse('wagtailsnippets_create',
                               args=('twitter', 'user')),
                               post_data)

    def test_simple(self):
        response = self.get()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wagtailsnippets/snippets/create.html')

    def test_create_invalid(self):
        response = self.post(post_data={'active': 'True'})
        self.assertContains(response, "The snippet could not be created due to errors.")
        self.assertContains(response, "This field is required.")

    def test_create_active(self):
        response = self.post(post_data={'screen_name': 'twitter',
                                        'active': 'True'})
        self.assertRedirects(response, reverse('wagtailsnippets_list', args=('twitter', 'user')))

        snippets = twitter_models.User.objects.filter(screen_name='twitter')
        self.assertEqual(snippets.count(), 1)
        self.assertEqual(snippets.first().active, True)

    def test_create_inactive(self):
        response = self.post(post_data={'screen_name': 'twitter',
                                        'active': 'False'})
        self.assertRedirects(response, reverse('wagtailsnippets_list', args=('twitter', 'user')))

        snippets = twitter_models.User.objects.filter(screen_name='twitter')
        self.assertEqual(snippets.count(), 1)
        self.assertEqual(snippets.first().active, False)


class TestTwitterFeedEditView(TestCase, WagtailTestUtils):
    fixtures = ['test.json']

    def setUp(self):
        self.test_snippet = twitter_models.User.objects.get(id=1)
        self.login()

    def get(self, params={}):
        return self.client.get(reverse('wagtailsnippets_edit',
                                       args=('twitter', 'user', self.test_snippet.id)),
                               params)

    def post(self, post_data={}):
        return self.client.post(reverse('wagtailsnippets_edit',
                                        args=('twitter', 'user', self.test_snippet.id)),
                                post_data)

    def test_simple(self):
        response = self.get()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wagtailsnippets/snippets/edit.html')

    def test_non_existant_model(self):
        response = self.client.get(reverse('wagtailsnippets_edit', args=('twitter', 'foo', self.test_snippet.id)))
        self.assertEqual(response.status_code, 404)

    def test_nonexistant_id(self):
        response = self.client.get(reverse('wagtailsnippets_edit', args=('twitter', 'user', 999999)))
        self.assertEqual(response.status_code, 404)

    def test_edit_invalid(self):
        response = self.post(post_data={'active': 'False'})
        self.assertContains(response, "The snippet could not be saved due to errors.")
        self.assertContains(response, "This field is required.")

    def test_edit(self):
        response = self.post(post_data={'screen_name': 'editted_twitter',
                                        'active': 'False'})
        self.assertRedirects(response, reverse('wagtailsnippets_list', args=('twitter', 'user')))

        snippets = twitter_models.User.objects.filter(screen_name='editted_twitter')
        self.assertEqual(snippets.count(), 1)
        self.assertEqual(snippets.first().active, False)


class TestTwitterFeedDelete(TestCase, WagtailTestUtils):
    fixtures = ['test.json']

    def setUp(self):
        self.test_snippet = twitter_models.User.objects.get(id=1)
        self.login()

    def test_delete_get(self):
        response = self.client.get(reverse('wagtailsnippets_delete', args=('twitter', 'user', self.test_snippet.id, )))
        self.assertEqual(response.status_code, 200)

    def test_delete_post(self):
        post_data = {'foo': 'bar'} # For some reason, this test doesn't work without a bit of POST data
        response = self.client.post(reverse('wagtailsnippets_delete', args=('twitter', 'user', self.test_snippet.id, )), post_data)

        # Should be redirected to explorer page
        self.assertRedirects(response, reverse('wagtailsnippets_list', args=('twitter', 'user')))

        # Check that the page is gone
        self.assertEqual(twitter_models.User.objects.filter(screen_name='twitter').count(), 0)


class TestLatestTweetsTemplateTag(TestCase):
    fixtures = ['test.json']

    def test_get_tweets_valid_number(self):
        tweets = twitter_tags.latest_tweets(2)
        self.assertEqual(len(tweets), 2)

    def test_get_tweets_not_a_number_raises_error(self):
        # tweets = twitter_tags.latest_tweets("Five")
        self.assertRaisesMessage(TemplateSyntaxError, "Tag latest_tweets requires a single positive integer argument, given 'Five'.", twitter_tags.latest_tweets, "Five")

    def test_get_more_tweets_then_exist_returns_all(self):
        tweets = twitter_tags.latest_tweets(200)
        self.assertEqual(len(tweets), twitter_models.Tweet.objects.all().count())


    def test_get_tweets_negative_number_raises_error(self):
        self.assertRaisesMessage(TemplateSyntaxError, "Tag latest_tweets requires a single positive integer argument, given -1.", twitter_tags.latest_tweets, -1)
