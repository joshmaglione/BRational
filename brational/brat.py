#
#   Copyright 2024--2025 Joshua Maglione
#
#   Distributed under MIT License
#

from sage.all import ZZ, SR, QQ, PolynomialRing, prod, vector
from sage.all import latex as LaTeX
from .util import my_print, DEBUG, brat_type, parenthesis_wrap, remove_unnecessary_braces_and_spaces

# Given a polynomial and a dictionary, decide if they represent zero.
def is_denominator_zero(den, sig) -> bool:
	if den == 0:		# Only need to check if den is zero
		return True
	if sig is None:		
		return False
	# Now we need to check that sig makes sense.
	if "coefficient" in sig.keys():
		if sig["coefficient"] == 0:
			return True
	if "factors" in sig.keys():
		return any(map(
			lambda v: list(v) == [0]*len(v), list(sig["factors"].keys())
		))
	return False

# Given two monomials f and g, determine if f/g is preferred.
def is_preferred(f, g) -> bool:
	P = f.parent()
	assert g in P
	if len(P.gens()) == 1:
		return f.degree() >= g.degree()
	degs = [f.degree(x) - g.degree(x) for x in P.gens()]
	if all(map(lambda d: d <= 0, degs)):
		return False
	if all(map(lambda d: d >= 0, degs)):
		return True
	i = 0
	while degs[i] == 0:
		i += 1
	return degs[i] < 0 

# Given a polynomial f with at least two monomials, decide if f is a finite
# geometric progression. If it is not, raise an error. This is because we assume
# our rational functions can be written as a product of factors of the form (1 -
# M_i), where M_i is a monomial. The function returns a triple (k, r, n) where 
# 	f = k(1 - r^n)/(1 - r). 
def is_finite_gp(f):
	m = f.monomials()
	assert len(m) > 1
	term = lambda k: f.monomial_coefficient(m[k])*m[k]
	if is_preferred(term(0), term(1)):
		r = term(0) / term(1)
		out = term(-1)
		step = 1
	else:
		r = term(1) / term(0)
		out = term(0)
		step = -1
	if any(term(i) / term(i+1) != r for i in range(1, len(m) - 1, step)):
		my_print(DEBUG, f"Believe given polynomial is not a finite geometric progression:\n\t{f=}")
		raise ValueError("Denominator not in correct form.")
	if f != out * (1 - r**len(m)) / (1 - r):
		my_print(DEBUG, f"Determined given polynomial\n\t{f=}\nis a finite geometric progression:\n\t({out})*(1 - ({r})^{len(m)})/(1 - ({r}))\nbut cannot determine equality.")
		raise RuntimeError("Unexpected behavior. Contact Josh.")
	return (out, r, len(m))

# Play games and hope you turn f into an element of P.
def get_poly(f, P):
	if f in ZZ:
		return f
	if f.parent() == SR:
		try:
			return P(f.polynomial(QQ))
		except TypeError:
			my_print(DEBUG, f"Cannot build polynomial. Given\n\t{f=} of type {type(f)}\n\t{P=} of type {type(P)}")
			raise TypeError("Numerator must be a polynomial.")
		except AttributeError:
			my_print(DEBUG, f"Cannot build polynomial. Given\n\t{f=} of type {type(f)}\n\t{P=} of type {type(P)}")
			raise TypeError("Numerator must be a polynomial.")
	elif len(f.monomials()) > 0:
		return P(f)
	else:
		my_print(DEBUG, f"Cannot build polynomial. Given\n\t{f=} of type {type(f)}\n\t{P=} of type {type(P)}")
		raise TypeError("Numerator must be a polynomial.")

# Given a denominator signature, determine if it represents an integer.
def is_sig_integral(sig:dict) -> bool:
	if sig is None:
		return True
	if sig["factors"] != {}:
		return False
	v = list(sig["monomial"])
	return bool(v == [0]*(len(v)))

