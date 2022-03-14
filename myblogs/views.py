
from  .models import BlogPost
from django.shortcuts import render, redirect, HttpResponse, Http404
from myblogs.forms import CreateGroupForm, PostComment, CreateClassForm, CreateTimeChoice, \
    CreateQuestion, TopicForm, EditsForm
from django.contrib.auth.decorators import login_required
from .models import Profile, Group, Comment, Classes, TimeChoice, Questions, Topic, Edits

@login_required
def index(request):
    return render(request, 'myblogs/index.html')


@login_required
def home(request):
    context = {'form': CreateGroupForm(),
               'groups': Group.objects.all()}
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            group.refresh_from_db()
            group.name = form.cleaned_data.get('name')
            group.description = form.cleaned_data.get('description')
            group.attendees.add(Profile.objects.get(user=request.user))
            group.save()
            return render(request, 'myblogs/home.html', context)
        else:
            return HttpResponse("The input is invalid")
    else:
        return render(request, 'myblogs/home.html', context)


@login_required
def GroupView(request, group_id):
    group = Group.objects.get(id=group_id)
    comments = Group.objects.get(id=group_id).comments.order_by('-time')
    classes = group.classes.all()
    questions = group.questions.all()
    context = {'commentform': PostComment(),
               'classform': CreateClassForm(),
               'questionform': CreateQuestion(),
               'group': group,
               'comments': comments,
               'classes': classes,
               'questions': questions,
               'error': ''}
    if request.method == 'POST' and 'btnPostComment' in request.POST:
        form = PostComment(request.POST)
        if form.is_valid():
            text = form.cleaned_data.get('text')
            sender = request.user
            profile = Profile.objects.get(user=sender)
            comment = Comment(text=text, sender=profile)
            comment.save()
            group = Group.objects.get(id=group_id)
            group.comments.add(comment)
            group.save()
            return render(request, 'myblogs/group.html', context)
        else:
            context['error'] = 'Invalid information'
            return render(request, 'myblogs/group.html', context)
    elif request.method == 'POST' and 'btnJoinGroup' in request.POST:
        profile = Profile.objects.get(user=request.user)
        group = Group.objects.get(id=group_id)
        group.attendees.add(profile)
        group.save()
        return render(request, 'myblogs/group.html', context)
    elif request.method == 'POST' and 'btnCreateClass' in request.POST:
        form = CreateClassForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            description = form.cleaned_data.get('description')
            aclass = Classes()
            aclass.name = name
            aclass.description = description
            aclass.save()
            group = Group.objects.get(id=group_id)
            group.classes.add(aclass)
            group.save()
            return render(request, 'myblogs/group.html', context)
    elif request.method == 'POST' and 'btnCreateQuestion' in request.POST:
        form = CreateQuestion(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('question')
            description = form.cleaned_data.get('description')
            question = Questions()
            question.question = name
            question.description = description
            question.sender = Profile.objects.get(user=request.user)
            question.save()
            group = Group.objects.get(id=group_id)
            group.questions.add(question)
            group.save()
            return render(request, 'myblogs/group.html', context)
        else:
            context['error'] = 'Invalid information'
            return render(request, 'myblogs/group.html', context)

    else:
        return render(request, 'myblogs/group.html', context)


@login_required
def ClassView(request, group_id, class_id):
    aclass = Classes.objects.get(id=class_id)
    profile = Profile.objects.get(user=request.user)
    comments = aclass.comments.order_by('-id')
    choices = aclass.times.all()
    context = {'class': aclass,
               'choices': choices,
               'comments': comments,
               'time_choice_form': CreateTimeChoice(),
               'form': PostComment(),
               'profile': profile,
               'error': ''}

    if request.method == 'POST':
        if 'btnJoinClass' in request.POST:
            aclass.attendees.add(profile)
            aclass.save()
            return render(request, 'myblogs/class.html', context)
        elif 'btnVote' in request.POST:
            timechoice = TimeChoice.objects.get(id=int(request.POST.get('btnVote')))
            timechoice.votes += 1
            timechoice.save()
            return render(request, 'myblogs/class.html', context)
        elif 'btnCreateChoice' in request.POST:
            form = CreateTimeChoice(request.POST)
            if form.is_valid():
                start = form.cleaned_data.get('start')
                duration = form.cleaned_data.get('duration')
                choice = TimeChoice()
                choice.start = start
                choice.duration = duration
                choice.votes = 0
                choice.save()
                aclass.times.add(choice)
                aclass.save()
                return render(request, 'myblogs/class.html', context)
            else:
                context['error'] = 'Invalid information'
                return render(request, 'myblogs/class.html', context)
        elif 'btnPostComment' in request.POST:
            form = PostComment(request.POST)
            if form.is_valid():
                text = form.cleaned_data.get('text')
                sender = request.user
                profile = Profile.objects.get(user=sender)
                comment = Comment(text=text, sender=profile)
                comment.save()
                aclass = Classes.objects.get(id=class_id)
                aclass.comments.add(comment)
                aclass.save()
                return render(request, 'myblogs/class.html', context)
            else:
                context['error'] = 'Invalid information'
                return render(request, 'myblogs/class.html', context)

    else:
        return render(request, 'myblogs/class.html', context)


@login_required
def blogposts(request):
    blogposts = BlogPost.objects.order_by('date_added')
    context = {'blogposts': blogposts}
    return render(request, 'myblogs/blogposts.html', context)

@login_required
def blogpost(request, blogpost_id):
    blogpost = BlogPost.objects.get(id=blogpost_id)
    entries = blogpost.entry_set.order_by('-date_added')
    context = {'blogpost':blogpost, 'entries':entries}
    return render(request, 'myblogs/blogpost.html',context)

@login_required
def services(request):
    return render(request, 'privy/services.html')

@login_required
def about(request):
    return render(request, 'privy/about.html')

@login_required
def contact(request):
    return render(request, 'privy/contact.html')

@login_required
def Topics(request):
    """show topics to display"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'myblogs/topics.html', context)

def topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    if topic.owner != request.user:
        raise Http404

    edits = topic.edits_set.order_by('-date_added')
    context = {'topic': topic, 'edits': edits}
    return render(request,'myblogs/topic.html', context)

@login_required
def new_topic(request):
    """Add a new topic"""
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('myblogs:topics')

    context = {'form': form}
    return render(request, 'myblogs/new_topic.html', context)

@login_required
def new_edits(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    """Add a new entry"""
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = EditsForm(data=request.POST)
        if form.is_valid():
            new_edits = form.save(commit=False)
            new_edits.topic = topic
            new_edits.save()
            return redirect('myblogs:topic', topic_id=topic_id)

    context = { 'topic': topic,'form': form}
    return render(request, 'myblogs/new_entry.html', context)

@login_required
def edit_edits(request, edits_id):
    edits = Edits.objects.get(id=edits_id)
    topic = edits.topic
    if topic.owner != request.user:
        raise Http404

    """Add a new entry"""
    if request.method != 'POST':
        form = EditsForm(instance=edits)
    else:
        form = EditsForm(instance=edits, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('myblogs:topic', topic_id=topic.id)

    context = {'edits': edits, 'topic': topic,'form': form}
    return render(request, 'myblogs/edit_entry.html', context)
