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

### Option 1: try online!
Powered by awesome Binder: https://mybinder.org/v2/gh/baking-bad/michelson-kernel/binder?filepath=michelson_quickstart.ipynb

### Option 2: run in docker
1. Get the latest image from dockerhub (only when new releases are published)
```
docker pull bakingbad/michelson-kernel
```
2. Create container using verified docker image:
```
docker run --rm -it -p 127.0.0.1:8888:8888 -v $(pwd):/home/jupyter/notebooks bakingbad/michelson-kernel
```
3. Open the link from container output in your browser
4. Save notebooks in the mapped folder in order not to loose them

### Option 3: install python package
1. Ensure you have several crypto libraries installed (see [pytezos docs](https://baking-bad.github.io/pytezos/#requirements)):
```
sudo apt install libsodium-dev libsecp256k1-dev libgmp-dev
```
2. Install the package using pip
```
pip install michelson-kernel
```
3. Check that Jupyter is now supporting Michelson kernel
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
Check out this introduction:  
https://nbviewer.jupyter.org/github/baking-bad/michelson-kernel/blob/binder/michelson_quickstart.ipynb  
Or [try it](https://mybinder.org/v2/gh/baking-bad/michelson-kernel/binder?filepath=michelson_quickstart.ipynb) in a Michelson notebook!

## Acknowledgments
* This project is supported by Tezos Foundation
* Michelson test set from the Tezos repo is used to ensure the interpreter workability
* Michelson structured documentation by Nomadic Labs is used for inline help