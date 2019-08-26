import pytest

from repositories.models import Repository
from taggit.managers import TaggableManager
from taggit.models import Tag, TaggedItem

pytestmark = pytest.mark.django_db

@pytest.fixture
def repository():
    '''Returns a Repository instance'''

    repository = Repository.objects.create(
        id="12345678",
        name="Test Repository",
        tags=["Test_tag_1", "Test_tag_2"]
    )
    return repository



def test_save(repository):

    assert repository.name == "Test Repository"
    assert repository.id == "12345678"
    assert repository.tags[0] == "Test_tag_1"
    assert repository.tags[1] == "Test_tag_2"
    assert len(repository.tags) == 2


def test_name_max_length(repository):
    max_length = repository._meta.get_field('name').max_length
    assert max_length == 50


def test_id_max_length(repository):
    max_length = repository._meta.get_field('id').max_length
    assert max_length == 50
