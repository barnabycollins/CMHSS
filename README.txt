===== INTRODUCTION =====
This project comes in three files:
- utils.py
- main.py
- run.py

Each function is described in-depth with docstring-style comments, which should get picked up
    by most IDEs when calling that function. Therefore, this file only provides a brief
    overview of what each file does, and what should be known on a high level about their
    contents.

Please read it all; there is some important information at the bottom!


===== FILES =====

=== utils.py ===
This file contains a number of functions written to provide functionality that is used in main.py.

These functions include standalone operations like finding data in map features and computing
    distances between co-ordinates.

Of most importance to someone intending to run this code is the parsePBF() function, which 
    takes a .osm.pbf file from BBBike.org's area extraction tool (https://extract.bbbike.org/)
    and returns the features contained within as a Python dict.

=== main.py ===
This file contains the function analyseCity(), which takes a Python dict representing an
    exported OSM export and outputs statistics on that area to the command line. It also takes
    three optional Boolean parameters, which can be set false to reduce what it analyses.

The contents of main.py rely on the contents of utils.py, so please ensure that they are in the
    same directory when running it!

=== run.py ===
This file imports analyseCity() and parsePBF() from main.py and utils.py respectively, and
    provides a simple framework to call them on city files, either in batch or individually.
    It is what I used to run the code when developing.

It is not required, but it is useful!


===== DATA FILES =====
The data employed during the development of this project can be downloaded from OneDrive at:
    https://durhamuniversity-my.sharepoint.com/:f:/g/personal/zrlr73_durham_ac_uk/EsIIX6weA9ZMl7dV9ldZOFMBEPHNYIvl9Oh-Bsqsb5NMvg

The folder permissions are currently set such that only Donald Sturgeon can access it. If
    any others need access, please email me and I will be more than happy to add them!


===== MODULES REQUIRED =====
This project has two external dependencies: pydriosm and tqdm. It also requires pandas, but
    this is already a dependency of pydriosm.

The former is used to import PBF map files, and the latter provides pretty progress bars when
    the program is running.

Both can be installed using pip, but pydriosm may throw up issues - in order to resolve it, I
    had to install a Visual C++ compiler and install the GDAL module from a standalone .whl
    file. More information on this is in the pydriosm documentation
    (https://pydriosm.readthedocs.io/en/latest/installation.html).
