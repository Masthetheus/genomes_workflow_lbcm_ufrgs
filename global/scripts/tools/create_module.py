import os
import shutil
import re
from datetime import date

def sanitize_folder_name(title):
    # Convert to lowercase and replace non-alphanumeric chars with underscores
    folder_name = re.sub(r'[^a-zA-Z0-9]', '_', title.lower())
    return folder_name

def create_module(module_title, module_subtitle=None, tags=None):

    # Create base variables for module construction
    folder_name = sanitize_folder_name(module_title)
    base_path = os.getcwd()
    templates_path = os.path.join(base_path, "global/templates")
    modules_dir = os.path.join(base_path, "modules")
    # Ensure the modules main directory exists
    if not os.path.exists(modules_dir):
        os.makedirs(modules_dir)
    # Ensure the module doesn't exists and create the necessary directories
    module_path = os.path.join(modules_dir, folder_name)
    if os.path.exists(module_path):
        print(f"Module '{folder_name}' already exists.")
        return
    os.makedirs(module_path)
    images_path = os.path.join(module_path, "images")
    os.makedirs(images_path)
    
    # Create base documentation for the module
    readme_template_path = os.path.join(templates_path, "README_template.md")
    readme_path = os.path.join(module_path, "README.md")
    if os.path.exists(readme_template_path):
        shutil.copy(readme_template_path, readme_path)
        print(f"README.md file created for '{folder_name}'.")
    else:
        print(f"README template not found at: {readme_template_path}")
    
    # Creates module references file
    references_path = os.path.join(module_path, "references.bib")
    open(references_path, 'w').close()
    print(f"references.bib file created for '{folder_name}'.")
    
    # Create metadata file with module title and folder name
    metadata_template_path = os.path.join(templates_path, "metadata_template.yaml")
    metadata_path = os.path.join(module_path, "metadata.yaml")
    if os.path.exists(metadata_template_path):
        with open(metadata_template_path, "r") as fin:
            metadata_content = fin.read()
        # Replace all placeholders
        metadata_content = metadata_content.replace("{{MODULE_TITLE}}", module_title)
        metadata_content = metadata_content.replace("{{FOLDER_NAME}}", folder_name)
        metadata_content = metadata_content.replace("{{MODULE_SUBTITLE}}", module_subtitle if module_subtitle else "")
        metadata_content = metadata_content.replace("{{DATE}}", date.today().isoformat())
    # Replace tag placeholder then add extra tags if present
        tag_list = tags if tags else []
        metadata_content = metadata_content.replace("{{TAG1}}", tag_list[0] if len(tag_list) > 0 else "")
        # If more than two tags, append them to the YAML
        if len(tag_list) > 1:
            extra_tags_yaml = "\n".join([f"  - \"{tag}\"" for tag in tag_list[1:]])
            metadata_content = metadata_content.rstrip() + "\n" + extra_tags_yaml + "\n"
        with open(metadata_path, "w") as fout:
            fout.write(metadata_content)
        print(f"metadata.yaml file created for '{folder_name}' with title '{module_title}'" + 
              (f" and subtitle '{module_subtitle}'" if module_subtitle else "") + ".")
    else:
        print(f"Metadata template not found at: {metadata_template_path}")

    # Create main.tex and preamble.tex files with templates
    tex_template_path = os.path.join(templates_path, "main_template.tex")
    tex_path = os.path.join(module_path, "main.tex")
    if os.path.exists(tex_template_path):
        with open(tex_template_path, "r") as fin:
            tex_content = fin.read()
        # Replace placeholders in the LaTeX template
        tex_content = tex_content.replace("MODULE_NAME_PLACEHOLDER", module_title)
        if module_subtitle:
            tex_content = tex_content.replace("MODULE_SUBTITLE_PLACEHOLDER", module_subtitle)
        else:
            tex_content = tex_content.replace("MODULE_SUBTITLE_PLACEHOLDER", "")
        with open(tex_path, "w") as fout:
            fout.write(tex_content)
        print(f"main.tex file created for '{folder_name}' with title '{module_title}'" + 
              (f" and subtitle '{module_subtitle}'" if module_subtitle else "") + ".")
    else:
        print(f"main template not found at: {tex_template_path}")

    # Replace placeholders in the preamble template
    preamble_template_path = os.path.join(templates_path, "preamble_template.tex")
    preamble_path = os.path.join(module_path, "preamble.tex")
    if os.path.exists(preamble_template_path):
        with open(preamble_template_path, "r") as fin:
            tex_content = fin.read()
        tex_content = tex_content.replace("MODULE_NAME_PLACEHOLDER", module_title)
        with open(preamble_path, "w") as fout:
            fout.write(tex_content)
        print(f"preamble.tex file created for '{folder_name}' with title '{module_title}'.")
    else:
        print(f"Preamble template not found at: {preamble_template_path}")

    print(f"Module '{folder_name}' created successfully at {module_path}!")

def get_parser():
    import argparse
    parser = argparse.ArgumentParser(description="Create a new module directory with templates.")
    parser.add_argument("module_title", help="Title of the module (for LaTeX).")
    parser.add_argument("--subtitle", "-s", dest="module_subtitle", 
                       help="Subtitle of the module (for LaTeX). Optional.", default=None)
    parser.add_argument("--tags", "-t", nargs="*", dest="tags",
                       help="Tags for the module (multiple allowed).", default=[])
    return parser

def main():
    args = get_parser().parse_args()
    create_module(args.module_title, args.module_subtitle, args.tags)

if __name__ == "__main__":
    main()