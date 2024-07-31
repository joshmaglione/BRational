
from sage.all import ZZ, SR, QQ, PolynomialRing, prod, vector
from sage.all import latex as LaTeX
from .util import my_print

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
		raise ValueError("Denominator must be a product of the form: monomial*(1 - monomial).")
	return (term(-1), r, len(m))

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

def _unfold_signature(R, sig, exp_func=lambda e: True):
	varbs = R.gens()
	mon = lambda v: R(prod(x**e for x, e in zip(varbs, v)))
	if not "monomial" in sig:
		sig.update({"monomial": 1})
	return sig["monomial"]*prod(
		(1 - mon(v))**abs(e) for v, e in sig["factors"].items() if exp_func(e)
	)

def _get_signature(R, N, D, verbose=False):
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
		k, r, n = _is_finite_gp(n_mon)
		r_num, r_den = R(r.numerator()), R(r.denominator())
		if r_num.monomial_coefficient(r_num.monomials()[0]) > 0:
			v = tuple(deg(r_num) - deg(r_den))
			v_n = tuple(n*(deg(r_num) - deg(r_den)))
			if v_n in gp_factors:
				m = min(e, gp_factors[v_n])
				gp_factors[v_n] -= m
				pos_facts_cleaned *= k*(1 - mon(v_n))**(e - m)
			if v in gp_factors:
				gp_factors[v] += e
			else:
				gp_factors[v] = e
	N_form = N*pos_facts_cleaned*_unfold_signature(
		R, {"factors": gp_factors}, lambda e: e < 0
	)
	D_form = const*_unfold_signature(
		R, {"factors": gp_factors}, lambda e: e > 0
	)
	if N_form/D_form != N/D:
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

def _remove_unnecessary_braces_and_spaces(latex_text):
	import re
	patt_braces = re.compile(r'\^\{.\}')
	patt_spaces = re.compile(r'[0-9] [a-zA-Z0-9]')
	def remove_braces(match):
		return f"^{match.group(0)[2]}"
	def remove_spaces(match):
		return match.group(0)[0] + match.group(0)[2]
	return patt_spaces.sub(
		remove_spaces, 
		patt_braces.sub(
			remove_braces, 
			latex_text
		)
	)

def _format(B, latex=False):
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
		n_wrap = False
	else:
		mon_n = numer.monomials()
		n_wrap = len(mon_n) > 1
		n_str = ""
		for i, m in enumerate(mon_n[::ORD]):
			c = numer.monomial_coefficient(m)
			if i == 0:
				n_str += wrap(c*m)
				if not n_wrap:
					n_wrap = not c in ZZ
			else: 
				if c > 0:
					n_str += " + " + wrap(numer.monomial_coefficient(m)*m)
				else:
					n_str += " - " + wrap(-numer.monomial_coefficient(m)*m)
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
	if not latex and n_wrap and d_str != "":
		n_str = "(" + n_str + ")"
	return (n_str, d_str)

class brat:

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

	def __repr__(self) -> str:
		N, D = _format(self)
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
		return _unfold_signature(self._ring, self._d_sig)

	def denominator_signature(self):
		return self._d_sig

	def fix_denominator(self, expression=None, signature=None):
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

	def latex(self, split=False):
		N, D = _format(self, latex=True)
		N_clean = _remove_unnecessary_braces_and_spaces(N)
		D_clean = _remove_unnecessary_braces_and_spaces(D)
		if split:
			return (f"{N_clean}", f"{D_clean}")
		return f"\\dfrac{{{N_clean}}}{{{D_clean}}}"
	
	def numerator(self):
			return self._n_poly
		
	def rational_function(self):
		return self._n_poly / self.denominator()
	
	def subs(self, S:dict):
		R = self.rational_function()
		Q = R.subs(S)
		try:
			return brat(Q)
		except ValueError:
			return Q

	def variables(self):
		return self._ring.gens()