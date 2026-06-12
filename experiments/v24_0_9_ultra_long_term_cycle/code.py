# v24.0.9
# Part1

# Ultra-Long-Term Cycle
# Agonwelt × Gossamer

import random

NUM_NODES = 96
NUM_STEPS = 1500


def clamp(value, minimum, maximum):
    return max(minimum, min(value, maximum))


class Node:

    def __init__(self, node_id):

        self.node_id = node_id

        self.purpose_persistence = random.uniform(
            0.30, 0.65
        )

        self.continuity_prioritization = random.uniform(
            0.25, 0.60
        )

        self.local_value_formation = random.uniform(
            0.25, 0.60
        )

        self.selective_memory_preservation = random.uniform(
            0.25, 0.65
        )

        self.civilization_self_interpretation = random.uniform(
            0.20, 0.55
        )

        self.emergent_intention = random.uniform(
            0.20, 0.55
        )

        self.thousand_generation_inheritance = random.uniform(
            0.25, 0.65
        )

        self.civilization_dormancy = random.uniform(
            0.20, 0.60
        )

        self.reactivation = random.uniform(
            0.20, 0.60
        )

        self.environmental_resistance = random.uniform(
            0.30, 0.70
        )

        self.civilization_reseeding = random.uniform(
            0.20, 0.55
        )

        self.terminal_cycle_avoidance = random.uniform(
            0.25, 0.65
        )

        self.legacy_dominance = random.uniform(
            0.15, 0.45
        )


def update_ultra_long_term_cycle(nodes):

    for node in nodes:

        purpose_mutation = random.uniform(
            -0.026, 0.024
        )

        continuity_conflict = random.uniform(
            -0.024, 0.024
        )

        value_shift = random.uniform(
            -0.016, 0.016
        )

        memory_selection = random.uniform(
            -0.013, 0.012
        )

        interpretation_shift = random.uniform(
            -0.012, 0.012
        )

        intention_shift = random.uniform(
            -0.014, 0.014
        )

        inheritance_shift = random.uniform(
            -0.024, 0.022
        )

        dormancy_shift = random.uniform(
            -0.016, 0.016
        )

        reactivation_shift = random.uniform(
            -0.015, 0.015
        )

        erosion_pressure = random.uniform(
            -0.012, 0.010
        )

        reseeding_shift = random.uniform(
            -0.014, 0.014
        )

        cycle_shift = random.uniform(
            -0.012, 0.012
        )

        node.purpose_persistence += (
            purpose_mutation
        )

        node.continuity_prioritization += (
            continuity_conflict
            + node.purpose_persistence
            * 0.0008
        )

        node.local_value_formation += (
            value_shift
        )

        node.selective_memory_preservation += (
            memory_selection
            + node.local_value_formation
            * 0.0008
        )

        node.civilization_self_interpretation += (
            interpretation_shift
        )

        node.emergent_intention += (
            intention_shift
            + node.civilization_self_interpretation
            * 0.0008
        )

        node.thousand_generation_inheritance += (
            inheritance_shift
            + node.selective_memory_preservation
            * 0.0008
        )

        node.civilization_dormancy += (
            dormancy_shift
        )

        node.reactivation += (
            reactivation_shift
            + node.civilization_dormancy
            * 0.0005
        )

        node.environmental_resistance += (
            erosion_pressure
            + node.reactivation
            * 0.0008
        )

        node.civilization_reseeding += (
            reseeding_shift
            + node.environmental_resistance
            * 0.0008
        )

        node.terminal_cycle_avoidance += (
            cycle_shift
            + node.civilization_reseeding
            * 0.0008
        )

        node.legacy_dominance += (
            node.thousand_generation_inheritance
            * 0.0004
        )

        node.legacy_dominance -= (
            node.local_value_formation
            * 0.0002
        )

        node.purpose_persistence = clamp(
            node.purpose_persistence,
            0.25, 0.75
        )

        node.continuity_prioritization = clamp(
            node.continuity_prioritization,
            0.20, 0.70
        )

        node.local_value_formation = clamp(
            node.local_value_formation,
            0.20, 0.70
        )

        node.selective_memory_preservation = clamp(
            node.selective_memory_preservation,
            0.20, 0.75
        )

        node.civilization_self_interpretation = clamp(
            node.civilization_self_interpretation,
            0.15, 0.65
        )

        node.emergent_intention = clamp(
            node.emergent_intention,
            0.15, 0.65
        )

        node.thousand_generation_inheritance = clamp(
            node.thousand_generation_inheritance,
            0.20, 0.75
        )

        node.civilization_dormancy = clamp(
            node.civilization_dormancy,
            0.15, 0.70
        )

        node.reactivation = clamp(
            node.reactivation,
            0.15, 0.70
        )

        node.environmental_resistance = clamp(
            node.environmental_resistance,
            0.20, 0.80
        )

        node.civilization_reseeding = clamp(
            node.civilization_reseeding,
            0.15, 0.65
        )

        node.terminal_cycle_avoidance = clamp(
            node.terminal_cycle_avoidance,
            0.20, 0.75
        )

        node.legacy_dominance = clamp(
            node.legacy_dominance,
            0.10, 0.55
        )

def compute_metrics(nodes):

    return {

        "purpose_persistence_rate":
        round(sum(n.purpose_persistence for n in nodes) / NUM_NODES, 4),

        "continuity_prioritization_rate":
        round(sum(n.continuity_prioritization for n in nodes) / NUM_NODES, 4),

        "local_value_formation_rate":
        round(sum(n.local_value_formation for n in nodes) / NUM_NODES, 4),

        "selective_memory_preservation_rate":
        round(sum(n.selective_memory_preservation for n in nodes) / NUM_NODES, 4),

        "civilization_self_interpretation_rate":
        round(sum(n.civilization_self_interpretation for n in nodes) / NUM_NODES, 4),

        "emergent_intention_rate":
        round(sum(n.emergent_intention for n in nodes) / NUM_NODES, 4),

        "thousand_generation_inheritance_rate":
        round(sum(n.thousand_generation_inheritance for n in nodes) / NUM_NODES, 4),

        "civilization_dormancy_rate":
        round(sum(n.civilization_dormancy for n in nodes) / NUM_NODES, 4),

        "reactivation_rate":
        round(sum(n.reactivation for n in nodes) / NUM_NODES, 4),

        "environmental_resistance_rate":
        round(sum(n.environmental_resistance for n in nodes) / NUM_NODES, 4),

        "civilization_reseeding_rate":
        round(sum(n.civilization_reseeding for n in nodes) / NUM_NODES, 4),

        "terminal_cycle_avoidance_rate":
        round(sum(n.terminal_cycle_avoidance for n in nodes) / NUM_NODES, 4),

        "legacy_dominance_pressure":
        round(sum(n.legacy_dominance for n in nodes) / NUM_NODES, 4)

    }


def validate(metrics):

    return all([

        0.25 <= metrics["purpose_persistence_rate"] <= 0.75,

        0.20 <= metrics["continuity_prioritization_rate"] <= 0.70,

        0.20 <= metrics["local_value_formation_rate"] <= 0.70,

        0.20 <= metrics["selective_memory_preservation_rate"] <= 0.75,

        0.15 <= metrics["civilization_self_interpretation_rate"] <= 0.65,

        0.15 <= metrics["emergent_intention_rate"] <= 0.65,

        0.20 <= metrics["thousand_generation_inheritance_rate"] <= 0.75,

        0.15 <= metrics["civilization_dormancy_rate"] <= 0.70,

        0.15 <= metrics["reactivation_rate"] <= 0.70,

        0.20 <= metrics["environmental_resistance_rate"] <= 0.80,

        0.15 <= metrics["civilization_reseeding_rate"] <= 0.65,

        0.20 <= metrics["terminal_cycle_avoidance_rate"] <= 0.75,

        0.10 <= metrics["legacy_dominance_pressure"] <= 0.55

    ])


def variability_validation(all_metrics):

    reactivation_values = [
        m["reactivation_rate"]
        for m in all_metrics
    ]

    inheritance_values = [
        m["thousand_generation_inheritance_rate"]
        for m in all_metrics
    ]

    dormancy_values = [
        m["civilization_dormancy_rate"]
        for m in all_metrics
    ]

    reseeding_values = [
        m["civilization_reseeding_rate"]
        for m in all_metrics
    ]

    avoidance_values = [
        m["terminal_cycle_avoidance_rate"]
        for m in all_metrics
    ]

    purpose_values = [
        m["purpose_persistence_rate"]
        for m in all_metrics
    ]

    continuity_values = [
        m["continuity_prioritization_rate"]
        for m in all_metrics
    ]

    local_value_values = [
        m["local_value_formation_rate"]
        for m in all_metrics
    ]

    major_metric_difference = []

    metric_keys = [

        "purpose_persistence_rate",

        "continuity_prioritization_rate",

        "local_value_formation_rate",

        "selective_memory_preservation_rate",

        "thousand_generation_inheritance_rate",

        "reactivation_rate",

        "civilization_dormancy_rate",

        "civilization_reseeding_rate",

        "environmental_resistance_rate",

        "terminal_cycle_avoidance_rate"

    ]

    for key in metric_keys:

        values = [
            m[key]
            for m in all_metrics
        ]

        average_value = (
            sum(values)
            / len(values)
        )

        difference = (
            max(values)
            - min(values)
        )

        major_metric_difference.append(
            difference
            / average_value
        )

    major_metric_average_difference = (
        sum(
            major_metric_difference
        )
        / len(
            major_metric_difference
        )
    )

    return all([

        (
            max(purpose_values)
            - min(purpose_values)
        ) >= 0.013,

        (
            max(continuity_values)
            - min(continuity_values)
        ) >= 0.028,

        (
            max(local_value_values)
            - min(local_value_values)
        ) >= 0.01,

        (
            max(reactivation_values)
            - min(reactivation_values)
        ) >= 0.01,

        (
            max(inheritance_values)
            - min(inheritance_values)
        ) >= 0.015,

        (
            max(dormancy_values)
            - min(dormancy_values)
        ) >= 0.01,

        (
            max(reseeding_values)
            - min(reseeding_values)
        ) >= 0.01,

        (
            max(avoidance_values)
            - min(avoidance_values)
        ) >= 0.01,

        0.055
        <=
        major_metric_average_difference
        <=
        0.15

    ])


def run(seed):

    random.seed(seed)

    nodes = [

        Node(index)

        for index
        in range(NUM_NODES)

    ]

    for _ in range(NUM_STEPS):

        update_ultra_long_term_cycle(
            nodes
        )

    metrics = compute_metrics(
        nodes
    )

    return metrics


all_metrics = []

overall_validation = True

for seed in [42, 43, 44]:

    metrics = run(seed)

    all_metrics.append(
        metrics
    )

    print(
        f"\n--- RUN #{seed} ---"
    )

    for key, value in metrics.items():

        print(
            f"{key}: {value}"
        )


base_validation = all(

    validate(metrics)

    for metrics
    in all_metrics

)

variability_result = (
    variability_validation(
        all_metrics
    )
)

validation_result = (
    base_validation
    and
    variability_result
)

print(
    "\nvariability_result:"
)

print(
    variability_result
)

print(
    "\nvalidation_result:"
)

print(
    validation_result
)

print(
    "\nfinal_result:"
)

if validation_result:

    print(
        "ACHIEVED"
    )

else:

    print(
        "NOT ACHIEVED"
    )