# Given the polynomial ring R and signature sig, multiply all suitable factors
# together. Here, suitable is determined by exp_func. By default, everything is
# suitable.
def unfold_signature(R, sig, exp_func=lambda _: True):
	varbs = R.gens()
	mon = lambda v: prod(x**e for x, e in zip(varbs, v))
	if not "monomial" in sig:
		zero = tuple([0]*len(varbs))
		sig.update({"monomial": zero})
	if not "coefficient" in sig:
		sig.update({"coefficient": 1})
	monomial = sig["coefficient"]*mon(sig["monomial"])
	factors = prod(
		(1 - mon(v))**abs(e) for v, e in sig["factors"].items() if exp_func(e)
	)
	return monomial*factors

# Given a list of polynomial factors, return the integer factor together with a
# list of positive degree terms
def split_integer_factor(factors):
	int_coeff = factors.unit()
	pos_facts = []
	for f, e in list(factors):
		if f in ZZ:
			int_coeff *= f**e
		else:
			pos_facts.append((f, e))
	return (int_coeff, pos_facts)

# Given the polynomial ring R, the numerator N, and the denominator D, construct
# the denominator signature.
def get_signature(R, N, D):
	# First rule out the case where D is in the field.
	if D in R.base_ring():
		return (N, {
			"coefficient": D,
			"monomial": tuple([0]*len(R.gens())),
			"factors": {},
		})
	varbs = R.gens()
	if len(varbs) == 1: 
		deg = lambda m: vector(ZZ, [m.degree()])
	else:
		deg = lambda m: vector(ZZ, m.degrees())
	mon = lambda v: prod(x**e for x, e in zip(varbs, v))
	const, D_factors = split_integer_factor(D.factor())
	gp_factors = {}							# all geometric progressions
	pos_facts = R(1)						# all factors to go to numerator
	my_print(DEBUG, f"Numerator:\n\t{N}")
	my_print(DEBUG, f"Denominator:\n\t{D_factors}")
	my_print(DEBUG, f"Monomial:\n\t{const}")
	while len(D_factors) > 0:
		f, e = D_factors.pop(0)
		m_f = f.monomials() 	## Need to ignore constants??
		if len(m_f) == 2 and prod(f.coefficients()) < 0:
			my_print(DEBUG, f"Polynomial: {f} -- is GP", 1)
			# We make sure that if there are negative values, the first non-zero
			# value is negative. We will always have a positive.
			if is_preferred(m_f[0], m_f[1]):
				v = tuple(deg(m_f[0]) - deg(m_f[1]))
				pos = 1
			else:
				v = tuple(deg(m_f[1]) - deg(m_f[0]))
				pos = 0
			my_print(DEBUG, f"degree: {v}", 2)
			if v in gp_factors:
				gp_factors[v] += e
			else:
				gp_factors[v] = e
			# if f.monomial_coefficient(m_f[pos]) < 0:
			my_print(
				DEBUG, 
				f"const: {(f.monomial_coefficient(m_f[pos])*m_f[pos])**e}", 
				2
			)
			const *= (f.monomial_coefficient(m_f[pos])*m_f[pos])**e
		elif len(m_f) == 1:
			my_print(DEBUG, f"Polynomial: {f} -- a monomial", 1)
			const *= f**e
			my_print(DEBUG, f"const: {const}", 2)
		else:
			my_print(DEBUG, f"Polynomial: {f} -- is not GP", 1)
			k, r, n = is_finite_gp(f)
			my_print(DEBUG, f"data: ({k}, {r}, {n})", 2)
			r_num, r_den = R(r.numerator()), R(r.denominator())
			const *= k
			if r_num.monomial_coefficient(r_num.monomials()[0]) > 0:
				v = tuple(deg(r_num) - deg(r_den))
				v_n = tuple(n*(deg(r_num) - deg(r_den)))
				my_print(DEBUG, f"n-degree: {v_n}", 2)
				my_print(DEBUG, f"degree: {v}", 2)
				if v_n in gp_factors:
					gp_factors[v_n] += e
				else:
					gp_factors[v_n] = e
				if v in gp_factors:
					gp_factors[v] -= e
				else:
					gp_factors[v] = -e
			else:
				my_print(DEBUG, f"Pushing: (1 + {(-r)**n}, {e})", 2)
				D_factors.append(((r_den**n + (-r_num)**n), e))
				pos_facts *= (r_den - r_num)**e
	my_print(DEBUG, f"Final factors: {gp_factors}", 1)
	my_print(DEBUG, f"Accumulated factors: {pos_facts}", 1)
	# Clean up the monomial a little bit. 
	pos_facts_cleaned = R.one()
	for n_mon, e in list(pos_facts.factor()):
		my_print(DEBUG, f"Polynomial: {n_mon}", 1)
		k, r, n = is_finite_gp(n_mon)
		my_print(DEBUG, f"data: ({k}, {r}, {n})", 2)
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
	N_form = N*pos_facts_cleaned*unfold_signature(
		R, {"factors": gp_factors}, lambda e: e < 0
	)
	D_form = const*unfold_signature(
		R, {"factors": gp_factors}, lambda e: e > 0
	)
	if N_form/D_form != N/D:	# Most important check!
		my_print(DEBUG, "ERROR!")
		my_print(DEBUG, f"Expected:\n\t{N/D}")
		my_print(DEBUG, f"Numerator:\n\t{N_form}")
		my_print(DEBUG, f"Denominator:\n\t{D_form}")
		raise ValueError("Rational function does not satisfy main assumption. For details see:\n\thttps://joshmaglione.com/BRational/brat/")
	my_print(DEBUG, f"const: {const}", 1)
	const_unit, const_mono_factors = split_integer_factor(const.factor())
	const_mono = R(prod(f**e for f, e in const_mono_factors))
	if const_unit < 0:
		N_form = -N_form
		const_unit = -const_unit
	gp_factors = {v: e for v, e in gp_factors.items() if e > 0}
	return (N_form, {
		"coefficient": const_unit,
		"monomial": tuple(deg(const_mono)), 
		"factors": gp_factors,
	})

