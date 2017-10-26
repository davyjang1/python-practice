from django.http import HttpResponse
from django.template import loader, Context
from jdh_blog.models import BlogPost, BlogPostForm

def archive(request):
    posts = BlogPost.objects.all().order_by('-timestamp')
    t = loader.get_template("archive.html")
    #c = Context({'posts': posts})
    return HttpResponse(t.render({'posts': posts, 'form' : BlogPostForm()}, request))
    
from datetime import datetime
from django.http import HttpResponseRedirect

def create_blogpost(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit = False)
            post.timestamp = datetime.now()
            post.save()
    return HttpResponseRedirect('/blog/')

