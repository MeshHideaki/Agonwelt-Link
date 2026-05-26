# Agonwelt-Link v19.1.5
# adaptive distributed ecological persistence
# strict validation mode

import random
import math

# ==================================================
# configuration
# ==================================================

NUM_NODES = 72
NUM_STEPS = 320

LOCAL_RADIUS = 0.24

BASE_REWIRE_RATE = 0.040
BASE_COLLAPSE_THRESHOLD = 0.29

MAX_CONNECTIONS = 8
MIN_CONNECTIONS = 2

DAMPING = 0.95

# bounded diversity
MIN_REGION_DIVERSITY = 0.14
MAX_REGION_DIVERSITY = 0.78

# validation thresholds
MIN_LOCAL_PERSISTENCE = 0.58
MIN_REGIONAL_CONTINUITY = 0.52
MIN_DISTRIBUTED_RECOVERY = 0.45
MIN_STRUCTURAL_PERSISTENCE = 0.55

# ==================================================
# node
# ==================================================

class Node:

    def __init__(self, idx):

        self.idx = idx

        self.x = random.random()
        self.y = random.random()

        self.vx = random.uniform(-0.005, 0.005)
        self.vy = random.uniform(-0.005, 0.005)

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
            0.32,
            0.68
        )

        self.persistence_score = 1.0

        self.collapse_events = 0
        self.recovery_events = 0

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

def update_local_ecology(nodes):

    global_mean = (
        sum(
            n.region_signature
            for n in nodes
        ) / NUM_NODES
    )

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
            0.92
            * node.instability_memory
            + 0.08
            * instability
        )

        node.local_pressure = (
            0.89
            * node.local_pressure
            + 0.11
            * instability
        )

        node.local_stability = (
            0.87
            * node.local_stability
            + 0.13
            * local_connectivity
        )

        local_alignment = (
            sum(
                other.region_signature
                for other in nearby
            ) / len(nearby)
        )

        divergence_force = (
            node.local_pressure
            - node.local_stability
        )

        # ecological differentiation
        node.region_signature += (
            divergence_force * 0.014
        )

        # weaker convergence
        node.region_signature += (
            local_alignment
            - node.region_signature
        ) * 0.007

        global_offset = abs(
            node.region_signature
            - global_mean
        )

        # adaptive diversity restoration
        if global_divergence < 0.18:

            if global_offset < 0.10:

                node.region_signature += (
                    random.uniform(
                        -0.030,
                        0.030
                    )
                )

            else:

                node.region_signature += (
                    random.uniform(
                        -0.016,
                        0.016
                    )
                )

        else:

            if global_offset < 0.06:

                node.region_signature += (
                    random.uniform(
                        -0.012,
                        0.012
                    )
                )

            else:

                node.region_signature += (
                    random.uniform(
                        -0.005,
                        0.005
                    )
                )

        node.region_signature = clamp(
            node.region_signature,
            0.08,
            0.92
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

            node.vx += (
                (cx - node.x)
                * 0.0028
            )

            node.vy += (
                (cy - node.y)
                * 0.0028
            )

            divergence_bias = (
                node.region_signature
                - 0.5
            )

            node.vx += (
                divergence_bias * 0.0015
            )

            node.vy += (
                -divergence_bias * 0.0015
            )

        node.vx *= DAMPING
        node.vy *= DAMPING

        node.x += node.vx
        node.y += node.vy

        node.x = clamp(node.x, 0.0, 1.0)
        node.y = clamp(node.y, 0.0, 1.0)

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
            + instability * 0.024
        )

        # remove incompatible links
        if (
            random.random() < rewire_rate
            and len(node.connections)
            > MIN_CONNECTIONS
        ):

            removable = []

            for cid in node.connections:

                target = nodes[cid]

                diff = abs(
                    target.region_signature
                    - node.region_signature
                )

                if diff > 0.34:

                    removable.append(cid)

            if removable:

                remove_id = random.choice(
                    removable
                )

                node.connections.remove(
                    remove_id
                )

        # stronger distributed rewiring
        if (
            random.random() < (
                rewire_rate * 1.25
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

                diff = abs(
                    other.region_signature
                    - node.region_signature
                )

                stability_gap = abs(
                    other.local_stability
                    - node.local_stability
                )

                if (
                    diff < 0.34
                    and stability_gap < 0.32
                ):

                    compatible.append(
                        (
                            stability_gap,
                            other
                        )
                    )

            compatible.sort(
                key=lambda x: x[0]
            )

            added = 0

            for _, target in compatible[:3]:

                if (
                    len(node.connections)
                    >= MAX_CONNECTIONS
                ):
                    break

                node.connections.add(
                    target.idx
                )

                added += 1

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
            + node.region_signature
            * 0.025
        )

        # softer collapse
        if instability > collapse_threshold:

            removable = int(
                len(node.connections)
                * 0.10
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
                    0.994
                )

        # aggressive distributed recovery
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

                diff = abs(
                    other.region_signature
                    - node.region_signature
                )

                stability_gap = abs(
                    other.local_stability
                    - node.local_stability
                )

                if (
                    diff < 0.36
                    and stability_gap < 0.34
                ):

                    compatible.append(
                        other
                    )

            compatible = sorted(
                compatible,
                key=lambda n:
                    abs(
                        n.region_signature
                        - node.region_signature
                    )
            )

            recovered = 0

            for target in compatible[:5]:

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
                    + recovered * 0.002
                )

        node.persistence_score = clamp(
            node.persistence_score,
            0.66,
            1.45
        )

