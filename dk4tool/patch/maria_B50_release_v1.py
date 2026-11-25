"""Pure cumulative B50 transaction with one source-owned FE continuation and 16 source credits."""
import inspect
from pathlib import Path
from dk4tool.patch import rafael_story_b81_b84_release_v1 as previous
from dk4tool.patch.market_goods_info_terminator_v1 import transform
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts.source_locked_derivation_v5118 import checked_text

load,sha=previous.load,previous.sha
def require(value,message):
    if not value:raise ValueError('Maria B50 release: '+message)

def qualify_evidence(conf,doc,reconstruction,stored):
    require((conf['record_count'],conf['speech_count'],conf['native_commands'],conf['native_pages'],conf['FE_count'],conf['typed_choice_count'],conf['style_count'])==(16,16,17,17,12,0,0), 'source/native panel membership')
    require(conf['captain']==3, 'current Maria context')
    require(conf['FE_owner_ID']=='DK4_MES_B50_R0043', 'exact single FE owner')
    ready=load(conf['research_completion'])
    require((ready['records'],ready['revisions'],ready['retentions'],ready['native_commands'],ready['native_pages'])==(16,9,7,17,17)
        and ready['all_individual_five_gates_pass'] and ready['registered_integration_pending'], '16 sealed five-gate reviews')
    require(ready['manuscript']==conf['manuscript'] and ready['manuscript_sha256']==sha(Path(conf['manuscript']).read_bytes()), 'sealed final manuscript')
    for p,h in ready['evidence'].items():require(sha(Path(p).read_bytes())==h, 'research dependency: '+p)
    sealed=load(conf['sealed_inputs'])
    require(sealed['research_completion_sha256']==sha(Path(conf['research_completion']).read_bytes()), 'sealed research identity')
    for key in ['manuscript','plan','reconstruction','stored_native','stored_lookup','loaders','compiled_native','actual','visual_review','scoped_names']:
        require(sealed['inputs'][key]==dict(path=conf[key],sha256=sha(Path(conf[key]).read_bytes())), 'sealed input: '+key)
    native,lookup,loaders,actual,visual,names=[load(conf[k]) for k in ['compiled_native','stored_lookup','loaders','actual','visual_review','scoped_names']]
    require(native['runtime']==stored['runtime']==lookup['runtime']==doc['runtime'] and native['runtime']['captain']==3, 'exact own Maria runtime')
    require(native['runtime']['candidate_sha256']==conf['parent_ROM_sha256'] and native['runtime']['ARM9_sha256']==conf['pre_runtime_ARM9_sha256'], 'exact current native parent')
    require(native['pages']==stored['complete_stored_pages']==visual['native_panels']==17 and visual['all17_final_panels_directly_viewed'], 'all17 viewed panels')
    require(visual['no_QA_waivers_or_prose_font_viewport_orengine_changes'] and native['all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass'] and native['complete_consumption_andpagination_exact'], 'unwaived native display checks')
    require(stored['reconstruction_sha256']==sha(Path(conf['reconstruction']).read_bytes()) and lookup['stored_sha256']==sha(Path(conf['stored_native']).read_bytes()), 'final storage identities')
    require(stored['all_stored_planes_equal_directly_viewed_compiled_planes'] and stored['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass'], 'all stored guards')
    require((stored['fresh_parity_dependent_pages'],stored['exact_compiled_pages_reused'],stored['fresh_relocated_native_relative_cases'])==(8,9,0), 'exact fresh/reused and absent-branch scope')
    require(lookup['all17_physical_bodies_checked'] and lookup['all_new_effective_bodies_byte_exact_before_original_macro_expansion'], 'all17 full native catalogue buffers')
    require((loaders['fresh_whole_archive_loads_andcache_hits'],loaders['fresh_parent_cases'],loaders['exact_reused_parent_cases'])==(303,606,0)
        and loaders['all_native_executed_instructions_current_ROM_exact'] and loaders['all_loaded_payloads_cache_metadata_neighbors_andparent_first_reads_exact'], 'complete SC3 loads/handoffs')
    physical={r['id']:r for r in native['records']};entries={r['id']:r for r in stored['records']}
    require(set(physical)==set(entries)=={r['id'] for r in lookup['records']} and len(physical)==17, 'complete physical membership')
    require(not stored['style_records'] and not stored['typed_objects'] and reconstruction['compound_objects']==0, 'exact zero compound scope')
    for row in native['records']:
        display=row['complete_native_English_display'];pages=[display] if row['kind']=='system-FE' else display['pages']
        require(len(pages)==1, 'one physical panel per native command')
        for page in pages:require(sha(Path(page['native_plane']).read_bytes())==page['native_plane_sha256'], 'exact viewed plane')
    require((actual['frames'],actual['initialized_runs'],actual['source_utterances_observed'],actual['native_commands_observed'],actual['native_body_pages_observed'],actual['offline_only_source_utterances'])==(13001,1,16,17,17,0), 'honest actual scope')
    require(actual['all17_native_panels_andboth_named_headers_complete_pixels_andblank_guards_match'] and actual['all17_body_pages_directly_viewed'], 'complete actual pixels')
    require(actual['source_owned_continuation_A_andfollowing_return_observed'] and actual['source_complete_QA_host_exit_to_resupply_andsailing_observed'], 'actual continuation/return/exit')
    require((actual['FE_first_panel_frame'],actual['FE_continuation_frame'],actual['following_source_FE_frame'],actual['ordinary_A_frames'])==(6185,6425,6665,[6400,6640]), 'source-bound ordinary A transitions')
    require(not any(actual[k] for k in ['natural_activation','original_location','earned_chronology','full_route','hardware']) and actual['original_B50_cutscene_art_effects_andevent_outcome_unvisited'], 'unvisited effects/chronology disclosed')
    for p,h in actual['evidence'].items():require(sha(Path(p).read_bytes())==h, 'actual dependency: '+p)
    for sheet in actual['review_sheets']:require(sha(Path(sheet['path']).read_bytes())==sheet['sha256'], 'directly viewed actual sheet')
    require(reconstruction['source_editorial_objects']==reconstruction['source_speeches']==16 and reconstruction['native_speech_commands']==reconstruction['complete_native_display_pages']==17, 'source versus native membership')
    require(len(reconstruction['seven_FE_pagination_invalid_cases_rejected'])==7 and reconstruction['source_owned_exact_FE_control_repeated_once'], 'all continuation rejects and exact control')
    require(reconstruction['all_original_scene_controls_andconditional_scopes_preserved'] and reconstruction['full_clean_current_block_archive_andserialized_NDS_inverses_exact'], 'whole scene and inverse')
    require(conf['scoped_name_IDs']==[3,10,28,74], 'four relevant scoped identities')
    validate_natural_dialogue_batch(names)
    name_rows={r['actor_ID']:r for r in names['records']}
    require(names['all28_individual_five_gates_pass_in_scoped_context'] and set(conf['scoped_name_IDs'])<=set(name_rows), 'inherited contextual name approvals')
    expected={3:'Maria Li',10:'Xien Yan',28:'James Clifford',74:'Richard Townsend'}
    for actor,text in expected.items():require(next(c['text'] for c in name_rows[actor]['current_consumers'] if c['consumer']=='progressive-nameplate')==text, 'approved source-bound name')
    old=previous.NdsImage.open(names['runtime']['candidate']);current=previous.NdsImage.open(conf['parent_ROM'])
    require(sha(Path(names['runtime']['candidate']).read_bytes())==names['runtime']['candidate_sha256'], 'inherited name runtime identity')
    arm,proof=transform(old.read_file('/__arm9__.bin'))
    require(arm==current.read_file('/__arm9__.bin') and proof['whole_serialized_parent_inverse_exact'], 'exact market transform preserves name/code data')
    require(current.read_file('/GRP/KANJI.FNT')==old.read_file('/GRP/KANJI.FNT') and current.read_file('/COMMON/MESFILE.DK4')==old.read_file('/COMMON/MESFILE.DK4'), 'exact name/macro/font dependencies')
    require(sha(current.read_file('/GRP/KANJI.FNT'))==native['font_sha256'], 'current font identity')
    require(max(g['target_bytes'] for g in reconstruction['groups'])<=9216, 'original allocation bound')
    require(not any(r.get('qa_waivers') for r in doc['records']), 'no record QA waivers')

