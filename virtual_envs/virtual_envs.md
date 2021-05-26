# Virtual environments

## Introduction

When coding you'll probably use a lot of packages and while you'll probably use standard library modules like `argparse`, `os`, `sys` you probably need to use external packages.

A few examples of those might be `pandas`, `pyvcf`, `regex`, etc..

And you might know that for example `pandas` has a lot of dependencies:
- Numpy
- pytz
- python-dateutil
- setuptools

Now Python has a module called `pip` for `Python Install Packages`. And it's pretty smart, it's going to install all the dependencies that pandas need when you try to install it by using the command `pip install pandas`.

```bash
$ pip install pandas
Collecting pandas
  Downloading https://files.pythonhosted.org/packages/c3/e2/00cacecafbab071c787019f00ad84ca3185952f6bb9bca9550ed83870d4d/pandas-1.1.5-cp36-cp36m-manylinux1_x86_64.whl (9.5MB)
    100% |████████████████████████████████| 9.5MB 1.4MB/s 
Collecting pytz>=2017.2 (from pandas)
  Downloading https://files.pythonhosted.org/packages/70/94/784178ca5dd892a98f113cdd923372024dc04b8d40abe77ca76b5fb90ca6/pytz-2021.1-py2.py3-none-any.whl (510kB)
    100% |████████████████████████████████| 512kB 5.5MB/s 
Collecting numpy>=1.15.4 (from pandas)
  Downloading https://files.pythonhosted.org/packages/45/b2/6c7545bb7a38754d63048c7696804a0d947328125d81bf12beaa692c3ae3/numpy-1.19.5-cp36-cp36m-manylinux1_x86_64.whl (13.4MB)
    100% |████████████████████████████████| 13.4MB 787kB/s 
Collecting python-dateutil>=2.7.3 (from pandas)
  Using cached https://files.pythonhosted.org/packages/d4/70/d60450c3dd48ef87586924207ae8907090de0b306af2bce5d134d78615cb/python_dateutil-2.8.1-py2.py3-none-any.whl
Collecting six>=1.5 (from python-dateutil>=2.7.3->pandas)
  Using cached https://files.pythonhosted.org/packages/d9/5a/e7c31adbe875f2abbb91bd84cf2dc52d792b5a01506781dbcf25c91daf11/six-1.16.0-py2.py3-none-any.whl
Installing collected packages: pytz, numpy, six, python-dateutil, pandas
Successfully installed numpy-1.19.5 pandas-1.1.5 python-dateutil-2.8.1 pytz-2021.1 six-1.16.0
You are using pip version 18.1, however version 21.1.1 is available.
You should consider upgrading via the 'pip install --upgrade pip' command.
```

You can even specify the version of the package you want to install by doing so:

```bash
$ pip install pandas==0.25.1
Collecting pandas==0.25.1
  Using cached pandas-0.25.1-cp36-cp36m-manylinux1_x86_64.whl (10.5 MB)
Requirement already satisfied: numpy>=1.13.3 in ./code_school/lib/python3.6/site-packages (from pandas==0.25.1) (1.19.5)
Requirement already satisfied: pytz>=2017.2 in ./code_school/lib/python3.6/site-packages (from pandas==0.25.1) (2021.1)
Requirement already satisfied: python-dateutil>=2.6.1 in ./code_school/lib/python3.6/site-packages (from pandas==0.25.1) (2.8.1)
Requirement already satisfied: six>=1.5 in ./code_school/lib/python3.6/site-packages (from python-dateutil>=2.6.1->pandas==0.25.1) (1.16.0)
Installing collected packages: pandas
  Attempting uninstall: pandas
    Found existing installation: pandas 1.1.5
    Uninstalling pandas-1.1.5:
      Successfully uninstalled pandas-1.1.5
Successfully installed pandas-0.25.1
```

However, maybe you want to separate different versions of the same package. Let's say pandas has a big update and you saw in the release notes that a function that you're using is going to change or is being deprecated.

So you need to keep the production side going while maybe doing some testing on the new version, to adjust your script. And that's an instance where virtual environments are useful.

## How to virtual environment

```bash
path="/home/kimy/NHS/repos/code_school/virtual_envs/code_school"
# You can create virtual enviromnents with this command
python -m venv ${path}

# And you can activate that environment by this one
source ${path}/bin/activate

# You can list installed packages
pip freeze

# You can see that the default python of the environment has been bundled up in the environment
which python
/home/kimy/NHS/repos/code_school/virtual_envs/code_school/bin/python

which pip
/home/kimy/NHS/repos/code_school/virtual_envs/code_school/bin/pip
```

As a example, here is what my pip freeze looked like without the environment:

