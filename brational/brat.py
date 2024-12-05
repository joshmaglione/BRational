
from sage.all import ZZ, SR, QQ, PolynomialRing, prod, vector, reduce, copy
from sage.all import latex as LaTeX
from .util import my_print, DEBUG

# Given a polynomial f, decide if f is a finite geometric progression. If it is
# not, raise an error. This is because we assume our rational functions can be
# written as a product of factors of the form (1 - M_i), where M_i is a
# monomial. The function returns a triple (k, r, n) where 
#	f = k(1 - r^n)/(1 - r). 
def _is_finite_gp(f):
	m = f.monomials()
	if len(m) == 1:
		return (f.monomial_coefficient(m[0]), f.parent()(1), 1)
	term = lambda k: f.monomial_coefficient(m[k])*m[k]
	r = term(0) / term(1) 		# higher degrees appear first by default
	if any(term(i) / term(i+1) != r for i in range(len(m) - 1)):
		raise ValueError("Denominator not in correct form.")
	return (term(-1), r, len(m))

# Play games and hope you turn f into an element of P.
def get_poly(f, P):
	if f in ZZ:
		return f
	if f.parent() == SR:
		try:
			return P(f.polynomial(QQ))
		except TypeError:
			raise TypeError("Numerator must be a polynomial.")
		except AttributeError:
			raise TypeError("Numerator must be a polynomial.")
	elif len(f.monomials()) > 0:
		return P(f)
	else:
		raise TypeError("Numerator must be a polynomial.")

# Takes the underlying polynomial ring R and the signature and multiplies all
# suitable factors together. Here, suitable is determined by exp_func. By
# default, everything is suitable.
def _unfold_signature(R, sig, exp_func=lambda _: True):
	varbs = R.gens()
	mon = lambda v: R(prod(x**e for x, e in zip(varbs, v)))
	if not "monomial" in sig:
		sig.update({"monomial": 1})
	return sig["monomial"]*prod(
		(1 - mon(v))**abs(e) for v, e in sig["factors"].items() if exp_func(e)
	)

