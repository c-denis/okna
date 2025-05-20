from django.http import HttpResponseForbidden
from functools import wraps
from django.contrib.auth.decorators import user_passes_test
from .models import User

def role_required(role_name):
    """
    Декоратор для проверки роли пользователя.
    Пример использования: @role_required('manager')
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return HttpResponseForbidden("Требуется авторизация")
            
            if not hasattr(request.user, 'role') or request.user.role.name != role_name:
                return HttpResponseForbidden(f"Требуется роль {role_name}")
                
            return view_func(request, *args, **kwargs)
        return wrapped_view
    return decorator

def log_execution_time(logger):
    """
    Логирует время выполнения функции.
    Пример: @log_execution_time(logger)
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(*args, **kwargs):
            import time
            start_time = time.time()
            
            result = view_func(*args, **kwargs)
            
            duration = time.time() - start_time
            logger.info(f"{view_func.__name__} выполнена за {duration:.2f} сек")
            
            return result
        return wrapped_view
    return decorator

def cache_view(timeout=60):
    """
    Кэширует результат view на указанное время (в секундах).
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            from django.core.cache import cache
            cache_key = f"view_cache:{request.path}:{request.GET.urlencode()}"
            
            result = cache.get(cache_key)
            if result is None:
                result = view_func(request, *args, **kwargs)
                cache.set(cache_key, result, timeout)
            
            return result
        return wrapped_view
    return decorator