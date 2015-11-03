__version__ = 0, 0, 1


class MicroDjango(object):
    NAME = '__main__'

    def __init__(self, **settings):
        module = self.get_module(self.NAME)

        self._urlpatterns_module = \
            Module('urlpatterns', module,
                   urlpatterns=[])
        self._urlpatterns_module.install()

        self._app_module = \
            Module(self.NAME, module)
        self._app_module.install()

        self._configure_setting(**settings)
        self.app_config = self._create_app_config(self._app_module)

        self._defaults(module)

    def run(self):
        import sys
        from django.core.management import execute_from_command_line
        execute_from_command_line(sys.argv)

    @property
    def urlpatterns(self):
        return self._urlpatterns_module.urlpatterns

    def relative_path(self, what=None):
        from os.path import join, abspath, dirname
        base = dirname(what or __file__)
        return lambda *parts: abspath(join(base, *parts))

    def get_settings(self, **kwargs):
        settings = dict(
            DEBUG=True,
            ROOT_URLCONF=self._urlpatterns_module.__name__,
            INSTALLED_APPS=(),
            TEMPLATE_DIRS=(
                self.relative_path()(),
            ),
        )
        settings.update(kwargs or {})
        return settings

    def get_module(self, name):
        import sys
        return sys.modules[name]

    def syncdb(self):
        from django.db import connection
        tables = connection.introspection.\
            get_table_list(connection.cursor())

        for model in self.app_config.get_models():
            if model._meta.db_table in tables:
                return
            with connection.schema_editor() as editor:
                editor.create_model(model)

    def _defaults(self, module):
        if not hasattr(module, 'urlpatterns'):
            module.urlpatterns = ()

        if not hasattr(module, 'application'):
            from django.core.wsgi import get_wsgi_application
            module.application = get_wsgi_application()

    def _create_app_config(self, app_module):
        from django.apps import apps, AppConfig
        from django.conf import settings
        app = AppConfig(app_module.__name__, app_module)
        apps.populate(list(settings.INSTALLED_APPS) + [app])
        return app

    def _configure_setting(self, **kwargs):
        from django.conf import settings
        if settings.configured:
            return
        settings.configure(**self.get_settings(**kwargs))


class Module(dict):
    def __init__(self, name, module, seq=None, **kwargs):
        self.__name__ = name
        self.__file__ = module.__file__
        self._module = module
        super(Module, self).__init__(seq=seq, **kwargs)

    def install(self):
        import sys
        sys.modules[self.__name__] = self

    def __getattribute__(self, name):
        try:
            return super(Module, self).__getattribute__(name)
        except AttributeError:
            if name in self:
                return self[name]
            raise

    def __hash__(self):
        return hash(self.__name__)
