"""Successor: ordinary A dismisses the directly inspected zero-crew warning339.

Frame48338 was viewed: Vestaros has no sailors, one A acknowledgement.
No crew is restored and no unknown or hot-spring text is skipped.
"""
from pathlib import Path
from scripts import navigate_hot_spring_search_v1648 as previous

if __name__ == '__main__':
    previous.KNOWN = previous.KNOWN | {339}
    previous.EVENTS = Path('work/analysis/hot_spring_notice_resilient_v1645/bounded_navigator_v1649.jsonl')
    previous.main()
