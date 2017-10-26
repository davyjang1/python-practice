from django.http import HttpResponse
from django.template import loader, Context
from jdh_blog.models import BlogPost

def archive(request):
    posts = BlogPost.objects.all().order_by('-timestamp')
    t = loader.get_template("archive.html")
    #c = Context({'posts': posts})
    return HttpResponse(t.render({'posts': posts}, request))
    
from datetime import datetime
from django.http import HttpResponseRedirect

def create_blogpost(request):
    if request.method == 'POST':
        BlogPost(
                title=request.POST.get('title'),
                body=request.POST.get('body'),
                timestamp=datetime.now(),
                ).save()
    return HttpResponseRedirect('/blog/')

