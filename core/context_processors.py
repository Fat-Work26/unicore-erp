from organization.models import PositionAssignment

def user_roles_context(request):
    """
    مُعالج موحد يمرر جميع مناصب وصلاحيات المستخدم الحالي دفعة واحدة
    """
    if not request.user.is_authenticated:
        return {
        'is_postgrad_vice_dean': False,
        'is_dean': False,
        'is_pedagogy_vice_dean': False,
        'active_roles': set(),
    }

    # إذا كان السوبر أدمن، نعطيه علم شامل
    if request.user.is_superuser:
        return {
            'is_superuser': True,
            'is_postgrad_vice_dean': True,
            'is_dean': True,
            # أي مناصب أخرى...
        }

    # جلب جميع أكواد المناصب النشطة للمستخدم في استعلام واحد (Query)
    active_codes = set(
        PositionAssignment.objects.filter(
            user=request.user,
            is_active=True
        ).values_list('position_type__code', flat=True)
    )

    return {
        'is_postgrad_vice_dean': 'VICE_DEAN_POSTGRAD' in active_codes,
        'is_dean': 'DEAN' in active_codes,
        'is_pedagogy_vice_dean': 'VICE_DEAN_PEDAGOGY' in active_codes,
        'active_roles': active_codes,  # لاستخدامها بشكل مرن
    }