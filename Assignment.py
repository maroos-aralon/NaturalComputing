import typing
import numpy as np


class CellularAutomata:
    """Skeleton CA, you should implement this."""

    def __init__(self, rule_number: int):
        """Intialize the cellular automaton with a given rule number"""
        self.rule_number = rule_number

    def __call__(self, c0: typing.List[int], t: int) -> typing.List[int]:
        """Evaluate for T timesteps. Return Ct for a given C0."""
        binary_rule = [eval(i) for i in list(f'{self.rule_number:08b}')]
        environments = []
        for i in reversed(range(8)):
            environments.append(tuple(np.binary_repr(i, 3)))
        environment_dict = dict(zip(environments, binary_rule))
        # value rule 30: {('1', '1', '1'): 0, ('1', '1', '0'): 0, ('1', '0', '1'): 0, ('1', '0', '0'): 1,
        # ('0', '1', '1'): 1, ('0', '1', '0'): 1, ('0', '0', '1'): 1, ('0', '0', '0'): 0}
        temp = []
        while t > 0:
            if temp:
                c0 = temp
            np.insert(c0, 0, 0)
            np.append(c0, 0)
            temp = []
            for i in range(len(c0)-2):
                for key in environment_dict:
                    # ToDo: get c0 slice & key in the same format
                    if tuple(c0[slice(i, i+3)]) == key:
                        np.append(temp, environment_dict[key])
                        print(key)
                    else:
                        print(tuple(c0[slice(i, i+3)]))
                        # (0, 0, 0)
                        print("is not")
                        print(key)
                        # ('0', '0', '0')
                
            t -= 1
        print(temp)
        res = temp
        return res

    @classmethod
    def test(cls, rule_number, c0, ct, t=1):
        ca = cls(rule_number)
        ct_prime = ca(c0, t)
        assert all(trial == expected for trial, expected in zip(ct_prime, ct))


if __name__ == "__main__":
    "If the following statements do not produce an error, your CA works correctly."
    x0 = np.zeros(7, dtype=int)
    x0[x0.size // 2] = 1
    CellularAutomata.test(0, x0, np.zeros(7, dtype=int)) # t = 1
    CellularAutomata.test(30, x0, [0, 1, 1, 0, 0, 1, 0], 2)

