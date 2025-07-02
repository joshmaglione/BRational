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


def test_univariate_rational_functions():
	x = polygen(QQ, 'x')
	assert brat(1/(1 - x)).latex() == "\\dfrac{1}{1 - x}"
	assert brat(1/(2*(1 - x))).latex() == "\\dfrac{1}{2(1 - x)}"
	assert brat(1/(x*(1 - x))).latex() == "\\dfrac{x^{-1}}{1 - x}"
	assert brat(1/(x*(1 - x)), hide_monomial=False).latex() == "\\dfrac{1}{x(1 - x)}"
	assert brat(1/(2*x*(1 - x))).latex() == "\\dfrac{x^{-1}}{2(1 - x)}"
	assert brat(1/(2*x*(1 - x)), hide_monomial=False).latex() == "\\dfrac{1}{2x(1 - x)}"
	assert brat(1/(1 - x)**5).latex() == "\\dfrac{1}{(1 - x)^5}"
	assert brat(numerator=x, denominator=1 - x).latex() == "\\dfrac{x}{1 - x}"
	assert brat(numerator=x**2, denominator_signature={
		"coefficient": 8,
		"monomial": (1,),
		"factors": {
			(1,) : 2
		}
	}).latex() == "\\dfrac{x}{8(1 - x)^2}"
	assert brat(numerator=x**2, denominator_signature={
		"coefficient": 8,
		"monomial": (1,),
		"factors": {
			(1,) : 2
		}
	}, hide_monomial=False).latex() == "\\dfrac{x^2}{8x(1 - x)^2}"
	assert brat(numerator=x**2, denominator_signature={
		"coefficient": 8,
		"monomial": (1,),
		"factors": {
			(1,) : 2
		}
	}, hide_monomial=False, increasing_order=False).latex() == "\\dfrac{x^2}{8x(1 - x)^2}"
	assert brat(numerator=x/12 + x**2/4 - x**5/3 + x**8/2, denominator=1 - x).latex() == "\\dfrac{x + 3x^2 - 4x^5 + 6x^8}{12(1 - x)}"
	assert brat(numerator=x/12 + x**2/4 - x**5/3 + x**8/2, denominator_signature={
		"coefficient": 42,
		"monomial": (3,),
		"factors": {
			(1,) : 2,
			(3,) : 1
		}
	}).latex() == "\\dfrac{x^{-2} + 3x^{-1} - 4x^2 + 6x^5}{504(1 - x)^2(1 - x^3)}"
	assert brat(numerator=x/12 + x**2/4 - x**5/3 + x**8/2, denominator_signature={
		"coefficient": 42,
		"monomial": (3,),
		"factors": {
			(1,) : 2,
			(3,) : 1
		}
	}, hide_monomial=False).latex() == "\\dfrac{x + 3x^2 - 4x^5 + 6x^8}{504x^3(1 - x)^2(1 - x^3)}"
	assert brat(numerator=x/12 + x**2/4 - x**5/3 + x**8/2, denominator_signature={
		"coefficient": 42,
		"monomial": (3,),
		"factors": {
			(1,) : 2,
			(3,) : 1
		}
	}, hide_monomial=False, increasing_order=False).latex() == "\\dfrac{6x^8 - 4x^5 + 3x^2 + x}{504x^3(1 - x)^2(1 - x^3)}"
	assert brat(numerator=x/12 + x**2/4 - x**5/3 + x**8/2, denominator_signature={
		"coefficient": 42,
		"monomial": (3,),
		"factors": {
			(1,) : 2,
			(3,) : 1
		}
	}, hide_monomial=False, increasing_order=False).factor().latex() == "\\dfrac{x(6x^7 - 4x^4 + 3x + 1)}{504x^3(1 - x)^2(1 - x^3)}"



