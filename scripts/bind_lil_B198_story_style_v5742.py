"""Bind unchanged B198 wording/compiled targets to the source-correct native style proof."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B198_story_style_binding_v5742')
INPUT=Path('translations/lil_B198_editorial_manuscript_v4.json')
OUTPUT=Path('translations/lil_B198_editorial_manuscript_v5.json')
FONT=Path('work/analysis/lil_B198_fonts_v5741/all17_progressive_FE_native_planes_and136_alignment_cases.json')
if __name__=='__main__':
    assert not ROOT.exists() and not OUTPUT.exists()
    doc=deepcopy(read(INPUT));font=read(FONT);oldfont=read(doc['native_font_proof'])
    assert font['source_original_progressive_caller_style']==11 and font['candidate_sha256']==doc['current_ROM_sha256']
    assert len(font['cases'])==17 and font['current_original_macro_alignment_calls']==136
    assert [r['encoded_hex'] for r in font['cases']]==[r['encoded_hex'] for r in oldfont['cases']]
    byid={r['id']:r for r in font['cases']}
    for r in doc['records']:
        assert r['compiled_hex']==byid[r['id']]['encoded_hex']
        r['native_font_case']=byid[r['id']]
        r['source_story_style11_native_reference']=r['kind']!='system-FE'
    doc.update(native_font_proof=str(FONT),native_font_proof_sha256=sha(FONT.read_bytes()),
        prior_native_approval_manuscript=str(INPUT),prior_native_approval_manuscript_sha256=sha(INPUT.read_bytes()),
        source_original_progressive_style_proof=font['source_original_progressive_style_proof'],
        source_original_progressive_style_proof_sha256=font['source_original_progressive_style_proof_sha256'],
        no_changed_prose_compiled_bytes_or_native_ROM_runtime=True)
    save(OUTPUT,doc);ROOT.mkdir(parents=True)
    save(ROOT/'unchanged17_targets_with_source_correct_story_style11.json',dict(manuscript=str(OUTPUT),manuscript_sha256=sha(OUTPUT.read_bytes()),
        previous=str(INPUT),previous_sha256=sha(INPUT.read_bytes()),font_proof=str(FONT),font_proof_sha256=sha(FONT.read_bytes()),
        all17_English_compiled_source_current_references_and_editorial_decisions_exact=True,
        corrected_native_reference_not_a_game_or_prose_fix=True,all_prior_evidence_preserved=True,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
    print('B198 v5 binds unchanged17 targets to original story style11. No text,control,ROM or runtime change;actual audit next.')