# ==================================================
# metrics
# ==================================================

def compute_metrics(nodes):

    local_adaptation_persistence = (
        sum(
            n.persistence_score
            for n in nodes
        ) / NUM_NODES
    )

    regional_continuity = (
        sum(
            len(n.connections)
            for n in nodes
        )
        /
        (
            NUM_NODES
            * MAX_CONNECTIONS
        )
    )

    total_recovery = sum(
        n.recovery_events
        for n in nodes
    )

    total_collapse = sum(
        n.collapse_events
        for n in nodes
    )

    distributed_recovery = (
        total_recovery
        /
        max(1, total_collapse)
    )

    signatures = [
        n.region_signature
        for n in nodes
    ]

    ecological_divergence = (
        max(signatures)
        - min(signatures)
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

    cross_region_instability = (
        sum(
            n.instability_memory
            for n in nodes
        ) / NUM_NODES
    )

    return {

        "local_adaptation_persistence":
            round(
                local_adaptation_persistence,
                4
            ),

        "regional_continuity":
            round(
                regional_continuity,
                4
            ),

        "distributed_recovery":
            round(
                distributed_recovery,
                4
            ),

        "ecological_divergence":
            round(
                ecological_divergence,
                4
            ),

        "structural_persistence":
            round(
                structural_persistence,
                4
            ),

        "cross_region_instability":
            round(
                cross_region_instability,
                4
            ),
    }

# ==================================================
# validation
# ==================================================

def validate(metrics):

    divergence_ok = (
        MIN_REGION_DIVERSITY
        <= metrics[
            "ecological_divergence"
        ]
        <= MAX_REGION_DIVERSITY
    )

    return all([

        metrics[
            "local_adaptation_persistence"
        ]
        >= MIN_LOCAL_PERSISTENCE,

        metrics[
            "regional_continuity"
        ]
        >= MIN_REGIONAL_CONTINUITY,

        metrics[
            "distributed_recovery"
        ]
        >= MIN_DISTRIBUTED_RECOVERY,

        metrics[
            "structural_persistence"
        ]
        >= MIN_STRUCTURAL_PERSISTENCE,

        divergence_ok
    ])

# ==================================================
# run
# ==================================================

def run(seed):

    random.seed(seed)

    nodes = initialize_network()

    for _ in range(NUM_STEPS):

        update_local_ecology(nodes)

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
