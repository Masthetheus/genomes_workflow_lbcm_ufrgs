"""
Module validator utility for course building.

This module provides functionality for validating module structure and content
to ensure they conform to the expected format.
"""

import os
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Union


class ModuleValidator:
    """
    A class for validating course module structure and content.
    
    Attributes:
        logger: Logger instance for validation messages
    """
    
    def __init__(self):
        """Initialize the module validator."""
        self.logger = logging.getLogger(__name__)
    
    def validate_module(self, module_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Validate a single module's structure and content.
        
        Args:
            module_path: Path to the module directory
            
        Returns:
            dict: Validation result with status and detailed information
        """
        module_path = Path(module_path)
        
        validation_result = {
            'valid': True,
            'warnings': [],
            'errors': [],
            'info': {
                'name': module_path.name,
                'path': str(module_path),
                'has_main_tex': False,
                'has_readme': False,
                'has_images': False,
                'has_data': False,
                'tex_files': [],
                'image_files': [],
                'data_files': []
            }
        }
        
        # Check if module directory exists
        if not module_path.exists():
            validation_result['valid'] = False
            validation_result['errors'].append(f"Module directory not found: {module_path}")
            return validation_result
        
        if not module_path.is_dir():
            validation_result['valid'] = False
            validation_result['errors'].append(f"Module path is not a directory: {module_path}")
            return validation_result
        
        # Check for main LaTeX file
        main_tex_candidates = ['main.tex', 'module.tex', f'{module_path.name}.tex']
        main_tex_file = None
        
        for candidate in main_tex_candidates:
            candidate_path = module_path / candidate
            if candidate_path.exists():
                main_tex_file = candidate_path
                validation_result['info']['has_main_tex'] = True
                break
        
        if not main_tex_file:
            validation_result['valid'] = False
            validation_result['errors'].append(
                f"No main LaTeX file found. Expected one of: {main_tex_candidates}"
            )
        
        # Check for README file
        readme_candidates = ['README.md', 'README.txt', 'readme.md', 'readme.txt']
        for candidate in readme_candidates:
            if (module_path / candidate).exists():
                validation_result['info']['has_readme'] = True
                break
        
        if not validation_result['info']['has_readme']:
            validation_result['warnings'].append("No README file found")
        
        # Find all LaTeX files
        tex_files = list(module_path.glob('*.tex'))
        validation_result['info']['tex_files'] = [str(f) for f in tex_files]
        
        # Check for images directory and files
        images_dir = module_path / 'images'
        if images_dir.exists() and images_dir.is_dir():
            validation_result['info']['has_images'] = True
            image_extensions = ['.png', '.jpg', '.jpeg', '.pdf', '.svg', '.eps', '.gif', '.bmp']
            image_files = []
            for ext in image_extensions:
                image_files.extend(images_dir.glob(f'*{ext}'))
            validation_result['info']['image_files'] = [str(f) for f in image_files]
        
        # Check for data directory and files
        data_dir = module_path / 'data'
        if data_dir.exists() and data_dir.is_dir():
            validation_result['info']['has_data'] = True
            data_files = [f for f in data_dir.iterdir() if f.is_file()]
            validation_result['info']['data_files'] = [str(f) for f in data_files]
        
        # Validate LaTeX content if main file exists
        if main_tex_file:
            latex_validation = self._validate_latex_content(main_tex_file)
            validation_result['warnings'].extend(latex_validation['warnings'])
            validation_result['errors'].extend(latex_validation['errors'])
            if latex_validation['errors']:
                validation_result['valid'] = False
        
        return validation_result
    
    def _validate_latex_content(self, tex_file: Path) -> Dict[str, List[str]]:
        """
        Validate LaTeX content for common issues.
        
        Args:
            tex_file: Path to the LaTeX file
            
        Returns:
            dict: Validation results with warnings and errors
        """
        result = {'warnings': [], 'errors': []}
        
        try:
            with open(tex_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for basic LaTeX structure
            if '\\documentclass' in content and ('\\begin{document}' not in content or '\\end{document}' not in content):
                result['errors'].append("Complete LaTeX document structure required")
            
            # Check for common LaTeX issues
            if '\\includegraphics' in content:
                # Check if images directory exists
                images_dir = tex_file.parent / 'images'
                if not images_dir.exists():
                    result['warnings'].append("\\includegraphics used but no images directory found")
            
            # Check for undefined references
            if '\\ref{' in content or '\\cite{' in content:
                if '\\label{' not in content and '\\bibitem{' not in content:
                    result['warnings'].append("References used but no labels or bibliography found")
            
            # Check for proper encoding
            try:
                content.encode('utf-8')
            except UnicodeEncodeError:
                result['errors'].append("File contains non-UTF-8 characters")
            
        except Exception as e:
            result['errors'].append(f"Failed to read LaTeX file: {e}")
        
        return result
    
    def validate_course_structure(self, course_dir: Union[str, Path]) -> Dict[str, Any]:
        """
        Validate the entire course structure.
        
        Args:
            course_dir: Path to the course directory
            
        Returns:
            dict: Validation result for the entire course
        """
        course_dir = Path(course_dir)
        
        validation_result = {
            'valid': True,
            'warnings': [],
            'errors': [],
            'modules': {},
            'info': {
                'course_path': str(course_dir),
                'total_modules': 0,
                'valid_modules': 0,
                'invalid_modules': 0
            }
        }
        
        if not course_dir.exists():
            validation_result['valid'] = False
            validation_result['errors'].append(f"Course directory not found: {course_dir}")
            return validation_result
        
        # Find all potential module directories
        module_dirs = [d for d in course_dir.iterdir() if d.is_dir() and not d.name.startswith('.')]
        
        if not module_dirs:
            validation_result['valid'] = False
            validation_result['errors'].append("No module directories found")
            return validation_result
        
        # Validate each module
        for module_dir in module_dirs:
            module_result = self.validate_module(module_dir)
            validation_result['modules'][module_dir.name] = module_result
            
            validation_result['info']['total_modules'] += 1
            if module_result['valid']:
                validation_result['info']['valid_modules'] += 1
            else:
                validation_result['info']['invalid_modules'] += 1
                validation_result['valid'] = False
        
        return validation_result
    
    def get_module_info(self, module_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Get detailed information about a module.
        
        Args:
            module_path: Path to the module directory
            
        Returns:
            dict: Detailed module information
        """
        module_path = Path(module_path)
        
        info = {
            'name': module_path.name,
            'path': str(module_path),
            'exists': module_path.exists(),
            'description': '',
            'learning_objectives': [],
            'prerequisites': [],
            'estimated_time': '',
            'resources': [],
            'files': {
                'tex': [],
                'images': [],
                'data': [],
                'other': []
            }
        }
        
        if not module_path.exists():
            return info
        
        # Try to read README for module description
        readme_files = ['README.md', 'README.txt', 'readme.md', 'readme.txt']
        for readme_file in readme_files:
            readme_path = module_path / readme_file
            if readme_path.exists():
                try:
                    with open(readme_path, 'r', encoding='utf-8') as f:
                        readme_content = f.read()
                    
                    # Simple parsing of README content
                    info['description'] = self._extract_description(readme_content)
                    info['learning_objectives'] = self._extract_objectives(readme_content)
                    info['prerequisites'] = self._extract_prerequisites(readme_content)
                    info['estimated_time'] = self._extract_time(readme_content)
                    info['resources'] = self._extract_resources(readme_content)
                    
                except Exception as e:
                    self.logger.warning(f"Failed to read README {readme_path}: {e}")
                
                break
        
        # Catalog files
        for file_path in module_path.rglob('*'):
            if file_path.is_file():
                relative_path = file_path.relative_to(module_path)
                ext = file_path.suffix.lower()
                
                if ext == '.tex':
                    info['files']['tex'].append(str(relative_path))
                elif ext in ['.png', '.jpg', '.jpeg', '.pdf', '.svg', '.eps', '.gif', '.bmp']:
                    info['files']['images'].append(str(relative_path))
                elif file_path.parent.name == 'data':
                    info['files']['data'].append(str(relative_path))
                else:
                    info['files']['other'].append(str(relative_path))
        
        return info
    
    def _extract_description(self, content: str) -> str:
        """Extract description from README content."""
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'description' in line.lower() and i + 1 < len(lines):
                return lines[i + 1].strip()
        return ''
    
    def _extract_objectives(self, content: str) -> List[str]:
        """Extract learning objectives from README content."""
        objectives = []
        in_objectives = False
        
        for line in content.split('\n'):
            if 'learning objectives' in line.lower():
                in_objectives = True
                continue
            elif in_objectives:
                if line.strip().startswith('-') or line.strip().startswith('*'):
                    objectives.append(line.strip()[1:].strip())
                elif line.strip().startswith('#') or (line.strip() and not line.startswith(' ')):
                    break
        
        return objectives
    
    def _extract_prerequisites(self, content: str) -> List[str]:
        """Extract prerequisites from README content."""
        prerequisites = []
        in_prerequisites = False
        
        for line in content.split('\n'):
            if 'prerequisites' in line.lower():
                in_prerequisites = True
                continue
            elif in_prerequisites:
                if line.strip().startswith('-') or line.strip().startswith('*'):
                    prerequisites.append(line.strip()[1:].strip())
                elif line.strip().startswith('#') or (line.strip() and not line.startswith(' ')):
                    break
        
        return prerequisites
    
    def _extract_time(self, content: str) -> str:
        """Extract estimated time from README content."""
        for line in content.split('\n'):
            if 'estimated time' in line.lower():
                # Look for time patterns
                import re
                time_pattern = r'(\d+)\s*(hours?|hrs?|minutes?|mins?)'
                match = re.search(time_pattern, line.lower())
                if match:
                    return f"{match.group(1)} {match.group(2)}"
        return ''
    
    def _extract_resources(self, content: str) -> List[str]:
        """Extract resources from README content."""
        resources = []
        in_resources = False
        
        for line in content.split('\n'):
            if 'resources' in line.lower():
                in_resources = True
                continue
            elif in_resources:
                if line.strip().startswith('-') or line.strip().startswith('*'):
                    resources.append(line.strip()[1:].strip())
                elif line.strip().startswith('#') or (line.strip() and not line.startswith(' ')):
                    break
        
        return resources
    
    def list_modules(self, course_dir: Union[str, Path]) -> List[Dict[str, Any]]:
        """
        List all modules in a course directory with basic information.
        
        Args:
            course_dir: Path to the course directory
            
        Returns:
            List[dict]: List of module information dictionaries
        """
        course_dir = Path(course_dir)
        modules = []
        
        if not course_dir.exists():
            return modules
        
        # Find all potential module directories
        module_dirs = [d for d in course_dir.iterdir() if d.is_dir() and not d.name.startswith('.')]
        module_dirs.sort(key=lambda x: x.name)
        
        for module_dir in module_dirs:
            module_info = self.get_module_info(module_dir)
            modules.append(module_info)
        
        return modules