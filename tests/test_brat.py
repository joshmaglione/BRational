import sys
import os
from sage.all import ZZ, QQ, polygens, var, polygen

sys.path.append(os.getcwd())
from brational import brat


def test_integers():
	assert str(brat(int(1))) == "1"
	assert str(brat(int(0))) == "0"
	assert str(brat(int(-1))) == "-1"
	assert str(brat(ZZ(1))) == "1"
	assert str(brat(ZZ(0))) == "0"
	assert str(brat(ZZ(-1))) == "-1"
	assert str(brat(ZZ(4))) == "4"
	assert str(brat(ZZ(-12))) == "-12"
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


def test_univariate_polynomials():
	x = var('x')
	assert str(brat(x + 1)) == "1 + x"
	assert str(brat(x**2 - 1 - x)) == "-(1 + x - x^2)"
	assert str(brat(1 + 2*x + x*x)) == "1 + 2*x + x^2"
	assert str(brat(1 + 2*x + x*x).factor()) == "(1 + x)^2"
	assert str(brat(3 + x - x**4, increasing_order=False)) == "-(x^4 - x - 3)"
	assert str(brat(x + QQ(1/2))) == "(1 + 2*x)/2"
	assert str(brat((x**2 - 1 - x)/4)) == "-(1 + x - x^2)/4"
	assert str(brat((1 + 2*x + x*x)/6)) == "(1 + 2*x + x^2)/6"
	assert str(brat((1 + 2*x + x*x)/6).factor()) == "(1 + x)^2/6"
	assert str(brat(3 + x - x**4/2, increasing_order=False)) == "-(x^4 - 2*x - 6)/2"
	assert str(brat(numerator=x + x**9 - x**12, denominator=x)) == "1 + x^8 - x^11"


def test_multivariate_polynomials():
	q, t = polygens(QQ, ('q', 't'))
	assert str(brat(q**2 + 2*q*t + t**2)) == "t^2 + 2*q*t + q^2"
	assert str(brat(q**2 + 2*q*t + t**2, increasing_order=False)) == "q^2 + 2*q*t + t^2"
	assert str(brat((q**2 + 2*q*t + t**2)/60)) == "(t^2 + 2*q*t + q^2)/60"
	assert str(brat((q**2 + 2*q*t + t**2)/60, increasing_order=False)) == "(q^2 + 2*q*t + t^2)/60"
	assert str(brat(q**2 + 2*q*t + t**2).factor()) == "(t + q)^2"
	assert str(brat(q**2 + 2*q*t + t**2, increasing_order=False).factor()) == "(q + t)^2"
	assert str(brat((q**2 + 2*q*t + t**2)/6).factor()) == "(t + q)^2/6"
	assert str(brat((q**2 + 2*q*t + t**2)/6, increasing_order=False).factor()) == "(q + t)^2/6"


def test_univariate_laurent_polynomials():
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
	assert str(brat(x + 1/x, hide_monomial=False)) == "(1 + x^2)/x"
	assert str(brat((1 + 2*x + x**2)/x**6, hide_monomial=False)) == "(1 + 2*x + x^2)/x^6"
	assert str(brat((1 + 2*x + x**2)/x**6, hide_monomial=False).factor()) == "(1 + x)^2/x^6"
	assert str(brat(x + 1/x, increasing_order=False, hide_monomial=False)) == "(x^2 + 1)/x"
	assert str(brat((1 + 2*x + x**2)/x**6, increasing_order=False, hide_monomial=False)) == "(x^2 + 2*x + 1)/x^6"
	assert str(brat((1 + 2*x + x**2)/x**6, increasing_order=False, hide_monomial=False).factor()) == "(x + 1)^2/x^6"
	assert str(brat(numerator=1, denominator=x**32, hide_monomial=False)) == "1/x^32"
	assert str(brat(numerator=1, denominator=x**32, hide_monomial=False).factor()) == "1/x^32"
	assert str(brat(numerator=(1 + x)*(1 + x**3 - x**5), denominator_signature={
		"coefficient": 2,
		"monomial": (32,),
		"factors": {},
	}, hide_monomial=False)) == "(1 + x + x^3 + x^4 - x^5 - x^6)/(2*x^32)"
	assert str(brat(numerator=(1 + x)*(1 + x**3 - x**5), denominator_signature={
		"coefficient": 2,
		"monomial": (32,),
		"factors": {},
	}, hide_monomial=False).factor()) == "(1 + x)*(1 + x^3 - x^5)/(2*x^32)"


