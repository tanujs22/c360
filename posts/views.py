# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from comments.models import Comment
from votes.models import Votes
from votes.forms import VoteForm
from comments.forms import CommentForm
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/login/')
def post_create(request):
	form = PostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.author = request.user
		instance.save()
		messages.success(request, "Successfully Created")
		return HttpResponseRedirect(instance.get_absolute_url())
	context = {
		"form" : form
	}
	return render(request, "posts/create.html", context)

def post_detail(request,id=None):
	instance = get_object_or_404(Post, id=id)
	comments = Comment.objects.filter_by_instance(instance)
	votes = Votes.objects
	initial_data = {
		"content_type" : instance.get_content_type,
		"object_id" : instance.id
	}
	comment_form = CommentForm(request.POST or None, initial=initial_data)
	if comment_form.is_valid():
		comment_form.cleaned_data
		c_type = comment_form.cleaned_data.get("content_type")
		content_type = ContentType.objects.get(model=c_type)
		obj_id = comment_form.cleaned_data.get("object_id")
		content_data = comment_form.cleaned_data.get("content")
		parent_obj = None
		try:
			parent_id = int(request.POST.get("parent_id"))
		except:
			parent_id = None

		if parent_id:
			parent_qs = Comment.objects.filter(id = parent_id)
			if parent_qs.exists():
				parent_obj = parent_qs.first()

		new_comment, created = Comment.objects.get_or_create(
									user = request.user,
									content_type = content_type,
									object_id = obj_id,
									content = content_data,
									parent = parent_obj
			)
		return HttpResponseRedirect(new_comment.content_object.get_absolute_url())
	vote_form = VoteForm(request.POST or None)
	upvote = Votes.objects.filter(value=True).count()
	dwvote = Votes.objects.filter(value=False).count()
	if vote_form.is_valid():
		vote(request, id)
	context = {
		"title" : instance.title,
		"obj" : instance,
		"comments" : comments,
		"comment_form" : comment_form,
		"vote_form":vote_form,
		"upvote" : upvote,
		"downvote" : dwvote
	}
	return render(request, "posts/detail.html", context)

def post_list(request):
	object_list = Post.objects.all()
	paginator = Paginator(object_list, 3)
	page = request.GET.get('page')
	try:
		obj = paginator.page(page)
	except PageNotAnInteger:
		obj = paginator.page(1)
	except EmptyPage:
		obj = paginator.page(paginator.num_pages)
	if request.user.is_authenticated or not request.user.is_authenticated:
		context = {
			"object_list" : obj,
			"title" : "User Posts"
		}
	else:
		context = {
		"title" : "Authentication Failed!"
		}

	return render(request, "posts/list.html", context)

@login_required(login_url='/login/')
def post_update(request, id=None):
	instance = get_object_or_404(Post, id=id)
	form = PostForm(request.POST or None, request.FILES or None, instance=instance)
	if form.is_valid():
		form.save()
		messages.success(request, "Item Saved")
		return HttpResponseRedirect(instance.get_absolute_url())
	context = {
		"title" : instance.title,
		"obj" : instance,
		"form" : form
	}
	return render(request, "posts/create.html", context)

@login_required(login_url='/login/')
def post_delete(request, id=None):
	instance = get_object_or_404(Post, id=id)
	instance.delete()
	messages.success(request, "Successfully deleted")
	return redirect("posts:list")

def vote(request,id=id):
	instance = get_object_or_404(Post, id=id)
	user = request.user
	if 'up' in request.POST:
		Votes.objects.create(
			user = user,
			post = instance,
			value = True
			)
	elif 'down' in request.POST:
		Votes.objects.create(
			user = user,
			post = instance,
			value = False
			)
	return redirect("posts:detail", id)