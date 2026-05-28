# Agonwelt × Gossamer
# v21.1.4
# Neural Thread Formation
# strict validation mode

import random
import math

# ==================================================
# configuration
# ==================================================

NUM_NODES = 76
NUM_STEPS = 950

LOCAL_RADIUS = 0.24

BASE_REWIRE_RATE = 0.045

MAX_CONNECTIONS = 8
MIN_CONNECTIONS = 2

DAMPING = 0.948

# neural thread ecology
THREAD_FORMATION_RATE = 0.089
THREAD_DECAY = 0.9964
THREAD_COLLAPSE_RATE = 0.031

# inheritance persistence
INHERITANCE_DECAY = 0.996

# instability
INSTABILITY_NOISE = 0.005

# synchronization limiter
MAX_NEURAL_ALIGNMENT = 0.31

# bounded diversity
MIN_DIVERGENCE = 0.15
MAX_DIVERGENCE = 0.78

# validation thresholds
MIN_THREAD_PERSISTENCE = 0.35
MAX_THREAD_PERSISTENCE = 0.72

MIN_INHERITANCE_DECAY_BALANCE = 0.20
MAX_INHERITANCE_DECAY_BALANCE = 0.55

MIN_LEGACY_DOMINANCE = 0.15
MAX_LEGACY_DOMINANCE = 0.48

MIN_FRAGMENTED_INSTABILITY = 0.08
MAX_FRAGMENTED_INSTABILITY = 0.30

MIN_DORMANT_SURVIVAL = 0.18
MAX_DORMANT_SURVIVAL = 0.60

MIN_NEURAL_FRICTION = 0.10
MAX_NEURAL_FRICTION = 0.35

# ==================================================
# node
# ==================================================

class Node:

    def __init__(self, idx):

        self.idx = idx

        self.x = random.random()
        self.y = random.random()

        self.vx = random.uniform(
            -0.005,
            0.005
        )

        self.vy = random.uniform(
            -0.005,
            0.005
        )

        self.connections = set()

        self.region_signature = random.uniform(
            0.20,
            0.80
        )

        self.structure_type = random.randint(
            0,
            4
        )

        self.persistence_field = random.uniform(
            0.10,
            0.24
        )

        self.local_pressure = random.uniform(
            0.40,
            0.60
        )

        self.local_stability = random.uniform(
            0.42,
            0.64
        )

        self.neural_threads = {}

        self.dormant_threads = {}

        self.neural_instability = random.uniform(
            0.05,
            0.09
        )

        self.neural_friction = random.uniform(
            0.04,
            0.07
        )

        self.inheritance_decay = random.uniform(
            0.14,
            0.22
        )

        self.legacy_pressure = random.uniform(
            0.10,
            0.16
        )

        self.fragmentation_level = random.uniform(
            0.02,
            0.06
        )

# ==================================================
# utility
# ==================================================

def clamp(v, lo, hi):

    return max(lo, min(hi, v))

def distance(a, b):

    return math.sqrt(
        (a.x - b.x) ** 2
        + (a.y - b.y) ** 2
    )

# ==================================================
# initialization
# ==================================================

def initialize_network():

    nodes = [Node(i) for i in range(NUM_NODES)]

    for node in nodes:

        nearby = sorted(
            nodes,
            key=lambda n: distance(node, n)
        )

        for other in nearby[1:6]:

            node.connections.add(
                other.idx
            )

    return nodes

# ==================================================
# neural ecology
# ==================================================