def test_multivariate_laurent_polynomials():
	q, t = polygens(QQ, ('q', 't'))
	assert str(brat(t + q**-1)) == "q^-1 + t"
	assert str(brat(t + q**-1, increasing_order=False)) == "t + q^-1"
	assert str(brat(t + q**-1, hide_monomial=False)) == "(1 + q*t)/q"
	assert str(brat((1 + q*t - t**2)/q**3)) == "q^-3 - q^-3*t^2 + q^-2*t"
	assert str(brat((1 + q*t - t**2)/q**3, increasing_order=False)) == "q^-2*t - q^-3*t^2 + q^-3"
	assert str(brat((1 + q*t - t**2)/q**3, hide_monomial=False)) == "(1 - t^2 + q*t)/q^3"
	assert str(brat(q**-5*t**-10)) == "q^-5*t^-10"
	assert str(brat(12*q**-5*t**-10)) == "12*q^-5*t^-10"
	assert str(brat(12**-1*(q**-5*t**-10+q**-3*t**-12))) == "(q^-5*t^-10 + q^-3*t^-12)/12"
	assert str(brat(12**-1*(q**-5*t**-10+q**-3*t**-12), hide_monomial=False)) == "(t^2 + q^2)/(12*q^5*t^12)"
	assert str(brat(q**-5*t**-10, hide_monomial=False)) == "1/(q^5*t^10)"
	assert str(brat((q + 1)**2*t**-5*(q + t))) == "t^-4 + q*t^-5 + 2*q*t^-4 + 2*q^2*t^-5 + q^2*t^-4 + q^3*t^-5"
	assert str(brat((q + 1)**2*t**-5*(q + t), hide_monomial=False)) == "(t + q + 2*q*t + 2*q^2 + q^2*t + q^3)/t^5"
	assert str(brat((q + 1)**2*t**-5*(q + t)).factor()) == "t^-5*(t + q)*(1 + q)^2"
	assert str(brat((q + 1)**2*t**-5*(q + t), hide_monomial=False).factor()) == "(t + q)*(1 + q)^2/t^5"
	assert str(brat(numerator=q*t, denominator_signature={
		"coefficient": 4,
		"monomial": (23, 29),
		"factors": {},
	})) == "q^-22*t^-28/4"
	assert str(brat(numerator=q*t, denominator_signature={
		"coefficient": 4,
		"monomial": (23, 29),
		"factors": {},
	}, hide_monomial=False)) == "q*t/(4*q^23*t^29)"
	assert str(brat(numerator=q*t, denominator_signature={
		"coefficient": 4,
		"monomial": (23, 29),
		"factors": {},
	}, hide_monomial=False, fix_denominator=False)) == "1/(4*q^22*t^28)"


def test_univariate_rational_functions():
	x = polygen(QQ, 'x')
	assert str(brat(1/(1 - x))) == "1/(1 - x)"
	assert str(brat(1/(1 - x)**5)) == "1/(1 - x)^5"
	assert str(brat(numerator=x, denominator=1 - x)) == "x/(1 - x)"
	assert str(brat(numerator=x**2, denominator_signature={
		"coefficient": 8,
		"monomial": (1,),
		"factors": {
			(1,) : 2
		}
	})) == "x/(8*(1 - x)^2)"
	assert str(brat(numerator=x**2, denominator_signature={
		"coefficient": 8,
		"monomial": (1,),
		"factors": {
			(1,) : 2
		}
	}, hide_monomial=False)) == "x^2/(8*x*(1 - x)^2)"
	assert str(brat(numerator=x**2, denominator_signature={
		"coefficient": 8,
		"monomial": (1,),
		"factors": {
			(1,) : 2
		}
	}, hide_monomial=False, increasing_order=False)) == "x^2/(8*x*(1 - x)^2)"
	assert str(brat(numerator=x/12 + x**2/4 - x**5/3 + x**8/2, denominator=1 - x)) == "(x + 3*x^2 - 4*x^5 + 6*x^8)/(12*(1 - x))"
	assert str(brat(numerator=x/12 + x**2/4 - x**5/3 + x**8/2, denominator_signature={
		"coefficient": 42,
		"monomial": (3,),
		"factors": {
			(1,) : 2,
			(3,) : 1
		}
	})) == "(x^-2 + 3*x^-1 - 4*x^2 + 6*x^5)/(504*(1 - x)^2*(1 - x^3))"
	assert str(brat(numerator=x/12 + x**2/4 - x**5/3 + x**8/2, denominator_signature={
		"coefficient": 42,
		"monomial": (3,),
		"factors": {
			(1,) : 2,
			(3,) : 1
		}
	}, hide_monomial=False)) == "(x + 3*x^2 - 4*x^5 + 6*x^8)/(504*x^3*(1 - x)^2*(1 - x^3))"
	assert str(brat(numerator=x/12 + x**2/4 - x**5/3 + x**8/2, denominator_signature={
		"coefficient": 42,
		"monomial": (3,),
		"factors": {
			(1,) : 2,
			(3,) : 1
		}
	}, hide_monomial=False, increasing_order=False)) == "(6*x^8 - 4*x^5 + 3*x^2 + x)/(504*x^3*(1 - x)^2*(1 - x^3))"
	assert str(brat(numerator=x/12 + x**2/4 - x**5/3 + x**8/2, denominator_signature={
		"coefficient": 42,
		"monomial": (3,),
		"factors": {
			(1,) : 2,
			(3,) : 1
		}
	}, hide_monomial=False, increasing_order=False).factor()) == "x*(6*x^7 - 4*x^4 + 3*x + 1)/(504*x^3*(1 - x)^2*(1 - x^3))"


