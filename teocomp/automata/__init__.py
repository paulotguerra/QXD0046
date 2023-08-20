"""
The :mod:`teocomp.automata` module.
"""
from .pda   import PDA, AP
from .nfa   import NFA, AFN
from .dfa   import DFA, AFD
from .mtntm import MTNTM
from .tm    import TM, MT

__all__ = [
    "PDA",
    "NFA",
    "DFA",
    "AP",
    "TM",
    "MT",
    "MTNTM"
]
