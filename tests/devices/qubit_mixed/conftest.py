# Copyright 2018-2024 Xanadu Quantum Technologies Inc.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Pytest configuration file for PennyLane qubit mixed state test suite."""
import numpy as np
import pytest
from scipy.stats import unitary_group


def get_random_mixed_state(num_qubits):
    """
    Generates a random mixed state for testing purposes.

    Args:
        num_qubits (int): The number of qubits in the mixed state.

    Returns:
        np.ndarray: A tensor representing the random mixed state.
    """
    dim = 2**num_qubits

    rng = np.random.default_rng(seed=4774)
    basis = unitary_group(dim=dim, seed=584545).rvs()
    schmidt_weights = rng.dirichlet(np.ones(dim), size=1).astype(complex)[0]
    mixed_state = np.zeros((dim, dim)).astype(complex)
    for i in range(dim):
        mixed_state += schmidt_weights[i] * np.outer(np.conj(basis[i]), basis[i])

    return mixed_state.reshape([2] * (2 * num_qubits))


@pytest.fixture(scope="package")
def random_mixed_state():
    return get_random_mixed_state


@pytest.fixture(scope="package")
def two_qubit_state():
    return get_random_mixed_state(2)


@pytest.fixture(scope="package")
def two_qubit_batched_state():
    return np.array([get_random_mixed_state(2) for _ in range(2)])