def test_multivariate_rational_functions():
	q, t = var('q t')
	assert str(brat(1/(1 - q**-1*t))) == "1/(1 - q^-1*t)"
	assert str(brat(q*t/(1 - q**-1*t)).invert_variables()) == "-q^-2/(1 - q^-1*t)"
	assert str(brat((1/q - 1)/(t/q - 1), increasing_order=False)) == "(1 - q^-1)/(1 - q^-1*t)"
	assert str(brat(-(2*t/q - 3/q - 3*t/q**2 + 2/q**2 + t/q**3 + 1)/(t**3/q**2 - t**4/q**3 + t/q - 1))) == "(q^-3*t + 2*q^-2 - 3*q^-2*t - 3*q^-1 + 2*q^-1*t + 1)/((1 - q^-1*t)*(1 - q^-2*t^3))"
	assert str(brat((3*t**3/q**2 - 6*t**5/q**4 + 4*t/q - 2*t**2/q**2 - 10*t**3/q**3 + 8*t**4/q**4 + 11*t**5/q**5 - 6/q - 12*t/q**2 + 9*t**2/q**3 + 9*t**3/q**4 - 12*t**4/q**5 - 6*t**5/q**6 + 11/q**2 + 8*t/q**3 - 10*t**2/q**4 - 2*t**3/q**5 + 4*t**4/q**6 + t**5/q**7 - 6/q**3 + 3*t**2/q**5 + 1)/(t**9/q**5 - 2*t**10/q**6 + t**11/q**7 - t**6/q**3 + 2*t**7/q**4 - t**8/q**5 - t**3/q**2 + 2*t**4/q**3 - t**5/q**4 - 2*t/q + t**2/q**2 + 1))) == "(3*q^-5*t^2 - 6*q^-3 + q^-7*t^5 + 4*q^-6*t^4 - 2*q^-5*t^3 - 10*q^-4*t^2 + 8*q^-3*t + 11*q^-2 - 6*q^-6*t^5 - 12*q^-5*t^4 + 9*q^-4*t^3 + 9*q^-3*t^2 - 12*q^-2*t - 6*q^-1 + 11*q^-5*t^5 + 8*q^-4*t^4 - 10*q^-3*t^3 - 2*q^-2*t^2 + 4*q^-1*t + 1 - 6*q^-4*t^5 + 3*q^-2*t^3)/((1 - q^-1*t)^2*(1 - q^-2*t^3)*(1 - q^-3*t^6))"
	assert str(brat(numerator=3*q**5*t**3 - 6*q**3*t**5 + q**7 + 4*q**6*t - 2*q**5*t**2 - 10*q**4*t**3 + 8*q**3*t**4 + 11*q**2*t**5 - 6*q**6 - 12*q**5*t + 9*q**4*t**2 + 9*q**3*t**3 - 12*q**2*t**4 - 6*q*t**5 + 11*q**5 + 8*q**4*t - 10*q**3*t**2 - 2*q**2*t**3 + 4*q*t**4 + t**5 - 6*q**4 + 3*q**2*t**2, denominator_signature={
		'coefficient': 1, 
		'monomial': (7, 0), 
		'factors': {(-1, 1): 2, (-2, 3): 1, (-3, 6): 1}
	})) == "(3*q^-5*t^2 - 6*q^-3 + q^-7*t^5 + 4*q^-6*t^4 - 2*q^-5*t^3 - 10*q^-4*t^2 + 8*q^-3*t + 11*q^-2 - 6*q^-6*t^5 - 12*q^-5*t^4 + 9*q^-4*t^3 + 9*q^-3*t^2 - 12*q^-2*t - 6*q^-1 + 11*q^-5*t^5 + 8*q^-4*t^4 - 10*q^-3*t^3 - 2*q^-2*t^2 + 4*q^-1*t + 1 - 6*q^-4*t^5 + 3*q^-2*t^3)/((1 - q^-1*t)^2*(1 - q^-2*t^3)*(1 - q^-3*t^6))"
	Y, T = var('Y T')
	assert str(brat((-Y**3*T**2 - 11*Y**3*T - 6*Y**2*T**2 - 6*Y**3 - 37*Y**2*T - 11*Y*T**2 - 11*Y**2 - 37*Y*T - 6*T**2 - 6*Y - 11*T - 1)/(T**3 - 3*T**2 + 3*T - 1))) == "(1 + 6*Y + 11*T + 11*Y^2 + 37*T*Y + 6*T^2 + 6*Y^3 + 37*T*Y^2 + 11*T^2*Y + 11*T*Y^3 + 6*T^2*Y^2 + T^2*Y^3)/(1 - T)^3"
	T1, T2, T3, T4 = var('T1 T2 T3 T4')
	assert str(brat((Y**2*T1*T2*T3 + 3*Y*T1*T2*T3 - Y**2*T1 - Y**2*T2 - Y*T1*T2 - Y**2*T3 - Y*T1*T3 - Y*T2*T3 + 2*T1*T2*T3 + 2*Y**2 - Y*T1 - Y*T2 - T1*T2 - Y*T3 - T1*T3 - T2*T3 + 3*Y + 1)/(T1*T2*T3*T4 - T1*T2*T3 - T1*T2*T4 - T1*T3*T4 - T2*T3*T4 + T1*T2 + T1*T3 + T2*T3 + T1*T4 + T2*T4 + T3*T4 - T1 - T2 - T3 - T4 + 1))) == "(1 + 3*Y + 2*Y^2 - T3*Y - T2*Y - T1*Y - T2*T3 - T1*T3 - T1*T2 - T3*Y^2 - T2*Y^2 - T1*Y^2 - T2*T3*Y - T1*T3*Y - T1*T2*Y + 2*T1*T2*T3 + 3*T1*T2*T3*Y + T1*T2*T3*Y^2)/((1 - T4)*(1 - T3)*(1 - T2)*(1 - T1))"


