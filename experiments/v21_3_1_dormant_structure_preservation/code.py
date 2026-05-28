# Agonwelt × Gossamer
# v21.3.1
# Dormant Structure Preservation
# strict validation mode

import random
import math

# ==================================================
# configuration
# ==================================================

NUM_NODES = 82
NUM_STEPS = 1100

LOCAL_RADIUS = 0.24

BASE_REWIRE_RATE = 0.046

MAX_CONNECTIONS = 8
MIN_CONNECTIONS = 2

DAMPING = 0.947

# dormant ecology

DORMANT_FORMATION_RATE = 0.084
DORMANT_DECAY = 0.9956
DORMANT_COLLAPSE_RATE = 0.036

REAWAKENING_RATE = 0.008

INSTABILITY_NOISE = 0.005

MAX_ALIGNMENT = 0.32

# ==================================================
# validation thresholds
# ==================================================

MIN_DORMANT_STRUCTURE_PERSISTENCE = 0.28
MAX_DORMANT_STRUCTURE_PERSISTENCE = 0.66

MIN_REACTIVATION_INSTABILITY = 0.12
MAX_REACTIVATION_INSTABILITY = 0.34

MIN_DORMANT_CONTAMINATION_PRESSURE = 0.18
MAX_DORMANT_CONTAMINATION_PRESSURE = 0.56

MIN_FRAGMENTED_DORMANT_DECAY = 0.16
MAX_FRAGMENTED_DORMANT_DECAY = 0.48

MIN_PARTIAL_REAWAKENING_SUCCESS = 0.10
MAX_PARTIAL_REAWAKENING_SUCCESS = 0.42

MIN_CROSS_STRUCTURE_DORMANT_FRICTION = 0.14
MAX_CROSS_STRUCTURE_DORMANT_FRICTION = 0.38

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

        self.persistence_field = random.uniform(
            0.10,
            0.24
        )

        self.local_pressure = random.uniform(
            0.40,
            0.60
        )

        self.local_stability = random.uniform(
            0.42,
            0.64
        )

        self.active_structures = {}

        self.dormant_structures = {}

        self.reactivation_instability = random.uniform(
            0.08,
            0.12
        )

        self.dormant_friction = random.uniform(
            0.10,
            0.13
        )

        self.dormant_decay = random.uniform(
            0.18,
            0.24
        )

        self.dormant_contamination = random.uniform(
            0.12,
            0.18
        )

        self.fragmentation_level = random.uniform(
            0.03,
            0.08
        )

        self.partial_reactivation_count = 0

# ==================================================
# utility
# ==================================================

def clamp(v, lo, hi):

    return max(
        lo,
        min(hi, v)
    )

