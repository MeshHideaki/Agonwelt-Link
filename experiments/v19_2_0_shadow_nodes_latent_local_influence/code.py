# Agonwelt-Link v19.2.0
# shadow nodes latent local influence
# strict validation mode

import random
import math

# ==================================================
# configuration
# ==================================================

NUM_NODES = 72
NUM_STEPS = 380

LOCAL_RADIUS = 0.24

BASE_REWIRE_RATE = 0.040
BASE_COLLAPSE_THRESHOLD = 0.29

MAX_CONNECTIONS = 8
MIN_CONNECTIONS = 2

DAMPING = 0.95

# shadow system
SHADOW_MEMORY_DECAY = 0.985
SHADOW_INFLUENCE_SCALE = 0.018
SHADOW_REINFORCEMENT_SCALE = 0.012

# bounded diversity
MIN_REGION_DIVERSITY = 0.14
MAX_REGION_DIVERSITY = 0.78

# validation thresholds
MIN_SHADOW_STABILITY = 0.52
MIN_LOCAL_CONTINUITY = 0.58
MIN_RECOVERY_REINFORCEMENT = 0.45
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
            0.28,
            0.72
        )

        # latent residual structure
        self.shadow_memory = random.uniform(
            0.20,
            0.40
        )

        self.shadow_echo = 0.0

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
# shadow ecology
# ==================================================

def update_shadow_ecology(nodes):

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

        # ==================================================
        # shadow residual interaction
        # ==================================================

        local_shadow = (
            sum(
                other.shadow_memory
                for other in nearby
            ) / len(nearby)
        )

        local_signature = (
            sum(
                other.region_signature
                for other in nearby
            ) / len(nearby)
        )

        instability_gap = abs(
            node.local_pressure
            - node.local_stability
        )

        # local interaction echo
        node.shadow_echo = (
            0.90 * node.shadow_echo
            +
            instability_gap * 0.10
        )

        # memory-like persistence
        node.shadow_memory *= (
            SHADOW_MEMORY_DECAY
        )

        node.shadow_memory += (
            local_shadow
            * SHADOW_INFLUENCE_SCALE
        )

        node.shadow_memory += (
            node.shadow_echo
            * SHADOW_REINFORCEMENT_SCALE
        )

        node.shadow_memory += random.uniform(
            -0.003,
            0.003
        )

        node.shadow_memory = clamp(
            node.shadow_memory,
            0.0,
            1.0
        )

        # ==================================================
        # latent influence
        # ==================================================

        divergence_force = (
            node.local_pressure
            - node.local_stability
        )

        latent_shift = (
            node.shadow_memory
            - local_shadow
        )

        # visible + latent interaction
        node.region_signature += (
            divergence_force * 0.016
        )

        node.region_signature += (
            latent_shift * 0.018
        )

        # weak continuity convergence
        node.region_signature += (
            local_signature
            - node.region_signature
        ) * 0.003

        # divergence floor preservation
        if global_divergence < 0.22:

            node.region_signature += (
                random.uniform(
                    -0.050,
                    0.050
                )
            )

        elif global_divergence < 0.30:

            node.region_signature += (
                random.uniform(
                    -0.020,
                    0.020
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
                * 0.0025
            )

            node.vy += (
                (cy - node.y)
                * 0.0025
            )

            # latent directional bias
            shadow_bias = (
                node.shadow_memory - 0.5
            )

            node.vx += (
                shadow_bias * 0.0014
            )

            node.vy += (
                -shadow_bias * 0.0014
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

        shadow_factor = (
            node.shadow_memory
            * 0.020
        )

        rewire_rate = (
            BASE_REWIRE_RATE
            + instability * 0.024
            + shadow_factor
        )

        # ==================================================
        # indirect rewiring tendency
        # ==================================================

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

                shadow_gap = abs(
                    target.shadow_memory
                    - node.shadow_memory
                )

                if (
                    signature_gap > 0.40
                    and shadow_gap > 0.20
                ):

                    removable.append(cid)

            if removable:

                remove_id = random.choice(
                    removable
                )

                node.connections.remove(
                    remove_id
                )

        # ==================================================
        # latent recovery rewiring
        # ==================================================

        if (
            random.random() < (
                rewire_rate * 1.40
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

                shadow_gap = abs(
                    other.shadow_memory
                    - node.shadow_memory
                )

                if (
                    signature_gap < 0.44
                    and shadow_gap < 0.22
                ):

                    compatible.append(
                        (
                            shadow_gap,
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
            + node.shadow_memory * 0.020
        )

        # ==================================================
        # bounded collapse
        # ==================================================

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

                # shadow persistence effect
                node.persistence_score *= (
                    0.998
                    +
                    node.shadow_memory
                    * 0.002
                )

        # ==================================================
        # local recovery reinforcement
        # ==================================================

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

                shadow_gap = abs(
                    other.shadow_memory
                    - node.shadow_memory
                )

                if (
                    signature_gap < 0.46
                    and shadow_gap < 0.24
                ):

                    compatible.append(
                        other
                    )

            compatible = sorted(
                compatible,
                key=lambda n:
                    abs(
                        n.shadow_memory
                        - node.shadow_memory
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

                # latent recovery continuity
                node.persistence_score *= (
                    1.010
                    + (
                        node.shadow_memory
                        * 0.004
                    )
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

    shadow_persistence_stability = (
        sum(
            n.shadow_memory
            for n in nodes
        ) / NUM_NODES
    )

    local_latent_influence_continuity = (
        sum(
            n.persistence_score
            for n in nodes
        ) / NUM_NODES
    )

    total_recovery = sum(
        n.recovery_events
        for n in nodes
    )

    total_collapse = sum(
        n.collapse_events
        for n in nodes
    )

    distributed_recovery_reinforcement = (
        total_recovery
        /
        max(1, total_collapse)
    )

    signatures = [
        n.region_signature
        for n in nodes
    ]

    bounded_shadow_divergence = (
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

    cross_region_latent_instability = (
        sum(
            n.instability_memory
            for n in nodes
        ) / NUM_NODES
    )

    local_recovery_continuity = (
        sum(
            n.shadow_echo
            for n in nodes
        ) / NUM_NODES
    )

    return {

        "shadow_persistence_stability":
            round(
                shadow_persistence_stability,
                4
            ),

        "local_latent_influence_continuity":
            round(
                local_latent_influence_continuity,
                4
            ),

        "distributed_recovery_reinforcement":
            round(
                distributed_recovery_reinforcement,
                4
            ),

        "bounded_shadow_divergence":
            round(
                bounded_shadow_divergence,
                4
            ),

        "structural_persistence":
            round(
                structural_persistence,
                4
            ),

        "cross_region_latent_instability":
            round(
                cross_region_latent_instability,
                4
            ),

        "local_recovery_continuity":
            round(
                local_recovery_continuity,
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
            "bounded_shadow_divergence"
        ]
        <= MAX_REGION_DIVERSITY
    )

    return all([

        metrics[
            "shadow_persistence_stability"
        ]
        >= MIN_SHADOW_STABILITY,

        metrics[
            "local_latent_influence_continuity"
        ]
        >= MIN_LOCAL_CONTINUITY,

        metrics[
            "distributed_recovery_reinforcement"
        ]
        >= MIN_RECOVERY_REINFORCEMENT,

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

        update_shadow_ecology(nodes)

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
