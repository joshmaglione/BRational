import sys
import os
from sage.all import ZZ, QQ, polygens, var, polygen

sys.path.append(os.getcwd())
from brational import brat

def test_integers_latex():
	assert brat(int(1)).latex() == "1"
	assert brat(int(0)).latex() == "0"
	assert brat(int(-1)).latex() == "-1"
	assert brat(ZZ(1)).latex() == "1"
	assert brat(ZZ(0)).latex() == "0"
	assert brat(ZZ(-1)).latex() == "-1"
	assert brat(ZZ(4)).latex() == "4"
	assert brat(ZZ(-12)).latex() == "-12"


def test_rationals_latex():
	assert brat(int(1)/int(2)).latex() == "\\dfrac{1}{2}"
	assert brat(int(3)/int(2)).latex() == "\\dfrac{3}{2}"
	assert brat(int(9)/int(12)).latex() == "\\dfrac{3}{4}"
	assert brat(ZZ(1)/ZZ(2)).latex() == "\\dfrac{1}{2}"
	assert brat(ZZ(3)/ZZ(2)).latex() == "\\dfrac{3}{2}"
	assert brat(ZZ(9)/ZZ(12)).latex() == "\\dfrac{3}{4}"
	assert brat(numerator=ZZ(5), denominator=int(10), fix_denominator=False).latex() == "\\dfrac{1}{2}"
	assert brat(numerator=ZZ(5), denominator=ZZ(10), fix_denominator=True).latex() == "\\dfrac{5}{10}"
	assert brat(numerator=ZZ(5), denominator=ZZ(-10), fix_denominator=True).latex() == "\\dfrac{-5}{10}"
	assert brat(numerator=ZZ(5), denominator=ZZ(-10), fix_denominator=False).latex() == "\\dfrac{-1}{2}"


def test_univariate_polynomials_latex():
	x = var('x')
	assert brat(x + 1).latex() == "1 + x"
	assert brat(x**2 - 1 - x).latex() == "-(1 + x - x^2)"
	assert brat(1 + 2*x + x*x).latex() == "1 + 2x + x^2"
	assert brat(1 + 2*x + x*x).factor().latex() == "(1 + x)^2"
	assert brat(3 + x - x**10, increasing_order=False).latex() == "-(x^{10} - x - 3)"
	assert brat(x + QQ(1/2)).latex() == "\\dfrac{1 + 2x}{2}"
	assert brat((x**58 - 1 - x)/4).latex() == "\\dfrac{-(1 + x - x^{58})}{4}"
	assert brat((1 + 2*x + x*x)/6).latex() == "\\dfrac{1 + 2x + x^2}{6}"
	assert brat((1 + 2*x + x*x)/6).factor().latex() == "\\dfrac{(1 + x)^2}{6}"
	assert brat(3 + x - x**4/2, increasing_order=False).latex() == "\\dfrac{-(x^4 - 2x - 6)}{2}"
	assert str(brat(numerator=x + x**9 - x**12, denominator=x).latex()) == "1 + x^8 - x^{11}"


def test_multivariate_polynomials_latex():
	q, t = polygens(QQ, ('q', 't'))
	assert str(brat(q**2 + 2*q*t + t**2).latex()) == "t^2 + 2qt + q^2"
	assert str(brat(q**2 + 2*q*t + t**2, increasing_order=False).latex()) == "q^2 + 2qt + t^2"
	assert str(brat((q**2 + 2*q*t + t**2)/60).latex()) == "\\dfrac{t^2 + 2qt + q^2}{60}"
	assert str(brat((q**2 + 2*q*t + t**2)/60, increasing_order=False).latex()) == "\\dfrac{q^2 + 2qt + t^2}{60}"
	assert str(brat(q**2 + 2*q*t + t**2).factor().latex()) == "(t + q)^2"
	assert str(brat(q**2 + 2*q*t + t**2, increasing_order=False).factor().latex()) == "(q + t)^2"
	assert str(brat((q**2 + 2*q*t + t**2)/6).factor().latex()) == "\\dfrac{(t + q)^2}{6}"
	assert str(brat((q**2 + 2*q*t + t**2)/6, increasing_order=False).factor().latex()) == "\\dfrac{(q + t)^2}{6}"


