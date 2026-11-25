"""Retain zero-length native4000 objects as explicit unclassified source leads."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    old=Path('scripts/inventory_lil_after_B119_v3257.py');new=Path('scripts/inventory_lil_after_B119_v3257b.py');assert not new.exists();t=old.read_text(encoding='utf-8')
    for a,b in [
        ('lil_after_B119_clean_scope_v3257','lil_after_B119_clean_scope_v3257b'),
        ('source_selector=raw[0]','source_selector=raw[0] if raw else None,zero_length_native4000_requires_original_consumer_classification=not raw,whole_native_command_hex=c[\'whole_command_hex\']'),
        ("sorted({r['source_selector'] for r in rows})","sorted({r['source_selector'] for r in rows if r['source_selector'] is not None})"),
        ("speeches=len(rows),FE_panels=","speeches=len(rows),nonempty_physical_speech_bodies=sum(bool(r['source_hex']) for r in rows),zero_length_native4000_objects=sum(not r['source_hex'] for r in rows),FE_panels="),
        ('new_editorial_credit=0))','zero_length_native4000_objects=sum(b[\'zero_length_native4000_objects\'] for b in results),new_editorial_credit=0))')]:assert a in t,a;t=t.replace(a,b)
    compile(t,str(new),'exec');new.write_text(t,encoding='utf-8')
    save(Path('work/analysis/lil_after_B119_clean_scope_v3257/zero_length_source_object_successor.json'),dict(previous=str(old),previous_sha256=sha(old.read_bytes()),successor=str(new),successor_sha256=sha(new.read_bytes()),finding='A next-scope native4000 object has a zero-length C-string body. Preserve its complete original command and exact reference as an unclassified lead; do not guess a speaker, discard it or count it as reviewed prose.',previous_failed_producer_preserved=True,no_source_ROM_or_editorial_credit_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
