"""Bind 175 clean meanings, source event context and the new full-name macro risk."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load,save
from scripts.prove_papal_trade_entries_v7628 import parse_events
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.generic_name_macro_owned_v5886b import expand as original_expand

ROOT=Path('work/analysis/Rafael_early_story_B36_B41_B51_B60_clean_20261104')
NAMES=Path('work/analysis/Rafael_B36_B41_new_name_bindings_20261104/names.json')
PRIOR_NAMES=Path('work/analysis/Rafael_early_tutorial_B42_B43_current_name_planes_20261104/native_name_planes.json')
MACROS=Path('work/analysis/Rafael_early_tutorial_B42_B43_source_display_20261104/40_native_selectors_macros_andcomplete_preamble_bindings.json')
RELEASE=Path('work/analysis/Hodram_B191_B210_release_verified_20261104/registered_release_verification.json')
STARTUP=Path('work/analysis/Rafael_early_tutorial_registered_context_20261104/registered_Rafael_context_v1.json')

if __name__=='__main__':
    output=ROOT/'B36_B41_175_complete_clean_meanings_v1.json'
    checkpoint=ROOT/'B36_B41_source_identity_andFU_checkpoint_v1.json'
    assert not output.exists() and not checkpoint.exists()
    paths=[ROOT/'B36_B37_92_clean_meanings_v1.json',ROOT/'B38_B41_83_clean_meanings_v1.json']
    rows=[r for p in paths for r in load(p)['records']]
    packet_path=ROOT/'clean_source_packet.json'
    packet=load(packet_path)
    groups=[g for g in packet['groups'] if g['block'] in range(36,42)]
    assert len(rows)==175 and len({r['id'] for r in rows})==175
    assert {r['id'] for r in rows}=={r['id'] for g in groups for r in g['records']}
    ledger_path=Path('translations/editorial_review_current_v1.json')
    ledger=load(ledger_path)
    keys={(r['file_path'],r['id']) for r in ledger['contextual_story_natural_dialogue_pass_v1871']['record_keys']}
    assert ledger['records_editorially_completed']==10306 and not any((r['file_path'],r['id']) in keys for r in rows)
    clean=NdsImage.open('work/clean.nds')
    ev=clean.read_file('/data/EV0.DK4')
    events=parse_events(ev)
    source_events=[]
    for group in groups:
        selected=[r for r in events if r['script_block']==group['block']]
        dependencies={v for r in selected for v in r['must_be_completed']+r['must_not_be_completed'] if v!=65535}
        source_events.append(dict(block=group['block'],events=selected,prerequisite_records=[r for r in events if r['event_ID'] in dependencies],
            numeric_block_order_not_chronology=True,natural_eligibility_andactual_activation_unvisited=True))
    names,old_names=map(load,[NAMES,PRIOR_NAMES])
    ctx=RegisteredRuntime(RELEASE,STARTUP,captain=0)
    assert names['runtime']==old_names['runtime']==ctx.receipt()
    assert names['actors']==[8,31,34,51,75,151,153]
    consumers=names['current_names']['rows']+old_names['consumer_bindings']
    actors=sorted({r['source_selector'] for r in rows})
    assert actors==[0,4,5,6,8,31,34,51,75,151,153]
    assert len(consumers)==22 and {r['actor_ID'] for r in consumers}==set(actors)
    full={r['actor_ID']:r for r in names['current_names']['rows'] if r['consumer']=='full-catalogue'}
    assert full[31]['text']=='Pedro デ Valdes' and full[34]['text']=='Barbarossa Ｆazul Hayreddin'
    pending=[dict(actor_ID=31,consumer='full-catalogue',current_text=full[31]['text'],proposed_text='Pedro de Valdes',
        source_name=next(r['text'] for r in names['clean_names']['rows'] if r['actor_ID']==31 and r['consumer']=='full-catalogue'),
        finding='The source particle デ remains Japanese in an otherwise localized Spanish name. Bind its exclusive middle-name field and all consumers before replacing it with de.'),
        dict(actor_ID=34,consumer='full-catalogue',current_text=full[34]['text'],proposed_text='Barbarossa Fazul Hayreddin',
        source_name=next(r['text'] for r in names['clean_names']['rows'] if r['actor_ID']==34 and r['consumer']=='full-catalogue'),
        finding='The inherited middle name uses full-width Ｆ alongside ASCII az ul. Preserve the established Fazul wording while qualifying its ASCII F and complete native name consumers.')]
    macros=load(MACROS)
    assert macros['runtime']==ctx.receipt()
    env=dict(original_expand.__globals__)
    exec(compile(macros['source_owned_progressive_adapter'],__file__+'::same-native-macro-ABI-distinct-FU','exec'),env)
    samples=[]
    for body,expected in [(b'FU',b'Rafael Castor'),(b'FI FA FO FU',b'Rafael Castor Castor Co. Rafael Castor')]:
        proof=ctx.execute(env['expand'],body,0)
        assert len(proof['cases'])==4 and all(c['output_hex']==expected.hex() for c in proof['cases'])
        samples.append(dict(input_hex=body.hex(),expected_hex=expected.hex(),native=proof))
    save(output,dict(format='dk4-clean-complete-exchange-meanings-v1',file_path='/data/SC0.DK4',blocks=list(range(36,42)),records=rows,
        source_meanings_saved=175,complete_clean_source_packet=str(packet_path),complete_clean_source_packet_sha256=sha(packet_path.read_bytes()),
        constituent_glosses={str(p):sha(p.read_bytes()) for p in paths},source_EV0_sha256=sha(ev),source_event_context=source_events,
        all175_meanings_saved_before_current_English_dialogue_comparison=True,current_English_bodies_not_extracted=True,
        completed_coverage_overlap=0,source_coverage_check_ledger_sha256=sha(ledger_path.read_bytes()),
        remaining_preserved_clean_blocks=list(range(51,61)),remaining_preserved_source_speeches=245,
        early_story_priority_not_claim_of_all_six_early_activation=True,B40_later_rematch_identified=True,new_credit=0,guide_photos=False))
    save(checkpoint,dict(runtime=ctx.receipt(),source=str(output),source_sha256=sha(output.read_bytes()),actors=actors,
        native_identity=str(NAMES),native_identity_sha256=sha(NAMES.read_bytes()),four_exact_reused_actors=str(PRIOR_NAMES),
        four_exact_reused_actors_sha256=sha(PRIOR_NAMES.read_bytes()),fresh_clean_getters=14,fresh_current_getters=14,exact_reused_current_getters=8,
        current_consumer_bindings=[{k:r[k] for k in ['actor_ID','consumer','text','text_hex']} for r in consumers],
        source_FU_record='DK4_MES_B37_R0099',default_macro_lengths=dict(FI=6,FA=6,FO=10,FU=13),default_macro_widths=dict(FI=36,FA=36,FO=60,FU=78),
        FU_native_samples=samples,FU_fresh_alignment_cases=8,FU_expands_complete_full_name_not_first_name=True,
        full_name_only_artifact_findings=pending,native_selectors_andall_unowned_snapshot_bytes_preserved=True,
        both_name_field_corrections_andfresh_font_planes_allocation_andcatalogue_gameplay_pending=True,
        metadata_name_binding_not_new_scene_coverage=True,full_catalogue_UI_not_observed=True,
        localized_English_drafts_current_comparisons_full_preambles_andformatting_pending=True,
        initial_voice_helper_rejected_stale_captain1_assumption_successor_requires_captain0=True,
        all175_current_dialogue_bodies_unread=True,new_credit=0,guide_photos=False,
        evidence={str(p):sha(p.read_bytes()) for p in [packet_path,*paths,NAMES,PRIOR_NAMES,MACROS,RELEASE,STARTUP,Path(__file__)]}))
    print('175 complete clean meanings/11 bound identities/22 name consumers;FU full-name13 measured in8 alignments;two name artifacts queued.')
