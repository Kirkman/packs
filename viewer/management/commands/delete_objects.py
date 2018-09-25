from django.core.management.base import BaseCommand, CommandError
from django.utils.text import slugify
from viewer.models import Group
from viewer.models import Pack
from viewer.models import Piece
from viewer.models import Artist



class Command(BaseCommand):
	help = 'Delete all objects of a given model type. DANGEROUS! Only use if you know what you are doing.'

	def add_arguments(self, parser):
		parser.add_argument('model', nargs='+', type=str)

	def handle(self, *args, **options):
		for model in options['model']:
			model_name = model.lower()
			if model_name in ['pack','group','piece','artist']:
				if query_yes_no(question='Delete all objects of model type "%s"?' % model_name, default='no'):
					if model_name == 'pack':
						try:
							Pack.objects.all().delete()
						except Pack.DoesNotExist:
							raise CommandError('Could not delete objects of model type "%s"' % model_name)
					elif model_name == 'group':
						try:
							Group.objects.all().delete()
						except Pack.DoesNotExist:
							raise CommandError('Could not delete objects of model type "%s"' % model_name)
					elif model_name == 'piece':
						try:
							Piece.objects.all().delete()
						except Pack.DoesNotExist:
							raise CommandError('Could not delete objects of model type "%s"' % model_name)
					elif model_name == 'artist':
						try:
							Artist.objects.all().delete()
						except Pack.DoesNotExist:
							raise CommandError('Could not delete objects of model type "%s"' % model_name)

					print 'SUCCESS: Deleted all objects of model type "%s"' % model_name

				else:
					print 'EXITING: Did not delete any models.'



def query_yes_no(question, default="yes"):
	import sys
	"""Ask a yes/no question via raw_input() and return their answer.

	"question" is a string that is presented to the user.
	"default" is the presumed answer if the user just hits <Enter>.
		It must be "yes" (the default), "no" or None (meaning
		an answer is required of the user).

	The "answer" return value is True for "yes" or False for "no".
	"""
	valid = {
		'yes': True,
		'y': True,
		'ye': True,
		'no': False,
		'n': False
	}
	if default is None:
		prompt = ' [y/n] '
	elif default == 'yes':
		prompt = ' [Y/n] '
	elif default == 'no':
		prompt = ' [y/N] '
	else:
		raise ValueError('invalid default answer: "%s"' % default)

	while True:
		sys.stdout.write(question + prompt)
		choice = raw_input().lower()
		if default is not None and choice == '':
			return valid[default]
		elif choice in valid:
			return valid[choice]
		else:
			sys.stdout.write('Please respond with "yes" or "no" (or "y" or "n").\n')


