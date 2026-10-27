"""Successor actual verifier for the fully audited crew/supply-enabled test run."""
from pathlib import Path

if __name__ == '__main__':
    source = Path('scripts/verify_hot_spring_notice_actual_v1646.py').read_text(encoding='utf-8')
    for old, new in [
        ('from scripts.audit_hot_spring_resilient_v1645c import audit', 'from scripts.audit_hot_spring_crew_v1654 import audit'),
        ("ROOT=Path('work/analysis/hot_spring_notice_actual_v1646')", "ROOT=Path('work/analysis/hot_spring_crew_actual_v1656')"),
        ('hot_spring_notice_resilient_v1645_1637', 'hot_spring_crew_v1651_1637'),
        ('artificial_locations_and_single_original_supply_refill_not_earned_travel_or_resupply',
         'artificial_locations_and_declared_crew_supply_refills_not_earned_travel_resupply_or_recruitment')]:
        assert source.count(old) == 1
        source = source.replace(old, new)
    exec(compile(source, __file__, 'exec'), {'__name__': '__main__', '__file__': __file__})
