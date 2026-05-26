# Agonwelt-Link v19.5.1
# bounded partial environmental resonance
# strict validation mode

import random
import math

# ==================================================
# configuration
# ==================================================

NUM_NODES = 72
NUM_STEPS = 520

LOCAL_RADIUS = 0.25

BASE_REWIRE_RATE = 0.040
BASE_COLLAPSE_THRESHOLD = 0.30

MAX_CONNECTIONS = 8
MIN_CONNECTIONS = 2

DAMPING = 0.95

# adaptation propagation
ADAPTATION_TRACE_DECAY = 0.994
ADAPTATION_PROPAGATION_SCALE = 0.024

# environmental resonance
ENVIRONMENT_RESONANCE_DECAY = 0.991
ENVIRONMENT_PROPAGATION_SCALE = 0.010
LOCAL_PRESSURE_RESONANCE = 0.012
RESONANCE_NOISE = 0.004

# bounded synchronization
MAX_RESONANCE_ALIGNMENT = 0.418

# bounded diversity
MIN_DIVERGENCE = 0.14
MAX_DIVERGENCE = 0.78

# validation thresholds
MIN_SYNC_STABILITY = 0.18
MIN_PROPAGATION_DECAY = 0.12
MIN_ENVIRONMENT_FLUCTUATION = 0.08
MIN_FRAGMENTED_CONTINUITY = 0.55
MIN_RECOVERY_SYNC = 0.42
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
            0.20,
            0.80
        )

        self.adaptation_trace = random.uniform(
            0.16,
            0.28
        )

        self.environment_state = random.uniform(
            0.12,
            0.26
        )

        self.environment_decay = random.uniform(
            0.02,
            0.08
        )

        self.local_resonance = 0.0

        self.persistence_score = 1.0

        self.collapse_events = 0
        self.recovery_events = 0

        self.resonance_events = 0

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

        local_environment = (
            sum(
                other.environment_state
                for other in nearby
            ) / len(nearby)
        )

        # ==================================================
        # partial environmental resonance
        # ==================================================

        previous_environment = (
            node.environment_state
        )

        node.environment_state *= (
            ENVIRONMENT_RESONANCE_DECAY
        )

        local_environment_delta = (
            (
                local_environment
                - node.environment_state
            )
            * ENVIRONMENT_PROPAGATION_SCALE
        )

        node.environment_state += (
            local_environment_delta
        )

        pressure_gap = abs(
            node.local_pressure
            - node.local_stability
        )

        node.environment_state += (
            pressure_gap
            * LOCAL_PRESSURE_RESONANCE
        )

        node.environment_state += random.uniform(
            -RESONANCE_NOISE,
            RESONANCE_NOISE
        )

        local_alignment_gap = abs(
            local_environment
            - node.environment_state
        )

        # stronger anti-sync divergence
        if (
            local_alignment_gap
            < 0.05
        ):

            node.environment_state += (
                random.uniform(
                    -0.016,
                    0.016
                )
            )

        node.environment_state = clamp(
            node.environment_state,
            0.02,
            0.78
        )

        # ==================================================
        # bounded resonance
        # ==================================================

        node.local_resonance *= 0.986

        node.local_resonance += (
            (
                1.0
                - local_alignment_gap
            ) * 0.0085
        )

        # soft saturation before hard clamp
        if (
            node.local_resonance
            > 0.390
        ):

            node.local_resonance *= 0.996

        node.local_resonance = clamp(
            node.local_resonance,
            0.0,
            MAX_RESONANCE_ALIGNMENT
        )

        if abs(
            node.environment_state
            - previous_environment
        ) > 0.0002:

            node.resonance_events += 1

        # environmental decay drift
        node.environment_decay *= 0.992

        node.environment_decay += (
            random.uniform(
                -0.003,
                0.003
            )
        )

        node.environment_decay += (
            pressure_gap * 0.004
        )

        node.environment_decay = clamp(
            node.environment_decay,
            0.0,
            0.40
        )

        # ==================================================
        # adaptation propagation
        # ==================================================

        local_trace = (
            sum(
                other.adaptation_trace
                for other in nearby
            ) / len(nearby)
        )

        node.adaptation_trace *= (
            ADAPTATION_TRACE_DECAY
        )

        node.adaptation_trace += (
            (
                local_trace
                - node.adaptation_trace
            )
            * ADAPTATION_PROPAGATION_SCALE
        )

        node.adaptation_trace += (
            node.environment_state
            * 0.006
        )

        node.adaptation_trace += random.uniform(
            -0.002,
            0.002
        )

        node.adaptation_trace = clamp(
            node.adaptation_trace,
            0.04,
            0.90
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
                node.environment_state
                - local_environment
            ) * 0.012
        )

        node.region_signature += (
            (
                node.adaptation_trace
                - local_trace
            ) * 0.008
        )

        node.region_signature += (
            local_signature
            - node.region_signature
        ) * 0.0010

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
                    0.048
                )
            )

        elif global_divergence < 0.24:

            if global_offset < 0.10:

                node.region_signature += (
                    random.uniform(
                        -0.050,
                        0.050
                    )
                )

            else:

                node.region_signature += (
                    random.uniform(
                        -0.020,
                        0.020
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
                0.0015
                +
                node.local_resonance
                * 0.0009
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
                -0.0024,
                0.0024
            )

            node.vy += random.uniform(
                -0.0024,
                0.0024
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

        resonance_factor = (
            node.local_resonance
            * 0.018
        )

        rewire_rate = (
            BASE_REWIRE_RATE
            + instability * 0.020
            + resonance_factor
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

                environment_gap = abs(
                    target.environment_state
                    - node.environment_state
                )

                if (
                    signature_gap > 0.46
                    and environment_gap > 0.16
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
                rewire_rate * 1.28
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

                environment_gap = abs(
                    other.environment_state
                    - node.environment_state
                )

                if (
                    signature_gap < 0.50
                    and environment_gap < 0.20
                ):

                    compatible.append(
                        (
                            environment_gap,
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
            + node.environment_state
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

                environment_gap = abs(
                    other.environment_state
                    - node.environment_state
                )

                if (
                    signature_gap < 0.52
                    and environment_gap < 0.22
                ):

                    compatible.append(
                        other
                    )

            compatible = sorted(
                compatible,
                key=lambda n:
                    abs(
                        n.environment_state
                        - node.environment_state
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

    partial_synchronization_stability = (
        sum(
            n.local_resonance
            for n in nodes
        ) / NUM_NODES
    )

    environmental_propagation_decay = (
        sum(
            n.environment_decay
            for n in nodes
        ) / NUM_NODES
    )

    distributed_environmental_fluctuation = (
        max(
            n.environment_state
            for n in nodes
        )
        -
        min(
            n.environment_state
            for n in nodes
        )
    )

    cross_region_resonance_instability = (
        sum(
            n.instability_memory
            for n in nodes
        ) / NUM_NODES
    )

    fragmented_continuity_persistence = (
        sum(
            n.persistence_score
            for n in nodes
        ) / NUM_NODES
    )

    local_recovery_synchronization = (
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

        "partial_synchronization_stability":
            round(
                partial_synchronization_stability,
                4
            ),

        "environmental_propagation_decay":
            round(
                environmental_propagation_decay,
                4
            ),

        "distributed_environmental_fluctuation":
            round(
                distributed_environmental_fluctuation,
                4
            ),

        "cross_region_resonance_instability":
            round(
                cross_region_resonance_instability,
                4
            ),

        "fragmented_continuity_persistence":
            round(
                fragmented_continuity_persistence,
                4
            ),

        "local_recovery_synchronization":
            round(
                local_recovery_synchronization,
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

    synchronization_ok = (
        metrics[
            "partial_synchronization_stability"
        ]
        < MAX_RESONANCE_ALIGNMENT
    )

    return all([

        metrics[
            "partial_synchronization_stability"
        ]
        >= MIN_SYNC_STABILITY,

        metrics[
            "environmental_propagation_decay"
        ]
        >= MIN_PROPAGATION_DECAY,

        metrics[
            "distributed_environmental_fluctuation"
        ]
        >= MIN_ENVIRONMENT_FLUCTUATION,

        metrics[
            "fragmented_continuity_persistence"
        ]
        >= MIN_FRAGMENTED_CONTINUITY,

        metrics[
            "local_recovery_synchronization"
        ]
        >= MIN_RECOVERY_SYNC,

        metrics[
            "structural_persistence"
        ]
        >= MIN_STRUCTURAL_PERSISTENCE,

        synchronization_ok,

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
