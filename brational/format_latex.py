from sage.all import latex as LaTeX
from sage.all import ZZ

def _poly_to_latex(P):
	monos = P.monomials()[::-1]
	if P.monomial_coefficient(monos[0]) < 0:
		flip = -1
	else:
		flip = 1
	coeffs = [flip*P.monomial_coefficient(m) for m in monos]
	out_str = ""
	for i, t in enumerate(zip(coeffs, monos)):
		c, m = t
		if c == 1 and i == 0:
			out_str += f"{LaTeX(m)}"
		elif c == 1:
			out_str += f" + {LaTeX(m)}"
		elif c == -1:
			out_str += f" - {LaTeX(m)}"
		else:
			out_str += f" {c} {LaTeX(m)}"
	return out_str, flip

def _factors_to_latex(factors):
	out_str = ""
	flip_prod = 1
	for f in [f for f in factors if not f[0] in ZZ]:
		poly, flip = _poly_to_latex(f[0])
		flip_prod *= flip
		if f[1] == 1 and len(factors) == 1:
			return f"{poly}", flip_prod
		if f[1] == 1:
			out_str += f"({poly})"
		else:
			flip_prod *= flip_prod**(f[1] - 1)
			out_str += f"({poly})^{{{f[1]}}}"
	return out_str, flip_prod

def my_latex(R, split=True):
	N = R.numerator().factor()
	D = R.denominator().factor()
	N_out, N_flips = _factors_to_latex(list(N))
	D_out, D_flips = _factors_to_latex(list(D)[::-1])
	u = N.unit() * N_flips / D.unit() / D_flips
	if u != 1:
		if len(list(N)) == 1 and list(N)[0][1] == 1:
			N_out = f"{u} ({N_out})"
		else:
			N_out = f"{u} {N_out}"
	else:
		if N_out.replace(' ', '') == '':
			N_out = "1"
	if split:
		out_str = (N_out, D_out)
	else:
		out_str = f"\\dfrac{{{N_out}}}{{{D_out}}}"
	return out_str


def split_polynomial_for_latex(poly, name=None, max_line_length=180, wrap=True):
	import re
	terms = re.findall(r'[+-]?[^+-]+', poly)
	if name:
		extra = len(name) + 2
	else:
		extra = 0
	lines = []
	current_line = "" 
	for term in terms:
		term = term.strip()
		if not current_line:
			new_line = "& " + term
		else:
			new_line = current_line + " " + term
		if len(new_line) + 2 > max_line_length - extra:
			lines.append(current_line + " \\\\")
			current_line = "& " + term
		else:
			current_line = new_line
	if current_line:
		lines.append(current_line)
	if wrap:
		start = "\\begin{align*}\n"
		end = "\n\\end{align*}"
	else:
		start = ""
		end = ""
	if name:
		start += f"{name}"
		lines[0] = lines[0].replace("&", "&=")
	latex_output = start + "\n".join(lines) + end
	return latex_output
