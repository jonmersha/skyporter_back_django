# import os
# import uuid

# def unique_file_path(instance, filename, folder="uploads"):
#     """
#     Generate a unique file path for uploaded files.
#     Example: products/uuid4.png
#     """
#     ext = filename.split('.')[-1]
#     # Generate UUID
#     unique_filename = f"{uuid.uuid4().hex}.{ext}"
#     # Return full path with folder
#     return os.path.join(folder, unique_filename)
