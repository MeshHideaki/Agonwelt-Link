# Agonwelt-Link v20.3.1
# stabilized fragmented routing memory
# strict validation mode

import random
import math

# ==================================================
# configuration
# ==================================================

NUM_NODES = 72
NUM_STEPS = 680

LOCAL_RADIUS = 0.24

BASE_REWIRE_RATE = 0.044
BASE_COLLAPSE_THRESHOLD = 0.30

MAX_CONNECTIONS = 8
MIN_CONNECTIONS = 2

MAX_BRIDGES = 3
MAX_DYNAMIC_PATHS = 4

DAMPING = 0.95

# bridge ecology
BRIDGE_FORMATION_RATE = 0.034
BRIDGE_DECAY_RATE = 0.988
BRIDGE_COLLAPSE_RATE = 0.036

# dynamic routing
ROUTING_FORMATION_RATE = 0.046
ROUTING_DECAY = 0.986
ROUTING_COLLAPSE_RATE = 0.040

# fragmented persistence
PERSISTENCE_DECAY = 0.992
LOCAL_RECOVERY_SCALE = 0.016

# instability ecology
INSTABILITY_NOISE = 0.005

# routing limits
MAX_ROUTE_ALIGNMENT = 0.32

# bounded diversity
MIN_DIVERGENCE = 0.14
MAX_DIVERGENCE = 0.78

