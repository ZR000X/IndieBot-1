import math


def collatz(n: int) -> int:
    if n % 2 == 0:
        return n // 2
    return 3 * n + 1


class collatz_info:
    def __init__(self, root: int):
        assert (root != 0)
        self.collatz_trajectory = []
        self.oddinity_trajectory = []
        self.evenity_trajectory = []
        self.limit_reached = False
        evenity = 0
        self.stopping_time = 0
        stopped = False
        self.collatz_trajectory.append(root)
        self.oddinity_trajectory.append(root)
        i = 0
        while not i in self.collatz_trajectory[:-1] and len(self.collatz_trajectory) < 5000:
            # get next collatz i
            if i == 0:
                i = collatz(root)
            else:
                i = collatz(i)
                # check if "stopped": we've reached a lower point than we started at
            if not stopped and abs(i) <= abs(root):
                self.stopping_time = len(self.collatz_trajectory)
                stopped = True
            # add to other trajectories
            if i % 2 == 0:
                evenity += 1
            else:
                self.evenity_trajectory.append(evenity)
                self.oddinity_trajectory.append(i)
                evenity = 0
            self.collatz_trajectory.append(i)
        if len(self.collatz_trajectory) == 1000:
            self.limit_reached = True


def multimod(a: int, b: int) -> int:
    if b == 0:
        return math.inf
    if a == 0:
        return 0
    if b == 1:
        return a
    iterations = 0
    while a % b == 0:
        assert (iterations < 2000)
        a /= b
        iterations += 1
    return int(a)


def oddinity(a: int) -> int:
    return multimod(a, 2)


def evenity(a: int) -> int:
    out = 0
    while a % 2 == 0:
        a /= 2
        out += 1
    return out
