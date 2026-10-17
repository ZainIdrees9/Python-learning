from .models import ActivityLog


# ============================================================
# FR10.3 - GET CLIENT IP
# ============================================================

def get_client_ip(request):

    forwarded_for = request.META.get(
        'HTTP_X_FORWARDED_FOR'
    )

    if forwarded_for:

        return forwarded_for.split(',')[0].strip()

    return request.META.get(
        'REMOTE_ADDR'
    )


# ============================================================
# FR10.3 - CREATE ACTIVITY LOG
# ============================================================

def log_activity(
    request,
    action,
    module='',
    description=''
):

    ActivityLog.objects.create(

        User=(
            request.user
            if request.user.is_authenticated
            else None
        ),

        Action=action,

        Module=module,

        Description=description,

        IPAddress=get_client_ip(request)
    )