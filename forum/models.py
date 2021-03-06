
from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.db.models.signals import post_save


class Forum(models.Model):
    title = models.CharField(max_length=60)
    def __unicode__(self):
        return self.title

    def num_posts(self):
        return sum([t.num_posts() for t in self.thread_set.all()])

    def last_post(self):
        if self.thread_set.count():
            last = None
            for t in self.thread_set.all():
                l = t.last_post()
                if l:
                    if not last: last = l
                    elif l.created > last.created: last = l
            return last

class Thread(models.Model):
    title = models.CharField(max_length=60)
    created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, blank=True, null=True)
    forum = models.ForeignKey(Forum)

    def __unicode__(self):
        return u'{0:s}'.format(self.creator) + " - " + self.title

    def num_posts(self):
        return self.post_set.count()

    def num_replies(self):
        return self.post_set.count() - 1

    def last_post(self):
        if self.post_set.count():
            return self.post_set.order_by("created")[0]

class Post(models.Model):
    title = models.CharField(max_length=60)
    created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, blank=True, null=True)
    thread = models.ForeignKey(Thread)
    body = models.TextField(max_length=10000)

    @property
    def __unicode__(self):
        return u"%s - %s - %s" % (self.creator, self.thread, self.title)

    def short(self):
        return u"%s - %s\n%s" % (self.creator, self.title, self.created.strftime("%b %d, %I:%M %p"))
    short.allow_tags = True

    def profile_data(self):
        p = self.creator.userprofile_set.all()[0]
        #print "profile data tralalala"
        print p.posts, p.avatar
        return p.posts, "/media/"+p.avatar

    def posts(self):
        p = self.creator.userprofile_set.all()[0]
        return p.posts

    def avatar(self):
        p = self.creator.userprofile_set.all()[0]
        #print p.avatar
        return p.avatar


class UserProfile(models.Model):
    avatar = models.ImageField("Profile Pic", upload_to="media/images/", blank=True, null=True)
    posts = models.IntegerField(default=0)
    user = models.ForeignKey(User, unique=True)

    @property
    def __unicode__(self):
        return self.user

def create_user_profile(sender, **kwargs):
    """When creating a new user, make a profile for him."""
    u = kwargs["instance"]
    #print u
    if not UserProfile.objects.filter(user=u):
        #print "if not UserProfile"
        #print UserProfile(user=u).avatar.name
        UserProfile(user=u).save()
    #else:
    #    print UserProfile(user=u).avatar


post_save.connect(create_user_profile, sender=User)
