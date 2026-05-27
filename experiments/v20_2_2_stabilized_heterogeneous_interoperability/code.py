# Agonwelt-Link v20.2.2
# stabilized heterogeneous interoperability
# strict validation mode

import random
import math

# ==================================================
# configuration
# ==================================================

NUM_NODES = 72
NUM_STEPS = 640

LOCAL_RADIUS = 0.24

BASE_REWIRE_RATE = 0.042
BASE_COLLAPSE_THRESHOLD = 0.29

MAX_CONNECTIONS = 8
MIN_CONNECTIONS = 2

MAX_BRIDGES = 3

DAMPING = 0.95

# bridge ecology
BRIDGE_FORMATION_RATE = 0.034
BRIDGE_DECAY_RATE = 0.988
BRIDGE_COLLAPSE_RATE = 0.036

# fragmented persistence
PERSISTENCE_DECAY = 0.992
LOCAL_RECOVERY_SCALE = 0.016

# instability ecology
INSTABILITY_NOISE = 0.005

# heterogeneous friction
MAX_COMPATIBILITY_ALIGNMENT = 0.34

# bounded diversity
MIN_DIVERGENCE = 0.14
MAX_DIVERGENCE = 0.78

# validation thresholds
MIN_HETEROGENEOUS_BRIDGE_FREQUENCY = 0.08
MIN_COMPATIBILITY_INSTABILITY = 0.08
MIN_TRANSLATION_LOSS = 0.08
MIN_CROSS_STRUCTURE_COLLAPSE = 0.14
MIN_LOCALIZED_INTEROPERABILITY = 0.10
MIN_BRIDGE_FRICTION = 0.06
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

        # stabilized partial compatibility
        self.compatibility_resonance = random.uniform(
            0.03,
            0.06
        )

        self.fragmentation_level = random.uniform(
            0.02,
            0.08
        )

        self.translation_loss = random.uniform(
            0.01,
            0.03
        )

        self.bridge_friction = random.uniform(
            0.01,
            0.03
        )

        self.persistence_score = 1.0

        self.collapse_events = 0
        self.recovery_events = 0

        self.bridge_events = 0
        self.bridge_collapses = 0

        self.cross_structure_collapses = 0

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

        local_signature = (
            sum(
                other.region_signature
                for other in nearby
            ) / len(nearby)
        )

        local_persistence = (
            sum(
                other.persistence_field
                for other in nearby
            ) / len(nearby)
        )

        pressure_gap = abs(
            node.local_pressure
            - node.local_stability
        )

        # ==================================================
        # fragmented persistence
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
        # bridge decay
        # ==================================================

        remove_bridges = []

        for target_id in list(
            node.bridge_links.keys()
        ):

            bridge_strength = (
                node.bridge_links[target_id]
            )

            bridge_strength *= (
                BRIDGE_DECAY_RATE
            )

            bridge_strength -= (
                random.uniform(
                    0.002,
                    0.010
                )
            )

            target = nodes[target_id]

            structure_gap = abs(
                node.structure_type
                - target.structure_type
            )

            friction = (
                structure_gap * 0.036
            )

            bridge_strength -= friction

            node.bridge_friction += (
                friction * 0.28
            )

            translation_noise = (
                abs(
                    node.region_signature
                    - target.region_signature
                )
                * 0.060
            )

            translation_noise += (
                structure_gap * 0.018
            )

            node.translation_loss += (
                translation_noise
            )

            if (
                random.random()
                < BRIDGE_COLLAPSE_RATE
            ):

                bridge_strength -= (
                    random.uniform(
                        0.06,
                        0.18
                    )
                )

            node.bridge_links[
                target_id
            ] = bridge_strength

            if bridge_strength <= 0.02:

                remove_bridges.append(
                    target_id
                )

        for target_id in remove_bridges:

            target = nodes[target_id]

            if (
                target.structure_type
                != node.structure_type
            ):

                node.cross_structure_collapses += 1

            del node.bridge_links[target_id]

            node.bridge_collapses += 1

        # ==================================================
        # heterogeneous bridge formation
        # ==================================================

        formation_bias = (
            BRIDGE_FORMATION_RATE
            +
            (
                node.fragmentation_level
                * 0.010
            )
        )

        if (
            len(node.bridge_links)
            >= 2
        ):

            formation_bias *= 0.55

        if (
            node.compatibility_resonance
            > 0.30
        ):

            formation_bias *= 0.50

        if (
            random.random()
            < formation_bias
            and len(node.bridge_links)
            < MAX_BRIDGES
        ):

            distant_candidates = []

            for other in nodes:

                if other.idx == node.idx:
                    continue

                if (
                    other.idx
                    in node.connections
                ):
                    continue

                if (
                    other.idx
                    in node.bridge_links
                ):
                    continue

                d = distance(node, other)

                structure_gap = abs(
                    node.structure_type
                    - other.structure_type
                )

                signature_gap = abs(
                    other.region_signature
                    - node.region_signature
                )

                persistence_gap = abs(
                    other.persistence_field
                    - node.persistence_field
                )

                if (
                    d > LOCAL_RADIUS * 1.55
                    and structure_gap >= 1
                    and structure_gap <= 2
                    and signature_gap < 0.42
                    and persistence_gap < 0.24
                ):

                    distant_candidates.append(
                        other
                    )

            if distant_candidates:

                target = random.choice(
                    distant_candidates
                )

                bridge_strength = random.uniform(
                    0.10,
                    0.22
                )

                node.bridge_links[
                    target.idx
                ] = bridge_strength

                node.bridge_events += 1

        # ==================================================
        # heterogeneous synchronization
        # ==================================================

        if node.bridge_links:

            bridge_values = []

            incompatibility = []

            for target_id in node.bridge_links:

                target = nodes[target_id]

                bridge_values.append(
                    target.persistence_field
                )

                incompatibility.append(
                    abs(
                        target.structure_type
                        - node.structure_type
                    )
                )

            bridge_mean = (
                sum(bridge_values)
                / len(bridge_values)
            )

            incompatibility_mean = (
                sum(incompatibility)
                / len(incompatibility)
            )

            bridge_gap = abs(
                bridge_mean
                - node.persistence_field
            )

            # stabilized compatibility
            node.compatibility_resonance *= (
                0.992
            )

            node.compatibility_resonance += (
                (
                    1.0
                    - bridge_gap
                ) * 0.020
            )

            # weak incompatibility suppression
            node.compatibility_resonance -= (
                incompatibility_mean
                * 0.0015
            )

            # weak reinforcement persistence
            node.compatibility_resonance += (
                len(node.bridge_links)
                * 0.002
            )

            propagation_strength = (
                0.0055
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
                    bridge_mean
                    - node.persistence_field
                )
                * propagation_strength
            )

            if (
                bridge_gap
                < 0.06
            ):

                node.persistence_field += (
                    random.uniform(
                        -0.028,
                        0.028
                    )
                )

                node.compatibility_resonance *= (
                    0.996
                )

            node.compatibility_resonance = clamp(
                node.compatibility_resonance,
                0.0,
                MAX_COMPATIBILITY_ALIGNMENT
            )

        else:

            node.compatibility_resonance *= (
                0.988
            )

        # ==================================================
        # friction decay
        # ==================================================

        node.translation_loss *= 0.996

        node.bridge_friction *= 0.993

        # ==================================================
        # fragmentation fluctuation
        # ==================================================

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

        # ==================================================
        # structural influence
        # ==================================================

        divergence_force = (
            node.local_pressure
            - node.local_stability
        )

        node.region_signature += (
            divergence_force * 0.015
        )

        node.region_signature += (
            (
                node.persistence_field
                - local_persistence
            ) * 0.010
        )

        node.region_signature += (
            (
                node.fragmentation_level
                - 0.18
            ) * 0.006
        )

        node.region_signature += (
            local_signature
            - node.region_signature
        ) * 0.0007

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
                node.compatibility_resonance
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

        bridge_factor = (
            node.compatibility_resonance
            * 0.012
        )

        rewire_rate = (
            BASE_REWIRE_RATE
            + instability * 0.022
            + bridge_factor
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
# collapse / recovery
# ==================================================

def collapse_and_recovery(nodes):

    for node in nodes:

        instability = abs(
            node.local_pressure
            - node.local_stability
        )

        collapse_threshold = (
            BASE_COLLAPSE_THRESHOLD
            + node.persistence_field
            * 0.014
        )

        if instability > collapse_threshold:

            removable = int(
                len(node.connections)
                * 0.05
            )

            removable = max(
                1,
                removable
            )

            removable = min(
                removable,
                max(
                    1,
                    len(node.connections)
                    - MIN_CONNECTIONS
                )
            )

            if removable > 0:

                removed = random.sample(
                    list(node.connections),
                    removable
                )

                for rid in removed:

                    node.connections.remove(
                        rid
                    )

                node.collapse_events += 1

                node.persistence_score *= (
                    0.997
                )

        if len(node.connections) <= 5:

            nearby = [
                other for other in nodes
                if (
                    other.idx != node.idx
                    and distance(node, other)
                    < LOCAL_RADIUS
                )
            ]

            compatible = []

            for other in nearby:

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
                    and persistence_gap < 0.24
                ):

                    compatible.append(
                        other
                    )

            compatible = sorted(
                compatible,
                key=lambda n:
                    abs(
                        n.persistence_field
                        - node.persistence_field
                    )
            )

            recovered = 0

            for target in compatible[:6]:

                if (
                    len(node.connections)
                    >= MAX_CONNECTIONS
                ):
                    break

                if (
                    target.idx
                    not in node.connections
                ):

                    node.connections.add(
                        target.idx
                    )

                    recovered += 1

            if recovered > 0:

                node.recovery_events += (
                    recovered
                )

                node.persistence_score *= (
                    1.005
                )

        node.persistence_score = clamp(
            node.persistence_score,
            0.72,
            1.60
        )

