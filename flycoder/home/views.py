from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Contact,Post,BlogComment
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from home.templatetags import extras
def index(request):
    allposts=Post.objects.all()
    return render(request,'index.html',{"allposts":allposts})

def contact(request):
    
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        content=request.POST['content']
        if(len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<4):
            messages.error(request,"PLease fill the form correctly")
        else:
            messages.success(request,"Your form has been submitted successfully")
            cont=Contact(name=name,email=email,phone=phone,content=content)
            cont.save()
        
        return render(request,'contact.html')
    return render(request,'contact.html')
def blogpost(request,slug):
    post=Post.objects.get(slug=slug)
    post.view=post.view+1
    post.save()
    comment=BlogComment.objects.filter(post=post,parent=None)
    replies=BlogComment.objects.filter(post=post).exclude(parent=None)
    replyDict={}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno]=[reply]
        else:
            replyDict[reply.parent.sno].append(reply)
 
    return render(request,"blogpost.html",{"post":post,"comment":comment,"replyDict":replyDict})
def search(request):
    query=request.GET['search']
    if len(query)>40:
        allposts=Post.objects.none()
    else:
        allpoststitle=Post.objects.filter(title__icontains=query)
        allpostscontent=Post.objects.filter(content__icontains=query)
        allposts=allpoststitle.union(allpostscontent)
    if allposts.count()==0:
        messages.warning(request,"no search result found please refind your search")
    return render(request,"search.html",{"allposts":allposts,"query":query})


def handlesignup(request):
    if request.method=="POST":
        username=request.POST['username']
        email=request.POST['email']
        fname=request.POST['fname']
        lname=request.POST['lname']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']
        if pass1 != pass2:
            messages.warning(request,"Password and Confirm Password Should be Same")
            return redirect('/')
        if username.isalnum()==False or len(username)<4:
            messages.warning(request,"Username should be alpha numeric and greater then 3 charecter")
            return redirect('/')
        if len(fname)<4 or len(lname)<4:
            messages.warning(request,"First and Last name should be more then 3 charecter")
            return redirect('/')
        if pass1 != pass2:
            messages.warning(request,"Password and Confirm Password Should be Same")
            return redirect('/')
        if fname.isalpha()==False or lname.isalpha()==False:
            messages.warning(request,"First and Last name shoul be alphabet")
            return redirect('/')
        if len(email)<9:
            messages.warning(request,"First and Last name shoul be alphabet")
            return redirect('/')
        myuser=User.objects.create_user(username,email,pass1)
        myuser.first_name=fname
        myuser.last_name=lname
        myuser.save()
        messages.success(request,"You Have successfully Signed up")
        
        return redirect('/')
    return redirect('/')
def handlelogin(request):
    if request.method=="POST":
        usern=request.POST['username']
        pass1=request.POST['pass1']

        if usern.isalnum()==False or len(usern)<4:
            messages.warning(request,"Username should be alpha numeric and greater then 3 charecter")
            return redirect('/')
            
        myuser=authenticate(username=usern,password=pass1)
        if myuser is not None:
            login(request,myuser)
            messages.success(request,"You Have successfully Logged In")
            return redirect('/')
        else:
            messages.error(request,"Invalid Credentials Please Try Again")
            return redirect('/')
    return HttpResponse('404 - not found')
def handlelogout(request):
    logout(request);
    messages.success(request,"Successfully Loggedout")
    return redirect('/')

def postcomment(request):
    if  request.method=="POST":
        comment=request.POST.get("comment")
        user=request.user
        postSno=request.POST.get("postsno")
        parentSno=request.POST.get("parentsno")
        post=Post.objects.get(sno=postSno)
        if parentSno=="":
            comment=BlogComment(comment=comment,user=user,post=post)
            comment.save()
            messages.success(request,"Thank you for commenting")
        else:
            parent=BlogComment.objects.get(sno=parentSno)
            comment=BlogComment(comment=comment,user=user,post=post,parent=parent)
            comment.save()
            messages.success(request,"Thank you for reply of comment")
        return redirect("/"+post.slug+"/")