# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.

from .models import Group
from .models import Artist
from .models import Pack
from .models import Piece

class GroupAdmin(admin.ModelAdmin):
	prepopulated_fields = {"slug": ("name",)}

class ArtistAdmin(admin.ModelAdmin):
	prepopulated_fields = {"slug": ("name",)}

class PackAdmin(admin.ModelAdmin):
	prepopulated_fields = {"slug": ("name",)}

class PieceAdmin(admin.ModelAdmin):
	prepopulated_fields = {"slug": ("name",)}


admin.site.register(Group, GroupAdmin)
admin.site.register(Artist, ArtistAdmin)
admin.site.register(Pack, PackAdmin)
admin.site.register(Piece, PieceAdmin)

