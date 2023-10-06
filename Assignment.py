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
                c0list = temp
            else:
                c0list = c0.tolist()
            c0list.insert(0, 0)
            c0list.append(0)
            temp = []
            for i in range(len(c0list)-2):
                for key in environment_dict:
                    slice = (str(c0list[i]), str(c0list[i + 1]), str(c0list[i + 2]))
                    if slice == key:
                        temp.append(environment_dict[key])
            t -= 1
            # TODO: hou per t de ct bij in een history variabele, zodat we ook het aantal veranderde cellen per
            #  discrete tijdstap kunnen bijhouden en de langste string van hetzelfde symbool
            #  (zie 2. Problem Description). Ik zou dit persoonlijk allemaal in een metadata dictionary oid zetten
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

