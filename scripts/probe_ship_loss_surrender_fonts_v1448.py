"""Reverify all624 source/native/name/font cases after natural address movement."""
from pathlib import Path

if __name__=='__main__':
    source = Path('scripts/probe_ship_loss_surrender_fonts_v1445.py').read_text(encoding='utf-8')
    for old,new in [
        ('scripts.ship_loss_surrender_native_plan_v1444b import compiled','scripts.ship_loss_surrender_native_plan_v1447 import compiled'),
        ("'work/analysis/ship_loss_surrender_fonts_v1445'","'work/analysis/ship_loss_surrender_fonts_v1448'"),
        ("'work/analysis/ship_loss_surrender_payload_v1444b/native_payload_plan.json'","'work/analysis/ship_loss_surrender_payload_v1447/native_payload_plan.json'"),
        ("'translations/ship_loss_surrender_editorial_manuscript_v1.json'","'translations/ship_loss_surrender_editorial_manuscript_v2.json'")]:
        assert source.count(old)==1,old
        source = source.replace(old,new)
    exec(compile(source,__file__,'exec'),{**globals(),'__name__':'__main__'})
