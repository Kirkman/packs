# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# from django.http import HttpResponse
# from django.template import loader
from django.shortcuts import get_object_or_404, render

from viewer.models import Artist
from viewer.models import Group
from viewer.models import Pack
from viewer.models import Piece


# Create your views here.

def index(request):
	latest_pack_list = Pack.objects.order_by('-date')[:20]
	context = {
		'latest_pack_list': latest_pack_list,
	}
	# template = loader.get_template('index.html')
	# return HttpResponse(template.render(context, request))
	return render(request, 'index.html', context)

def group(request, pack_slug):
	return HttpResponse("You're looking at pack %s." % pack_slug)

def pack(request, group_slug, pack_slug):
	this_group = Group.objects.get(slug=group_slug)
	this_pack = get_object_or_404(Pack, slug=pack_slug, group=this_group)
	pack_pieces = Piece.objects.filter(pack=this_pack)

	context = {
		'pieces': pack_pieces,
		'pack': this_pack,
		'group': this_group,
	}
	# template = loader.get_template('index.html')
	# return HttpResponse(template.render(context, request))
	return render(request, 'pack.html', context)



	return HttpResponse("You're looking at pack %s." % pack_slug)

def piece(request, pack_slug, piece_slug):
	return HttpResponse("You're looking at the results of piece %s." % piece_slug)

def artist(request, artist_slug):
	return HttpResponse("You're voting on question %s." % artist_slug)
