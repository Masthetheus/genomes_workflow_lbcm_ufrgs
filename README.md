# Genomes Workflow - LBCM - UFRGS

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

A general repository to store mainly .tex files compiling instructions of common bioinformatics tools used in genome assembly and annotation. It aims to help LBCM students to start on the field in a more approachable way but maintaining their autonomy. In this sense, Linux general usage, environment manipulation and doc's referral practice is still present and highly encouraged to be further explored.

## Getting Started

### Prerequisites

- Linux is strongly recommended and used as base to all logic present in the current workflow.
- [Git](https://git-scm.com/)
- [Python 3.8+](https://www.python.org/)
- [pip](https://github.com/pypa/pip)
- [conda](https://docs.conda.io/en/latest/) (recommended)
- [LaTeX](https://www.latex-project.org/get/) (recommended only for direct work on the project)

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
├── README.md
├── global
│   ├── bibliography
│   ├── scripts
│   └── templates
├── modules
│   └── 01_introduction
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
- **setup.py**:
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

#WORK IN DEVELOPMENT

## Contributing

Guidelines for contributing new guides, corrections, or improvements:
- How to submit a pull request
- Code of conduct
- Acknowledgement of contributors

## References & Further Reading

Curated list of useful resources and references for deeper learning.

## Contact

Information for reaching out to repository maintainers or LBCM coordinators.
