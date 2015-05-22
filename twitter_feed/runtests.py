import os, sys
import django
from django.test.utils import get_runner
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "twitter_feed.test_settings")
django.setup()


test_dir = os.path.dirname(__file__)
sys.path.insert(0, test_dir)


def runtests():
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=1, interactive=True)
    failures = test_runner.run_tests(['twitter_feed'])
    sys.exit(bool(failures))
