# Agonwelt × Gossamer
# v21.2.2
# Localized Memory Linking
# strict validation mode

import random
import math

# ==================================================
# configuration
# ==================================================

NUM_NODES = 78
NUM_STEPS = 1000

LOCAL_RADIUS = 0.24

BASE_REWIRE_RATE = 0.045

MAX_CONNECTIONS = 8
MIN_CONNECTIONS = 2

DAMPING = 0.948

# neural-memory ecology

MEMORY_FORMATION_RATE = 0.088
MEMORY_DECAY = 0.9963
MEMORY_COLLAPSE_RATE = 0.033

INSTABILITY_NOISE = 0.005

MAX_ALIGNMENT = 0.31

# divergence

MIN_DIVERGENCE = 0.16
MAX_DIVERGENCE = 0.78

# ==================================================
# validation thresholds
# ==================================================

MIN_LOCALIZED_MEMORY_PERSISTENCE = 0.32
MAX_LOCALIZED_MEMORY_PERSISTENCE = 0.70

MIN_MEMORY_DECAY_BALANCE = 0.22
MAX_MEMORY_DECAY_BALANCE = 0.58

MIN_LEGACY_CONTAMINATION_PRESSURE = 0.18
MAX_LEGACY_CONTAMINATION_PRESSURE = 0.52

MIN_FRAGMENTED_MEMORY_INSTABILITY = 0.10
MAX_FRAGMENTED_MEMORY_INSTABILITY = 0.33

MIN_DORMANT_MEMORY_SURVIVAL = 0.20
MAX_DORMANT_MEMORY_SURVIVAL = 0.64

MIN_CROSS_STRUCTURE_MEMORY_FRICTION = 0.12
MAX_CROSS_STRUCTURE_MEMORY_FRICTION = 0.36

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

        self.memory_links = {}

        self.dormant_memories = {}

        self.memory_instability = random.uniform(
            0.06,
            0.10
        )

        self.memory_friction = random.uniform(
            0.08,
            0.12
        )

        self.memory_decay = random.uniform(
            0.16,
            0.24
        )

        self.legacy_contamination = random.uniform(
            0.12,
            0.18
        )

        self.fragmentation_level = random.uniform(
            0.03,
            0.08
        )

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

    return nodes

# ==================================================
# memory ecology
# ==================================================

