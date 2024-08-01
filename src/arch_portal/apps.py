from django.apps import AppConfig


class ArchPortalConfig(AppConfig):
    """
    Django Application Configuration for the Auth Portal.

    This class is a subclass of Django's AppConfig, which is used to configure
    Django applications. It's an essential part of Django's app loading mechanism
    and provides a way to customize the initialization of the auth_portal app.

    Attributes:
        name (str): The full Python path to the application. This tells Django
                    where to find the app's code.

        label (str): A shorter name for the app, used as a unique identifier.
                     It's used in database table names and other places where
                     a brief reference to the app is needed.

        default_auto_field (str): Specifies the type of auto-created primary key
                                  field to use for models in this app that don't
                                  explicitly specify a primary key type.

    The 'ready' method:
        This method is called by Django when the application is fully loaded.
        It's used here to import the models, ensuring they are registered with
        Django's model registry. This is crucial for Django to recognize and
        use the models, especially when they are located in a non-standard
        directory structure.

    Usage:
    To use this configuration, ensure it's referenced in the INSTALLED_APPS
    setting in settings.py:
    INSTALLED_APPS = [
        ...
        'arch_portal.apps.AuthPortalConfig',
        ...
    ]

    This file is a crucial part of integrating a custom-structured Django app
    into the broader Django framework, ensuring proper model registration and
    app initialization.
    """

    name = "arch_portal"
    label = "arch_portal"
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self):
        import arch_portal.domain.models  # noqa: F401 (required to disable because of Flake8)
