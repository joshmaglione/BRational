# BRational

&emsp;

The goal of **BRational** is to format certain rational functions in SageMath to enable users to think entirely about their own work and interests and not about formatting.

&ensp;

## Install

The simplest way to install BRational is to run the following 

- in a terminal:

```sh
$ sage --pip install brational
```

- or in SageMath:

```python
sage: %pip install brational
```

Alternatively, one can download the [latest release](https://github.com/joshmaglione/brational/releases/latest) and unzip it into a directory that SageMath can find for importing.

&ensp;

## Update

To update an older version of BRational to the latest version, run the following 

- in a terminal: 

```sh 
$ sage --pip install brational --upgrade 
```

- or in SageMath:

```python
sage: %pip install brational --upgrade 
```

BRational has no external dependencies and is compatible with SageMath 9.6 and later. It may work just fine with earlier versions of SageMath, but these have not been tested.

&ensp;


## Uninstall

Assuming you installed BRational by using `pip` (see [Install](#install)), then you can run one of the following

- in a terminal:

```sh
$ sage --pip uninstall brational
```

- or in SageMath:

```python
sage: %pip uninstall brational
```

&ensp;


## Importing

Import BRational during your SageMath run with the following

```python
import brational as br
```

Throughout this documentation, we use `br` for the reference name of `brational`.

&ensp;

## Citing 

If you have used BRational and would like to cite us, please adapt the following to your style.

- Joshua Maglione, *BRational: Beautiful formatting of rational functions*, version 2.0.1, 2025, https://github.com/joshmaglione/BRational.

BibTeX format:

```bibtex
@misc{BRational,
  author       = {Joshua Maglione},
  title        = {{BR}ational: {B}eautiful formatting of rational functions, version 2.0.1},
  note          = {\url{https://github.com/joshmaglione/BRational}},
  year         = {2025},
}
```