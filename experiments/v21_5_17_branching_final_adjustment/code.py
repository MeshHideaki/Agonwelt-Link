# Agonwelt × Gossamer
# v21.5.17
# Branching Final Adjustment
# strict validation mode

import random
import math

NUM_NODES = 84
NUM_STEPS = 1200

LOCAL_RADIUS = 0.24

BASE_REWIRE_RATE = 0.048

MAX_CONNECTIONS = 8
MIN_CONNECTIONS = 2

MAX_PATHS_PER_NODE = 6

DAMPING = 0.946

COLLAPSE_RATE = 0.046
RECONNECTION_RATE = 0.018

PATHWAY_FORMATION_RATE = 0.067
PATHWAY_MUTATION_RATE_BASE = 0.003
PATHWAY_EROSION_RATE_BASE = 0.045

GLOBAL_PATH_LIMIT = 180

MIN_INHERITANCE_PATH_DENSITY = 0.22
MAX_INHERITANCE_PATH_DENSITY = 0.58

MIN_LINEAGE_BRANCHING_RATE = 0.14
MAX_LINEAGE_BRANCHING_RATE = 0.42

MIN_PATHWAY_EROSION_RATE = 0.12
MAX_PATHWAY_EROSION_RATE = 0.38

MIN_INHERITANCE_FRICTION = 0.14
MAX_INHERITANCE_FRICTION = 0.40

MIN_LINEAGE_CONTAMINATION = 0.18
MAX_LINEAGE_CONTAMINATION = 0.56

MIN_PATHWAY_MUTATION_RATE = 0.10
MAX_PATHWAY_MUTATION_RATE = 0.36

def clamp(v, lo, hi):
    return max(lo, min(hi, v))

def distance(a, b):
    return math.sqrt(
        (a.x - b.x) ** 2 +
        (a.y - b.y) ** 2
    )

class Node:

    def __init__(self, idx):

        self.idx = idx
        self.x = random.random()
        self.y = random.random()

        self.vx = random.uniform(-0.005, 0.005)
        self.vy = random.uniform(-0.005, 0.005)

        self.connections = set()

        self.active_structures = {}
        self.dormant_remnants = {}
        self.inheritance_paths = {}

        self.pathway_mutations = 0
        self.pathway_erosions = 0
        self.lineage_branches = 0

        self.total_paths_created = 0
        self.total_mutation_events = 0

        self.inheritance_friction = random.uniform(
            0.18,
            0.24
        )

        self.lineage_contamination = random.uniform(
            0.20,
            0.26
        )

        self.pathway_cooldown = 0

def initialize_network():

    nodes = [
        Node(i)
        for i in range(NUM_NODES)
    ]

    for node in nodes:

        nearby = sorted(
            nodes,
            key=lambda n: distance(node, n)
        )

        for other in nearby[1:6]:

            node.connections.add(other.idx)

            node.active_structures[
                other.idx
            ] = random.uniform(
                0.10,
                0.18
            )

    return nodes

