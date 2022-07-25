import os.path
from collections import defaultdict
from random import Random

import matplotlib.pyplot as plt
import numpy as np

from entropy.entropy_average_approximation import EntropyAverageApproximation
from entropy.entropy_poly_approximation import EntropyPolyApproximationDeg2
from entropy.entropy_poly_approximation1_deg3 import EntropyPolyApproximation1Deg3
from entropy.entropy_poly_approximation2 import EntropyPolyApproximation2
from entropy.entropy_poly_approximation2_deg3 import EntropyPolyApproximation2Deg3
from entropy.entropy_vec import EntropyVec
from sketches.clifford_entropy_sketch import CliffordEntropySketch
from utils.distributions import synthetic_distributions
from utils.functional_utils import map_list
from utils.itertools_utils import enumerate1
from utils.os_utils import join_create_dir
from utils.paths_dir import RESULTS_DIR_PATH
from utils.plotting_utils import gen_plot, plot_horizontal
import matplotlib as mpl

mpl.rcParams['pdf.fonttype'] = 42  # truetype font
mpl.rcParams['ps.fonttype'] = 42  # truetype fontfrom
mpl.rcParams['mathtext.fontset'] = 'stix'
mpl.rcParams['font.family'] = 'STIXGeneral'
mpl.rcParams['figure.autolayout'] = True
mpl.rcParams['figure.autolayout'] = True
mpl.rcParams['lines.markeredgewidth'] = 0.4


mpl.rcParams.update({'font.size': 9})


def plot_sketches_std(distribution1_name: str, entropy_vec1: EntropyVec, distribution2_name: str, entropy_vec2: EntropyVec,
                      max_sketch_size: int, save_path: str) -> None:
    prng = Random(20)
    vector_length = len(entropy_vec1)

    plt.figure(figsize=(2.4, 2.2))

    times = 50
    clifford_values = defaultdict(list)
    poly2_values = defaultdict(list)
    for time in range(times):
        print(f'{time + 1} / {times}')
        clifford = CliffordEntropySketch(max_sketch_size, vector_length, prng.randint(0, 1000000))
        for sketch_size, sketch_value in clifford.sketch_approximations(entropy_vec1, entropy_vec2):
            clifford_values[sketch_size].append(sketch_value)
        poly2 = EntropyPolyApproximationDeg2(0.0002)
        for sketch_size, sketch_value in poly2.sketch_approximations(max_sketch_size, entropy_vec1, entropy_vec2, prng.randint(0, 1000000)):
            poly2_values[sketch_size].append(sketch_value)

    plt.plot(list(clifford_values.keys()), map_list(np.std, clifford_values.values()), color='green', label='Clifford', alpha=0.85)
    plt.plot(list(poly2_values.keys()), map_list(np.std, poly2_values.values()), color='blue', label='Poly2', alpha=0.85)

    plt.legend(loc='best')
    plt.xlabel('Sketch Size')
    plt.ylabel('Standard Deviation')
    plt.xlim((0, None))
    plt.ylim((0, None))
    plt.ticklabel_format(axis='y', useMathText='true')
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close('all')


def simulate_sketches_synthetic_std(vector_length: int, max_sketch_size: int) -> None:
    distribution1_name = 'Uniform (1)'
    entropy_vec1 = EntropyVec(np.random.uniform(0.01, 1, size=vector_length)).normalize()
    distribution2_name = 'Uniform (2)'
    entropy_vec2 = EntropyVec(np.random.uniform(0.01, 1, size=vector_length)).normalize()
    print(max(entropy_vec1))
    print(max(entropy_vec2))
    result_dir_path = join_create_dir('results', 'for_paper', 'sketches_variance')
    save_path = os.path.join(result_dir_path, f'Standard_Deviation.pdf')
    plot_sketches_std(distribution1_name, entropy_vec1, distribution2_name, entropy_vec2, max_sketch_size, save_path)


if __name__ == '__main__':
    simulate_sketches_synthetic_std(vector_length=10000, max_sketch_size=1001)