def update_neural_ecology(nodes):

    global_divergence = (
        max(n.region_signature for n in nodes)
        -
        min(n.region_signature for n in nodes)
    )

    global_mean = (
        sum(
            n.region_signature
            for n in nodes
        ) / NUM_NODES
    )

    for node in nodes:

        nearby = [
            other for other in nodes
            if (
                other.idx != node.idx
                and distance(node, other)
                < LOCAL_RADIUS
            )
        ]

        if not nearby:
            continue

        local_density = (
            len(nearby) / NUM_NODES
        )

        local_connectivity = (
            sum(
                len(other.connections)
                for other in nearby
            )
            /
            max(
                1,
                len(nearby)
                * MAX_CONNECTIONS
            )
        )

        instability_gap = abs(
            local_density
            - local_connectivity
        )

        node.local_pressure = (
            0.92
            * node.local_pressure
            + 0.08
            * instability_gap
        )

        node.local_stability = (
            0.90
            * node.local_stability
            + 0.10
            * local_connectivity
        )

        pressure_gap = abs(
            node.local_pressure
            - node.local_stability
        )

        node.persistence_field *= (
            INHERITANCE_DECAY
        )

        node.persistence_field += (
            pressure_gap * 0.008
        )

        node.persistence_field += random.uniform(
            -INSTABILITY_NOISE,
            INSTABILITY_NOISE
        )

        node.persistence_field = clamp(
            node.persistence_field,
            0.03,
            0.76
        )

        # ==========================================
        # thread maintenance
        # ==========================================

        remove_threads = []

        for target_id in list(
            node.neural_threads.keys()
        ):

            thread_strength = (
                node.neural_threads[target_id]
            )

            target = nodes[target_id]

            signature_gap = abs(
                node.region_signature
                - target.region_signature
            )

            structure_gap = abs(
                node.structure_type
                - target.structure_type
            )

            thread_strength *= THREAD_DECAY

            thread_strength -= (
                signature_gap * 0.014
            )

            thread_strength -= (
                structure_gap * 0.006
            )

            if (
                random.random() < 0.32
            ):

                thread_strength += random.uniform(
                    -0.007,
                    0.016
                )

            propagation = (
                0.0024
                -
                (
                    structure_gap * 0.0002
                )
            )

            propagation = max(
                0.0010,
                propagation
            )

            node.persistence_field += (
                (
                    target.persistence_field
                    - node.persistence_field
                )
                * propagation
            )

            if (
                random.random()
                < THREAD_COLLAPSE_RATE
            ):

                thread_strength -= random.uniform(
                    0.05,
                    0.09
                )

                node.neural_instability += (
                    random.uniform(
                        0.003,
                        0.007
                    )
                )

            node.neural_threads[
                target_id
            ] = thread_strength

            node.inheritance_decay += (
                signature_gap * 0.008
            )

            node.neural_friction += (
                structure_gap * 0.005
            )

            if (
                target.persistence_field
                > node.persistence_field
            ):

                node.legacy_pressure += (
                    0.0015
                )

            if thread_strength <= 0.040:

                remove_threads.append(
                    target_id
                )

        # ==========================================
        # dormant transition
        # ==========================================

        for target_id in remove_threads:

            if (
                len(node.dormant_threads)
                < 2
            ):

                residual = random.uniform(
                    0.015,
                    0.040
                )

                node.dormant_threads[
                    target_id
                ] = residual

            del node.neural_threads[
                target_id
            ]

        # ==========================================
        # dormant
        # ==========================================

        remove_dormant = []

        for target_id in list(
            node.dormant_threads.keys()
        ):

            dormant_strength = (
                node.dormant_threads[target_id]
            )

            dormant_strength *= 0.980

            dormant_strength += random.uniform(
                -0.002,
                0.001
            )

            node.dormant_threads[
                target_id
            ] = dormant_strength

            if (
                dormant_strength > 0.022
                and random.random() < 0.030
            ):

                node.neural_threads[
                    target_id
                ] = random.uniform(
                    0.10,
                    0.16
                )

                remove_dormant.append(
                    target_id
                )

            elif dormant_strength <= 0.010:

                remove_dormant.append(
                    target_id
                )

        for target_id in remove_dormant:

            if target_id in node.dormant_threads:

                del node.dormant_threads[
                    target_id
                ]

        # ==========================================
        # formation
        # ==========================================

        formation_bias = (
            THREAD_FORMATION_RATE
            +
            (
                pressure_gap * 0.014
            )
        )

        if (
            len(node.neural_threads)
            >= 5
        ):

            formation_bias *= 0.72

        if (
            len(node.neural_threads)
            >= 7
        ):

            formation_bias *= 0.58

        if (
            node.legacy_pressure
            > 0.34
        ):

            formation_bias *= 0.82

        if (
            random.random()
            < formation_bias
        ):

            candidates = []

            for other in nearby:

                if (
                    other.idx
                    in node.neural_threads
                ):
                    continue

                signature_gap = abs(
                    other.region_signature
                    - node.region_signature
                )

                persistence_gap = abs(
                    other.persistence_field
                    - node.persistence_field
                )

                if (
                    signature_gap < 0.41
                    and persistence_gap < 0.18
                ):

                    candidates.append(
                        other
                    )

            if candidates:

                target = random.choice(
                    candidates
                )

                node.neural_threads[
                    target.idx
                ] = random.uniform(
                    0.10,
                    0.18
                )

        # ==========================================
        # fragmentation
        # ==========================================

        node.fragmentation_level *= 0.994

        node.fragmentation_level += (
            pressure_gap * 0.004
        )

        node.fragmentation_level += random.uniform(
            -0.002,
            0.002
        )

        node.fragmentation_level = clamp(
            node.fragmentation_level,
            0.01,
            0.40
        )

        # ==========================================
        # instability
        # ==========================================

        node.neural_instability *= 0.997

        node.neural_instability += (
            node.fragmentation_level
            * 0.0015
        )

        node.neural_instability = clamp(
            node.neural_instability,
            0.02,
            MAX_NEURAL_ALIGNMENT
        )

        # ==========================================
        # inheritance decay
        # ==========================================

        node.inheritance_decay *= 0.996

        node.inheritance_decay += (
            pressure_gap * 0.0025
        )

        node.inheritance_decay = clamp(
            node.inheritance_decay,
            0.08,
            0.55
        )

        # ==========================================
        # legacy pressure
        # ==========================================

        node.legacy_pressure *= 0.994

        node.legacy_pressure += (
            len(node.neural_threads)
            * 0.00035
        )

        node.legacy_pressure += (
            len(node.dormant_threads)
            * 0.00020
        )

        node.legacy_pressure = clamp(
            node.legacy_pressure,
            0.03,
            0.50
        )

        # ==========================================
        # friction
        # ==========================================

        node.neural_friction *= 0.995

        node.neural_friction += (
            node.fragmentation_level
            * 0.0010
        )

        node.neural_friction = clamp(
            node.neural_friction,
            0.03,
            0.348
        )

        # ==========================================
        # divergence
        # ==========================================

        global_offset = abs(
            node.region_signature
            - global_mean
        )

        if global_divergence < 0.18:

            polarity = (
                1
                if node.region_signature
                >= global_mean
                else -1
            )

            node.region_signature += (
                polarity
                * random.uniform(
                    0.011,
                    0.024
                )
            )

        elif global_divergence < 0.28:

            if global_offset < 0.10:

                node.region_signature += (
                    random.uniform(
                        -0.020,
                        0.020
                    )
                )

        else:

            node.region_signature += (
                random.uniform(
                    -0.003,
                    0.003
                )
            )

        node.region_signature = clamp(
            node.region_signature,
            0.01,
            0.99
        )