# Given data, determine the polynomial ring, the numerator and the denominator.
def process_input(num, dem=None, sig=None, fix=True):
	# Normalize
	if sig and sig["coefficient"] < 0:
		num *= -1 
		sig["coefficient"] *= -1
	if dem is None:
		R = num
	else:
		R = num/dem

	# Deal with integers and rationals
	if R in QQ:
		if dem is None and is_sig_integral(sig):
			# Implies num in QQ
			if fix:
				if sig["coefficient"] == 1:
					return (QQ, num, sig, brat_type("i"))
				return (QQ, num, sig, brat_type("r"))
			R /= sig["coefficient"]
			if R.denominator() == 1:
				br_type = brat_type("i")
			else:
				br_type = brat_type("r")
			return (QQ, R.numerator(), {
				"coefficient": R.denominator(), 
				"monomial": (), 
				"factors": {}
			}, br_type)
		if dem in QQ:
			if fix:
				if dem < 0:
					num *= -1
					dem *= -1
				if dem == 1:
					br_type = brat_type("i")
				else: 
					br_type = brat_type("r")
				return (QQ, num, {
					"coefficient": dem, 
					"monomial": (), 
					"factors": {}
				}, br_type)
			if R.denominator() == 1:
				br_type = brat_type("i")
			else:
				br_type = brat_type("r")
			return (QQ, R.numerator(), {
				"coefficient": R.denominator(), 
				"monomial": (), 
				"factors": {}
			}, br_type)
		if not fix:
			if R.denominator() == 1:
				br_type = brat_type("i")
			else:
				br_type = brat_type("r")
			return (QQ, R.numerator(), {
				"coefficient": R.denominator(), 
				"monomial": (), 
				"factors": {}
			}, br_type)
	
	# Attempt to grab the variables
	try:	# Not sure how best to do this. Argh!
		varbs = (R.numerator()*R.denominator()).parent().gens()
	except AttributeError and RuntimeError:
		varbs = R.variables()
	P = PolynomialRing(QQ, varbs)

	if dem is None:		# Then we are given a signature
		# Can be given negative exponents, so we take numerator.
		# Seems pointless but needed if fix = False
		dem = unfold_signature(P, sig)
		R /= dem
		dem = dem.numerator()
	
	# Determine the polynomial expressions for the numerator and denominator.
	if fix:
		N = get_poly(num, P)
		D = get_poly(dem, P)
	else: 
		N = get_poly(R.numerator(), P)
		D = get_poly(R.denominator(), P)

	# # Numerators can contain rationals still
	u = N.denominator()
	R = PolynomialRing(ZZ, varbs)
	N = R(N*u)
	D = R(D*u)

	# Now get the signature	
	if fix and sig is not None:
		sig["coefficient"] *= u
		D_sig = sig
		N_new = N
	else:
		N_new, D_sig = get_signature(R, N, D)
	
	# Determine the brat type
	br_type = brat_type("rf")
	if D == 1:
		if N in R.base_ring():
			br_type = brat_type("i")
		else:
			br_type = brat_type("ip")
	if D != 1 and D in R.base_ring():
		if N in R.base_ring():
			br_type = brat_type("r")
		else:
			br_type = brat_type("rp")
	if D not in R.base_ring() and D_sig["factors"] == {}:
		if D_sig["coefficient"] == 1:
			br_type = brat_type("ilp")
		else:
			br_type = brat_type("rlp")
	
	# Celebrate!
	return (R, N_new, D_sig, br_type)

