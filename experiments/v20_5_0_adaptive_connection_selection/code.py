# Agonwelt-Link v20.5.0
# adaptive connection selection
# strict validation mode

import random
import math

# ==================================================
# configuration
# ==================================================

NUM_NODES = 72
NUM_STEPS = 760

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

# adaptive selection
PRUNING_FORMATION_RATE = 0.042
PRUNING_DECAY = 0.993
PRUNING_COLLAPSE_RATE = 0.041

# fragmented persistence
PERSISTENCE_DECAY = 0.992
LOCAL_RECOVERY_SCALE = 0.016

# instability ecology
INSTABILITY_NOISE = 0.005

# adaptive limits
MAX_SELECTION_ALIGNMENT = 0.34

# bounded diversity
MIN_DIVERGENCE = 0.14
MAX_DIVERGENCE = 0.78

# validation thresholds
MIN_ADAPTIVE_PRUNING_FREQUENCY = 0.12
MIN_SELECTION_COLLAPSE_FLUCTUATION = 0.10
MIN_LOCALIZED_MALADAPTATION = 0.08
MIN_SELECTION_FRICTION = 0.08
MIN_FRAGMENTED_PRUNING_CYCLES = 0.10
MIN_SELECTION_PROPAGATION_INSTABILITY = 0.08
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

        self.semantic_fragments = {}

        # adaptive pruning fragments
        self.pruning_fragments = {}

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

        self.selection_drift = random.uniform(
            0.05,
            0.10
        )

        self.fragmentation_level = random.uniform(
            0.02,
            0.08
        )

        self.selection_friction = random.uniform(
            0.02,
            0.05
        )

        self.selection_instability = random.uniform(
            0.04,
            0.08
        )

        self.maladaptation_persistence = random.uniform(
            0.03,
            0.06
        )

        self.persistence_score = 1.0

        self.pruning_events = 0
        self.selection_collapses = 0
        self.pruning_cycles = 0

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
        # adaptive pruning decay
        # ==================================================

        remove_pruning = []

        for target_id in list(
            node.pruning_fragments.keys()
        ):

            pruning_strength = (
                node.pruning_fragments[target_id]
            )

            pruning_strength *= (
                PRUNING_DECAY
            )

            pruning_strength -= random.uniform(
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

            pruning_loss = (
                structure_gap * 0.018
            )

            pruning_loss += (
                signature_gap * 0.040
            )

            pruning_strength -= pruning_loss

            node.selection_friction += (
                pruning_loss * 0.40
            )

            node.selection_drift += (
                signature_gap * 0.045
            )

            node.maladaptation_persistence += (
                structure_gap * 0.012
            )

            # maladaptive pruning
            if (
                random.random()
                < 0.18
            ):

                pruning_strength -= random.uniform(
                    0.010,
                    0.040
                )

                node.maladaptation_persistence += (
                    random.uniform(
                        0.004,
                        0.012
                    )
                )

            if (
                random.random()
                < PRUNING_COLLAPSE_RATE
            ):

                pruning_strength -= random.uniform(
                    0.08,
                    0.20
                )

                node.selection_instability += (
                    random.uniform(
                        0.010,
                        0.024
                    )
                )

            node.pruning_fragments[
                target_id
            ] = pruning_strength

            if pruning_strength <= 0.02:

                remove_pruning.append(
                    target_id
                )

        for target_id in remove_pruning:

            del node.pruning_fragments[target_id]

            node.selection_collapses += 1

            node.pruning_cycles += (
                random.uniform(
                    0.02,
                    0.06
                )
            )

        # ==================================================
        # localized adaptive pruning
        # ==================================================

        pruning_bias = (
            PRUNING_FORMATION_RATE
            +
            (
                pressure_gap * 0.020
            )
        )

        if (
            len(node.pruning_fragments)
            >= 3
        ):

            pruning_bias *= 0.55

        if (
            node.selection_drift
            > 0.28
        ):

            pruning_bias *= 0.50

        if (
            random.random()
            < pruning_bias
        ):

            candidates = []

            for other in nearby:

                if other.idx == node.idx:
                    continue

                if (
                    other.idx
                    in node.pruning_fragments
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

                node.pruning_fragments[
                    target.idx
                ] = random.uniform(
                    0.10,
                    0.22
                )

                node.pruning_events += 1

        # ==================================================
        # fragmented adaptive propagation
        # ==================================================

        if node.pruning_fragments:

            pruning_values = []

            incompatibility = []

            for target_id in node.pruning_fragments:

                target = nodes[target_id]

                pruning_values.append(
                    target.persistence_field
                )

                incompatibility.append(
                    abs(
                        target.structure_type
                        - node.structure_type
                    )
                )

            pruning_mean = (
                sum(pruning_values)
                / len(pruning_values)
            )

            incompatibility_mean = (
                sum(incompatibility)
                / len(incompatibility)
            )

            pruning_gap = abs(
                pruning_mean
                - node.persistence_field
            )

            node.selection_drift *= (
                0.993
            )

            node.selection_drift += (
                (
                    1.0
                    - pruning_gap
                ) * 0.020
            )

            node.selection_drift -= (
                incompatibility_mean
                * 0.002
            )

            node.selection_drift += random.uniform(
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
                    pruning_mean
                    - node.persistence_field
                )
                * propagation_strength
            )

            # maladaptive propagation
            if (
                pruning_gap
                < 0.08
            ):

                node.persistence_field += (
                    random.uniform(
                        -0.035,
                        0.035
                    )
                )

                node.selection_instability += (
                    random.uniform(
                        0.006,
                        0.016
                    )
                )

                node.maladaptation_persistence += (
                    random.uniform(
                        0.004,
                        0.012
                    )
                )

            node.selection_drift = clamp(
                node.selection_drift,
                0.0,
                MAX_SELECTION_ALIGNMENT
            )

        else:

            node.selection_drift *= (
                0.988
            )

            node.selection_instability += (
                random.uniform(
                    0.001,
                    0.004
                )
            )

        # ==================================================
        # unstable pruning collapse
        # ==================================================

        if (
            random.random()
            < 0.024
            and len(node.connections)
            > MIN_CONNECTIONS
        ):

            removable = random.choice(
                list(node.connections)
            )

            node.connections.remove(
                removable
            )

            node.selection_collapses += 1

            node.maladaptation_persistence += (
                random.uniform(
                    0.010,
                    0.024
                )
            )

        # ==================================================
        # maladaptive reconnection
        # ==================================================

        if (
            random.random()
            < 0.020
            and len(node.connections)
            < MAX_CONNECTIONS
        ):

            malformed = random.choice(
                nodes
            )

            if (
                malformed.idx != node.idx
            ):

                node.connections.add(
                    malformed.idx
                )

                node.pruning_cycles += (
                    random.uniform(
                        0.006,
                        0.020
                    )
                )

        # ==================================================
        # decay
        # ==================================================

        node.selection_friction *= 0.995

        node.selection_instability *= 0.9990

        node.maladaptation_persistence *= (
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

        node.selection_instability = clamp(
            node.selection_instability,
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
                node.selection_drift
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

        adaptive_factor = (
            node.selection_drift
            * 0.012
        )

        rewire_rate = (
            BASE_REWIRE_RATE
            + instability * 0.022
            + adaptive_factor
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

    adaptive_pruning_frequency = (
        sum(
            n.pruning_events
            for n in nodes
        )
        / NUM_NODES
    )

    selection_collapse_fluctuation = (
        sum(
            n.selection_collapses
            for n in nodes
        )
        / NUM_NODES
    )

    localized_maladaptation_persistence = (
        sum(
            n.maladaptation_persistence
            for n in nodes
        )
        / NUM_NODES
    )

    cross_structure_selection_friction = (
        sum(
            n.selection_friction
            for n in nodes
        )
        / NUM_NODES
    )

    fragmented_pruning_cycles = (
        sum(
            n.pruning_cycles
            for n in nodes
        )
        / NUM_NODES
    )

    selection_propagation_instability = (
        sum(
            n.selection_instability
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

        "adaptive_pruning_frequency":
            round(
                adaptive_pruning_frequency,
                4
            ),

        "selection_collapse_fluctuation":
            round(
                selection_collapse_fluctuation,
                4
            ),

        "localized_maladaptation_persistence":
            round(
                localized_maladaptation_persistence,
                4
            ),

        "cross_structure_selection_friction":
            round(
                cross_structure_selection_friction,
                4
            ),

        "fragmented_pruning_cycles":
            round(
                fragmented_pruning_cycles,
                4
            ),

        "selection_propagation_instability":
            round(
                selection_propagation_instability,
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

    adaptive_ok = (
        metrics[
            "selection_propagation_instability"
        ]
        < MAX_SELECTION_ALIGNMENT
    )

    return all([

        metrics[
            "adaptive_pruning_frequency"
        ]
        >= MIN_ADAPTIVE_PRUNING_FREQUENCY,

        metrics[
            "selection_collapse_fluctuation"
        ]
        >= MIN_SELECTION_COLLAPSE_FLUCTUATION,

        metrics[
            "localized_maladaptation_persistence"
        ]
        >= MIN_LOCALIZED_MALADAPTATION,

        metrics[
            "cross_structure_selection_friction"
        ]
        >= MIN_SELECTION_FRICTION,

        metrics[
            "fragmented_pruning_cycles"
        ]
        >= MIN_FRAGMENTED_PRUNING_CYCLES,

        metrics[
            "selection_propagation_instability"
        ]
        >= MIN_SELECTION_PROPAGATION_INSTABILITY,

        metrics[
            "distributed_structural_persistence"
        ]
        >= MIN_DISTRIBUTED_PERSISTENCE,

        metrics[
            "structural_persistence"
        ]
        >= MIN_STRUCTURAL_PERSISTENCE,

        divergence_ok,

        adaptive_ok
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
