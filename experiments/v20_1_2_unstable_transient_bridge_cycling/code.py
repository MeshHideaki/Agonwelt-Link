# Agonwelt-Link v20.1.2
# unstable transient bridge cycling
# strict validation mode

import random
import math

# ==================================================
# configuration
# ==================================================

NUM_NODES = 72
NUM_STEPS = 620

LOCAL_RADIUS = 0.24

BASE_REWIRE_RATE = 0.042
BASE_COLLAPSE_THRESHOLD = 0.29

MAX_CONNECTIONS = 8
MIN_CONNECTIONS = 2

# reduced transient bridges
MAX_BRIDGES = 3

DAMPING = 0.95

# bridge ecology
BRIDGE_FORMATION_RATE = 0.036

# faster decay
BRIDGE_DECAY_RATE = 0.989

# stronger collapse
BRIDGE_COLLAPSE_RATE = 0.034

# fragmented persistence
PERSISTENCE_DECAY = 0.992
LOCAL_RECOVERY_SCALE = 0.016

# instability ecology
INSTABILITY_NOISE = 0.005

# bounded bridge persistence
MAX_BRIDGE_ALIGNMENT = 0.36

# bounded diversity
MIN_DIVERGENCE = 0.14
MAX_DIVERGENCE = 0.78

