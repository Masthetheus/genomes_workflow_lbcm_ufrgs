"""
File manager utility for course building.

This module provides functionality for managing files and creating LaTeX documents
from module content.
"""

import os
import shutil
import tempfile
import logging
from pathlib import Path
from typing import Optional, List, Dict, Any, Union


class FileManager:
    """
    A class for managing files and creating LaTeX documents.
    
    Attributes:
        temp_dir: Temporary directory for file operations
        logger: Logger instance for file operations
    """
    
    def __init__(self, temp_dir: Optional[str] = None):
        """
        Initialize the file manager.
        
        Args:
            temp_dir: Temporary directory for operations (creates one if None)
        """
        self.temp_dir = temp_dir or tempfile.mkdtemp()
        self.logger = logging.getLogger(__name__)
        
        # Ensure temp directory exists
        os.makedirs(self.temp_dir, exist_ok=True)
    
    def create_latex_document(self, content: str, filename: str, 
                            document_class: str = 'article',
                            packages: Optional[List[str]] = None) -> str:
        """
        Create a complete LaTeX document from content.
        
        Args:
            content: LaTeX content to include in the document
            filename: Name of the output .tex file
            document_class: LaTeX document class to use
            packages: List of LaTeX packages to include
            
        Returns:
            str: Path to the created .tex file
        """
        if packages is None:
            packages = [
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
        
        # Create LaTeX document structure
        latex_content = f"\\documentclass{{{document_class}}}\n\n"
        
        # Add packages
        for package in packages:
            latex_content += f"\\usepackage{{{package}}}\n"
        
        # Add document content
        latex_content += "\n\\begin{document}\n\n"
        latex_content += content
        latex_content += "\n\n\\end{document}\n"
        
        # Write to file
        output_path = Path(self.temp_dir) / filename
        if not output_path.suffix:
            output_path = output_path.with_suffix('.tex')
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(latex_content)
            
            self.logger.info(f"Created LaTeX document: {output_path}")
            return str(output_path)
        
        except Exception as e:
            self.logger.error(f"Failed to create LaTeX document: {e}")
            raise
    
    def combine_modules(self, module_paths: List[str], output_filename: str = 'combined_course.tex') -> str:
        """
        Combine multiple module LaTeX files into a single document.
        
        Args:
            module_paths: List of paths to module directories or .tex files
            output_filename: Name of the output combined file
            
        Returns:
            str: Path to the combined LaTeX file
        """
        combined_content = ""
        
        for module_path in module_paths:
            module_path = Path(module_path)
            
            if module_path.is_dir():
                # Look for main.tex or module.tex in the directory
                tex_files = list(module_path.glob('*.tex'))
                main_files = [f for f in tex_files if f.name in ['main.tex', 'module.tex']]
                
                if main_files:
                    tex_file = main_files[0]
                elif tex_files:
                    tex_file = tex_files[0]
                else:
                    self.logger.warning(f"No .tex files found in {module_path}")
                    continue
            else:
                tex_file = module_path
            
            if not tex_file.exists():
                self.logger.warning(f"LaTeX file not found: {tex_file}")
                continue
            
            try:
                with open(tex_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Extract content between \begin{document} and \end{document}
                content = self._extract_document_content(content)
                
                # Add module separator
                combined_content += f"\\section{{{module_path.stem.replace('_', ' ').title()}}}\n"
                combined_content += content + "\n\n"
                
            except Exception as e:
                self.logger.error(f"Failed to read {tex_file}: {e}")
                continue
        
        # Create combined document
        return self.create_latex_document(combined_content, output_filename)
    
    def _extract_document_content(self, latex_content: str) -> str:
        """
        Extract content between \\begin{document} and \\end{document}.
        
        Args:
            latex_content: Full LaTeX document content
            
        Returns:
            str: Content between document tags
        """
        begin_marker = "\\begin{document}"
        end_marker = "\\end{document}"
        
        begin_idx = latex_content.find(begin_marker)
        end_idx = latex_content.find(end_marker)
        
        if begin_idx != -1 and end_idx != -1:
            return latex_content[begin_idx + len(begin_marker):end_idx].strip()
        
        # If no document environment found, return as is
        return latex_content
    
    def copy_resources(self, source_dir: str, target_dir: str, 
                      extensions: Optional[List[str]] = None) -> List[str]:
        """
        Copy resource files (images, data files) from source to target directory.
        
        Args:
            source_dir: Source directory containing resources
            target_dir: Target directory for resources
            extensions: List of file extensions to copy (default: common resource types)
            
        Returns:
            List[str]: List of copied file paths
        """
        if extensions is None:
            extensions = ['.png', '.jpg', '.jpeg', '.pdf', '.svg', '.eps', '.gif', '.bmp']
        
        source_path = Path(source_dir)
        target_path = Path(target_dir)
        
        if not source_path.exists():
            self.logger.warning(f"Source directory not found: {source_dir}")
            return []
        
        target_path.mkdir(parents=True, exist_ok=True)
        copied_files = []
        
        for ext in extensions:
            for file_path in source_path.glob(f'**/*{ext}'):
                if file_path.is_file():
                    relative_path = file_path.relative_to(source_path)
                    target_file = target_path / relative_path
                    
                    # Create parent directories if needed
                    target_file.parent.mkdir(parents=True, exist_ok=True)
                    
                    try:
                        shutil.copy2(file_path, target_file)
                        copied_files.append(str(target_file))
                        self.logger.debug(f"Copied {file_path} to {target_file}")
                    except Exception as e:
                        self.logger.error(f"Failed to copy {file_path}: {e}")
        
        return copied_files
    
    def create_module_template(self, module_name: str, module_dir: str) -> str:
        """
        Create a template structure for a new module.
        
        Args:
            module_name: Name of the module
            module_dir: Directory to create the module in
            
        Returns:
            str: Path to the created module directory
        """
        module_path = Path(module_dir) / module_name
        module_path.mkdir(parents=True, exist_ok=True)
        
        # Create main.tex file
        main_tex_content = f"""% Module: {module_name}
% Author: Course Builder
% Date: Generated automatically

\\section{{{module_name.replace('_', ' ').title()}}}

\\subsection{{Introduction}}

% Add your content here

\\subsection{{Practical Exercise}}

% Add practical exercises here

\\subsection{{Solutions}}

% Add solutions here (optional)
"""
        
        main_tex_path = module_path / 'main.tex'
        with open(main_tex_path, 'w', encoding='utf-8') as f:
            f.write(main_tex_content)
        
        # Create images directory
        images_dir = module_path / 'images'
        images_dir.mkdir(exist_ok=True)
        
        # Create data directory
        data_dir = module_path / 'data'
        data_dir.mkdir(exist_ok=True)
        
        # Create module info file
        info_content = f"""# Module: {module_name}

## Description
Brief description of the module content.

## Learning Objectives
- Objective 1
- Objective 2
- Objective 3

## Prerequisites
- Prerequisite 1
- Prerequisite 2

## Estimated Time
X hours

## Resources
- Resource 1
- Resource 2
"""
        
        info_path = module_path / 'README.md'
        with open(info_path, 'w', encoding='utf-8') as f:
            f.write(info_content)
        
        self.logger.info(f"Created module template: {module_path}")
        return str(module_path)
    
    def clean_temp_files(self, directory: str, extensions: Optional[List[str]] = None) -> None:
        """
        Clean temporary files from a directory.
        
        Args:
            directory: Directory to clean
            extensions: List of file extensions to remove
        """
        if extensions is None:
            extensions = ['.aux', '.log', '.out', '.toc', '.bbl', '.blg', '.fls', '.fdb_latexmk']
        
        dir_path = Path(directory)
        if not dir_path.exists():
            return
        
        for ext in extensions:
            for file_path in dir_path.glob(f'**/*{ext}'):
                try:
                    file_path.unlink()
                    self.logger.debug(f"Cleaned up {file_path}")
                except Exception as e:
                    self.logger.warning(f"Failed to clean up {file_path}: {e}")
    
    def __del__(self):
        """Clean up temporary directory on deletion."""
        if hasattr(self, 'temp_dir') and self.temp_dir and os.path.exists(self.temp_dir):
            try:
                shutil.rmtree(self.temp_dir)
            except Exception:
                pass  # Ignore cleanup errors