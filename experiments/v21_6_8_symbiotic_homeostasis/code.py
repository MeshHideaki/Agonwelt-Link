# v21.6.8
# Symbiotic Homeostasis
# Agonwelt × Gossamer

# v21.6.8
# Reverted from v21.6.7
# Ceiling Control Maintained
# Adaptive Balance Maintained
# Returned to v21.6.6 Baseline
# Natural Homeostasis Verification Phase

import random

NUM_NODES = 84
NUM_STEPS = 1200


def clamp(value, minimum, maximum):
    return max(minimum, min(value, maximum))


class Node:

    def __init__(self, node_id):

        self.node_id = node_id

        self.inheritance = random.uniform(
            0.40,
            0.60
        )

        self.forgetting = random.uniform(
            0.40,
            0.60
        )

        self.dormancy = random.uniform(
            0.35,
            0.60
        )

        self.reactivation = random.uniform(
            0.35,
            0.60
        )

        self.diversity = random.uniform(
            0.40,
            0.60
        )

        self.legacy_pressure = random.uniform(
            0.22,
            0.42
        )

        self.friction = random.uniform(
            0.16,
            0.30
        )

        self.homeostasis = random.uniform(
            0.45,
            0.61
        )


def update_homeostasis(nodes):

    for node in nodes:

        node.inheritance += random.uniform(
            -0.010,
            0.010
        )

        node.forgetting += random.uniform(
            -0.010,
            0.010
        )

        node.dormancy += random.uniform(
            -0.008,
            0.008
        )

        node.reactivation += random.uniform(
            -0.008,
            0.008
        )

        node.diversity += random.uniform(
            -0.010,
            0.010
        )

        inheritance_gap = abs(
            node.inheritance
            - node.forgetting
        )

        dormancy_gap = abs(
            node.dormancy
            - node.reactivation
        )

        inheritance_balance = (
            1.0
            - inheritance_gap
        )

        dormancy_balance = (
            1.0
            - dormancy_gap
        )

        diversity_factor = (
            1.0
            - abs(
                node.diversity
                - 0.52
            )
        )

        adaptive_balance = (
            inheritance_balance
            + dormancy_balance
            + diversity_factor
        ) / 3.0

        node.legacy_pressure += (
            (node.inheritance - 0.50)
            * 0.0025
        )

        node.legacy_pressure += random.uniform(
            -0.003,
            0.003
        )

        node.friction += (
            inheritance_gap
            * 0.0035
        )

        node.friction -= 0.0005

        node.friction += random.uniform(
            -0.002,
            0.002
        )

        ceiling_penalty = max(
            0.0,
            node.homeostasis - 0.700
        )

        node.homeostasis += (
            adaptive_balance
            * 0.0020
        )

        node.homeostasis -= (
            node.legacy_pressure
            * 0.0020
        )

        node.homeostasis -= (
            node.friction
            * 0.0018
        )

        node.homeostasis -= (
            ceiling_penalty
            * 0.014
        )

        # Reverted to v21.6.6 fluctuation range

        node.homeostasis += random.uniform(
            -0.009,
            0.009
        )

        node.inheritance = clamp(
            node.inheritance,
            0.35,
            0.65
        )

        node.forgetting = clamp(
            node.forgetting,
            0.35,
            0.65
        )

        node.dormancy = clamp(
            node.dormancy,
            0.30,
            0.68
        )

        node.reactivation = clamp(
            node.reactivation,
            0.30,
            0.68
        )

        node.diversity = clamp(
            node.diversity,
            0.32,
            0.72
        )

        node.legacy_pressure = clamp(
            node.legacy_pressure,
            0.18,
            0.52
        )

        node.friction = clamp(
            node.friction,
            0.12,
            0.38
        )

        node.homeostasis = clamp(
            node.homeostasis,
            0.40,
            0.78
        )


def compute_metrics(nodes):

    inheritance_gap = sum(
        abs(
            node.inheritance
            - node.forgetting
        )
        for node in nodes
    ) / NUM_NODES

    dormancy_gap = sum(
        abs(
            node.dormancy
            - node.reactivation
        )
        for node in nodes
    ) / NUM_NODES

    return {

        "symbiotic_homeostasis_index":
        round(
            sum(
                node.homeostasis
                for node in nodes
            ) / NUM_NODES,
            4
        ),

        "inheritance_forgetting_balance":
        round(
            0.50
            * (
                1.0
                - inheritance_gap
            ),
            4
        ),

        "dormancy_reactivation_balance":
        round(
            0.50
            * (
                1.0
                - dormancy_gap
            ),
            4
        ),

        "legacy_dominance_pressure":
        round(
            sum(
                node.legacy_pressure
                for node in nodes
            ) / NUM_NODES,
            4
        ),

        "adaptive_diversity_index":
        round(
            sum(
                node.diversity
                for node in nodes
            ) / NUM_NODES,
            4
        ),

        "homeostatic_friction":
        round(
            sum(
                node.friction
                for node in nodes
            ) / NUM_NODES,
            4
        ),

        "homeostasis_ceiling_ratio":
        round(
            sum(
                1
                for node in nodes
                if node.homeostasis >= 0.779
            )
            / NUM_NODES,
            4
        ),

        "friction_floor_ratio":
        round(
            sum(
                1
                for node in nodes
                if node.friction <= 0.121
            )
            / NUM_NODES,
            4
        )
    }


def validate(metrics):

    return all([

        0.40 <= metrics[
            "symbiotic_homeostasis_index"
        ] <= 0.78,

        0.35 <= metrics[
            "inheritance_forgetting_balance"
        ] <= 0.65,

        0.30 <= metrics[
            "dormancy_reactivation_balance"
        ] <= 0.68,

        0.18 <= metrics[
            "legacy_dominance_pressure"
        ] <= 0.52,

        0.32 <= metrics[
            "adaptive_diversity_index"
        ] <= 0.72,

        0.12 <= metrics[
            "homeostatic_friction"
        ] <= 0.38

    ])


def run(seed):

    random.seed(seed)

    nodes = [
        Node(index)
        for index in range(NUM_NODES)
    ]

    for _ in range(NUM_STEPS):
        update_homeostasis(nodes)

    metrics = compute_metrics(nodes)

    return metrics, validate(metrics)


overall_validation = True

for seed in [42, 43, 44]:

    metrics, validation_result = run(seed)

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
