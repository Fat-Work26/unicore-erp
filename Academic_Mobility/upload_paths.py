from core.upload_paths import build_upload_path

# 1. Path function for Administrative File (الملف الإداري)
def mobility_admin_file_path(instance, filename):
    order_id = instance.id if instance.id else 'temp'
    return build_upload_path('academic_mobility', 'orders', order_id, 'administrative', filename)

# 2. Path function for Scientific File (الملف العلمي)
def mobility_scientific_file_path(instance, filename):
    order_id = instance.id if instance.id else 'temp'
    return build_upload_path('academic_mobility', 'orders', order_id, 'scientific', filename)

# 3. Path function for Final Report File (تقرير نهاية التربص)
def mobility_report_file_path(instance, filename):
    order_id = instance.id if instance.id else 'temp'
    return build_upload_path('academic_mobility', 'orders', order_id, 'reports', filename)