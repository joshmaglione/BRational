from brational import brat
from sage.all import ZZ, QQ, polygens, var, polygen

def test_integers():
	assert str(brat(int(1))) == "1"
	assert str(brat(int(0))) == "0"
	assert str(brat(int(-1))) == "-1"
	assert brat(int(1)).latex() == "1"
	assert brat(int(0)).latex() == "0"
	assert brat(int(-1)).latex() == "-1"
	assert str(brat(ZZ(1))) == "1"
	assert str(brat(ZZ(0))) == "0"
	assert str(brat(ZZ(-1))) == "-1"
	assert str(brat(ZZ(4))) == "4"
	assert str(brat(ZZ(-12))) == "-12"
	assert brat(ZZ(1)).latex() == "1"
	assert brat(ZZ(0)).latex() == "0"
	assert brat(ZZ(-1)).latex() == "-1"
	assert brat(ZZ(4)).latex() == "4"
	assert brat(ZZ(-12)).latex() == "-12"
	assert str(brat(numerator=ZZ(-12), denominator=int(3), fix_denominator=False)) == "-4"
	assert str(brat(numerator=ZZ(12), denominator=int(-3), fix_denominator=False)) == "-4"
	assert str(brat(ZZ(4)).factor()) == "4"
	assert str(brat(ZZ(-12)).factor()) == "-12"
	assert str(brat(numerator=int(2), denominator_signature={
		"coefficient": 1,
		"monomial": (0,0,0),
		"factors": {},
	})) == "2"
	assert str(brat(numerator=int(2), denominator_signature={
		"coefficient": -1,
		"monomial": (0,0,0),
		"factors": {},
	})) == "-2"
	assert str(brat(numerator=int(-6), denominator_signature={
		"coefficient": -2,
		"monomial": (),
		"factors": {},
	}, fix_denominator=False)) == "3"
	

def test_rationals():
	assert str(brat(int(1)/int(2))) == "1/2"
	assert str(brat(int(3)/int(2))) == "3/2"
	assert str(brat(int(9)/int(12))) == "3/4"
	assert str(brat(ZZ(1)/ZZ(2))) == "1/2"
	assert str(brat(ZZ(3)/ZZ(2))) == "3/2"
	assert str(brat(ZZ(9)/ZZ(12))) == "3/4"
	assert str(brat(numerator=ZZ(5), denominator=int(10), fix_denominator=False)) == "1/2"
	assert str(brat(numerator=ZZ(5), denominator=ZZ(10), fix_denominator=True)) == "5/10"
	assert str(brat(numerator=ZZ(5), denominator=ZZ(-10), fix_denominator=True)) == "-5/10"
	assert str(brat(numerator=ZZ(5), denominator=ZZ(-10), fix_denominator=False)) == "-1/2"
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


