# experiments/v18_6_adaptive_homeostasis/code.py

import numpy as np
import random
import copy
from collections import deque

# =========================================================
# constants
# =========================================================

BASE_SEED = 42

NODE_COUNT = 12
STEP_COUNT = 700

DIM = 8
ESSENCE_SLOTS = 3

MAX_CONNECTIONS = 4
SEARCH_K = 5

MIN_TRUST = 0.05
MAX_TRUST = 0.95

TRUST_DECAY = 0.02
UPDATE_SCALE = 0.05

TARGET_VAR_MIN = 0.02
TARGET_VAR_MAX = 0.06
TARGET_VARIANCE_CENTER = 0.036

ANOMALY_Z = 1.2

SHORT_WINDOW = 12
MID_WINDOW = 40
LONG_WINDOW = 120

ENV_DECAY = 0.992

INHERITANCE_MEMORY_LIMIT = 180
HOMEOSTASIS_MEMORY_LIMIT = 140

BASE_INHERITANCE_DECAY = 0.989

NOVELTY_BURST_PROB = 0.03

TARGET_PERSISTENCE_CENTER = 58.0

# =========================================================
# node
# =========================================================

class Node:

    def __init__(self, node_id):

        self.id = node_id

        self.essences = np.random.randn(
            ESSENCE_SLOTS,
            DIM
        )

        self.essences /= (
            np.linalg.norm(
                self.essences,
                axis=1,
                keepdims=True
            ) + 1e-8
        )

        self.trust = random.uniform(
            0.3,
            0.7
        )

        self.connections = set()

        self.persistence_counter = 0.0

        self.anomaly_score = 0.0
        self.is_anomaly = False

# =========================================================
# utility
# =========================================================

def clamp(x):

    return float(
        np.clip(x, 0.0, 1.0)
    )

def similarity(a, b):

    return np.max(
        np.dot(a, b.T)
    )

def compute_variance(nodes):

    vectors = np.array([
        e
        for n in nodes
        for e in n.essences
    ])

    return float(
        np.mean(
            np.var(vectors, axis=0)
        )
    )

def compute_density(nodes):

    total_edges = sum(
        len(n.connections)
        for n in nodes
    )

    return clamp(
        total_edges /
        (
            NODE_COUNT *
            MAX_CONNECTIONS +
            1e-8
        )
    )

def compute_persistence(nodes):

    return float(np.mean([
        n.persistence_counter
        for n in nodes
    ]))

def compute_trust_range(nodes):

    values = [
        n.trust
        for n in nodes
    ]

    return (
        max(values)
        -
        min(values)
    )

def compute_entropy(nodes):

    trusts = np.array([
        n.trust
        for n in nodes
    ])

    probs = trusts / (
        np.sum(trusts) + 1e-8
    )

    entropy = -np.sum(
        probs * np.log(probs + 1e-8)
    )

    return clamp(
        entropy / np.log(NODE_COUNT)
    )

def compute_signature(nodes):

    return tuple(sorted([
        tuple(sorted(list(n.connections)))
        for n in nodes
    ]))

def topology_overlap(a, b):

    if a is None or b is None:
        return 0.0

    overlap = 0
    total = 0

    for sa, sb in zip(a, b):

        set_a = set(sa)
        set_b = set(sb)

        overlap += len(
            set_a & set_b
        )

        total += len(
            set_a | set_b
        )

    return overlap / (
        total + 1e-8
    )

# =========================================================
# anomaly
# =========================================================

def detect_anomaly(nodes):

    trusts = np.array([
        n.trust
        for n in nodes
    ])

    mean = np.mean(trusts)

    std = np.std(trusts) + 1e-8

    for i, n in enumerate(nodes):

        z = abs(
            (
                trusts[i] - mean
            ) / std
        )

        n.anomaly_score = z

        n.is_anomaly = (
            z > ANOMALY_Z
        )

# =========================================================
# trust update
# =========================================================

def update_trust(nodes):

    scores = []

    for n in nodes:

        neighbors = [
            nodes[i]
            for i in n.connections
        ]

        if neighbors:

            sims = [
                similarity(
                    n.essences,
                    nb.essences
                )
                for nb in neighbors
            ]

            score = np.mean(sims)

        else:

            score = 0.5

        scores.append(score)

    scores = np.array(scores)

    order = np.argsort(scores)

    ranks = np.empty_like(order)

    ranks[order] = np.arange(len(nodes))

    targets = (

        MIN_TRUST +

        (
            MAX_TRUST - MIN_TRUST
        )

        * (
            ranks /
            (
                NODE_COUNT - 1 + 1e-8
            )
        )
    )

    for i, n in enumerate(nodes):

        updated = (

            (1 - TRUST_DECAY)
            * n.trust

            +

            0.48
            * (
                targets[i]
                - n.trust
            )
        )

        penalty = (

            1.0 -

            0.04 *

            (
                n.anomaly_score /
                (
                    1.0 +
                    n.anomaly_score
                )
            )
        )

        n.trust = float(
            np.clip(
                updated * penalty,
                MIN_TRUST,
                MAX_TRUST
            )
        )

