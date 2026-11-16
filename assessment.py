"""Simple teaching/demo EC2 sizing rules.

This is a classroom estimation model, not an official AWS migration tool.
It checks minimum vCPU and memory requirements; production sizing should
also consider CPU utilization, storage performance, networking and workload tests.
"""

INSTANCE_CATALOG = [
    {"type": "t3.micro", "vcpu": 2, "ram_gb": 1, "description": "Small test or low-traffic workload"},
    {"type": "t3.small", "vcpu": 2, "ram_gb": 2, "description": "Small application workload"},
    {"type": "t3.medium", "vcpu": 2, "ram_gb": 4, "description": "Small-to-medium application workload"},
    {"type": "t3.large", "vcpu": 2, "ram_gb": 8, "description": "Memory-heavier application workload"},
    {"type": "m5.large", "vcpu": 2, "ram_gb": 8, "description": "General-purpose workload"},
    {"type": "m5.xlarge", "vcpu": 4, "ram_gb": 16, "description": "Larger general-purpose workload"},
    {"type": "c5.xlarge", "vcpu": 4, "ram_gb": 8, "description": "Compute-oriented workload"},
]

def recommend_instance(required_vcpu: int, required_ram_gb: float) -> dict:
    """Return the smallest catalog entry meeting CPU and RAM requirements."""
    candidates = [
        item for item in INSTANCE_CATALOG
        if item["vcpu"] >= required_vcpu and item["ram_gb"] >= required_ram_gb
    ]
    if not candidates:
        raise ValueError(
            "No instance in the demo catalog meets these requirements. "
            "Try lower requirements or extend INSTANCE_CATALOG."
        )
    candidates.sort(key=lambda item: (item["vcpu"] * item["ram_gb"], item["ram_gb"], item["vcpu"]))
    return candidates[0]
