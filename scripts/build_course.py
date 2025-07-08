#!/usr/bin/env python3
"""
Main course builder script for LaTeX-based genome annotation course materials.

This script provides a command-line interface for building single modules,
complete courses, or custom selections of modules.
"""

import os
import sys
import argparse
import logging
import yaml
from pathlib import Path
from typing import List, Dict, Any, Optional

# Add the utils directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'utils'))

from utils.latex_compiler import LaTeXCompiler
from utils.file_manager import FileManager
from utils.module_validator import ModuleValidator
from utils.pdf_merger import PDFMerger


class CourseBuilder:
    """
    Main course builder class for managing LaTeX course compilation.
    
    Attributes:
        config: Configuration dictionary
        logger: Logger instance
        latex_compiler: LaTeX compiler instance
        file_manager: File manager instance
        module_validator: Module validator instance
        pdf_merger: PDF merger instance
    """
    
    def __init__(self, config_file: str = 'config.yaml'):
        """
        Initialize the course builder.
        
        Args:
            config_file: Path to the configuration file
        """
        self.config = self._load_config(config_file)
        self.logger = self._setup_logging()
        
        # Initialize utility classes
        self.latex_compiler = LaTeXCompiler()
        self.file_manager = FileManager()
        self.module_validator = ModuleValidator()
        self.pdf_merger = PDFMerger()
    
    def _load_config(self, config_file: str) -> Dict[str, Any]:
        """
        Load configuration from YAML file.
        
        Args:
            config_file: Path to configuration file
            
        Returns:
            dict: Configuration dictionary
        """
        config_path = Path(config_file)
        
        # Default configuration
        default_config = {
            'course': {
                'title': 'Genome Annotation Course',
                'author': 'LBCM',
                'modules_dir': 'examples/modules',
                'output_dir': 'output',
                'temp_dir': 'temp'
            },
            'latex': {
                'compiler': 'pdflatex',
                'document_class': 'article',
                'packages': [
                    'inputenc{utf8}',
                    'fontenc{T1}',
                    'geometry{margin=1in}',
                    'hyperref',
                    'graphicx',
                    'amsmath',
                    'amsfonts',
                    'listings',
                    'xcolor'
                ]
            },
            'build': {
                'include_solutions': False,
                'create_toc': True,
                'merge_pdfs': False,
                'cleanup_temp': True
            },
            'logging': {
                'level': 'INFO',
                'file': 'course_builder.log'
            }
        }
        
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    loaded_config = yaml.safe_load(f)
                    # Merge with defaults
                    default_config.update(loaded_config)
            except Exception as e:
                print(f"Warning: Failed to load config file {config_file}: {e}")
                print("Using default configuration")
        
        return default_config
    
    def _setup_logging(self) -> logging.Logger:
        """
        Set up logging configuration.
        
        Returns:
            Logger instance
        """
        log_level = getattr(logging, self.config['logging']['level'].upper())
        log_file = self.config['logging']['file']
        
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        return logging.getLogger(__name__)
    
    def build_single_module(self, module_name: str, output_dir: Optional[str] = None) -> Dict[str, Any]:
        """
        Build a single module.
        
        Args:
            module_name: Name of the module to build
            output_dir: Output directory (uses config default if None)
            
        Returns:
            dict: Build result
        """
        self.logger.info(f"Building single module: {module_name}")
        
        modules_dir = Path(self.config['course']['modules_dir'])
        module_path = modules_dir / module_name
        
        if not module_path.exists():
            return {
                'success': False,
                'error': f'Module not found: {module_name}',
                'output_path': None
            }
        
        # Validate module
        validation_result = self.module_validator.validate_module(module_path)
        if not validation_result['valid']:
            return {
                'success': False,
                'error': f'Module validation failed: {validation_result["errors"]}',
                'output_path': None
            }
        
        # Find main LaTeX file
        main_tex_candidates = ['main.tex', 'module.tex', f'{module_name}.tex']
        main_tex_file = None
        
        for candidate in main_tex_candidates:
            candidate_path = module_path / candidate
            if candidate_path.exists():
                main_tex_file = candidate_path
                break
        
        if not main_tex_file:
            return {
                'success': False,
                'error': f'No main LaTeX file found in module {module_name}',
                'output_path': None
            }
        
        # Set output directory
        if output_dir is None:
            output_dir = self.config['course']['output_dir']
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Copy resources
        self.file_manager.copy_resources(str(module_path), str(output_path))
        
        # Compile LaTeX
        compile_result = self.latex_compiler.compile_tex_file(
            str(main_tex_file),
            str(output_path)
        )
        
        if compile_result['success']:
            self.logger.info(f"Successfully built module: {module_name}")
        else:
            self.logger.error(f"Failed to build module {module_name}: {compile_result['error']}")
        
        return compile_result
    
    def build_complete_course(self, output_dir: Optional[str] = None) -> Dict[str, Any]:
        """
        Build the complete course from all modules.
        
        Args:
            output_dir: Output directory (uses config default if None)
            
        Returns:
            dict: Build result
        """
        self.logger.info("Building complete course")
        
        modules_dir = Path(self.config['course']['modules_dir'])
        
        if not modules_dir.exists():
            return {
                'success': False,
                'error': f'Modules directory not found: {modules_dir}',
                'output_path': None
            }
        
        # Get all modules
        modules = self.module_validator.list_modules(modules_dir)
        
        if not modules:
            return {
                'success': False,
                'error': 'No modules found in modules directory',
                'output_path': None
            }
        
        # Build course with all modules
        module_names = [m['name'] for m in modules]
        return self.build_custom_course(module_names, output_dir)
    
    def build_custom_course(self, module_names: List[str], output_dir: Optional[str] = None) -> Dict[str, Any]:
        """
        Build a custom course with selected modules.
        
        Args:
            module_names: List of module names to include
            output_dir: Output directory (uses config default if None)
            
        Returns:
            dict: Build result
        """
        self.logger.info(f"Building custom course with modules: {module_names}")
        
        modules_dir = Path(self.config['course']['modules_dir'])
        
        if output_dir is None:
            output_dir = self.config['course']['output_dir']
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Validate all modules first
        valid_modules = []
        for module_name in module_names:
            module_path = modules_dir / module_name
            validation_result = self.module_validator.validate_module(module_path)
            
            if validation_result['valid']:
                valid_modules.append(module_path)
            else:
                self.logger.warning(f"Skipping invalid module {module_name}: {validation_result['errors']}")
        
        if not valid_modules:
            return {
                'success': False,
                'error': 'No valid modules to build',
                'output_path': None
            }
        
        # Create combined LaTeX document
        combined_tex = self.file_manager.combine_modules(
            [str(m) for m in valid_modules],
            'combined_course.tex'
        )
        
        # Copy resources from all modules
        for module_path in valid_modules:
            self.file_manager.copy_resources(str(module_path), str(output_path))
        
        # Compile combined document
        compile_result = self.latex_compiler.compile_multiple_passes(
            combined_tex,
            str(output_path),
            passes=2  # Multiple passes for TOC and references
        )
        
        # Clean up temporary files if configured
        if self.config['build']['cleanup_temp']:
            self.file_manager.clean_temp_files(str(output_path))
        
        if compile_result['success']:
            self.logger.info(f"Successfully built custom course with {len(valid_modules)} modules")
        else:
            self.logger.error(f"Failed to build custom course: {compile_result['error']}")
        
        return compile_result
    
    def list_modules(self) -> List[Dict[str, Any]]:
        """
        List all available modules.
        
        Returns:
            List of module information dictionaries
        """
        modules_dir = Path(self.config['course']['modules_dir'])
        
        if not modules_dir.exists():
            self.logger.warning(f"Modules directory not found: {modules_dir}")
            return []
        
        return self.module_validator.list_modules(modules_dir)
    
    def validate_all_modules(self) -> Dict[str, Any]:
        """
        Validate all modules in the course.
        
        Returns:
            dict: Validation results
        """
        modules_dir = Path(self.config['course']['modules_dir'])
        
        if not modules_dir.exists():
            return {
                'valid': False,
                'error': f'Modules directory not found: {modules_dir}',
                'modules': {}
            }
        
        return self.module_validator.validate_course_structure(modules_dir)


