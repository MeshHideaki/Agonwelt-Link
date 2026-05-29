# Agonwelt × Gossamer
# v21.4.6
# Final Reconnection Tuning
# strict validation mode

import random
import math

# ==================================================
# configuration
# ==================================================

NUM_NODES = 84
NUM_STEPS = 1200

LOCAL_RADIUS = 0.24

BASE_REWIRE_RATE = 0.048

MAX_CONNECTIONS = 8
MIN_CONNECTIONS = 2

DAMPING = 0.946

COLLAPSE_RATE = 0.046

RECONNECTION_RATE = 0.0178

MUTATION_RATE = 0.22

LEGACY_PRESSURE_GAIN = 0.0048
FRICTION_GAIN = 0.0060
IDENTITY_LOSS_GAIN = 0.0042

MAX_ALIGNMENT = 0.32


# ==================================================
# validation thresholds
# ==================================================

MIN_COLLAPSE_RECONNECTION_RATE = 0.18
MAX_COLLAPSE_RECONNECTION_RATE = 0.52

MIN_RECONNECTION_MUTATION_RATE = 0.12
MAX_RECONNECTION_MUTATION_RATE = 0.42

MIN_DORMANT_REUSE_RATIO = 0.24
MAX_DORMANT_REUSE_RATIO = 0.68

MIN_LEGACY_CONTAMINATION_PRESSURE = 0.18
MAX_LEGACY_CONTAMINATION_PRESSURE = 0.58

MIN_RECONNECTION_FRICTION = 0.14
MAX_RECONNECTION_FRICTION = 0.40

MIN_STRUCTURAL_IDENTITY_LOSS = 0.20
MAX_STRUCTURAL_IDENTITY_LOSS = 0.60


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

        self.region_signature = random.uniform(
            0.20,
            0.80
        )

        self.structure_type = random.randint(
            0,
            4
        )

        self.active_structures = {}
        self.dormant_remnants = {}

        self.reconnection_count = 0
        self.mutation_count = 0
        self.reuse_count = 0

        self.reconnection_cooldown = 0

        self.identity_loss = random.uniform(
            0.22,
            0.28
        )

        self.reconnection_friction = random.uniform(
            0.16,
            0.22
        )

        self.legacy_contamination = random.uniform(
            0.20,
            0.26
        )


# ==================================================
# initialization
# ==================================================

def initialize_network():

    nodes = [
        Node(i)
        for i in range(NUM_NODES)
    ]

    for node in nodes:

        nearby = sorted(
            nodes,
            key=lambda n: distance(
                node,
                n
            )
        )

        for other in nearby[1:6]:

            node.connections.add(
                other.idx
            )

            node.active_structures[
                other.idx
            ] = random.uniform(
                0.10,
                0.18
            )

    return nodes

# ==================================================
# collapse reconnection ecology
# ==================================================

