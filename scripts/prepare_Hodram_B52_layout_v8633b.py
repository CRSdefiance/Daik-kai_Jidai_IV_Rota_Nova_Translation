"""Derive unchanged full-width guarded progressive planning for three B52 speeches; choices remain distinct."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B52_layout_tools_v8633b');assert not root.exists();tools=[]
    logical=Path('scripts/prove_Hodram_B52_logical_v8633.py');proof=Path('work/analysis/Hodram_B52_logical_v8633/logical_paragraphs.json')
    tools.append(dict(existing_successor=str(logical),successor_sha256=__import__('hashlib').sha256(logical.read_bytes()).hexdigest(),completed_native_proof=str(proof),completed_native_proof_sha256=__import__('hashlib').sha256(proof.read_bytes()).hexdigest(),completed_twelve_logical_alignments_preserved_without_replay=True))
    source=Path('scripts/plan_Hodram_B51_v8562.py').read_text(encoding='utf-8')
    a=source.index('PAIRS=');b=source.index('\nENV=',a)
    tools.append(derive('scripts/plan_Hodram_B51_v8562.py','scripts/plan_Hodram_B52_v8634.py',{
        'Hodram_B51_layout_v8562':'Hodram_B52_layout_v8634','hodram_B51_editorial_manuscript_v1':'hodram_B52_editorial_manuscript_v1','Hodram_B51_logical_v8561':'Hodram_B52_logical_v8633',
        "row['source_selector'] in [1,16,18,113]":"row['source_selector'] in [113]",
        'Hodram B51 plan:':'Hodram B52 plan:','Hodram-B51-RESEARCH-ONLY:':'Hodram-B52-RESEARCH-ONLY:',
        source[a:b]:source[a:b]+'''|{("hayreddin's",'outfit'),('death','wish')}''',
        "logical['fresh_native_alignment_cases']==20 and len(doc['records'])==5":"logical['fresh_native_alignment_cases']==12 and len(doc['records'])==3",
        'len(rows)==5':'len(rows)==3',
    }))
    tools.append(derive('scripts/prove_Hodram_B51_pages_v8563.py','scripts/prove_Hodram_B52_pages_v8635.py',{
        'scripts.Hodram_B50_registered_route_context_v8546':'scripts.Hodram_B51_registered_route_context_v8612',
        'Hodram_B51_pages_v8563':'Hodram_B52_pages_v8635','hodram_B51_editorial_manuscript_v1':'hodram_B52_editorial_manuscript_v1','Hodram_B51_layout_v8562':'Hodram_B52_layout_v8634','Hodram_B51_logical_v8561':'Hodram_B52_logical_v8633','Hodram_B51_source_display_v8556':'Hodram_B52_source_display_v8626','current_V8543_Hodram_native_v8546':'current_V8609_Hodram_native_v8612',
        "len(plan['records']) == 5":"len(plan['records']) == 3",'len(rows) == len(pictures) == 5':'len(rows) == len(pictures) == 3',
        '(912, 480)':'(912, 320)','five_complete_English_native_pages':'three_complete_English_native_pages',
        'fresh_compiled_alignment_cases=20, progressive_alignment_cases=20':'fresh_compiled_alignment_cases=12, progressive_alignment_cases=12','complete_progressive_pages=5':'complete_progressive_pages=3',
        'all_five_single_pages_no_blank_orunintended_extra_page':'all_three_speech_single_pages_no_blank_orunintended_extra_page',
        'Five complete B51 native English pages and twenty compiled macro alignments.':'Three complete B52 native English speech pages and twelve compiled macro alignments; choices uncompiled.',
        'Five complete native B51 English pages, twenty compiled alignments':'Three complete native B52 English speech pages, twelve compiled alignments',
    }))
    root.mkdir(parents=True);save(root/'derivations.json',dict(tools=tools,all_native_high_integer_constants_andmultiplicity_preserved=True,full216px_original_metrics_guards_pair_phase_macro_lengths_QA_andfont_oracles_preserved=True,only_actor113_andthree_speeches_in_scope_two_typed_choices_compile_separately=True,no_authored_ordinary_breaks_padding_shortening_orQA_waiver=True,no_ROM_registry_orcredit_change=True,new_credit=0,full_goal_complete=False))