def distance(a, b):

    return math.sqrt(
        (a.x - b.x) ** 2
        +
        (a.y - b.y) ** 2
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
            key=lambda n: distance(node, n)
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
# dormant ecology
# ==================================================

def update_dormant_ecology(nodes):

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

    global_mean = (
        sum(
            n.region_signature
            for n in nodes
        )
        / NUM_NODES
    )

    for node in nodes:

        nearby = [
            other for other in nodes
            if (
                other.idx != node.idx
                and
                distance(node, other)
                < LOCAL_RADIUS
            )
        ]

        if not nearby:
            continue

        local_density = (
            len(nearby)
            / NUM_NODES
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

        instability_gap = abs(
            local_density
            -
            local_connectivity
        )

        node.local_pressure = (
            0.92
            * node.local_pressure
            +
            0.08
            * instability_gap
        )

        node.local_stability = (
            0.90
            * node.local_stability
            +
            0.10
            * local_connectivity
        )

        pressure_gap = abs(
            node.local_pressure
            -
            node.local_stability
        )

        remove_active = []

        # ==========================================
        # active structures
        # ==========================================

        for target_id in list(
            node.active_structures.keys()
        ):

            strength = (
                node.active_structures[
                    target_id
                ]
            )

            target = nodes[target_id]

            signature_gap = abs(
                node.region_signature
                -
                target.region_signature
            )

            structure_gap = abs(
                node.structure_type
                -
                target.structure_type
            )

            strength *= DORMANT_DECAY

            strength -= (
                signature_gap
                * 0.013
            )

            strength -= (
                structure_gap
                * 0.006
            )

            if (
                random.random()
                < 0.36
            ):

                strength += random.uniform(
                    -0.008,
                    0.014
                )

            if (
                random.random()
                < DORMANT_COLLAPSE_RATE
            ):

                strength -= random.uniform(
                    0.05,
                    0.10
                )

                node.reactivation_instability += (
                    random.uniform(
                        0.004,
                        0.008
                    )
                )

            node.active_structures[
                target_id
            ] = strength

            if (
                target.persistence_field
                >
                node.persistence_field
            ):

                node.dormant_contamination += (
                    0.0016
                )

            node.dormant_friction += (
                structure_gap
                * 0.0034
            )

            if strength <= 0.040:

                remove_active.append(
                    target_id
                )

        # ==========================================
        # dormant conversion
        # ==========================================

        for target_id in remove_active:

            if (
                len(node.dormant_structures)
                < 3
            ):

                node.dormant_structures[
                    target_id
                ] = random.uniform(
                    0.014,
                    0.036
                )

            del node.active_structures[
                target_id
            ]

        # ==========================================
        # dormant preservation
        # ==========================================

        remove_dormant = []

        for target_id in list(
            node.dormant_structures.keys()
        ):

            dormant_strength = (
                node.dormant_structures[
                    target_id
                ]
            )

            dormant_strength *= 0.975

            dormant_strength += random.uniform(
                -0.003,
                0.001
            )

            node.dormant_structures[
                target_id
            ] = dormant_strength

            node.dormant_decay += (
                random.uniform(
                    0.0001,
                    0.0004
                )
            )

            if (
                dormant_strength > 0.022
                and
                random.random()
                < REAWAKENING_RATE
            ):

                restored = random.uniform(
                    0.05,
                    0.10
                )

                node.active_structures[
                    target_id
                ] = restored

                node.partial_reactivation_count += 1

                remove_dormant.append(
                    target_id
                )

            elif dormant_strength <= 0.008:

                remove_dormant.append(
                    target_id
                )

        for target_id in remove_dormant:

            if target_id in node.dormant_structures:

                del node.dormant_structures[
                    target_id
                ]

        # ==========================================
        # structure formation
        # ==========================================

        formation_bias = (
            DORMANT_FORMATION_RATE
            +
            (
                pressure_gap
                * 0.014
            )
        )

        if (
            len(node.active_structures)
            >= 6
        ):

            formation_bias *= 0.74

        if (
            node.dormant_contamination
            > 0.38
        ):

            formation_bias *= 0.86

        if (
            random.random()
            < formation_bias
        ):

            candidates = []

            for other in nearby:

                if (
                    other.idx
                    in node.active_structures
                ):
                    continue

                signature_gap = abs(
                    other.region_signature
                    -
                    node.region_signature
                )

                if signature_gap < 0.38:

                    candidates.append(
                        other
                    )

            if candidates:

                target = random.choice(
                    candidates
                )

                node.active_structures[
                    target.idx
                ] = random.uniform(
                    0.10,
                    0.17
                )

        # ==========================================
        # fragmentation
        # ==========================================

        node.fragmentation_level *= 0.994

        node.fragmentation_level += (
            pressure_gap
            * 0.004
        )

        node.fragmentation_level += random.uniform(
            -0.002,
            0.002
        )

        node.fragmentation_level = clamp(
            node.fragmentation_level,
            0.02,
            0.42
        )

        # ==========================================
        # instability
        # ==========================================

        node.reactivation_instability *= 0.997

        node.reactivation_instability += (
            node.fragmentation_level
            * 0.0017
        )

        node.reactivation_instability = clamp(
            node.reactivation_instability,
            0.04,
            MAX_ALIGNMENT
        )

        # ==========================================
        # dormant decay
        # ==========================================

        node.dormant_decay *= 0.996

        node.dormant_decay += (
            pressure_gap
            * 0.0024
        )

        node.dormant_decay = clamp(
            node.dormant_decay,
            0.12,
            0.50
        )

        # ==========================================
        # contamination
        # ==========================================

        node.dormant_contamination *= 0.995

        node.dormant_contamination += (
            len(node.dormant_structures)
            * 0.00026
        )

        node.dormant_contamination += (
            len(node.active_structures)
            * 0.00018
        )

        node.dormant_contamination = clamp(
            node.dormant_contamination,
            0.04,
            0.58
        )

        # ==========================================
        # dormant friction
        # ==========================================

        node.dormant_friction *= 0.995

        node.dormant_friction += (
            node.fragmentation_level
            * 0.0010
        )

        node.dormant_friction = clamp(
            node.dormant_friction,
            0.08,
            0.375
        )

        # ==========================================
        # divergence
        # ==========================================

        if global_divergence < 0.18:

            polarity = (
                1
                if node.region_signature
                >= global_mean
                else -1
            )

            node.region_signature += (
                polarity
                * random.uniform(
                    0.010,
                    0.020
                )
            )

        elif global_divergence > 0.74:

            node.region_signature += (
                (
                    global_mean
                    - node.region_signature
                )
                * 0.010
            )

        else:

            node.region_signature += (
                random.uniform(
                    -0.003,
                    0.003
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
                and
                distance(node, other)
                < LOCAL_RADIUS
            )
        ]

        if nearby:

            cx = (
                sum(
                    n.x for n in nearby
                )
                / len(nearby)
            )

            cy = (
                sum(
                    n.y for n in nearby
                )
                / len(nearby)
            )

            cohesion_strength = (
                0.0010
                +
                (
                    min(
                        5,
                        len(node.active_structures)
                    )
                    * 0.00005
                )
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
                -0.002,
                0.002
            )

            node.vy += random.uniform(
                -0.002,
                0.002
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
                and
                distance(node, other)
                < LOCAL_RADIUS
            )
        ]

        if not nearby:
            continue

        instability = abs(
            node.local_pressure
            -
            node.local_stability
        )

        rewire_rate = (
            BASE_REWIRE_RATE
            +
            instability
            * 0.013
        )

        if (
            random.random()
            < rewire_rate
            and
            len(node.connections)
            > MIN_CONNECTIONS
        ):

            removable = []

            for cid in node.connections:

                target = nodes[cid]

                signature_gap = abs(
                    target.region_signature
                    -
                    node.region_signature
                )

                if signature_gap > 0.40:

                    removable.append(cid)

            if removable:

                remove_id = random.choice(
                    removable
                )

                node.connections.remove(
                    remove_id
                )

        if (
            random.random()
            < rewire_rate * 1.03
            and
            len(node.connections)
            < MAX_CONNECTIONS
        ):

            candidates = []

            for other in nearby:

                if (
                    other.idx
                    in node.connections
                ):
                    continue

                signature_gap = abs(
                    other.region_signature
                    -
                    node.region_signature
                )

                if signature_gap < 0.36:

                    candidates.append(
                        other
                    )

            if candidates:

                target = random.choice(
                    candidates
                )

                node.connections.add(
                    target.idx
                )

# ==================================================
# metrics
# ==================================================

def compute_metrics(nodes):

    dormant_structure_persistence = (
        sum(
            len(n.dormant_structures)
            for n in nodes
        )
        /
        (
            NUM_NODES * 2.0
        )
    )

    reactivation_instability = (
        sum(
            n.reactivation_instability
            for n in nodes
        )
        / NUM_NODES
    )

    dormant_contamination_pressure = (
        sum(
            n.dormant_contamination
            for n in nodes
        )
        / NUM_NODES
    )

    fragmented_dormant_decay = (
        sum(
            n.dormant_decay
            for n in nodes
        )
        / NUM_NODES
    )

    partial_reawakening_success = (
        sum(
            n.partial_reactivation_count
            for n in nodes
        )
        /
        (
            NUM_NODES * 10
        )
    )

    cross_structure_dormant_friction = (
        sum(
            n.dormant_friction
            for n in nodes
        )
        / NUM_NODES
    )

    return {

        "dormant_structure_persistence":
            round(
                dormant_structure_persistence,
                4
            ),

        "reactivation_instability":
            round(
                reactivation_instability,
                4
            ),

        "dormant_contamination_pressure":
            round(
                dormant_contamination_pressure,
                4
            ),

        "fragmented_dormant_decay":
            round(
                fragmented_dormant_decay,
                4
            ),

        "partial_reawakening_success":
            round(
                partial_reawakening_success,
                4
            ),

        "cross_structure_dormant_friction":
            round(
                cross_structure_dormant_friction,
                4
            ),
    }

# ==================================================
# validation
# ==================================================

def validate(metrics):

    return all([

        MIN_DORMANT_STRUCTURE_PERSISTENCE
        <= metrics[
            "dormant_structure_persistence"
        ]
        <= MAX_DORMANT_STRUCTURE_PERSISTENCE,

        MIN_REACTIVATION_INSTABILITY
        <= metrics[
            "reactivation_instability"
        ]
        <= MAX_REACTIVATION_INSTABILITY,

        MIN_DORMANT_CONTAMINATION_PRESSURE
        <= metrics[
            "dormant_contamination_pressure"
        ]
        <= MAX_DORMANT_CONTAMINATION_PRESSURE,

        MIN_FRAGMENTED_DORMANT_DECAY
        <= metrics[
            "fragmented_dormant_decay"
        ]
        <= MAX_FRAGMENTED_DORMANT_DECAY,

        MIN_PARTIAL_REAWAKENING_SUCCESS
        <= metrics[
            "partial_reawakening_success"
        ]
        <= MAX_PARTIAL_REAWAKENING_SUCCESS,

        MIN_CROSS_STRUCTURE_DORMANT_FRICTION
        <= metrics[
            "cross_structure_dormant_friction"
        ]
        <= MAX_CROSS_STRUCTURE_DORMANT_FRICTION,
    ])

# ==================================================
# run
# ==================================================

def run(seed):

    random.seed(seed)

    nodes = initialize_network()

    for _ in range(NUM_STEPS):

        update_dormant_ecology(nodes)

        update_positions(nodes)

        update_connections(nodes)

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
