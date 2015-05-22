from django import template
from twitter.models import Tweet

register = template.Library()


@register.assignment_tag
def latest_tweets(number_of_tweets=2):
    tweets = Tweet.objects.filter(
        user__active=True).order_by('-time')[:number_of_tweets]
    return tweets