# Given variables, a vector of integers, and a latex flag, return the associated
# monomial.
def vec_to_mono(varbs:list[str], vec:list[int], latex:bool) -> str:
	strings = []
	for i, x in enumerate(varbs):
		if vec[i] == 0:
			continue
		if vec[i] == 1:
			strings.append(x)
		else:
			if latex:
				strings.append(f"{x}^{{{vec[i]}}}")
			else:
				strings.append(f"{x}^{vec[i]}")
	if latex:
		return "".join(strings)
	return "*".join(strings)

# Given a polynomial ring, an element in the base field, and a pair of monomials
# mono and neg, and a latex flag, return the string representing the Laurent
# monomial coeff*mono/neg.
def stringify(poly_ring, coeff, mono, neg, latex:bool) -> str:
	if latex:
		wrap = lambda X: LaTeX(X)
		mult = ""
	else:
		wrap = lambda X: str(X)
		mult = "*"
	if len(poly_ring.gens()) == 1:
		deg_vec = [mono.degree() - neg.degree()]
	else:
		deg_vec = [mono.degree(x) - neg.degree(x) for x in poly_ring.gens()]
	varbs = list(map(wrap, poly_ring.gens()))
	if mono/neg in poly_ring.base_ring():
		return f"{coeff}"
	if coeff == 1:
		return vec_to_mono(varbs, deg_vec, latex)
	if coeff == -1:
		return f"-{vec_to_mono(varbs, deg_vec, latex)}"
	return f"{coeff}{mult}{vec_to_mono(varbs, deg_vec, latex)}"

# Given data, format the numerator. Returns the formatted and expanded numerator
# as a string.
def format_numerator(
		numer,			# numerator polynomial 
		neg,			# denominator monomial
		inc_ord:bool,
		latex:bool,
	) -> str:
	# initial set up
	P = numer.parent()
	ORD = -1 if inc_ord else 1

	n_str = ""
	mon_n = numer.monomials()
	flip = 1
	unit = 1
	for i, m in enumerate(mon_n[::ORD]):
		c = numer.monomial_coefficient(m)
		if i == 0:
			if c < 0:
				flip = -1
				unit = -unit
			n_str += stringify(P, flip*c, m, neg, latex)
		else: 
			if flip*c > 0:
				n_str += " + " + stringify(
					P, flip*numer.monomial_coefficient(m), m, neg, latex
				)
			else:
				n_str += " - " + stringify(
					P, -flip*numer.monomial_coefficient(m), m, neg, latex
				)
	if unit != 1: 		# unit is only 1 or -1
		if ' + ' in n_str or ' - ' in n_str:
			n_str = f"-({n_str})"
		else:
			n_str = f"-{n_str}"
	return n_str