source=checked_text(inspect.getsource(previous.plan_release),{
    "'dk4-rafael-B81-B84-release-v1'":"'dk4-reviewed-maria-B50-FE-release-v1'",
    "len(doc['records'])==len({r['id'] for r in doc['records']})==conf['record_count']==330":"len(doc['records'])==len({r['id'] for r in doc['records']})==conf['record_count']==16",
    "    doc,layout,reconstruction,stored,menu=[load(conf[k]) for k in ['manuscript','plan','reconstruction','stored_native','typed_menu']]":
        "    doc,layout,reconstruction,stored=[load(conf[k]) for k in ['manuscript','plan','reconstruction','stored_native']];menu={'menus':[]}",
    'len(speech)==len(plans)==325 and len(choices)==5':'len(speech)==len(plans)==16 and len(choices)==0',
    "[81,82,83,84],'four complete source exchanges'":"[50],'complete B50 source exchange'",
    "path=='/data/SC0.DK4'":"path=='/data/SC3.DK4'",'len(container.blocks)==len(original)==343':'len(container.blocks)==len(original)==303',
    "        rows=[r for r in speech if r['block']==number]":
        "        rows=[previous.deepcopy(r) for r in speech if r['block']==number]\n        for row in rows:row['current_record_index']=row['current_reference']['record_index']",
    "{'DK4_MES_B84_R0470','DK4_MES_B84_R0539'},'onlytwo qualified FE owners'":"{'DK4_MES_B50_R0043'},'exact single qualified FE owner'",
    'native_pages=336,native_commands=327,typed_labels=5':'native_pages=17,native_commands=17,typed_labels=0',
    'source_editorial_objects=330,fresh_relative_cases=140,native_loads=343,actual_frames=72406':'source_editorial_objects=16,fresh_relative_cases=0,native_loads=303,actual_frames=13001',
})
env={**previous.plan_release.__globals__,'previous':previous,'qualify_evidence':qualify_evidence,'require':require,'__file__':__file__}
exec(compile(source,__file__+'::same-source-owned-FE-transaction-complete-SC3-inverses-one-source-owner','exec'),env)
plan_release=env['plan_release']
