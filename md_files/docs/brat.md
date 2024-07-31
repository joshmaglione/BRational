# brat

The class we use to format rational functions is `brat`, and the kinds of rational functions accepted have the form
\[ 
	\dfrac{F(\bm{X})}{C\cdot \prod_{i=1}^m(1 - \bm{X}^{\alpha_i})}, 
\] 

where the following hold:

- $\bm{X}=(X_1, \dots, X_n)$ are variables,
- $F(\bm{X})\in \mathbb{Q}[\bm{X}]$,
- $C\in \mathbb{Q}$, 
- $m\in\N_0$, 
- $\alpha_i\in\N_0^n$, where $\bm{X}^{\alpha_i} = X_1^{\alpha_{i,1}}\cdots X_n^{\alpha_{i,n}}$.

The (ordered) keyword arguments for `brat` are

- `rational_expression`: the rational function (default: `None`),
- `numerator`: the numerator polynomial of the rational function (default: `None`),
- `denominator`: the denominator polynomial of the rational function (default: `None`),
- `denominator_signature`: the dictionary of data for the denominator (default: `None`),
- `fix_denominator`: whether to keep the given denominator fixed (default: `True`),
- `increasing_order`: whether to display polynomials in increasing degree (default: `True`).

*Additional notes*. The `denominator_signature` must be a dictionary whose keys are tuples of non-negative integers and whose keys are non-negative integers. If given a `denominator_signature`, the `numerator` will be used to determine the accepted ordered variables. [We do this by looking to its parent ring if `numerator` is a polynomial, or at the variables present if a symbolic expression.] Examples of acceptable `denominator_signature` are given below.

### Algebraic operations and relations

One can use the usual algebraic operations with `brat`: add, subtract, multiply, divide (i.e. 'true' divide), powers. The Boolean relations `==` and `!=` can also be used. When adding a `brat` with something else, we attempt to make another `brat` object. To "opt out", use the method `rational_function`. 

**Warning:** we cannot do anything about algebraic operations where the first object is *not* a `brat` object. For example, if `F` is a `brat` but `G` is a polynomial in SageMath, then `G + F` may raise errors, while `F + G` will attempt to add the two objects&mdash;other errors may arise.

### Examples

We expression the rational function
\[
	f(x,y)=\dfrac{1 + xy + x^2y^2}{(1 - x)(1 - y)}.
\]
First we write this in the usual way, using symbolic variables. 

```python
sage: x, y = var('x y')
sage: f = (1 + x*y + x^2*y^2)/((1 - x)*(1 - y))
sage: f
(x^2*y^2 + x*y + 1)/((x - 1)*(y - 1))
```

Now we build a `brat` from $f(x,y)$.
```python
sage: F = br.brat(f)
sage: F
(1 + x*y + x^2*y^2)/((1 - y)*(1 - x))
```

---

Now we write the rational function 
\[
	g(t) = \dfrac{1 + 4t + 6t^2 + 4t^3 + t^4}{(1 - t)(1 - t^2)(1 - t^3)(1 - t^4)} . 
\]

```python
sage: t = polygens(QQ, 't')[0]
sage: g = (1 + 4*t + 6*t^2 + 4*t^3 + t^4)/((1 - t)*(1 - t^2)*(1 - t^3)*(1 - t^4))
sage: g
(t^2 + 2*t + 1)/(t^8 - 3*t^7 + 4*t^6 - 5*t^5 + 6*t^4 - 5*t^3 + 4*t^2 - 3*t + 1)
```

Now we build a brat. 

```python
sage: G = br.brat(g)
sage: G
(1 + 2*t - 2*t^3 - t^4)/((1 - t)^3*(1 - t^3)*(1 - t^4))
```

## .denominator

Returns the polynomial in the denominator of the rational function. This is not necessarily reduced.

## .denominator_signature

Returns the dictionary signature for the denominator. The format of the dictionary is as follows. The keys are 

- "monomial": rational number,
- "factors": dictionary with keys given by vectors and values in the positive integers. 

#### Example 

If the variables are ordered as $(x,y,z)$ and the denominator is 
\[ 
	3\cdot (1 - x^2y)(1 - y^4)^3(1 - xyz)(1 - x^2)^5
\]