def test_polynomials():
	x = var('x')
	assert str(brat(x + 1)) == "1 + x"
	assert str(brat(x**2 - 1 - x)) == "-(1 + x - x^2)"
	assert str(brat(1 + 2*x + x*x)) == "1 + 2*x + x^2"
	assert str(brat(1 + 2*x + x*x).factor()) == "(1 + x)^2"
	assert str(brat(3 + x - x**4, increasing_order=False)) == "-(x^4 - x - 3)"
	assert str(brat(x + 1/2)) == "(1 + 2*x)/2"
	assert str(brat((x**2 - 1 - x)/4)) == "-(1 + x - x^2)/4"
	assert str(brat((1 + 2*x + x*x)/6)) == "(1 + 2*x + x^2)/6"
	assert str(brat((1 + 2*x + x*x)/6).factor()) == "(1 + x)^2/6"
	assert str(brat(3 + x - x**4/2, increasing_order=False)) == "-(x^4 - 2*x - 6)/2"
	assert brat(x + 1).latex() == "1 + x"
	assert brat(x**2 - 1 - x).latex() == "-(1 + x - x^2)"
	assert brat(1 + 2*x + x*x).latex() == "1 + 2x + x^2"
	assert brat(1 + 2*x + x*x).factor().latex() == "(1 + x)^2"
	assert brat(3 + x - x**10, increasing_order=False).latex() == "-(x^{10} - x - 3)"
	assert brat(x + 1/2).latex() == "\\dfrac{1 + 2x}{2}"
	assert brat((x**58 - 1 - x)/4).latex() == "\\dfrac{-(1 + x - x^{58})}{4}"
	assert brat((1 + 2*x + x*x)/6).latex() == "\\dfrac{1 + 2x + x^2}{6}"
	assert brat((1 + 2*x + x*x)/6).factor().latex() == "\\dfrac{(1 + x)^2}{6}"
	assert brat(3 + x - x**4/2, increasing_order=False).latex() == "\\dfrac{-(x^4 - 2x - 6)}{2}"
	q, t = polygens(QQ, ('q', 't'))
	assert str(brat(q**2 + 2*q*t + t**2)) == "t^2 + 2*q*t + q^2"
	assert str(brat(q**2 + 2*q*t + t**2, increasing_order=False)) == "q^2 + 2*q*t + t^2"
	assert str(brat((q**2 + 2*q*t + t**2)/60)) == "(t^2 + 2*q*t + q^2)/60"
	assert str(brat((q**2 + 2*q*t + t**2)/60, increasing_order=False)) == "(q^2 + 2*q*t + t^2)/60"
	assert str(brat(q**2 + 2*q*t + t**2).factor()) == "(t + q)^2"
	assert str(brat(q**2 + 2*q*t + t**2, increasing_order=False).factor()) == "(q + t)^2"
	assert str(brat((q**2 + 2*q*t + t**2)/6).factor()) == "(t + q)^2/6"
	assert str(brat((q**2 + 2*q*t + t**2)/6, increasing_order=False).factor()) == "(q + t)^2/6"
	assert str(brat(q**2 + 2*q*t + t**2).latex()) == "t^2 + 2qt + q^2"
	assert str(brat(q**2 + 2*q*t + t**2, increasing_order=False).latex()) == "q^2 + 2qt + t^2"
	assert str(brat((q**2 + 2*q*t + t**2)/60).latex()) == "\\dfrac{t^2 + 2qt + q^2}{60}"
	assert str(brat((q**2 + 2*q*t + t**2)/60, increasing_order=False).latex()) == "\\dfrac{q^2 + 2qt + t^2}{60}"
	assert str(brat(q**2 + 2*q*t + t**2).factor().latex()) == "(t + q)^2"
	assert str(brat(q**2 + 2*q*t + t**2, increasing_order=False).factor().latex()) == "(q + t)^2"
	assert str(brat((q**2 + 2*q*t + t**2)/6).factor().latex()) == "\\dfrac{(t + q)^2}{6}"
	assert str(brat((q**2 + 2*q*t + t**2)/6, increasing_order=False).factor().latex()) == "\\dfrac{(q + t)^2}{6}"


def test_laurent_polynomials():
	x = polygen(QQ, 'x')
	assert str(brat(x + 1/x)) == "x^-1 + x"
	assert str(brat((1 + 2*x + x**2)/x**6)) == "x^-6 + 2*x^-5 + x^-4"
	assert str(brat((1 + 2*x + x**2)/x**6).factor()) == "x^-6*(1 + x)^2"



def test_previous_bugs():
	t = var('t')
	R1 = brat((t^8 - 1)/((t^4 + t^3 + t^2 + t + 1)*(t^4 + t^2 + 1)*(t^3 - 1)*(t^2 - 1)*(t - 1)^5))
	R2 = brat((t^8 - 1)/((t^6 - 1)*(t^5 - 1)*(t^2 + t + 1)*(t - 1)^5))
	assert str(R1) == "(1 - t^8)/((1 - t)^4*(1 - t^3)*(1 - t^5)*(1 - t^6))"
	assert R1.latex() == "\\dfrac{1 - t^8}{(1 - t)^4(1 - t^3)(1 - t^5)(1 - t^6)}"
	assert str(R2) == "(1 - t^8)/((1 - t)^4*(1 - t^3)*(1 - t^5)*(1 - t^6))"
	assert R2.latex() == "\\dfrac{1 - t^8}{(1 - t)^4(1 - t^3)(1 - t^5)(1 - t^6)}"

def main():
	test_integers()
	test_rationals()
	test_polynomials()
	test_laurent_polynomials()
	test_previous_bugs()
	print("All tests passed!")

if __name__ == "__main__":
	main()