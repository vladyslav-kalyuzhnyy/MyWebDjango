from django.urls import reverse, resolve


class TestUrl:
    def test_detail_url(self):
        path = reverse('add_review', kwargs={'pk': 1})
        assert resolve(path).view_name == 'add_review'
