# Agonwelt-Link v19.3.0
# pseudo collective formation
# strict validation mode

import random
import math

# ==================================================
# configuration
# ==================================================

NUM_NODES = 72
NUM_STEPS = 420

LOCAL_RADIUS = 0.24

BASE_REWIRE_RATE = 0.040
BASE_COLLAPSE_THRESHOLD = 0.30

MAX_CONNECTIONS = 8
MIN_CONNECTIONS = 2

DAMPING = 0.95

# shadow ecology
SHADOW_MEMORY_DECAY = 0.986
SHADOW_INFLUENCE_SCALE = 0.016

# collective system
COLLECTIVE_FORMATION_THRESHOLD = 0.22
COLLECTIVE_DECAY = 0.982
MAX_COLLECTIVE_INTENSITY = 0.75

# bounded diversity
MIN_DIVERGENCE = 0.14
MAX_DIVERGENCE = 0.78

# validation thresholds
MIN_FORMATION_FREQUENCY = 0.30
MIN_COLLAPSE_RECOVERY = 0.45
MIN_SYNC_STABILITY = 0.42
MIN_PERSISTENCE = 0.55

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
            0.44,
            0.66
        )

        self.region_signature = random.uniform(
            0.28,
            0.72
        )

        self.shadow_memory = random.uniform(
            0.18,
            0.42
        )

        # temporary collective state
        self.collective_tension = 0.0
        self.collective_alignment = 0.0
        self.collective_decay = 0.0

        self.persistence_score = 1.0

        self.collapse_events = 0
        self.recovery_events = 0

        self.collective_formations = 0
        self.collective_collapses = 0

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
# local ecology
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
            0.94
            * node.instability_memory
            + 0.06
            * instability
        )

        node.local_pressure = (
            0.91
            * node.local_pressure
            + 0.09
            * instability
        )

        node.local_stability = (
            0.89
            * node.local_stability
            + 0.11
            * local_connectivity
        )

        local_signature = (
            sum(
                other.region_signature
                for other in nearby
            ) / len(nearby)
        )

        local_shadow = (
            sum(
                other.shadow_memory
                for other in nearby
            ) / len(nearby)
        )

        # shadow persistence
        node.shadow_memory *= (
            SHADOW_MEMORY_DECAY
        )

        node.shadow_memory += (
            local_shadow
            * SHADOW_INFLUENCE_SCALE
        )

        node.shadow_memory += random.uniform(
            -0.002,
            0.002
        )

        node.shadow_memory = clamp(
            node.shadow_memory,
            0.0,
            1.0
        )

        divergence_force = (
            node.local_pressure
            - node.local_stability
        )

        node.region_signature += (
            divergence_force * 0.016
        )

        node.region_signature += (
            (
                node.shadow_memory
                - local_shadow
            ) * 0.014
        )

        # weak local continuity
        node.region_signature += (
            local_signature
            - node.region_signature
        ) * 0.003

        # bounded divergence preservation
        if global_divergence < 0.22:

            node.region_signature += (
                random.uniform(
                    -0.045,
                    0.045
                )
            )

        elif global_divergence < 0.30:

            node.region_signature += (
                random.uniform(
                    -0.018,
                    0.018
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
            0.03,
            0.97
        )

# ==================================================
# pseudo collectives
# ==================================================

def update_collectives(nodes):

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

        local_instability = abs(
            node.local_pressure
            - node.local_stability
        )

        local_alignment = (
            sum(
                abs(
                    other.region_signature
                    - node.region_signature
                )
                for other in nearby
            ) / len(nearby)
        )

        # temporary collective trigger
        formation_pressure = (
            local_instability
            + node.shadow_memory
        ) * 0.5

        if (
            formation_pressure
            > COLLECTIVE_FORMATION_THRESHOLD
        ):

            node.collective_tension += (
                formation_pressure * 0.04
            )

            node.collective_formations += 1

        # partial synchronization only
        node.collective_alignment *= (
            COLLECTIVE_DECAY
        )

        node.collective_alignment += (
            (
                1.0 - local_alignment
            ) * 0.018
        )

        node.collective_alignment += (
            random.uniform(
                -0.003,
                0.003
            )
        )

        node.collective_alignment = clamp(
            node.collective_alignment,
            0.0,
            MAX_COLLECTIVE_INTENSITY
        )

        # collapse-prone collective
        if (
            node.collective_alignment
            > 0.52
        ):

            node.collective_decay += (
                random.uniform(
                    0.008,
                    0.020
                )
            )

        else:

            node.collective_decay *= 0.96

        # collective collapse
        if (
            node.collective_decay
            > 0.24
        ):

            node.collective_alignment *= (
                random.uniform(
                    0.35,
                    0.65
                )
            )

            node.collective_decay *= 0.45

            node.collective_collapses += 1

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

            # loose temporary cohesion
            cohesion_strength = (
                0.0020
                +
                node.collective_alignment
                * 0.0020
            )

            node.vx += (
                (cx - node.x)
                * cohesion_strength
            )

            node.vy += (
                (cy - node.y)
                * cohesion_strength
            )

            # avoid perfect sync
            node.vx += random.uniform(
                -0.0018,
                0.0018
            )

            node.vy += random.uniform(
                -0.0018,
                0.0018
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

        collective_factor = (
            node.collective_alignment
            * 0.018
        )

        rewire_rate = (
            BASE_REWIRE_RATE
            + instability * 0.022
            + collective_factor
        )

        # remove unstable links
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

                if signature_gap > 0.42:

                    removable.append(cid)

            if removable:

                remove_id = random.choice(
                    removable
                )

                node.connections.remove(
                    remove_id
                )

        # adaptive regrouping
        if (
            random.random() < (
                rewire_rate * 1.35
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

                collective_gap = abs(
                    other.collective_alignment
                    - node.collective_alignment
                )

                if (
                    signature_gap < 0.44
                    and collective_gap < 0.30
                ):

                    compatible.append(
                        (
                            collective_gap,
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
            + node.collective_alignment
            * 0.020
        )

        # collective-prone collapse
        if instability > collapse_threshold:

            removable = int(
                len(node.connections)
                * 0.06
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

        # distributed repair assistance
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

                collective_gap = abs(
                    other.collective_alignment
                    - node.collective_alignment
                )

                if (
                    signature_gap < 0.46
                    and collective_gap < 0.34
                ):

                    compatible.append(
                        other
                    )

            compatible = sorted(
                compatible,
                key=lambda n:
                    abs(
                        n.collective_alignment
                        - node.collective_alignment
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
                    1.008
                )

        node.persistence_score = clamp(
            node.persistence_score,
            0.72,
            1.55
        )

# ==================================================
# metrics
# ==================================================

def compute_metrics(nodes):

    total_formations = sum(
        n.collective_formations
        for n in nodes
    )

    total_collapses = sum(
        n.collective_collapses
        for n in nodes
    )

    collective_formation_frequency = (
        total_formations
        / (NUM_NODES * NUM_STEPS)
    )

    collective_collapse_recovery = (
        total_collapses
        /
        max(1, total_formations)
    )

    partial_sync_stability = (
        sum(
            n.collective_alignment
            for n in nodes
        ) / NUM_NODES
    )

    distributed_regrouping = (
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

    collective_persistence_balance = (
        sum(
            n.collective_decay
            for n in nodes
        ) / NUM_NODES
    )

    local_cohesion_continuity = (
        sum(
            n.persistence_score
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

    divergence = (
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

        "collective_formation_frequency":
            round(
                collective_formation_frequency,
                4
            ),

        "collective_collapse_recovery":
            round(
                collective_collapse_recovery,
                4
            ),

        "partial_sync_stability":
            round(
                partial_sync_stability,
                4
            ),

        "distributed_regrouping":
            round(
                distributed_regrouping,
                4
            ),

        "collective_persistence_balance":
            round(
                collective_persistence_balance,
                4
            ),

        "local_cohesion_continuity":
            round(
                local_cohesion_continuity,
                4
            ),

        "structural_persistence":
            round(
                structural_persistence,
                4
            ),

        "bounded_divergence":
            round(
                divergence,
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

    return all([

        metrics[
            "collective_formation_frequency"
        ]
        >= MIN_FORMATION_FREQUENCY,

        metrics[
            "collective_collapse_recovery"
        ]
        >= 0.02,

        metrics[
            "partial_sync_stability"
        ]
        >= MIN_SYNC_STABILITY,

        metrics[
            "distributed_regrouping"
        ]
        >= MIN_COLLAPSE_RECOVERY,

        metrics[
            "local_cohesion_continuity"
        ]
        >= MIN_PERSISTENCE,

        metrics[
            "structural_persistence"
        ]
        >= MIN_PERSISTENCE,

        divergence_ok
    ])

# ==================================================
# run
# ==================================================

def run(seed):

    random.seed(seed)

    nodes = initialize_network()

    for _ in range(NUM_STEPS):

        update_ecology(nodes)

        update_collectives(nodes)

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
