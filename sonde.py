"""
La sonde va aller inspecter, importer et modifier a la volée un certain nombre de module avec d'enregister les appels

"""

from functools import wraps
from importlib import import_module
from collections import defaultdict
from pprint import pformat
import inspect

code_report = defaultdict(list)


def sonder_module(nom_module: str):
    print(f"import de {nom_module}")
    module = import_module(nom_module)
    print(module)
    import ipdb

    elements_names = [var for var in dir(module) if not var.startswith("_")]
    for name in elements_names:

        element = getattr(module, name)
        if callable(element):
            print(f"{element} est callable on l'ajoute")
            sondee = sonder_vers(code_report)(element)
            setattr(module, name, sondee)
        if inspect.isclass(element):
            import ipdb

            ipdb.set_trace()
    pass


def sonder_vers(report: dict):
    def ajouter_sonde(func: callable):
        @wraps(func)
        def sondee(*args, **kwargs):
            echantillon = (func.__qualname__, repr(args), repr(kwargs))
            res = func(*args, **kwargs)
            report[echantillon].append(res)
            return res

        return sondee

    return ajouter_sonde


sonder_module("code")

from code import mafonction

mafonction(1, 2)

print(pformat(dict(code_report)))


mon_rapport = defaultdict(list)


@sonder_vers(mon_rapport)
def somme(a, b, c):
    return a + b + c


somme(1, 2, 3)
somme(1, c=2, b=2)

print(pformat(dict(mon_rapport)))
