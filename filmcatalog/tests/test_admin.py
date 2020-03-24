import pytest


@pytest.mark.django_db
def test_unauthorized(client):
    response = client.get('/admin/')
    assert response.status_code == 302


@pytest.mark.django_db
def test_superuser_view(admin_client):
    response = admin_client.get('/admin/')
    assert response.status_code == 200
