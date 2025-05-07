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
	assert str(brat(numerator=x + x**9 - x**12, denominator=x)) == "1 + x^8 - x^11"
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
	assert str(brat(numerator=x + x**9 - x**12, denominator=x).latex()) == "1 + x^8 - x^{11}"
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
	assert str(brat(x + 1/x, increasing_order=False)) == "x + x^-1"
	assert str(brat((1 + 2*x + x**2)/x**6, increasing_order=False)) == "x^-4 + 2*x^-5 + x^-6"
	assert str(brat((1 + 2*x + x**2)/x**6, increasing_order=False).factor()) == "x^-6*(x + 1)^2"
	assert str(brat(numerator=1, denominator=x**32)) == "x^-32"
	assert str(brat(numerator=1, denominator=x**32).factor()) == "x^-32"
	assert str(brat(numerator=(1 + x)*(1 + x**3 - x**5), denominator_signature={
		"coefficient": 2,
		"monomial": (32,),
		"factors": {},
	})) == "(x^-32 + x^-31 + x^-29 + x^-28 - x^-27 - x^-26)/2"
	assert str(brat(numerator=(1 + x)*(1 + x**3 - x**5), denominator_signature={
		"coefficient": 2,
		"monomial": (32,),
		"factors": {},
	}).factor()) == "x^-32*(1 + x)*(1 + x^3 - x^5)/2"
	assert str(brat(x + 1/x, negative_exponents=False)) == "(1 + x^2)/x"
	assert str(brat((1 + 2*x + x**2)/x**6, negative_exponents=False)) == "(1 + 2*x + x^2)/x^6"
	assert str(brat((1 + 2*x + x**2)/x**6, negative_exponents=False).factor()) == "(1 + x)^2/x^6"
	assert str(brat(x + 1/x, increasing_order=False, negative_exponents=False)) == "(x^2 + 1)/x"
	assert str(brat((1 + 2*x + x**2)/x**6, increasing_order=False, negative_exponents=False)) == "(x^2 + 2*x + 1)/x^6"
	assert str(brat((1 + 2*x + x**2)/x**6, increasing_order=False, negative_exponents=False).factor()) == "(x + 1)^2/x^6"
	assert str(brat(numerator=1, denominator=x**32, negative_exponents=False)) == "1/x^32"
	assert str(brat(numerator=1, denominator=x**32, negative_exponents=False).factor()) == "1/x^32"
	assert str(brat(numerator=(1 + x)*(1 + x**3 - x**5), denominator_signature={
		"coefficient": 2,
		"monomial": (32,),
		"factors": {},
	}, negative_exponents=False)) == "(1 + x + x^3 + x^4 - x^5 - x^6)/(2*x^32)"
	assert str(brat(numerator=(1 + x)*(1 + x**3 - x**5), denominator_signature={
		"coefficient": 2,
		"monomial": (32,),
		"factors": {},
	}, negative_exponents=False).factor()) == "(1 + x)*(1 + x^3 - x^5)/(2*x^32)"
	


def test_previous_bugs():
	t = var('t')
	R1 = brat((t^8 - 1)/((t^4 + t^3 + t^2 + t + 1)*(t^4 + t^2 + 1)*(t^3 - 1)*(t^2 - 1)*(t - 1)^5))
	R2 = brat((t^8 - 1)/((t^6 - 1)*(t^5 - 1)*(t^2 + t + 1)*(t - 1)^5))
	assert str(R1) == "(1 - t^8)/((1 - t)^4*(1 - t^3)*(1 - t^5)*(1 - t^6))"
	assert R1.latex() == "\\dfrac{1 - t^8}{(1 - t)^4(1 - t^3)(1 - t^5)(1 - t^6)}"
	assert str(R2) == "(1 - t^8)/((1 - t)^4*(1 - t^3)*(1 - t^5)*(1 - t^6))"
	assert R2.latex() == "\\dfrac{1 - t^8}{(1 - t)^4(1 - t^3)(1 - t^5)(1 - t^6)}"


