"""Assemble all539 contextual decisions and bind fresh formatting to the current own runtime."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save
from scripts.generic_name_macro_owned_v5886b import expand as original_expand
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime

ROOT=Path('work/analysis/Rafael_B61_B80_clean_20261104')
OUT=Path('work/analysis/Rafael_B61_B80_formatting_20261104')
FINAL=Path('translations/rafael_B61_B80_contextual_editorial_manuscript_v1.json')
CURRENT=Path('work/analysis/Rafael_B61_B80_latest_runtime_20261104/all539_current_effective_qualified_v1.json')
RELEASE=Path('work/analysis/Rafael_B51_B60_release_verified_20261104/registered_release_verification.json')
MACROS=Path('work/analysis/Rafael_early_tutorial_B42_B43_source_display_20261104/40_native_selectors_macros_andcomplete_preamble_bindings.json')

if __name__=='__main__':
    assert not OUT.exists() and not FINAL.exists()
    parts=[ROOT/name for name in ['B61_B67_289_contextual_comparisons_latest_v1.json',
        'B69_B70_108_whole_exchange_comparison_v1.json','B71_B75_116_whole_exchange_comparison_v1.json',
        'B76_B80_26_whole_exchange_comparison_v1.json']]
    current=load(CURRENT);prior={r['id']:r for g in current['groups'] for r in g['records']}
    rows=[deepcopy(r) for p in parts for r in load(p)['records']]
    assert len(rows)==len(prior)==539 and len({r['id'] for r in rows})==539
    assert (sum(r['decision']=='revision' for r in rows),sum(r['decision']=='retention' for r in rows))==(210,329)
    nonascii=Counter(c for r in rows for c in r['english'] if ord(c)>127)
    assert set(nonascii)<={'…'},nonascii
    for row in rows:
        assert row['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False)
        assert all(row[k]==prior[row['id']][k] for k in ['source_reference','current_reference','source_hex','current_hex','source_complete_preamble_hex'])
        assert not any(t in row['english'] for t in ['\n','{LB','{ALIGN','{PAD}','Ｉ'])
        assert all(row['english'].count('{MACRO:'+m+'}')==bytes.fromhex(row['source_hex'])[1:].count(m.encode()) for m in ['FI','FA','FO','FU'])
        if '…' in row['english']:
            assert row['decision']=='retention' and row['english'].count('…')==prior[row['id']]['current_comparison_paragraph'].count('…')
        if row['id']=='DK4_MES_B75_R0075':
            row['finding']=row['finding'].replace('dueI','duel')
            row['localization_note']=row['finding']
        if row['id']=='DK4_MES_B78_R0024':
            row['finding']='Make the renewed rally natural and energetic with Let us contracted to Let\'s and the invitation to go, rather than a stiff proclamation.'
            row['localization_note']=row['finding']
        row.update(kind='system-FE' if row['source_selector']==254 else 'progressive',
            source_record_index=row['source_reference']['record_index'],source_native_extent=row['native_extent'],
            planned_English_markup='{SPEAKER:'+format(row['source_selector'],'02X')+'}'+row['english'],
            prior_macro_normalized_comparison=row['english'] if row['decision']=='retention' else None,
            current_ROM=current['current_ROM'],current_ROM_sha256=current['current_ROM_sha256'],
            current_English_comparison_pending=False,fresh_formatting_native_visual_stored_andrepresentative_gameplay_pending=True)
        if row['source_selector']==254:
            if row['block']==69:
                assert row['speaker']=='Charlotte Miller'
                row['FE_is_Charlotte_dialogue_not_system_speaker']=True
            else:
                assert row['id']=='DK4_MES_B61_R0113' and row['speaker']=='Military-funds notice'
                row['FE_is_source_military_funds_notice']=True
    assert sum(r['source_selector']==254 for r in rows)==6
    ctx=RegisteredRuntime(RELEASE,RELEASE.with_name('own_registered_startup_verification.json'),captain=0)
    qualification_path=Path('work/analysis/Rafael_B61_B80_latest_runtime_20261104/dependency_qualification.json')
    qualification=load(qualification_path)
    assert current['runtime']==qualification['runtime']==ctx.receipt()
    macros=load(MACROS)
    assert macros['macro_ascii_lengths']==dict(FI=6,FA=6,FO=10) and macros['selector00_native_actor_is_current_Rafael_captain']
    env=dict(original_expand.__globals__)
    exec(compile(macros['source_owned_progressive_adapter'],__file__+'::same-original-captain0-macro-ABI','exec'),env)
    default=ctx.execute(env['expand'],b'FI FA FO',0)
    assert len(default['cases'])==4 and all(r['output_hex']==b'Rafael Castor Castor Co.'.hex() for r in default['cases'])
    OUT.mkdir()
    proof_path=OUT/'own_default_macros_andsource_qualification_v1.json'
    save(proof_path,dict(runtime=ctx.receipt(),macro_ascii_lengths=dict(FI=6,FA=6,FO=10),
        own_native_default_macro_cases=default,selector00_current_actor_is_Rafael=True,
        source_dispatch_ABI_reused_by_exact_dependency_qualification=str(qualification_path),
        source_dispatch_ABI_reused_by_exact_dependency_qualification_sha256=sha(qualification_path.read_bytes()),
        previous_complete_preamble_macro_proof=str(MACROS),previous_complete_preamble_macro_proof_sha256=sha(MACROS.read_bytes()),
        five_FE_records_are_Charlotte_CG_dialogue_not_system_announcements=True,
        no_new_original_scene_CG_dispatch_gameplay_claim=True,new_credit=0,
        producer_sha256=sha(Path(__file__).read_bytes())))
    doc=dict(format='dk4-editorial-prose-packet-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        encoder='dialogue-relocatable-v1',file_path='/data/SC0.DK4',blocks=list(range(61,81)),
        current_ROM=current['current_ROM'],current_ROM_sha256=current['current_ROM_sha256'],current_archive_sha256=current['current_archive_sha256'],
        review_gates=['source','context','localization','naturalness','formatting'],records=rows,
        proposed_revisions=210,wording_retentions=329,complete_four_gate_comparisons=539,
        all_formatting_gates_false=True,physical_speech_objects=539,ordinary_speech_objects=534,FE_speech_objects=5,
        typed_choice_objects=0,typed_choice_commands=0,personality_alternatives=0,
        source_bound_existing_nonASCII_punctuation=dict(nonascii),
        scoped_fullwidth_I_fixes=sum(r['current_comparison_paragraph'].count('Ｉ') for r in rows),
        no_legacy_wraps_orpadding_copied=True,registered_release_andcompletion_credit_pending=True,
        own_default_macro_proof=str(proof_path),own_default_macro_proof_sha256=sha(proof_path.read_bytes()),
        all20_source_blocks_preserved_including_zero_speech_B68=True,
        new_credit=0,guide_photos=False,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [*parts,CURRENT,qualification_path,
            ROOT/'source_identity_event_andterm_checkpoint_v1.json',ROOT/'trade_house_andBamboo_Assembly_Plan_binding_v1.json',Path(__file__)]})
    assert doc['scoped_fullwidth_I_fixes']==16
    doc.update(ordinary_speech_objects=533,FE_speech_objects=6,Charlotte_FE_speech_objects=5,military_funds_FE_notices=1)
    save(FINAL,doc)
    save(OUT/'formatting_input.json',dict(**doc,source_full_manuscript=str(FINAL),source_full_manuscript_sha256=sha(FINAL.read_bytes())))
    save(OUT/'initial_preferences_v1.json',dict(records={},no_visual_findings_before_native_pages=True))
    print('Prepared all539 four-gate reviews:210 revisions/329 retentions/16 I fixes;533 progressive/five Charlotte FE/one funds FE;four own macro alignments. Fresh formatting pending.',flush=True)
