# LaTeX Course Builder

A comprehensive Python-based automation tool for building LaTeX-based course materials from modular genome annotation and assembly content.

## Features

- **Modular Design**: Build individual modules or complete courses
- **Flexible Output**: Support for single modules, complete courses, or custom selections
- **LaTeX Integration**: Seamless LaTeX compilation with comprehensive error handling
- **Interactive Interface**: Both command-line and menu-driven interfaces
- **Configuration-Driven**: YAML-based configuration for easy customization
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Validation**: Comprehensive module structure and content validation
- **PDF Management**: Optional PDF merging and bookmark creation

## Quick Start

### Prerequisites

- Python 3.7 or higher
- LaTeX distribution (TeX Live, MiKTeX, or MacTeX)
- Optional: PDF processing libraries (PyPDF2, ReportLab)

### Installation

1. Clone or download the scripts folder
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure LaTeX is installed and accessible:
   ```bash
   pdflatex --version
   ```

### Basic Usage

#### Command Line Interface

```bash
# List available modules
python build_course.py list

# Build a single module
python build_course.py single --module module_name

# Build complete course
python build_course.py build

# Build custom course with selected modules
python build_course.py build --modules module1 module2 module3

# Validate all modules
python build_course.py validate
```

#### Interactive Interface

```bash
# Launch interactive builder
python interactive_builder.py
```

The interactive builder provides a user-friendly menu system for:
- Browsing and selecting modules
- Viewing detailed module information
- Building courses with real-time feedback
- Opening generated PDFs automatically

## Configuration

The course builder uses `config.yaml` for configuration. Key settings include:

### Course Settings
```yaml
course:
  title: "Your Course Title"
  author: "Your Name"
  modules_dir: "examples/modules"
  output_dir: "output"
```

### LaTeX Settings
```yaml
latex:
  compiler: "pdflatex"
  document_class: "article"
  packages:
    - "inputenc{utf8}"
    - "hyperref"
    - "graphicx"
```

### Build Settings
```yaml
build:
  include_solutions: false
  create_toc: true
  cleanup_temp: true
  latex_passes: 2
```

## Module Structure

Each module should follow this recommended structure:

```
module_name/
├── main.tex          # Main LaTeX content
├── README.md         # Module description and metadata
├── images/           # Image files
│   ├── figure1.png
│   └── diagram.pdf
└── data/             # Data files and examples
    ├── sample.fasta
    └── config.txt
```

### Module LaTeX Template

```latex
% Module: Introduction to Genome Annotation
% Author: Your Name
% Date: 2024

\section{Introduction to Genome Annotation}

\subsection{Overview}
Brief introduction to the topic...

\subsection{Learning Objectives}
By the end of this module, students will be able to:
\begin{itemize}
    \item Objective 1
    \item Objective 2
    \item Objective 3
\end{itemize}

\subsection{Content}
Main content goes here...

\subsection{Practical Exercise}
\begin{verbatim}
# Example command
busco -i genome.fasta -l bacteria_odb10 -o busco_output
\end{verbatim}

\subsection{Solutions}
% Solutions can be conditionally included
```

### Module README Template

```markdown
# Module: Introduction to Genome Annotation

## Description
Brief description of the module content and purpose.

## Learning Objectives
- Understand basic concepts of genome annotation
- Learn to use annotation tools
- Analyze annotation results

## Prerequisites
- Basic knowledge of genomics
- Familiarity with command line

## Estimated Time
2 hours

## Resources
- Link to relevant papers
- Software documentation
- Additional reading materials
```

## Advanced Features

### PDF Merging

When multiple modules are built, the system can merge them into a single PDF:

```python
# Enable PDF merging in config.yaml
build:
  merge_pdfs: true

pdf:
  merger_backend: "pypdf2"
  add_bookmarks: true
```

### Custom LaTeX Templates

Customize the LaTeX document structure:

```yaml
latex:
  document_class: "report"
  packages:
    - "geometry{margin=1.5in}"
    - "fancyhdr"
    - "titlesec"
```

### Validation Rules

Configure module validation:

```yaml
validation:
  required_files:
    - "main.tex"
  recommended_files:
    - "README.md"
    - "images/"
  max_file_size: 10  # MB
```

## Directory Structure

```
scripts/
├── build_course.py           # Main command-line builder
├── interactive_builder.py    # Interactive menu interface
├── config.yaml              # Configuration file
├── requirements.txt          # Python dependencies
├── README.md                # This documentation
├── .gitignore               # Git ignore rules
├── examples/                # Example modules and configurations
│   ├── modules/
│   │   ├── 01_introduction/
│   │   │   ├── main.tex
│   │   │   ├── README.md
│   │   │   └── images/
│   │   └── 02_busco_analysis/
│   │       ├── main.tex
│   │       ├── README.md
│   │       ├── images/
│   │       └── data/
│   └── course_config.yaml
└── utils/                   # Utility modules
    ├── __init__.py
    ├── latex_compiler.py    # LaTeX compilation
    ├── file_manager.py      # File operations
    ├── module_validator.py  # Module validation
    └── pdf_merger.py        # PDF merging
```

## Error Handling

The course builder includes comprehensive error handling:

- **Module Validation**: Checks for required files and structure
- **LaTeX Compilation**: Captures and reports compilation errors
- **File Operations**: Handles missing files and permissions
- **Configuration**: Validates YAML configuration files

## Logging

Detailed logging is available at multiple levels:

```yaml
logging:
  level: "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
  file: "course_builder.log"
  console: true
```

## Troubleshooting

### Common Issues

1. **LaTeX not found**: Ensure LaTeX is installed and in PATH
2. **PDF merge fails**: Install PyPDF2 or ReportLab
3. **Module validation errors**: Check module structure and required files
4. **Permission errors**: Ensure write permissions for output directory

### Debug Mode

Enable verbose logging for troubleshooting:

```bash
python build_course.py --verbose build
```

## Contributing

This course builder is designed to be extensible. Key areas for contribution:

- Additional LaTeX templates
- Enhanced PDF processing
- Module validation rules
- Interactive interface improvements
- Plugin system for custom processors

## License

[Add your license information here]

## Support

For support and questions:
- Check the logs in `course_builder.log`
- Review module validation output
- Ensure all dependencies are installed
- Verify LaTeX installation

---

*Generated by LaTeX Course Builder v1.0*