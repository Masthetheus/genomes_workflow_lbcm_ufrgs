import os
import yaml
from datetime import date

def import_metadata_template(module_path):
    base_path = os.getcwd()
    template_path = os.path.join(base_path, "global/templates", "metadata_template.yaml")
    metadata_path = os.path.join(module_path, "metadata.yaml")
    if os.path.exists(template_path):
        with open(template_path, "r") as fin:
            content = fin.read()
        # Replace placeholders with minimal info
        folder_name = os.path.basename(module_path)
        content = content.replace("{{MODULE_TITLE}}", folder_name)
        content = content.replace("{{FOLDER_NAME}}", folder_name)
        content = content.replace("{{MODULE_SUBTITLE}}", "")
        content = content.replace("{{AUTHOR}}", "LBCM Team")
        content = content.replace("{{DATE}}", date.today().isoformat())
        content = content.replace("{{REFERENCES}}", "")
        content = content.replace("{{TAG1}}", "")
        content = content.replace("{{TAG2}}", "")
        with open(metadata_path, "w") as fout:
            fout.write(content)
        print(f"metadata.yaml imported from template for '{folder_name}'")
    else:
        print("Metadata template not found.")

def show_available_modules():
    base_path = os.getcwd()
    modules_dir = os.path.join(base_path, "modules")
    if not os.path.exists(modules_dir):
        print("No modules directory found.")
        return []
    modules = [d for d in os.listdir(modules_dir) if os.path.isdir(os.path.join(modules_dir, d))]
    print("Available modules:")
    for i, mod in enumerate(modules, 1):
        print(f"{i}. {mod}")
    return modules

def module_selection():
    modules = show_available_modules()
    if not modules:
        return None
    choice = input("Select a module to refresh metadata (0 to exit): ")
    if choice == '0':
        print("Exiting.")
        return None
    try:
        choice = int(choice)
        if 1 <= choice <= len(modules):
            return modules[choice - 1]
        else:
            print("Invalid choice. Please try again.")
            return module_selection()
    except ValueError:
        print("Invalid input. Please enter a number.")
        return module_selection()
    
def extract_bib_keys(bib_path):
    keys = []
    if os.path.exists(bib_path):
        with open(bib_path, "r") as fin:
            for line in fin:
                if line.strip().startswith("@"):
                    # Example: @book{garrelsIntroductionLinux2008,
                    key = line.split("{", 1)[1].split(",", 1)[0].strip()
                    keys.append(key)
    return keys

def adjust_metadata(module_folder, module_title=None, module_subtitle=None, tags=None, update_references=True):
    base_path = os.getcwd()
    module_path = os.path.join(base_path, "modules", module_folder)
    metadata_path = os.path.join(module_path, "metadata.yaml")
    bib_path = os.path.join(module_path, "references.bib")
    if os.path.exists(metadata_path):
        with open(metadata_path, "r") as fin:
            metadata = yaml.safe_load(fin)
        if module_title:
            metadata['title'] = module_title
        if module_subtitle is not None:
            metadata['subtitle'] = module_subtitle
        if tags is not None and tags:
            existing_tags = metadata.get('tags', [])
            new_tags = [tag for tag in tags if tag and tag not in existing_tags]
            metadata['tags'] = existing_tags + new_tags
        if update_references:
            bib_keys = extract_bib_keys(bib_path)
            metadata['references'] = bib_keys if bib_keys else []
        with open(metadata_path, "w") as fout:
            yaml.dump(metadata, fout, sort_keys=False, allow_unicode=True)
        print(f"metadata.yaml updated for '{module_folder}'")
    else:
        print(f"metadata.yaml not found at: {metadata_path}")

def get_parser():
    import argparse
    parser = argparse.ArgumentParser(description="Refresh metadata for a module.")
    parser.add_argument("--module_title", "-m", help="Title of the module (for LaTeX). Optional.", default=None)
    parser.add_argument("--subtitle", "-s", dest="module_subtitle", 
                       help="Subtitle of the module (for LaTeX). Optional.", default=None)
    parser.add_argument("--tags", "-t", nargs="*", dest="tags",
                       help="Tags for the module (multiple allowed).", default=[])
    return parser

def main():
    parser = get_parser()
    args = parser.parse_args()
    selected_module = module_selection()
    if not selected_module:
        return
    base_path = os.getcwd()
    module_path = os.path.join(base_path, "modules", selected_module)
    metadata_path = os.path.join(module_path, "metadata.yaml")
    # If metadata.yaml does not exist, import template
    if not os.path.exists(metadata_path):
        import_metadata_template(module_path)
    # If no args passed, only refresh references
    if not any([args.module_title, args.module_subtitle, args.tags]):
        adjust_metadata(selected_module, update_references=True)
    else:
        adjust_metadata(selected_module, args.module_title, args.module_subtitle, args.tags, update_references=True)

if __name__ == "__main__":
    main()