# Genomes Workflow - LBCM - UFRGS

![Project Status](https://img.shields.io/badge/status-active-brightgreen)
![Contributions welcome](https://img.shields.io/badge/contributions-welcome-orange)
![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![Platform](https://img.shields.io/badge/platform-linux-lightgrey)

Repository contains mainly MD files aimed to structure a easy to start approach to genome annotation and assembly.

---

## Index

1. [About the Project](#about-the-project)
2. [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Repository Installation](#repository_installation)
3. [Repository Structure](#repository-structure)
4. [Genomic Workflows](#genomic-workflows)
    - [Genome Assembly](#genome-assembly)
    - [Genome Annotation](#genome-annotation)
5. [Bioinformatics Tools](#bioinformatics-tools)
6. [Best Practices](#best-practices)
7. [Contributing](#contributing)
8. [References & Further Reading](#references--further-reading)
9. [Contact](#contact)

---

## About the Project

A general repository to store mainly .tex files compiling instructions of common bioinformatics tools used in genome assembly and annotation. It aims to help LBCM students to start on the field in a more approachable way but maintaining their autonomy. In this sense, Linux general usage, environment manipulation and doc's referral practice is still present and highly encouraged to be further explored. **Currently, development work is focused on the base workflow usage. Theoretical references, although mencioned and valuable, shall be implemented on due time.**

## Getting Started

### Prerequisites

- Linux is strongly recommended and used as base to all logic present in the current workflow.
- [Git](https://git-scm.com/)
- [Python 3.8+](https://www.python.org/)
- [pip](https://github.com/pypa/pip)
- [conda](https://docs.conda.io/en/latest/) (recommended)
- [LaTeX](https://www.latex-project.org/get/) (recommended only for direct work on the project)
- [PyYAML](https://pyyaml.org/) (for metadata management)

**Obs:** Further detailed instructions on prerequisites installation can be found on the given links above, and won't be approached directly during the current project. Although, the basics of them can be found on the Introduction module.

### Repository Installation

- The repository can be cloned as seen below:
```bash
git clone https://github.com/Masthetheus/genomes_workflow_lbcm_ufrgs.git
cd genomes_workflow_lbcm_ufrgs
```
- The needed python packages can then be installed with:
```bash
pip install -r requirements.txt
```
- As an alternative, a conda environment can be set. (#WORK IN DEVELOPMENT)

## Repository Structure

```
genomes_workflow_lbcm_ufrgs/
├── CHANGELOG.md
├── README.md
├── global
│   ├── bibliography
│   ├── scripts
│   └── templates
├── main.log
├── modules
│   ├── 00_introduction
│   └── 01_general_guidelines
├── requirements.txt
├── scripts
│   ├── README.md
│   ├── build_course.py
│   ├── config.yaml
│   ├── interactive_builder.py
│   ├── main.py
│   ├── requirements.txt
│   └── utils
└── setup.py
```
- **modules/**: Folder containing one subfolder per chapter, that includes its README, main and reference files.
- **global/**: Global files directed to modules constructions and maintenence.
- **global/scripts/**: Scripts aimed to help automate the process of module and directory construction.
- **global/templates/**: Base templates for module creation.
- **scripts/**:  Scripts aimed at base user usage, e.g course creation for user visualization.
- **scripts/utils/**: Utilities modules for script correct operation.
- **setup.py**:#WORK IN DEVELOPMENT
- **requirements.txt**: #WORK IN DEVELOPMENT

## Genomic Workflows

### Genome Assembly

- #WORK IN DEVELOPMENT

### Genome Annotation

- #WORK IN DEVELOPMENT

## Bioinformatics Tools

#WORK IN DEVELOPMENT
- [Tool 1](./tools/tool1.md)
- [Tool 2](./tools/tool2.md)
- [Add more as needed...]

## Best Practices

- When opening an issue, provide the most information possible about the bug found or feature implementation suggestion.
- When working actively on the project, pay attention to commit messages and remember to update the documentation as needed.
- Manage the pip packages needed with conda to avoid major versioning problems.

## Contributing

We welcome contributions! Here’s how you can help:

### 1. Reporting Issues

- Found a bug or typo? Please [open an issue](https://github.com/Masthetheus/genomes_workflow_lbcm_ufrgs/issues).
- Suggestions for new modules or improvements are also welcome.

### 2. Submitting Changes

1. **Fork** the repository.
2. **Create a new branch** for your feature or fix:
```bash
    git checkout -b my-feature
```
3. **Make your changes** (add and update documentation, scripts, etc.).
4. **Commit** and **push** to your fork:
```bash
    git add .
    git commit -m "Describe your change"
    git push origin my-feature
```
5. **Open a Pull Request** on GitHub and describe your changes.

### 3. Adding New Documentation or Modules

- Place new workflow modules in the `modules/` directory.
- Add new tool instructions in the `tools/` directory.
- Update the `README.md` index if you add new major sections.
- Remember to update the implemented module's `README.md` file.

### 4. Code of Conduct

- Please be respectful and constructive in all interactions.
- Remember to add the correct references when needed and providing new information.

### 5. Acknowledgement

- All contributors will be listed in the [Acknowledgements](#acknowledgements) section.

---

*Thank you for helping improve this resource!*

## References & Further Reading

#WORK IN DEVELOPMENT

## Contact

#TO BE IMPLEMENTED
