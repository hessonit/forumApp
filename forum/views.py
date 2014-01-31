from django.conf.global_settings import MEDIA_URL, MEDIA_ROOT
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.core.paginator import InvalidPage, EmptyPage, Paginator
from django.core.urlresolvers import reverse
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response

from forum.models import Forum, Thread, Post, UserProfile
from PIL import Image as PImage
from os.path import join as pjoin

class ProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        exclude = ["posts", "user"]

@login_required
def profile(request, pk):
    """Edit user profile."""
    u = User.objects.get(id=pk)
    profile, a = UserProfile.objects.get_or_create(user=u)#pk)
    img = None

    if request.method == "POST":
        pf = ProfileForm(request.POST, request.FILES, instance=profile)
        if pf.is_valid():
            pf.save()
            # resize and save image under same filename
            imfn = pjoin("media"+MEDIA_ROOT, profile.avatar.name)
            try:
                print "resize"
                im = PImage.open(imfn)
                im.thumbnail((80,80), PImage.ANTIALIAS)
                im.save(imfn, "JPEG")
            except:
                print "dupa"
                pass
    else:
        pf = ProfileForm(instance=profile)

    if profile.avatar:
        img = "/media/" + profile.avatar.name
        print profile.avatar.name
    else:
        img = "/media/media/images/images.jpg"
        profile.avatar.name = "media/images/images.jpg"
        profile.save()

    return render_to_response("forum/profile.html", add_csrf(request, pf=pf, img=img))

def main(request):
    """Main listing."""
    forums = Forum.objects.all()
    return render(request, 'forum/list.html', dict(forums=forums, user=request.user))

def add_csrf(request, ** kwargs):
    d = dict(user=request.user, ** kwargs)
    d.update(csrf(request))
    return d

def mk_paginator(request, items, num_items):
    """Create and return a paginator."""
    paginator = Paginator(items, num_items)
    try: page = int(request.GET.get("page", '1'))
    except ValueError: page = 1

    try:
        items = paginator.page(page)
    except (InvalidPage, EmptyPage):
        items = paginator.page(paginator.num_pages)
    return items


def forum(request, pk):
    """Listing of threads in a forum."""
    threads = Thread.objects.filter(forum=pk).order_by("-created")
    threads = mk_paginator(request, threads, 10)
    return render(request, "forum/forum.html", add_csrf(request, threads=threads, pk=pk))

def thread(request, pk):
    """Listing of posts in a thread."""
    posts = Post.objects.filter(thread=pk).order_by("created")
    posts = mk_paginator(request, posts, 10)
    title = Thread.objects.get(pk=pk).title
    t = Thread.objects.get(pk=pk)
    return render_to_response("forum/thread.html", add_csrf(request, posts=posts, pk=pk, title=t.title,
                                                           forum_pk=t.forum.pk, media_url=MEDIA_URL))
@login_required
def post(request, ptype, pk):
    """Display a post form."""
    action = reverse("forum.views.%s" % ptype, args=[pk])
    print("forum.views.%s" % ptype)
    #print(action)
    if ptype == "new_thread":
        title = "Start New Topic"
        subject = ''
        #print("loooooooooooooooooooool")
    elif ptype == "reply":
        title = "Reply"
        subject = "Re: " + Thread.objects.get(pk=pk).title
    #print "loo00ooooooool"
    return render(request, "forum/post.html", add_csrf(request, subject=subject, action=action,
                                                          title=title))

def increment_post_counter(request):
    profile = request.user.userprofile_set.all()[0]
    profile.posts += 1
    profile.save()


def aaa():
    return 2

@login_required
def new_thread(request, pk):
    """Start a new thread."""
    #print "new_thread aaaaaaaaaaaaaaaaaaaaaaa"
    p = request.POST
    if p["subject"] and p["body"]:
        #print UserProfile(user=request.user).avatar
        #print str(UserProfile(user=request.user).avatar)

        forum = Forum.objects.get(pk=pk)
        thread = Thread.objects.create(forum=forum, title=p["subject"], creator=request.user)
        Post.objects.create(thread=thread, title=p["subject"], body=p["body"], creator=request.user)
        increment_post_counter(request)

    return HttpResponseRedirect(reverse("forum.views.forum", args=[pk]))

@login_required
def reply(request, pk):
    """Reply to a thread."""
    p = request.POST
    if p["body"]:
        #print "request user: "
        #print request.user
        u = User.objects.get(username=request.user)
        #print u.email
        profile = UserProfile.objects.get(user=u)#pk)
        #print profile.avatar.name
        #print profile.posts
        thread = Thread.objects.get(pk=pk)
        post = Post.objects.create(thread=thread, title=p["subject"], body=p["body"], creator=request.user)
        increment_post_counter(request)
    return HttpResponseRedirect(reverse("forum.views.thread", args=[pk]) + "?page=last")