def test_previous_reported_bugs():
	t = var('t')
	R1 = brat((t**8 - 1)/((t**4 + t**3 + t**2 + t + 1)*(t**4 + t**2 + 1)*(t**3 - 1)*(t**2 - 1)*(t - 1)**5))
	R2 = brat((t**8 - 1)/((t**6 - 1)*(t**5 - 1)*(t**2 + t + 1)*(t - 1)**5))
	assert str(R1) == "(1 - t^8)/((1 - t)^4*(1 - t^3)*(1 - t^5)*(1 - t^6))"
	assert str(R2) == "(1 - t^8)/((1 - t)^4*(1 - t^3)*(1 - t^5)*(1 - t^6))"
	q, X = polygens(QQ, ('q', 'X'))
	R3 = brat(numerator=-q**2*X**2 + q, denominator=-q**6*X**3 + q**5*X**4 + q**6*X**2 - q**5*X**3 + q**4*X**2 - q**3*X**3 - q**4*X + 2*q**3*X**2 - q**2*X**3 - q**3*X + q**2*X**2 - q*X + X**2 + q - X)
	assert str(R3) == "(1 - q*X^2)/((1 - q^-1*X)*(1 - X)*(1 - q^2*X)*(1 - q^3*X))"


def test_Zeta_examples():
	# Pulled from Rossmann's Zeta package.
	# https://torossmann.github.io/Zeta/
	q, t, sc_0 = polygens(QQ, ('q', 't', 'sc_0'))
	R1 = -(q**2*t**2 + q*t + 1)/((q**3*t**2 - 1)*(q*t + 1)*(q*t - 1)*(t - 1))
	R2 = -1/((q**2*t**3 - 1)*(q*t - 1)*(t - 1))
	R3 = (t - 1)/(q*t - 1)
	R4 = -(q*sc_0*t - q*t**2 - sc_0*t + 1)*(t - 1)/((q**3*t**2 - 1)*(q*t - 1))
	R5 = (q**4 + q**2*t**2 - q**3 - 2*q**2*t - q*t**2 + q**2 + t**2)*(q - 1)/((q**2 + q*t + t**2)*(q - t)**3)
	R6 = -(q**3 - t)/((q - t)*q**2*(t - 1))
	R7 = -(t - 1)/((q**2*t - 1)*(q*t - 1))
	R8 = (q - t)**3/(q**3*(t - 1)**4)
	R9 = -(q**4 - t)*(q**3 - t)**2/((q**2 - t)**3*q**4*(t - 1))
	R10 = -(q**3*t + q**3 - 2*q**2*t - 2*q*t + t**2 + t)/((q*t - 1)**2*q**3*(t - 1))
	R11 = (q**6*t**6 + q**5*t**7 - q**6*t**5 - 3*q**5*t**6 - 6*q**4*t**7 + q**7*t**3 - 5*q**6*t**4 + 3*q**5*t**5 + 3*q**4*t**6 + 14*q**3*t**7 - 3*q**7*t**2 + 7*q**6*t**3 + 5*q**5*t**4 + 17*q**4*t**5 - 12*q**3*t**6 - 14*q**2*t**7 - q**7*t + 24*q**6*t**2 - 58*q**5*t**3 + 45*q**4*t**4 - 83*q**3*t**5 + 46*q**2*t**6 - 2*q*t**7 + t**8 - q**7 + 2*q**6*t - 46*q**5*t**2 + 83*q**4*t**3 - 45*q**3*t**4 + 58*q**2*t**5 - 24*q*t**6 + t**7 + 14*q**5*t + 12*q**4*t**2 - 17*q**3*t**3 - 5*q**2*t**4 - 7*q*t**5 + 3*t**6 - 14*q**4*t - 3*q**3*t**2 - 3*q**2*t**3 + 5*q*t**4 - t**5 + 6*q**3*t + 3*q**2*t**2 + q*t**3 - q**2*t - q*t**2)/((q*t - 1)*(q - t)**3*q**4*(t + 1)*(t - 1)**4)
	R12 = (q**3 + 2*q**2 - 3*q + 1)*(2*q - 1)*q**2
	R13 = -(q*t**3 - 1)/((q*t**2 - 1)*(q*t - 1)*(t + 1)*(t - 1)**2)
	assert str(brat(R1)) == "(1 + q*t + q^2*t^2)/((1 - t)*(1 - q^2*t^2)*(1 - q^3*t^2))"
	assert str(brat(R2)) == "1/((1 - t)*(1 - q*t)*(1 - q^2*t^3))"
	assert str(brat(R3)) == "(1 - t)/(1 - q*t)"
	assert str(brat(R4)) == "(1 - t - t*sc_0 + t^2*sc_0 + q*t*sc_0 - q*t^2 - q*t^2*sc_0 + q*t^3)/((1 - q*t)*(1 - q^3*t^2))"
	assert str(brat(R4).factor()) == "(1 - t)*(1 - t*sc_0 + q*t*sc_0 - q*t^2)/((1 - q*t)*(1 - q^3*t^2))"
	assert str(brat(R5, increasing_order=False)) == "(1 + q^-2*t^2 - 2*q^-1 - 2*q^-2*t - 2*q^-3*t^2 + 2*q^-2 + 2*q^-3*t + 2*q^-4*t^2 - q^-3 - q^-5*t^2)/((1 - q^-1*t)^2*(1 - q^-3*t^3))"
	assert str(brat(R5, increasing_order=False).factor()) == "q^-5*(q - 1)*(q^4 + q^2*t^2 - q^3 - 2*q^2*t - q*t^2 + q^2 + t^2)/((1 - q^-1*t)^2*(1 - q^-3*t^3))"
	assert str(brat(R5, increasing_order=False, hide_monomial=False)) == "(q^5 + q^3*t^2 - 2*q^4 - 2*q^3*t - 2*q^2*t^2 + 2*q^3 + 2*q^2*t + 2*q*t^2 - q^2 - t^2)/(q^5*(1 - q^-1*t)^2*(1 - q^-3*t^3))"
	assert str(brat(R5, increasing_order=False, hide_monomial=False).factor()) == "(q - 1)*(q^4 + q^2*t^2 - q^3 - 2*q^2*t - q*t^2 + q^2 + t^2)/(q^5*(1 - q^-1*t)^2*(1 - q^-3*t^3))"
	assert str(brat(R6, increasing_order=False)) == "(1 - q^-3*t)/((1 - q^-1*t)*(1 - t))"
	assert str(brat(R7)) == "(1 - t)/((1 - q*t)*(1 - q^2*t))"
	assert str(brat(R8, increasing_order=False)) == "(1 - 3*q^-1*t + 3*q^-2*t^2 - q^-3*t^3)/(1 - t)^4"
	assert str(brat(R9, increasing_order=False)) == "(1 - 2*q^-3*t - q^-4*t + q^-6*t^2 + 2*q^-7*t^2 - q^-10*t^3)/((1 - q^-2*t)^3*(1 - t))"
	assert str(brat(R9, increasing_order=False).factor()) == "q^-10*(q^3 - t)^2*(q^4 - t)/((1 - q^-2*t)^3*(1 - t))"
	assert str(brat(R9, increasing_order=False, hide_monomial=False).factor()) == "(q^3 - t)^2*(q^4 - t)/(q^10*(1 - q^-2*t)^3*(1 - t))"
	assert str(brat(R10, increasing_order=False)) == "(t + 1 - 2*q^-1*t - 2*q^-2*t + q^-3*t^2 + q^-3*t)/((1 - t)*(1 - q*t)^2)"
	assert str(brat(R11)) == "(q^-6*t^2 + q^-5*t - q^-6*t^3 - 3*q^-5*t^2 - 6*q^-4*t + q^-7*t^5 - 5*q^-6*t^4 + 3*q^-5*t^3 + 3*q^-4*t^2 + 14*q^-3*t - 3*q^-7*t^6 + 7*q^-6*t^5 + 5*q^-5*t^4 + 17*q^-4*t^3 - 12*q^-3*t^2 - 14*q^-2*t - q^-7*t^7 + 24*q^-6*t^6 - 58*q^-5*t^5 + 45*q^-4*t^4 - 83*q^-3*t^3 + 46*q^-2*t^2 - 2*q^-1*t + 1 - q^-7*t^8 + 2*q^-6*t^7 - 46*q^-5*t^6 + 83*q^-4*t^5 - 45*q^-3*t^4 + 58*q^-2*t^3 - 24*q^-1*t^2 + t + 14*q^-5*t^7 + 12*q^-4*t^6 - 17*q^-3*t^5 - 5*q^-2*t^4 - 7*q^-1*t^3 + 3*t^2 - 14*q^-4*t^7 - 3*q^-3*t^6 - 3*q^-2*t^5 + 5*q^-1*t^4 - t^3 + 6*q^-3*t^7 + 3*q^-2*t^6 + q^-1*t^5 - q^-2*t^7 - q^-1*t^6)/((1 - q^-1*t)^3*(1 - t)^3*(1 - t^2)*(1 - q*t))"
	assert str(brat(R12)) == "-(q^2 - 5*q^3 + 8*q^4 - 3*q^5 - 2*q^6)"
	assert str(brat(R12, increasing_order=False).factor()) == "(2*q - 1)*q^2*(q^3 + 2*q^2 - 3*q + 1)"
	assert str(brat(R13)) == "(1 - q*t^3)/((1 - t)*(1 - t^2)*(1 - q*t)*(1 - q*t^2))"


