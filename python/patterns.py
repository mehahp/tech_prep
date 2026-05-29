#!/usr/bin/env python3
"""
Runnable reference implementations of the core interview patterns.
Read them, then CLOSE the file and re-type each from memory (that's the rep).

Run the built-in self-tests:   python3 patterns.py
Everything below is plain stdlib — no pandas required.
"""
from collections import Counter, defaultdict, deque
import bisect
import heapq


# ----------------------------------------------------------------------------
# (a) Hash-map one-pass
# ----------------------------------------------------------------------------
def two_sum(nums, target):
    """Return indices of two numbers summing to target, or None. O(n)."""
    seen = {}  # value -> index
    for i, n in enumerate(nums):
        if target - n in seen:
            return [seen[target - n], i]
        seen[n] = i
    return None


# ----------------------------------------------------------------------------
# (b) Two pointers on a sorted array
# ----------------------------------------------------------------------------
def pair_sum_sorted(a, target):
    """Indices of a pair summing to target in a SORTED array. O(n)."""
    i, j = 0, len(a) - 1
    while i < j:
        s = a[i] + a[j]
        if s == target:
            return (i, j)
        if s < target:
            i += 1
        else:
            j -= 1
    return None


# ----------------------------------------------------------------------------
# (c) Sliding window
# ----------------------------------------------------------------------------
def longest_unique_substr(s):
    """Length of the longest substring without repeating chars. O(n)."""
    last = {}  # char -> last seen index
    start = best = 0
    for i, ch in enumerate(s):
        if ch in last and last[ch] >= start:
            start = last[ch] + 1
        last[ch] = i
        best = max(best, i - start + 1)
    return best


def max_subarray_sum_k(nums, k):
    """Max sum of any contiguous window of length k. O(n)."""
    if k > len(nums):
        return None
    window = sum(nums[:k])
    best = window
    for i in range(k, len(nums)):
        window += nums[i] - nums[i - k]
        best = max(best, window)
    return best


# ----------------------------------------------------------------------------
# (d) Frequency / grouping
# ----------------------------------------------------------------------------
def group_anagrams(words):
    """Group words that are anagrams of each other."""
    groups = defaultdict(list)
    for w in words:
        groups[tuple(sorted(w))].append(w)
    return list(groups.values())


def top_k_frequent(items, k):
    """k most frequent items (any order among ties)."""
    return [item for item, _ in Counter(items).most_common(k)]


# ----------------------------------------------------------------------------
# "SQL in Python" — the data-wrangling patterns most relevant to this role
# ----------------------------------------------------------------------------
def group_by_sum(rows, key, value):
    """GROUP BY key, SUM(value).  rows = list of dicts."""
    agg = defaultdict(float)
    for r in rows:
        agg[r[key]] += r[value]
    return dict(agg)


def left_join(left, right, on):
    """Enrich each left row with matching right row's fields (dict index join)."""
    index = {r[on]: r for r in right}
    out = []
    for l in left:
        merged = dict(l)
        match = index.get(l[on])
        if match:
            merged.update({k: v for k, v in match.items() if k != on})
        out.append(merged)
    return out


def moving_average(series, window):
    """Trailing moving average over a list of (date, value), sorted by date."""
    series = sorted(series)
    vals = [v for _, v in series]
    out = []
    running = 0.0
    dq = deque()
    for (d, v) in series:
        dq.append(v)
        running += v
        if len(dq) > window:
            running -= dq.popleft()
        out.append((d, round(running / len(dq), 3)))
    return out


def top_n_per_group(rows, group_key, metric_key, n):
    """Top-n rows per group by metric (the window-function pattern, in Python)."""
    groups = defaultdict(list)
    for r in rows:
        groups[r[group_key]].append(r)
    out = []
    for g, items in groups.items():
        items.sort(key=lambda r: r[metric_key], reverse=True)
        out.extend(items[:n])
    return out


# ----------------------------------------------------------------------------
# Graph BFS + binary search (round them out)
# ----------------------------------------------------------------------------
def bfs_shortest(graph, start, goal):
    """Fewest edges from start to goal in an unweighted adjacency dict."""
    if start == goal:
        return 0
    seen = {start}
    q = deque([(start, 0)])
    while q:
        node, dist = q.popleft()
        for nbr in graph.get(node, []):
            if nbr == goal:
                return dist + 1
            if nbr not in seen:
                seen.add(nbr)
                q.append((nbr, dist + 1))
    return -1


def binary_search(a, target):
    """Index of target in sorted a, or -1."""
    i = bisect.bisect_left(a, target)
    return i if i < len(a) and a[i] == target else -1


# ----------------------------------------------------------------------------
# self-tests
# ----------------------------------------------------------------------------
def _test():
    assert two_sum([2, 7, 11, 15], 9) == [0, 1]
    assert two_sum([1, 2, 3], 7) is None
    assert pair_sum_sorted([1, 2, 4, 7, 11], 15) == (2, 4)
    assert longest_unique_substr("abcabcbb") == 3
    assert longest_unique_substr("") == 0
    assert max_subarray_sum_k([1, 2, 3, 4], 2) == 7
    assert sorted(map(sorted, group_anagrams(["eat", "tea", "tan", "nat"]))) \
        == sorted(map(sorted, [["eat", "tea"], ["tan", "nat"]]))
    assert set(top_k_frequent([1, 1, 1, 2, 2, 3], 2)) == {1, 2}

    rows = [{"region": "us", "cost": 10.0},
            {"region": "us", "cost": 5.0},
            {"region": "eu", "cost": 7.0}]
    assert group_by_sum(rows, "region", "cost") == {"us": 15.0, "eu": 7.0}

    servers = [{"dc_id": 1, "name": "s1"}, {"dc_id": 2, "name": "s2"}]
    dcs = [{"dc_id": 1, "region": "us"}, {"dc_id": 2, "region": "eu"}]
    joined = left_join(servers, dcs, "dc_id")
    assert joined[0]["region"] == "us" and joined[1]["region"] == "eu"

    ma = moving_average([("d1", 2), ("d2", 4), ("d3", 6)], 2)
    assert ma[-1] == ("d3", 5.0)

    grp = top_n_per_group(rows, "region", "cost", 1)
    assert {r["region"]: r["cost"] for r in grp} == {"us": 10.0, "eu": 7.0}

    g = {"a": ["b", "c"], "b": ["d"], "c": ["d"], "d": []}
    assert bfs_shortest(g, "a", "d") == 2
    assert binary_search([1, 3, 5, 7], 5) == 2
    assert binary_search([1, 3, 5, 7], 4) == -1

    print("patterns.py: all self-tests passed ✔")


if __name__ == "__main__":
    _test()
