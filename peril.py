from __future__ import annotations

from typing import *
from functools import lru_cache

from matplotlib import pyplot as plt
from tqdm import tqdm

class Peril:
    __slot__ = ['required_symbols']

    def __init__(self, required_symbols: Tuple[int, ...]) -> None:
        self.required_symbols = required_symbols
        # (n_unpresent_symbols, n_once_symbols, n_twice_symbols, n_third_symbols, ...)
        # e.g. 🗡🛡☀☀ -> (3, 2, 1)
        assert sum(required_symbols) == 6
    
    def __eq__(self, other: Peril) -> bool:
        return self.required_symbols == other.required_symbols

    def __hash__(self) -> int:
        return hash(tuple(self.required_symbols)) ^ hash('Peril')
    
    def __str__(self):
        symbol_acc = ord('A')
        buf = []
        for (repetition, n) in enumerate(self.required_symbols):
            for _ in range(n):
                buf.append(chr(symbol_acc) * repetition)
                symbol_acc += 1
        return ''.join(buf)

@lru_cache(maxsize=None)
def perilPassProb(hero_n_dice: int, peril: Peril) -> float:
    # dynamic programing
    if peril.required_symbols[0] == 6:
        return 1.0
    if hero_n_dice == 0:
        return 0.0
    prob = 0.0
    for symbol_repetition, n_symbols in enumerate(peril.required_symbols):
        case_prob = n_symbols / 6
        if symbol_repetition == 0:
            remainingPeril = peril
        else:
            required = [*peril.required_symbols]
            required[symbol_repetition] -= 1
            required[symbol_repetition - 1] += 1
            remainingPeril = Peril(tuple(required))
        prob += case_prob * perilPassProb(
            hero_n_dice - 1, remainingPeril, 
        )
    return prob

def monteCarloValidation():
    ...

def visualize():
    perils = (
        (Peril((5, 1)), ''), 
        (Peril((4, 2)), ''), 
        (Peril((3, 3)), ''), 
        (Peril((2, 4)), ' (Palace Default)'), 
        (Peril((2, 3, 1)), ''), 
    )
    X = [*range(1, 18)]
    for peril, comment in tqdm(perils):
        Y = [perilPassProb(x, peril) for x in X]
        plt.plot(X, Y, label=str(peril) + comment)
    plt.xlabel('# of Hero Dice')
    plt.ylabel('Pass Probability')
    plt.legend()
    plt.title('Armello Peril')
    plt.show()

if __name__ == '__main__':
    visualize()
