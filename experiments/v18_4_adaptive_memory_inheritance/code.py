# experiments/v18_4_adaptive_memory_inheritance/code.py

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

ANOMALY_Z = 1.2

SHORT_WINDOW = 12
MID_WINDOW = 40
LONG_WINDOW = 120

ENV_DECAY = 0.996

INHERITANCE_MEMORY_LIMIT = 180
INHERITANCE_DECAY = 0.994

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

        self.persistence_counter = 0

        self.anomaly_score = 0.0
        self.is_anomaly = False

        self.environmental_fitness = 0.5

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

            0.50
            * (
                targets[i]
                - n.trust
            )
        )

        penalty = (

            1.0 -

            0.05 *

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
# inheritance reuse
# =========================================================

def inheritance_bias_score(
    signature,
    inheritance_memory
):

    if not inheritance_memory:
        return 0.0

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

    top_k = overlaps[:5]

    if not top_k:
        return 0.0

    return clamp(
        np.mean(top_k)
    )

# =========================================================
# propagation
# =========================================================

def propagate_essences(
    nodes,
    inheritance_bias
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

            adaptive_scale = (

                UPDATE_SCALE *

                (
                    0.75
                    +
                    0.25 *
                    (
                        1.0 -
                        inheritance_bias
                    )
                )
            )

            if sim < 0.70:

                n.essences[i] += (

                    adaptive_scale *

                    (
                        src -
                        n.essences[i]
                    )
                )

            elif sim > 0.90:

                n.essences[i] -= (

                    adaptive_scale
                    * 0.18 *

                    (
                        src -
                        n.essences[i]
                    )
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
    env_tag,
    inheritance_bias
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

        exploration_bias = 0.35
        persistence_bias = 0.50

        if env_tag == "chaotic_environment":

            exploration_bias = 0.72
            persistence_bias = 0.22

        elif env_tag == "stable_environment":

            exploration_bias = 0.15
            persistence_bias = 0.84

        elif env_tag == "isolated_region":

            exploration_bias = 0.55
            persistence_bias = 0.38

        inheritance_weight = (
            0.12
            +
            0.22 *
            inheritance_bias
        )

        scored = sorted(

            [
                (
                    (
                        0.42 *
                        c.trust

                        +

                        0.32 *
                        similarity(
                            n.essences,
                            c.essences
                        )

                        +

                        0.12 *
                        random.random()
                        *
                        exploration_bias

                        +

                        inheritance_weight
                        *
                        persistence_bias
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

            if all(

                similarity(
                    c.essences,
                    s.essences
                ) < 0.90

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

        if overlap >= 1:

            reinforcement = (
                1
                +
                int(
                    2 *
                    inheritance_bias
                )
            )

            n.persistence_counter += reinforcement

            if n.persistence_counter > 80:
                n.persistence_counter = 80

        else:

            n.persistence_counter *= 0.996

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

        for n in nodes:

            recovery_noise = (

                0.030 +

                0.015 *

                (
                    TARGET_VAR_MIN
                    -
                    variance
                )
            )

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
# environment state
# =========================================================

def generate_environment_state(
    nodes,
    continuity_score
):

    density = compute_density(nodes)

    variance = compute_variance(nodes)

    trust_range = compute_trust_range(
        nodes
    )

    persistence = clamp(
        compute_persistence(nodes)
        / 80.0
    )

    entropy = compute_entropy(nodes)

    topology_stability = clamp(
        1.0 -
        abs(
            0.04 - variance
        ) / 0.04
    )

    divergence_pressure = clamp(
        entropy * 0.6
        +
        trust_range * 0.4
    )

    convergence_pressure = clamp(
        persistence * 0.55
        +
        continuity_score * 0.45
    )

    novelty_pressure = clamp(
        divergence_pressure
        *
        (
            1.0 -
            continuity_score * 0.4
        )
    )

    return {

        "interaction_density":
            density,

        "topology_stability":
            topology_stability,

        "divergence_pressure":
            divergence_pressure,

        "convergence_pressure":
            convergence_pressure,

        "novelty_pressure":
            novelty_pressure,

        "local_entropy":
            entropy,

        "continuity_strength":
            continuity_score
    }

# =========================================================
# environment tagging
# =========================================================

def generate_environment_tag(env):

    if (
        env["topology_stability"] > 0.72
        and
        env["continuity_strength"] > 0.55
    ):
        return "stable_environment"

    if (
        env["divergence_pressure"] > 0.65
        and
        env["novelty_pressure"] > 0.42
    ):
        return "chaotic_environment"

    if (
        env["interaction_density"] < 0.45
    ):
        return "isolated_region"

    if (
        env["convergence_pressure"] > 0.72
    ):
        return "repetitive_interaction_region"

    return "high_adaptation_region"

# =========================================================
# inheritance scoring
# =========================================================

def compute_inheritance_strength(
    fitness,
    continuity_strength,
    reuse_score,
    recovery_score
):

    inheritance_strength = (

        0.30 * fitness
        +
        0.28 * continuity_strength
        +
        0.22 * reuse_score
        +
        0.20 * recovery_score
    )

    return clamp(
        inheritance_strength
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

    short_memory = deque(
        maxlen=SHORT_WINDOW
    )

    mid_memory = deque(
        maxlen=MID_WINDOW
    )

    long_memory = deque(
        maxlen=LONG_WINDOW
    )

    inheritance_memory = deque(
        maxlen=INHERITANCE_MEMORY_LIMIT
    )

    inheritance_scores = []

    recovery_history = []

    inheritance_reuse_events = 0

    previous_signature = None

    continuity_strength = 0.82

    env_tag = "stable_environment"

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

        update_trust(nodes)

        propagate_essences(
            nodes,
            inheritance_bias
        )

        rewire(
            nodes,
            env_tag,
            inheritance_bias
        )

        regulate_variance(nodes)

        variance = compute_variance(
            nodes
        )

        persistence = compute_persistence(
            nodes
        )

        persistence_score = clamp(
            persistence / 80.0
        )

        trust_range = compute_trust_range(
            nodes
        )

        anomaly_ratio = (
            sum(
                n.is_anomaly
                for n in nodes
            )
            / NODE_COUNT
        )

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
                continuity_strength * 0.985
            )
        )

        continuity_strength = clamp(
            continuity_strength
        )

        env_state = generate_environment_state(
            nodes,
            continuity_strength
        )

        env_tag = generate_environment_tag(
            env_state
        )

        short_memory.append(env_state)

        mid_memory.append(env_state)

        long_memory.append(env_state)

        topology_stability = clamp(
            1.0 -
            abs(
                0.04 - variance
            ) / 0.04
        )

        recovery_score = clamp(
            1.0 - anomaly_ratio
        )

        adaptive_fitness = (

            0.24 *
            topology_stability

            +

            0.26 *
            continuity_strength

            +

            0.26 *
            persistence_score

            +

            0.24 *
            recovery_score
        )

        adaptive_fitness = clamp(
            adaptive_fitness
        )

        inheritance_strength = (
            compute_inheritance_strength(
                adaptive_fitness,
                continuity_strength,
                inheritance_bias,
                recovery_score
            )
        )

        inheritance_scores.append(
            inheritance_strength
        )

        if inheritance_bias > 0.20:
            inheritance_reuse_events += 1

        inheritance_memory.append({

            "signature":
                signature,

            "inheritance_strength":
                inheritance_strength,

            "fitness":
                adaptive_fitness
        })

        recovery_history.append(
            recovery_score
        )

        for item in inheritance_memory:

            item[
                "inheritance_strength"
            ] *= INHERITANCE_DECAY

        previous_signature = signature

    reusable_hits = 0

    inheritance_values = []

    for item in inheritance_memory:

        inheritance_values.append(
            item[
                "inheritance_strength"
            ]
        )

        if (
            item[
                "inheritance_strength"
            ] > 0.22
        ):
            reusable_hits += 1

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

    inheritance_reuse_rate = (

        inheritance_reuse_events
        /
        STEP_COUNT
    )

    adaptive_lineage_strength = float(
        np.mean(
            inheritance_scores
        )
    )

    inheritance_decay_rate = (

        1.0 -
        float(
            np.mean(
                inheritance_values
            )
        )
    )

    reusable_memory_ratio = (

        reusable_hits
        /
        (
            len(inheritance_memory)
            + 1e-8
        )
    )

    recovery_success_rate = float(
        np.mean(recovery_history)
    )

    adaptive_inheritance_variance = float(
        np.var(
            inheritance_scores
        )
    )

    average_persistence = (
        compute_persistence(nodes)
    )

    mean_variance = (
        compute_variance(nodes)
    )

    validation_result = all([

        0.0 <=
        inheritance_reuse_rate
        <= 1.0,

        0.0 <=
        adaptive_lineage_strength
        <= 1.0,

        0.0 <=
        inheritance_decay_rate
        <= 1.0,

        reusable_memory_ratio > 0.08,

        continuity_strength > 0.40,

        structural_diversity >= 0.35,

        recovery_success_rate > 0.40,

        adaptive_inheritance_variance > 0.0001,

        len(inheritance_memory)
        <= INHERITANCE_MEMORY_LIMIT,

        10.0 <=
        average_persistence
        <= 80.0,

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
        "inheritance_reuse_rate:",
        round(
            inheritance_reuse_rate,
            6
        )
    )

    print(
        "adaptive_lineage_strength:",
        round(
            adaptive_lineage_strength,
            6
        )
    )

    print(
        "inheritance_decay_rate:",
        round(
            inheritance_decay_rate,
            6
        )
    )

    print(
        "reusable_memory_ratio:",
        round(
            reusable_memory_ratio,
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
        "structural_diversity:",
        round(
            structural_diversity,
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
        "adaptive_inheritance_variance:",
        round(
            adaptive_inheritance_variance,
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
