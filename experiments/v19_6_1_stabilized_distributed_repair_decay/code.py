# Agonwelt-Link v19.6.1
# stabilized distributed repair decay
# strict validation mode

import random
import math

# ==================================================
# configuration
# ==================================================

NUM_NODES = 72
NUM_STEPS = 560

LOCAL_RADIUS = 0.25

BASE_REWIRE_RATE = 0.042
BASE_COLLAPSE_THRESHOLD = 0.29

MAX_CONNECTIONS = 8
MIN_CONNECTIONS = 2

DAMPING = 0.95

# distributed persistence
PERSISTENCE_DECAY = 0.992
PERSISTENCE_PROPAGATION = 0.010
LOCAL_RECOVERY_SCALE = 0.016

# fragmented ecology
INSTABILITY_NOISE = 0.005
LOCAL_COLLAPSE_SCALE = 0.012

# stabilized repair decay
REPAIR_DECAY = 0.991

# bounded unstable homeostasis
MAX_HOMEOSTASIS_ALIGNMENT = 0.40

# bounded diversity
MIN_DIVERGENCE = 0.14
MAX_DIVERGENCE = 0.78

# validation thresholds
MIN_PERSISTENCE_STABILITY = 0.16
MIN_RECOVERY_BALANCE = 0.40
MIN_FRAGMENTED_CONTINUITY = 0.55
MIN_INSTABILITY_FLUCTUATION = 0.08
MIN_ECOLOGICAL_PERSISTENCE = 0.12
MIN_REPAIR_DECAY = 0.10
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

        # higher initial repair decay floor
        self.persistence_decay = random.uniform(
            0.05,
            0.10
        )

        self.local_homeostasis = 0.0

        self.persistence_score = 1.0

        self.fragmentation_level = random.uniform(
            0.02,
            0.08
        )

        self.collapse_events = 0
        self.recovery_events = 0

        self.repair_decay_events = 0

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

            node.connections.add(other.idx)

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
        # distributed unstable homeostasis
        # ==================================================

        previous_persistence = (
            node.persistence_field
        )

        node.persistence_field *= (
            PERSISTENCE_DECAY
        )

        persistence_delta = (
            (
                local_persistence
                - node.persistence_field
            )
            * PERSISTENCE_PROPAGATION
        )

        node.persistence_field += (
            persistence_delta
        )

        pressure_gap = abs(
            node.local_pressure
            - node.local_stability
        )

        node.persistence_field += (
            pressure_gap
            * LOCAL_COLLAPSE_SCALE
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

        local_alignment_gap = abs(
            local_persistence
            - node.persistence_field
        )

        if (
            local_alignment_gap
            < 0.05
        ):

            node.persistence_field += (
                random.uniform(
                    -0.018,
                    0.018
                )
            )

        node.persistence_field = clamp(
            node.persistence_field,
            0.02,
            0.82
        )

        # ==================================================
        # bounded local homeostasis
        # ==================================================

        node.local_homeostasis *= 0.986

        node.local_homeostasis += (
            (
                1.0
                - local_alignment_gap
            ) * 0.008
        )

        if (
            node.local_homeostasis
            > 0.37
        ):

            node.local_homeostasis *= 0.994

        node.local_homeostasis = clamp(
            node.local_homeostasis,
            0.0,
            MAX_HOMEOSTASIS_ALIGNMENT
        )

        # ==================================================
        # stabilized fragmented decay
        # ==================================================

        node.persistence_decay *= (
            REPAIR_DECAY
        )

        node.persistence_decay += (
            random.uniform(
                -0.002,
                0.004
            )
        )

        # stronger instability reinforcement
        node.persistence_decay += (
            pressure_gap * 0.007
        )

        # fragmented ecology reinforcement
        node.persistence_decay += (
            node.fragmentation_level
            * 0.003
        )

        node.persistence_decay = clamp(
            node.persistence_decay,
            0.02,
            0.42
        )

        if abs(
            node.persistence_field
            - previous_persistence
        ) > 0.0002:

            node.repair_decay_events += 1

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
        ) * 0.0009

        # ==================================================
        # bounded divergence preservation
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
                0.0014
                +
                node.local_homeostasis
                * 0.0008
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
                -0.0025,
                0.0025
            )

            node.vy += random.uniform(
                -0.0025,
                0.0025
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

        persistence_factor = (
            node.local_homeostasis
            * 0.018
        )

        rewire_rate = (
            BASE_REWIRE_RATE
            + instability * 0.022
            + persistence_factor
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
                rewire_rate * 1.26
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
                    signature_gap < 0.52
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

    distributed_persistence_stability = (
        sum(
            n.local_homeostasis
            for n in nodes
        ) / NUM_NODES
    )

    local_collapse_recovery_balance = (
        sum(
            n.recovery_events
            for n in nodes
        )
        /
        max(
            1,
            sum(
                n.collapse_events
                for n in nodes
            )
        )
    )

    fragmented_continuity_persistence = (
        sum(
            n.persistence_score
            for n in nodes
        ) / NUM_NODES
    )

    adaptive_instability_fluctuation = (
        sum(
            n.fragmentation_level
            for n in nodes
        ) / NUM_NODES
    )

    bounded_ecological_persistence = (
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

    distributed_repair_decay = (
        sum(
            n.persistence_decay
            for n in nodes
        ) / NUM_NODES
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

        "distributed_persistence_stability":
            round(
                distributed_persistence_stability,
                4
            ),

        "local_collapse_recovery_balance":
            round(
                local_collapse_recovery_balance,
                4
            ),

        "fragmented_continuity_persistence":
            round(
                fragmented_continuity_persistence,
                4
            ),

        "adaptive_instability_fluctuation":
            round(
                adaptive_instability_fluctuation,
                4
            ),

        "bounded_ecological_persistence":
            round(
                bounded_ecological_persistence,
                4
            ),

        "distributed_repair_decay":
            round(
                distributed_repair_decay,
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

    homeostasis_ok = (
        metrics[
            "distributed_persistence_stability"
        ]
        < MAX_HOMEOSTASIS_ALIGNMENT
    )

    return all([

        metrics[
            "distributed_persistence_stability"
        ]
        >= MIN_PERSISTENCE_STABILITY,

        metrics[
            "local_collapse_recovery_balance"
        ]
        >= MIN_RECOVERY_BALANCE,

        metrics[
            "fragmented_continuity_persistence"
        ]
        >= MIN_FRAGMENTED_CONTINUITY,

        metrics[
            "adaptive_instability_fluctuation"
        ]
        >= MIN_INSTABILITY_FLUCTUATION,

        metrics[
            "bounded_ecological_persistence"
        ]
        >= MIN_ECOLOGICAL_PERSISTENCE,

        metrics[
            "distributed_repair_decay"
        ]
        >= MIN_REPAIR_DECAY,

        metrics[
            "structural_persistence"
        ]
        >= MIN_STRUCTURAL_PERSISTENCE,

        divergence_ok,

        homeostasis_ok
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
