from django.apps import AppConfig


class SalesProductAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sales_product_app'

    def ready(self):
        import sales_product_app.signals