def test_Zeta_examples():
	# Pulled from Rossmann's Zeta package.
	# https://torossmann.github.io/Zeta/
	q, t, sc_0 = polygens(QQ, ('q', 't', 'sc_0'))
	R1 = -(q^2*t^2 + q*t + 1)/((q^3*t^2 - 1)*(q*t + 1)*(q*t - 1)*(t - 1))
	R2 = -1/((q^2*t^3 - 1)*(q*t - 1)*(t - 1))
	R3 = (t - 1)/(q*t - 1)
	R4 = -(q*sc_0*t - q*t^2 - sc_0*t + 1)*(t - 1)/((q^3*t^2 - 1)*(q*t - 1))
	R5 = (q^4 + q^2*t^2 - q^3 - 2*q^2*t - q*t^2 + q^2 + t^2)*(q - 1)/((q^2 + q*t + t^2)*(q - t)^3)
	R6 = -(q^3 - t)/((q - t)*q^2*(t - 1))
	R7 = -(t - 1)/((q^2*t - 1)*(q*t - 1))
	R8 = (q - t)^3/(q^3*(t - 1)^4)
	R9 = -(q^4 - t)*(q^3 - t)^2/((q^2 - t)^3*q^4*(t - 1))
	R10 = -(q^3*t + q^3 - 2*q^2*t - 2*q*t + t^2 + t)/((q*t - 1)^2*q^3*(t - 1))
	R11 = (q^6*t^6 + q^5*t^7 - q^6*t^5 - 3*q^5*t^6 - 6*q^4*t^7 + q^7*t^3 - 5*q^6*t^4 + 3*q^5*t^5 + 3*q^4*t^6 + 14*q^3*t^7 - 3*q^7*t^2 + 7*q^6*t^3 + 5*q^5*t^4 + 17*q^4*t^5 - 12*q^3*t^6 - 14*q^2*t^7 - q^7*t + 24*q^6*t^2 - 58*q^5*t^3 + 45*q^4*t^4 - 83*q^3*t^5 + 46*q^2*t^6 - 2*q*t^7 + t^8 - q^7 + 2*q^6*t - 46*q^5*t^2 + 83*q^4*t^3 - 45*q^3*t^4 + 58*q^2*t^5 - 24*q*t^6 + t^7 + 14*q^5*t + 12*q^4*t^2 - 17*q^3*t^3 - 5*q^2*t^4 - 7*q*t^5 + 3*t^6 - 14*q^4*t - 3*q^3*t^2 - 3*q^2*t^3 + 5*q*t^4 - t^5 + 6*q^3*t + 3*q^2*t^2 + q*t^3 - q^2*t - q*t^2)/((q*t - 1)*(q - t)^3*q^4*(t + 1)*(t - 1)^4)
	R12 = (q^3 + 2*q^2 - 3*q + 1)*(2*q - 1)*q^2
	R13 = -(q*t^3 - 1)/((q*t^2 - 1)*(q*t - 1)*(t + 1)*(t - 1)^2)
	assert str(brat(R1)) == "(1 + q*t + q^2*t^2)/((1 - t)*(1 - q^2*t^2)*(1 - q^3*t^2))"
	assert str(brat(R2)) == "1/((1 - t)*(1 - q*t)*(1 - q^2*t^3))"
	assert str(brat(R3)) == "(1 - t)/(1 - q*t)"
	assert str(brat(R4)) == "(1 - t - t*sc_0 + t^2*sc_0 + q*t*sc_0 - q*t^2 - q*t^2*sc_0 + q*t^3)/((1 - q*t)*(1 - q^3*t^2))"
	assert str(brat(R4).factor()) == "(1 - t)*(1 - t*sc_0 + q*t*sc_0 - q*t^2)/((1 - q*t)*(1 - q^3*t^2))"
	assert str(brat(R5, increasing_order=False)) == "(1 + q^-2*t^2 - 2*q^-1 - 2*q^-2*t - 2*q^-3*t^2 + 2*q^-2 + 2*q^-3*t + 2*q^-4*t^2 - q^-3 - q^-5*t^2)/((1 - q^-1*t)^2*(1 - q^-3*t^3))"
	assert str(brat(R5, increasing_order=False).factor()) == "q^-5*(q - 1)*(q^4 + q^2*t^2 - q^3 - 2*q^2*t - q*t^2 + q^2 + t^2)/((1 - q^-1*t)^2*(1 - q^-3*t^3))"
	assert str(brat(R5, increasing_order=False, negative_exponents=False)) == "(q^5 + q^3*t^2 - 2*q^4 - 2*q^3*t - 2*q^2*t^2 + 2*q^3 + 2*q^2*t + 2*q*t^2 - q^2 - t^2)/(q^5*(1 - q^-1*t)^2*(1 - q^-3*t^3))"
	assert str(brat(R5, increasing_order=False, negative_exponents=False).factor()) == "(q - 1)*(q^4 + q^2*t^2 - q^3 - 2*q^2*t - q*t^2 + q^2 + t^2)/(q^5*(1 - q^-1*t)^2*(1 - q^-3*t^3))"
	assert str(brat(R6, increasing_order=False)) == "(1 - q^-3*t)/((1 - q^-1*t)*(1 - t))"
	assert str(brat(R7)) == "(1 - t)/((1 - q*t)*(1 - q^2*t))"
	assert str(brat(R8, increasing_order=False)) == "(1 - 3*q^-1*t + 3*q^-2*t^2 - q^-3*t^3)/(1 - t)^4"
	assert str(brat(R9, increasing_order=False)) == "(1 - 2*q^-3*t - q^-4*t + q^-6*t^2 + 2*q^-7*t^2 - q^-10*t^3)/((1 - q^-2*t)^3*(1 - t))"
	assert str(brat(R9, increasing_order=False).factor()) == "q^-10*(q^3 - t)^2*(q^4 - t)/((1 - q^-2*t)^3*(1 - t))"
	assert str(brat(R9, increasing_order=False, negative_exponents=False).factor()) == "(q^3 - t)^2*(q^4 - t)/(q^10*(1 - q^-2*t)^3*(1 - t))"
	assert str(brat(R10, increasing_order=False)) == "(t + 1 - 2*q^-1*t - 2*q^-2*t + q^-3*t^2 + q^-3*t)/((1 - t)*(1 - q*t)^2)"
	assert str(brat(R11)) == "(q^-6*t^2 + q^-5*t - q^-6*t^3 - 3*q^-5*t^2 - 6*q^-4*t + q^-7*t^5 - 5*q^-6*t^4 + 3*q^-5*t^3 + 3*q^-4*t^2 + 14*q^-3*t - 3*q^-7*t^6 + 7*q^-6*t^5 + 5*q^-5*t^4 + 17*q^-4*t^3 - 12*q^-3*t^2 - 14*q^-2*t - q^-7*t^7 + 24*q^-6*t^6 - 58*q^-5*t^5 + 45*q^-4*t^4 - 83*q^-3*t^3 + 46*q^-2*t^2 - 2*q^-1*t + 1 - q^-7*t^8 + 2*q^-6*t^7 - 46*q^-5*t^6 + 83*q^-4*t^5 - 45*q^-3*t^4 + 58*q^-2*t^3 - 24*q^-1*t^2 + t + 14*q^-5*t^7 + 12*q^-4*t^6 - 17*q^-3*t^5 - 5*q^-2*t^4 - 7*q^-1*t^3 + 3*t^2 - 14*q^-4*t^7 - 3*q^-3*t^6 - 3*q^-2*t^5 + 5*q^-1*t^4 - t^3 + 6*q^-3*t^7 + 3*q^-2*t^6 + q^-1*t^5 - q^-2*t^7 - q^-1*t^6)/((1 - q^-1*t)^3*(1 - t)^3*(1 - t^2)*(1 - q*t))"
	assert str(brat(R12)) == "-(q^2 - 5*q^3 + 8*q^4 - 3*q^5 - 2*q^6)"
	assert str(brat(R12, increasing_order=False).factor()) == "(2*q - 1)*q^2*(q^3 + 2*q^2 - 3*q + 1)"
	assert str(brat(R13)) == "(1 - q*t^3)/((1 - t)*(1 - t^2)*(1 - q*t)*(1 - q*t^2))"
	assert brat(R1).latex() == "\\dfrac{1 + qt + q^2t^2}{(1 - t)(1 - q^2t^2)(1 - q^3t^2)}"
	assert brat(R2).latex() == "\\dfrac{1}{(1 - t)(1 - qt)(1 - q^2t^3)}"
	assert brat(R3).latex() == "\\dfrac{1 - t}{(1 - qt)}"
	assert brat(R4).latex() == "\\dfrac{1 - t - t\\mathit{sc}_0 + t^2\\mathit{sc}_0 + qt\\mathit{sc}_0 - qt^2 - qt^2\\mathit{sc}_0 + qt^3}{(1 - qt)(1 - q^3t^2)}"
	assert brat(R4).factor().latex() == "\\dfrac{(1 - t)(1 - t\\mathit{sc}_0 + qt\\mathit{sc}_0 - qt^2)}{(1 - qt)(1 - q^3t^2)}"
	assert brat(R5, increasing_order=False).latex() == "\\dfrac{1 + q^{-2}t^2 - 2q^{-1} - 2q^{-2}t - 2q^{-3}t^2 + 2q^{-2} + 2q^{-3}t + 2q^{-4}t^2 - q^{-3} - q^{-5}t^2}{(1 - q^{-1}t)^2(1 - q^{-3}t^3)}"
	assert brat(R6, increasing_order=False).latex() == "\\dfrac{1 - q^{-3}t}{(1 - q^{-1}t)(1 - t)}"
	assert brat(R7).latex() == "\\dfrac{1 - t}{(1 - qt)(1 - q^2t)}"
	assert brat(R8, increasing_order=False).latex() == "\\dfrac{1 - 3q^{-1}t + 3q^{-2}t^2 - q^{-3}t^3}{(1 - t)^4}"
	assert brat(R9, increasing_order=False).latex() == "\\dfrac{1 - 2q^{-3}t - q^{-4}t + q^{-6}t^2 + 2q^{-7}t^2 - q^{-10}t^3}{(1 - q^{-2}t)^3(1 - t)}"
	assert brat(R10, increasing_order=False).latex() == "\\dfrac{t + 1 - 2q^{-1}t - 2q^{-2}t + q^{-3}t^2 + q^{-3}t}{(1 - t)(1 - qt)^2}"
	assert brat(R11).latex() == "\\dfrac{q^{-6}t^2 + q^{-5}t - q^{-6}t^3 - 3q^{-5}t^2 - 6q^{-4}t + q^{-7}t^5 - 5q^{-6}t^4 + 3q^{-5}t^3 + 3q^{-4}t^2 + 14q^{-3}t - 3q^{-7}t^6 + 7q^{-6}t^5 + 5q^{-5}t^4 + 17q^{-4}t^3 - 12q^{-3}t^2 - 14q^{-2}t - q^{-7}t^7 + 24q^{-6}t^6 - 58q^{-5}t^5 + 45q^{-4}t^4 - 83q^{-3}t^3 + 46q^{-2}t^2 - 2q^{-1}t + 1 - q^{-7}t^8 + 2q^{-6}t^7 - 46q^{-5}t^6 + 83q^{-4}t^5 - 45q^{-3}t^4 + 58q^{-2}t^3 - 24q^{-1}t^2 + t + 14q^{-5}t^7 + 12q^{-4}t^6 - 17q^{-3}t^5 - 5q^{-2}t^4 - 7q^{-1}t^3 + 3t^2 - 14q^{-4}t^7 - 3q^{-3}t^6 - 3q^{-2}t^5 + 5q^{-1}t^4 - t^3 + 6q^{-3}t^7 + 3q^{-2}t^6 + q^{-1}t^5 - q^{-2}t^7 - q^{-1}t^6}{(1 - q^{-1}t)^3(1 - t)^3(1 - t^2)(1 - qt)}"
	assert brat(R12).latex() == "-(q^2 - 5q^3 + 8q^4 - 3q^5 - 2q^6)"
	assert brat(R13).latex() == "\\dfrac{1 - qt^3}{(1 - t)(1 - t^2)(1 - qt)(1 - qt^2)}"


def main():
	test_integers()
	test_rationals()
	test_polynomials()
	test_laurent_polynomials()
	test_previous_bugs()
	test_Zeta_examples()
	print("All tests passed!")

if __name__ == "__main__":
	main()