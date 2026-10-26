"""Fix extraction of actor00 source objects using the native command boundary."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    old=Path('scripts/inventory_lil_after_B119_v3257b.py');new=Path('scripts/inventory_lil_after_B119_v3257c.py');assert not new.exists();t=old.read_text(encoding='utf-8')
    a="at=c['offset']+5;raw=block[at:block.index(bytes([0]),at)];ident="
    b="at=c['offset']+5;raw=block[at:block.index(bytes([0]),at+1)];assert c['native_extent']==(5+len(raw)+1+1)//2*2;ident="
    assert t.count(a)==1;t=t.replace(a,b)
    for a,b in [('lil_after_B119_clean_scope_v3257b','lil_after_B119_clean_scope_v3257c'),('source_selector=raw[0] if raw else None,zero_length_native4000_requires_original_consumer_classification=not raw','source_selector=raw[0],zero_valued_native_actor_selector_requires_current_binding=raw[0]==0'),("nonempty_physical_speech_bodies=sum(bool(r['source_hex']) for r in rows),zero_length_native4000_objects=sum(not r['source_hex'] for r in rows)","all_native_speech_bodies_include_complete_selector=True,zero_valued_native_actor_selectors=sum(r['source_selector']==0 for r in rows)"),("zero_length_native4000_objects=sum(b['zero_length_native4000_objects'] for b in results)","zero_valued_native_actor_selectors=sum(b['zero_valued_native_actor_selectors'] for b in results)")]:assert a in t,a;t=t.replace(a,b)
    compile(t,str(new),'exec');new.write_text(t,encoding='utf-8')
    save(Path('work/analysis/lil_after_B119_clean_scope_v3257/zero_selector_extraction_correction.json'),dict(previous=str(old),previous_sha256=sha(old.read_bytes()),successor=str(new),successor_sha256=sha(new.read_bytes()),finding='The18 apparent empty B133 objects have complete native extents containing real Japanese after source selector00. Search for the body terminator after the mandatory selector byte; retain selector00 and verify every native even extent from the complete source object. They are not empty paragraphs. Static actor identity,current consumer,route/company andentry semantics still require binding before review.',previous_failure_and_nonexhaustive3257b_packet_preserved=True,new_source_classification_not_later_older_record_technical_reaudit=True,no_source_ROM_or_editorial_credit_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
