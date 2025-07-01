from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.views import redirect_to_login

def empleado_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path())
        if request.user.is_staff:
            # Si es admin, puede acceder igual (por si aplica este decorador)
            return view_func(request, *args, **kwargs)
        return view_func(request, *args, **kwargs)
    return _wrapped_view
