import os
import uuid

def build_upload_path(app_name, category, instance_id, subfolder, filename):
    # Extract the file extension (e.g., 'pdf', 'png')
    ext = filename.split('.')[-1]
    
    # Generate a unique 8-character filename to avoid file overwrite collisions
    clean_filename = f"{uuid.uuid4().hex[:8]}.{ext}"
    
    # Construct and return the full relative directory path
    return os.path.join(app_name, category, f"id_{instance_id}", subfolder, clean_filename)