# Given the polynomial ring R, the numerator N, and the denominator D, construct
# the denominator signature.
def _get_signature(R, N, D, verbose=DEBUG):
	varbs = R.gens()
	def deg(m):
		try: 
			return vector(ZZ, [m.degree(v) for v in varbs])
		except TypeError:
			return vector(ZZ, [m.degree() for _ in varbs])
	mon = lambda v: R(prod(x**e for x, e in zip(varbs, v)))
	D_factors = list(D.factor())
	gp_factors = {}
	pos_facts = R(1)
	const = D.factor().unit()
	my_print(verbose, f"Numerator:\n\t{N}")
	my_print(verbose, f"Denominator:\n\t{D_factors}")
	my_print(verbose, f"Monomial:\n\t{const}")
	while len(D_factors) > 0:
		f, e = D_factors[0]
		m_f = f.monomials()
		if len(m_f) == 2 and prod(f.coefficients()) < 0:
			my_print(verbose, f"Polynomial: {f} -- is GP", 1)
			v = tuple(deg(m_f[0]) - deg(m_f[1]))
			my_print(verbose, f"degree: {v}", 2)
			if v in gp_factors:
				gp_factors[v] += e
			else:
				gp_factors[v] = e
			if f.monomial_coefficient(m_f[1]) < 0:
				my_print(verbose, f"const: {(-1)**e}", 2)
				const *= (-1)**e
		elif len(m_f) == 1:
			my_print(verbose, f"Polynomial: {f} -- a monomial", 1)
			const *= f**e
			my_print(verbose, f"const: {const}", 2)
		else:
			my_print(verbose, f"Polynomial: {f} -- is not GP", 1)
			k, r, n = _is_finite_gp(f)
			my_print(verbose, f"data: ({k}, {r}, {n})", 2)
			r_num, r_den = R(r.numerator()), R(r.denominator())
			const *= k
			if r_num.monomial_coefficient(r_num.monomials()[0]) > 0:
				v = tuple(deg(r_num) - deg(r_den))
				v_n = tuple(n*(deg(r_num) - deg(r_den)))
				my_print(verbose, f"n-degree: {v_n}", 2)
				my_print(verbose, f"degree: {v}", 2)
				if v_n in gp_factors:
					gp_factors[v_n] += e
				else:
					gp_factors[v_n] = e
				if v in gp_factors:
					gp_factors[v] -= e
				else:
					gp_factors[v] = -e
			else:
				my_print(verbose, f"Pushing: (1 + {(-r)**n}, {e})", 2)
				D_factors.append(((r_den**n + (-r_num)**n), e))
				pos_facts *= (r_den - r_num)**e
		D_factors = D_factors[1:]
	my_print(verbose, f"Final factors: {gp_factors}", 1)
	my_print(verbose, f"Accumulated factors: {pos_facts}", 1)
	# Clean up the monomial a little bit. 
	pos_facts_cleaned = R.one()
	for n_mon, e in list(pos_facts.factor()):
		my_print(verbose, f"Polynomial: {n_mon}", 1)
		k, r, n = _is_finite_gp(n_mon)
		my_print(verbose, f"data: ({k}, {r}, {n})", 2)
		r_num, r_den = R(r.numerator()), R(r.denominator())
		if r_num.monomial_coefficient(r_num.monomials()[0]) > 0:
			v = tuple(deg(r_num) - deg(r_den))
			v_n = tuple(n*(deg(r_num) - deg(r_den)))
			if v_n in gp_factors:
				m = min(e, gp_factors[v_n])
				gp_factors[v_n] -= m
				pos_facts_cleaned *= k*(1 - mon(v_n))**(e - m)
			else:
				pos_facts_cleaned *= k*(1 - mon(v_n))**e
			if v in gp_factors:
				gp_factors[v] += e
			else:
				gp_factors[v] = e
		else:
			pos_facts_cleaned *= n_mon**e
	N_form = N*pos_facts_cleaned*_unfold_signature(
		R, {"factors": gp_factors}, lambda e: e < 0
	)
	D_form = const*_unfold_signature(
		R, {"factors": gp_factors}, lambda e: e > 0
	)
	if N_form/D_form != N/D:	# Most important check!
		my_print(verbose, "ERROR!")
		my_print(verbose, f"Expected:\n\t{N/D}")
		my_print(verbose, f"Numerator:\n\t{N_form}")
		my_print(verbose, f"Denominator:\n\t{D_form}")
		raise ValueError("Error in implementation. Contact Josh.")
	if const < 0:
		N_form = -N_form
		const = -const
	gp_factors = {v: e for v, e in gp_factors.items() if e > 0}
	return (N_form, {"monomial": const, "factors": gp_factors})

def _process_input(num, dem=None, sig=None, fix=True):
	if dem is None:
		R = num
	else:
		R = num/dem
	if R in QQ and (dem is None or dem in QQ) and (sig is None or sig["factors"] == {}):
		N, D = R.numerator(), R.denominator()
		return (QQ, N, {"monomial": D, "factors": {}})
	try:	# Not sure how best to do this. Argh!
		varbs = (R.numerator()*R.denominator()).parent().gens()
	except AttributeError and RuntimeError:
		varbs = R.variables()
	P = PolynomialRing(QQ, varbs)
	if dem is None:
		dem = _unfold_signature(P, sig)
	if fix:
		N = get_poly(num, P)
		D = get_poly(dem, P)
	else: 
		N = get_poly(R.numerator(), P)
		D = get_poly(R.denominator(), P)
	if sig is None:
		N_new, D_sig = _get_signature(P, P(N), P(D))
	else:
		D_sig = sig
		N_new = N
	return (P, N_new, D_sig)

# The length of the function name is unnecessarily long.
def _remove_unnecessary_braces_and_spaces(latex_text):
	import re
	patt_braces = re.compile(r'[\^\_]\{.\}')
	patt_spaces = re.compile(r'[0-9] [a-zA-Z0-9]')
	patt_spaces2 = re.compile(r'\} [a-zA-Z0-9]')
	def remove_braces(match):
		return f"{match.group(0)[0]}{match.group(0)[2]}"
	def remove_spaces(match):
		return match.group(0)[0] + match.group(0)[2]
	pairs = [
		(patt_braces, remove_braces), 
		(patt_spaces, remove_spaces), 
		(patt_spaces2, remove_spaces)
	]
	return reduce(lambda x, y: y[0].sub(y[1], x), pairs, latex_text)

