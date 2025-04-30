import os
from folder_structure import FolderStructureGenerator

# List of folders to be ignored in the folder structure generation
folders_to_ignore = [
    "__pycache__",
    ".git",
    ".idea",
    ".venv",
    ".pytest_cache",
    "Postcode_lookup",
    "Shared"
]

# Generate the markdown representation of the folder structure
folder_structure_generator = FolderStructureGenerator(ignored_folders=folders_to_ignore)
folder_structure_md = folder_structure_generator.generate_folder_structure_md(current_directory=os.path.dirname(os.getcwd()))

# Print the markdown representation of the folder structure
print(folder_structure_md)
