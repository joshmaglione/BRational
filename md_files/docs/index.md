# BRational

Author: [Joshua Maglione](https://www.joshmaglione/com).

Documentation for the [BRational](https://github.com/joshmaglione/brational) package for [SageMath](https://www.sagemath.org/).

## Purpose

The goal of **BRational** is to format certain rational functions in SageMath in a particular format. These rational functions contain the class of generating series, which is our primary use case. The main purpose is to enable users to manipulate such expressions and to rewrite expressions for ease of comprehension. 

## Setup

The simplest way to **install** BRational is to run the following 

```sh
$ sage --pip install brational
```

Alternatively, one can download the [latest release](https://github.com/joshmaglione/brational/releases/latest) and unzip it into a directory that SageMath can find for importing.

To **update** an older version of BRational to the latest version, run the following 

```sh 
$ sage --pip install brational --upgrade 
```

BRational has no external dependencies and is compatible with SageMath 9.6 and later. It may work just fine with earlier versions of SageMath, but these have not been tested.

## Importing

Import BRational during your SageMath run with the following

```python
import brational as br
```

Throughout this documentation, we use `br` for the reference name of `brational`.
