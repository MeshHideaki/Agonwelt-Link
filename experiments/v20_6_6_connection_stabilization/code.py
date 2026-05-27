# Agonwelt-Link v20.6.6
# connection stabilization
# strict validation mode

import random
import math

# ==================================================
# configuration
# ==================================================

NUM_NODES = 72
NUM_STEPS = 820

LOCAL_RADIUS = 0.24

BASE_REWIRE_RATE = 0.044

MAX_CONNECTIONS = 8
MIN_CONNECTIONS = 2

DAMPING = 0.95

# stabilization layer
STABILIZATION_FORMATION_RATE = 0.040
STABILIZATION_DECAY = 0.994
STABILIZATION_COLLAPSE_RATE = 0.038

# fragmented persistence
PERSISTENCE_DECAY = 0.992
LOCAL_RECOVERY_SCALE = 0.016

# instability ecology
INSTABILITY_NOISE = 0.005

# stabilization limits
MAX_STABILIZATION_ALIGNMENT = 0.2755

# bounded diversity
MIN_DIVERGENCE = 0.14
MAX_DIVERGENCE = 0.78

# validation thresholds
MIN_CONTINUITY_STABILIZATION_FREQUENCY = 0.12
MIN_STABILIZATION_COLLAPSE_FLUCTUATION = 0.10
MIN_LOCALIZED_RECOVERY_FAILURE = 0.08
MIN_STABILIZATION_FRICTION = 0.08
MIN_FRAGMENTED_STABILIZATION_CYCLES = 0.10
MIN_STABILIZATION_PROPAGATION_INSTABILITY = 0.08
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

        self.stabilization_fragments = {}

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

        self.stabilization_drift = random.uniform(
            0.04,
            0.08
        )

        self.fragmentation_level = random.uniform(
            0.02,
            0.08
        )

        self.stabilization_friction = random.uniform(
            0.03,
            0.06
        )

        self.stabilization_instability = random.uniform(
            0.05,
            0.09
        )

        self.recovery_failure_persistence = random.uniform(
            0.05,
            0.09
        )

        self.stabilization_events = 0
        self.stabilization_collapses = 0
        self.stabilization_cycles = 0

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

        node.persistence_field *= (
            PERSISTENCE_DECAY
        )

        node.persistence_field += (
            pressure_gap * 0.010
        )

        node.persistence_field += (
            (
                1.0
                - node.fragmentation_level
            )
            * LOCAL_RECOVERY_SCALE
            * 0.18
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

        remove_stabilization = []

        for target_id in list(
            node.stabilization_fragments.keys()
        ):

            stabilization_strength = (
                node.stabilization_fragments[target_id]
            )

            stabilization_strength *= (
                STABILIZATION_DECAY
            )

            stabilization_strength -= random.uniform(
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

            stabilization_loss = (
                structure_gap * 0.018
            )

            stabilization_loss += (
                signature_gap * 0.034
            )

            stabilization_strength -= (
                stabilization_loss
            )

            node.stabilization_friction += (
                stabilization_loss * 0.36
            )

            node.stabilization_drift += (
                signature_gap * 0.017
            )

            node.recovery_failure_persistence += (
                structure_gap * 0.010
            )

            if (
                random.random()
                < 0.18
            ):

                stabilization_strength += random.uniform(
                    -0.013,
                    0.007
                )

            if (
                random.random()
                < STABILIZATION_COLLAPSE_RATE
            ):

                stabilization_strength -= random.uniform(
                    0.08,
                    0.18
                )

                node.stabilization_instability += (
                    random.uniform(
                        0.003,
                        0.009
                    )
                )

                node.recovery_failure_persistence += (
                    random.uniform(
                        0.004,
                        0.009
                    )
                )

            node.stabilization_fragments[
                target_id
            ] = stabilization_strength

            if stabilization_strength <= 0.02:

                remove_stabilization.append(
                    target_id
                )

        for target_id in remove_stabilization:

            del node.stabilization_fragments[target_id]

            node.stabilization_collapses += 1

            node.stabilization_cycles += (
                random.uniform(
                    0.02,
                    0.06
                )
            )

        stabilization_bias = (
            STABILIZATION_FORMATION_RATE
            +
            (
                pressure_gap * 0.017
            )
        )

        if (
            len(node.stabilization_fragments)
            >= 3
        ):

            stabilization_bias *= 0.55

        if (
            node.stabilization_drift
            > 0.218
        ):

            stabilization_bias *= 0.34

        if (
            random.random()
            < stabilization_bias
        ):

            candidates = []

            for other in nearby:

                if other.idx == node.idx:
                    continue

                if (
                    other.idx
                    in node.stabilization_fragments
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
                    signature_gap < 0.43
                    and persistence_gap < 0.23
                ):

                    candidates.append(
                        other
                    )

            if candidates:

                target = random.choice(
                    candidates
                )

                node.stabilization_fragments[
                    target.idx
                ] = random.uniform(
                    0.10,
                    0.16
                )

                node.stabilization_events += 1

        if node.stabilization_fragments:

            stabilization_values = []

            incompatibility = []

            for target_id in node.stabilization_fragments:

                target = nodes[target_id]

                stabilization_values.append(
                    target.persistence_field
                )

                incompatibility.append(
                    abs(
                        target.structure_type
                        - node.structure_type
                    )
                )

            stabilization_mean = (
                sum(stabilization_values)
                / len(stabilization_values)
            )

            incompatibility_mean = (
                sum(incompatibility)
                / len(incompatibility)
            )

            stabilization_gap = abs(
                stabilization_mean
                - node.persistence_field
            )

            node.stabilization_drift *= (
                0.9982
            )

            node.stabilization_drift += (
                (
                    1.0
                    - stabilization_gap
                ) * 0.0050
            )

            node.stabilization_drift -= (
                incompatibility_mean
                * 0.0031
            )

            node.stabilization_drift += random.uniform(
                -0.0007,
                0.0007
            )

            propagation_strength = (
                0.0023
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
                    stabilization_mean
                    - node.persistence_field
                )
                * propagation_strength
            )

            if (
                stabilization_gap
                < 0.08
            ):

                node.persistence_field += (
                    random.uniform(
                        -0.009,
                        0.009
                    )
                )

                node.stabilization_instability += (
                    random.uniform(
                        0.001,
                        0.0022
                    )
                )

                node.recovery_failure_persistence += (
                    random.uniform(
                        0.002,
                        0.004
                    )
                )

            node.stabilization_drift = clamp(
                node.stabilization_drift,
                0.0,
                MAX_STABILIZATION_ALIGNMENT
            )

        else:

            node.stabilization_drift *= (
                0.995
            )

            node.stabilization_instability += (
                random.uniform(
                    0.001,
                    0.0014
                )
            )

        if (
            random.random()
            < 0.020
            and len(node.connections)
            > MIN_CONNECTIONS
        ):

            removable = random.choice(
                list(node.connections)
            )

            node.connections.remove(
                removable
            )

            node.stabilization_collapses += 1

            node.recovery_failure_persistence += (
                random.uniform(
                    0.008,
                    0.013
                )
            )

        if (
            random.random()
            < 0.016
            and len(node.connections)
            < MAX_CONNECTIONS
        ):

            malformed = random.choice(
                nodes
            )

            if malformed.idx != node.idx:

                node.connections.add(
                    malformed.idx
                )

                node.stabilization_cycles += (
                    random.uniform(
                        0.004,
                        0.008
                    )
                )

        node.stabilization_friction *= 0.995

        node.stabilization_instability *= (
            0.9976
        )

        node.recovery_failure_persistence *= (
            0.9984
        )

        node.fragmentation_level *= 0.992

        node.fragmentation_level += (
            random.uniform(
                -0.003,
                0.003
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

        node.stabilization_instability = clamp(
            node.stabilization_instability,
            0.02,
            0.2755
        )

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
                    0.018,
                    0.038
                )
            )

        elif global_divergence < 0.24:

            if global_offset < 0.10:

                node.region_signature += (
                    random.uniform(
                        -0.038,
                        0.038
                    )
                )

            else:

                node.region_signature += (
                    random.uniform(
                        -0.015,
                        0.015
                    )
                )

        elif global_divergence < 0.34:

            node.region_signature += (
                random.uniform(
                    -0.005,
                    0.005
                )
            )

        else:

            node.region_signature += (
                random.uniform(
                    -0.002,
                    0.002
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
                node.stabilization_drift
                * 0.00018
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
                -0.0020,
                0.0020
            )

            node.vy += random.uniform(
                -0.0020,
                0.0020
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

        stabilization_factor = (
            node.stabilization_drift
            * 0.0045
        )

        rewire_rate = (
            BASE_REWIRE_RATE
            + instability * 0.014
            + stabilization_factor
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
                    signature_gap > 0.43
                    and persistence_gap > 0.14
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
                rewire_rate * 1.06
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
                    signature_gap < 0.45
                    and persistence_gap < 0.16
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

    continuity_stabilization_frequency = (
        sum(
            n.stabilization_events
            for n in nodes
        )
        / NUM_NODES
    )

    stabilization_collapse_fluctuation = (
        sum(
            n.stabilization_collapses
            for n in nodes
        )
        / NUM_NODES
    )

    localized_recovery_failure_persistence = (
        sum(
            n.recovery_failure_persistence
            for n in nodes
        )
        / NUM_NODES
    )

    cross_structure_stabilization_friction = (
        sum(
            n.stabilization_friction
            for n in nodes
        )
        / NUM_NODES
    )

    fragmented_stabilization_cycles = (
        sum(
            n.stabilization_cycles
            for n in nodes
        )
        / NUM_NODES
    )

    stabilization_propagation_instability = (
        sum(
            n.stabilization_instability
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

        "continuity_stabilization_frequency":
            round(
                continuity_stabilization_frequency,
                4
            ),

        "stabilization_collapse_fluctuation":
            round(
                stabilization_collapse_fluctuation,
                4
            ),

        "localized_recovery_failure_persistence":
            round(
                localized_recovery_failure_persistence,
                4
            ),

        "cross_structure_stabilization_friction":
            round(
                cross_structure_stabilization_friction,
                4
            ),

        "fragmented_stabilization_cycles":
            round(
                fragmented_stabilization_cycles,
                4
            ),

        "stabilization_propagation_instability":
            round(
                stabilization_propagation_instability,
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

    stabilization_ok = (
        metrics[
            "stabilization_propagation_instability"
        ]
        < MAX_STABILIZATION_ALIGNMENT
    )

    return all([

        metrics[
            "continuity_stabilization_frequency"
        ]
        >= MIN_CONTINUITY_STABILIZATION_FREQUENCY,

        metrics[
            "stabilization_collapse_fluctuation"
        ]
        >= MIN_STABILIZATION_COLLAPSE_FLUCTUATION,

        metrics[
            "localized_recovery_failure_persistence"
        ]
        >= MIN_LOCALIZED_RECOVERY_FAILURE,

        metrics[
            "cross_structure_stabilization_friction"
        ]
        >= MIN_STABILIZATION_FRICTION,

        metrics[
            "fragmented_stabilization_cycles"
        ]
        >= MIN_FRAGMENTED_STABILIZATION_CYCLES,

        metrics[
            "stabilization_propagation_instability"
        ]
        >= MIN_STABILIZATION_PROPAGATION_INSTABILITY,

        metrics[
            "distributed_structural_persistence"
        ]
        >= MIN_DISTRIBUTED_PERSISTENCE,

        metrics[
            "structural_persistence"
        ]
        >= MIN_STRUCTURAL_PERSISTENCE,

        divergence_ok,

        stabilization_ok
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
