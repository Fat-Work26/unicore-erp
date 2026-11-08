from functools import wraps
from django.core.exceptions import PermissionDenied
from organization.models import PositionAssignment




def check_is_postgrad_vice_dean(user):
   
    if not user.is_authenticated:
        return False
        
    if user.is_superuser:
        return True
        
    return PositionAssignment.objects.filter(
        user=user,
        is_active=True,
        position_type__code="VICE_DEAN_POSTGRAD"  # البحث بالرمز الثابت أضمن وأسرع
    ).exists()   

def postgrad_vice_dean_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if check_is_postgrad_vice_dean(request.user):
            return view_func(request, *args, **kwargs)
        raise PermissionDenied
    return _wrapped_view    