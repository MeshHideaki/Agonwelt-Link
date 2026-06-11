# v22.0.10
# Inheritance Formation
# Agonwelt × Gossamer
import random
NUM_NODES = 84
NUM_STEPS = 1200
def clamp(value, minimum, maximum):
    return max(minimum, min(value, maximum))
class Node:
    def __init__(self, node_id):
        self.node_id = node_id
        self.fragment_memory = random.uniform(
            0.20, 0.45
        )
        self.memory_erosion = random.uniform(
            0.25, 0.55
        )
        self.knowledge_fusion = random.uniform(
            0.15, 0.35
        )
        self.lineage_inheritance = random.uniform(
            0.25, 0.50
        )
        self.cultural_compression = random.uniform(
            0.40, 0.75
        )
        self.civilization_resonance = random.uniform(
            0.15, 0.40
        )
        self.memory_circulation = random.uniform(
            0.30, 0.60
        )
        self.legacy_dominance = random.uniform(
            0.20, 0.45
        )
        self.memory_contamination = random.uniform(
            0.08, 0.20
        )
def update_inheritance_formation(nodes):
    for node in nodes:
        memory_loss = random.uniform(
            0.000, 0.010
        )
        recovery_attempt = random.uniform(
            0.0015, 0.0085
        )
        fusion_conflict = random.uniform(
            0.000, 0.006
        )
        lineage_decay = random.uniform(
            0.000, 0.003
        )
        compression_loss = random.uniform(
            0.000, 0.002
        )
        resonance_decay = random.uniform(
            0.000, 0.002
        )
        circulation_shift = random.uniform(
            -0.006, 0.006
        )
        contamination_shift = random.uniform(
            -0.003, 0.003
        )
        node.fragment_memory += (
            recovery_attempt
            - memory_loss
        )
        node.memory_erosion += (
            memory_loss * 0.05
        )
        node.knowledge_fusion += (
            recovery_attempt * 0.60
            - fusion_conflict
        )
        node.lineage_inheritance += (
            node.fragment_memory * 0.0035
            - lineage_decay
        )
        node.cultural_compression += (
            node.lineage_inheritance * 0.0028
            - compression_loss
        )
        node.civilization_resonance += (
            node.cultural_compression * 0.0022
            - resonance_decay
        )
        node.memory_circulation += (
            circulation_shift
        )
        node.memory_contamination += (
            contamination_shift
        )
        node.legacy_dominance += (
            node.lineage_inheritance
            * 0.001
        )
        node.legacy_dominance -= (
            node.memory_circulation
            * 0.0005
        )
        node.fragment_memory = clamp(
            node.fragment_memory,
            0.15, 0.55
        )
        node.memory_erosion = clamp(
            node.memory_erosion,
            0.20, 0.65
        )
        node.knowledge_fusion = clamp(
            node.knowledge_fusion,
            0.10, 0.45
        )
        node.lineage_inheritance = clamp(
            node.lineage_inheritance,
            0.20, 0.60
        )
        node.cultural_compression = clamp(
            node.cultural_compression,
            0.30, 0.85
        )
        node.civilization_resonance = clamp(
            node.civilization_resonance,
            0.10, 0.50
        )
        node.memory_circulation = clamp(
            node.memory_circulation,
            0.20, 0.70
        )
        node.legacy_dominance = clamp(
            node.legacy_dominance,
            0.15, 0.55
        )
        node.memory_contamination = clamp(
            node.memory_contamination,
            0.05, 0.25
        )
def compute_metrics(nodes):
    return {
        "fragment_recovery_rate":
        round(sum(
            n.fragment_memory
            for n in nodes
        ) / NUM_NODES, 4),
        "memory_erosion_rate":
        round(sum(
            n.memory_erosion
            for n in nodes
        ) / NUM_NODES, 4),
        "knowledge_fusion_rate":
        round(sum(
            n.knowledge_fusion
            for n in nodes
        ) / NUM_NODES, 4),
        "lineage_inheritance_rate":
        round(sum(
            n.lineage_inheritance
            for n in nodes
        ) / NUM_NODES, 4),
        "cultural_compression_rate":
        round(sum(
            n.cultural_compression
            for n in nodes
        ) / NUM_NODES, 4),
        "civilization_resonance_rate":
        round(sum(
            n.civilization_resonance
            for n in nodes
        ) / NUM_NODES, 4),
        "memory_circulation_rate":
        round(sum(
            n.memory_circulation
            for n in nodes
        ) / NUM_NODES, 4),
        "legacy_dominance_pressure":
        round(sum(
            n.legacy_dominance
            for n in nodes
        ) / NUM_NODES, 4),
        "memory_contamination_rate":
        round(sum(
            n.memory_contamination
            for n in nodes
        ) / NUM_NODES, 4)
    }
def validate(metrics):
    return all([
        0.20 <= metrics["fragment_recovery_rate"] <= 0.50,
        0.20 <= metrics["memory_erosion_rate"] <= 0.65,
        0.10 <= metrics["knowledge_fusion_rate"] <= 0.45,
        0.23 <= metrics["lineage_inheritance_rate"] <= 0.58,
        0.31 <= metrics["cultural_compression_rate"] <= 0.83,
        0.11 <= metrics["civilization_resonance_rate"] <= 0.48,
        0.20 <= metrics["memory_circulation_rate"] <= 0.70,
        0.15 <= metrics["legacy_dominance_pressure"] <= 0.55,
        0.05 <= metrics["memory_contamination_rate"] <= 0.25
    ])
def run(seed):
    random.seed(seed)
    nodes = [
        Node(index)
        for index in range(NUM_NODES)
    ]
    for _ in range(NUM_STEPS):
        update_inheritance_formation(
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
