import pytest

from repositories.models import Repository
from taggit.managers import TaggableManager
from taggit.models import Tag, TaggedItem

from repositories.view
pytestmark = pytest.mark.django_db