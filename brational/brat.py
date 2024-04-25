
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

def _get_signature(R, N, D, verbose=False):
	varbs = R.gens()
	deg = lambda m: vector(ZZ, [m.degree(v) for v in varbs])
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
			v = tuple(deg(r_num) - deg(r_den))
			if r_num.monomial_coefficient(r_num.monomials()[0]) > 0:
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
	N_form = N*pos_facts*prod(
		(1 - mon(v))**(-e) for v, e in gp_factors.items() if e < 0
	)
	D_form = const*prod((1 - mon(v))**e for v, e in gp_factors.items() if e > 0)
	if N_form/D_form != N/D:
		print("ERROR!")
		print(f"Expected:\n\t{N/D}")
		print(f"Numerator:\n\t{N_form}")
		print(f"Denominator:\n\t{D_form}")
		raise ValueError("Error in implementation. Contact Josh.")
	if const < 0:
		N_form = -N_form
		const = -const
	gp_factors = {v: e for v, e in gp_factors.items() if e > 0}
	return (N_form, {"monomial": const, "factors": gp_factors})

def _process_input(R):
	if R in QQ:
		N, D = R.numerator(), R.denominator()
		return ([], N, D, N, {"monomial": D, "factors": {}})
	try:	# Not sure how best to do this. Argh!
		varbs = (R.numerator()*R.denominator()).parent().gens()
	except AttributeError:
		varbs = R.variables()
	P = PolynomialRing(QQ, varbs)
	N = get_poly(R.numerator(), P)
	D = get_poly(R.denominator(), P)
	R_simple = (N / D).factor().expand()
	N, D = R_simple.numerator(), R_simple.denominator()
	N_form, gp_facts = _get_signature(P, N, D)
	return (varbs, N, D, N_form, gp_facts)

def _format(B, latex=False):
	if latex:
		wrap = lambda X: LaTeX(X)
	else:
		wrap = lambda X: str(X)
	numer = B._n_sig
	mon_n = numer.monomials()
	n_str = ""
	for i, m in enumerate(mon_n[::-1]):
		if i == 0:
			n_str += wrap(numer.monomial_coefficient(m)*m)
		else: 
			c = numer.monomial_coefficient(m)
			if c > 0:
				n_str += " + " + wrap(numer.monomial_coefficient(m)*m)
			else:
				n_str += " - " + wrap(-numer.monomial_coefficient(m)*m)
	if not latex and len(mon_n) > 1:
		n_str = "(" + n_str + ")"
	varbs = B.variables
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
		if not latex:
			d_str += "*"
	if not latex:
		d_str = "(" + d_str + ")"
	return (n_str, d_str)

class brat:

	def __init__(self, 
			rational_expression=None, 
			numerator=None, 
			denominator=None
		):
		if not denominator is None and denominator == 0:
			raise ValueError("Denominator cannot be zero.")
		if rational_expression is None:
			R = numerator / denominator
		else:
			R = rational_expression
			try:
				_ = R.numerator()
				_ = R.denominator()
			except AttributeError:
				raise TypeError("Input must be a rational function.")
		T = _process_input(R)
		self.variables = T[0]		# Tuple of variables
		self._n_poly = T[1]			# Numerator polynomial
		self._d_poly = T[2]			# Denominator polynomial
		self._n_sig = T[3]			# Numerator for the denominator from d_sig
		self._d_sig = T[4]			# Denominator with form \prod_i (1 - M_i)
									# recorded as a dictionary

	def __repr__(self) -> str:
		N, D = _format(self)
		if self._d_poly == 1:
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
	
	def denominator_signature(self):
		return self._d_sig

	def formatted_denominator(self):
		mon = lambda v: prod(x**e for x, e in zip(self.variables, v))
		return self._d_sig["monomial"] * prod(
			(1 - mon(v))**e for v, e in self._d_sig["factors"].items()
		)

	def formatted_numerator(self):
		return self._n_sig

	def invert_variables(self, quotient=False):
		R = self.rational_function()
		Xs = R.parent().gens()
		R_inv = R.subs({x: x**-1 for x in Xs})
		if quotient:
			return brat(R_inv/R)
		return brat(R_inv)

	def latex(self, split=False, align_environment=False):
		N, D = _format(self, latex=True)
		if split:
			return (f"{N}", f"{D}")
		return f"\\dfrac{{{N}}}{{{D}}}"
	
	def rational_function(self):
		return self._n_poly / self._d_poly
	
	def subs(self, S:dict):
		R = self.rational_function()
		Q = R.subs(S)
		try:
			return brat(Q)
		except ValueError:
			return Q