# ==================================================
# movement
# ==================================================

def update_positions(nodes):

    for node in nodes:

        nearby = [
            other for other in nodes
            if (
                other.idx != node.idx
                and distance(node, other)
                < LOCAL_RADIUS
            )
        ]

        if nearby:

            cx = (
                sum(
                    n.x for n in nearby
                ) / len(nearby)
            )

            cy = (
                sum(
                    n.y for n in nearby
                ) / len(nearby)
            )

            cohesion_strength = (
                0.0010
                +
                (
                    min(
                        5,
                        len(node.neural_threads)
                    )
                    * 0.00006
                )
            )

            node.vx += (
                (cx - node.x)
                * cohesion_strength
            )

            node.vy += (
                (cy - node.y)
                * cohesion_strength
            )

            node.vx += random.uniform(
                -0.002,
                0.002
            )

            node.vy += random.uniform(
                -0.002,
                0.002
            )

        node.vx *= DAMPING
        node.vy *= DAMPING

        node.x += node.vx
        node.y += node.vy

        node.x = clamp(
            node.x,
            0.0,
            1.0
        )

        node.y = clamp(
            node.y,
            0.0,
            1.0
        )

# ==================================================
# rewiring
# ==================================================

def update_connections(nodes):

    for node in nodes:

        nearby = [
            other for other in nodes
            if (
                other.idx != node.idx
                and distance(node, other)
                < LOCAL_RADIUS
            )
        ]

        if not nearby:
            continue

        instability = abs(
            node.local_pressure
            - node.local_stability
        )

        rewire_rate = (
            BASE_REWIRE_RATE
            + instability * 0.013
        )

        if (
            random.random() < rewire_rate
            and len(node.connections)
            > MIN_CONNECTIONS
        ):

            removable = []

            for cid in node.connections:

                target = nodes[cid]

                signature_gap = abs(
                    target.region_signature
                    - node.region_signature
                )

                if signature_gap > 0.40:

                    removable.append(cid)

            if removable:

                remove_id = random.choice(
                    removable
                )

                node.connections.remove(
                    remove_id
                )

        if (
            random.random()
            < rewire_rate * 1.04
            and len(node.connections)
            < MAX_CONNECTIONS
        ):

            candidates = []

            for other in nearby:

                if (
                    other.idx
                    in node.connections
                ):
                    continue

                signature_gap = abs(
                    other.region_signature
                    - node.region_signature
                )

                if signature_gap < 0.38:

                    candidates.append(other)

            if candidates:

                target = random.choice(
                    candidates
                )

                node.connections.add(
                    target.idx
                )

