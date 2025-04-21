# Methods (brat)

We describe all of the methods associated with the class `brat` together with an example. 

## .denominator

Returns the polynomial in the denominator of the rational function. This is not necessarily reduced.

### Example

We build a `brat` for the following rational function and extract the denominator:
\[ 
	f(x,y) = \dfrac{1 + xy^2}{1 - x^2y^4}. 
\]

```python
sage: x, y = polygens(QQ, 'x,y')
sage: f = br.brat(
	numerator=1 + x*y^2,
	denominator=1 - x^2*y^4
)
sage: f
(1 + x*y^2)/(1 - x^2*y^4)
sage: f.denominator()
-x^2*y^4 + 1
```

## .denominator_signature

Returns the dictionary signature for the denominator. The format of the dictionary is as follows. The keys are 

- "monomial": dictionary with one key given by a vector and a positive integer value.
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

We can extract this dictionary by creating a `brat` with numerator `1`.

```python
sage: x, y, z = polygens(ZZ, 'x,y,z')
sage: F = br.brat(1/(3*(1 - x^2*y)*(1 - y^4)^3*(1 - x*y*z)*(1 - x^2)^5))
sage: F
1/(3*(1 - x^2)^5*(1 - x*y*z)*(1 - x^2*y)*(1 - y^4)^3)
sage: F.denominator_signature()
{'monomial': 3,
 'factors': {(2, 0, 0): 5, (0, 4, 0): 3, (1, 1, 1): 1, (2, 1, 0): 1}}
```

## .factor 

Returns a new `brat` object with the numerator polynomial factored.

## .fix_denominator

Given a polynomial&mdash;or data equivalent to a polynomial (see arguments)&mdash;returns a new `brat`, equal to the original, whose denominator is the given polynomial.

(Ordered) keyword arguments:

