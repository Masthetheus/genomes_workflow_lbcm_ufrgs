#!/usr/bin/env python3
"""
Interactive course builder for LaTeX-based genome annotation course materials.

This script provides a user-friendly menu-driven interface for building
course materials with module selection and configuration options.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path
from typing import List, Dict, Any, Optional

# Add the utils directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'utils'))

from build_course import CourseBuilder


class InteractiveBuilder:
    """
    Interactive course builder with menu-driven interface.
    
    Attributes:
        builder: CourseBuilder instance
        config: Configuration dictionary
    """
    
    def __init__(self, config_file: str = 'config.yaml'):
        """
        Initialize the interactive builder.
        
        Args:
            config_file: Path to the configuration file
        """
        self.builder = CourseBuilder(config_file)
        self.config = self.builder.config
    
    def run(self):
        """Run the interactive builder main loop."""
        print("=" * 60)
        print("📚 LaTeX Course Builder - Interactive Mode")
        print("=" * 60)
        print()
        
        while True:
            self._show_main_menu()
            
            try:
                choice = input("\nEnter your choice (1-7): ").strip()
                
                if choice == '1':
                    self._list_modules()
                elif choice == '2':
                    self._show_module_details()
                elif choice == '3':
                    self._build_single_module()
                elif choice == '4':
                    self._build_custom_course()
                elif choice == '5':
                    self._build_complete_course()
                elif choice == '6':
                    self._validate_modules()
                elif choice == '7':
                    print("\n👋 Goodbye!")
                    break
                else:
                    print("\n❌ Invalid choice. Please try again.")
                
                if choice != '7':
                    input("\nPress Enter to continue...")
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                input("\nPress Enter to continue...")
    
    def _show_main_menu(self):
        """Display the main menu."""
        print("\n" + "=" * 60)
        print("🎯 MAIN MENU")
        print("=" * 60)
        print("1. 📋 List all available modules")
        print("2. 🔍 View module details")
        print("3. 🏗️  Build single module")
        print("4. 🎨 Build custom course")
        print("5. 📚 Build complete course")
        print("6. ✅ Validate all modules")
        print("7. 🚪 Exit")
    
    def _list_modules(self):
        """List all available modules."""
        print("\n" + "=" * 60)
        print("📋 AVAILABLE MODULES")
        print("=" * 60)
        
        modules = self.builder.list_modules()
        
        if not modules:
            print("❌ No modules found in the modules directory.")
            return
        
        print(f"\n📊 Found {len(modules)} modules:\n")
        
        for i, module in enumerate(modules, 1):
            print(f"{i:2}. 📄 {module['name']}")
            if module['description']:
                print(f"    📝 {module['description']}")
            if module['estimated_time']:
                print(f"    ⏱️  {module['estimated_time']}")
            
            # Show file counts
            tex_count = len(module['files']['tex'])
            img_count = len(module['files']['images'])
            data_count = len(module['files']['data'])
            
            files_info = []
            if tex_count > 0:
                files_info.append(f"{tex_count} LaTeX")
            if img_count > 0:
                files_info.append(f"{img_count} images")
            if data_count > 0:
                files_info.append(f"{data_count} data files")
            
            if files_info:
                print(f"    📁 Files: {', '.join(files_info)}")
            
            print()
    
    def _show_module_details(self):
        """Show detailed information about a specific module."""
        print("\n" + "=" * 60)
        print("🔍 MODULE DETAILS")
        print("=" * 60)
        
        modules = self.builder.list_modules()
        
        if not modules:
            print("❌ No modules found.")
            return
        
        # Show module list
        print("\nAvailable modules:")
        for i, module in enumerate(modules, 1):
            print(f"{i:2}. {module['name']}")
        
        try:
            choice = input(f"\nEnter module number (1-{len(modules)}): ").strip()
            module_index = int(choice) - 1
            
            if 0 <= module_index < len(modules):
                module = modules[module_index]
                self._display_module_details(module)
            else:
                print("❌ Invalid module number.")
                
        except ValueError:
            print("❌ Please enter a valid number.")
    
    def _display_module_details(self, module: Dict[str, Any]):
        """Display detailed information about a module."""
        print(f"\n📄 MODULE: {module['name']}")
        print("=" * 60)
        
        if module['description']:
            print(f"📝 Description: {module['description']}")
        
        if module['estimated_time']:
            print(f"⏱️  Estimated Time: {module['estimated_time']}")
        
        if module['learning_objectives']:
            print("\n🎯 Learning Objectives:")
            for obj in module['learning_objectives']:
                print(f"   • {obj}")
        
        if module['prerequisites']:
            print("\n📋 Prerequisites:")
            for prereq in module['prerequisites']:
                print(f"   • {prereq}")
        
        if module['resources']:
            print("\n📚 Resources:")
            for resource in module['resources']:
                print(f"   • {resource}")
        
        # File information
        print("\n📁 Files:")
        for file_type, files in module['files'].items():
            if files:
                print(f"   {file_type.title()}: {len(files)} files")
                for file_path in files[:3]:  # Show first 3 files
                    print(f"     - {file_path}")
                if len(files) > 3:
                    print(f"     ... and {len(files) - 3} more")
        
        # Validation status
        validation = self.builder.module_validator.validate_module(module['path'])
        if validation['valid']:
            print("\n✅ Module is valid")
        else:
            print("\n❌ Module validation issues:")
            for error in validation['errors']:
                print(f"   • {error}")
            for warning in validation['warnings']:
                print(f"   ⚠️  {warning}")
    
    def _build_single_module(self):
        """Build a single module."""
        print("\n" + "=" * 60)
        print("🏗️  BUILD SINGLE MODULE")
        print("=" * 60)
        
        modules = self.builder.list_modules()
        
        if not modules:
            print("❌ No modules found.")
            return
        
        # Show module list
        print("\nAvailable modules:")
        for i, module in enumerate(modules, 1):
            print(f"{i:2}. {module['name']}")
        
        try:
            choice = input(f"\nEnter module number (1-{len(modules)}): ").strip()
            module_index = int(choice) - 1
            
            if 0 <= module_index < len(modules):
                module = modules[module_index]
                module_name = module['name']
                
                print(f"\n🔨 Building module: {module_name}")
                print("⏳ This may take a few moments...")
                
                result = self.builder.build_single_module(module_name)
                
                if result['success']:
                    print(f"✅ Successfully built module: {module_name}")
                    print(f"📂 Output: {result['output_path']}")
                    
                    # Ask if user wants to open the PDF
                    if result['output_path'] and self._ask_yes_no("\nOpen PDF file?"):
                        self._open_pdf(result['output_path'])
                else:
                    print(f"❌ Failed to build module: {result['error']}")
            else:
                print("❌ Invalid module number.")
                
        except ValueError:
            print("❌ Please enter a valid number.")
    
    def _build_custom_course(self):
        """Build a custom course with selected modules."""
        print("\n" + "=" * 60)
        print("🎨 BUILD CUSTOM COURSE")
        print("=" * 60)
        
        modules = self.builder.list_modules()
        
        if not modules:
            print("❌ No modules found.")
            return
        
        # Show module list with checkboxes
        print("\nAvailable modules:")
        for i, module in enumerate(modules, 1):
            print(f"{i:2}. {module['name']}")
        
        print("\nEnter module numbers separated by spaces (e.g., 1 3 5)")
        print("or 'all' to include all modules:")
        
        try:
            choice = input("\nYour selection: ").strip()
            
            if choice.lower() == 'all':
                selected_modules = [m['name'] for m in modules]
            else:
                indices = [int(x) - 1 for x in choice.split()]
                selected_modules = []
                
                for idx in indices:
                    if 0 <= idx < len(modules):
                        selected_modules.append(modules[idx]['name'])
                    else:
                        print(f"⚠️  Warning: Invalid module number {idx + 1}")
            
            if not selected_modules:
                print("❌ No valid modules selected.")
                return
            
            print(f"\n📋 Selected modules: {', '.join(selected_modules)}")
            
            if self._ask_yes_no("Proceed with building?"):
                print(f"\n🔨 Building custom course with {len(selected_modules)} modules...")
                print("⏳ This may take a few moments...")
                
                result = self.builder.build_custom_course(selected_modules)
                
                if result['success']:
                    print(f"✅ Successfully built custom course!")
                    print(f"📂 Output: {result['output_path']}")
                    
                    # Ask if user wants to open the PDF
                    if result['output_path'] and self._ask_yes_no("\nOpen PDF file?"):
                        self._open_pdf(result['output_path'])
                else:
                    print(f"❌ Failed to build course: {result['error']}")
                    
        except ValueError:
            print("❌ Please enter valid numbers.")
    
    def _build_complete_course(self):
        """Build the complete course."""
        print("\n" + "=" * 60)
        print("📚 BUILD COMPLETE COURSE")
        print("=" * 60)
        
        modules = self.builder.list_modules()
        
        if not modules:
            print("❌ No modules found.")
            return
        
        print(f"📋 This will build a course with all {len(modules)} modules:")
        for module in modules:
            print(f"   • {module['name']}")
        
        if self._ask_yes_no("\nProceed with building the complete course?"):
            print("\n🔨 Building complete course...")
            print("⏳ This may take a few moments...")
            
            result = self.builder.build_complete_course()
            
            if result['success']:
                print(f"✅ Successfully built complete course!")
                print(f"📂 Output: {result['output_path']}")
                
                # Ask if user wants to open the PDF
                if result['output_path'] and self._ask_yes_no("\nOpen PDF file?"):
                    self._open_pdf(result['output_path'])
            else:
                print(f"❌ Failed to build course: {result['error']}")
    
    def _validate_modules(self):
        """Validate all modules."""
        print("\n" + "=" * 60)
        print("✅ VALIDATE ALL MODULES")
        print("=" * 60)
        
        print("🔍 Validating all modules...")
        
        result = self.builder.validate_all_modules()
        
        if result['valid']:
            print("✅ All modules are valid!")
            print(f"📊 Total modules: {result['info']['total_modules']}")
            print(f"✅ Valid modules: {result['info']['valid_modules']}")
        else:
            print("❌ Some modules have validation issues:")
            print(f"📊 Total modules: {result['info']['total_modules']}")
            print(f"✅ Valid modules: {result['info']['valid_modules']}")
            print(f"❌ Invalid modules: {result['info']['invalid_modules']}")
            
            print("\n🔍 Detailed issues:")
            for module_name, module_result in result['modules'].items():
                if not module_result['valid']:
                    print(f"\n📄 {module_name}:")
                    for error in module_result['errors']:
                        print(f"   ❌ {error}")
                    for warning in module_result['warnings']:
                        print(f"   ⚠️  {warning}")
    
    def _ask_yes_no(self, question: str) -> bool:
        """Ask a yes/no question."""
        while True:
            answer = input(f"{question} [y/N]: ").strip().lower()
            if answer in ['y', 'yes']:
                return True
            elif answer in ['n', 'no', '']:
                return False
            else:
                print("Please enter 'y' or 'n'.")
    
    def _open_pdf(self, pdf_path: str):
        """Open a PDF file using the system's default PDF viewer."""
        try:
            pdf_path = Path(pdf_path)
            if not pdf_path.exists():
                print(f"❌ PDF file not found: {pdf_path}")
                return
            
            system = platform.system()
            
            if system == 'Darwin':  # macOS
                subprocess.run(['open', str(pdf_path)])
            elif system == 'Windows':
                subprocess.run(['start', str(pdf_path)], shell=True)
            else:  # Linux and other Unix-like systems
                subprocess.run(['xdg-open', str(pdf_path)])
            
            print(f"📂 Opening PDF: {pdf_path}")
            
        except Exception as e:
            print(f"❌ Failed to open PDF: {e}")
            print(f"📂 PDF location: {pdf_path}")


def main():
    """Main entry point for the interactive builder."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Interactive LaTeX course builder'
    )
    
    parser.add_argument(
        '--config',
        default='config.yaml',
        help='Configuration file path'
    )
    
    args = parser.parse_args()
    
    try:
        builder = InteractiveBuilder(args.config)
        builder.run()
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()