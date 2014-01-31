from django.test import TestCase
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from forum.models import *
# Create your tests here.

class SimpleTest(TestCase):
    def setUp(self):
        f = Forum.objects.create(title="forum")
        u = User.objects.create_user("ak", "ak@abc.org", "pwd")
        t = Thread.objects.create(title="thread", creator=u, forum=f)
        p = Post.objects.create(title="post", body="body", creator=u, thread=t)


    def content_test(self, url, values):
        """Get content of url and test that each of items in `values` list is present."""
        r = self.c.get(url)
        self.assertEquals(r.status_code, 200)
        for v in values:
            #print "V: " +v
            #print "R: " +r.content
            self.assertTrue(v in r.content)

    def test(self):
        self.c = Client()
        self.c.login(username="ak", password="pwd")

        self.content_test("", ['<a href="/1/forum/">forum</a>'])
        self.content_test("/1/forum/", ['<a href="/1/thread/">thread</a>', "ak - post"])

        self.content_test("/1/thread/", ['<div class="ttitle">thread</div>',
               '<span class="title">post</span>', 'body <br />', 'by ak |'])

        r = self.c.post("/post/new_thread/1/", {"subject": "thread2", "body": "body2"})

        r = self.c.post("/post/reply/1/", {"subject": "post2", "body": "body3"})

        self.c.logout()