# ==================================================
# metrics
# ==================================================

def compute_metrics(nodes):

    heterogeneous_bridge_frequency = (
        sum(
            n.bridge_events
            for n in nodes
        )
        / NUM_NODES
    )

    compatibility_instability = (
        sum(
            n.fragmentation_level
            for n in nodes
        )
        / NUM_NODES
    )

    translation_loss_fluctuation = (
        sum(
            n.translation_loss
            for n in nodes
        )
        / NUM_NODES
    )

    cross_structure_collapse_cycles = (
        sum(
            n.cross_structure_collapses
            for n in nodes
        )
        / NUM_NODES
    )

    localized_interoperability_persistence = (
        sum(
            n.compatibility_resonance
            for n in nodes
        )
        / NUM_NODES
    )

    bridge_friction_stability = (
        sum(
            n.bridge_friction
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

        "heterogeneous_bridge_frequency":
            round(
                heterogeneous_bridge_frequency,
                4
            ),

        "compatibility_instability":
            round(
                compatibility_instability,
                4
            ),

        "translation_loss_fluctuation":
            round(
                translation_loss_fluctuation,
                4
            ),

        "cross_structure_collapse_cycles":
            round(
                cross_structure_collapse_cycles,
                4
            ),

        "localized_interoperability_persistence":
            round(
                localized_interoperability_persistence,
                4
            ),

        "bridge_friction_stability":
            round(
                bridge_friction_stability,
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

    compatibility_ok = (
        metrics[
            "localized_interoperability_persistence"
        ]
        < MAX_COMPATIBILITY_ALIGNMENT
    )

    return all([

        metrics[
            "heterogeneous_bridge_frequency"
        ]
        >= MIN_HETEROGENEOUS_BRIDGE_FREQUENCY,

        metrics[
            "compatibility_instability"
        ]
        >= MIN_COMPATIBILITY_INSTABILITY,

        metrics[
            "translation_loss_fluctuation"
        ]
        >= MIN_TRANSLATION_LOSS,

        metrics[
            "cross_structure_collapse_cycles"
        ]
        >= MIN_CROSS_STRUCTURE_COLLAPSE,

        metrics[
            "localized_interoperability_persistence"
        ]
        >= MIN_LOCALIZED_INTEROPERABILITY,

        metrics[
            "bridge_friction_stability"
        ]
        >= MIN_BRIDGE_FRICTION,

        metrics[
            "distributed_structural_persistence"
        ]
        >= MIN_DISTRIBUTED_PERSISTENCE,

        metrics[
            "structural_persistence"
        ]
        >= MIN_STRUCTURAL_PERSISTENCE,

        divergence_ok,

        compatibility_ok
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

        collapse_and_recovery(nodes)

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
