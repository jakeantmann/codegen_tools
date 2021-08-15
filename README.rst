=============
Codegen tools
=============


.. image:: https://img.shields.io/pypi/v/codegen_tools.svg
        :target: https://pypi.python.org/pypi/codegen_tools

.. image:: https://img.shields.io/travis/jakeantmann/codegen_tools.svg
        :target: https://travis-ci.com/jakeantmann/codegen_tools

.. image:: https://readthedocs.org/projects/codegen-tools/badge/?version=latest
        :target: https://codegen-tools.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status




Tools for OpenAPI3 codegen-based development, using python.


* Free software: BSD license
* Documentation: https://codegen-tools.readthedocs.io.

Overview
--------

Developing APIs with OpenAPI codegen is preferable to directly using the swagger OAS for several reasons:

* Much easier and more pleasant to design an API
* Clean, standardised code structure
* Allows for centralised definitions of shared components
* Instantly ready for Docker

However, I've found that whenever I needed to regenerate an API, I ran into many small issues:

* There's no feature for retaining functions from previously generated versions of an API
* Simply copying all the handlers across means that if a handler function has had updated inputs/outputs, we lose that information with a straight copy
* There's no easy, automated versioning
* Regeneration is codebreaking, meaning regularly updating the OpenAPI3 yaml isn't feasible when working with teams
* When working with multiple APIs that use the same models (eg services behind a gateway), updating the models in all the relevant APIs is tricky

This package is intended to resolve the above issues, make developing python apps with OpenAPI3 codegen a smoother experience. The central idea is to use git to track the core components that you actually have control over (yamls, handlers, helpers, requirements.txt, Dockerfile etc), instead of the APIs themselves. The workflow will look something like the following:

**Initialise your API(s)**

* Write a core yaml file (eg with the help of VScode's OpenAPI extension)
* Write API yaml(s) that reference the models defined in the core yaml file
* Note key information in info.yaml:

  - Preamble information (eg starting version, author etc that go in each API yaml)
  - Which APIs will each API call
  - Which files you want to keep (requirements.txt, Dockerfile etc) for each API in a yaml file
	
* Generate the APIs (clients and servers), and update using info.yaml

**Develop your APIs**

* Update handlers, add helpers, and alter files like requirements.txt etc
  
  - Use the built-in helpers for inter-container communication
	
* When you're happy with you APIs, the package lets you save just the key files to git. You can control how the versioning is updated, and can use tox, travis.ci etc for testing.

**Update your API(s)**

* Update the core, API or info yamls
* Regenerate the API(s)
* Back to developing

**Use the APIs**

Because the development servers (that contain the APIs) are generated using OpenAPI3, they have many features that make them easy to quickly put into production:
  
* Built-in .gitignore, requirements.txt Dockerfile, .dockerignore etc.
* Built-in Readme to run each docker container

Current features
----------------

* Build: Build a server and a client for every yaml in a given folder

To do for v1
-----------------

* Save: Store key files from servers:

  - Extract handlers
  - Extract helpers (and if none, make a new module for the with empty __init__.py
  - Extract any other import files/directories (requirements.txt etc)

* Version: Create versioning system for key files, tracked by Git
* Update: Add current functions to current generated servers/clients

  - Update current functions (git merge or manually)
    + Replace a single function in a handler
    + Replace the generated function in a handler if their docstring/name matches the docstring/name in the corresponding version.
  - Combine and simplify imports
    + If a function is no longer being used, remove it from imports
* Combine: How should it all fit together?

  - If no versioning system, extract should create it
  - Extract should replace current functions and commit
  - Build should be followed automatically by update


To do for v2
------------

* Inter-API connections

  - Sharing definitions via a single, central yaml file
  - Sharing wheels/eggs for using OpenAPI3's client SDKs for inter-API communication
  - Helper functions that simplify this communication

Credits
-------

This package is is being written by Jake Antmann.

The skeleton for this package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage