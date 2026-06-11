# v23.0.7
# Self-Sustaining Sphere
# Agonwelt × Gossamer

import random

NUM_NODES = 84
NUM_STEPS = 1200


def clamp(value, minimum, maximum):
    return max(minimum, min(value, maximum))


class Node:

    def __init__(self, node_id):

        self.node_id = node_id

        self.role_differentiation = random.uniform(
            0.30, 0.60
        )

        self.collective_intention = random.uniform(
            0.20, 0.45
        )

        self.adaptive_evolution = random.uniform(
            0.25, 0.55
        )

        self.generational_replacement = random.uniform(
            0.20, 0.50
        )

        self.self_repair = random.uniform(
            0.25, 0.60
        )

        self.civilization_homeostasis = random.uniform(
            0.35, 0.65
        )

        self.remote_memory_connection = random.uniform(
            0.15, 0.35
        )

        self.civilization_divergence = random.uniform(
            0.25, 0.60
        )

        self.knowledge_propagation = random.uniform(
            0.20, 0.50
        )

        self.disconnection_resistance = random.uniform(
            0.25, 0.55
        )

        self.self_compression = random.uniform(
            0.40, 0.75
        )

        self.partial_synchronization = random.uniform(
            0.15, 0.40
        )

        self.legacy_dominance = random.uniform(
            0.20, 0.45
        )


def update_self_sustaining_sphere(nodes):

    for node in nodes:

        role_shift = random.uniform(
            -0.008, 0.008
        )

        intention_conflict = random.uniform(
            -0.007, 0.007
        )

        adaptation_shift = random.uniform(
            -0.008, 0.006
        )

        generation_shift = random.uniform(
            -0.008, 0.005
        )

        repair_shift = random.uniform(
            -0.008, 0.006
        )

        homeostasis_shift = random.uniform(
            -0.009, 0.006
        )

        remote_shift = random.uniform(
            -0.005, 0.005
        )

        divergence_shift = random.uniform(
            -0.008, 0.008
        )

        propagation_shift = random.uniform(
            -0.006, 0.005
        )

        resistance_shift = random.uniform(
            -0.008, 0.005
        )

        compression_shift = random.uniform(
            -0.007, 0.004
        )

        synchronization_shift = random.uniform(
            -0.005, 0.005
        )

        node.role_differentiation += role_shift

        node.collective_intention += intention_conflict

        node.adaptive_evolution += (
            adaptation_shift
            + node.collective_intention
            * 0.0012
        )

        node.generational_replacement += (
            generation_shift
            + node.adaptive_evolution
            * 0.0012
        )

        node.self_repair += (
            repair_shift
            + node.generational_replacement
            * 0.0012
        )

        node.civilization_homeostasis += (
            homeostasis_shift
            + node.self_repair
            * 0.0012
        )

        node.remote_memory_connection += (
            remote_shift
        )

        node.civilization_divergence += (
            divergence_shift
        )

        node.knowledge_propagation += (
            propagation_shift
            + node.remote_memory_connection
            * 0.001
        )

        node.disconnection_resistance += (
            resistance_shift
            + node.knowledge_propagation
            * 0.0012
        )

        node.self_compression += (
            compression_shift
        )

        node.partial_synchronization += (
            synchronization_shift
            + node.remote_memory_connection
            * 0.0005
        )

        node.legacy_dominance += (
            node.generational_replacement
            * 0.0005
        )

        node.legacy_dominance -= (
            node.civilization_divergence
            * 0.0003
        )

        node.role_differentiation = clamp(
            node.role_differentiation,
            0.25, 0.70
        )

        node.collective_intention = clamp(
            node.collective_intention,
            0.15, 0.55
        )

        node.adaptive_evolution = clamp(
            node.adaptive_evolution,
            0.20, 0.62
        )

        node.generational_replacement = clamp(
            node.generational_replacement,
            0.15, 0.58
        )

        node.self_repair = clamp(
            node.self_repair,
            0.20, 0.68
        )

        node.civilization_homeostasis = clamp(
            node.civilization_homeostasis,
            0.25, 0.72
        )

        node.remote_memory_connection = clamp(
            node.remote_memory_connection,
            0.10, 0.45
        )

        node.civilization_divergence = clamp(
            node.civilization_divergence,
            0.20, 0.70
        )

        node.knowledge_propagation = clamp(
            node.knowledge_propagation,
            0.15, 0.60
        )

        node.disconnection_resistance = clamp(
            node.disconnection_resistance,
            0.20, 0.62
        )

        node.self_compression = clamp(
            node.self_compression,
            0.30, 0.82
        )

        node.partial_synchronization = clamp(
            node.partial_synchronization,
            0.10, 0.50
        )

        node.legacy_dominance = clamp(
            node.legacy_dominance,
            0.15, 0.55
        )