# ==================================================
# metrics
# ==================================================

def compute_metrics(nodes):

    neural_thread_persistence = (
        sum(
            len(n.neural_threads)
            for n in nodes
        )
        /
        (
            NUM_NODES * 3.1
        )
    )

    inheritance_decay_balance = (
        sum(
            n.inheritance_decay
            for n in nodes
        )
        / NUM_NODES
    )

    legacy_dominance_pressure = (
        sum(
            n.legacy_pressure
            for n in nodes
        )
        / NUM_NODES
    )

    fragmented_neural_instability = (
        sum(
            n.neural_instability
            for n in nodes
        )
        / NUM_NODES
    )

    dormant_thread_survival = (
        sum(
            len(n.dormant_threads)
            for n in nodes
        )
        /
        (
            NUM_NODES * 2.0
        )
    )

    cross_structure_neural_friction = (
        sum(
            n.neural_friction
            for n in nodes
        )
        / NUM_NODES
    )

    distributed_inheritance_persistence = (
        max(
            n.persistence_field
            for n in nodes
        )
        -
        min(
            n.persistence_field
            for n in nodes
        )
    )

    bounded_divergence = (
        max(
            n.region_signature
            for n in nodes
        )
        -
        min(
            n.region_signature
            for n in nodes
        )
    )

    return {

        "neural_thread_persistence":
            round(
                neural_thread_persistence,
                4
            ),

        "inheritance_decay_balance":
            round(
                inheritance_decay_balance,
                4
            ),

        "legacy_dominance_pressure":
            round(
                legacy_dominance_pressure,
                4
            ),

        "fragmented_neural_instability":
            round(
                fragmented_neural_instability,
                4
            ),

        "dormant_thread_survival":
            round(
                dormant_thread_survival,
                4
            ),

        "cross_structure_neural_friction":
            round(
                cross_structure_neural_friction,
                4
            ),

        "distributed_inheritance_persistence":
            round(
                distributed_inheritance_persistence,
                4
            ),

        "bounded_divergence":
            round(
                bounded_divergence,
                4
            ),
    }

# ==================================================
# validation
# ==================================================

def validate(metrics):

    return all([

        MIN_THREAD_PERSISTENCE
        <= metrics[
            "neural_thread_persistence"
        ]
        <= MAX_THREAD_PERSISTENCE,

        MIN_INHERITANCE_DECAY_BALANCE
        <= metrics[
            "inheritance_decay_balance"
        ]
        <= MAX_INHERITANCE_DECAY_BALANCE,

        MIN_LEGACY_DOMINANCE
        <= metrics[
            "legacy_dominance_pressure"
        ]
        <= MAX_LEGACY_DOMINANCE,

        MIN_FRAGMENTED_INSTABILITY
        <= metrics[
            "fragmented_neural_instability"
        ]
        <= MAX_FRAGMENTED_INSTABILITY,

        MIN_DORMANT_SURVIVAL
        <= metrics[
            "dormant_thread_survival"
        ]
        <= MAX_DORMANT_SURVIVAL,

        MIN_NEURAL_FRICTION
        <= metrics[
            "cross_structure_neural_friction"
        ]
        <= MAX_NEURAL_FRICTION,

        MIN_DIVERGENCE
        <= metrics[
            "bounded_divergence"
        ]
        <= MAX_DIVERGENCE,
    ])

# ==================================================
# run
# ==================================================

def run(seed):

    random.seed(seed)

    nodes = initialize_network()

    for _ in range(NUM_STEPS):

        update_neural_ecology(nodes)

        update_positions(nodes)

        update_connections(nodes)

    metrics = compute_metrics(nodes)

    validation_result = validate(
        metrics
    )

    return (
        metrics,
        validation_result
    )

# ==================================================
# strict validation
# ==================================================

overall = True

for seed in [42, 43, 44]:

    print(f"\n--- RUN #{seed} ---")

    metrics, validation_result = run(
        seed
    )

    for k, v in metrics.items():

        print(f"{k}: {v}")

    print(
        f"validation_result: "
        f"{validation_result}"
    )

    if not validation_result:

        overall = False

print("\nfinal_result:")

if overall:

    print("ACHIEVED")

else:

    print("NOT ACHIEVED")
