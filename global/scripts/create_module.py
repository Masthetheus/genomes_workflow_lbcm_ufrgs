import os
import shutil

def create_module(module_name):
    # Paths
    base_path = os.getcwd()
    templates_path = os.path.join(base_path, "templates")
    module_path = os.path.join(base_path, module_name)
    
    # Check if module directory already exists
    if os.path.exists(module_path):
        print(f"Module '{module_name}' already exists.")
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
        print(f"README.md file created for '{module_name}'.")
    else:
        print(f"README template not found at: {readme_template_path}")
    
    # Create references.bib file
    references_path = os.path.join(module_path, "references.bib")
    open(references_path, 'w').close()
    print(f"references.bib file created for '{module_name}'.")
    
    # Create main.tex file based on the template
    tex_template_path = os.path.join(templates_path, "main_template.tex")
    tex_path = os.path.join(module_path, "main.tex")
    if os.path.exists(tex_template_path):
        shutil.copy(tex_template_path, tex_path)
        print(f"main.tex file created for '{module_name}'.")
    else:
        print(f"main template not found at: {tex_template_path}")

    # Create preamble.tex file based on the template
    preamble_template_path = os.path.join(templates_path, "preamble_template.tex")
    preamble_path = os.path.join(module_path, "preamble.tex")
    if os.path.exists(tex_template_path):
        shutil.copy(preamble_template_path, preamble_path)
        print(f"main.tex file created for '{module_name}'.")
    else:
        print(f"main template not found at: {tex_template_path}")

    print(f"Module '{module_name}' created successfully!")

if __name__ == "__main__":
    module_name = input("Enter the module name: ")
    create_module(module_name)