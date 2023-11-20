import numpy as np
from sympy import lambdify, symbols, solve
from sympy.parsing.latex import parse_latex

class ExpressionParse:
    def __init__(self, latex: str):
        self.latex = latex # latex-выражение

        # Парсим latex-строку
        self._parse_expression()

        # Преобразование выражения sympy в python-функцию
        self._expr2lambda()

    @property
    def parameters(self):
        return self.params
        
    def _parse_expression(self):
        # Парсинг latex-строки в sympy-выражение
        if 'displaystyle' in self.latex:
            self.latex = self.latex.replace('{\displaystyle', '')[:-1]
        
        self.sympy_expression = parse_latex(self.latex)

    def _expr2lambda(self):
        # Преобразование выражения sympy в python-функцию

        expr = self.sympy_expression
        # Получаем символы из выражения
        x, y, z = symbols('x y z')
        all_symbols = expr.free_symbols
        other_symbols = all_symbols - {x, y, z}

        # Решаем выражение относительно зависимой переменной
        if z in all_symbols:
            expr_solve = solve(expr, z)
        elif y in all_symbols:
            expr_solve = solve(expr, y)     
        else:
            expr_solve = solve(expr, x)

        # Преобразуем выражение в python-функцию
        lets = sorted([*[x, y], *other_symbols], key=str)
        self.z_func = lambdify(lets, expr_solve)
        self.params_str = sorted(map(str, (other_symbols)))

    def calculate_points(self, params_value=4, xy_lim=55, density=35, **params) -> np.ndarray:
        # Нахождение точек (x, y, z+, z-) поверхности для значений (x, y) в заданном диапазоне
        # для заданных параметров или для параметров по умолчанию

        # Параметры и их стартовые значения
        self.params = {p: params_value for p in self.params_str} if not params else params
        
        self.xy_iter = np.linspace(-xy_lim, xy_lim, density) # для итерации по XY-сетке

        return np.array([[x, y, z] 
                         for x in self.xy_iter 
                         for y in self.xy_iter 
                         for z in self.z_func(*[p for p in self.params.values()] + [x, y]) 
                         if not np.isnan(z) and type(z) != complex])


if __name__ == '__main__':
    latex = r'{\displaystyle {\frac {x^{2}}{a^{2}}}+{\frac {y^{2}}{p^{2}}}=1}'

    calc = ExpressionParse(latex)
    points = calc.calculate_points()
    print(points)
    print(calc.params)