- `expression`: the polynomial expression. Default: `None`.
- `signature`: the signature for the polynomial expression. See [denominator signature](#denominator_signature) method. Default: `None`.

### Example 

We construct the following rational function:
\[ 
	H = \dfrac{(1 + x^3)(1 + x^4)(1 + x^5)}{(1 - x)(1 - x^2)(1 - x^3)^2(1 - x^4)(1 - x^5)}
\]
from a simplified expression. Then we recover this particular expression using `fix_denominator`.

```python
sage: x = polygens(QQ, 'x')[0]
sage: h = (1 + x^3)*(1 + x^4)*(1 + x^5)/((1 - x)*(1 - x^2)*(1 - x^3)^2*(1 - x^4)*(1 - x^5))
sage: h
(x^10 - 2*x^9 + 3*x^8 - 3*x^7 + 4*x^6 - 4*x^5 + 4*x^4 - 3*x^3 + 3*x^2 - 2*x + 1)/(x^16 - 3*x^15 + 4*x^14 - 6*x^
13 + 9*x^12 - 10*x^11 + 12*x^10 - 13*x^9 + 12*x^8 - 13*x^7 + 12*x^6 - 10*x^5 + 9*x^4 - 6*x^3 + 4*x^2 - 3*x + 1)
sage: H = br.brat(h)
sage: H
(1 - 2*x + 2*x^2 - x^3 + x^4 - x^5 + x^7 - x^8 + x^9 - 2*x^10 + 2*x^11 - x^12)/((1 - x)^3*(1 - x^3)^2*(1 - x^4)
*(1 - x^5))
sage: H.fix_denominator(
	signature={(1,): 1, (2,): 1, (3,): 2, (4,): 1, (5,): 1}
)
(1 + x^3 + x^4 + x^5 + x^7 + x^8 + x^9 + x^12)/((1 - x)*(1 - x^2)*(1 - x^3)^2*(1 - x^4)*(1 - x^5))
```

## .increasing_order

This is set to `True` by default&mdash;unless it was set to `False` upon construction. This can be toggled to either `True` or `False`. It will affect the print out and the `.latex` method. 

This is an *attribute* and not a method like the rest of the functions on this page. This means it is called without parentheses 

### Example

We construct the following polynomial and then switch the display order:
\[ 
	h = t^3 - 6t^2 + 11t - 6.
\]

```python
sage: t = polygens(QQ, 't')[0]
sage: h = br.brat(t^3 - 6*t^2 + 11*t - 6)
sage: h
-6 + 11*t - 6*t^2 + t^3
sage: h.increasing_order = False
sage: h
t^3 - 6*t^2 + 11*t - 6
```


## .invert_variables

Returns the corresponding `brat` after inverting all of the variables and then rewriting the rational function so that all exponents are non-negative. 

Keyword argument:

- `ratio`: returns the ratio of the original brat divided by the brat with inverted variables. Default: `False`.

### Example 1

We will verify that, after inverting the variables of 
\[ 
	E = \dfrac{1 + 26T + 66T^2 + 26T^3 + T^4}{(1 - T)^5},
\]
we obtain a $T$-multiple of it.

```python
sage: T = var('T')
sage: E = br.brat(
	numerator=1 + 26*T + 66*T^2 + 26*T^3 + T^4,
	denominator_signature={(1,): 5}
)
sage: E
(1 + 26*T + 66*T^2 + 26*T^3 + T^4)/(1 - T)^5
sage: E.invert_variables()
(-T - 26*T^2 - 66*T^3 - 26*T^4 - T^5)/(1 - T)^5
```

Now we can show it more clearly.
```python
sage: E.invert_variables()/E
-T
```

We can achieve this all in one go by using the keyword `ratio`.
```python
sage: E.invert_variables(ratio=True)
-T
```

### Example 2

We show that, after inverting the variables of 
\[ 
	P = 1 + 2x + x^2
\]
we do not get a rational function that satisfies the [main assumption](brat.md#brat) of a `brat`. Hence the output is not a `brat`.

```python
sage: x = var('x')
sage: P = br.brat(1 + 2*x + x^2)
sage: P
1 + 2*x + x^2
sage: P.invert_variables()
(x^2 + 2*x + 1)/x^2
sage: isinstance(P.invert_variables(), br.brat)
False
```

## .latex 

Returns a string that formats the `brat` in $\LaTeX$ in the `'\dfrac{...}{...}'` format.

Additional argument:

- `factor`: factor the numerator polynomial. Default: `False`.
- `split`: if true, returns a pair of strings formatted in $\LaTeX$: the first is the numerator and the second is the denominator. Default: `False`.

#### Example

We obtain a $\LaTeX$ formatting of the following rational function:
\[ 
	\dfrac{1 + 2t^2 + 4t^4 + 4t^6 + 2t^8 + t^{10}}{\prod_{i=1}^5(1 - t^i)} . 
\]

```python
sage: t = var('t')
sage: F = br.brat(
	numerator=1 + 2*t^2 + 4*t^4 + 4*t^6 + 2*t^8 + t^10,
	denominator=prod(1 - t^i for i in range(1, 6))
)
sage: F
(1 + 2*t^2 + 4*t^4 + 4*t^6 + 2*t^8 + t^10)/((1 - t)*(1 - t^2)*(1 - t^3)*(1 - t^4)*(1 - t^5))
sage: F.latex()
'\\dfrac{1 + 2t^2 + 4t^4 + 4t^6 + 2t^8 + t^{10}}{(1 - t)(1 - t^2)(1 - t^3)(1 - t^4)(1 - t^5)}'
```

By setting `split` to `True`, we get the numerator and denominator separated.
```python
sage: F.latex(split=True)
('1 + 2t^2 + 4t^4 + 4t^6 + 2t^8 + t^{10}',
 '(1 - t)(1 - t^2)(1 - t^3)(1 - t^4)(1 - t^5)')
```

## .numerator

Returns the polynomial in the numerator of the rational function. This is not necessarily reduced.

### Example

We build a `brat` for the following rational function and extract the numerator:
\[ 
	f(x,y) = \dfrac{1 + xy^2}{1 - x^2y^4}. 
\]

```python
sage: x, y = polygens(QQ, 'x,y')
sage: f = br.brat(
	numerator=1 + x*y^2,
	denominator=1 - x^2*y^4
)
sage: f
(1 + x*y^2)/(1 - x^2*y^4)
sage: f.numerator()
x*y^2 + 1
```

## .rational_function

Returns the reduced rational function. The underlying type of this object is not a `brat`. 

This method should be used if you do not want SageMath to convert to a `brat` after applying operations to the rational function.

### Example

We build a `brat` for the following rational function and extract the rational function:
\[ 
	f(x,y) = \dfrac{1 + xy^2}{1 - x^2y^4}. 
\]

```python
sage: x, y = polygens(QQ, 'x,y')
sage: f = br.brat(
	numerator=1 + x*y^2,
	denominator=1 - x^2*y^4
)
sage: f
(1 + x*y^2)/(1 - x^2*y^4)
sage: f.rational_function()
1/(-x*y^2 + 1)
```

## .subs

Given a dictionary of the desired substitutions, return the new `brat` obtained by performing the substitutions. 

This works in the same as the `subs` method for rational functions in SageMath. 

### Example 

We apply some substitutions to the following rational function:
\[ 
	C(T,Y) = \dfrac{1 + 3Y + 2Y^2 + (2 + 3Y + Y^2)T}{(1 - T)^2} . 
\]

```python
sage: Y, T = polygens(QQ, 'Y,T')
sage: C = br.brat(
	numerator=1 + 3*Y + 2*Y^2 + (2 + 3*Y + Y^2)*T,
	denominator_signature={(0,1): 2}
)
sage: C
(1 + 2*T + 3*Y + 3*Y*T + 2*Y^2 + Y^2*T)/(1 - T)^2
```

We set $Y$ to $0$ by applying a substitution.
```python
sage: C.subs({Y: 0})
(1 + 2*T)/(1 - T)^2
```

Note that some substitutions yield rational functions that do not satisfy the [main assumption](brat.md#brat), so the output will not be a `brat`.
```python
sage: C.subs({T: T - 1})
(Y^2*T + Y^2 + 3*Y*T + 2*T - 1)/(T^2 - 4*T + 4)
```

## .variables

Returns the polynomial variables used.

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

## .write_latex

Writes the `brat` object to a file formatted in $\LaTeX$. The (default) output is a displayed equation (using `\[` and `\]`) of the `brat`. There are many parameters to change the format of the output.

(Ordered) keyword arguments:

- `filename`: the string for the output filename. Default: `None`, which will output a timestamp name of the form `%Y-%m-%d_%H-%M-%S.tex`.
- `just_numerator`: write just the numerator. Default: `False`.
- `just_denominator`: write just the denominator. Default: `False`.
- `align`: format using the `align*` environment. This is especially useful for long polynomials. Default: `False`.
- `factor`: factor the numerator polynomial. Default: `False`.
- `line_width`: determines the line width in characters for each line of the `align*` environment. Only used when `align` is set to `True`. Default: `120`.
- `function_name`: turns the expression to an equation by displaying the function name. Default: `None`.
- `save_message`: turns on the save message at the end. Default: `True`.

#### Examples

We will write the following function to `test.tex` with all the other parameters set to their defaults:
\[ 
	\dfrac{1 + xy^2}{1 - x^2y^4}
\]

```python
sage: x, y = polygens(QQ, 'x,y')
sage: f = br.brat(
	numerator=1 + x*y^2,
	denominator=1 - x^2*y^4
)
sage: f
(1 + x*y^2)/(1 - x^2*y^4)
sage: f.write_latex('test.tex')
File saved as test.tex.
sage: with open('test.tex', 'r') as out_file:
....:     print(out_file.read())
\[
	\dfrac{1 + x y^2}{(1 - x^2y^4)}
\]
```

Now we write the expanded polynomial to the file `binomial.tex`:
\[ 
	(1 + X)^{20}
\]

Since it is just a polynomial, we will set `just_numerator` to `True`. We will also print this in an `algin` environment, leaving the `line_width` at 120 characters. 

```python
sage: X = polygens(QQ, 'X')[0]
sage: f = br.brat((1 + X)^20)
sage: f
1 + 20*X + 190*X^2 + 1140*X^3 + 4845*X^4 + 15504*X^5 + 38760*X^6 + 77520*X^7 + 125970*X^8 + 167960*X^9 + 184756*X^10 + 167960*X^11 + 125970*X^12 + 77520*X^13 + 38760*X^14 + 15504*X^15 + 4845*X^16 + 1140*X^17 + 190*X^18 + 20*X^19 + X^20
sage: f.write_latex(
	filename="binomial.tex",
	just_numerator=True,
	align=True,
	function_name="B_{20}(X)"
)
sage: with open("binomial.tex", "r") as output:
....:     print(output.read())
\begin{align*}
	B_{20}(X) &= 1 + 20X + 190X^2 + 1140X^3 + 4845X^4 + 15504X^5 + 38760X^6 + 77520X^7 + 125970X^8 \\ 
	&\quad + 167960X^9 + 184756X^{10} + 167960X^{11} + 125970X^{12} + 77520X^{13} + 38760X^{14} + 15504X^{15} \\ 
	&\quad + 4845X^{16} + 1140X^{17} + 190X^{18} + 20X^{19} + X^{20}
\end{align*}
```

The polynomial compiles to 

\[\begin{aligned}
	B_{20}(X) &= 1 + 20X + 190X^2 + 1140X^3 + 4845X^4 + 15504X^5 + 38760X^6 + 77520X^7 + 125970X^8 \\\\
	&\quad + 167960X^9 + 184756X^{10} + 167960X^{11} + 125970X^{12} + 77520X^{13} + 38760X^{14} + 15504X^{15} \\\\
	&\quad + 4845X^{16} + 1140X^{17} + 190X^{18} + 20X^{19} + X^{20}
\end{aligned}\]