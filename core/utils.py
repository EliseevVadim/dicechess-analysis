import random

import numpy as np


def init_random_seed(seed=0):
    random.seed(seed)
    np.random.seed(seed)