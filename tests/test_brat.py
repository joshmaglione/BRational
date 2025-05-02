from brational import brat
from sage.all import ZZ, QQ, polygens, var

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
	q, t = polygens(QQ, ('q', 't'))
	assert str(brat(q**2 + 2*q*t + t**2)) == "t^2 + 2*q*t + q^2"
	assert str(brat(q**2 + 2*q*t + t**2, increasing_order=False)) == "q^2 + 2*q*t + t^2"
	assert str(brat(q**2 + 2*q*t + t**2).factor()) == "(t + q)^2"
	assert str(brat(q**2 + 2*q*t + t**2, increasing_order=False).factor()) == "(q + t)^2"




def main():
	test_integers()
	test_rationals()
	test_polynomials()
	print("All tests passed!")

if __name__ == "__main__":
	main()