def update_memory_ecology(nodes):

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

        node.persistence_field *= 0.996

        node.persistence_field += (
            pressure_gap
            * 0.008
        )

        node.persistence_field += random.uniform(
            -INSTABILITY_NOISE,
            INSTABILITY_NOISE
        )

        node.persistence_field = clamp(
            node.persistence_field,
            0.03,
            0.76
        )

        # ==========================================
        # memory maintenance
        # ==========================================

        remove_memories = []

        for target_id in list(
            node.memory_links.keys()
        ):

            memory_strength = (
                node.memory_links[target_id]
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

            memory_strength *= MEMORY_DECAY

            memory_strength -= (
                signature_gap
                * 0.013
            )

            memory_strength -= (
                structure_gap
                * 0.006
            )

            if (
                random.random()
                < 0.38
            ):

                memory_strength += random.uniform(
                    -0.007,
                    0.016
                )

            if (
                random.random()
                < MEMORY_COLLAPSE_RATE
            ):

                memory_strength -= random.uniform(
                    0.05,
                    0.09
                )

                node.memory_instability += (
                    random.uniform(
                        0.004,
                        0.008
                    )
                )

            node.memory_links[
                target_id
            ] = memory_strength

            node.memory_decay += (
                signature_gap
                * 0.008
            )

            node.memory_friction += (
                structure_gap
                * 0.005
            )

            if (
                target.persistence_field
                >
                node.persistence_field
            ):

                node.legacy_contamination += (
                    0.0018
                )

            if memory_strength <= 0.040:

                remove_memories.append(
                    target_id
                )

        # ==========================================
        # dormant transition
        # ==========================================

        for target_id in remove_memories:

            if (
                len(node.dormant_memories)
                < 2
            ):

                residual = random.uniform(
                    0.012,
                    0.034
                )

                node.dormant_memories[
                    target_id
                ] = residual

            del node.memory_links[
                target_id
            ]

        # ==========================================
        # dormant memory
        # ==========================================

        remove_dormant = []

        for target_id in list(
            node.dormant_memories.keys()
        ):

            dormant_strength = (
                node.dormant_memories[
                    target_id
                ]
            )

            dormant_strength *= 0.972

            dormant_strength += random.uniform(
                -0.003,
                0.001
            )

            node.dormant_memories[
                target_id
            ] = dormant_strength

            if (
                dormant_strength > 0.019
                and
                random.random() < 0.040
            ):

                node.memory_links[
                    target_id
                ] = random.uniform(
                    0.08,
                    0.14
                )

                remove_dormant.append(
                    target_id
                )

            elif dormant_strength <= 0.008:

                remove_dormant.append(
                    target_id
                )

        for target_id in remove_dormant:

            if target_id in node.dormant_memories:

                del node.dormant_memories[
                    target_id
                ]

        # ==========================================
        # memory formation
        # ==========================================

        formation_bias = (
            MEMORY_FORMATION_RATE
            +
            (
                pressure_gap
                * 0.016
            )
        )

        if (
            len(node.memory_links)
            >= 5
        ):

            formation_bias *= 0.74

        if (
            len(node.memory_links)
            >= 7
        ):

            formation_bias *= 0.60

        if (
            node.legacy_contamination
            > 0.36
        ):

            formation_bias *= 0.84

        if (
            global_divergence > 0.72
        ):

            formation_bias *= 1.10

            node.region_signature += random.uniform(
                -0.006,
                0.006
            )

        if (
            random.random()
            < formation_bias
        ):

            candidates = []

            for other in nearby:

                if (
                    other.idx
                    in node.memory_links
                ):
                    continue

                signature_gap = abs(
                    other.region_signature
                    -
                    node.region_signature
                )

                persistence_gap = abs(
                    other.persistence_field
                    -
                    node.persistence_field
                )

                if (
                    signature_gap < 0.40
                    and
                    persistence_gap < 0.18
                ):

                    candidates.append(
                        other
                    )

            if candidates:

                target = random.choice(
                    candidates
                )

                node.memory_links[
                    target.idx
                ] = random.uniform(
                    0.10,
                    0.19
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

        node.memory_instability *= 0.997

        node.memory_instability += (
            node.fragmentation_level
            * 0.0017
        )

        node.memory_instability = clamp(
            node.memory_instability,
            0.03,
            MAX_ALIGNMENT
        )

        # ==========================================
        # memory decay
        # ==========================================

        node.memory_decay *= 0.996

        node.memory_decay += (
            pressure_gap
            * 0.0028
        )

        node.memory_decay = clamp(
            node.memory_decay,
            0.10,
            0.58
        )

        # ==========================================
        # contamination
        # ==========================================

        node.legacy_contamination *= 0.995

        node.legacy_contamination += (
            len(node.memory_links)
            * 0.00042
        )

        node.legacy_contamination += (
            len(node.dormant_memories)
            * 0.00018
        )

        node.legacy_contamination = clamp(
            node.legacy_contamination,
            0.04,
            0.54
        )

        # ==========================================
        # friction
        # ==========================================

        node.memory_friction *= 0.995

        node.memory_friction += (
            node.fragmentation_level
            * 0.0011
        )

        node.memory_friction = clamp(
            node.memory_friction,
            0.06,
            0.36
        )

        # ==========================================
        # divergence
        # ==========================================

        global_offset = abs(
            node.region_signature
            -
            global_mean
        )

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
                    0.022
                )
            )

        elif global_divergence < 0.30:

            if global_offset < 0.10:

                node.region_signature += (
                    random.uniform(
                        -0.018,
                        0.018
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
                        len(node.memory_links)
                    )
                    * 0.00006
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
            < rewire_rate * 1.04
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

                    candidates.append(other)

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

    localized_memory_persistence = (
        sum(
            len(n.memory_links)
            for n in nodes
        )
        /
        (
            NUM_NODES * 3.0
        )
    )

    memory_decay_balance = (
        sum(
            n.memory_decay
            for n in nodes
        )
        / NUM_NODES
    )

    legacy_contamination_pressure = (
        sum(
            n.legacy_contamination
            for n in nodes
        )
        / NUM_NODES
    )

    fragmented_memory_instability = (
        sum(
            n.memory_instability
            for n in nodes
        )
        / NUM_NODES
    )

    dormant_memory_survival = (
        sum(
            len(n.dormant_memories)
            for n in nodes
        )
        /
        (
            NUM_NODES * 2.0
        )
    )

    cross_structure_memory_friction = (
        sum(
            n.memory_friction
            for n in nodes
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

        "localized_memory_persistence":
            round(
                localized_memory_persistence,
                4
            ),

        "memory_decay_balance":
            round(
                memory_decay_balance,
                4
            ),

        "legacy_contamination_pressure":
            round(
                legacy_contamination_pressure,
                4
            ),

        "fragmented_memory_instability":
            round(
                fragmented_memory_instability,
                4
            ),

        "dormant_memory_survival":
            round(
                dormant_memory_survival,
                4
            ),

        "cross_structure_memory_friction":
            round(
                cross_structure_memory_friction,
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

    return all([

        MIN_LOCALIZED_MEMORY_PERSISTENCE
        <= metrics[
            "localized_memory_persistence"
        ]
        <= MAX_LOCALIZED_MEMORY_PERSISTENCE,

        MIN_MEMORY_DECAY_BALANCE
        <= metrics[
            "memory_decay_balance"
        ]
        <= MAX_MEMORY_DECAY_BALANCE,

        MIN_LEGACY_CONTAMINATION_PRESSURE
        <= metrics[
            "legacy_contamination_pressure"
        ]
        <= MAX_LEGACY_CONTAMINATION_PRESSURE,

        MIN_FRAGMENTED_MEMORY_INSTABILITY
        <= metrics[
            "fragmented_memory_instability"
        ]
        <= MAX_FRAGMENTED_MEMORY_INSTABILITY,

        MIN_DORMANT_MEMORY_SURVIVAL
        <= metrics[
            "dormant_memory_survival"
        ]
        <= MAX_DORMANT_MEMORY_SURVIVAL,

        MIN_CROSS_STRUCTURE_MEMORY_FRICTION
        <= metrics[
            "cross_structure_memory_friction"
        ]
        <= MAX_CROSS_STRUCTURE_MEMORY_FRICTION,

        MIN_DIVERGENCE
        <= metrics[
            "bounded_divergence"
        ]
        <= MAX_DIVERGENCE,
    ])

# ==================================================
# run
# ==================================================

def run(seed):

    random.seed(seed)

    nodes = initialize_network()

    for _ in range(NUM_STEPS):

        update_memory_ecology(nodes)

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
