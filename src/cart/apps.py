from django.apps import AppConfig


class CartConfig(AppConfig):
    verbose_name = "1. Кошики та замовлення"
    default_auto_field = "django.db.models.BigAutoField"
    name = "cart"

    # Import signals module to register signal handlers
    # This ensures the signal receivers are connected when the app is ready
    def ready(self):
        import cart.signal_cart  # NOQA 401
