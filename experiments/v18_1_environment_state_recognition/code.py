# experiments/v18_1_environment_state_recognition/simulation.py

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

ENV_DECAY = 0.985

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

        self.trust = random.uniform(0.3, 0.7)

        self.connections = set()

        self.persistence_counter = 0

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

    return np.max(np.dot(a, b.T))

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

    values = [n.trust for n in nodes]

    return (
        max(values) - min(values)
    )

def compute_entropy(nodes):

    trusts = np.array([
        n.trust for n in nodes
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

        overlap += len(set_a & set_b)
        total += len(set_a | set_b)

    return overlap / (total + 1e-8)

# =========================================================
# anomaly
# =========================================================

def detect_anomaly(nodes):

    trusts = np.array([
        n.trust for n in nodes
    ])

    mean = np.mean(trusts)
    std = np.std(trusts) + 1e-8

    for i, n in enumerate(nodes):

        z = abs(
            (trusts[i] - mean) / std
        )

        n.anomaly_score = z
        n.is_anomaly = z > ANOMALY_Z

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

        (MAX_TRUST - MIN_TRUST)

        * (
            ranks /
            (NODE_COUNT - 1 + 1e-8)
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
                (1.0 + n.anomaly_score)
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
# propagation
# =========================================================

def propagate_essences(nodes):

    for n in nodes:

        neighbors = [
            nodes[i]
            for i in n.connections
        ]

        if not neighbors:
            continue

        for i in range(ESSENCE_SLOTS):

            src_node = random.choice(neighbors)

            src = src_node.essences[
                random.randrange(ESSENCE_SLOTS)
            ]

            sim = np.dot(
                n.essences[i],
                src
            )

            if sim < 0.70:

                n.essences[i] += (

                    UPDATE_SCALE *

                    (
                        src
                        - n.essences[i]
                    )
                )

            elif sim > 0.90:

                n.essences[i] -= (

                    UPDATE_SCALE * 0.20 *

                    (
                        src
                        - n.essences[i]
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

def rewire(nodes):

    previous = {

        n.id:
        copy.deepcopy(n.connections)

        for n in nodes
    }

    for n in nodes:

        candidates = [

            c for c in nodes
            if c.id != n.id
        ]

        scored = sorted(

            [
                (
                    0.60 * c.trust
                    +
                    0.40 * similarity(
                        n.essences,
                        c.essences
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
                ) < 0.84

                for s in selected
            ):
                selected.append(c)

        while len(selected) < SEARCH_K:

            c = random.choice(candidates)

            if c not in selected:
                selected.append(c)

        n.connections = set(

            c.id
            for c in selected[:MAX_CONNECTIONS]
        )

        overlap = len(
            previous[n.id]
            &
            n.connections
        )

        if overlap >= 2:

            n.persistence_counter += 1

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
            (variance + 1e-8)
        )

        for n in nodes:
            n.essences *= scale

    elif variance < TARGET_VAR_MIN:

        for n in nodes:

            n.essences += (

                np.random.randn(
                    *n.essences.shape
                ) * 0.01
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

    trust_range = compute_trust_range(nodes)

    persistence = clamp(
        compute_persistence(nodes) / 80.0
    )

    entropy = compute_entropy(nodes)

    activity_level = clamp(
        density * 0.8
        +
        persistence * 0.2
    )

    interaction_density = density

    topology_stability = clamp(
        1.0 -
        abs(0.04 - variance) / 0.04
    )

    divergence_pressure = clamp(
        entropy * 0.7
        +
        trust_range * 0.3
    )

    convergence_pressure = clamp(
        persistence * 0.6
        +
        continuity_score * 0.4
    )

    novelty_pressure = clamp(
        divergence_pressure
        *
        (1.0 - continuity_score)
    )

    local_entropy = entropy

    continuity_strength = continuity_score

    return {

        "activity_level":
            activity_level,

        "interaction_density":
            interaction_density,

        "topology_stability":
            topology_stability,

        "divergence_pressure":
            divergence_pressure,

        "convergence_pressure":
            convergence_pressure,

        "novelty_pressure":
            novelty_pressure,

        "local_entropy":
            local_entropy,

        "continuity_strength":
            continuity_strength
    }

# =========================================================
# environment tagging
# =========================================================

def generate_environment_tag(env):

    if (
        env["topology_stability"] > 0.72
        and
        env["continuity_strength"] > 0.70
    ):
        return "stable_environment"

    if (
        env["divergence_pressure"] > 0.68
        and
        env["novelty_pressure"] > 0.55
    ):
        return "chaotic_environment"

    if (
        env["interaction_density"] < 0.40
    ):
        return "isolated_region"

    if (
        env["convergence_pressure"] > 0.72
    ):
        return "repetitive_interaction_region"

    return "high_adaptation_region"

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

    environment_history = []

    short_memory = deque(
        maxlen=SHORT_WINDOW
    )

    mid_memory = deque(
        maxlen=MID_WINDOW
    )

    long_memory = deque(
        maxlen=LONG_WINDOW
    )

    environment_tags = []

    previous_signature = None

    continuity_strength = 0.65

    for step in range(STEP_COUNT):

        detect_anomaly(nodes)

        update_trust(nodes)

        propagate_essences(nodes)

        rewire(nodes)

        regulate_variance(nodes)

        signature = compute_signature(nodes)

        overlap = topology_overlap(
            signature,
            previous_signature
        )

        continuity_strength = (

            ENV_DECAY
            * continuity_strength

            +

            (1.0 - ENV_DECAY)
            * overlap
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

        environment_tags.append(env_tag)

        environment_history.append({

            "step": step,

            "environment_state":
                env_state,

            "environment_tag":
                env_tag
        })

        previous_signature = signature

    unique_tags = len(
        set(environment_tags)
    )

    patterns = {

        tuple(sorted(list(n.connections)))
        for n in nodes
    }

    structural_diversity = (
        len(patterns) / NODE_COUNT
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

    bounded_vectors = all([

        0.0 <= v <= 1.0

        for item in environment_history
        for v in item[
            "environment_state"
        ].values()
    ])

    memory_bounded = (

        len(short_memory) <= SHORT_WINDOW
        and
        len(mid_memory) <= MID_WINDOW
        and
        len(long_memory) <= LONG_WINDOW
    )

    reusable_environment_detection = (
        unique_tags >= 3
    )

    validation_result = all([

        bounded_vectors,

        memory_bounded,

        reusable_environment_detection,

        structural_diversity >= 0.35,

        10.0 <= average_persistence <= 80.0,

        0.02 <= mean_variance <= 0.06,

        0.15 <= trust_range <= 0.85
    ])

    print(f"\n--- RUN #{seed - BASE_SEED + 1} ---")

    print(
        "environment_history_length:",
        len(environment_history)
    )

    print(
        "unique_environment_tags:",
        unique_tags
    )

    print(
        "short_memory_size:",
        len(short_memory)
    )

    print(
        "mid_memory_size:",
        len(mid_memory)
    )

    print(
        "long_memory_size:",
        len(long_memory)
    )

    print(
        "structural_diversity:",
        round(structural_diversity, 6)
    )

    print(
        "average_persistence:",
        round(average_persistence, 6)
    )

    print(
        "mean_variance:",
        round(mean_variance, 6)
    )

    print(
        "trust_range:",
        round(trust_range, 6)
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
