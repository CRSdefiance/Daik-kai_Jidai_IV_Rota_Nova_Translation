"""Fresh cold-boot original encounter pilot from a closer water point."""
from pathlib import Path

if __name__=='__main__':
    source = Path('scripts/run_combat_approach_v1464.py').read_text(encoding='utf-8')
    for old,new in [
        ('scripts.native_combat_approach_fixture_v1463 import apply_fixture,ROM','scripts.native_close_approach_fixture_v1467 import apply_fixture,ROM'),
        ("'work/analysis/combat_approach_v1464'","'work/analysis/close_combat_approach_v1468'"),
        ('combat_approach_v1464_1456','close_combat_approach_v1468_1456')]:
        assert source.count(old)==1,old
        source = source.replace(old,new)
    exec(compile(source,__file__,'exec'),{**globals(),'__name__':'__main__'})
