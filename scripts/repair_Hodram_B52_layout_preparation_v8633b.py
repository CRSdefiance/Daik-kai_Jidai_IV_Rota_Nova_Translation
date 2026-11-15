"""Preserve the completed logical proof and correct only an absent derivation spelling."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive,checked_text
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B52_layout_preparation_repair_v8633b');assert not root.exists()
    original=Path('scripts/prove_Hodram_B51_logical_v8561.py').read_text(encoding='utf-8')
    expected=checked_text(original,{
        'scripts.Hodram_B50_registered_route_context_v8546':'scripts.Hodram_B51_registered_route_context_v8612',
        'Hodram_B51_logical_v8561':'Hodram_B52_logical_v8633','hodram_B51_editorial_manuscript_v1':'hodram_B52_editorial_manuscript_v1','Hodram_B51_source_display_v8556':'Hodram_B52_source_display_v8626','current_V8543_Hodram_native_v8546':'current_V8609_Hodram_native_v8612',
        "len(doc['records']) == 5":"len(doc['records']) == 3",'prefix in [1, 16, 18, 113]':'prefix in [113]','len(rows) == 5':'len(rows) == 3',
        'fresh_native_alignment_cases=20, progressive_alignment_cases=20':'fresh_native_alignment_cases=12, progressive_alignment_cases=12',
        'Twenty native macro alignments for B51\'s five one-paragraph English drafts.':'Twelve native macro alignments for B52\'s three one-paragraph English drafts; typed choices remain separate.',
        'B51 logical: twenty':'B52 logical: twelve'})
    logical=Path('scripts/prove_Hodram_B52_logical_v8633.py');proof=Path('work/analysis/Hodram_B52_logical_v8633/logical_paragraphs.json')
    assert logical.read_text(encoding='utf-8')==expected and read(proof)['fresh_native_alignment_cases']==12
    source=Path('scripts/prepare_Hodram_B52_layout_v8633.py').read_text(encoding='utf-8')
    a=source.index('    tools.append(derive(');b=source.index('    source=Path(',a)
    preserved="""    logical=Path('scripts/prove_Hodram_B52_logical_v8633.py');proof=Path('work/analysis/Hodram_B52_logical_v8633/logical_paragraphs.json')
    tools.append(dict(existing_successor=str(logical),successor_sha256=__import__('hashlib').sha256(logical.read_bytes()).hexdigest(),completed_native_proof=str(proof),completed_native_proof_sha256=__import__('hashlib').sha256(proof.read_bytes()).hexdigest(),completed_twelve_logical_alignments_preserved_without_replay=True))
"""
    result=derive('scripts/prepare_Hodram_B52_layout_v8633.py','scripts/prepare_Hodram_B52_layout_v8633b.py',{
        source[a:b]:preserved,
        "Path('work/analysis/Hodram_B52_layout_tools_v8633')":"Path('work/analysis/Hodram_B52_layout_tools_v8633b')",
        '''        "row['source_selector'] in [1, 16, 18, 113]":"row['source_selector'] in [113]",
''':'',
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(derivation=result,original_failed_preparer_preserved=True,prior_failure='Derivation key absent: spaced selector list; actual planner uses unspaced list',existing_logical_source_matches_exact_checked_successor=True,logical_proof=str(proof),logical_proof_sha256=sha(proof.read_bytes()),no_completed_logical_probe_replayed=True,all_native_constants_prose_profile_width_andQA_guards_preserved=True,new_credit=0,full_goal_complete=False))