def update_inheritance_pathways(nodes):

    global_path_count = sum(
        len(n.inheritance_paths)
        for n in nodes
    )

    for node in nodes:

        if node.pathway_cooldown > 0:
            node.pathway_cooldown -= 1

        nearby = [
            other
            for other in nodes
            if (
                other.idx != node.idx
                and distance(node, other)
                < LOCAL_RADIUS
            )
        ]

        if not nearby:
            continue

        collapse_targets = []

        for target_id in list(
            node.active_structures.keys()
        ):

            strength = (
                node.active_structures[target_id]
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

        for target_id in collapse_targets:

            if len(node.dormant_remnants) < 6:

                node.dormant_remnants[
                    target_id
                ] = {
                    "strength":
                    random.uniform(
                        0.024,
                        0.055
                    ),
                    "age": 0
                }

            del node.active_structures[
                target_id
            ]

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
            remnant["strength"] *= 0.988

            if remnant["strength"] <= 0.005:

                remove_remnants.append(
                    remnant_id
                )

                continue

            if (
                remnant["age"] > 12
                and node.pathway_cooldown == 0
                and random.random()
                < RECONNECTION_RATE
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

                    if (
                        len(node.inheritance_paths)
                        < MAX_PATHS_PER_NODE
                        and global_path_count
                        < GLOBAL_PATH_LIMIT
                        and random.random()
                        < PATHWAY_FORMATION_RATE
                    ):

                        node.inheritance_paths[
                            target.idx
                        ] = {
                            "strength":
                            random.uniform(
                                0.10,
                                0.18
                            ),
                            "age": 0,
                            "usage": 1
                        }

                        node.total_paths_created += 1

                    node.pathway_cooldown = (
                        random.randint(
                            6,
                            12
                        )
                    )

                    remove_remnants.append(
                        remnant_id
                    )

        for remnant_id in remove_remnants:

            if remnant_id in node.dormant_remnants:

                del node.dormant_remnants[
                    remnant_id
                ]

        remove_paths = []

        for path_id in list(
            node.inheritance_paths.keys()
        ):

            path = (
                node.inheritance_paths[
                    path_id
                ]
            )

            path["age"] += 1
            path["strength"] *= 0.997

            if random.random() < 0.075:
                path["usage"] += 1

            if path["usage"] > 3:
                path["strength"] += 0.0006

            if (
                path["age"] > 60
                and
                path["usage"] < 4
                and
                random.random()
                < PATHWAY_EROSION_RATE_BASE
            ):

                node.pathway_erosions += 1

                path["strength"] -= random.uniform(
                    0.02,
                    0.04
                )

            if (
                path["usage"] > 18
                and
                random.random()
                < PATHWAY_MUTATION_RATE_BASE
            ):

                node.pathway_mutations += 1
                node.total_mutation_events += 1

                path["strength"] += random.uniform(
                    -0.003,
                    0.003
                )

            if (
                path["usage"] > 21
                and
                len(
                    node.inheritance_paths
                ) < MAX_PATHS_PER_NODE
                and
                random.random()
                < 0.004
            ):

                candidates = [
                    other
                    for other in nearby
                    if (
                        other.idx
                        not in
                        node.inheritance_paths
                    )
                ]

                if candidates:

                    branch = random.choice(
                        candidates
                    )

                    node.inheritance_paths[
                        branch.idx
                    ] = {
                        "strength":
                        path["strength"] * 0.40,
                        "age": 0,
                        "usage": 0
                    }

                    node.lineage_branches += 1

            if (
                path["strength"] <= 0.010
                or
                path["age"] > 320
            ):
                remove_paths.append(
                    path_id
                )

        for path_id in remove_paths:

            if path_id in node.inheritance_paths:

                del node.inheritance_paths[
                    path_id
                ]

        node.lineage_contamination += (
            len(node.inheritance_paths)
            * 0.0005
        )

        node.lineage_contamination *= 0.9993

        node.lineage_contamination = clamp(
            node.lineage_contamination,
            0.18,
            0.56
        )

        node.inheritance_friction += (
            len(node.inheritance_paths)
            * 0.00010
        )

        node.inheritance_friction *= 0.9995

        node.inheritance_friction = clamp(
            node.inheritance_friction,
            0.14,
            0.40
        )

def update_positions(nodes):

    for node in nodes:

        nearby = [
            other
            for other in nodes
            if (
                other.idx != node.idx
                and distance(node, other)
                < LOCAL_RADIUS
            )
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

            node.vx += (
                (cx - node.x)
                * 0.0010
            )

            node.vy += (
                (cy - node.y)
                * 0.0010
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

def update_connections(nodes):

    for node in nodes:

        nearby = [
            other
            for other in nodes
            if (
                other.idx != node.idx
                and distance(node, other)
                < LOCAL_RADIUS
            )
        ]

        if not nearby:
            continue

        if (
            random.random()
            < BASE_REWIRE_RATE
            and
            len(node.connections)
            > MIN_CONNECTIONS
        ):

            node.connections.remove(
                random.choice(
                    list(node.connections)
                )
            )

        if (
            random.random()
            < BASE_REWIRE_RATE
            and
            len(node.connections)
            < MAX_CONNECTIONS
        ):

            node.connections.add(
                random.choice(
                    nearby
                ).idx
            )

def compute_metrics(nodes):

    total_paths = sum(
        len(n.inheritance_paths)
        for n in nodes
    )

    total_branches = sum(
        n.lineage_branches
        for n in nodes
    )

    total_erosions = sum(
        n.pathway_erosions
        for n in nodes
    )

    total_mutations = sum(
        n.total_mutation_events
        for n in nodes
    )

    total_created = max(
        1,
        sum(
            n.total_paths_created
            for n in nodes
        )
    )

    return {

        "inheritance_path_density":
        round(
            total_paths
            / NUM_NODES,
            4
        ),

        "lineage_branching_rate":
        round(
            total_branches
            / total_created,
            4
        ),

        "pathway_erosion_rate":
        round(
            total_erosions
            / total_created,
            4
        ),

        "inheritance_friction":
        round(
            sum(
                n.inheritance_friction
                for n in nodes
            )
            / NUM_NODES,
            4
        ),

        "lineage_contamination_pressure":
        round(
            sum(
                n.lineage_contamination
                for n in nodes
            )
            / NUM_NODES,
            4
        ),

        "pathway_mutation_rate":
        round(
            total_mutations
            / total_created,
            4
        ),
    }

def validate(metrics):

    return all([

        0.22 <= metrics[
            "inheritance_path_density"
        ] <= 0.58,

        0.14 <= metrics[
            "lineage_branching_rate"
        ] <= 0.42,

        0.12 <= metrics[
            "pathway_erosion_rate"
        ] <= 0.38,

        0.14 <= metrics[
            "inheritance_friction"
        ] <= 0.40,

        0.18 <= metrics[
            "lineage_contamination_pressure"
        ] <= 0.56,

        0.10 <= metrics[
            "pathway_mutation_rate"
        ] <= 0.36,
    ])

def run(seed):

    random.seed(seed)

    nodes = initialize_network()

    for _ in range(NUM_STEPS):

        update_inheritance_pathways(
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

overall = True

for seed in [42, 43, 44]:

    metrics, validation_result = run(
        seed
    )

    print(
        f"\n--- RUN #{seed} ---"
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