# validation thresholds
MIN_BRIDGE_FREQUENCY = 0.08
MIN_BRIDGE_COLLAPSE_STABILITY = 0.40
MIN_PARTIAL_SYNC = 0.12
MIN_LOCAL_CONTINUITY = 0.55
MIN_BRIDGE_FLUCTUATION = 0.08
MIN_RECONNECTION_CYCLES = 0.18
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

        self.persistence_field = random.uniform(
            0.10,
            0.24
        )

        self.bridge_resonance = 0.0

        self.fragmentation_level = random.uniform(
            0.02,
            0.08
        )

        self.persistence_score = 1.0

        self.collapse_events = 0
        self.recovery_events = 0

        self.bridge_events = 0
        self.bridge_collapses = 0

        self.reconnections = 0

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

        # ==================================================
        # fragmented persistence
        # ==================================================

        pressure_gap = abs(
            node.local_pressure
            - node.local_stability
        )

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

            node.bridge_links[target_id] *= (
                BRIDGE_DECAY_RATE
            )

            node.bridge_links[target_id] -= (
                random.uniform(
                    0.002,
                    0.010
                )
            )

            if (
                random.random()
                < BRIDGE_COLLAPSE_RATE
            ):

                node.bridge_links[target_id] -= (
                    random.uniform(
                        0.06,
                        0.18
                    )
                )

            if (
                node.bridge_links[target_id]
                <= 0.02
            ):

                remove_bridges.append(
                    target_id
                )

        for target_id in remove_bridges:

            del node.bridge_links[target_id]

            node.bridge_collapses += 1

            # reconnection impulse
            node.reconnections += (
                random.uniform(
                    0.030,
                    0.070
                )
            )

        # ==================================================
        # bridge formation
        # ==================================================

        formation_bias = (
            BRIDGE_FORMATION_RATE
            +
            (
                node.fragmentation_level
                * 0.010
            )
        )

        # anti-overconnection suppression
        if (
            len(node.bridge_links)
            >= 2
        ):

            formation_bias *= 0.55

        if (
            node.bridge_resonance
            > 0.28
        ):

            formation_bias *= 0.45

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
                    and signature_gap < 0.30
                    and persistence_gap < 0.18
                ):

                    distant_candidates.append(
                        other
                    )

            if distant_candidates:

                target = random.choice(
                    distant_candidates
                )

                bridge_strength = random.uniform(
                    0.12,
                    0.26
                )

                node.bridge_links[
                    target.idx
                ] = bridge_strength

                node.bridge_events += 1

        # ==================================================
        # partial bridge synchronization
        # ==================================================

        if node.bridge_links:

            bridge_values = []

            for target_id in node.bridge_links:

                target = nodes[target_id]

                bridge_values.append(
                    target.persistence_field
                )

            bridge_mean = (
                sum(bridge_values)
                / len(bridge_values)
            )

            bridge_gap = abs(
                bridge_mean
                - node.persistence_field
            )

            # stronger decay
            node.bridge_resonance *= 0.981

            node.bridge_resonance += (
                (
                    1.0
                    - bridge_gap
                ) * 0.0075
            )

            # anti-stable bridge
            if (
                bridge_gap
                < 0.05
            ):

                node.persistence_field += (
                    random.uniform(
                        -0.020,
                        0.020
                    )
                )

                node.bridge_resonance *= 0.992

            # weaker propagation
            node.persistence_field += (
                (
                    bridge_mean
                    - node.persistence_field
                ) * 0.004
            )

            if (
                node.bridge_resonance
                > 0.30
            ):

                node.bridge_resonance *= 0.990

            node.bridge_resonance = clamp(
                node.bridge_resonance,
                0.0,
                MAX_BRIDGE_ALIGNMENT
            )

        else:

            node.bridge_resonance *= 0.975

            # isolated reconnection pressure
            if pressure_gap > 0.10:

                node.reconnections += (
                    random.uniform(
                        0.002,
                        0.010
                    )
                )

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
        ) * 0.0008

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
                node.bridge_resonance
                * 0.0006
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
            node.bridge_resonance
            * 0.014
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

    bridge_formation_frequency = (
        sum(
            n.bridge_events
            for n in nodes
        )
        / NUM_NODES
    )

    bridge_collapse_stability = (
        sum(
            n.bridge_collapses
            for n in nodes
        )
        /
        max(
            1,
            sum(
                n.bridge_events
                for n in nodes
            )
        )
    )

    partial_synchronization_persistence = (
        sum(
            n.bridge_resonance
            for n in nodes
        ) / NUM_NODES
    )

    localized_continuity_support = (
        sum(
            n.persistence_score
            for n in nodes
        ) / NUM_NODES
    )

    bridge_decay_fluctuation = (
        sum(
            n.fragmentation_level
            for n in nodes
        ) / NUM_NODES
    )

    fragmented_reconnection_cycles = (
        sum(
            n.reconnections
            for n in nodes
        ) / NUM_NODES
    )

    distributed_persistence = (
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

        "bridge_formation_frequency":
            round(
                bridge_formation_frequency,
                4
            ),

        "bridge_collapse_stability":
            round(
                bridge_collapse_stability,
                4
            ),

        "partial_synchronization_persistence":
            round(
                partial_synchronization_persistence,
                4
            ),

        "localized_continuity_support":
            round(
                localized_continuity_support,
                4
            ),

        "bridge_decay_fluctuation":
            round(
                bridge_decay_fluctuation,
                4
            ),

        "fragmented_reconnection_cycles":
            round(
                fragmented_reconnection_cycles,
                4
            ),

        "distributed_persistence":
            round(
                distributed_persistence,
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

    bridge_ok = (
        metrics[
            "partial_synchronization_persistence"
        ]
        < MAX_BRIDGE_ALIGNMENT
    )

    return all([

        metrics[
            "bridge_formation_frequency"
        ]
        >= MIN_BRIDGE_FREQUENCY,

        metrics[
            "bridge_collapse_stability"
        ]
        >= MIN_BRIDGE_COLLAPSE_STABILITY,

        metrics[
            "partial_synchronization_persistence"
        ]
        >= MIN_PARTIAL_SYNC,

        metrics[
            "localized_continuity_support"
        ]
        >= MIN_LOCAL_CONTINUITY,

        metrics[
            "bridge_decay_fluctuation"
        ]
        >= MIN_BRIDGE_FLUCTUATION,

        metrics[
            "fragmented_reconnection_cycles"
        ]
        >= MIN_RECONNECTION_CYCLES,

        metrics[
            "distributed_persistence"
        ]
        >= MIN_DISTRIBUTED_PERSISTENCE,

        metrics[
            "structural_persistence"
        ]
        >= MIN_STRUCTURAL_PERSISTENCE,

        divergence_ok,

        bridge_ok
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
