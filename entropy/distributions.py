from typing import Iterable, Tuple, Callable

import numpy as np

from entropy.entropy_vec import EntropyVec


def synthetic_distributions_generators(vector_size: int, random_seed: int = 200)\
        -> Iterable[Tuple[str, Callable[[], EntropyVec]]]:
    np.random.seed(random_seed)
    yield 'Beta a=0.1 b=100', lambda: EntropyVec(np.random.beta(a=0.1, b=100, size=vector_size)).normalize()
    yield 'Beta a=0.01 b=100', lambda: EntropyVec(np.random.beta(a=0.01, b=100, size=vector_size)).normalize()
    yield 'Uniform (0-0.1)', lambda: EntropyVec(np.random.uniform(0, 0.1, size=vector_size)).normalize()
    yield 'Uniform (1-2)', lambda: EntropyVec(np.random.uniform(1, 2, size=vector_size)).normalize()
    yield 'Exponential scale=0.02', lambda: EntropyVec(np.random.exponential(scale=0.02, size=vector_size)).normalize()
    yield 'Exponential scale=0.01', lambda: EntropyVec(np.random.exponential(scale=0.01, size=vector_size)).normalize()


def synthetic_distributions(vector_size: int, random_seed: int = 200) -> Iterable[Tuple[str, EntropyVec]]:
    yield from ((name, distribution_generator())
                for name, distribution_generator in synthetic_distributions_generators(vector_size, random_seed))
