from django.core.management.base import BaseCommand, CommandError
from django.utils.text import slugify
from viewer.models import Artist
from viewer.models import Pack
from viewer.models import Piece
import subprocess


from datetime import datetime
import os
from zipfile import ZipFile
import re
from sauce import SAUCE

FNULL = open(os.devnull, 'w')

class Command(BaseCommand):
	help = 'Parse a zipped pack and import it to the database'

	def add_arguments(self, parser):
		parser.add_argument('pack_slug', nargs='+', type=str)

	def handle(self, *args, **options):
		for pack_slug in options['pack_slug']:
			try:
				pack = Pack.objects.get(slug=pack_slug)
			except Pack.DoesNotExist:
				raise CommandError('Pack "%s" does not exist' % pack_slug)

			# Get pack details
			pack_date = pack.date
			pack_group = pack.group.name

			# Construct zip filepath and dirpath
			zip_file = pack.file.url
			zip_dir =  os.path.dirname(zip_file)

			# Unzip the zipped pack file
			zip_ref = ZipFile(zip_file, 'r')

			# Get modification time of file_id.diz, which can serve as a good backup default date
			try:
				# Get zip datetime tuple
				nfo_date_time = zip_ref.getinfo('file_id.diz').date_time
				# Convert to python datetime object
				zip_mod_date = datetime( *nfo_date_time ) 
			except:
				zip_mod_date = None

			# Unzip the zipped pack file
			zip_ref.extractall( zip_dir )
			zip_ref.close()

			# Get a list of the extracted files
			file_list = []

			allowed_piece_extensions = [
				'.txt',
				'.ans',
				'.asc',
				'.bin',
				'.xb',
				'.nfo',
				'.diz',
				'.tnd',
				'.rip',
				'.adf',
				'.avt',
				'.idf',
				'.cg',
				'.jpg',
				'.jpeg',
				'.gif',
				'.png',
				'.bmp',
				'.tiff',
				'.tif',
			]

			allowed_ansilove_extensions = [
				'.txt',
				'.ans',
				'.asc',
				'.bin',
				'.xb',
				'.nfo',
				'.diz',
				'.tnd',
				'.rip',
				'.adf',
				'.avt',
				'.idf',
				'.cg',
			]
			for file in os.listdir( zip_dir ):
				if os.path.isfile( os.path.join(zip_dir, file) ):
					extension = os.path.splitext(file)[1]
					if extension.lower() in allowed_piece_extensions:
						file_list.append( file )
					else:
						print 'EXCLUDING: ' + str(file)



			# Add each piece to the DB
			for file in file_list:
				print '\n\n\n'
				print '================================================================================='

				piece_name = None
				piece_date = None
				piece_artist_name = None
				piece_artist = None
				piece_datatype = None
				piece_filetype = None
				piece_ch_width = None
				piece_ch_height = None
				piece_slug = None
				piece_preview_path = None

				filename_pieces = file.split('-')
				filename_artist = filename_pieces[0].strip()
				filename_name = os.path.splitext( '-'.join(filename_pieces[1:]) )[0]

				# Get SAUCE info, if there is any
				sauce = SAUCE( os.path.join(zip_dir, file) )

				# Check if successfully found SAUCE
				if sauce.record:
					# Extract any metadata
					if sauce.title:
						piece_name = sauce.title
					if sauce.date: 
						piece_date = datetime.strptime(sauce.date, '%Y%m%d')
					if sauce.author: 
						# This isn't an artist name if its the same as the group name
						if sauce.author.lower() not in [pack_group.lower()] and pack_group.lower() not in sauce.author.lower():
							piece_artist_name = sauce.author
					if sauce.datatype:
						piece_datatype = sauce.datatype
					if sauce.filetype:
						piece_filetype = sauce.filetype
					# BINs datatypes store HALF their width in the sauce filetype field, strange as that sounds
					if piece_datatype == 5:
						piece_ch_width = piece_filetype * 2
					# Otherwise, for Character, Bitmap, or Xbin datatypes, height and width are stored in tinfo1 and tinfo2
					elif piece_datatype in [1,2,6]:
						if sauce.tinfo1:
							piece_ch_width = sauce.tinfo1
						if sauce.tinfo2:
							piece_ch_height = sauce.tinfo2

				# Try to fill in missing values with backup data
				if not piece_name:
					if filename_name:
						piece_name = filename_name
					else:
						piece_name = file
				if not piece_artist_name:
					# Also need to filter out .diz and .nfo files, which show up here
					if filename_artist.lower() not in ['67','us', pack_group.lower()]:
						piece_artist_name = filename_artist
				if not piece_date:
					# Use pack date, if one was set
					if pack_date:
						piece_date = pack_date
					# Use file_id.diz mod date, if one was found
					elif zip_mod_date:
						piece_date = zip_mod_date

				print str(file)
				print str(piece_artist_name) + ' | ' + str(filename_artist)
				print str(piece_ch_width) + ' | ' + str(piece_ch_height)


				piece_slug = slugify(piece_name)

				# Create preview directory if it doesn't exist
				if not os.path.exists( os.path.join(zip_dir,'previews') ):
					os.makedirs( os.path.join(zip_dir,'previews') )

				file_ext = os.path.splitext(file)[1]
				file_no_ext = os.path.splitext(file)[0]

				# Use ansilove to create a preview image, but only for textmode files.
				if file_ext.lower() in allowed_ansilove_extensions:
					# If we found a character width in SAUCE, pass it to the renderer. 
					# Right now ansilove only respects this for BINs, but I'm hoping they will soon add column support for ANSI as well.
					if piece_ch_width:
						subprocess.check_output([ 'ansilove', '-c', str(piece_ch_width), '-o', os.path.join(zip_dir,'previews',file_no_ext+'.png'), os.path.join(zip_dir,file) ])
					# Otherwise cross fingers and hope ansilove does it right
					else:
						subprocess.check_output([ 'ansilove', '-o', os.path.join(zip_dir,'previews',file_no_ext+'.png'), os.path.join(zip_dir,file) ])
					
					piece_preview_path = os.path.join(zip_dir,'previews',file_no_ext+'.png').replace('static/','')

				# JPGs, GIFs, TIFs, etc will server as their own previews. Just copy the image file to the preview directory
				else:
					subprocess.check_output([ 'cp', os.path.join(zip_dir,file), os.path.join(zip_dir,'previews',file) ])

					piece_preview_path = os.path.join(zip_dir,'previews',file).replace('static/','')


				# Search for artist. If not found, search for handle. If not found, just leave it blank.

				# TO-DO: 
				#        * Create NEW artist when can't find one in the database

				# Check for delimiters that might indicate multiple artists
				if piece_artist_name and any(x in piece_artist_name for x in [',','/','\\','|'] ):
					# Split the string at any of these delimiters: , / \ |
					piece_artists_names = re.split(r'\s*,\s*|\s*/\s*|\s*\\\s*|\s*\|\s*',piece_artist_name )
					# Remove blanks
					piece_artists_names = filter(None, piece_artists_names)
					print piece_artists_names
				elif piece_artist_name:
					piece_artists_names = [piece_artist_name]
				else:
					piece_artists_names = []


				piece_artists = []
				for p in piece_artists_names:
					try:
						piece_artists.append( Artist.objects.get(name__iexact=p) )
					except:
						try:
							piece_artists.append( Artist.objects.get(handle__iexact=p) )
						except:
							# THIS IS WHERE WE WOULD CODE ADDING ARTISTS, I GUESS?
							pass


				# Search for piece. If it's already in the DB, then just update it. Otherwise, create new piece object.
				try:
					piece = Piece.objects.filter(file_path__iexact=os.path.join(zip_dir, file), pack=pack)
					if len(piece) == 1:
						piece = piece[0]
						piece.name = piece_name
						slug = piece_slug
						file_name = file,
						piece.pack = pack
						piece.date = piece_date
						piece.graphics_format = piece_filetype
						piece.preview = piece_preview_path

						if len(piece_artists) > 0:
							for p in piece_artists:
								piece.artists.add( p )
						piece.save()
						print '---------------------------------------------------------------------------------'
						print 'FOUND ONE INSTANCE OF ' + os.path.join(zip_dir, file) + ' IN DB. UPDATING.'
						print '================================================================================='
					elif len(piece) == 0:
						piece = Piece(
							name = piece_name,
							slug = piece_slug,
							file_path = os.path.join(zip_dir, file),
							file_name = file,
							pack = pack,
							date = piece_date,
							graphics_format = piece_filetype,
							preview = piece_preview_path,
						)
						piece.save()
						# Django wants an id to exist first before adding manytomany fields. 
						# So we save the Piece above to create the id, then add the artists.
						if piece_artist:
							piece.artists.add( piece_artist )
							piece.save()
						print '---------------------------------------------------------------------------------'
						print 'FOUND ZERO INSTANCES OF ' + os.path.join(zip_dir, file) + ' IN DB. ADDING.'
						print '================================================================================='
					else:
						print '---------------------------------------------------------------------------------'
						print 'FOUND MULTIPLE INSTANCES OF ' + os.path.join(zip_dir, file) + ' IN DB.'
						print '================================================================================='
				except Exception as e:
					print '---------------------------------------------------------------------------------'
					print 'Exception: ' + str(e)
					print '================================================================================='


			# pack.opened = False
			# pack.save()

			# self.stdout.write(self.style.SUCCESS('Successfully imported pack "%s"' % pack_slug))







