from __future__ import annotations

import math
from collections import Counter


def shannon_entropy(data: bytes) -> float:
    if not data:
        return 0.0
    total = len(data)
    return -sum((count / total) * math.log2(count / total) for count in Counter(data).values())

