"""Prepare44 complete current native planes and352 macro-alignment cases."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
if __name__=='__main__':
    registry=read('translations/release_stack.json');assert len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v1492'
    a=Path('scripts/verify_lil_B137_fonts_v3394b.py');b=Path('scripts/verify_lil_B138_fonts_v3435.py');assert not b.exists();t=a.read_text(encoding='utf-8')
    changes=[('Current1192macro calls,149progressive planes andall150paragraph QA.','Current352 macro calls,44 progressive planes and44 full paragraph QA.'),('lil_B137','lil_B138'),('fonts_v3394b','fonts_v3435'),('blocks[137]','blocks[138]'),('blocks[136]','blocks[137]'),('len(cases)==48','len(cases)==44'),('len(qa_reports)==48','len(qa_reports)==44'),('macro_calls==384','macro_calls==352'),('selectors=[2,9,14,16,17,20,22,23,38,92,198]','selectors=[2,14,20,21,22,23,92]'),('format(9 if selector==2 else 2','format(14 if selector==2 else 2'),('len(negatives)==31','len(negatives)==23'),('all48','all44'),('current_original_macro_alignment_calls=384','current_original_macro_alignment_calls=352'),('48complete progressiveplanes,384macro cases,48QAplans and31source-consumer','44complete progressiveplanes,352macro cases,44QAplans and23source-consumer')]
    for x,y in changes:assert x in t,x;t=t.replace(x,y)
    compile(t,str(b),'exec');b.write_text(t,encoding='utf-8');root=Path('work/analysis/lil_B138_font_tools_v3435');assert not root.exists();root.mkdir(parents=True)
    save(root/'provenance.json',dict(previous=str(a),previous_sha256=sha(a.read_bytes()),successor=str(b),successor_sha256=sha(b.read_bytes()),registry_sha256=sha(Path('translations/release_stack.json').read_bytes()),producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
