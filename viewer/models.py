# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.exceptions import ObjectDoesNotExist

# This custom storage class allows files to be overwritten, 
# rather than appending a hash to the filename when a file with same name already exists
# https://stackoverflow.com/questions/9522759/imagefield-overwrite-image-file-with-same-name
from viewer.storage import OverwriteStorage

import os


def get_profile_image_path(instance, filename):
	return os.path.join('static', 'images', str(instance.slug), filename)

def get_pack_path(instance, filename):
	print filename
	return os.path.join('static', 'images', str(instance.group.slug), str(instance.slug), filename)

def get_piece_path(instance, filename):
	return os.path.join('static', 'images', str(instance.pack.group.slug), str(instance.pack.slug), filename)

def get_piece_preview_path(instance, filename):
	return os.path.join('images', str(instance.pack.group.slug), 'previews', str(instance.pack.slug), filename)

class Group(models.Model):
	# id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=100)
	slug = models.SlugField(max_length=100)

	website = models.CharField(max_length = 100, blank=True)
	about = models.CharField(max_length = 100, blank=True)
	date_founded = models.DateField(auto_now=False, auto_now_add=False, blank=True)
	header_photo = models.ImageField(upload_to=get_profile_image_path, storage=OverwriteStorage(), blank=True)

	def __str__(self):
		return self.name

class Artist(models.Model):
	# id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=100)
	slug = models.SlugField(max_length=100)
	handle = models.CharField(max_length=100)
	email = models.EmailField(max_length=254, blank=True)

	country = models.CharField(max_length=100, blank=True)
	profile_photo = models.ImageField(upload_to=get_profile_image_path, storage=OverwriteStorage(), blank=True)


	groups = models.ManyToManyField(Group, blank=True) # At parse time, may not be possible to identify the group(s)

	def __str__(self):
		return self.name


class Pack(models.Model):
	# id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=100)
	slug = models.SlugField(max_length=100)
	date = models.DateField(auto_now=False, auto_now_add=False, blank=True)

	group = models.ForeignKey(Group, on_delete=models.CASCADE)

	file = models.FileField(upload_to=get_pack_path, storage=OverwriteStorage() )

	def __str__(self):
		return self.name


class Piece(models.Model):
	# id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=100)
	slug = models.SlugField(max_length=100)
	file = models.FileField(upload_to=get_piece_path, storage=OverwriteStorage() )

	artists = models.ManyToManyField(Artist, blank=True) # At parse time, may not be possible to identify the artist(s)
	# artists = models.ForeignKey(Artist, on_delete=models.CASCADE, null=True)
	pack = models.ForeignKey(Pack, on_delete=models.CASCADE)

	date = models.DateField(auto_now=False, auto_now_add=False)
	graphics_format = models.CharField(max_length=100, blank=True, null=True)

	preview = models.FileField(upload_to=get_piece_preview_path, storage=OverwriteStorage(), blank=True )

	def __str__(self):
		return self.name




