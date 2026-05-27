# Agonwelt-Link v20.4.0
# localized semantic transformation
# strict validation mode

import random
import math

# ==================================================
# configuration
# ==================================================

NUM_NODES = 72
NUM_STEPS = 720

LOCAL_RADIUS = 0.24

BASE_REWIRE_RATE = 0.044
BASE_COLLAPSE_THRESHOLD = 0.30

MAX_CONNECTIONS = 8
MIN_CONNECTIONS = 2

MAX_BRIDGES = 3
MAX_DYNAMIC_PATHS = 4

DAMPING = 0.95

# bridge ecology
BRIDGE_FORMATION_RATE = 0.034
BRIDGE_DECAY_RATE = 0.988
BRIDGE_COLLAPSE_RATE = 0.036

# dynamic routing
ROUTING_FORMATION_RATE = 0.046
ROUTING_DECAY = 0.986
ROUTING_COLLAPSE_RATE = 0.040

# semantic layer
SEMANTIC_FORMATION_RATE = 0.040
SEMANTIC_DECAY = 0.992
SEMANTIC_COLLAPSE_RATE = 0.038

# fragmented persistence
PERSISTENCE_DECAY = 0.992
LOCAL_RECOVERY_SCALE = 0.016

# instability ecology
INSTABILITY_NOISE = 0.005

# semantic limits
MAX_SEMANTIC_ALIGNMENT = 0.34

# bounded diversity
MIN_DIVERGENCE = 0.14
MAX_DIVERGENCE = 0.78

# validation thresholds
MIN_SEMANTIC_DRIFT_FREQUENCY = 0.12
MIN_SEMANTIC_COLLAPSE_FLUCTUATION = 0.10
MIN_LOCALIZED_MISUNDERSTANDING = 0.08
MIN_SEMANTIC_FRICTION = 0.08
MIN_FRAGMENTED_INTERPRETATION = 0.10
MIN_SEMANTIC_PROPAGATION_INSTABILITY = 0.08
MIN_DISTRIBUTED_PERSISTENCE = 0.12
MIN_STRUCTURAL_PERSISTENCE = 0.55

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

        self.bridge_links = {}

        self.dynamic_routes = {}

        # localized semantic fragments
        self.semantic_fragments = {}

        self.local_pressure = random.uniform(
            0.40,
            0.60
        )

        self.local_stability = random.uniform(
            0.42,
            0.66
        )

        self.region_signature = random.uniform(
            0.20,
            0.80
        )

        self.structure_type = random.randint(
            0,
            3
        )

        self.persistence_field = random.uniform(
            0.10,
            0.24
        )

        self.routing_resonance = random.uniform(
            0.03,
            0.06
        )

        self.fragmentation_level = random.uniform(
            0.02,
            0.08
        )

        self.semantic_drift = random.uniform(
            0.05,
            0.10
        )

        self.semantic_friction = random.uniform(
            0.02,
            0.05
        )

        self.semantic_instability = random.uniform(
            0.04,
            0.08
        )

        self.misunderstanding_persistence = random.uniform(
            0.03,
            0.06
        )

        self.persistence_score = 1.0

        self.semantic_events = 0
        self.semantic_collapses = 0
        self.interpretation_cycles = 0

        self.instability_memory = 0.0

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
# ecology
# ==================================================