# Given data, format the numerator. Returns the formatted and factored numerator
# as a string.
def format_factored_numerator(
		numer,
		neg,
		inc_ord:bool,
		latex:bool,
	) -> str:
	# initial set up
	ORD = -1 if inc_ord else 1
	P = numer.parent()
	
	factors = list(numer.factor())
	unit = numer.factor().unit()
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
				f_str += stringify(P, flip*c, m, P(1), latex)
			else: 
				if flip*c > 0:
					f_str += " + " + stringify(
						P, flip*f.monomial_coefficient(m), m, P(1), latex
					)
				else:
					f_str += " - " + stringify(
						P, -flip*f.monomial_coefficient(m), m, P(1), latex
					)
		if e > 1:
			if len(mon_n) != 1:
				f_str = f"({f_str})"
			if latex:
				f_str = f"{f_str}^{{{e}}}"
			else:
				f_str = f"{f_str}^{e}*"
		elif (len(factors) > 1 or unit != 1):
			if len(f.monomials()) != 1:
				if latex:
					f_str = f"({f_str})"
				else:
					f_str = f"({f_str})*"
			else:
				if latex:
					f_str = f"{f_str}"
				else:
					f_str = f"{f_str}*"
		n_str += f_str
	
	# If we still have an empty string, it will just be the monomial unit*neg
	# that we need.
	if len(n_str) == 0:
		return f"{stringify(P, unit, P(1), P(neg), latex)}"
	
	# Now we can assume the string is not empty.
	if n_str[-1] == "*":
		n_str = n_str[:-1]
	if unit*neg != 1:
		if unit*neg == -1:
			n_str = "-" + n_str
		else:
			if latex:
				return f"{stringify(P, unit, P(1), P(neg), latex)}{n_str}"
			return f"{stringify(P, unit, P(1), P(neg), latex)}*{n_str}"
	return n_str

# Given data, return the formatted denominator as a string.
def format_denominator(R, sig:dict, latex:bool, hidden_mono:bool) -> str:
	from .util import at_least_two
	def wrap(v:tuple[int]):
		mono = prod(x**e for x, e in zip(R.gens(), v) if e > 0)
		neg = prod(x**(-e) for x, e in zip(R.gens(), v) if e < 0)
		return stringify(R, R(1), R(mono), R(neg), latex)
	mono_factor = prod(x**e for x, e in zip(R.gens(), sig["monomial"]))
	d_str = ""
	if sig["coefficient"] != 1:
		d_str += stringify(R, sig["coefficient"], R(1), R(1), latex)
		if (len(sig["factors"]) > 0 or mono_factor != 1) and not latex:
			d_str += "*"
	if mono_factor != 1:
		d_str += stringify(R, R(1), mono_factor, R(1), latex)
		if len(sig["factors"]) > 0 and not latex:
			d_str += "*"
	gp_list = list(sig["factors"].items())
	gp_list.sort(key=lambda x: sum(x[0]))
	for v, e in gp_list:
		if e == 1:
			d_str += f"(1 - {wrap(v)})"
		else:
			if latex:
				d_str += f"(1 - {wrap(v)})^{{{e}}}"
			else:
				d_str += f"(1 - {wrap(v)})^{e}"
		if not latex and gp_list[-1] != (v, e):
			d_str += "*"
	
	if latex:
		if hidden_mono:
			if len(sig["factors"]) == 1 and list(sig["factors"].values())[0] == 1 and sig["coefficient"] == 1:
				d_str = d_str[1:-1]
		else:
			if len(sig["factors"]) == 1 and list(sig["factors"].values())[0] == 1 and sig["coefficient"] == 1 and list(sig["monomial"]) == [0]*len(sig["monomial"]):
				d_str = d_str[1:-1]
		return d_str
	if len(gp_list) > 1 or len(mono_factor.factor()) > 1 or at_least_two(
		sig["coefficient"] != 1, 
		mono_factor != 1,
		len(gp_list) > 0
	):
		return f"({d_str})"
	return d_str

def format_polynomial_for_align(POLY, COLWIDTH, first=0):
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