def test_multivariate_rational_functions():
	q, t = var('q t')
	assert brat(1/(1 - q**-1*t)).latex() == "\\dfrac{1}{1 - q^{-1}t}"
	assert brat(q*t/(1 - q**-1*t)).invert_variables().latex() == "\\dfrac{-q^{-2}}{1 - q^{-1}t}"
	assert brat((1/q - 1)/(t/q - 1), increasing_order=False).latex() == "\\dfrac{1 - q^{-1}}{1 - q^{-1}t}"
	assert brat(-(2*t/q - 3/q - 3*t/q**2 + 2/q**2 + t/q**3 + 1)/(t**3/q**2 - t**4/q**3 + t/q - 1)).latex() == "\\dfrac{q^{-3}t + 2q^{-2} - 3q^{-2}t - 3q^{-1} + 2q^{-1}t + 1}{(1 - q^{-1}t)(1 - q^{-2}t^3)}"
	assert brat((3*t**3/q**2 - 6*t**5/q**4 + 4*t/q - 2*t**2/q**2 - 10*t**3/q**3 + 8*t**4/q**4 + 11*t**5/q**5 - 6/q - 12*t/q**2 + 9*t**2/q**3 + 9*t**3/q**4 - 12*t**4/q**5 - 6*t**5/q**6 + 11/q**2 + 8*t/q**3 - 10*t**2/q**4 - 2*t**3/q**5 + 4*t**4/q**6 + t**5/q**7 - 6/q**3 + 3*t**2/q**5 + 1)/(t**9/q**5 - 2*t**10/q**6 + t**11/q**7 - t**6/q**3 + 2*t**7/q**4 - t**8/q**5 - t**3/q**2 + 2*t**4/q**3 - t**5/q**4 - 2*t/q + t**2/q**2 + 1)).latex() == "\\dfrac{3q^{-5}t^2 - 6q^{-3} + q^{-7}t^5 + 4q^{-6}t^4 - 2q^{-5}t^3 - 10q^{-4}t^2 + 8q^{-3}t + 11q^{-2} - 6q^{-6}t^5 - 12q^{-5}t^4 + 9q^{-4}t^3 + 9q^{-3}t^2 - 12q^{-2}t - 6q^{-1} + 11q^{-5}t^5 + 8q^{-4}t^4 - 10q^{-3}t^3 - 2q^{-2}t^2 + 4q^{-1}t + 1 - 6q^{-4}t^5 + 3q^{-2}t^3}{(1 - q^{-1}t)^2(1 - q^{-2}t^3)(1 - q^{-3}t^6)}"
	assert brat(numerator=3*q**5*t**3 - 6*q**3*t**5 + q**7 + 4*q**6*t - 2*q**5*t**2 - 10*q**4*t**3 + 8*q**3*t**4 + 11*q**2*t**5 - 6*q**6 - 12*q**5*t + 9*q**4*t**2 + 9*q**3*t**3 - 12*q**2*t**4 - 6*q*t**5 + 11*q**5 + 8*q**4*t - 10*q**3*t**2 - 2*q**2*t**3 + 4*q*t**4 + t**5 - 6*q**4 + 3*q**2*t**2, denominator_signature={
		'coefficient': 1, 
		'monomial': (7, 0), 
		'factors': {(-1, 1): 2, (-2, 3): 1, (-3, 6): 1}
	}).latex() == "\\dfrac{3q^{-5}t^2 - 6q^{-3} + q^{-7}t^5 + 4q^{-6}t^4 - 2q^{-5}t^3 - 10q^{-4}t^2 + 8q^{-3}t + 11q^{-2} - 6q^{-6}t^5 - 12q^{-5}t^4 + 9q^{-4}t^3 + 9q^{-3}t^2 - 12q^{-2}t - 6q^{-1} + 11q^{-5}t^5 + 8q^{-4}t^4 - 10q^{-3}t^3 - 2q^{-2}t^2 + 4q^{-1}t + 1 - 6q^{-4}t^5 + 3q^{-2}t^3}{(1 - q^{-1}t)^2(1 - q^{-2}t^3)(1 - q^{-3}t^6)}"
	assert brat(numerator=3*q**5*t**3 - 6*q**3*t**5 + q**7 + 4*q**6*t - 2*q**5*t**2 - 10*q**4*t**3 + 8*q**3*t**4 + 11*q**2*t**5 - 6*q**6 - 12*q**5*t + 9*q**4*t**2 + 9*q**3*t**3 - 12*q**2*t**4 - 6*q*t**5 + 11*q**5 + 8*q**4*t - 10*q**3*t**2 - 2*q**2*t**3 + 4*q*t**4 + t**5 - 6*q**4 + 3*q**2*t**2, denominator_signature={
		'coefficient': 1, 
		'monomial': (7, 0), 
		'factors': {(-1, 1): 2, (-2, 3): 1, (-3, 6): 1}
	}, hide_monomial=False).latex() == "\\dfrac{3q^2t^2 - 6q^4 + t^5 + 4qt^4 - 2q^2t^3 - 10q^3t^2 + 8q^4t + 11q^5 - 6qt^5 - 12q^2t^4 + 9q^3t^3 + 9q^4t^2 - 12q^5t - 6q^6 + 11q^2t^5 + 8q^3t^4 - 10q^4t^3 - 2q^5t^2 + 4q^6t + q^7 - 6q^3t^5 + 3q^5t^3}{q^7(1 - q^{-1}t)^2(1 - q^{-2}t^3)(1 - q^{-3}t^6)}"
	Y, T = var('Y T')
	assert brat((-Y**3*T**2 - 11*Y**3*T - 6*Y**2*T**2 - 6*Y**3 - 37*Y**2*T - 11*Y*T**2 - 11*Y**2 - 37*Y*T - 6*T**2 - 6*Y - 11*T - 1)/(T**3 - 3*T**2 + 3*T - 1)).latex() == "\\dfrac{1 + 6Y + 11T + 11Y^2 + 37TY + 6T^2 + 6Y^3 + 37TY^2 + 11T^2Y + 11TY^3 + 6T^2Y^2 + T^2Y^3}{(1 - T)^3}"
	T1, T2, T3, T4 = var('T1 T2 T3 T4')
	assert brat((Y**2*T1*T2*T3 + 3*Y*T1*T2*T3 - Y**2*T1 - Y**2*T2 - Y*T1*T2 - Y**2*T3 - Y*T1*T3 - Y*T2*T3 + 2*T1*T2*T3 + 2*Y**2 - Y*T1 - Y*T2 - T1*T2 - Y*T3 - T1*T3 - T2*T3 + 3*Y + 1)/(T1*T2*T3*T4 - T1*T2*T3 - T1*T2*T4 - T1*T3*T4 - T2*T3*T4 + T1*T2 + T1*T3 + T2*T3 + T1*T4 + T2*T4 + T3*T4 - T1 - T2 - T3 - T4 + 1)).latex() == "\\dfrac{1 + 3Y + 2Y^2 - T_3Y - T_2Y - T_1Y - T_2T_3 - T_1T_3 - T_1T_2 - T_3Y^2 - T_2Y^2 - T_1Y^2 - T_2T_3Y - T_1T_3Y - T_1T_2Y + 2T_1T_2T_3 + 3T_1T_2T_3Y + T_1T_2T_3Y^2}{(1 - T_4)(1 - T_3)(1 - T_2)(1 - T_1)}"