def update_ecology(nodes):

    global_divergence = (
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

    global_signature_mean = (
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

        instability = abs(
            local_density
            - local_connectivity
        )

        node.instability_memory = (
            0.95
            * node.instability_memory
            + 0.05
            * instability
        )

        node.local_pressure = (
            0.92
            * node.local_pressure
            + 0.08
            * instability
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

        # ==================================================
        # persistence
        # ==================================================

        node.persistence_field *= (
            PERSISTENCE_DECAY
        )

        node.persistence_field += (
            pressure_gap * 0.012
        )

        node.persistence_field += (
            (
                1.0
                - node.fragmentation_level
            )
            * LOCAL_RECOVERY_SCALE
            * 0.20
        )

        node.persistence_field += random.uniform(
            -INSTABILITY_NOISE,
            INSTABILITY_NOISE
        )

        node.persistence_field = clamp(
            node.persistence_field,
            0.02,
            0.82
        )

        # ==================================================
        # semantic fragment decay
        # ==================================================

        remove_semantics = []

        for target_id in list(
            node.semantic_fragments.keys()
        ):

            semantic_strength = (
                node.semantic_fragments[target_id]
            )

            semantic_strength *= (
                SEMANTIC_DECAY
            )

            semantic_strength -= random.uniform(
                0.003,
                0.010
            )

            target = nodes[target_id]

            structure_gap = abs(
                node.structure_type
                - target.structure_type
            )

            signature_gap = abs(
                node.region_signature
                - target.region_signature
            )

            semantic_loss = (
                structure_gap * 0.018
            )

            semantic_loss += (
                signature_gap * 0.040
            )

            semantic_strength -= semantic_loss

            node.semantic_friction += (
                semantic_loss * 0.40
            )

            node.semantic_drift += (
                signature_gap * 0.045
            )

            node.misunderstanding_persistence += (
                structure_gap * 0.010
            )

            if (
                random.random()
                < SEMANTIC_COLLAPSE_RATE
            ):

                semantic_strength -= random.uniform(
                    0.08,
                    0.20
                )

                node.semantic_instability += (
                    random.uniform(
                        0.010,
                        0.024
                    )
                )

            node.semantic_fragments[
                target_id
            ] = semantic_strength

            if semantic_strength <= 0.02:

                remove_semantics.append(
                    target_id
                )

        for target_id in remove_semantics:

            del node.semantic_fragments[target_id]

            node.semantic_collapses += 1

            node.interpretation_cycles += (
                random.uniform(
                    0.02,
                    0.06
                )
            )

        # ==================================================
        # local semantic transformation
        # ==================================================

        semantic_bias = (
            SEMANTIC_FORMATION_RATE
            +
            (
                pressure_gap * 0.020
            )
        )

        if (
            len(node.semantic_fragments)
            >= 3
        ):

            semantic_bias *= 0.55

        if (
            node.semantic_drift
            > 0.28
        ):

            semantic_bias *= 0.50

        if (
            random.random()
            < semantic_bias
        ):

            candidates = []

            for other in nearby:

                if other.idx == node.idx:
                    continue

                if (
                    other.idx
                    in node.semantic_fragments
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
                    signature_gap < 0.48
                    and persistence_gap < 0.28
                ):

                    candidates.append(
                        other
                    )

            if candidates:

                target = random.choice(
                    candidates
                )

                node.semantic_fragments[
                    target.idx
                ] = random.uniform(
                    0.10,
                    0.22
                )

                node.semantic_events += 1

        # ==================================================
        # fragmented semantic propagation
        # ==================================================

        if node.semantic_fragments:

            semantic_values = []

            incompatibility = []

            for target_id in node.semantic_fragments:

                target = nodes[target_id]

                semantic_values.append(
                    target.persistence_field
                )

                incompatibility.append(
                    abs(
                        target.structure_type
                        - node.structure_type
                    )
                )

            semantic_mean = (
                sum(semantic_values)
                / len(semantic_values)
            )

            incompatibility_mean = (
                sum(incompatibility)
                / len(incompatibility)
            )

            semantic_gap = abs(
                semantic_mean
                - node.persistence_field
            )

            # unstable semantic drift
            node.semantic_drift *= (
                0.993
            )

            node.semantic_drift += (
                (
                    1.0
                    - semantic_gap
                ) * 0.020
            )

            node.semantic_drift -= (
                incompatibility_mean
                * 0.002
            )

            node.semantic_drift += random.uniform(
                -0.005,
                0.005
            )

            propagation_strength = (
                0.0045
                -
                (
                    incompatibility_mean
                    * 0.0010
                )
            )

            propagation_strength = max(
                0.0010,
                propagation_strength
            )

            node.persistence_field += (
                (
                    semantic_mean
                    - node.persistence_field
                )
                * propagation_strength
            )

            # semantic misunderstanding
            if (
                semantic_gap
                < 0.08
            ):

                node.persistence_field += (
                    random.uniform(
                        -0.035,
                        0.035
                    )
                )

                node.semantic_instability += (
                    random.uniform(
                        0.006,
                        0.016
                    )
                )

                node.misunderstanding_persistence += (
                    random.uniform(
                        0.004,
                        0.012
                    )
                )

            node.semantic_drift = clamp(
                node.semantic_drift,
                0.0,
                MAX_SEMANTIC_ALIGNMENT
            )

        else:

            node.semantic_drift *= (
                0.988
            )

            node.semantic_instability += (
                random.uniform(
                    0.001,
                    0.004
                )
            )

        # ==================================================
        # decay
        # ==================================================

        node.semantic_friction *= 0.995

        node.semantic_instability *= 0.9990

        node.misunderstanding_persistence *= (
            0.998
        )

        node.fragmentation_level *= 0.992

        node.fragmentation_level += (
            random.uniform(
                -0.004,
                0.004
            )
        )

        node.fragmentation_level += (
            pressure_gap * 0.006
        )

        node.fragmentation_level = clamp(
            node.fragmentation_level,
            0.01,
            0.48
        )

        node.semantic_instability = clamp(
            node.semantic_instability,
            0.02,
            0.30
        )

        # ==================================================
        # bounded divergence
        # ==================================================

        global_offset = abs(
            node.region_signature
            - global_signature_mean
        )

        if global_divergence < 0.16:

            polarity = (
                1
                if node.region_signature
                >= global_signature_mean
                else -1
            )

            node.region_signature += (
                polarity
                * random.uniform(
                    0.022,
                    0.050
                )
            )

        elif global_divergence < 0.24:

            if global_offset < 0.10:

                node.region_signature += (
                    random.uniform(
                        -0.052,
                        0.052
                    )
                )

            else:

                node.region_signature += (
                    random.uniform(
                        -0.022,
                        0.022
                    )
                )

        elif global_divergence < 0.34:

            node.region_signature += (
                random.uniform(
                    -0.010,
                    0.010
                )
            )

        else:

            node.region_signature += (
                random.uniform(
                    -0.004,
                    0.004
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
                0.0013
                +
                node.semantic_drift
                * 0.0005
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
                -0.0028,
                0.0028
            )

            node.vy += random.uniform(
                -0.0028,
                0.0028
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

        semantic_factor = (
            node.semantic_drift
            * 0.012
        )

        rewire_rate = (
            BASE_REWIRE_RATE
            + instability * 0.022
            + semantic_factor
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

                persistence_gap = abs(
                    target.persistence_field
                    - node.persistence_field
                )

                if (
                    signature_gap > 0.46
                    and persistence_gap > 0.16
                ):

                    removable.append(cid)

            if removable:

                remove_id = random.choice(
                    removable
                )

                node.connections.remove(
                    remove_id
                )

        if (
            random.random() < (
                rewire_rate * 1.24
            )
            and len(node.connections)
            < MAX_CONNECTIONS
        ):

            compatible = []

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

                persistence_gap = abs(
                    other.persistence_field
                    - node.persistence_field
                )

                if (
                    signature_gap < 0.54
                    and persistence_gap < 0.22
                ):

                    compatible.append(
                        (
                            persistence_gap,
                            other
                        )
                    )

            compatible.sort(
                key=lambda x: x[0]
            )

            for _, target in compatible[:5]:

                if (
                    len(node.connections)
                    >= MAX_CONNECTIONS
                ):
                    break

                node.connections.add(
                    target.idx
                )

# ==================================================
# metrics
# ==================================================

def compute_metrics(nodes):

    semantic_drift_frequency = (
        sum(
            n.semantic_events
            for n in nodes
        )
        / NUM_NODES
    )

    semantic_collapse_fluctuation = (
        sum(
            n.semantic_collapses
            for n in nodes
        )
        / NUM_NODES
    )

    localized_misunderstanding_persistence = (
        sum(
            n.misunderstanding_persistence
            for n in nodes
        )
        / NUM_NODES
    )

    cross_structure_semantic_friction = (
        sum(
            n.semantic_friction
            for n in nodes
        )
        / NUM_NODES
    )

    fragmented_interpretation_cycles = (
        sum(
            n.interpretation_cycles
            for n in nodes
        )
        / NUM_NODES
    )

    semantic_propagation_instability = (
        sum(
            n.semantic_instability
            for n in nodes
        )
        / NUM_NODES
    )

    distributed_structural_persistence = (
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

    structural_persistence = (
        sum(
            1
            for n in nodes
            if len(n.connections)
            >= MIN_CONNECTIONS
        )
        / NUM_NODES
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

        "semantic_drift_frequency":
            round(
                semantic_drift_frequency,
                4
            ),

        "semantic_collapse_fluctuation":
            round(
                semantic_collapse_fluctuation,
                4
            ),

        "localized_misunderstanding_persistence":
            round(
                localized_misunderstanding_persistence,
                4
            ),

        "cross_structure_semantic_friction":
            round(
                cross_structure_semantic_friction,
                4
            ),

        "fragmented_interpretation_cycles":
            round(
                fragmented_interpretation_cycles,
                4
            ),

        "semantic_propagation_instability":
            round(
                semantic_propagation_instability,
                4
            ),

        "distributed_structural_persistence":
            round(
                distributed_structural_persistence,
                4
            ),

        "structural_persistence":
            round(
                structural_persistence,
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

    divergence_ok = (
        MIN_DIVERGENCE
        <= metrics[
            "bounded_divergence"
        ]
        <= MAX_DIVERGENCE
    )

    semantic_ok = (
        metrics[
            "semantic_propagation_instability"
        ]
        < MAX_SEMANTIC_ALIGNMENT
    )

    return all([

        metrics[
            "semantic_drift_frequency"
        ]
        >= MIN_SEMANTIC_DRIFT_FREQUENCY,

        metrics[
            "semantic_collapse_fluctuation"
        ]
        >= MIN_SEMANTIC_COLLAPSE_FLUCTUATION,

        metrics[
            "localized_misunderstanding_persistence"
        ]
        >= MIN_LOCALIZED_MISUNDERSTANDING,

        metrics[
            "cross_structure_semantic_friction"
        ]
        >= MIN_SEMANTIC_FRICTION,

        metrics[
            "fragmented_interpretation_cycles"
        ]
        >= MIN_FRAGMENTED_INTERPRETATION,

        metrics[
            "semantic_propagation_instability"
        ]
        >= MIN_SEMANTIC_PROPAGATION_INSTABILITY,

        metrics[
            "distributed_structural_persistence"
        ]
        >= MIN_DISTRIBUTED_PERSISTENCE,

        metrics[
            "structural_persistence"
        ]
        >= MIN_STRUCTURAL_PERSISTENCE,

        divergence_ok,

        semantic_ok
    ])

# ==================================================
# run
# ==================================================

def run(seed):

    random.seed(seed)

    nodes = initialize_network()

    for _ in range(NUM_STEPS):

        update_ecology(nodes)

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
