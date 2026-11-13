"""Prepare48 format approvals withviewed-sheet ancestry andemote/thought checks."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    old=Path('scripts/approve_lil_B135_B136_native_v3360.py');new=Path('scripts/approve_lil_B137_native_v3398b.py');assert not new.exists();t=old.read_text(encoding='utf-8')
    changes={
      'lil_B135_B136_native_approval_v3360':'lil_B137_native_approval_v3398b',
      'lil_B135_B136_editorial_manuscript_v4':'lil_B137_editorial_manuscript_v6',
      'lil_B135_B136_editorial_manuscript_v5':'lil_B137_editorial_manuscript_v7',
      'lil_B135_B136_fonts_v3359':'lil_B137_fonts_v3397c',
      'work/analysis/lil_B135_B136_visual_refinement_v3358/all5_viewed_native_sheets_and_phrase_findings.json':'work/analysis/lil_B137_name_prompt_refinement_v3397/viewed_successors_and_final_name_prompt_finding.json',
      'lil_B135_B136_layout_v2':'lil_B137_layout_v3','lil_B135_B136_profile':'lil_B137_profile',
      "len(font['cases'])==35":"len(font['cases'])==48","font['current_original_macro_alignment_calls']==280":"font['current_original_macro_alignment_calls']==384",
      "len(font['negative_controls'])==21":"len(font['negative_controls'])==31",'==(5,30)':'==(3,45)',
      "old=read(font['reused_proof']);assert visual['all5_progressive_sheets_viewed'];sheets=[]":"old=read(visual['previous_proof']);assert sha(Path(visual['previous_proof']).read_bytes())==visual['previous_proof_sha256'] and visual['all6_previous_progressive_sheets_viewed_or_hash_identical'];sheets=[]",
      'changed=={2,3,4,5}':'changed=={4}',"for v in visual['sheets']":"for v in visual['previous_sheets']",
      'len(sheets)==5':'len(sheets)==6',"{'revise':16,'retain-wording':19}":"{'revise':22,'retain-wording':26}",
      "for r in doc['records'])==15":"for r in doc['records'])==18",
      'all35_native_macro_font_and_source_reconciliation':'all48_native_macro_font_and_source_reconciliation',
      'current_original_macro_alignment_calls=280':'current_original_macro_alignment_calls=384',
      'all35_current_native_speech_planes_pass':'all48_current_native_speech_planes_pass',
      "Path('work/analysis/lil_B135_conditional_refinement_v3358c/finding_and_successors.json')":"Path('work/analysis/lil_B137_timing_complaint_refinement_v3393c/finding_and_successors.json')",
      'one_registered_Camille_effective_current_wording_retained=True':'zero_registered_catalogue_replacements_provenance_preserved=True',
      'chart_cheese_tart_joke_reviewed_as_complete_exchange=True':'nested_rating_joke_private_thought_wordless_shock_and_fivefold_wages_reviewed=True',
      'all35_five_review_gates_true':'all48_five_review_gates_true','progressive_planes=35':'progressive_planes=48','current_macro_alignment_cases=280':'current_macro_alignment_cases=384','source_consumer_negatives=21':'source_consumer_negatives=31',
      'narrow_row_count_notes=15':'narrow_row_count_notes=18','revised=16,retained=19':'revised=22,retained=26','actual_selected_B135_B136_IDs':'actual_selected_B137_IDs',
    }
    for a,b in sorted(changes.items(),key=lambda kv:-len(kv[0])):assert a in t,a;t=t.replace(a,b)
    a='    negatives=[]\n';assert a in t;t=t.replace(a,"""    shock=byid['DK4_MES_B137_R0276'];visible=[e for e in shock['complete_glyph_events'] if e['code']!=32]
    assert bytes.fromhex(shock['encoded_hex'])==bytes([2,33]) and [(e['code'],e['x'],e['y']) for e in visible]==[(33,0,0)]
    thought=bytes.fromhex(byid['DK4_MES_B137_R0231']['expanded_hex']);assert thought.startswith(b'(Wow, Lil!') and thought.endswith(b')') and thought.count(b'(')==thought.count(b')')==1
    negatives=[]
""")
    t=t.replace('all48_current_native_speech_planes_pass=True,','all48_current_native_speech_planes_pass=True,source_wordless_exclamation_complete_at_origin_and_private_thought_parentheses_verified=True,')
    t=t[:t.rindex('    print(')]+"    print('All48 fivegates pass:22revisions/26retentions,48planes/384macro cases,31consumer/14formatter negatives,sixviewed/hash-exact sheets. Wordlessshock andprivate-thought markers verified;relocation/release pending.')\n"
    compile(t,str(new),'exec');new.write_text(t,encoding='utf-8');root=Path('work/analysis/lil_B137_approval_tools_v3398');root.mkdir(parents=True);save(root/'provenance.json',dict(previous=str(old),previous_sha256=sha(old.read_bytes()),successor=str(new),successor_sha256=sha(new.read_bytes()),producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
