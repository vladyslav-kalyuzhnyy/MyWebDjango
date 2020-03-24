import pytest

from django.contrib.auth.models import User


@pytest.mark.django_db
def test_user_create():
    User.objects.create_user('testuser', 'lennon@thebeatles.com', 'testpassword')
    assert User.objects.count() == 1
