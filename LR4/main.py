import os
import importlib.util
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# load module 4задание.py by filepath (module name cannot start with digit)
def load_module_from_path(path):
    spec = importlib.util.spec_from_file_location('zadanie4_module', path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def valid_color(c: str) -> bool:
    try:
        _ = mcolors.to_rgb(c)
        return True
    except Exception:
        return False


def input_float(prompt: str, default: float = None) -> float:
    s = input(f"{prompt} [{'Enter' if default is not None else ''}]: ").strip()
    if not s and default is not None:
        return default
    try:
        v = float(s)
        if v <= 0:
            raise ValueError
        return v
    except Exception:
        print('Некорректное число, попробуйте ещё раз.')
        return input_float(prompt, default)


def input_int(prompt: str, default: int = None) -> int:
    s = input(f"{prompt} [{'Enter' if default is not None else ''}]: ").strip()
    if not s and default is not None:
        return default
    try:
        v = int(s)
        if v <= 0:
            raise ValueError
        return v
    except Exception:
        print('Некорректное целое число, попробуйте ещё раз.')
        return input_int(prompt, default)


def demo():
    base = os.path.dirname(__file__)
    module = load_module_from_path(os.path.join(base, '4задание.py'))
    Rectangle = module.Rectangle
    RegularPolygon = module.RegularPolygon

    print('Демонстрация работы: создаём прямоугольник и правильный многоугольник')
    rect = Rectangle(5, 8, color='blue')
    poly = RegularPolygon(6, 2, color='orange')

    print(rect.description())
    print(poly.description())

    fig, ax = plt.subplots()
    rect.draw(ax, origin=(0,0), fill=True)
    poly.draw(ax, center=(8,4), fill=True)
    ax.set_aspect('equal')
    ax.autoscale_view()
    out = 'fig_demo.png'
    plt.savefig(out)
    print('Сохранено изображение', out)


if __name__ == '__main__':
    demo()