# =========================================================
# inheritance
# =========================================================

def inheritance_bias_score(
    signature,
    inheritance_memory
):

    if not inheritance_memory:
        return 0.34

    overlaps = []

    for item in inheritance_memory:

        overlap = topology_overlap(
            signature,
            item["signature"]
        )

        weighted = (
            overlap *
            item["inheritance_strength"]
        )

        overlaps.append(weighted)

    overlaps.sort(reverse=True)

    top_k = overlaps[:8]

    if not top_k:
        return 0.34

    reuse_strength = (

        0.55 * np.mean(top_k)
        +
        0.45 * max(top_k)
    )

    return clamp(
        0.24 +
        reuse_strength * 0.44
    )

# =========================================================
# propagation
# =========================================================

def propagate_essences(
    nodes,
    novelty_pressure
):

    for n in nodes:

        neighbors = [
            nodes[i]
            for i in n.connections
        ]

        if not neighbors:
            continue

        for i in range(ESSENCE_SLOTS):

            src_node = random.choice(
                neighbors
            )

            src = src_node.essences[
                random.randrange(
                    ESSENCE_SLOTS
                )
            ]

            sim = np.dot(
                n.essences[i],
                src
            )

            novelty_scale = (
                1.0
                +
                0.08 *
                novelty_pressure
            )

            if sim < 0.72:

                n.essences[i] += (

                    UPDATE_SCALE
                    * novelty_scale *

                    (
                        src -
                        n.essences[i]
                    )
                )

            elif sim > 0.91:

                n.essences[i] -= (

                    UPDATE_SCALE
                    * 0.14 *

                    (
                        src -
                        n.essences[i]
                    )
                )

            if (
                random.random()
                <
                NOVELTY_BURST_PROB
                * novelty_pressure
            ):

                n.essences[i] += (

                    np.random.randn(DIM)
                    * 0.004
                )

            n.essences[i] /= (
                np.linalg.norm(
                    n.essences[i]
                ) + 1e-8
            )

# =========================================================
# rewiring
# =========================================================

def rewire(
    nodes,
    inheritance_bias,
    novelty_pressure,
    persistence_pressure,
    continuity_strength
):

    previous = {

        n.id:
        copy.deepcopy(
            n.connections
        )

        for n in nodes
    }

    for n in nodes:

        candidates = [

            c for c in nodes
            if c.id != n.id
        ]

        adaptive_inheritance = (

            inheritance_bias
            *
            (
                1.0 -
                0.28 *
                novelty_pressure
            )
        )

        scored = sorted(

            [
                (
                    (
                        0.38 *
                        c.trust

                        +

                        0.30 *
                        similarity(
                            n.essences,
                            c.essences
                        )

                        +

                        0.12 *
                        adaptive_inheritance

                        +

                        0.10 *
                        continuity_strength

                        +

                        0.10 *
                        random.random()
                        *
                        novelty_pressure
                    ),
                    c
                )

                for c in candidates
            ],

            reverse=True,
            key=lambda x: x[0]
        )

        selected = []

        for _, c in scored:

            if len(selected) >= SEARCH_K:
                break

            similarity_limit = (
                0.86
                -
                0.05 *
                novelty_pressure
            )

            if all(

                similarity(
                    c.essences,
                    s.essences
                ) < similarity_limit

                for s in selected
            ):
                selected.append(c)

        while len(selected) < SEARCH_K:

            c = random.choice(
                candidates
            )

            if c not in selected:
                selected.append(c)

        n.connections = set(

            c.id
            for c in selected[
                :MAX_CONNECTIONS
            ]
        )

        overlap = len(
            previous[n.id]
            &
            n.connections
        )

        if overlap >= 2:

            persistence_gain = (

                0.68

                +

                0.18 *
                adaptive_inheritance

                +

                0.10 *
                continuity_strength

                -

                0.26 *
                persistence_pressure

                -

                0.10 *
                novelty_pressure
            )

            persistence_gain = max(
                persistence_gain,
                0.16
            )

            n.persistence_counter += (
                persistence_gain
            )

        else:

            decay_strength = (

                0.975

                -

                0.01 *
                novelty_pressure

                +

                0.01 *
                persistence_pressure
            )

            n.persistence_counter *= (
                decay_strength
            )

        if n.persistence_counter > 80:
            n.persistence_counter = 80