```bash
# Exit the environment
deactivate

pip freeze
aiohttp==3.6.3
alabaster==0.7.12
anyio==2.0.2
argcomplete==1.12.0
argon2-cffi==20.1.0
asgiref @ file:///tmp/build/80754af9/asgiref_1594338739818/work
asttokens==2.0.4
async-generator==1.10
async-timeout==3.0.1
attrs==20.2.0
avro-python3==1.8.2
Babel==2.8.0
backcall==0.2.0
beautifulsoup4==4.4.1
bleach==3.1.5
brotlipy==0.7.0
certifi==2020.6.20
cffi==1.14.0
chardet==3.0.4
colorama==0.4.3
conda==4.8.5
conda-package-handling==1.7.0
contextvars==2.4
cryptography==2.9.2
dataclasses==0.8
dateparser==0.7.6
decorator==4.4.2
defusedxml==0.6.0
dictdiffer==0.8.1
Django @ file:///tmp/build/80754af9/django_1600355803933/work
docopt==0.6.2
docutils==0.16
dxpy==0.298.1
entrypoints==0.3
et-xmlfile==1.0.1
executing==0.5.4
factory-boy==2.9.2
Faker==4.1.1
future==0.16.0
GelReportModels==7.2.10
hgnc-queries==0.1.0
humanize==0.5.1
icecream==2.0.0
idna==2.8
idna-ssl==1.1.0
imagesize==1.2.0
immutables==0.14
importlib-metadata @ file:///tmp/build/80754af9/importlib-metadata_1593446433964/work
ipykernel==5.4.2
ipython==7.16.1
ipython-genutils==0.2.0
jdcal==1.4.1
jedi==0.18.0
jeepney==0.4.3
Jinja2==2.11.2
json5==0.9.5
jsonschema==3.2.0
jupyter-client==6.1.7
jupyter-core==4.7.0
jupyter-server==1.1.3
jupyterlab==3.0.0
jupyterlab-pygments==0.1.2
jupyterlab-server==2.0.0
keyring==21.4.0
Mako==1.1.3
Markdown @ file:///tmp/build/80754af9/markdown_1597433258348/work
MarkupSafe==1.1.1
maya==0.6.1
mistune==0.8.4
mkl-fft==1.1.0
mkl-random==1.1.1
mkl-service==2.3.0
more-itertools==8.4.0
multidict==4.7.6
mysql==0.0.2
mysqlclient==2.0.1
nbclassic==0.2.5
nbclient==0.5.1
nbconvert==6.0.7
nbformat==5.0.8
nest-asyncio==1.4.3
notebook==6.1.6
numpy @ file:///tmp/build/80754af9/numpy_and_numpy_base_1596233737064/work
openpyxl==2.6.3
packaging==20.4
pandas==0.25.1
pandocfilters==1.4.3
parso==0.8.1
pathlib==1.0.1
pdoc3 @ file:///tmp/build/80754af9/pdoc3_1599273136638/work
pendulum==2.1.2
pexpect==4.8.0
pickleshare==0.7.5
pkginfo==1.5.0.1
pluggy==0.13.1
powerline-gitstatus==1.3.1
powerline-status==2.7
pretty-errors==1.2.18
prometheus-client==0.9.0
prompt-toolkit==3.0.8
psutil==5.7.2
psycopg2 @ file:///tmp/build/80754af9/psycopg2_1594305089590/work
ptyprocess==0.7.0
py==1.8.2
pycodestyle==2.6.0
pycosat==0.6.3
pycparser==2.20
Pygments==2.6.1
PyJWT==1.7.1
pyopencga==2.0.0rc4
pyOpenSSL @ file:///tmp/build/80754af9/pyopenssl_1594392929924/work
pyparsing==2.4.7
pyrsistent==0.17.3
pysam==0.16.0.1
PySocks==1.7.1
pytest==5.4.3
python-dateutil==2.8.1
python-magic==0.4.6
pytz==2020.1
pytzdata==2020.1
PyVCF==0.6.8
PyYAML==5.3.1
pyzmq==20.0.0
readme-renderer==26.0
regex==2020.7.14
requests==2.22.0
requests-toolbelt==0.9.1
rfc3986==1.4.0
ruamel-yaml==0.15.87
SecretStorage==3.1.2
Send2Trash==1.5.0
six==1.15.0
slackclient==2.9.2
snaptime==0.2.4
sniffio==1.2.0
snowballstemmer==2.0.0
Sphinx==1.6.2
sphinx-rtd-theme==0.2.4
sphinxcontrib-serializinghtml==1.1.4
sphinxcontrib-websupport==1.2.4
SQLAlchemy==1.2.0b2
sqlparse==0.3.1
terminado==0.9.1
testpath==0.4.4
text-unidecode==1.3
tornado==6.1
tqdm==4.46.0
traitlets==4.3.3
twine==3.2.0
typing-extensions==3.7.4.3
tzlocal==2.1
ujson==1.35
urllib3==1.25.9
wcwidth==0.2.4
webencodings==0.5.1
websocket-client==0.53.0
xattr==0.9.6
xlrd==1.2.0
yarl==1.5.1
zipp==3.1.0
```

The common practice is to have a requirements file in which you specify which packages you want and which version of those packages are needed for this environment (<https://github.com/eastgenomics/panel_ops/blob/main/requirements.txt>).

```txt
Django==3.1.4
dxpy==0.303.1
hgnc-queries==0.1.0
mysqlclient==2.0.1
panelapp==0.7.3
packaging==20.9
PyVCF==0.6.8
regex==2020.7.14
requests==2.22.0
SQLAlchemy==1.3.20
xlrd==1.2.0
```

And here is how you install those packages from the requirements file

```bash
# install packages in the requirements file
pip install -r requirements.txt
```

As you can see, the `pip freeze` output looks like the content of a requirements file and it is. A quick way to make a requirements file is to do `pip freeze > requirements.txt`

Since the python executable is part of the environment, that means that you can transfer that folder to another computer, activate the environment and be ready to go. An example is present in the panel palace manual where you source the environment before running any commands.

You can see the environment as a lower level version of Docker.

## Conda

Conda is a package manager akin to pip. However Conda is not limited to Python. It works with several languages such as C++ or JavaScript.

Here is the complete documentation for managing environments in Conda: <https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html>

The main take aways from the documentation are that:
- you can create an environment from a yaml file: `conda env create -f environment.yml`
- activating a conda environment: `conda activate myenv`
- updating the environment: `conda env update --prefix ./env --file environment.yml  --prune`
- deactivate a conda environment: `conda deactivate`
