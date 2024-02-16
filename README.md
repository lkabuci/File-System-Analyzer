# File-System-Analyzer
command-line tool that analyzes and reports on the file system structure and usage on a Linux system.

## Installation


[//]: # (<h1 align="center">)

[//]: # (  <br>)

[//]: # (  <a href="http://www.amitmerchant.com/electron-markdownify"><img src="https://raw.githubusercontent.com/amitmerchant1990/electron-markdownify/master/app/img/markdownify.png" alt="Markdownify" width="200"></a>)

[//]: # (  <br>)

[//]: # (  Markdownify)

[//]: # (  <br>)

[//]: # (</h1>)

[//]: # (<h4 align="center">A minimal Markdown Editor desktop app built on top of <a href="http://electron.atom.io" target="_blank">Electron</a>.</h4>)

[//]: # (<p align="center">)

[//]: # (  <a href="https://badge.fury.io/js/electron-markdownify">)

[//]: # (    <img src="https://badge.fury.io/js/electron-markdownify.svg")

[//]: # (         alt="Gitter">)

[//]: # (  </a>)

[//]: # (  <a href="https://gitter.im/amitmerchant1990/electron-markdownify"><img src="https://badges.gitter.im/amitmerchant1990/electron-markdownify.svg"></a>)

[//]: # (  <a href="https://saythanks.io/to/bullredeyes@gmail.com">)

[//]: # (      <img src="https://img.shields.io/badge/SayThanks.io-%E2%98%BC-1EAEDB.svg">)

[//]: # (  </a>)

[//]: # (  <a href="https://www.paypal.me/AmitMerchant">)

[//]: # (    <img src="https://img.shields.io/badge/$-donate-ff69b4.svg?maxAge=2592000&amp;style=flat">)

[//]: # (  </a>)

[//]: # (</p>)

<p align="center">
  <a href="#key-features">Key Features</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#download">Download</a> •
  <a href="#credits">Credits</a> •
  <a href="#related">Related</a> •
  <a href="#license">License</a>
</p>

![Demo]()



## Key Features

* List all files inside a given directory
* Classify files into categories (e.g. images, documents, code, etc.)
* Calculate and display the total size for each file type category.
* Generate a report of files with unusual permission settings (e.g., world-writable files).
* Identify and list files above a certain size threshold.
* Delete reported files if the user chooses to do so.
* Log the output of the program to a file.
* The CLI configuration in one file.
* Run the program in a Docker container.

## Installation

To clone and run this application, you'll need the following installed on your computer.

### prerequisites
- [git](https://git-scm.com/downloads)
- [Python](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/)
- [virtualenv](https://virtualenv.pypa.io/en/latest/)
- [Docker](https://www.docker.com/products/docker-desktop)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Makefile](https://www.gnu.org/software/make/)

```bash
# Clone this repository
$ git clone https://github.com/kaboussi/File-System-Analyzer

# Go into the repository
$ cd File-System-Analyzer

# Create and setup virtual environment
$ make venv

# Run the app
$ python3 main.py [PATH] [OPTIONS]
```

## Usage

* To get help
![Help flag](./.github/assets/help.svg)

<details>
<summary>Get reports of files inside a directory</summary>
<br>

![List files](./.github/assets/list_files.svg)
</details>

* Delete reported files

<details>
<summary>Delete reported files</summary>
<br>

![Delete files](.github/assets/delete_files.svg)
</details>

* Log the output of the program to a file
```commandline
 python3 main.py . --size 100000 -l file.log
```

* Run unittests inside a Docker container
```commandline
make test
```
<details>
<summary>Run the program in a Docker container</summary>
<br>

![Docker](./.github/assets/docker.svg)
</details>

* Or just simply use the configuration file
```commandline
python3 main.py . --config config.conf
```


## Credits

This software uses the following open source packages:

- [Python](https://www.python.org/)
- [Pip](https://pypi.org/project/pip/)
- [VirtualEnv](https://virtualenv.pypa.io/en/latest/)
- [Docker](https://www.docker.com/)
- [Rich](https://github.com/Textualize/rich)
- [Pydantic](https://pydantic-docs.helpmanual.io/)
- [Pytest](https://docs.pytest.org/en/)
- [black](https://black.readthedocs.io/en/stable/)
- [isort](https://pycqa.github.io/isort/)
- [flake8](https://flake8.pycqa.org/en/latest/)
- [pre-commit](https://pre-commit.com/)
- [Makefile](https://www.gnu.org/software/make/)
- [Git](https://git-scm.com/)
- [GitHub](https://github.com/)

## License

[MIT](./LICENSE)

---

> GitHub [@kaboussi](https://github.com/kaboussi) &nbsp;&middot;&nbsp;
> Twitter [@kaboussi_](https://twitter.com/kaboussi_)
