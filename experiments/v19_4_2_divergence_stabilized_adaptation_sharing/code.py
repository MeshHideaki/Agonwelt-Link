# Agonwelt-Link v19.4.2
# divergence stabilized adaptation sharing
# strict validation mode

import random
import math

# ==================================================
# configuration
# ==================================================

NUM_NODES = 72
NUM_STEPS = 480

LOCAL_RADIUS = 0.25

BASE_REWIRE_RATE = 0.040
BASE_COLLAPSE_THRESHOLD = 0.30

MAX_CONNECTIONS = 8
MIN_CONNECTIONS = 2

DAMPING = 0.95

# shadow ecology
SHADOW_MEMORY_DECAY = 0.989
SHADOW_INFLUENCE_SCALE = 0.014

# adaptation propagation
ADAPTATION_TRACE_DECAY = 0.994
ADAPTATION_PROPAGATION_SCALE = 0.026
LOCAL_REPAIR_INFLUENCE = 0.018

# bounded diversity
MIN_DIVERGENCE = 0.14
MAX_DIVERGENCE = 0.78

# validation thresholds
MIN_PROPAGATION = 0.22
MIN_DECAY_STABILITY = 0.45
MIN_RECOVERY_REINFORCEMENT = 0.45
MIN_CONTINUITY_SUPPORT = 0.55
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
            0.44,
            0.66
        )

        self.region_signature = random.uniform(
            0.22,
            0.78
        )

        self.shadow_memory = random.uniform(
            0.18,
            0.42
        )

        self.adaptation_trace = random.uniform(
            0.16,
            0.28
        )

        self.repair_tendency = random.uniform(
            -0.04,
            0.04
        )

        self.persistence_score = 1.0

        self.collapse_events = 0
        self.recovery_events = 0

        self.propagation_events = 0

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

    global_trace_mean = (
        sum(
            n.adaptation_trace
            for n in nodes
        ) / NUM_NODES
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

        local_trace = (
            sum(
                other.adaptation_trace
                for other in nearby
            ) / len(nearby)
        )

        local_repair = (
            sum(
                other.repair_tendency
                for other in nearby
            ) / len(nearby)
        )

        # ==================================================
        # weak adaptation propagation
        # ==================================================

        previous_trace = (
            node.adaptation_trace
        )

        node.adaptation_trace *= (
            ADAPTATION_TRACE_DECAY
        )

        propagation_delta = (
            (
                local_trace
                - node.adaptation_trace
            )
            * ADAPTATION_PROPAGATION_SCALE
        )

        node.adaptation_trace += (
            propagation_delta
        )

        node.adaptation_trace += (
            local_repair
            * LOCAL_REPAIR_INFLUENCE
        )

        instability_gap = abs(
            node.local_pressure
            - node.local_stability
        )

        node.adaptation_trace += (
            instability_gap * 0.010
        )

        if global_trace_mean < 0.26:

            node.adaptation_trace += (
                random.uniform(
                    -0.008,
                    0.018
                )
            )

        else:

            node.adaptation_trace += (
                random.uniform(
                    -0.004,
                    0.006
                )
            )

        node.adaptation_trace = clamp(
            node.adaptation_trace,
            0.02,
            0.92
        )

        if abs(
            node.adaptation_trace
            - previous_trace
        ) > 0.00012:

            node.propagation_events += 1

        # ==================================================
        # repair tendency
        # ==================================================

        node.repair_tendency *= 0.992

        node.repair_tendency += (
            (
                node.local_stability
                - node.local_pressure
            ) * 0.018
        )

        node.repair_tendency += (
            propagation_delta * 0.25
        )

        node.repair_tendency = clamp(
            node.repair_tendency,
            -0.4,
            0.4
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
                node.adaptation_trace
                - local_trace
            ) * 0.011
        )

        # further weakened convergence
        node.region_signature += (
            local_signature
            - node.region_signature
        ) * 0.0011

        # divergence restoration
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
                    0.040
                )
            )

        elif global_divergence < 0.24:

            if global_offset < 0.10:

                node.region_signature += (
                    random.uniform(
                        -0.045,
                        0.045
                    )
                )

            else:

                node.region_signature += (
                    random.uniform(
                        -0.018,
                        0.018
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
                0.0018
                +
                node.adaptation_trace
                * 0.0014
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

        adaptation_factor = (
            node.adaptation_trace
            * 0.020
        )

        rewire_rate = (
            BASE_REWIRE_RATE
            + instability * 0.020
            + adaptation_factor
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

                adaptation_gap = abs(
                    target.adaptation_trace
                    - node.adaptation_trace
                )

                if (
                    signature_gap > 0.44
                    and adaptation_gap > 0.14
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
                rewire_rate * 1.30
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

                adaptation_gap = abs(
                    other.adaptation_trace
                    - node.adaptation_trace
                )

                if (
                    signature_gap < 0.48
                    and adaptation_gap < 0.18
                ):

                    compatible.append(
                        (
                            adaptation_gap,
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
            + node.adaptation_trace
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
                    0.998
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

                adaptation_gap = abs(
                    other.adaptation_trace
                    - node.adaptation_trace
                )

                if (
                    signature_gap < 0.50
                    and adaptation_gap < 0.20
                ):

                    compatible.append(
                        other
                    )

            compatible = sorted(
                compatible,
                key=lambda n:
                    abs(
                        n.adaptation_trace
                        - node.adaptation_trace
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
                    1.006
                )

        node.persistence_score = clamp(
            node.persistence_score,
            0.74,
            1.60
        )

# ==================================================
# metrics
# ==================================================

def compute_metrics(nodes):

    local_adaptation_propagation = (
        sum(
            n.propagation_events
            for n in nodes
        )
        /
        (NUM_NODES * NUM_STEPS)
    )

    adaptation_decay_stability = (
        sum(
            n.adaptation_trace
            for n in nodes
        ) / NUM_NODES
    )

    distributed_recovery_reinforcement = (
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

    bounded_adaptation_persistence = (
        sum(
            n.adaptation_trace
            for n in nodes
        ) / NUM_NODES
    )

    local_continuity_support = (
        sum(
            n.persistence_score
            for n in nodes
        ) / NUM_NODES
    )

    cross_region_propagation_instability = (
        sum(
            n.instability_memory
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

        "local_adaptation_propagation":
            round(
                local_adaptation_propagation,
                4
            ),

        "adaptation_decay_stability":
            round(
                adaptation_decay_stability,
                4
            ),

        "distributed_recovery_reinforcement":
            round(
                distributed_recovery_reinforcement,
                4
            ),

        "bounded_adaptation_persistence":
            round(
                bounded_adaptation_persistence,
                4
            ),

        "local_continuity_support":
            round(
                local_continuity_support,
                4
            ),

        "cross_region_propagation_instability":
            round(
                cross_region_propagation_instability,
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
            "local_adaptation_propagation"
        ]
        >= MIN_PROPAGATION,

        metrics[
            "adaptation_decay_stability"
        ]
        >= MIN_DECAY_STABILITY,

        metrics[
            "distributed_recovery_reinforcement"
        ]
        >= MIN_RECOVERY_REINFORCEMENT,

        metrics[
            "bounded_adaptation_persistence"
        ]
        >= 0.12,

        metrics[
            "local_continuity_support"
        ]
        >= MIN_CONTINUITY_SUPPORT,

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