# =========================================================
# variance regulation
# =========================================================

def regulate_variance(nodes):

    variance = compute_variance(nodes)

    if variance > TARGET_VAR_MAX:

        scale = np.sqrt(
            TARGET_VAR_MAX /
            (
                variance + 1e-8
            )
        )

        for n in nodes:
            n.essences *= scale

    elif variance < TARGET_VAR_MIN:

        recovery_noise = (

            0.05 +

            0.015 *

            (
                TARGET_VAR_MIN
                - variance
            )
        )

        for n in nodes:

            n.essences += (

                np.random.randn(
                    *n.essences.shape
                )

                * recovery_noise
            )

            n.essences /= (

                np.linalg.norm(
                    n.essences,
                    axis=1,
                    keepdims=True
                ) + 1e-8
            )

# =========================================================
# simulation
# =========================================================

def run_simulation(seed):

    random.seed(seed)
    np.random.seed(seed)

    nodes = [
        Node(i)
        for i in range(NODE_COUNT)
    ]

    inheritance_memory = deque(
        maxlen=INHERITANCE_MEMORY_LIMIT
    )

    homeostasis_memory = deque(
        maxlen=HOMEOSTASIS_MEMORY_LIMIT
    )

    inheritance_history = []
    novelty_history = []
    equilibrium_history = []
    recovery_history = []
    persistence_regulation_history = []
    drift_history = []

    previous_signature = None

    continuity_strength = 0.72

    homeostatic_stability = 0.68

    adaptive_drift = 0.30

    for step in range(STEP_COUNT):

        detect_anomaly(nodes)

        current_signature = compute_signature(
            nodes
        )

        inheritance_bias = (
            inheritance_bias_score(
                current_signature,
                inheritance_memory
            )
        )

        variance = compute_variance(
            nodes
        )

        persistence = compute_persistence(
            nodes
        )

        entropy = compute_entropy(
            nodes
        )

        anomaly_ratio = (
            sum(
                n.is_anomaly
                for n in nodes
            )
            / NODE_COUNT
        )

        topology_stability = clamp(
            1.0 -
            abs(
                TARGET_VARIANCE_CENTER
                - variance
            ) / TARGET_VARIANCE_CENTER
        )

        persistence_pressure = clamp(
            (
                persistence
                -
                TARGET_PERSISTENCE_CENTER
            ) / 28.0
        )

        novelty_pressure = clamp(

            0.18 *

            (
                1.0 -
                inheritance_bias
            )

            +

            0.16 *
            entropy

            +

            0.16 *
            anomaly_ratio

            +

            0.12 *
            (
                1.0 -
                continuity_strength
            )

            +

            0.20 *
            persistence_pressure

            +

            0.10
        )

        novelty_pressure *= (
            1.0
            -
            0.16 *
            homeostatic_stability
        )

        novelty_pressure = clamp(
            novelty_pressure
        )

        update_trust(nodes)

        propagate_essences(
            nodes,
            novelty_pressure
        )

        rewire(
            nodes,
            inheritance_bias,
            novelty_pressure,
            persistence_pressure,
            continuity_strength
        )

        regulate_variance(nodes)

        signature = compute_signature(
            nodes
        )

        overlap = topology_overlap(
            signature,
            previous_signature
        )

        continuity_strength = (

            ENV_DECAY *
            continuity_strength

            +

            (
                1.0 - ENV_DECAY
            )

            * max(
                overlap,
                continuity_strength * 0.992
            )
        )

        continuity_strength = clamp(
            continuity_strength
        )

        recovery_score = clamp(
            1.0 - anomaly_ratio
        )

        persistence_score = clamp(
            persistence / 80.0
        )

        adaptive_fitness = clamp(

            0.28 *
            topology_stability

            +

            0.28 *
            continuity_strength

            +

            0.20 *
            persistence_score

            +

            0.24 *
            recovery_score
        )

        adaptive_decay = clamp(
            novelty_pressure * 0.16
        )

        inheritance_strength = clamp(

            adaptive_fitness

            * (
                1.0 -
                adaptive_decay * 0.28
            )
        )

        inheritance_memory.append({

            "signature":
                signature,

            "inheritance_strength":
                inheritance_strength
        })

        for item in inheritance_memory:

            item[
                "inheritance_strength"
            ] *= (

                BASE_INHERITANCE_DECAY

                -

                0.003 *
                novelty_pressure

                +

                0.002 *
                persistence_pressure
            )

        equilibrium_score = clamp(

            1.0 -

            abs(
                inheritance_bias
                -
                novelty_pressure
            ) * 0.68

            -

            abs(
                persistence_pressure
                - 0.25
            ) * 0.25
        )

        homeostatic_stability = (

            0.94 *
            homeostatic_stability

            +

            0.06 *
            equilibrium_score
        )

        adaptive_drift = (

            0.92 *
            adaptive_drift

            +

            0.08 *
            abs(
                novelty_pressure
                -
                inheritance_bias
            )
        )

        homeostasis_memory.append({

            "equilibrium":
                equilibrium_score,

            "drift":
                adaptive_drift,

            "persistence":
                persistence_score
        })

        inheritance_history.append(
            inheritance_bias
        )

        novelty_history.append(
            novelty_pressure
        )

        equilibrium_history.append(
            equilibrium_score
        )

        recovery_history.append(
            recovery_score
        )

        persistence_regulation_history.append(
            1.0 -
            abs(
                persistence
                -
                TARGET_PERSISTENCE_CENTER
            ) / 80.0
        )

        drift_history.append(
            adaptive_drift
        )

        previous_signature = signature

    patterns = {

        tuple(sorted(
            list(n.connections)
        ))
        for n in nodes
    }

    structural_diversity = (
        len(patterns)
        / NODE_COUNT
    )

    adaptive_equilibrium_score = float(
        np.mean(
            equilibrium_history
        )
    )

    persistence_regulation_score = float(
        np.mean(
            persistence_regulation_history
        )
    )

    adaptive_drift_rate = float(
        np.mean(
            drift_history
        )
    )

    inheritance_reuse_rate = float(
        np.mean(
            inheritance_history
        )
    )

    adaptive_novelty_rate = float(
        np.mean(
            novelty_history
        )
    )

    recovery_success_rate = float(
        np.mean(
            recovery_history
        )
    )

    adaptive_homeostasis_variance = float(
        np.var(
            equilibrium_history
        )
    )

    average_persistence = (
        compute_persistence(nodes)
    )

    mean_variance = (
        compute_variance(nodes)
    )

    trust_range = (
        compute_trust_range(nodes)
    )

    validation_result = all([

        adaptive_equilibrium_score
        > 0.60,

        persistence_regulation_score
        > 0.55,

        homeostatic_stability
        > 0.60,

        adaptive_drift_rate
        < 0.36,

        0.18 <=
        inheritance_reuse_rate
        <= 0.76,

        0.12 <=
        adaptive_novelty_rate
        <= 0.68,

        continuity_strength
        > 0.48,

        recovery_success_rate
        > 0.45,

        structural_diversity
        >= 0.35,

        adaptive_homeostasis_variance
        > 0.00005,

        len(inheritance_memory)
        <= INHERITANCE_MEMORY_LIMIT,

        len(homeostasis_memory)
        <= HOMEOSTASIS_MEMORY_LIMIT,

        10.0 <=
        average_persistence
        <= 75.0,

        0.02 <=
        mean_variance
        <= 0.06,

        0.15 <=
        trust_range
        <= 0.85
    ])

    print(
        f"\n--- RUN #{seed - BASE_SEED + 1} ---"
    )

    print(
        "adaptive_equilibrium_score:",
        round(
            adaptive_equilibrium_score,
            6
        )
    )

    print(
        "persistence_regulation_score:",
        round(
            persistence_regulation_score,
            6
        )
    )

    print(
        "homeostatic_stability:",
        round(
            homeostatic_stability,
            6
        )
    )

    print(
        "adaptive_drift_rate:",
        round(
            adaptive_drift_rate,
            6
        )
    )

    print(
        "inheritance_reuse_rate:",
        round(
            inheritance_reuse_rate,
            6
        )
    )

    print(
        "adaptive_novelty_rate:",
        round(
            adaptive_novelty_rate,
            6
        )
    )

    print(
        "continuity_strength:",
        round(
            continuity_strength,
            6
        )
    )

    print(
        "recovery_success_rate:",
        round(
            recovery_success_rate,
            6
        )
    )

    print(
        "structural_diversity:",
        round(
            structural_diversity,
            6
        )
    )

    print(
        "adaptive_homeostasis_variance:",
        round(
            adaptive_homeostasis_variance,
            6
        )
    )

    print(
        "average_persistence:",
        round(
            average_persistence,
            6
        )
    )

    print(
        "mean_variance:",
        round(
            mean_variance,
            6
        )
    )

    print(
        "trust_range:",
        round(
            trust_range,
            6
        )
    )

    print(
        "validation_result:",
        validation_result
    )

    return validation_result

# =========================================================
# triple execution
# =========================================================

results = []

for seed in [42, 43, 44]:

    results.append(
        run_simulation(seed)
    )

print("\nfinal_result:")

if all(results):
    print("ACHIEVED")
else:
    print("NOT ACHIEVED")
