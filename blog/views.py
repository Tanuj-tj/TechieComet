from django.shortcuts import render, HttpResponse,redirect
from blog.models import Post, BlogComment
from django.contrib import messages
from blog.templatetags import extras
from .forms import PostEditForm

def blogHome(request):
    allPosts = Post.objects.all()
    context = {
        'allPosts' : allPosts,
    }
    return render(request,'blog/blogHome.html', context)


def blogPost(request,slug):
    post = Post.objects.filter(slug=slug).first()
    post.views = post.views + 1
    post.save()

    comments = BlogComment.objects.filter(post=post, parent=None)
    replies = BlogComment.objects.filter(post=post).exclude(parent=None)  # .exclude means not equal to something
    replyDict = {}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno] = [reply]
        else:
            replyDict[reply.parent.sno].append(reply)

    context = {
        'post' : post,
        'comments':comments,
        'user':request.user,
        'replyDict' : replyDict,
    } 
    return render(request,'blog/blogPost.html',context)

def postComment(request):
    if request.method=="POST":
        comment = request.POST.get("comment")
        user = request.user
        postSno = request.POST.get("postSno")
        post = Post.objects.get(sno=postSno)
        parentSno = request.POST.get("parentSno")

        if parentSno == "":
            comment = BlogComment(comment=comment,user=user,post=post)
            comment.save()
            messages.success(request,"Your comment has been posted successfullly ")
        else:
            parent = BlogComment.objects.get(sno=parentSno)
            comment = BlogComment(comment=comment,user=user,post=post,parent=parent)
            comment.save()
            messages.success(request,"Your reply has been posted successfullly ")
   
    return redirect(f"/blog/{post.slug}")


def blogEdit(request,slug):
    post = Post.objects.filter(slug=slug).first()
    form = PostEditForm(instance=post)

    if request.method == 'POST':
        form = PostEditForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect(f"/blog/{post.slug}")

    context = {
        'form': form
        }
    return render(request,'blog/blogEdit.html',context)


# def editProject(request, pk):
#     project = Project.objects.get(id=pk)
#     form = ProjectForm(instance=project)

#     if request.method == 'POST':
#         form = ProjectForm(request.POST, request.FILES, instance=project)
#         if form.is_valid():
#             form.save()
#             return redirect('home')

#     context = {'form': form}
#     return render(request, 'base/project_form.html', context)