def test_previous_reported_bugs():
	t = var('t')
	R1 = brat((t**8 - 1)/((t**4 + t**3 + t**2 + t + 1)*(t**4 + t**2 + 1)*(t**3 - 1)*(t**2 - 1)*(t - 1)**5))
	R2 = brat((t**8 - 1)/((t**6 - 1)*(t**5 - 1)*(t**2 + t + 1)*(t - 1)**5))
	assert R1.latex() == "\\dfrac{1 - t^8}{(1 - t)^4(1 - t^3)(1 - t^5)(1 - t^6)}"
	assert R2.latex() == "\\dfrac{1 - t^8}{(1 - t)^4(1 - t^3)(1 - t^5)(1 - t^6)}"
	q, X = polygens(QQ, ('q', 'X'))
	R3 = brat(numerator=-q**2*X**2 + q, denominator=-q**6*X**3 + q**5*X**4 + q**6*X**2 - q**5*X**3 + q**4*X**2 - q**3*X**3 - q**4*X + 2*q**3*X**2 - q**2*X**3 - q**3*X + q**2*X**2 - q*X + X**2 + q - X)
	assert R3.latex() == "\\dfrac{1 - qX^2}{(1 - q^{-1}X)(1 - X)(1 - q^2X)(1 - q^3X)}"


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
	assert brat(R1).latex() == "\\dfrac{1 + qt + q^2t^2}{(1 - t)(1 - q^2t^2)(1 - q^3t^2)}"
	assert brat(R2).latex() == "\\dfrac{1}{(1 - t)(1 - qt)(1 - q^2t^3)}"
	assert brat(R3).latex() == "\\dfrac{1 - t}{1 - qt}"
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
	test_integers_latex()
	test_rationals_latex()
	test_univariate_polynomials_latex()
	test_multivariate_polynomials_latex()
	test_univariate_laurent_polynomials_latex()
	test_multivariate_laurent_polynomials_latex()
	test_univariate_rational_functions()
	test_multivariate_rational_functions()
	test_previous_reported_bugs()
	test_Zeta_examples()
	print("All tests passed!")


if __name__ == "__main__":
	main()