def update_collapse_reconnection(nodes):

    global_mean = (
        sum(
            n.region_signature
            for n in nodes
        )
        / NUM_NODES
    )

    for node in nodes:

        if node.reconnection_cooldown > 0:
            node.reconnection_cooldown -= 1

        nearby = [
            other
            for other in nodes
            if (
                other.idx != node.idx
                and
                distance(
                    node,
                    other
                ) < LOCAL_RADIUS
            )
        ]

        if not nearby:
            continue

        collapse_targets = []

        for target_id in list(
            node.active_structures.keys()
        ):

            strength = (
                node.active_structures[
                    target_id
                ]
            )

            strength *= 0.994

            if (
                random.random()
                < COLLAPSE_RATE
            ):
                strength -= random.uniform(
                    0.05,
                    0.11
                )

            node.active_structures[
                target_id
            ] = strength

            if strength <= 0.04:

                collapse_targets.append(
                    target_id
                )

        # ------------------------------------------
        # remnant creation
        # ------------------------------------------

        for target_id in collapse_targets:

            if (
                len(
                    node.dormant_remnants
                ) < 5
            ):

                node.dormant_remnants[
                    target_id
                ] = {

                    "strength":
                    random.uniform(
                        0.024,
                        0.051
                    ),

                    "origin":
                    node.structure_type,

                    "age":
                    0
                }

            del node.active_structures[
                target_id
            ]

        # ------------------------------------------
        # remnant evolution
        # ------------------------------------------

        remove_remnants = []

        for remnant_id in list(
            node.dormant_remnants.keys()
        ):

            remnant = (
                node.dormant_remnants[
                    remnant_id
                ]
            )

            remnant["age"] += 1

            remnant["strength"] *= (
                0.984
            )

            remnant["strength"] += (
                random.uniform(
                    -0.001,
                    0.001
                )
            )

            reconnect_bias = (
                RECONNECTION_RATE
            )

            if remnant["age"] < 40:
                reconnect_bias *= 0.70

            if (
                node.reconnection_cooldown == 0
                and
                remnant["age"] > 16
                and
                remnant["strength"] > 0.0185
                and
                random.random()
                < reconnect_bias
            ):

                candidates = [
                    other
                    for other in nearby
                    if (
                        other.idx
                        not in
                        node.active_structures
                    )
                ]

                if candidates:

                    target = random.choice(
                        candidates
                    )

                    node.active_structures[
                        target.idx
                    ] = random.uniform(
                        0.05,
                        0.10
                    )

                    node.reconnection_count += 1
                    node.reuse_count += 1

                    node.reconnection_cooldown = (
                        random.randint(
                            12,
                            22
                        )
                    )

                    mutation_happened = False

                    if (
                        random.random()
                        < MUTATION_RATE
                    ):

                        mutation_happened = True

                        node.mutation_count += 1

                        node.structure_type = (
                            node.structure_type
                            +
                            random.randint(
                                1,
                                4
                            )
                        ) % 5

                        node.region_signature += (
                            random.uniform(
                                -0.10,
                                0.10
                            )
                        )

                    node.identity_loss += (
                        IDENTITY_LOSS_GAIN
                    )

                    if mutation_happened:

                        node.identity_loss += (
                            random.uniform(
                                0.004,
                                0.012
                            )
                        )

                    node.reconnection_friction += (
                        FRICTION_GAIN
                    )

                    node.legacy_contamination += (
                        LEGACY_PRESSURE_GAIN
                    )

                    remove_remnants.append(
                        remnant_id
                    )

            elif (
                remnant["strength"]
                <= 0.005
            ):

                remove_remnants.append(
                    remnant_id
                )

        for remnant_id in remove_remnants:

            if remnant_id in node.dormant_remnants:

                del node.dormant_remnants[
                    remnant_id
                ]

        node.legacy_contamination *= (
            0.999
        )

        node.legacy_contamination += (
            len(
                node.dormant_remnants
            )
            * 0.0009
        )

        node.legacy_contamination = clamp(
            node.legacy_contamination,
            0.18,
            0.60
        )

        node.reconnection_friction *= (
            0.9995
        )

        node.reconnection_friction = clamp(
            node.reconnection_friction,
            0.14,
            0.42
        )

        node.identity_loss *= (
            0.9995
        )

        node.identity_loss = clamp(
            node.identity_loss,
            0.20,
            0.70
        )

        node.region_signature += (
            random.uniform(
                -0.003,
                0.003
            )
        )

        offset = abs(
            node.region_signature
            -
            global_mean
        )

        if offset < 0.08:

            node.region_signature += (
                random.uniform(
                    -0.015,
                    0.015
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
            other
            for other in nodes
            if (
                other.idx != node.idx
                and
                distance(
                    node,
                    other
                ) < LOCAL_RADIUS
            )
        ]

        if nearby:

            cx = (
                sum(
                    n.x
                    for n in nearby
                )
                / len(nearby)
            )

            cy = (
                sum(
                    n.y
                    for n in nearby
                )
                / len(nearby)
            )

            cohesion = (
                0.0010
                +
                min(
                    5,
                    len(
                        node.active_structures
                    )
                )
                * 0.00005
            )

            node.vx += (
                (cx - node.x)
                * cohesion
            )

            node.vy += (
                (cy - node.y)
                * cohesion
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
            other
            for other in nodes
            if (
                other.idx != node.idx
                and
                distance(
                    node,
                    other
                ) < LOCAL_RADIUS
            )
        ]

        if not nearby:
            continue

        if (
            random.random()
            < BASE_REWIRE_RATE
        ):

            if (
                len(node.connections)
                > MIN_CONNECTIONS
            ):

                node.connections.remove(
                    random.choice(
                        list(
                            node.connections
                        )
                    )
                )

        if (
            random.random()
            < BASE_REWIRE_RATE
        ):

            if (
                len(node.connections)
                < MAX_CONNECTIONS
            ):

                node.connections.add(
                    random.choice(
                        nearby
                    ).idx
                )


# ==================================================
# metrics
# ==================================================

def compute_metrics(nodes):

    total_reconnections = sum(
        n.reconnection_count
        for n in nodes
    )

    total_mutations = sum(
        n.mutation_count
        for n in nodes
    )

    total_reuse = sum(
        n.reuse_count
        for n in nodes
    )

    return {

        "collapse_reconnection_rate":
        round(
            total_reconnections
            /
            (NUM_NODES * 6),
            4
        ),

        "reconnection_mutation_rate":
        round(
            total_mutations
            /
            max(
                1,
                total_reconnections
            ),
            4
        ),

        "dormant_reuse_ratio":
        round(
            total_reuse
            /
            (NUM_NODES * 3),
            4
        ),

        "legacy_contamination_pressure":
        round(
            sum(
                n.legacy_contamination
                for n in nodes
            )
            /
            NUM_NODES,
            4
        ),

        "reconnection_friction":
        round(
            sum(
                n.reconnection_friction
                for n in nodes
            )
            /
            NUM_NODES,
            4
        ),

        "structural_identity_loss":
        round(
            sum(
                n.identity_loss
                for n in nodes
            )
            /
            NUM_NODES,
            4
        ),
    }


# ==================================================
# validation
# ==================================================

def validate(metrics):

    return all([

        0.18 <= metrics[
            "collapse_reconnection_rate"
        ] <= 0.52,

        0.12 <= metrics[
            "reconnection_mutation_rate"
        ] <= 0.42,

        0.24 <= metrics[
            "dormant_reuse_ratio"
        ] <= 0.68,

        0.18 <= metrics[
            "legacy_contamination_pressure"
        ] <= 0.58,

        0.14 <= metrics[
            "reconnection_friction"
        ] <= 0.40,

        0.20 <= metrics[
            "structural_identity_loss"
        ] <= 0.60,
    ])


# ==================================================
# run
# ==================================================

def run(seed):

    random.seed(seed)

    nodes = initialize_network()

    for _ in range(NUM_STEPS):

        update_collapse_reconnection(
            nodes
        )

        update_positions(
            nodes
        )

        update_connections(
            nodes
        )

    metrics = compute_metrics(
        nodes
    )

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

    print(
        f"\n--- RUN #{seed} ---"
    )

    metrics, validation_result = run(
        seed
    )

    for k, v in metrics.items():

        print(
            f"{k}: {v}"
        )

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