Then the dictionary is 
```python
{
	"monomial": 3
	"factors": {
		(2, 1, 0): 1, 
		(0, 4, 0): 3, 
		(1, 1, 1): 1, 
		(2, 0, 0): 5
	}
}
```

In nearly every situation, the monomial is absorbed to the numerator as a rational multiple. Now we do this in SageMath.

```python
sage: x, y, z = polygens(ZZ, 'x,y,z')
sage: F = br.brat(1/(3*(1 - x^2*y)*(1 - y^4)^3*(1 - x*y*z)*(1 - x^2)^5))
sage: F
(1/3)/((1 - x^2)^5*(1 - x*y*z)*(1 - x^2*y)*(1 - y^4)^3)
sage: F.denominator_signature()
{'monomial': 1,
 'factors': {(2, 0, 0): 5, (0, 4, 0): 3, (1, 1, 1): 1, (2, 1, 0): 1}}
```

## .increasing_order

This *attribute* is set to `True` by default&mdash;unless it was set to `False` upon construction. This can be toggled to either `True` or `False`. It will affect the print out and the `.latex` method.

## .invert_variables

Returns the corresponding `brat` after inverting all of the variables and then rewriting the rational function so that all exponents are non-negative. 

## .latex 

Returns a string that formats the `brat` in $\LaTeX$ in the `'\dfrac{...}{...}'` format.

Additional argument:

- `split`: If true, returns a pair of strings formatted in $\LaTeX$: the first is the numerator and the second is the denominator. Default: `False`.

#### Example

We obtain a $\LaTeX$ formatting of the following rational function:
\[ 
	\dfrac{1 + 2t + 4t^2 + 4t^3 + 2t^4 + t^5}{\prod_{i=1}^5(1 - t^i)} . 
\]

```python
sage: t = var('t')
sage: F = br.brat(
	numerator=1 + 2*t + 4*t^2 + 4*t^3 + 2*t^4 + t^5,
	denominator=prod(1 - t^i for i in range(1, 6))
)
sage: F
(1 + t + 3*t^2 + t^3 + t^4)/((1 - t)^2*(1 - t^3)*(1 - t^4)*(1 - t^5))
sage: F.latex()
'\\dfrac{1 + t + 3 t^{2} + t^{3} + t^{4}}{(1 - t)^{2}(1 - t^{3})(1 - t^{4})(1 - t^{5})}'
```

## .numerator

Returns the polynomial in the numerator of the rational function. This is not necessarily reduced.

## .rational_function

Returns the reduced rational function. The underlying type of this object is not a `brat`. 

This method should be used if you do not want SageMath to convert to a `brat` after applying operations to the rational function.

## .fix_denominator

Given a polynomial&mdash;or data equivalent to a polynomial (see arguments)&mdash;returns a new `brat`, equal to the original, whose denominator is the given polynomial.

(Ordered) keyword arguments:

- `expression`: the polynomial expression. Default: `None`.
- `signature`: the signature for the polynomial expression. See [denominator signature](#denominator_signature) method. Default: `None`.

## .subs

Given a dictionary of the desired substitutions, return the new `brat` obtained by performing the substitutions. 

This works in the same as the `subs` method for rational functions in SageMath. 

## .variables

Returns the variables used in the brat. These are polynomial variables rather than symbolic variables. 

#### Example 

We define the following rational function using symbolic variables
\[ 
	f(x,y,z) = \dfrac{1 + x^2y^2z^2}{(1 - xy)(1 - xz)(1 - yz)}
\]

```python
sage: x, y, z = var('x y z')
sage: f = (1 + x^2*y^2*z^2)/((1 - x*y)*(1 - x*z)*(1 - y*z))
sage: F = br.brat(f)
sage: F
(1 + x^2*y^2*z^2)/((1 - y*z)*(1 - x*z)*(1 - x*y))
```

We extract the variables and note that the type of variables have changed to be polynomial variables. 
```python
sage: varbs = F.variables()
sage: varbs
(x, y, z)
sage: type(varbs[0])
<class 'sage.rings.polynomial.multi_polynomial_libsingular.MPolynomial_libsingular'>
```