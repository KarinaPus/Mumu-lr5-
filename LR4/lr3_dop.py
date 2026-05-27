import math
import csv
import os
from typing import List, Tuple
from statistics import mean, median, mode, variance, StatisticsError, pstdev
import matplotlib.pyplot as plt


class SeriesAnalyzer:
    def __init__(self, xs: List[float], ns: List[int]):
        self.xs = xs
        self.ns = ns
        self.series_values = []  # computed series F(x)
        self.math_values = []    # math.acos(x)
        self.errors = []

    @staticmethod
    def arcsin_series_term_coeff(n: int) -> float:
        # coefficient for x^{2n+1} in arcsin series: (2n)!/(4^n (n!)^2 (2n+1))
        return math.factorial(2*n) / (4**n * (math.factorial(n)**2) * (2*n + 1))

    @classmethod
    def arccos_series(cls, x: float, n_terms: int) -> float:
        # arccos x = pi/2 - arcsin x; arcsin x = sum_{k=0}^{inf} coeff_k * x^{2k+1}
        s = 0.0
        for k in range(n_terms):
            coeff = cls.arcsin_series_term_coeff(k)
            s += coeff * (x ** (2*k + 1))
        return math.pi/2 - s

    def compute(self):
        self.series_values = []
        self.math_values = []
        self.errors = []
        for x, n in zip(self.xs, self.ns):
            fx_series = self.arccos_series(x, n)
            try:
                fx_math = math.acos(x)
            except ValueError:
                fx_math = float('nan')
            self.series_values.append(fx_series)
            self.math_values.append(fx_math)
            self.errors.append(abs(fx_series - fx_math) if not math.isnan(fx_math) else float('nan'))

    def stats(self) -> dict:
        vals = self.series_values
        res = {}
        res['mean'] = mean(vals)
        res['median'] = median(vals)
        try:
            res['mode'] = mode(vals)
        except StatisticsError:
            res['mode'] = None
        try:
            res['variance'] = variance(vals)
        except StatisticsError:
            res['variance'] = 0.0
        res['stddev'] = pstdev(vals)
        return res

    def save_table(self, path: str):
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['x', 'n', 'Series F(x)', 'Math F(x)', 'abs_error'])
            for x, n, s, m, e in zip(self.xs, self.ns, self.series_values, self.math_values, self.errors):
                writer.writerow([f'{x:.6g}', n, f'{s:.10g}', f'{m:.10g}', f'{e:.10g}'])

    def plot(self, out_path: str):
        plt.figure(figsize=(8,6))
        # plot series and math values vs x
        plt.plot(self.xs, self.series_values, label='Series approximation', color='tab:blue', marker='o')
        plt.plot(self.xs, self.math_values, label='math.acos(x)', color='tab:orange', linestyle='--')
        # annotate maximum error
        if any(not math.isnan(e) for e in self.errors):
            max_idx = max(range(len(self.errors)), key=lambda i: self.errors[i])
            mx = self.xs[max_idx]
            my_series = self.series_values[max_idx]
            my_math = self.math_values[max_idx]
            err = self.errors[max_idx]
            plt.annotate(f'max err={err:.2e}\n x={mx:.3f}', xy=(mx, my_series), xytext=(mx, my_series+0.5),
                         arrowprops=dict(arrowstyle='->', color='red'), color='red')
        plt.xlabel('x')
        plt.ylabel('F(x)')
        plt.title('Series approximation vs math.acos(x)')
        plt.grid(True)
        plt.legend()
        plt.savefig(out_path)
        plt.close()


def generate_sample_data(num_points: int = 21) -> Tuple[List[float], List[int]]:
    # generate x values in [-1,1] and choose n based on |x| (more terms for larger x)
    xs = [ -1 + 2*i/(num_points-1) for i in range(num_points) ]
    ns = []
    for x in xs:
        # choose n from 1 to 10 depending on |x|
        n = int(1 + (abs(x) * 9))
        if n < 1:
            n = 1
        ns.append(n)
    return xs, ns


def main():
    base = os.path.dirname(__file__)
    csv_in = os.path.join(base, 'lr3_input.csv')
    csv_out = os.path.join(base, 'lr3_results.csv')
    plot_out = os.path.join(base, 'lr3_plot.png')

    if os.path.exists(csv_in):
        xs = []
        ns = []
        with open(csv_in, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                xs.append(float(row['x']))
                ns.append(int(row.get('n', 5)))
    else:
        xs, ns = generate_sample_data(41)

    analyzer = SeriesAnalyzer(xs, ns)
    analyzer.compute()
    stats = analyzer.stats()
    analyzer.save_table(csv_out)
    analyzer.plot(plot_out)

    # save stats to a small report
    report = os.path.join(base, 'lr3_stats.txt')
    with open(report, 'w', encoding='utf-8') as f:
        f.write('Statistics for series values:\n')
        for k,v in stats.items():
            f.write(f'{k}: {v}\n')

    print('Saved table to', csv_out)
    print('Saved plot to', plot_out)
    print('Saved stats to', report)


if __name__ == '__main__':
    main()