def brat_to_str(B, latex=False) -> str:
	if B._factor:
		numerator = format_factored_numerator
	else:
		numerator = format_numerator
	if latex:
		quo = lambda n, d: f"\\dfrac{{{n}}}@{{{d}}}"
	else:
		quo = lambda n, d: f"{parenthesis_wrap(str(n))}/{d}"
	my_print(DEBUG, f"Printing with type {B._type.name}")

	if B._type.name == "INTEGER":
		return f"{B._n_poly}"
	if B._type.name == "RATIONAL":
		return quo(B._n_poly, B._d_sig["coefficient"])
	
	# Polynomial
	if B._type.name in ["INTEGRAL_POLY", "RATIONAL_POLY"]:
		N = numerator(
			B._n_poly,
			B._ring(1),
			B.increasing_order,
			latex,
		)
		if B._type.name == "INTEGRAL_POLY":
			return f"{N}"
		return quo(N, B._d_sig["coefficient"])
	
	# Laurent polynomial
	if B._type.name in ["INTEGRAL_L_POLY", "RATIONAL_L_POLY"] and B.hide_monomial:
		vars_vec = zip(B._ring.gens(), B._d_sig["monomial"])
		monomial = prod(x**e for x, e in vars_vec)
		N = numerator(
			B._n_poly,
			monomial,
			B.increasing_order,
			latex,
		)
		if B._type.name == "INTEGRAL_L_POLY":
			return f"{N}"
		return quo(N, B._d_sig["coefficient"])

	# Rational function
	if B.hide_monomial:
		vars_vec = zip(B._ring.gens(), B._d_sig["monomial"])
		monomial = prod(x**e for x, e in vars_vec)
		N = numerator(
			B._n_poly,
			monomial,
			B.increasing_order,
			latex,
		)
		sig = deep_sig_copy(B._d_sig)
		sig["monomial"] = tuple([0]*len(B._ring.gens()))
	else:
		N = numerator(
			B._n_poly,
			B._ring(1),
			B.increasing_order,
			latex,
		)
		sig = B._d_sig
	D = format_denominator(B._ring, sig, latex, B.hide_monomial)
	return quo(N, D)