def _format(B, latex=False, factor=False):
	if latex:
		wrap = lambda X: LaTeX(X)
	else:
		wrap = lambda X: str(X)
	if B.increasing_order:
		ORD = -1
	else:
		ORD = 1
	numer = B._n_poly
	if numer in ZZ:
		n_str = wrap(numer)
	else:
		if factor:
			factors = list(numer.factor())
			unit = numer.factor().unit()
		else:
			factors = [(numer, 1)]
			unit = 1
		n_str = ""
		for f, e in factors:
			f_str = ""
			mon_n = f.monomials()
			flip = 1
			for i, m in enumerate(mon_n[::ORD]):
				c = f.monomial_coefficient(m)
				if i == 0:
					if c < 0:
						flip = -1
						unit = (-1)**e*unit
					f_str += wrap(flip*c*m)
				else: 
					if flip*c > 0:
						f_str += " + " + wrap(flip*f.monomial_coefficient(m)*m)
					else:
						f_str += " - " + wrap(-flip*f.monomial_coefficient(m)*m)
			if e > 1:
				if latex:
					f_str = f"({f_str})^{{{e}}}"
				else:
					f_str = f"({f_str})^{e}*"
			elif len(factors) > 1 or unit != 1:
				if latex:
					f_str = f"({f_str})"
				else:
					f_str = f"({f_str})*"
			n_str += f_str
		if n_str[-1] == "*":
			n_str = n_str[:-1]
		if unit != 1:
			if unit == -1:
				n_str = "-" + n_str
			else:
				if latex:
					n_str = f"{wrap(unit)}{n_str}"
				else:
					n_str = f"{wrap(unit)}*{n_str}"
		if len(factors) == 1 and unit == 1 and factors[0][1] == 1 and len(factors[0][0].monomials()) > 1 and not latex and B.denominator() != 1:
			n_str = f"({n_str})"
	varbs = B._ring.gens()
	mon = lambda v: prod(x**e for x, e in zip(varbs, v))
	d_str = ""
	if B._d_sig["monomial"] != 1:
		d_str += wrap(B._d_sig["monomial"])
		if len(B._d_sig["factors"]) > 0 and not latex:
			d_str += "*"
	gp_list = list(B._d_sig["factors"].items())
	gp_list.sort(key=lambda x: sum(x[0]))
	for v, e in gp_list:
		if e == 1:
			d_str += f"(1 - {wrap(mon(v))})"
		else:
			if latex:
				d_str += f"(1 - {wrap(mon(v))})^{{{e}}}"
			else:
				d_str += f"(1 - {wrap(mon(v))})^{e}"
		if not latex and gp_list[-1] != (v, e):
			d_str += "*"
	if not latex and len(gp_list) > 1:
		d_str = "(" + d_str + ")"
	return (n_str, d_str)

def _format_polynomial_for_align(POLY, COLWIDTH, first=0):
	def split_polynomial(poly):
		terms = []
		i = 0
		while i < len(poly):
			start = i
			if poly[i] in '+-':
				i += 1
			while i < len(poly) and poly[i] not in '+-':
				i += 1
			terms.append(poly[start:i].strip())
		return terms
	terms = split_polynomial(POLY)
	output_lines = []
	current_line = ""
	capped = lambda curr, t, extra: len(curr) + len(t) > COLWIDTH - extra
	for term in terms:
		if (len(output_lines) == 0 and capped(current_line, term, first)) or (len(output_lines) > 0 and capped(current_line, term, 0)):
			if current_line:
				output_lines.append(current_line)
			current_line = term
		else:
			if current_line:
				current_line += " " + term
			else:
				current_line = term
	if current_line:
		output_lines.append(current_line)
	output_string = " \\\\ \n\t&\\quad ".join(output_lines)
	return output_string

