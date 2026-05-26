# Agonwelt-Link v19.1.2
# resilient local ecological differentiation
# strict validation mode

import random
import math

# ==================================================
# configuration
# ==================================================

NUM_NODES = 72
NUM_STEPS = 240

LOCAL_RADIUS = 0.22

BASE_REWIRE_RATE = 0.035
BASE_COLLAPSE_THRESHOLD = 0.31

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

        self.vx = random.uniform(-0.006, 0.006)
        self.vy = random.uniform(-0.006, 0.006)

        self.connections = set()

        self.local_pressure = random.uniform(0.38, 0.62)
        self.local_stability = random.uniform(0.42, 0.68)

        # narrower initialization
        self.region_signature = random.uniform(0.35, 0.65)

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
        (a.x - b.x) ** 2 +
        (a.y - b.y) ** 2
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

        # stronger initial continuity
        for other in nearby[1:6]:

            node.connections.add(other.idx)

    return nodes

# ==================================================
# local ecology
# ==================================================

def update_local_ecology(nodes):

    for node in nodes:

        nearby = [
            other for other in nodes
            if other.idx != node.idx
            and distance(node, other) < LOCAL_RADIUS
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
                len(nearby) * MAX_CONNECTIONS
            )
        )

        instability = abs(
            local_density
            - local_connectivity
        )

        node.instability_memory = (
            0.88 * node.instability_memory
            + 0.12 * instability
        )

        # local ecological pressure
        node.local_pressure = (
            0.86 * node.local_pressure
            + 0.14 * instability
        )

        node.local_stability = (
            0.84 * node.local_stability
            + 0.16 * local_connectivity
        )

        # bounded divergence
        local_alignment = (
            sum(
                other.region_signature
                for other in nearby
            ) / len(nearby)
        )

        divergence_shift = (
            node.local_pressure
            - node.local_stability
        ) * 0.006

        # continuity-preserving convergence
        node.region_signature += (
            local_alignment
            - node.region_signature
        ) * 0.022

        # local ecological drift
        node.region_signature += divergence_shift

        # very small stochastic divergence
        node.region_signature += random.uniform(
            -0.004,
            0.004
        )

        node.region_signature = clamp(
            node.region_signature,
            0.18,
            0.82
        )

# ==================================================
# movement
# ==================================================

def update_positions(nodes):

    for node in nodes:

        nearby = [
            other for other in nodes
            if other.idx != node.idx
            and distance(node, other) < LOCAL_RADIUS
        ]

        if nearby:

            cx = (
                sum(n.x for n in nearby)
                / len(nearby)
            )

            cy = (
                sum(n.y for n in nearby)
                / len(nearby)
            )

            cohesion_strength = 0.0032

            node.vx += (
                (cx - node.x)
                * cohesion_strength
            )

            node.vy += (
                (cy - node.y)
                * cohesion_strength
            )

            divergence_bias = (
                node.region_signature - 0.5
            )

            node.vx += divergence_bias * 0.0010
            node.vy += -divergence_bias * 0.0010

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
            if other.idx != node.idx
            and distance(node, other) < LOCAL_RADIUS
        ]

        if not nearby:
            continue

        instability = abs(
            node.local_pressure
            - node.local_stability
        )

        rewire_rate = (
            BASE_REWIRE_RATE
            + instability * 0.025
        )

        # remove ecologically incompatible links
        if (
            random.random() < rewire_rate
            and len(node.connections) > MIN_CONNECTIONS
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

                remove_id = random.choice(removable)

                node.connections.remove(remove_id)

        # bounded rewiring
        if (
            random.random() < rewire_rate
            and len(node.connections) < MAX_CONNECTIONS
        ):

            compatible = []

            for other in nearby:

                if other.idx in node.connections:
                    continue

                diff = abs(
                    other.region_signature
                    - node.region_signature
                )

                if diff < 0.22:

                    compatibility = abs(
                        other.local_stability
                        - node.local_stability
                    )

                    compatible.append(
                        (compatibility, other)
                    )

            compatible.sort(
                key=lambda x: x[0]
            )

            if compatible:

                target = compatible[0][1]

                node.connections.add(target.idx)

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
            + node.region_signature * 0.04
        )

        # local bounded collapse
        if instability > collapse_threshold:

            removable = int(
                len(node.connections) * 0.15
            )

            removable = max(1, removable)

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
                    node.connections.remove(rid)

                node.collapse_events += 1

                # softer persistence decay
                node.persistence_score *= 0.988

        # distributed ecological recovery
        if len(node.connections) <= 4:

            nearby = [
                other for other in nodes
                if other.idx != node.idx
                and distance(node, other) < LOCAL_RADIUS
            ]

            compatible = []

            for other in nearby:

                diff = abs(
                    other.region_signature
                    - node.region_signature
                )

                stability_diff = abs(
                    other.local_stability
                    - node.local_stability
                )

                if (
                    diff < 0.26
                    and stability_diff < 0.22
                ):

                    compatible.append(other)

            compatible = sorted(
                compatible,
                key=lambda n:
                    abs(
                        n.region_signature
                        - node.region_signature
                    )
            )

            recovered = 0

            for target in compatible[:3]:

                if (
                    len(node.connections)
                    >= MAX_CONNECTIONS
                ):
                    break

                if target.idx not in node.connections:

                    node.connections.add(target.idx)

                    recovered += 1

            if recovered > 0:

                node.recovery_events += 1

                node.persistence_score *= (
                    1.003 + recovered * 0.002
                )

        node.persistence_score = clamp(
            node.persistence_score,
            0.55,
            1.35
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
        (NUM_NODES * MAX_CONNECTIONS)
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
            round(local_adaptation_persistence, 4),

        "regional_continuity":
            round(regional_continuity, 4),

        "distributed_recovery":
            round(distributed_recovery, 4),

        "ecological_divergence":
            round(ecological_divergence, 4),

        "structural_persistence":
            round(structural_persistence, 4),

        "cross_region_instability":
            round(cross_region_instability, 4),
    }

# ==================================================
# validation
# ==================================================

def validate(metrics):

    divergence_ok = (
        MIN_REGION_DIVERSITY
        <= metrics["ecological_divergence"]
        <= MAX_REGION_DIVERSITY
    )

    return all([

        metrics["local_adaptation_persistence"]
        >= MIN_LOCAL_PERSISTENCE,

        metrics["regional_continuity"]
        >= MIN_REGIONAL_CONTINUITY,

        metrics["distributed_recovery"]
        >= MIN_DISTRIBUTED_RECOVERY,

        metrics["structural_persistence"]
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

    validation_result = validate(metrics)

    return metrics, validation_result

# ==================================================
# strict validation
# ==================================================

overall = True

for seed in [42, 43, 44]:

    print(f"\n--- RUN #{seed} ---")

    metrics, validation_result = run(seed)

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
