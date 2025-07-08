"""
PDF merger utility for course building.

This module provides functionality for merging multiple PDF files into a single
document using various backends.
"""

import os
import logging
from pathlib import Path
from typing import List, Optional, Dict, Any, Union

# Try to import PDF libraries
try:
    import PyPDF2
    HAS_PYPDF2 = True
except ImportError:
    HAS_PYPDF2 = False

try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    HAS_REPORTLAB = True
except ImportError:
    HAS_REPORTLAB = False


class PDFMerger:
    """
    A class for merging PDF files with multiple backend support.
    
    Attributes:
        logger: Logger instance for PDF operations
        backend: PDF processing backend to use
    """
    
    def __init__(self, backend: str = 'auto'):
        """
        Initialize the PDF merger.
        
        Args:
            backend: PDF processing backend ('pypdf2', 'reportlab', 'auto')
        """
        self.logger = logging.getLogger(__name__)
        self.backend = backend
        
        # Determine available backend
        if backend == 'auto':
            if HAS_PYPDF2:
                self.backend = 'pypdf2'
            elif HAS_REPORTLAB:
                self.backend = 'reportlab'
            else:
                self.backend = 'none'
        
        if self.backend == 'pypdf2' and not HAS_PYPDF2:
            self.logger.warning("PyPDF2 not available, falling back to reportlab")
            self.backend = 'reportlab' if HAS_REPORTLAB else 'none'
        
        if self.backend == 'reportlab' and not HAS_REPORTLAB:
            self.logger.warning("ReportLab not available")
            self.backend = 'none'
    
    def is_available(self) -> bool:
        """
        Check if PDF merging functionality is available.
        
        Returns:
            bool: True if PDF merging is available, False otherwise
        """
        return self.backend != 'none'
    
    def merge_pdfs(self, pdf_files: List[Union[str, Path]], output_path: Union[str, Path],
                   bookmarks: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Merge multiple PDF files into a single document.
        
        Args:
            pdf_files: List of paths to PDF files to merge
            output_path: Path for the output merged PDF
            bookmarks: Optional list of bookmark names for each PDF
            
        Returns:
            dict: Merge result with success status and information
        """
        if not self.is_available():
            return {
                'success': False,
                'error': 'No PDF processing library available. Install PyPDF2 or ReportLab.',
                'output_path': None
            }
        
        # Validate input files
        valid_files = []
        for pdf_file in pdf_files:
            pdf_path = Path(pdf_file)
            if pdf_path.exists() and pdf_path.suffix.lower() == '.pdf':
                valid_files.append(pdf_path)
            else:
                self.logger.warning(f"PDF file not found or invalid: {pdf_file}")
        
        if not valid_files:
            return {
                'success': False,
                'error': 'No valid PDF files to merge',
                'output_path': None
            }
        
        # Perform merge based on backend
        if self.backend == 'pypdf2':
            return self._merge_with_pypdf2(valid_files, output_path, bookmarks)
        elif self.backend == 'reportlab':
            return self._merge_with_reportlab(valid_files, output_path, bookmarks)
        else:
            return {
                'success': False,
                'error': 'No supported PDF backend available',
                'output_path': None
            }
    
    def _merge_with_pypdf2(self, pdf_files: List[Path], output_path: Union[str, Path],
                          bookmarks: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Merge PDFs using PyPDF2.
        
        Args:
            pdf_files: List of PDF file paths
            output_path: Output file path
            bookmarks: Optional bookmark names
            
        Returns:
            dict: Merge result
        """
        try:
            merger = PyPDF2.PdfMerger()
            
            for i, pdf_file in enumerate(pdf_files):
                bookmark_name = None
                if bookmarks and i < len(bookmarks):
                    bookmark_name = bookmarks[i]
                elif not bookmarks:
                    bookmark_name = pdf_file.stem
                
                try:
                    merger.append(str(pdf_file), bookmark=bookmark_name)
                    self.logger.info(f"Added {pdf_file} to merge")
                except Exception as e:
                    self.logger.error(f"Failed to add {pdf_file}: {e}")
                    continue
            
            # Write merged PDF
            with open(output_path, 'wb') as output_file:
                merger.write(output_file)
            
            merger.close()
            
            self.logger.info(f"Successfully merged {len(pdf_files)} PDFs to {output_path}")
            return {
                'success': True,
                'output_path': str(output_path),
                'files_merged': len(pdf_files),
                'backend': 'pypdf2'
            }
            
        except Exception as e:
            self.logger.error(f"PDF merge failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'output_path': None
            }
    
    def _merge_with_reportlab(self, pdf_files: List[Path], output_path: Union[str, Path],
                             bookmarks: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Merge PDFs using ReportLab (basic functionality).
        
        Args:
            pdf_files: List of PDF file paths
            output_path: Output file path
            bookmarks: Optional bookmark names
            
        Returns:
            dict: Merge result
        """
        try:
            # ReportLab doesn't have direct PDF merging, so we create a simple cover page
            # and note that full merging requires PyPDF2
            
            c = canvas.Canvas(str(output_path), pagesize=letter)
            
            # Create a cover page
            c.drawString(100, 750, "Course Materials")
            c.drawString(100, 720, "Combined PDF Document")
            c.drawString(100, 680, "Files included:")
            
            y_pos = 650
            for i, pdf_file in enumerate(pdf_files):
                c.drawString(120, y_pos, f"• {pdf_file.name}")
                y_pos -= 20
                if y_pos < 100:
                    c.showPage()
                    y_pos = 750
            
            c.drawString(100, y_pos - 40, "Note: Install PyPDF2 for full PDF merging functionality")
            c.save()
            
            self.logger.warning("ReportLab backend only creates a cover page. Install PyPDF2 for full merging.")
            return {
                'success': True,
                'output_path': str(output_path),
                'files_merged': len(pdf_files),
                'backend': 'reportlab',
                'warning': 'Only cover page created. Install PyPDF2 for full merging.'
            }
            
        except Exception as e:
            self.logger.error(f"PDF creation failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'output_path': None
            }
    
    def add_bookmarks(self, pdf_path: Union[str, Path], bookmarks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Add bookmarks to an existing PDF.
        
        Args:
            pdf_path: Path to the PDF file
            bookmarks: List of bookmark dictionaries with 'title' and 'page' keys
            
        Returns:
            dict: Result of bookmark addition
        """
        if not self.is_available() or self.backend != 'pypdf2':
            return {
                'success': False,
                'error': 'PyPDF2 required for bookmark functionality',
                'output_path': None
            }
        
        try:
            pdf_path = Path(pdf_path)
            
            # Read existing PDF
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                writer = PyPDF2.PdfWriter()
                
                # Copy all pages
                for page in reader.pages:
                    writer.add_page(page)
                
                # Add bookmarks
                for bookmark in bookmarks:
                    title = bookmark.get('title', 'Untitled')
                    page_num = bookmark.get('page', 0)
                    
                    if page_num < len(writer.pages):
                        writer.add_outline_item(title, page_num)
                
                # Write back to file
                with open(pdf_path, 'wb') as output_file:
                    writer.write(output_file)
            
            self.logger.info(f"Added {len(bookmarks)} bookmarks to {pdf_path}")
            return {
                'success': True,
                'output_path': str(pdf_path),
                'bookmarks_added': len(bookmarks)
            }
            
        except Exception as e:
            self.logger.error(f"Failed to add bookmarks: {e}")
            return {
                'success': False,
                'error': str(e),
                'output_path': None
            }
    
    def get_pdf_info(self, pdf_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Get information about a PDF file.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            dict: PDF information
        """
        pdf_path = Path(pdf_path)
        
        info = {
            'exists': pdf_path.exists(),
            'path': str(pdf_path),
            'size': 0,
            'pages': 0,
            'title': '',
            'author': '',
            'subject': '',
            'creator': ''
        }
        
        if not pdf_path.exists():
            return info
        
        try:
            info['size'] = pdf_path.stat().st_size
            
            if self.backend == 'pypdf2':
                with open(pdf_path, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)
                    info['pages'] = len(reader.pages)
                    
                    # Get metadata
                    if reader.metadata:
                        info['title'] = reader.metadata.get('/Title', '')
                        info['author'] = reader.metadata.get('/Author', '')
                        info['subject'] = reader.metadata.get('/Subject', '')
                        info['creator'] = reader.metadata.get('/Creator', '')
            
        except Exception as e:
            self.logger.error(f"Failed to get PDF info: {e}")
            info['error'] = str(e)
        
        return info
    
    def validate_pdfs(self, pdf_files: List[Union[str, Path]]) -> Dict[str, Any]:
        """
        Validate a list of PDF files.
        
        Args:
            pdf_files: List of PDF file paths to validate
            
        Returns:
            dict: Validation results
        """
        results = {
            'valid_files': [],
            'invalid_files': [],
            'total_files': len(pdf_files),
            'total_pages': 0,
            'total_size': 0
        }
        
        for pdf_file in pdf_files:
            pdf_path = Path(pdf_file)
            
            if not pdf_path.exists():
                results['invalid_files'].append({
                    'path': str(pdf_path),
                    'error': 'File not found'
                })
                continue
            
            if pdf_path.suffix.lower() != '.pdf':
                results['invalid_files'].append({
                    'path': str(pdf_path),
                    'error': 'Not a PDF file'
                })
                continue
            
            try:
                info = self.get_pdf_info(pdf_path)
                
                if 'error' in info:
                    results['invalid_files'].append({
                        'path': str(pdf_path),
                        'error': info['error']
                    })
                else:
                    results['valid_files'].append(info)
                    results['total_pages'] += info['pages']
                    results['total_size'] += info['size']
                    
            except Exception as e:
                results['invalid_files'].append({
                    'path': str(pdf_path),
                    'error': str(e)
                })
        
        return results