# BRational
A SageMath package to beautifully format rational functions arising from enumerative algebra into plaintext and latex.

Version: 2.0.1

[Documentation](https://joshmaglione.com/BRational/)

---

### Example 1

The default factored expression for 

$$\dfrac{1 + 3q^{-1}t - 4q^{-1} - 4q^{-2}t + 3q^{-2} + q^{-3}t}{(1 - q^{-1}t)(1 - q^{-2}t^4)}$$

in SageMath is sometimes expressed as
```python
-(q^2 + 3*q*t - 3*q - t)*(q - 1)/((t^2 + q)*(t^2 - q)*(q - t))
```

Using `brational`, we get 

```python
q^-3*(1 - q)*(t + 3*q - 3*q*t - q^2)/((1 - q^-1*t)*(1 - q^-2*t^4))
```

Want $\LaTeX$? No problem:

```python
sage: print(br.brat(q^-3*(1 - q)*(t + 3*q - 3*q*t - q^2)/((1 - q^-1*t)*(1 - q^-2*t^4))).factor().latex())
\dfrac{q^{-3}(1 - q)(t + 3q - 3qt - q^2)}{(1 - q^{-1}t)(1 - q^{-2}t^4)}
```


### Example 2

The default expression for 

$$\dfrac{1 + 26T + 66T^2 + 26T^3 + T^4}{(1 - T)^5}$$

in SageMath is sometimes expressed as
```python
(-T^4 - 26*T^3 - 66*T^2 - 26*T - 1)/(T^5 - 5*T^4 + 10*T^3 - 10*T^2 + 5*T - 1)
```

Using `brational`, the default is 

```python
(1 + 26*T + 66*T^2 + 26*T^3 + T^4)/(1 - T)^5
```

And latex:

```python
sage: print(br.brat((1 + 26*T + 66*T^2 + 26*T^3 + T^4)/(1 - T)^5).latex())
\dfrac{1 + 26T + 66T^2 + 26T^3 + T^4}{(1 - T)^5}
```