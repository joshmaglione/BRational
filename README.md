# BRational
A SageMath package to beautifully format a class of rational functions.

Version: 1.1.2

[Documentation](https://joshmaglione.com/BRational/)

---

The default expression for 

$$\dfrac{1 + 26T + 66T^2 + 26T^3 + T^4}{(1 - T)^5}$$

in SageMath is 
```python
(-T^4 - 26*T^3 - 66*T^2 - 26*T - 1)/(T^5 - 5*T^4 + 10*T^3 - 10*T^2 + 5*T - 1)
```

Using `brational`, the default is 

```python
(1 + 26*T + 66*T^2 + 26*T^3 + T^4)/(1 - T)^5
```