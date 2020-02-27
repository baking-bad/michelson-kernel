# Michelson kernel
[![Docker Build Status](https://img.shields.io/docker/cloud/build/bakingbad/michelson-kernel)](https://hub.docker.com/r/bakingbad/michelson-kernel)
[![made_with pytezos](https://img.shields.io/badge/made_with-pytezos-yellowgreen.svg)](https://github.com/baking-bad/pytezos)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/baking-bad/michelson-kernel/binder?filepath=michelson_quickstart.ipynb)

Jupyter kernel for the Michelson language

## Features
* Custom interpreter with runtime type checker
* Syntax highlighter
* Autocomplete by `Tab`
* Inplace docstrings by `Shift+Tab`
* Macros support
* Verbose execution logging
* Debug helpers

## Purposes
* Learning
* Demonstration
* Fast prototyping
* Case investigation

## How to install

### Option 1: run online!
Powered by awesome Binder: https://mybinder.org/v2/gh/baking-bad/michelson-kernel/binder?filepath=michelson_quickstart.ipynb

### Option 2: run in docker
0. Get the latest image from dockerhub (only when new releases are published)
```
docker pull bakingbad/michelson-kernel
```
1. Create container using verified docker image:
```
docker run --rm -it -p 127.0.0.1:8888:8888 -v $(pwd):/home/jupyter/notebooks bakingbad/michelson-kernel
```
2. Open the link from container output in your browser
3. Save notebooks in the mapped folder in order not to loose them

### Option 3: install python package
1. Install the package using pip
```
pip install michelson-kernel
```
2. Check that Jupyter is now supporting Michelson kernel
```
jupyter kernelspec list
```

### Option 4: install from sources
1. Ensure the following packages are installed: `libssl-dev zlib1g-dev uuid-dev`
2. Get the sources, build and install
```
git clone https://github.com/baking-bad/michelson-kernel
cd michelson-kernel
make
```
3. Check that Jupyter is now supporting Michelson kernel
```
jupyter kernelspec list
```

## How to uninstall
1. Run the following command
```
jupyter kernelspec uninstall michelson -f
```
2. Check that Jupyter is no longer supporting Michelson kernel
```
jupyter kernelspec list
```
3. Uninstall Python package
```
pip uninstall michelson-kernel
```

## How it works

### Basics

#### Cells and the stack state

#### Single instruction

#### `DUMP` and `DROP_ALL` helpers

#### Instruction sequences

#### The `PRINT` helper

#### Disable `DEBUG` mode

#### Runtime errors

### Blockchain-specific instructions

#### The `PATCH` helper

#### Default values

### Contract structure

#### `parameter` / `storage` / `code` sections

#### `INCLUDE` and `RUN` helpers

### Advanced

#### Entrypoints

#### Big Maps