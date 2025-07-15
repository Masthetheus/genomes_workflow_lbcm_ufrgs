import os
import shutil

def create_module(folder_name, module_title, module_subtitle=None):
    # Paths
    base_path = os.getcwd()
    templates_path = os.path.join(base_path, "global/templates")
    modules_dir = os.path.join(base_path, "modules")
    if not os.path.exists(modules_dir):
        os.makedirs(modules_dir)
    module_path = os.path.join(modules_dir, folder_name)
    
    # Check if module directory already exists
    if os.path.exists(module_path):
        print(f"Module '{folder_name}' already exists.")
        return
    
    # Create the module directory
    os.makedirs(module_path)
    
    # Create the images folder
    images_path = os.path.join(module_path, "images")
    os.makedirs(images_path)
    
    # Create README file based on the template
    readme_template_path = os.path.join(templates_path, "README_template.md")
    readme_path = os.path.join(module_path, "README.md")
    if os.path.exists(readme_template_path):
        shutil.copy(readme_template_path, readme_path)
        print(f"README.md file created for '{folder_name}'.")
    else:
        print(f"README template not found at: {readme_template_path}")
    
    # Create references.bib file
    references_path = os.path.join(module_path, "references.bib")
    open(references_path, 'w').close()
    print(f"references.bib file created for '{folder_name}'.")
    
    # Create main.tex file based on the template and replace placeholders
    tex_template_path = os.path.join(templates_path, "main_template.tex")
    tex_path = os.path.join(module_path, "main.tex")
    if os.path.exists(tex_template_path):
        with open(tex_template_path, "r") as fin:
            tex_content = fin.read()
        tex_content = tex_content.replace("MODULE_NAME_PLACEHOLDER", module_title)
        
        # Handle optional subtitle
        if module_subtitle:
            tex_content = tex_content.replace("MODULE_SUBTITLE_PLACEHOLDER", module_subtitle)
        else:
            # Remove the subtitle placeholder or replace with empty string
            tex_content = tex_content.replace("MODULE_SUBTITLE_PLACEHOLDER", "")
            
        with open(tex_path, "w") as fout:
            fout.write(tex_content)
        print(f"main.tex file created for '{folder_name}' with title '{module_title}'" + 
              (f" and subtitle '{module_subtitle}'" if module_subtitle else "") + ".")
    else:
        print(f"main template not found at: {tex_template_path}")

    # Create preamble.tex file based on the template
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
    parser.add_argument("folder_name", help="Name of the module folder to create.")
    parser.add_argument("module_title", help="Title of the module (for LaTeX).")
    parser.add_argument("--subtitle", "-s", dest="module_subtitle", 
                       help="Subtitle of the module (for LaTeX). Optional.", default=None)
    return parser

def main():
    args = get_parser().parse_args()
    create_module(args.folder_name, args.module_title, args.module_subtitle)

if __name__ == "__main__":
    main()