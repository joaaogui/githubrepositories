import pytest

from repositories.models import Repository
from taggit.managers import TaggableManager
from taggit.models import Tag, TaggedItem

pytestmark = pytest.mark.django_db


class TestRepositoryModel:

    def test_save(self):
        repository = Repository.objects.create(
            id = "12345678",
            name ="Test Repository",
            tags = ["Test_tag_1", "Test_tag_2"]
        )
        assert repository.name == "Test Repository"
        assert repository.id == "12345678"
        assert repository.tags[0] ==  "Test_tag_1"
        assert repository.tags[1] ==  "Test_tag_2"
        assert len(repository.tags) == 2

    # def test_tag_adding(self):

