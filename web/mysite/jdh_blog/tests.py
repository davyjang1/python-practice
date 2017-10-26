from datetime import datetime
from django.test import TestCase
#from django.test.client import Client
from jdh_blog.models import BlogPost

class BlogPostTest(TestCase):
    def test_obj_create(self):
        BlogPost.objects.create(title = 'raw_file', 
                body = 'raw_body', timestamp = datetime.now())
        self.assertEqual(1, BlogPost.objects.count())
        self.assertEqual('raw_file', BlogPost.objects.get(id = 1).title)
    def test_slash(self):
        response = self.client.get('/')
        self.assertIn(response.status_code, (301, 302))