def test_univariate_laurent_polynomials_latex():
	x = var('x')
	assert brat(x + 1/x).latex() == "x^{-1} + x"
	assert brat((1 + 2*x + x**2)/x**6).latex() == "x^{-6} + 2x^{-5} + x^{-4}"
	assert brat((1 + 2*x + x**2)/x**6).factor().latex() == "x^{-6}(1 + x)^2"
	assert brat(x + 1/x, increasing_order=False).latex() == "x + x^{-1}"
	assert brat((1 + 2*x + x**2)/x**6, increasing_order=False).latex() == "x^{-4} + 2x^{-5} + x^{-6}"
	assert brat((1 + 2*x + x**2)/x**6, increasing_order=False).factor().latex() == "x^{-6}(x + 1)^2"
	assert brat(numerator=1, denominator=x**32).latex() == "x^{-32}"
	assert brat(numerator=1, denominator=x**32).factor().latex() == "x^{-32}"
	assert brat(numerator=(1 + x)*(1 + x**3 - x**5), denominator_signature={
		"coefficient": 2,
		"monomial": (32,),
		"factors": {},
	}).latex() == "\\dfrac{x^{-32} + x^{-31} + x^{-29} + x^{-28} - x^{-27} - x^{-26}}{2}"
	assert brat(numerator=(1 + x)*(1 + x**3 - x**5), denominator_signature={
		"coefficient": 2,
		"monomial": (32,),
		"factors": {},
	}).factor().latex() == "\\dfrac{x^{-32}(1 + x)(1 + x^3 - x^5)}{2}"
	assert brat(x + 1/x, hide_monomial=False).latex() == "\\dfrac{1 + x^2}{x}"
	assert brat((1 + 2*x + x**2)/x**6, hide_monomial=False).latex() == "\\dfrac{1 + 2x + x^2}{x^6}"
	assert brat((1 + 2*x + x**2)/x**6, hide_monomial=False).factor().latex() == "\\dfrac{(1 + x)^2}{x^6}"
	assert brat(x + 1/x, increasing_order=False, hide_monomial=False).latex() == "\\dfrac{x^2 + 1}{x}"
	assert brat((1 + 2*x + x**2)/x**6, increasing_order=False, hide_monomial=False).latex() == "\\dfrac{x^2 + 2x + 1}{x^6}"
	assert brat((1 + 2*x + x**2)/x**6, increasing_order=False, hide_monomial=False).factor().latex() == "\\dfrac{(x + 1)^2}{x^6}"
	assert brat(numerator=1, denominator=x**32, hide_monomial=False).latex() == "\\dfrac{1}{x^{32}}"
	assert brat(numerator=1, denominator=x**32, hide_monomial=False).factor().latex() == "\\dfrac{1}{x^{32}}"
	assert brat(numerator=(1 + x)*(1 + x**3 - x**5), denominator_signature={
		"coefficient": 2,
		"monomial": (32,),
		"factors": {},
	}, hide_monomial=False).latex() == "\\dfrac{1 + x + x^3 + x^4 - x^5 - x^6}{2x^{32}}"
	assert brat(numerator=(1 + x)*(1 + x**3 - x**5), denominator_signature={
		"coefficient": 2,
		"monomial": (32,),
		"factors": {},
	}, hide_monomial=False).factor().latex() == "\\dfrac{(1 + x)(1 + x^3 - x^5)}{2x^{32}}"


def test_multivariate_laurent_polynomials_latex():
	q, t = polygens(QQ, ('q', 't'))
	assert brat(t + q**-1).latex() == "q^{-1} + t"
	assert brat(t + q**-1, increasing_order=False).latex() == "t + q^{-1}"
	assert brat(t + q**-1, hide_monomial=False).latex() == "\\dfrac{1 + qt}{q}"
	assert brat((1 + q*t - t**2)/q**3).latex() == "q^{-3} - q^{-3}t^2 + q^{-2}t"
	assert brat((1 + q*t - t**2)/q**3, increasing_order=False).latex() == "q^{-2}t - q^{-3}t^2 + q^{-3}"
	assert brat((1 + q*t - t**2)/q**3, hide_monomial=False).latex() == "\\dfrac{1 - t^2 + qt}{q^3}"
	assert brat(q**-5*t**-10).latex() == "q^{-5}t^{-10}"
	assert brat(12*q**-5*t**-10).latex() == "12q^{-5}t^{-10}"
	assert brat(12**-1*(q**-5*t**-10+q**-3*t**-12)).latex() == "\\dfrac{q^{-5}t^{-10} + q^{-3}t^{-12}}{12}"
	assert brat(12**-1*(q**-5*t**-10+q**-3*t**-12), hide_monomial=False).latex() == "\\dfrac{t^2 + q^2}{12q^5t^{12}}"
	assert brat(q**-5*t**-10, hide_monomial=False).latex() == "\\dfrac{1}{q^5t^{10}}"
	assert brat((q + 1)**2*t**-5*(q + t)).latex() == "t^{-4} + qt^{-5} + 2qt^{-4} + 2q^2t^{-5} + q^2t^{-4} + q^3t^{-5}"
	assert brat((q + 1)**2*t**-5*(q + t), hide_monomial=False).latex() == "\\dfrac{t + q + 2qt + 2q^2 + q^2t + q^3}{t^5}"
	assert brat((q + 1)**2*t**-5*(q + t)).factor().latex() == "t^{-5}(t + q)(1 + q)^2"
	assert brat((q + 1)**2*t**-5*(q + t), hide_monomial=False).factor().latex() == "\\dfrac{(t + q)(1 + q)^2}{t^5}"
	assert brat(numerator=q*t, denominator_signature={
		"coefficient": 4,
		"monomial": (23, 29),
		"factors": {},
	}).latex() == "\\dfrac{q^{-22}t^{-28}}{4}"
	assert brat(numerator=q*t, denominator_signature={
		"coefficient": 4,
		"monomial": (23, 29),
		"factors": {},
	}, hide_monomial=False).latex() == "\\dfrac{qt}{4q^{23}t^{29}}"
	assert brat(numerator=q*t, denominator_signature={
		"coefficient": 4,
		"monomial": (23, 29),
		"factors": {},
	}, hide_monomial=False, fix_denominator=False).latex() == "\\dfrac{1}{4q^{22}t^{28}}"


def main():
	test_integers_latex()
	test_rationals_latex()
	test_univariate_polynomials_latex()
	test_multivariate_polynomials_latex()
	test_univariate_laurent_polynomials_latex()
	test_multivariate_laurent_polynomials_latex()
	print("All tests passed!")


if __name__ == "__main__":
	main()