def compute_metrics(nodes):

    return {

        "role_differentiation_rate":
        round(sum(n.role_differentiation for n in nodes) / NUM_NODES, 4),

        "collective_intention_rate":
        round(sum(n.collective_intention for n in nodes) / NUM_NODES, 4),

        "adaptive_evolution_rate":
        round(sum(n.adaptive_evolution for n in nodes) / NUM_NODES, 4),

        "generational_replacement_rate":
        round(sum(n.generational_replacement for n in nodes) / NUM_NODES, 4),

        "self_repair_rate":
        round(sum(n.self_repair for n in nodes) / NUM_NODES, 4),

        "civilization_homeostasis_rate":
        round(sum(n.civilization_homeostasis for n in nodes) / NUM_NODES, 4),

        "remote_memory_connection_rate":
        round(sum(n.remote_memory_connection for n in nodes) / NUM_NODES, 4),

        "civilization_divergence_rate":
        round(sum(n.civilization_divergence for n in nodes) / NUM_NODES, 4),

        "knowledge_propagation_rate":
        round(sum(n.knowledge_propagation for n in nodes) / NUM_NODES, 4),

        "disconnection_resistance_rate":
        round(sum(n.disconnection_resistance for n in nodes) / NUM_NODES, 4),

        "self_compression_rate":
        round(sum(n.self_compression for n in nodes) / NUM_NODES, 4),

        "partial_synchronization_rate":
        round(sum(n.partial_synchronization for n in nodes) / NUM_NODES, 4),

        "legacy_dominance_pressure":
        round(sum(n.legacy_dominance for n in nodes) / NUM_NODES, 4)
    }


def validate(metrics):

    return all([

        0.25 <= metrics["role_differentiation_rate"] <= 0.70,
        0.15 <= metrics["collective_intention_rate"] <= 0.55,

        0.21 <= metrics["adaptive_evolution_rate"] < 0.60,

        0.15 <= metrics["generational_replacement_rate"] < 0.58,

        0.20 <= metrics["self_repair_rate"] < 0.65,

        0.25 <= metrics["civilization_homeostasis_rate"] < 0.68,

        0.10 <= metrics["remote_memory_connection_rate"] <= 0.45,

        0.20 <= metrics["civilization_divergence_rate"] <= 0.70,

        0.15 <= metrics["knowledge_propagation_rate"] <= 0.60,

        0.20 <= metrics["disconnection_resistance_rate"] < 0.60,

        0.30 <= metrics["self_compression_rate"] < 0.80,

        0.10 <= metrics["partial_synchronization_rate"] <= 0.50,

        0.15 <= metrics["legacy_dominance_pressure"] <= 0.55

    ])


def run(seed):

    random.seed(seed)

    nodes = [
        Node(index)
        for index in range(NUM_NODES)
    ]

    for _ in range(NUM_STEPS):
        update_self_sustaining_sphere(
            nodes
        )

    metrics = compute_metrics(
        nodes
    )

    return metrics, validate(metrics)


overall_validation = True

for seed in [42, 43, 44]:

    metrics, validation_result = run(
        seed
    )

    print(
        f"\n--- RUN #{seed} ---"
    )

    for key, value in metrics.items():

        print(
            f"{key}: {value}"
        )

    print(
        f"validation_result: "
        f"{validation_result}"
    )

    if not validation_result:
        overall_validation = False


print("\nfinal_result:")

if overall_validation:
    print("ACHIEVED")
else:
    print("NOT ACHIEVED")