def test_CICO():
	q, t = var('q t')
	C1 = -(q**8*t**2 - q**9 - 4*q**6*t**3 + q**5*t**4 + 4*q**7*t - 2*q**6*t**2 + 3*q**5*t**3 + 2*q**6*t - 10*q**5*t**2 + 10*q**4*t**3 - 2*q**3*t**4 - 3*q**4*t**2 + 2*q**3*t**3 - 4*q**2*t**4 - q**4*t + 4*q**3*t**2 + t**5 - q*t**3)/((q**2 - t)*(q*t - 1)*(q - t)*q**6*(t - 1)**3) #404
	C2 = (q**9*t**12 - 2*q**9*t**11 - q**8*t**12 - q**7*t**13 - 5*q**6*t**14 + q**5*t**15 + q**11*t**8 - 13*q**9*t**10 + 6*q**8*t**11 + 7*q**7*t**12 + 7*q**6*t**13 + 18*q**5*t**14 - q**4*t**15 + q**12*t**6 - q**11*t**7 - 19*q**10*t**8 + 69*q**9*t**9 - 18*q**8*t**10 + 7*q**7*t**11 + 27*q**6*t**12 - 89*q**5*t**13 + q**4*t**14 - 10*q**3*t**15 + q**12*t**5 - 13*q**11*t**6 - 2*q**10*t**7 + 143*q**9*t**8 - 309*q**8*t**9 + 80*q**7*t**10 + 49*q**6*t**11 - 181*q**5*t**12 + 243*q**4*t**13 - 44*q**3*t**14 + 22*q**2*t**15 + 7*q**12*t**4 - 31*q**11*t**5 + 145*q**10*t**6 - 301*q**9*t**7 - 29*q**8*t**8 + 427*q**7*t**9 - 123*q**6*t**10 + 109*q**5*t**11 + 42*q**4*t**12 - 145*q**3*t**13 - 7*q**2*t**14 - 5*q*t**15 - t**16 + 3*q**12*t**3 - 92*q**11*t**4 + 353*q**10*t**5 - 876*q**9*t**6 + 1481*q**8*t**7 - 498*q**7*t**8 - 896*q**6*t**9 + 940*q**5*t**10 - 945*q**4*t**11 + 465*q**3*t**12 - 67*q**2*t**13 + 34*q*t**14 - t**15 + 7*q**12*t**2 - 45*q**11*t**3 + 395*q**10*t**4 - 1065*q**9*t**5 + 1675*q**8*t**6 - 1996*q**7*t**7 + 1996*q**5*t**9 - 1675*q**4*t**10 + 1065*q**3*t**11 - 395*q**2*t**12 + 45*q*t**13 - 7*t**14 + q**12*t - 34*q**11*t**2 + 67*q**10*t**3 - 465*q**9*t**4 + 945*q**8*t**5 - 940*q**7*t**6 + 896*q**6*t**7 + 498*q**5*t**8 - 1481*q**4*t**9 + 876*q**3*t**10 - 353*q**2*t**11 + 92*q*t**12 - 3*t**13 + q**12 + 5*q**11*t + 7*q**10*t**2 + 145*q**9*t**3 - 42*q**8*t**4 - 109*q**7*t**5 + 123*q**6*t**6 - 427*q**5*t**7 + 29*q**4*t**8 + 301*q**3*t**9 - 145*q**2*t**10 + 31*q*t**11 - 7*t**12 - 22*q**10*t + 44*q**9*t**2 - 243*q**8*t**3 + 181*q**7*t**4 - 49*q**6*t**5 - 80*q**5*t**6 + 309*q**4*t**7 - 143*q**3*t**8 + 2*q**2*t**9 + 13*q*t**10 - t**11 + 10*q**9*t - q**8*t**2 + 89*q**7*t**3 - 27*q**6*t**4 - 7*q**5*t**5 + 18*q**4*t**6 - 69*q**3*t**7 + 19*q**2*t**8 + q*t**9 - t**10 + q**8*t - 18*q**7*t**2 - 7*q**6*t**3 - 7*q**5*t**4 - 6*q**4*t**5 + 13*q**3*t**6 - q*t**8 - q**7*t + 5*q**6*t**2 + q**5*t**3 + q**4*t**4 + 2*q**3*t**5 - q**3*t**4)/((q + t)*(q - t)**4*q**7*(t + 1)**4*(t - 1)**8) # 503
	C3 = (q**15 + 6*q**11*t**2 + 20*q**11*t - 14*q**10*t**2 - 56*q**10*t + 7*q**9*t**2 + 49*q**9*t + 15*q**7*t**3 - 15*q**8*t - 49*q**6*t**3 - 7*q**6*t**2 + 56*q**5*t**3 + 14*q**5*t**2 - 20*q**4*t**3 - 6*q**4*t**2 - t**4)/((q**4 - t)*(q**2 + t)*(q**2 - t)*q**7*(t - 1)**2) #853
	# TESTS
	assert C1 == (q**-8*t**3 - q**-9*t**5 - 4*q**-6*t**2 + q**-5*t + 4*q**-7*t**4 - 2*q**-6*t**3 + 3*q**-5*t**2 + 2*q**-6*t**4 - 10*q**-5*t**3 + 10*q**-4*t**2 - 2*q**-3*t - 3*q**-4*t**3 + 2*q**-3*t**2 - 4*q**-2*t - q**-4*t**4 + 4*q**-3*t**3 + 1 - q**-1*t**2)/((1 - q**-2*t)*(1 - q**-1*t)*(1 - t)**3*(1 - q*t))
	assert str(brat(C1)) == "(q^-8*t^3 - q^-9*t^5 - 4*q^-6*t^2 + q^-5*t + 4*q^-7*t^4 - 2*q^-6*t^3 + 3*q^-5*t^2 + 2*q^-6*t^4 - 10*q^-5*t^3 + 10*q^-4*t^2 - 2*q^-3*t - 3*q^-4*t^3 + 2*q^-3*t^2 - 4*q^-2*t - q^-4*t^4 + 4*q^-3*t^3 + 1 - q^-1*t^2)/((1 - q^-2*t)*(1 - q^-1*t)*(1 - t)^3*(1 - q*t))"
	assert str(brat(C2)) == "-(q^-9*t^4 - 2*q^-9*t^5 - q^-8*t^4 - q^-7*t^3 - 5*q^-6*t^2 + q^-5*t + q^-11*t^8 - 13*q^-9*t^6 + 6*q^-8*t^5 + 7*q^-7*t^4 + 7*q^-6*t^3 + 18*q^-5*t^2 - q^-4*t + q^-12*t^10 - q^-11*t^9 - 19*q^-10*t^8 + 69*q^-9*t^7 - 18*q^-8*t^6 + 7*q^-7*t^5 + 27*q^-6*t^4 - 89*q^-5*t^3 + q^-4*t^2 - 10*q^-3*t + q^-12*t^11 - 13*q^-11*t^10 - 2*q^-10*t^9 + 143*q^-9*t^8 - 309*q^-8*t^7 + 80*q^-7*t^6 + 49*q^-6*t^5 - 181*q^-5*t^4 + 243*q^-4*t^3 - 44*q^-3*t^2 + 22*q^-2*t + 7*q^-12*t^12 - 31*q^-11*t^11 + 145*q^-10*t^10 - 301*q^-9*t^9 - 29*q^-8*t^8 + 427*q^-7*t^7 - 123*q^-6*t^6 + 109*q^-5*t^5 + 42*q^-4*t^4 - 145*q^-3*t^3 - 7*q^-2*t^2 - 5*q^-1*t - 1 + 3*q^-12*t^13 - 92*q^-11*t^12 + 353*q^-10*t^11 - 876*q^-9*t^10 + 1481*q^-8*t^9 - 498*q^-7*t^8 - 896*q^-6*t^7 + 940*q^-5*t^6 - 945*q^-4*t^5 + 465*q^-3*t^4 - 67*q^-2*t^3 + 34*q^-1*t^2 - t + 7*q^-12*t^14 - 45*q^-11*t^13 + 395*q^-10*t^12 - 1065*q^-9*t^11 + 1675*q^-8*t^10 - 1996*q^-7*t^9 + 1996*q^-5*t^7 - 1675*q^-4*t^6 + 1065*q^-3*t^5 - 395*q^-2*t^4 + 45*q^-1*t^3 - 7*t^2 + q^-12*t^15 - 34*q^-11*t^14 + 67*q^-10*t^13 - 465*q^-9*t^12 + 945*q^-8*t^11 - 940*q^-7*t^10 + 896*q^-6*t^9 + 498*q^-5*t^8 - 1481*q^-4*t^7 + 876*q^-3*t^6 - 353*q^-2*t^5 + 92*q^-1*t^4 - 3*t^3 + q^-12*t^16 + 5*q^-11*t^15 + 7*q^-10*t^14 + 145*q^-9*t^13 - 42*q^-8*t^12 - 109*q^-7*t^11 + 123*q^-6*t^10 - 427*q^-5*t^9 + 29*q^-4*t^8 + 301*q^-3*t^7 - 145*q^-2*t^6 + 31*q^-1*t^5 - 7*t^4 - 22*q^-10*t^15 + 44*q^-9*t^14 - 243*q^-8*t^13 + 181*q^-7*t^12 - 49*q^-6*t^11 - 80*q^-5*t^10 + 309*q^-4*t^9 - 143*q^-3*t^8 + 2*q^-2*t^7 + 13*q^-1*t^6 - t^5 + 10*q^-9*t^15 - q^-8*t^14 + 89*q^-7*t^13 - 27*q^-6*t^12 - 7*q^-5*t^11 + 18*q^-4*t^10 - 69*q^-3*t^9 + 19*q^-2*t^8 + q^-1*t^7 - t^6 + q^-8*t^15 - 18*q^-7*t^14 - 7*q^-6*t^13 - 7*q^-5*t^12 - 6*q^-4*t^11 + 13*q^-3*t^10 - q^-1*t^8 - q^-7*t^15 + 5*q^-6*t^14 + q^-5*t^13 + q^-4*t^12 + 2*q^-3*t^11 - q^-3*t^12)/((1 - q^-2*t^2)*(1 - q^-1*t)^3*(1 - t)^4*(1 - t^2)^4)"
	assert C2 == -(q**-9*t**4 - 2*q**-9*t**5 - q**-8*t**4 - q**-7*t**3 - 5*q**-6*t**2 + q**-5*t + q**-11*t**8 - 13*q**-9*t**6 + 6*q**-8*t**5 + 7*q**-7*t**4 + 7*q**-6*t**3 + 18*q**-5*t**2 - q**-4*t + q**-12*t**10 - q**-11*t**9 - 19*q**-10*t**8 + 69*q**-9*t**7 - 18*q**-8*t**6 + 7*q**-7*t**5 + 27*q**-6*t**4 - 89*q**-5*t**3 + q**-4*t**2 - 10*q**-3*t + q**-12*t**11 - 13*q**-11*t**10 - 2*q**-10*t**9 + 143*q**-9*t**8 - 309*q**-8*t**7 + 80*q**-7*t**6 + 49*q**-6*t**5 - 181*q**-5*t**4 + 243*q**-4*t**3 - 44*q**-3*t**2 + 22*q**-2*t + 7*q**-12*t**12 - 31*q**-11*t**11 + 145*q**-10*t**10 - 301*q**-9*t**9 - 29*q**-8*t**8 + 427*q**-7*t**7 - 123*q**-6*t**6 + 109*q**-5*t**5 + 42*q**-4*t**4 - 145*q**-3*t**3 - 7*q**-2*t**2 - 5*q**-1*t - 1 + 3*q**-12*t**13 - 92*q**-11*t**12 + 353*q**-10*t**11 - 876*q**-9*t**10 + 1481*q**-8*t**9 - 498*q**-7*t**8 - 896*q**-6*t**7 + 940*q**-5*t**6 - 945*q**-4*t**5 + 465*q**-3*t**4 - 67*q**-2*t**3 + 34*q**-1*t**2 - t + 7*q**-12*t**14 - 45*q**-11*t**13 + 395*q**-10*t**12 - 1065*q**-9*t**11 + 1675*q**-8*t**10 - 1996*q**-7*t**9 + 1996*q**-5*t**7 - 1675*q**-4*t**6 + 1065*q**-3*t**5 - 395*q**-2*t**4 + 45*q**-1*t**3 - 7*t**2 + q**-12*t**15 - 34*q**-11*t**14 + 67*q**-10*t**13 - 465*q**-9*t**12 + 945*q**-8*t**11 - 940*q**-7*t**10 + 896*q**-6*t**9 + 498*q**-5*t**8 - 1481*q**-4*t**7 + 876*q**-3*t**6 - 353*q**-2*t**5 + 92*q**-1*t**4 - 3*t**3 + q**-12*t**16 + 5*q**-11*t**15 + 7*q**-10*t**14 + 145*q**-9*t**13 - 42*q**-8*t**12 - 109*q**-7*t**11 + 123*q**-6*t**10 - 427*q**-5*t**9 + 29*q**-4*t**8 + 301*q**-3*t**7 - 145*q**-2*t**6 + 31*q**-1*t**5 - 7*t**4 - 22*q**-10*t**15 + 44*q**-9*t**14 - 243*q**-8*t**13 + 181*q**-7*t**12 - 49*q**-6*t**11 - 80*q**-5*t**10 + 309*q**-4*t**9 - 143*q**-3*t**8 + 2*q**-2*t**7 + 13*q**-1*t**6 - t**5 + 10*q**-9*t**15 - q**-8*t**14 + 89*q**-7*t**13 - 27*q**-6*t**12 - 7*q**-5*t**11 + 18*q**-4*t**10 - 69*q**-3*t**9 + 19*q**-2*t**8 + q**-1*t**7 - t**6 + q**-8*t**15 - 18*q**-7*t**14 - 7*q**-6*t**13 - 7*q**-5*t**12 - 6*q**-4*t**11 + 13*q**-3*t**10 - q**-1*t**8 - q**-7*t**15 + 5*q**-6*t**14 + q**-5*t**13 + q**-4*t**12 + 2*q**-3*t**11 - q**-3*t**12)/((1 - q**-2*t**2)*(1 - q**-1*t)**3*(1 - t)**4*(1 - t**2)**4)
	assert str(brat(C3, increasing_order=False)) == "(1 + 6*q^-4*t^2 + 20*q^-4*t - 14*q^-5*t^2 - 56*q^-5*t + 7*q^-6*t^2 + 49*q^-6*t + 15*q^-8*t^3 - 15*q^-7*t - 49*q^-9*t^3 - 7*q^-9*t^2 + 56*q^-10*t^3 + 14*q^-10*t^2 - 20*q^-11*t^3 - 6*q^-11*t^2 - q^-15*t^4)/((1 - q^-4*t)*(1 - q^-4*t^2)*(1 - t)^2)"
	assert C3 == (1 + 6*q**-4*t**2 + 20*q**-4*t - 14*q**-5*t**2 - 56*q**-5*t + 7*q**-6*t**2 + 49*q**-6*t + 15*q**-8*t**3 - 15*q**-7*t - 49*q**-9*t**3 - 7*q**-9*t**2 + 56*q**-10*t**3 + 14*q**-10*t**2 - 20*q**-11*t**3 - 6*q**-11*t**2 - q**-15*t**4)/((1 - q**-4*t)*(1 - q**-4*t**2)*(1 - t)**2)


def main():
	test_integers()
	test_rationals()
	test_univariate_polynomials()
	test_multivariate_polynomials()
	test_univariate_laurent_polynomials()
	test_multivariate_laurent_polynomials()
	test_univariate_rational_functions()
	test_previous_reported_bugs()
	test_Zeta_examples()
	test_CICO()
	print("All tests passed!")


if __name__ == "__main__":
	main()