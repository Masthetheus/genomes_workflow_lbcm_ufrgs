"""
LaTeX compiler utility for course building.

This module provides functionality for compiling LaTeX documents with proper
error handling and PDF generation.
"""

import os
import subprocess
import logging
import tempfile
from pathlib import Path
from typing import Optional, List, Dict, Any


class LaTeXCompiler:
    """
    A class for compiling LaTeX documents with comprehensive error handling.
    
    Attributes:
        compiler_cmd: The LaTeX compiler command to use (default: pdflatex)
        temp_dir: Temporary directory for compilation
        logger: Logger instance for compilation messages
    """
    
    def __init__(self, compiler_cmd: str = 'pdflatex', temp_dir: Optional[str] = None):
        """
        Initialize the LaTeX compiler.
        
        Args:
            compiler_cmd: The LaTeX compiler command to use
            temp_dir: Temporary directory for compilation (creates one if None)
        """
        self.compiler_cmd = compiler_cmd
        self.temp_dir = temp_dir or tempfile.mkdtemp()
        self.logger = logging.getLogger(__name__)
        
        # Ensure temp directory exists
        os.makedirs(self.temp_dir, exist_ok=True)
    
    def check_latex_installation(self) -> bool:
        """
        Check if LaTeX is properly installed and accessible.
        
        Returns:
            bool: True if LaTeX is available, False otherwise
        """
        try:
            result = subprocess.run(
                [self.compiler_cmd, '--version'],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def compile_tex_file(self, tex_file: str, output_dir: Optional[str] = None) -> Dict[str, Any]:
        """
        Compile a LaTeX file to PDF.
        
        Args:
            tex_file: Path to the .tex file to compile
            output_dir: Directory to save the output PDF (uses temp_dir if None)
            
        Returns:
            dict: Compilation result with success status, output path, and error messages
        """
        tex_path = Path(tex_file)
        if not tex_path.exists():
            return {
                'success': False,
                'error': f'LaTeX file not found: {tex_file}',
                'output_path': None
            }
        
        if not self.check_latex_installation():
            return {
                'success': False,
                'error': f'LaTeX compiler not found: {self.compiler_cmd}',
                'output_path': None
            }
        
        output_directory = output_dir or self.temp_dir
        os.makedirs(output_directory, exist_ok=True)
        
        # Compile command
        cmd = [
            self.compiler_cmd,
            '-interaction=nonstopmode',
            '-output-directory', output_directory,
            str(tex_path)
        ]
        
        try:
            self.logger.info(f"Compiling {tex_file}...")
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300,  # 5 minutes timeout
                cwd=tex_path.parent
            )
            
            pdf_name = tex_path.stem + '.pdf'
            pdf_path = Path(output_directory) / pdf_name
            
            if result.returncode == 0 and pdf_path.exists():
                self.logger.info(f"Successfully compiled {tex_file}")
                return {
                    'success': True,
                    'output_path': str(pdf_path),
                    'log': result.stdout
                }
            else:
                self.logger.error(f"Failed to compile {tex_file}")
                return {
                    'success': False,
                    'error': f'Compilation failed: {result.stderr}',
                    'output_path': None,
                    'log': result.stdout
                }
                
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': 'Compilation timed out after 5 minutes',
                'output_path': None
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Compilation error: {str(e)}',
                'output_path': None
            }
    
    def compile_multiple_passes(self, tex_file: str, output_dir: Optional[str] = None, 
                              passes: int = 2) -> Dict[str, Any]:
        """
        Compile a LaTeX file multiple times (useful for references, citations, etc.).
        
        Args:
            tex_file: Path to the .tex file to compile
            output_dir: Directory to save the output PDF
            passes: Number of compilation passes
            
        Returns:
            dict: Final compilation result
        """
        result = None
        for i in range(passes):
            self.logger.info(f"Compilation pass {i+1}/{passes}")
            result = self.compile_tex_file(tex_file, output_dir)
            if not result['success']:
                break
        
        return result
    
    def get_compilation_log(self, tex_file: str) -> Optional[str]:
        """
        Get the compilation log for a LaTeX file.
        
        Args:
            tex_file: Path to the .tex file
            
        Returns:
            str: Log content if available, None otherwise
        """
        log_path = Path(tex_file).with_suffix('.log')
        
        if log_path.exists():
            try:
                with open(log_path, 'r', encoding='utf-8') as f:
                    return f.read()
            except Exception as e:
                self.logger.error(f"Failed to read log file: {e}")
                return None
        
        return None
    
    def cleanup_temp_files(self, tex_file: str) -> None:
        """
        Clean up temporary files created during compilation.
        
        Args:
            tex_file: Path to the .tex file
        """
        tex_path = Path(tex_file)
        temp_extensions = ['.aux', '.log', '.out', '.toc', '.bbl', '.blg', '.fls', '.fdb_latexmk']
        
        for ext in temp_extensions:
            temp_file = tex_path.with_suffix(ext)
            if temp_file.exists():
                try:
                    temp_file.unlink()
                    self.logger.debug(f"Cleaned up {temp_file}")
                except Exception as e:
                    self.logger.warning(f"Failed to clean up {temp_file}: {e}")
    
    def __del__(self):
        """Clean up temporary directory on deletion."""
        if hasattr(self, 'temp_dir') and self.temp_dir and os.path.exists(self.temp_dir):
            try:
                import shutil
                shutil.rmtree(self.temp_dir)
            except Exception:
                pass  # Ignore cleanup errors