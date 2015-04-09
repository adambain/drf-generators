
from django.core.management.base import AppCommand
from drf_generators.generators import *


class Command(AppCommand):
    help = 'Generates DRF API Views and Serializers for a Django app'

    args = "[appname ...]"

    def add_arguments(self, parser):
        parser.add_argument('-f', '--format',
                            dest='format',
                            default='viewset')
        parser.add_argument('--serializers',
                            dest='serializers',
                            action='store_true')
        parser.add_argument('--views',
                            dest='views',
                            action='store_true')
        parser.add_argument('--urls',
                            dest='urls',
                            action='store_true')

    def handle_app_config(self, app_config, **options):
        if app_config.models_module is None:
            raise CommandError('You must provide an app to generate an API')

        if options['format'] == 'viewset':
            generator = ViewSetGenerator(app_config)
        elif options['format'] == 'apiview':
            generator = APIViewGenerator(app_config)
        elif options['format'] == 'function':
            generator = FunctionViewGenerator(app_config)
        else:
            message = '\'%s\' is not a valid format.' % options['format'] 
            message += '(viewset, apiview, function)'
            raise CommandError(message)

        if options['serializers']:
            result = generator.generate_serializers()
        elif options['views']:
            result = generator.generate_views()
        elif options['urls']:
            result = generator.generate_urls()
        else:
            result = generator.generate_serializers() + '\n'
            result += generator.generate_views() + '\n'
            result += generator.generate_urls()

        print(result)
