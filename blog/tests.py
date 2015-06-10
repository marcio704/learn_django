from django.test import TestCase
from django.core.urlresolvers import reverse

# Create your tests here.

### Tests for Views
class BlogViewTests(TestCase):
	def test_if_index_view_is_loaded(self):
		response = self.client.get(reverse('blog:index'))
		self.assertEqual(response.status_code, 200)
		self.assertGreater(len(response.content), 0)