# validation thresholds
MIN_DYNAMIC_ROUTING_FREQUENCY = 0.12
MIN_ROUTING_COLLAPSE_FLUCTUATION = 0.12
MIN_PATHWAY_INSTABILITY = 0.08
MIN_ROUTING_FRICTION = 0.08
MIN_LOCALIZED_REROUTING = 0.10
MIN_FRAGMENTED_PROPAGATION = 0.08
MIN_DISTRIBUTED_PERSISTENCE = 0.12
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

        self.bridge_links = {}

        self.dynamic_routes = {}

        self.local_pressure = random.uniform(
            0.40,
            0.60
        )

        self.local_stability = random.uniform(
            0.42,
            0.66
        )

        self.region_signature = random.uniform(
            0.20,
            0.80
        )

        self.structure_type = random.randint(
            0,
            3
        )

        self.persistence_field = random.uniform(
            0.10,
            0.24
        )

        self.routing_resonance = random.uniform(
            0.03,
            0.06
        )

        self.fragmentation_level = random.uniform(
            0.02,
            0.08
        )

        self.routing_friction = random.uniform(
            0.01,
            0.03
        )

        # stabilized fragmented memory
        self.propagation_fragmentation = random.uniform(
            0.05,
            0.10
        )

        self.persistence_score = 1.0

        self.route_events = 0
        self.route_collapses = 0
        self.rerouting_events = 0

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

            node.connections.add(
                other.idx
            )

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

        local_persistence = (
            sum(
                other.persistence_field
                for other in nearby
            ) / len(nearby)
        )

        pressure_gap = abs(
            node.local_pressure
            - node.local_stability
        )

        # ==================================================
        # persistence
        # ==================================================

        node.persistence_field *= (
            PERSISTENCE_DECAY
        )

        node.persistence_field += (
            pressure_gap * 0.012
        )

        node.persistence_field += (
            (
                1.0
                - node.fragmentation_level
            )
            * LOCAL_RECOVERY_SCALE
            * 0.20
        )

        node.persistence_field += random.uniform(
            -INSTABILITY_NOISE,
            INSTABILITY_NOISE
        )

        node.persistence_field = clamp(
            node.persistence_field,
            0.02,
            0.82
        )

        # ==================================================
        # bridge maintenance
        # ==================================================

        remove_bridges = []

        for target_id in list(
            node.bridge_links.keys()
        ):

            strength = (
                node.bridge_links[target_id]
            )

            strength *= BRIDGE_DECAY_RATE

            strength -= random.uniform(
                0.002,
                0.010
            )

            target = nodes[target_id]

            structure_gap = abs(
                node.structure_type
                - target.structure_type
            )

            friction = (
                structure_gap * 0.034
            )

            strength -= friction

            node.routing_friction += (
                friction * 0.22
            )

            if (
                random.random()
                < BRIDGE_COLLAPSE_RATE
            ):

                strength -= random.uniform(
                    0.06,
                    0.18
                )

            node.bridge_links[
                target_id
            ] = strength

            if strength <= 0.02:

                remove_bridges.append(
                    target_id
                )

        for target_id in remove_bridges:

            del node.bridge_links[target_id]

        # ==================================================
        # fragmented bridge formation
        # ==================================================

        formation_bias = (
            BRIDGE_FORMATION_RATE
            +
            (
                node.fragmentation_level
                * 0.010
            )
        )

        if (
            random.random()
            < formation_bias
            and len(node.bridge_links)
            < MAX_BRIDGES
        ):

            candidates = []

            for other in nodes:

                if other.idx == node.idx:
                    continue

                if (
                    other.idx
                    in node.bridge_links
                ):
                    continue

                if (
                    other.idx
                    in node.connections
                ):
                    continue

                d = distance(node, other)

                structure_gap = abs(
                    node.structure_type
                    - other.structure_type
                )

                if (
                    d > LOCAL_RADIUS * 1.50
                    and structure_gap >= 1
                    and structure_gap <= 2
                ):

                    candidates.append(
                        other
                    )

            if candidates:

                target = random.choice(
                    candidates
                )

                node.bridge_links[
                    target.idx
                ] = random.uniform(
                    0.10,
                    0.22
                )

        # ==================================================
        # dynamic routing decay
        # ==================================================

        remove_routes = []

        for target_id in list(
            node.dynamic_routes.keys()
        ):

            route_strength = (
                node.dynamic_routes[target_id]
            )

            route_strength *= (
                ROUTING_DECAY
            )

            route_strength -= random.uniform(
                0.003,
                0.014
            )

            target = nodes[target_id]

            structure_gap = abs(
                node.structure_type
                - target.structure_type
            )

            route_strength -= (
                structure_gap * 0.020
            )

            node.routing_friction += (
                structure_gap * 0.012
            )

            # strengthened fragmented propagation
            propagation_gain = (
                abs(
                    node.region_signature
                    - target.region_signature
                )
                * 0.055
            )

            propagation_gain += (
                structure_gap * 0.012
            )

            node.propagation_fragmentation += (
                propagation_gain
            )

            if (
                random.random()
                < ROUTING_COLLAPSE_RATE
            ):

                route_strength -= random.uniform(
                    0.08,
                    0.22
                )

                # collapse propagation memory
                node.propagation_fragmentation += (
                    random.uniform(
                        0.010,
                        0.026
                    )
                )

            node.dynamic_routes[
                target_id
            ] = route_strength

            if route_strength <= 0.02:

                remove_routes.append(
                    target_id
                )

        for target_id in remove_routes:

            del node.dynamic_routes[target_id]

            node.route_collapses += 1

            node.rerouting_events += (
                random.uniform(
                    0.02,
                    0.08
                )
            )

            # rerouting residue
            node.propagation_fragmentation += (
                random.uniform(
                    0.008,
                    0.020
                )
            )

        # ==================================================
        # dynamic fragmented routing
        # ==================================================

        route_bias = (
            ROUTING_FORMATION_RATE
            +
            (
                pressure_gap * 0.020
            )
        )

        if (
            len(node.dynamic_routes)
            >= 2
        ):

            route_bias *= 0.55

        if (
            node.routing_resonance
            > 0.28
        ):

            route_bias *= 0.45

        if (
            random.random()
            < route_bias
            and len(node.dynamic_routes)
            < MAX_DYNAMIC_PATHS
        ):

            route_candidates = []

            for bridge_id in node.bridge_links:

                target = nodes[bridge_id]

                signature_gap = abs(
                    target.region_signature
                    - node.region_signature
                )

                persistence_gap = abs(
                    target.persistence_field
                    - node.persistence_field
                )

                if (
                    signature_gap < 0.42
                    and persistence_gap < 0.26
                ):

                    route_candidates.append(
                        target
                    )

            if route_candidates:

                target = random.choice(
                    route_candidates
                )

                node.dynamic_routes[
                    target.idx
                ] = random.uniform(
                    0.12,
                    0.24
                )

                node.route_events += 1

        # ==================================================
        # unstable routing propagation
        # ==================================================

        if node.dynamic_routes:

            route_values = []

            incompatibility = []

            for target_id in node.dynamic_routes:

                target = nodes[target_id]

                route_values.append(
                    target.persistence_field
                )

                incompatibility.append(
                    abs(
                        target.structure_type
                        - node.structure_type
                    )
                )

            route_mean = (
                sum(route_values)
                / len(route_values)
            )

            incompatibility_mean = (
                sum(incompatibility)
                / len(incompatibility)
            )

            route_gap = abs(
                route_mean
                - node.persistence_field
            )

            node.routing_resonance *= (
                0.991
            )

            node.routing_resonance += (
                (
                    1.0
                    - route_gap
                ) * 0.018
            )

            node.routing_resonance -= (
                incompatibility_mean
                * 0.002
            )

            node.routing_resonance += (
                random.uniform(
                    -0.004,
                    0.004
                )
            )

            propagation_strength = (
                0.0048
                -
                (
                    incompatibility_mean
                    * 0.0010
                )
            )

            propagation_strength = max(
                0.0010,
                propagation_strength
            )

            node.persistence_field += (
                (
                    route_mean
                    - node.persistence_field
                )
                * propagation_strength
            )

            if (
                route_gap
                < 0.06
            ):

                node.persistence_field += (
                    random.uniform(
                        -0.030,
                        0.030
                    )
                )

                node.routing_resonance *= (
                    0.996
                )

                # fragmented instability memory
                node.propagation_fragmentation += (
                    random.uniform(
                        0.006,
                        0.016
                    )
                )

            node.routing_resonance = clamp(
                node.routing_resonance,
                0.0,
                MAX_ROUTE_ALIGNMENT
            )

        else:

            node.routing_resonance *= (
                0.986
            )

            # isolated route residue
            node.propagation_fragmentation += (
                random.uniform(
                    0.001,
                    0.004
                )
            )

        # ==================================================
        # decay
        # ==================================================

        node.routing_friction *= 0.994

        # reduced decay
        node.propagation_fragmentation *= (
            0.9992
        )

        node.fragmentation_level *= 0.992

        node.fragmentation_level += (
            random.uniform(
                -0.004,
                0.004
            )
        )

        node.fragmentation_level += (
            pressure_gap * 0.006
        )

        node.fragmentation_level = clamp(
            node.fragmentation_level,
            0.01,
            0.48
        )

        node.propagation_fragmentation = clamp(
            node.propagation_fragmentation,
            0.02,
            0.30
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
                node.persistence_field
                - local_persistence
            ) * 0.010
        )

        node.region_signature += (
            (
                node.fragmentation_level
                - 0.18
            ) * 0.006
        )

        node.region_signature += (
            local_signature
            - node.region_signature
        ) * 0.0007

        # ==================================================
        # bounded divergence
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
                    0.050
                )
            )

        elif global_divergence < 0.24:

            if global_offset < 0.10:

                node.region_signature += (
                    random.uniform(
                        -0.052,
                        0.052
                    )
                )

            else:

                node.region_signature += (
                    random.uniform(
                        -0.022,
                        0.022
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
                0.0013
                +
                node.routing_resonance
                * 0.0005
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
                -0.0028,
                0.0028
            )

            node.vy += random.uniform(
                -0.0028,
                0.0028
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

        route_factor = (
            node.routing_resonance
            * 0.012
        )

        rewire_rate = (
            BASE_REWIRE_RATE
            + instability * 0.022
            + route_factor
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

                persistence_gap = abs(
                    target.persistence_field
                    - node.persistence_field
                )

                if (
                    signature_gap > 0.46
                    and persistence_gap > 0.16
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
                rewire_rate * 1.24
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

                persistence_gap = abs(
                    other.persistence_field
                    - node.persistence_field
                )

                if (
                    signature_gap < 0.54
                    and persistence_gap < 0.22
                ):

                    compatible.append(
                        (
                            persistence_gap,
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
            + node.persistence_field
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

                node.persistence_score *= (
                    0.997
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

                persistence_gap = abs(
                    other.persistence_field
                    - node.persistence_field
                )

                if (
                    signature_gap < 0.54
                    and persistence_gap < 0.24
                ):

                    compatible.append(
                        other
                    )

            compatible = sorted(
                compatible,
                key=lambda n:
                    abs(
                        n.persistence_field
                        - node.persistence_field
                    )
            )

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

        node.persistence_score = clamp(
            node.persistence_score,
            0.72,
            1.60
        )

# ==================================================
# metrics
# ==================================================

def compute_metrics(nodes):

    dynamic_routing_frequency = (
        sum(
            n.route_events
            for n in nodes
        )
        / NUM_NODES
    )

    routing_collapse_fluctuation = (
        sum(
            n.route_collapses
            for n in nodes
        )
        / NUM_NODES
    )

    pathway_instability_persistence = (
        sum(
            n.fragmentation_level
            for n in nodes
        )
        / NUM_NODES
    )

    cross_structure_routing_friction = (
        sum(
            n.routing_friction
            for n in nodes
        )
        / NUM_NODES
    )

    localized_rerouting_cycles = (
        sum(
            n.rerouting_events
            for n in nodes
        )
        / NUM_NODES
    )

    fragmented_propagation_stability = (
        sum(
            n.propagation_fragmentation
            for n in nodes
        )
        / NUM_NODES
    )

    distributed_structural_persistence = (
        max(
            n.persistence_field
            for n in nodes
        )
        -
        min(
            n.persistence_field
            for n in nodes
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

        "dynamic_routing_frequency":
            round(
                dynamic_routing_frequency,
                4
            ),

        "routing_collapse_fluctuation":
            round(
                routing_collapse_fluctuation,
                4
            ),

        "pathway_instability_persistence":
            round(
                pathway_instability_persistence,
                4
            ),

        "cross_structure_routing_friction":
            round(
                cross_structure_routing_friction,
                4
            ),

        "localized_rerouting_cycles":
            round(
                localized_rerouting_cycles,
                4
            ),

        "fragmented_propagation_stability":
            round(
                fragmented_propagation_stability,
                4
            ),

        "distributed_structural_persistence":
            round(
                distributed_structural_persistence,
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

    routing_ok = (
        metrics[
            "fragmented_propagation_stability"
        ]
        < MAX_ROUTE_ALIGNMENT
    )

    return all([

        metrics[
            "dynamic_routing_frequency"
        ]
        >= MIN_DYNAMIC_ROUTING_FREQUENCY,

        metrics[
            "routing_collapse_fluctuation"
        ]
        >= MIN_ROUTING_COLLAPSE_FLUCTUATION,

        metrics[
            "pathway_instability_persistence"
        ]
        >= MIN_PATHWAY_INSTABILITY,

        metrics[
            "cross_structure_routing_friction"
        ]
        >= MIN_ROUTING_FRICTION,

        metrics[
            "localized_rerouting_cycles"
        ]
        >= MIN_LOCALIZED_REROUTING,

        metrics[
            "fragmented_propagation_stability"
        ]
        >= MIN_FRAGMENTED_PROPAGATION,

        metrics[
            "distributed_structural_persistence"
        ]
        >= MIN_DISTRIBUTED_PERSISTENCE,

        metrics[
            "structural_persistence"
        ]
        >= MIN_STRUCTURAL_PERSISTENCE,

        divergence_ok,

        routing_ok
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
