import sys
import os
from sage.all import QQ, polygens, var, PolynomialRing, prod

sys.path.append(os.getcwd())
from brational import brat


def test_introduction():
    x, y = var('x y')
    f = (1 + x*y + x**2*y**2)/((1 - x)*(1 - y))
    assert str(f) == "(x^2*y^2 + x*y + 1)/((x - 1)*(y - 1))"
    F = brat(f)
    s = str(F)
    assert s == "(1 + x*y + x^2*y^2)/((1 - y)*(1 - x))" or s == "(1 + x*y + x^2*y^2)/((1 - x)*(1 - y))"


def test_prescribed_denominator_I():
    t = polygens(QQ, 't')[0]
    g = (1 + 4*t + 6*t**2 + 4*t**3 + t**4)/((1 - t)*(1 - t**2)*(1 - t**3)*(1 - t**4))
    G = brat(g)
    s = str(G)
    assert s == "(1 + 2*t - 2*t^3 - t^4)/((1 - t)^3*(1 - t^3)*(1 - t^4))"
    G2 = brat(numerator=1 + 4*t + 6*t**2 + 4*t**3 + t**4, denominator=(1 - t)*(1 - t**2)*(1 - t**3)*(1 - t**4))
    assert str(G2) == "(1 + 4*t + 6*t^2 + 4*t^3 + t^4)/((1 - t)*(1 - t^2)*(1 - t^3)*(1 - t^4))"
    G3 = brat(numerator=1 + 4*t + 6*t**2 + 4*t**3 + t**4, denominator=(1 - t)*(1 - t**2)*(1 - t**3)*(1 - t**4), fix_denominator=False)
    assert str(G3) == "(1 + 2*t - 2*t^3 - t^4)/((1 - t)^3*(1 - t^3)*(1 - t^4))"


def test_prescribed_denominator_II():
    T = polygens(QQ, 'T')[0]
    P = brat((1 + 6*T + 11*T**2 + 6*T**3)/(1 - T**4))
    assert str(P) == "(1 + 5*T + 5*T^2 - 5*T^3 - 6*T^4)/((1 - T)*(1 - T^4))"
    P2 = brat(numerator=1 + 6*T + 11*T**2 + 6*T**3, denominator=(1 - T)**4)
    assert str(P2) == "(1 + 6*T + 11*T^2 + 6*T^3)/(1 - T)^4"
    P3 = brat(numerator=1 + 6*T + 11*T**2 + 6*T**3, denominator=(1 - T)**4, increasing_order=False)
    assert str(P3) == "(6*T^3 + 11*T^2 + 6*T + 1)/(1 - T)^4"


def test_denominator_signature():
    R = PolynomialRing(QQ, 'X1,X2,X3')
    d_sig = {
        "coefficient": 8,
        "monomial": (0, 0, 0),
        "factors": {
            (1, 0, 0): 1,
            (0, 1, 0): 3,
            (1, 1, 1): 4,
            (1, 1, 2): 1
        }
    }
    H = brat(numerator=R(1), denominator_signature=d_sig)
    assert str(H) == "1/(8*(1 - X1)*(1 - X2)^3*(1 - X1*X2*X3)^4*(1 - X1*X2*X3^2))"


def test_negative_exponents_I():
    q, t = var('q t')
    Z2 = (1 - 3*q**-1 + 2*q**-2 + 2*q**-1*t - 3*q**-2*t + q**-3*t)/((1 - q**-1*t)*(1 - q**-2*t**3))
    Z2_brat = brat(Z2)
    assert str(Z2_brat) == "(q^-3*t + 2*q^-2 - 3*q^-2*t - 3*q^-1 + 2*q^-1*t + 1)/((1 - q^-1*t)*(1 - q^-2*t^3))"
    Z2_brat_dec = brat(Z2, increasing_order=False)
    assert str(Z2_brat_dec) == "(1 + 2*q^-1*t - 3*q^-1 - 3*q^-2*t + 2*q^-2 + q^-3*t)/((1 - q^-1*t)*(1 - q^-2*t^3))"


