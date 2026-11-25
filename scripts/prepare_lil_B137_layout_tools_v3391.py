"""Prepare the exact48-speech progressive profile andfull native font proof."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    pairs=[]
    old=Path('scripts/prepare_lil_B135_B136_layout_v3356.py');new=Path('scripts/prepare_lil_B137_layout_v3391b.py');assert not new.exists();t=old.read_text(encoding='utf-8')
    changes={
      'scripts.author_lil_B135_B136_v3355':'scripts.author_lil_B137_v3390b',
      'lil_B135_B136_layout_tools_v3356':'lil_B137_layout_tools_v3391b',
      'plan_lil_B135_B136_layout_v3356b':'plan_lil_B137_layout_v3391c',
      'lil_B135_B136_controls_v3347':'lil_B137_controls_v3384',
      'lil_B135_B136_layout_v3356b':'lil_B137_layout_v3391c',
      'B135/B136':'B137','B135-B136':'B137','lil_B135_B136':'lil_B137',
      'frozenset({2,9,14,36,47,96})':'frozenset({2,9,14,16,17,20,22,23,38,92,198})',
      "len(control['speech_dispatch_cases'])!=70":"len(control['speech_dispatch_cases'])!=96",
      "len(control['current_original_predicate_cases'])!=1":"len(control['current_original_predicate_cases'])!=12",
      "{'FI':0,'FA':0,'FO':1}":"{'FI':3,'FA':0,'FO':0}",
      "len(voice['fresh_six_actor_names']['rows'])!=6":"len(voice['fresh_eleven_actor_names']['rows'])!=11",
      '35 progressive speeches,six static actors':'48 progressive speeches,eleven static actors',
      "('goddess','temptation'),('cheese','tart'),('upper','stone'),('lower','stone'),('stone','tablets'),":"('bar','snacks'),('below','average'),('big','tip'),('five','times'),('poetry','notes'),('my','money'),('other','girls'),('under','my'),('my','control'),('world','go'),('go','round'),",
      'all35_paragraph_layout_QA':'all48_paragraph_layout_QA','len(reports)==35':'len(reports)==48','plans=35':'plans=48',
    }
    for a,b in sorted(changes.items(),key=lambda kv:-len(kv[0])):assert a in t,a;t=t.replace(a,b)
    compile(t,str(new),'exec');new.write_text(t,encoding='utf-8');pairs.append((old,new))
    old=Path('scripts/verify_lil_B135_B136_fonts_v3357b.py');new=Path('scripts/verify_lil_B137_fonts_v3392.py');assert not new.exists();t=old.read_text(encoding='utf-8')
    changes={'lil_B135_B136_fonts_v3357b':'lil_B137_fonts_v3392','lil_B135_B136':'lil_B137',
      'len(cases)==35 and len(qa_reports)==35 and macro_calls==280':'len(cases)==48 and len(qa_reports)==48 and macro_calls==384',
      'blocks[135]':'blocks[137]','blocks[134]':'blocks[136]','selectors=[2,9,14,36,47,96]':'selectors=[2,9,14,16,17,20,22,23,38,92,198]',
      'len(negatives)==21':'len(negatives)==31','all35_complete_source_speech_prefixes_preserved':'all48_complete_source_speech_prefixes_preserved',
      'all35_full_QA_reports':'all48_full_QA_reports','current_original_macro_alignment_calls=280':'current_original_macro_alignment_calls=384',
      'all35_progressive_full_QA_and_complete_native_fonts_pass':'all48_progressive_full_QA_and_complete_native_fonts_pass',
      'all35_painted_consumers_original_progressive54020':'all48_painted_consumers_original_progressive54020',
      'all35_speeches_share_original_progressive_consumer':'all48_speeches_share_original_progressive_consumer',
      'actual_selected_B135_B136_IDs':'actual_selected_B137_IDs'}
    for a,b in sorted(changes.items(),key=lambda kv:-len(kv[0])):assert a in t,a;t=t.replace(a,b)
    t=t[:t.rindex('    print(')]+"    print('48complete progressiveplanes,384macro cases,48QAplans and31source-consumer negatives pass;sixsheets requirevisualreview. No gameplay orcredit.')\n"
    compile(t,str(new),'exec');new.write_text(t,encoding='utf-8');pairs.append((old,new));root=Path('work/analysis/lil_B137_layout_tool_preparation_v3391');root.mkdir(parents=True);save(root/'provenance.json',dict(producers=[dict(previous=str(a),previous_sha256=sha(a.read_bytes()),successor=str(b),successor_sha256=sha(b.read_bytes())) for a,b in pairs],allglobalhelpers_and_previous_profiles_unchanged=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