def main():
    """Main entry point for the course builder."""
    parser = argparse.ArgumentParser(
        description='Build LaTeX-based genome annotation course materials'
    )
    
    parser.add_argument(
        'action',
        choices=['build', 'list', 'validate', 'single'],
        help='Action to perform'
    )
    
    parser.add_argument(
        '--module',
        help='Module name (for single module builds)'
    )
    
    parser.add_argument(
        '--modules',
        nargs='+',
        help='List of module names (for custom builds)'
    )
    
    parser.add_argument(
        '--output',
        help='Output directory'
    )
    
    parser.add_argument(
        '--config',
        default='config.yaml',
        help='Configuration file path'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    # Initialize course builder
    try:
        builder = CourseBuilder(args.config)
        
        if args.verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        
        # Perform requested action
        if args.action == 'list':
            modules = builder.list_modules()
            if modules:
                print("Available modules:")
                for module in modules:
                    print(f"  - {module['name']}")
                    if module['description']:
                        print(f"    Description: {module['description']}")
                    if module['estimated_time']:
                        print(f"    Time: {module['estimated_time']}")
            else:
                print("No modules found.")
        
        elif args.action == 'validate':
            result = builder.validate_all_modules()
            if result['valid']:
                print("All modules are valid!")
                print(f"Total modules: {result['info']['total_modules']}")
            else:
                print("Validation failed!")
                for module_name, module_result in result['modules'].items():
                    if not module_result['valid']:
                        print(f"  - {module_name}: {module_result['errors']}")
        
        elif args.action == 'single':
            if not args.module:
                print("Error: --module is required for single module builds")
                sys.exit(1)
            
            result = builder.build_single_module(args.module, args.output)
            if result['success']:
                print(f"Successfully built module: {args.module}")
                print(f"Output: {result['output_path']}")
            else:
                print(f"Failed to build module: {result['error']}")
                sys.exit(1)
        
        elif args.action == 'build':
            if args.modules:
                result = builder.build_custom_course(args.modules, args.output)
                print(f"Building custom course with modules: {args.modules}")
            else:
                result = builder.build_complete_course(args.output)
                print("Building complete course")
            
            if result['success']:
                print("Course built successfully!")
                print(f"Output: {result['output_path']}")
            else:
                print(f"Failed to build course: {result['error']}")
                sys.exit(1)
    
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()