# The main class of BRational.
class brat:
	r"""
	A class for beautifully formatted rational functions.

	- ``rational_expression``: the rational function (default: ``None``),

	- ``numerator``: the numerator polynomial of the rational function (default: ``None``),

	- ``denominator``: the denominator polynomial of the rational function (default: ``None``),

	- ``denominator_signature``: the dictionary of data for the denominator (default: ``None``),

	- ``fix_denominator``: whether to keep the given denominator fixed (default: ``True``),

	- ``increasing_order``: whether to display polynomials in increasing degree (default: ``True``),

	- ``hide_monomial``: whether to absorb the monomial in the denominator into the numerator (default: ``True``).
	"""

	def __init__(self, 
			rational_expression=None, 
			numerator=None, 
			denominator=None,
			denominator_signature:dict=None,
			fix_denominator:bool=True,
			increasing_order:bool=True,
			hide_monomial:bool=True,
		):
		# Don't give me too much! 
		if rational_expression is not None and numerator is not None:
			raise ValueError("Do not provide a rational expression and a numerator.")
		if rational_expression is not None and denominator is not None:
			raise ValueError("Do not provide a rational expression and a denominator.")
		if rational_expression is not None and denominator_signature is not None:
			raise ValueError("Do not provide a rational expression and a denominator signature.")
		if denominator is not None and denominator_signature is not None:
			raise ValueError("Do not provide a denominator and a denominator signature.")

		# First we remove zero denominator
		if is_denominator_zero(denominator, denominator_signature):
			raise ValueError("Denominator cannot be zero.")
		
		# int and float can be problematic
		if isinstance(rational_expression, int):
			rational_expression = ZZ(rational_expression)
		if isinstance(numerator, int):
			numerator = ZZ(numerator)
		if isinstance(denominator, int):
			denominator = ZZ(denominator)
		if isinstance(rational_expression, float):
			try:
				rational_expression = QQ(rational_expression)
			except TypeError:
				raise TypeError("Input must be a rational function.")
		
		# Sort through the input and raise potential errors
		if rational_expression is not None:
			# rational_expression is given
			try:
				N = rational_expression.numerator()
				D = rational_expression.denominator()
			except AttributeError:
				raise TypeError("Input must be a rational function.")
		else: 
			# rational_expression is not given
			if numerator is None:
				raise ValueError("Must provide a numerator.")
			if denominator is None and denominator_signature is None:
				raise ValueError("Must provide a denominator.")
			N = numerator
			if denominator is None:
				if not isinstance(denominator_signature, dict):
					raise TypeError("Denominator signature must be a dictionary.")
				if any(k not in ["coefficient", "monomial", "factors"] for k in denominator_signature.keys()):
					raise ValueError("Denominator signature contains an unexpected key.")
				D = None
			else:
				D = denominator
		
		# Finally process the input
		my_print(DEBUG, f"Given\n\tNumerator: {N}\n\tDenominator: {D}\n\tSignature: {denominator_signature}")
		T = process_input(
			N, 
			dem=D, 
			sig=denominator_signature, 
			fix=fix_denominator
		)
		my_print(DEBUG, f"Output of _process_intput:\n\t{T}")
		self._ring = T[0]			# Parent ring for rational function
		self._n_poly = T[1]			# Numerator polynomial
		self._d_sig = T[2]			# Denominator with form \prod_i (1 - M_i)
		self._type = T[3]			# Enum for printing
		self.increasing_order = increasing_order
		self.hide_monomial = hide_monomial
		self._factor = False

	def __str__(self) -> str:
		return brat_to_str(self, latex=False)
	
	def __repr__(self) -> str:
		return brat_to_str(self, latex=False)
	
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
	
	def change_denominator(self, expression=None, signature:dict=None):
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
			sage: H.change_denominator(
				signature={(1,): 1, (2,): 1, (3,): 2, (4,): 1, (5,): 1}
			)
			(1 + x^3 + x^4 + x^5 + x^7 + x^8 + x^9 + x^12)/((1 - x)*(1 - x^2)*(1 - x^3)^2*(1 - x^4)*(1 - x^5))
		"""
		rat = self.rational_function()
		if signature:
			d = unfold_signature(self._ring, signature)
			new_num = rat*d.numerator()*d.denominator()
			return brat(
				numerator=new_num.numerator(),
				denominator=d.numerator()
			)
		new_num = rat*expression
		return brat(
			numerator=new_num.numerator(),
			denominator=expression
		)

	def denominator(self):
		r"""Returns the polynomial in the denominator of the rational function.

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
		new_sig = deep_sig_copy(self._d_sig)
		if self.hide_monomial:
			new_sig["monomial"] = tuple(
				[0]*(len(new_sig["monomial"]))
			)
		return brat(unfold_signature(self._ring, new_sig))
	
	def denominator_signature(self):
		r"""Returns the dictionary signature for the denominator. The format of the dictionary is as follows. The keys are 

		- ``coefficient``: a positive integer,
		- ``monomial``: a degree tuple,
		- ``factors``: dictionary with keys given by vectors and values in the positive integers. 
		
		EXAMPLE::

			sage: x, y, z = polygens(ZZ, 'x,y,z')
			sage: F = br.brat(1/(3*(1 - x^2*y)*(1 - y^4)^3*(1 - x*y*z)*(1 - x^2)^5))
			sage: F
			1/(3*(1 - x^2)^5*(1 - x*y*z)*(1 - x^2*y)*(1 - y^4)^3)
			sage: F.denominator_signature()
			{'coefficient': 3,
 			 'monomial': (0, 0, 0),
 			 'factors': {(2, 0, 0): 5, (0, 4, 0): 3, (1, 1, 1): 1, (2, 1, 0): 1}}
		"""
		return self._d_sig

	def factor(self):
		r"""Returns a new ``brat`` object with the numerator polynomial factored.
		"""
		B = deep_brat_copy(self)
		B._factor = True
		return B

	def invert_variables(self, ratio:bool=False):
		r"""Returns the corresponding ``brat`` after inverting all of the variables and then rewriting the rational function so that all exponents are non-negative. 

		- ``ratio'': returns the ratio of the original brat divided by the brat with inverted variables. Default: ``False''.
		
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
		if ratio:
			return self.invert_variables()/self
		varbs = self._ring.gens()
		mon = lambda v: prod(x**e for x, e in zip(varbs, v))
		factor = prod(
			mon(v)**e*(-1)**e for v, e in self._d_sig["factors"].items()
		)
		N = self._n_poly.subs({x: x**-1 for x in varbs})*factor*mon(
			self._d_sig["monomial"]
		)
		if N.denominator() in ZZ:
			return brat(
				numerator=self._ring(N), 
				denominator_signature=self._d_sig, 
				increasing_order=self.increasing_order
			)
		new_sig = deep_sig_copy(self._d_sig)
		if len(self._ring.gens()) == 1:
			new_sig["monomial"] = tuple([N.denominator().degree()])
		else:
			new_sig["monomial"] = tuple(N.denominator().degrees())
		return brat(numerator=N.numerator(), denominator_signature=new_sig)

	def latex(self, factor:bool=False, split:bool=False):
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
		if factor:
			B = self.factor()
		else:
			B = self
		latex_str = remove_unnecessary_braces_and_spaces(brat_to_str(B, True))
		if split:
			N, D = latex_str.split('@')
			N = N[7:-1]
			D = D[1:-1]
			return (N, D)
		return latex_str.replace('@', '')

	# Just for SageMath's `pretty_print` function
	def _latex_(self):
		return self.latex(factor=self._factor)
	
	def numerator(self):
		r"""Returns the polynomial in the numerator of the rational function as a ``brat``.

		EXAMPLE::

			sage: x, y = polygens(QQ, 'x,y')
			sage: f = br.brat(
				numerator=1 + x*y^2,
				denominator=1 - x^2*y^4
			)
			sage: f
			(1 + x*y^2)/(1 - x^2*y^4)
			sage: f.numerator()
			1 + x*y^2
		"""
		B = deep_brat_copy(self)
		B._d_sig["coefficient"] = 1
		B._d_sig["factors"] = {}
		match B._type.name:
			case "RATIONAL":
				B._type = brat_type("i")
			case "RATIONAL_POLY":
				B._type = brat_type("ip")
		if B.hide_monomial:
			if list(B._d_sig["monomial"]) != [0]*len(B._ring.gens()):
				B._type = brat_type("ilp")
			else:
				B._type = brat_type("ip")
			return B
		if B._type.name != "INTEGER":
			B._type = brat_type("ip")
		B._d_sig["monomial"] = tuple([0]*len(B._ring.gens()))
		return B
		
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
		return self._n_poly / unfold_signature(self._ring, self._d_sig)
	
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
			filename:str=None,
			just_numerator:bool=False,
			just_denominator:bool=False,
			align:bool=False,
			factor:bool=False,
			line_width:int=100,
			function_name:str=None,
			save_message:bool=True
		) -> None:
		r"""Writes the ``brat`` object to a file formatted in LaTeX. The (default) output is a displayed equation (using ``\[`` and ``\]``) of the ``brat``. There are many parameters to change the format of the output.

		- ``filename``: the string for the output filename. Default: ``None``, which will output a timestamp name of the form ``%Y-%m-%d_%H-%M-%S.tex``.
		- ``just_numerator``: write just the numerator. Default: ``False``.
		- ``just_denominator``: write just the denominator. Default: ``False``.
		- ``align``: format using the ``align*`` environment. Default: ``False``.
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
		if not function_name is None:
			if align:
				function_name = f"{function_name} &= "
			else:
				function_name = f"{function_name} = "
		else:
			function_name = ""
		if align:
			func = format_polynomial_for_align(func, line_width, first=len(function_name))
			output = f"\\begin{{align*}}\n\t{function_name}{func}\n\\end{{align*}}"
		else:
			output = f"\\[\n\t{function_name}{func}\n\\]"
		with open(filename, "w") as f:
			f.write(output)
		if save_message:
			print(f"Output saved to {filename}.")
		return None
	
def deep_sig_copy(sig:dict) -> dict:
	return {
		"coefficient": sig["coefficient"],
		"monomial": sig["monomial"],
		"factors": {k: v for k, v in sig["factors"].items()},
	}

def deep_brat_copy(B:brat) -> brat:
	B_new = brat(
		numerator=B._n_poly, 
		denominator_signature=deep_sig_copy(B._d_sig), 
		hide_monomial=B.hide_monomial,
		increasing_order=B.increasing_order,
	)
	B_new._factor = B._factor
	return B_new