def test_negative_exponents_II():
    q, t = var('q t')
    W_minus = (q**3 - t)/(q**3*(1 - t)*(1 - q*t))
    W_brat = brat(W_minus)
    s = str(W_brat)
    assert s == "-(q^-3*t - 1)/((1 - t)*(1 - q*t))" or s == "(1 - q^-3*t)/((1 - t)*(1 - q*t))"
    W_brat_dec = brat(W_minus, increasing_order=False)
    assert str(W_brat_dec) == "(1 - q^-3*t)/((1 - t)*(1 - q*t))"


def test_change_denominator():
	x = polygens(QQ, 'x')[0]
	h = (1 + x**3)*(1 + x**4)*(1 + x**5)/((1 - x)*(1 - x**2)*(1 - x**3)**2*(1 - x**4)*(1 - x**5))
	assert str(h) == "(x^10 - 2*x^9 + 3*x^8 - 3*x^7 + 4*x^6 - 4*x^5 + 4*x^4 - 3*x^3 + 3*x^2 - 2*x + 1)/(x^16 - 3*x^15 + 4*x^14 - 6*x^13 + 9*x^12 - 10*x^11 + 12*x^10 - 13*x^9 + 12*x^8 - 13*x^7 + 12*x^6 - 10*x^5 + 9*x^4 - 6*x^3 + 4*x^2 - 3*x + 1)"
	H = brat(h)
	assert str(H) == "(1 - 2*x + 2*x^2 - x^3 + x^4 - x^5 + x^7 - x^8 + x^9 - 2*x^10 + 2*x^11 - x^12)/((1 - x)^3*(1 - x^3)^2*(1 - x^4)*(1 - x^5))"
	H2 = H.change_denominator(
		(1 - x) * (1 - x**2) * (1 - x**3)**2 * (1 - x**4) * (1 - x**5)
	)
	assert str(H2) == "(1 + x^3 + x^4 + x^5 + x^7 + x^8 + x^9 + x^12)/((1 - x)*(1 - x^2)*(1 - x^3)^2*(1 - x^4)*(1 - x^5))"
	H3 = H.change_denominator(
		signature={
			"coefficient": 1,
			"monomial": (0,), 
			"factors": {
				(1,): 1, (2,): 1, (3,): 2, (4,): 1, (5,): 1
			}
		}
	)
	assert str(H3) == "(1 + x^3 + x^4 + x^5 + x^7 + x^8 + x^9 + x^12)/((1 - x)*(1 - x^2)*(1 - x^3)^2*(1 - x^4)*(1 - x^5))"



def test_denominator_method():
    x, y = polygens(QQ, 'x,y')
    f = brat(numerator=1 + x*y**2, denominator=1 - x**2*y**4)
    assert str(f) == "(1 + x*y^2)/(1 - x^2*y^4)"
    assert str(f.denominator()) == "1 - x^2*y^4"


def test_denominator_signature_method():
    d_sig = {
		"coefficient": 3,
		"monomial": (1, 3, 0),
		"factors": {
			(2, 1, 0): 1, 
			(0, 4, 0): 3, 
			(1, 1, 1): 1, 
			(2, 0, 0): 5,
		},
	}
    x, y, z = polygens(QQ, 'x,y,z')
    F = brat(1/(3*x*y**3*(1 - x**2*y)*(1 - y**4)**3*(1 - x*y*z)*(1 - x**2)**5))
    assert str(F) == "x^-1*y^-3/(3*(1 - x^2)^5*(1 - x*y*z)*(1 - x^2*y)*(1 - y^4)^3)"
    d = F.denominator_signature()
    assert d["coefficient"] == 3
    assert d["monomial"] == (1, 3, 0)
    assert d["factors"] == {(2, 0, 0): 5, (0, 4, 0): 3, (1, 1, 1): 1, (2, 1, 0): 1}


