from __future__ import absolute_import

from twitter import models as twitter_models
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailsnippets.models import register_snippet

register_snippet(twitter_models.User)

twitter_models.User.panels = [
    FieldPanel('screen_name'),
    FieldPanel('active'),
]
