"""
DAA Assignment 2026 - Batch 15: Cloud VM Consolidation
Module: Heuristics & Data Structures (First-Fit Decreasing, Best-Fit Decreasing, Segment Tree)
"""

import math
from typing import List, Tuple, Dict, Any

class SegmentTree:
    """
    Max-Segment Tree over physical server capacities.
    Supports:
      - query_first_fit(capacity_needed): O(log m) time to find leftmost server with >= capacity_needed
      - update(server_idx, new_remaining_capacity): O(log m)
    Enables O(N log N) First-Fit placement across 5,000+ servers.
    """
    def __init__(self, size: int, initial_capacity: int):
        self.n = size
        self.capacity = initial_capacity
        self.tree = [0] * (4 * size)
        self.build(1, 0, size - 1)

    def build(self, node: int, start: int, end: int):
        if start == end:
            self.tree[node] = self.capacity
            return
        mid = (start + end) // 2
        self.build(2 * node, start, mid)
        self.build(2 * node + 1, mid + 1, end)
        self.tree[node] = max(self.tree[2 * node], self.tree[2 * node + 1])

    def query_first_fit(self, node: int, start: int, end: int, val: int) -> int:
        """Finds the lowest index (leftmost server) with residual capacity >= val."""
        if self.tree[node] < val:
            return -1  # No server in this subtree has enough room
        if start == end:
            return start
        mid = (start + end) // 2
        # Greedily search left child first for First-Fit
        if self.tree[2 * node] >= val:
            return self.query_first_fit(2 * node, start, mid, val)
        else:
            return self.query_first_fit(2 * node + 1, mid + 1, end, val)

    def update(self, node: int, start: int, end: int, idx: int, new_val: int):
        if start == end:
            self.tree[node] = new_val
            return
        mid = (start + end) // 2
        if start <= idx <= mid:
            self.update(2 * node, start, mid, idx, new_val)
        else:
            self.update(2 * node + 1, mid + 1, end, idx, new_val)
        self.tree[node] = max(self.tree[2 * node], self.tree[2 * node + 1])


def first_fit_decreasing(items: List[int], bin_capacity: int) -> Tuple[List[List[int]], List[Dict[str, Any]]]:
    """
    First-Fit Decreasing (FFD) approximation algorithm.
    Sorts items in descending order, places each item in the first bin that can accommodate it.
    Returns: (list_of_bins, trace_log)
    """
    sorted_items = sorted(items, reverse=True)
    bins: List[List[int]] = []
    bin_rem: List[int] = []
    trace_log = []

    for item in sorted_items:
        placed = False
        step_info = {"item": item, "action": None, "bin_idx": None, "state_after": None}
        for b_idx in range(len(bins)):
            if bin_rem[b_idx] >= item:
                bins[b_idx].append(item)
                bin_rem[b_idx] -= item
                placed = True
                step_info["action"] = f"Placed {item} in existing Server {b_idx + 1}"
                step_info["bin_idx"] = b_idx + 1
                break
        if not placed:
            bins.append([item])
            bin_rem.append(bin_capacity - item)
            step_info["action"] = f"Opened new Server {len(bins)} with VM {item}"
            step_info["bin_idx"] = len(bins)
        
        step_info["state_after"] = [
            {"server": i + 1, "vms": list(bins[i]), "used": bin_capacity - bin_rem[i], "free": bin_rem[i]}
            for i in range(len(bins))
        ]
        trace_log.append(step_info)

    return bins, trace_log


def best_fit_decreasing(items: List[int], bin_capacity: int) -> List[List[int]]:
    """
    Best-Fit Decreasing (BFD) algorithm.
    Places item into the bin that leaves the least residual capacity.
    """
    sorted_items = sorted(items, reverse=True)
    bins: List[List[int]] = []
    bin_rem: List[int] = []

    for item in sorted_items:
        best_idx = -1
        min_rem = bin_capacity + 1
        for b_idx in range(len(bins)):
            if bin_rem[b_idx] >= item and (bin_rem[b_idx] - item) < min_rem:
                min_rem = bin_rem[b_idx] - item
                best_idx = b_idx
        if best_idx != -1:
            bins[best_idx].append(item)
            bin_rem[best_idx] -= item
        else:
            bins.append([item])
            bin_rem.append(bin_capacity - item)

    return bins


def get_ffd_counterexample() -> Dict[str, Any]:
    """
    Constructs a concrete instance where FFD uses strictly more servers than optimal.
    Capacity C = 16.
    Items: [7, 6, 5, 5, 5, 4]
    Total sum = 32.
    Optimal: 2 bins:
      Server 1: [7, 5, 4] = 16
      Server 2: [6, 5, 5] = 16
    FFD: 3 bins:
      Server 1: [7, 6] = 13 (rem 3)
      Server 2: [5, 5, 5] = 15 (rem 1)
      Server 3: [4] = 4 (rem 12)
    """
    items = [7, 6, 5, 5, 5, 4]
    capacity = 16
    bins_ffd, trace = first_fit_decreasing(items, capacity)
    optimal_packing = [[7, 5, 4], [6, 5, 5]]
    return {
        "capacity": capacity,
        "items": items,
        "optimal_bins": optimal_packing,
        "optimal_count": len(optimal_packing),
        "ffd_bins": bins_ffd,
        "ffd_count": len(bins_ffd),
        "trace": trace
    }


if __name__ == "__main__":
    test_instance = [9, 8, 7, 6, 5, 4, 3, 2]
    C = 16
    print(f"=== Running FFD on Batch 15 Instance {test_instance} (C = {C}) ===")
    bins, trace = first_fit_decreasing(test_instance, C)
    print(f"Total Servers Used by FFD: {len(bins)}")
    for i, b in enumerate(bins, 1):
        print(f"  Server {i}: VMs {b} -> Total = {sum(b)}/{C} vCPUs (Remaining: {C - sum(b)})")
    
    print("\n=== Counterexample for FFD ===")
    counter = get_ffd_counterexample()
    print(f"Items: {counter['items']}, Capacity: {counter['capacity']}")
    print(f"Optimal Servers ({counter['optimal_count']}): {counter['optimal_bins']}")
    print(f"FFD Servers ({counter['ffd_count']}): {counter['ffd_bins']}")