def test_increasing_order():
    t = polygens(QQ, 't')[0]
    h = brat(t**3 - 6*t**2 + 11*t - 6)
    assert str(h) == "-(6 - 11*t + 6*t^2 - t^3)"
    h.increasing_order = False
    assert str(h) == "t^3 - 6*t^2 + 11*t - 6"


def test_invert_variables():
    T = var('T')
    E = brat(numerator=1 + 26*T + 66*T**2 + 26*T**3 + T**4, denominator_signature={"coefficient": 1, "monomial": (0,), "factors": {(1,): 5}})
    assert str(E) == "(1 + 26*T + 66*T^2 + 26*T^3 + T^4)/(1 - T)^5"
    E_inv = E.invert_variables()
    assert str(E_inv) == "-(T + 26*T^2 + 66*T^3 + 26*T^4 + T^5)/(1 - T)^5"
    assert str(E.invert_variables()/E) == "-T"
    assert str(E.invert_variables(ratio=True)) == "-T"


def test_latex():
    t = var('t')
    F = brat(numerator=1 + 2*t**2 + 4*t**4 + 4*t**6 + 2*t**8 + t**10, denominator=prod(1 - t**i for i in range(1, 6)))
    assert str(F) == "(1 + 2*t^2 + 4*t^4 + 4*t^6 + 2*t^8 + t^10)/((1 - t)*(1 - t^2)*(1 - t^3)*(1 - t^4)*(1 - t^5))"
    assert F.latex() == '\\dfrac{1 + 2t^2 + 4t^4 + 4t^6 + 2t^8 + t^{10}}{(1 - t)(1 - t^2)(1 - t^3)(1 - t^4)(1 - t^5)}'
    assert F.latex(split=True)[0] == '1 + 2t^2 + 4t^4 + 4t^6 + 2t^8 + t^{10}'
    assert F.latex(split=True)[1] == '(1 - t)(1 - t^2)(1 - t^3)(1 - t^4)(1 - t^5)'


def test_numerator_method():
    x, y = polygens(QQ, 'x,y')
    f = brat(numerator=1 + x*y**2, denominator=1 - x**2*y**4)
    assert str(f) == "(1 + x*y^2)/(1 - x^2*y^4)"
    assert str(f.numerator()) == "1 + x*y^2"


def test_rational_function():
    x, y = polygens(QQ, 'x,y')
    f = brat(numerator=1 + x*y**2, denominator=1 - x**2*y**4)
    assert str(f) == "(1 + x*y^2)/(1 - x^2*y^4)"
    assert str(f.rational_function()) == "1/(-x*y^2 + 1)"


def test_subs():
    Y, T = polygens(QQ, 'Y,T')
    C = brat(numerator=1 + 3*Y + 2*Y**2 + (2 + 3*Y + Y**2)*T, denominator=(1 - T)**2)
    assert str(C) == "(1 + 2*T + 3*Y + 3*Y*T + 2*Y^2 + Y^2*T)/(1 - T)^2"
    assert str(C.subs({Y: 0})) == "(1 + 2*T)/(1 - T)^2"
    assert str(C.subs({T: T - 1})) == "(Y^2*T + Y^2 + 3*Y*T + 2*T - 1)/(T^2 - 4*T + 4)"


def test_variables():
    x, y, z = var('x y z')
    f = (1 + x**2*y**2*z**2)/((1 - x*y)*(1 - x*z)*(1 - y*z))
    F = brat(f)
    assert str(F) == "(1 + x^2*y^2*z^2)/((1 - y*z)*(1 - x*z)*(1 - x*y))"
    varbs = F.variables()
    assert str(varbs) == "(x, y, z)"


def main():
	test_introduction()
	test_prescribed_denominator_I()
	test_prescribed_denominator_II()
	test_denominator_signature()
	test_negative_exponents_I()
	test_negative_exponents_II()
	test_change_denominator()
	test_denominator_method()
	test_denominator_signature_method()
	test_increasing_order()
	test_invert_variables()
	test_latex()
	test_numerator_method()
	test_rational_function()
	test_subs()
	test_variables()
	print("All tests passed!")


if __name__ == "__main__":
	main()