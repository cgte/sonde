"""
La sonde va aller inspecter, importer et modifier a la volée un certain nombre de module avec d'enregister les appels

Use case: we have code with no test. What we want is to probe the code for later unittest/pytest generation

    >>> def sumfun(a, b):
    ...     return a + b

    >>> def record_to(recorder):
    ...     def probe_function(function_to_probe):
    ...         def probed_function(*args, **kwargs):
    ...             res = function_to_probe(*args, **kwargs)
    ...             qname = function_to_probe.__qualname__
    ...             recorder[(qname, args, str(kwargs))].append(res)
    ...             return res
    ...         return probed_function
    ...     return probe_function

    >>> record = defaultdict(list)
    >>> function_prober = record_to(record)
    >>> sumfun = function_prober(sumfun)
    >>> sumfun(1,2)
    3
    >>> sumfun('a' , 'b')
    'ab'
    >>> dict(record)
    {('sumfun', (1, 2), '{}'): [3], ('sumfun', ('a', 'b'), '{}'): ['ab']}
    >>> import json
    >>> json.dumps(record)

"""

from functools import wraps
from importlib import import_module
from collections import defaultdict
from pprint import pformat
import inspect
from typing import List, Dict


# Simple code reporter for dev, this would be a persitent thing.
code_report = defaultdict(list)


def listattr(something):
    """Returns public/classic attributeof the givent object """
    return [var for var in dir(something) if not var.startswith("_")]


def sonder_module(nom_module: str):
    """ This functions scans a module for callables:
        will patch them so as to record I/O for later use
    Should be done like in unitest discover ? so as to patch everything.
    """
    print(f"import de {nom_module}")
    module = import_module(nom_module)
    print(module)

    elements_names = listattr(module)
    for name in elements_names:
        element = getattr(module, name)
        if callable(element):
            print(f"{element} est callable on l'ajoute")
            sondee = sonder_vers(code_report)(element)
            setattr(module, name, sondee)

        if inspect.isclass(element):

            attributes = listattr(element)
            for name in attributes:
                target = getattr(element, name)
                if callable(target):
                    sondee = sonder_vers(code_report)(target)
                    setattr(element, name, sondee)


def sonder_vers(report: Dict[tuple, list]):
    """Probe call and record into adictionary """

    def ajouter_sonde(func: callable):
        @wraps(func)
        def sondee(*args, **kwargs):
            """ Process computaiton and records input and ouputs
            This is ok for a poc but using signatures and inspect would be much better
            """

            echantillon = (func.__qualname__, repr(args), repr(kwargs))
            res = func(*args, **kwargs)
            report[echantillon].append(res)
            return res

        return sondee

    return ajouter_sonde


sonder_module("code")

from code import mafonction, UneClasse

mafonction(1, 2)
moninstance = UneClasse(1)
moninstance.uncalcul(3)


print(pformat(dict(code_report)))


mon_rapport = defaultdict(list)


@sonder_vers(mon_rapport)
def somme(a, b, c):
    return a + b + c


somme(1, 2, 3)
somme(1, c=2, b=2)

print(pformat(dict(mon_rapport)))
