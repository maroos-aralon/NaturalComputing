import typing
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['image.cmap'] = 'binary'


class CellularAutomata:

    def __init__(self, rule_number: int):
        """Intialize the cellular automaton with a given rule number"""
        self.rule_number = rule_number

    def metadata(self, history):
        cells_changed = []
        zero_count = []
        largest_equal = []  # bedoelen ze hiermee per tijdsstap of in totaal?
        # /\ lijkt me trouwens niet perse nodig voor het bepalen van Wolfram class

        for t_i in range(len(history)):
            t = history[t_i]
            zero_count.append(t.count(0))
            cells_changed.append(0)
            if "prev_t" in locals():
                for i in range(len(t)):
                    if prev_t[i] != t[i]:
                        cells_changed[t_i] += 1
                prev_t = t
            else:
                prev_t = t
                continue

        return cells_changed, zero_count

    def __call__(self, c0: typing.List[int], t: int) -> typing.List[int]:
        """Evaluate for T timesteps. Return Ct for a given C0."""
        # creating the necessary variables
        binary_rule = [eval(i) for i in list(f'{self.rule_number:08b}')]
        environments = []
        for i in reversed(range(8)):
            environments.append(tuple(np.binary_repr(i, 3)))
        environment_dict = dict(zip(environments, binary_rule))

        # creating each timestep for the CA
        temp = []
        history = [c0.tolist()]
        initial_time = t
        while t > 0:
            if temp:
                c0list = temp
            else:
                c0list = history[0]
            c0list.insert(0, 0)
            c0list.append(0)
            temp = []
            for i in range(len(c0list) - 2):
                for key in environment_dict:
                    slice = (str(c0list[i]), str(c0list[i + 1]), str(c0list[i + 2]))
                    if slice == key:
                        temp.append(environment_dict[key])
            t -= 1
            history.append(temp)

        # the following is a bit of convoluted code, but for now the only possibility to make it work
        final_temp = temp.copy()
        final_temp.insert(0, 0)
        final_temp.append(0)
        history[-1] = final_temp
        #########################

        # Printing metadata
        metadata = self.metadata(history)
        print(f'rule number: {self.rule_number}, t: {initial_time}')
        for time in range(len(history)):
            print(f't:{time}', end=" ")
            # print(history[time], end=" ")
            print(f'Cells changed:{metadata[0][time]}', end=" ")
            print(f'Amount of zeros:{metadata[1][time]}')

        # Plotting the CAs
        fig, ax = plt.subplots()
        ax.matshow(history)
        ax.set_title(f'rule {self.rule_number}')
        ax.get_xaxis().set_ticks([])
        ax.set_xlabel(f'array of {len(x0)}')
        ax.set_ylabel('t')
        plt.show()

        res = temp
        return res

    @classmethod
    def run(cls, rule_number, c0, t=1):
        ca = cls(rule_number)
        ca(c0, t)

    @classmethod
    def test(cls, rule_number, c0, ct, t=1):
        ca = cls(rule_number)
        ct_prime = ca(c0, t)
        assert all(trial == expected for trial, expected in zip(ct_prime, ct))


if __name__ == "__main__":
    # test
    "If the following statements do not produce an error, your CA works correctly."
    x0 = np.zeros(7, dtype=int)
    x0[x0.size // 2] = 1
    CellularAutomata.test(0, x0, np.zeros(7, dtype=int))  # t = 1
    CellularAutomata.test(30, x0, [0, 1, 1, 0, 0, 1, 0], 2)
    CellularAutomata.test(30, x0, [1, 1, 1, 1, 1, 0, 0], 5)

    # own input
    x0 = np.zeros(30, dtype=int)
    x0[x0.size // 2] = 1

    CellularAutomata.run(30, x0, 10)
    CellularAutomata.run(49, x0, 40)
    CellularAutomata.run(13, x0, 40)
    CellularAutomata.run(45, x0, 40)
    CellularAutomata.run(129, x0, 100)