# The main class of BRational.
class brat:
	r"""
	A class for beautifully formatted rational functions.

	- ``rational_expression``: the rational function (default: ``None``),

	- ``numerator``: the numerator polynomial of the rational function (default: ``None``),

	- ``denominator``: the denominator polynomial of the rational function (default: ``None``),

	- ``denominator_signature``: the dictionary of data for the denominator (default: ``None``),

	- ``fix_denominator``: whether to keep the given denominator fixed (default: ``True``),

	- ``increasing_order``: whether to display polynomials in increasing degree (default: ``True``).
	"""

	def __init__(self, 
			rational_expression=None, 
			numerator=None, 
			denominator=None,
			denominator_signature=None,
			fix_denominator=True,
			increasing_order=True
		):
		if not denominator is None and denominator == 0:
			raise ValueError("Denominator cannot be zero.")
		if not rational_expression is None:
			try:
				N = rational_expression.numerator()
				D = rational_expression.denominator()
			except AttributeError:
				raise TypeError("Input must be a rational function.")
		else: 
			if numerator is None or (denominator is None and denominator_signature is None):
				raise ValueError("Must provide a numerator and denominator.")
			N = numerator
			if denominator is None:
				if not isinstance(denominator_signature, dict):
					raise TypeError("Denominator signature must be a dictionary.")
				if not "factors" in denominator_signature:
					denominator_signature = {"factors": denominator_signature}
				D = None
			else:
				D = denominator
		T = _process_input(
			N, 
			dem=D, 
			sig=denominator_signature, 
			fix=fix_denominator
		)
		self._ring = T[0]			# Parent ring for rational function
		self._n_poly = T[1]			# Numerator polynomial
		self._d_sig = T[2]			# Denominator with form \prod_i (1 - M_i)
		self.increasing_order = increasing_order
		self._factor = False

	def __repr__(self) -> str:
		N, D = _format(self, factor=self._factor)
		if D == "":
			return f"{N}"
		return f"{N}/{D}"
	
	def __add__(self, other):
		if isinstance(other, brat):
			S = other.rational_function()
		else:
			S = other
		R = self.rational_function()
		Q = R + S
		try:
			return brat(Q)
		except ValueError:
			return Q
		
	def __sub__(self, other):
		if isinstance(other, brat):
			S = other.rational_function()
		else:
			S = other
		R = self.rational_function()
		Q = R - S
		try:
			return brat(Q)
		except ValueError:
			return Q
		
	def __mul__(self, other):
		if isinstance(other, brat):
			S = other.rational_function()
		else:
			S = other
		R = self.rational_function()
		Q = R * S
		try:
			return brat(Q)
		except ValueError:
			return Q
		
	def __truediv__(self, other):
		if isinstance(other, brat):
			S = other.rational_function()
		else:
			S = other
		R = self.rational_function()
		Q = R / S
		try:
			return brat(Q)
		except ValueError:
			return Q
		
	def __pow__(self, other):
		R = self.rational_function()
		Q = R**other
		try:
			return brat(Q)
		except ValueError:
			return Q
		
	def __eq__(self, other):
		if isinstance(other, brat):
			S = other.rational_function()
		else:
			S = other
		R = self.rational_function()
		return R == S
	
	def __ne__(self, other):
		return not self == other
	
	def denominator(self):
		r"""Returns the polynomial in the denominator of the rational function. This is not necessarily reduced.

		EXAMPLE::

			sage: x, y = polygens(QQ, 'x,y')
			sage: f = br.brat(
				numerator=1 + x*y^2,
				denominator=1 - x^2*y^4
			)
			sage: f
			(1 + x*y^2)/(1 - x^2*y^4)
			sage: f.denominator()
			-x^2*y^4 + 1
		"""
		return _unfold_signature(self._ring, self._d_sig)

	def denominator_signature(self):
		r"""Returns the dictionary signature for the denominator. The format of the dictionary is as follows. The keys are 

		- ``monomial``: rational number,
		- ``factors``: dictionary with keys given by vectors and values in the positive integers. 
		
		EXAMPLE::

			sage: x, y, z = polygens(ZZ, 'x,y,z')
			sage: F = br.brat(1/(3*(1 - x^2*y)*(1 - y^4)^3*(1 - x*y*z)*(1 - x^2)^5))
			sage: F
			1/(3*(1 - x^2)^5*(1 - x*y*z)*(1 - x^2*y)*(1 - y^4)^3)
			sage: F.denominator_signature()
			{'monomial': 3,
			'factors': {(2, 0, 0): 5, (0, 4, 0): 3, (1, 1, 1): 1, (2, 1, 0): 1}}
		"""
		return self._d_sig

	def factor(self):
		r"""Returns a new ``brat`` object with the numerator polynomial factored.

		"""
		B = copy(self)
		B._factor = True
		return B

	def fix_denominator(self, expression=None, signature=None):
		r"""Given a polynomial, or data equivalent to a polynomial, returns a new ``brat``, equal to the original, whose denominator is the given polynomial.

		- ``expression``: the polynomial expression. Default: ``None``.
		- ``signature``: the signature for the polynomial expression. See the denominator signature method. Default: ``None``.

		EXAMPLE::

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
		"""
		if expression:
			if expression == 0:
				raise ValueError("Expression cannot be zero.")
			D_new = brat(1/expression)
			return self.fix_denominator(signature=D_new.denominator_signature())
		if signature is None:
			raise ValueError("Must provide an expression or signature.")
		if not isinstance(signature, dict):
			raise TypeError("Signature must be a dictionary.")
		if not "factors" in signature:
			signature = {"factors": signature}
		expr = _unfold_signature(self._ring, signature)
		new_numer = self._ring(self._n_poly*expr/self.denominator())
		if not new_numer.denominator() in ZZ:
			raise ValueError("New denominator must be a multiple of the old one.")
		return brat(
			numerator=new_numer, 
			denominator_signature=signature,
			fix_denominator=True,
			increasing_order=self.increasing_order
		)

	def invert_variables(self):
		r"""Returns the corresponding ``brat`` after inverting all of the variables and then rewriting the rational function so that all exponents are non-negative. 
		
		EXAMPLE::

			sage: T = var('T')
			sage: E = br.brat(
				numerator=1 + 26*T + 66*T^2 + 26*T^3 + T^4,
				denominator_signature={(1,): 5}
			)
			sage: E
			(1 + 26*T + 66*T^2 + 26*T^3 + T^4)/(1 - T)^5
			sage: E.invert_variables()
			(-T - 26*T^2 - 66*T^3 - 26*T^4 - T^5)/(1 - T)^5
		"""
		varbs = self._ring.gens()
		mon = lambda v: self._ring(prod(x**e for x, e in zip(varbs, v)))
		factor = prod(
			mon(v)**e*(-1)**e for v, e in self._d_sig["factors"].items()
		)
		N = self._n_poly.subs({x: x**-1 for x in varbs})*factor
		if N.denominator() in ZZ:
			return brat(
				numerator=self._ring(N), 
				denominator_signature=self._d_sig, 
				increasing_order=self.increasing_order
			)
		return N/self.denominator()

	def latex(self, factor=False, split=False):
		r"""Returns a string that formats the ``brat` `in LaTeX in the ``\dfrac{...}{...}`` format.

		Additional argument:

		- ``factor``: factor the numerator polynomial. Default: ``False``.
		- ``split``: if true, returns a pair of strings formatted in LaTeX: the first is the numerator and the second is the denominator. Default: ``False``.

		EXAMPLE::

			sage: t = var('t')
			sage: F = br.brat(
				numerator=1 + 2*t^2 + 4*t^4 + 4*t^6 + 2*t^8 + t^10,
				denominator=prod(1 - t^i for i in range(1, 6))
			)
			sage: F
			(1 + 2*t^2 + 4*t^4 + 4*t^6 + 2*t^8 + t^10)/((1 - t)*(1 - t^2)*(1 - t^3)*(1 - t^4)*(1 - t^5))
			sage: F.latex()
			'\\dfrac{1 + 2t^2 + 4t^4 + 4t^6 + 2t^8 + t^{10}}{(1 - t)(1 - t^2)(1 - t^3)(1 - t^4)(1 - t^5)}'
			sage: F.latex(split=True)
			('1 + 2t^2 + 4t^4 + 4t^6 + 2t^8 + t^{10}',
			'(1 - t)(1 - t^2)(1 - t^3)(1 - t^4)(1 - t^5)')
		"""
		N, D = _format(self, latex=True, factor=factor)
		N_clean = _remove_unnecessary_braces_and_spaces(N)
		D_clean = _remove_unnecessary_braces_and_spaces(D)
		if split:
			return (f"{N_clean}", f"{D_clean}")
		return f"\\dfrac{{{N_clean}}}{{{D_clean}}}"
	
	def numerator(self):
			r"""Returns the polynomial in the numerator of the rational function. This is not necessarily reduced.

			EXAMPLE::

				sage: x, y = polygens(QQ, 'x,y')
				sage: f = br.brat(
					numerator=1 + x*y^2,
					denominator=1 - x^2*y^4
				)
				sage: f
				(1 + x*y^2)/(1 - x^2*y^4)
				sage: f.numerator()
				x*y^2 + 1
			"""
			return self._n_poly
		
	def rational_function(self):
		r"""Returns the reduced rational function. The underlying type of this object is not a ``brat``.

		EXAMPLE::

			sage: x, y = polygens(QQ, 'x,y')
			sage: f = br.brat(
				numerator=1 + x*y^2,
				denominator=1 - x^2*y^4
			)
			sage: f
			(1 + x*y^2)/(1 - x^2*y^4)
			sage: f.rational_function()
			1/(-x*y^2 + 1) 
		"""
		return self._n_poly / self.denominator()
	
	def subs(self, S:dict):
		r"""Given a dictionary of the desired substitutions, return the new ``brat`` obtained by performing the substitutions. 

		This works in the same as the ``subs`` method for rational functions in SageMath. 

		EXAMPLE::

			sage: Y, T = polygens(QQ, 'Y,T')
			sage: C = br.brat(
				numerator=1 + 3*Y + 2*Y^2 + (2 + 3*Y + Y^2)*T,
				denominator_signature={(0,1): 2}
			)
			sage: C
			(1 + 2*T + 3*Y + 3*Y*T + 2*Y^2 + Y^2*T)/(1 - T)^2
			sage: C.subs({Y: 0})
			(1 + 2*T)/(1 - T)^2
		"""
		R = self.rational_function()
		Q = R.subs(S)
		try:
			return brat(Q)
		except ValueError:
			return Q

	def variables(self):
		r"""Returns the polynomial variables used.

		EXAMPLE::

			sage: x, y, z = var('x y z')
			sage: f = (1 + x^2*y^2*z^2)/((1 - x*y)*(1 - x*z)*(1 - y*z))
			sage: F = br.brat(f)
			sage: F
			(1 + x^2*y^2*z^2)/((1 - y*z)*(1 - x*z)*(1 - x*y))
			sage: F.variables()
			(x, y, z)
		"""
		return self._ring.gens()
	
	def write_latex(
			self,
			filename=None,
			just_numerator=False,
			just_denominator=False,
			align=False,
			factor=False,
			line_width=100,
			function_name=None,
			save_message=True
		):
		r"""Writes the ``brat`` object to a file formatted in LaTeX. The (default) output is a displayed equation (using ``\[`` and ``\]``) of the ``brat``. There are many parameters to change the format of the output.

		- ``filename``: the string for the output filename. Default: ``None``, which will output a timestamp name of the form ``%Y-%m-%d_%H-%M-%S.tex``.
		- ``just_numerator``: write just the numerator. Default: ``False``.
		- ``just_denominator``: write just the denominator. Default: ``False``.
		- ``align``: format using the ``align*`` environment. This is especially useful for long polynomials. Default: ``False``.
		- ``factor``: factor the numerator polynomial. Default: ``False``.
		- ``line_width``: determines the line width in characters for each line of the ``align*`` environment. Only used when ``align`` is set to ``True``. Default: ``120``.
		- ``function_name``: turns the expression to an equation by displaying the function name. Default: ``None``.
		- ``save_message``: turns on the save message at the end. Default: ``True``.

		EXAMPLES::

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
		"""
		from datetime import datetime
		if filename is None:
			filename = datetime.now().strftime('%Y-%m-%d_%H-%M-%S.tex')
		if just_numerator and just_denominator:
			raise ValueError("'just_numerator' and 'just_denominator' cannot both be True.")
		if line_width < 60:
			raise ValueError("line width must be at least 60.")
		if just_numerator:
			func = self.latex(split=True, factor=factor)[0]
		elif just_denominator:
			func = self.latex(split=True, factor=factor)[1]
		else:
			func = self.latex(factor=factor)
			align = False
		if not function_name is None:
			if align:
				function_name = f"{function_name} &= "
			else:
				function_name = f"{function_name} = "
		else:
			function_name = ""
		if align:
			func = _format_polynomial_for_align(func, line_width, first=len(function_name))
			output = f"\\begin{{align*}}\n\t{function_name}{func}\n\\end{{align*}}"
		else:
			output = f"\\[\n\t{function_name}{func}\n\\]"
		with open(filename, "w") as f:
			f.write(output)
		if save_message:
			print(f"File saved as {filename}.")
		return None