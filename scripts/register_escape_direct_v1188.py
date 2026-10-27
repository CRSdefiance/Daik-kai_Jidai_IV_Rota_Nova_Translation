"""Register a bounded formatter successor, retaining complete V1166 ancestry."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch import escape_direct_formatting as owned
from scripts.escape_direct_runtime_v1183b import apply
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/escape_direct_release_v1188')
PROFILE='all-routes-unified-v1189'
MANUSCRIPT=Path('translations/duel_editorial_manuscript_v5.json')


def main():
    assert not ROOT.exists() and not Path(owned.CONFIG).exists() and not MANUSCRIPT.exists()
    prior_path=Path('translations/duel_editorial_manuscript_v4.json');prior=read(prior_path)
    runtime_path=Path('work/analysis/escape_direct_runtime_v1184c/native_runtime_verification.json')
    font_path=Path('work/analysis/escape_direct_fonts_v1185/native_direct_escape_fonts.json')
    pipeline_path=Path('work/analysis/escape_direct_source_v1186c/original_direct_pipeline.json')
    runtime,fonts,pipeline=map(read,(runtime_path,font_path,pipeline_path))
    assert runtime['all122324_exact_dispatch_ABI_cases'] and runtime['all140_status_whole8MiB_guards_exact']
    assert len(fonts['cases'])==1417 and len(pipeline['all13_direct_pipeline_cases'])==13
    doc=deepcopy(prior)
    doc.update(supersedes_manuscript=str(prior_path),supersedes_manuscript_sha256=sha(prior_path.read_bytes()),
        escape_font_proof=str(font_path),escape_font_proof_sha256=sha(font_path.read_bytes()),
        native_runtime_proof=str(runtime_path),native_runtime_proof_sha256=sha(runtime_path.read_bytes()),
        direct_escape_source_pipeline=str(pipeline_path),direct_escape_source_pipeline_sha256=sha(pipeline_path.read_bytes()),
        direct_escape_review_sheet_visually_inspected={'path':fonts['review_sheet'],'sha256':fonts['review_sheet_sha256'],
            'complete_words_first_last_letters_uniform_row_margins_and_bounds':True,'scope':'CPU native-font sheet; actual gameplay remains pending'},
        direct_escape_binding_erratum='V1166 gameplay1973 splits Everyone: actual original parent02053F40/table+274 differs from the old manual53DB8/+27C CPU frame. V5 retains all33 source/prose/compiled bytes and replaces escape native-format evidence with the proven direct caller. Original gameplay verification is still separate and incomplete.',
        actual_escape_gameplay_verified=False,full_goal_complete=False)
    assert [(r['message_id'],r['english'],r['source_meaning'],r['compiled_hex']) for r in doc['records']]==[
        (r['message_id'],r['english'],r['source_meaning'],r['compiled_hex']) for r in prior['records']]
    assert all(all(row['review'].values()) for row in doc['records'])
    registry_path=Path('translations/release_stack.json');builder=Path('scripts/build_integrated_release.py')
    registry=read(registry_path);registry_before=registry_path.read_bytes();before=builder.read_bytes()
    assert PROFILE not in registry['profiles']
    anchor=b'    # Lexically valid "% o"'
    assert before.count(anchor)==1 and b"profile_config.get('escape_direct_formatting')" not in before
    block=b'''    escape_direct_formatting = profile_config.get('escape_direct_formatting')
    if escape_direct_formatting:
        from dk4tool.patch.escape_direct_formatting import apply_release as apply_escape_direct_formatting

        arm_path = '/__arm9__.bin'
        final_arm, escape_direct_report = apply_escape_direct_formatting(
            candidate.read_file(arm_path), escape_direct_formatting)
        candidate.replace_file(arm_path, final_arm)
        grouped.setdefault(arm_path, [])
        relocation_checks.setdefault(arm_path, {})['escape_direct_formatting'] = {
            'release_config': escape_direct_formatting,
            'release_config_sha256': sha256(Path(escape_direct_formatting).read_bytes()),
            'proof': escape_direct_report}
        changed_records.setdefault(arm_path, []).append('DIRECT_ESCAPE_PORTRAIT_SCOPE_AND_PRESERVED_STATUS_LITERAL')

'''
    at=before.index(anchor);after=before[:at]+block+before[at:]
    assert after.replace(block,b'',1)==before;compile(after,str(builder),'exec')
    rom=NdsImage.open('out/all_routes_combined_v1166_candidate.nds');arm=rom.read_file('/__arm9__.bin')
    target,plan=apply(arm)
    assert sha(target)==runtime['target_ARM9_sha256']==fonts['ARM9_sha256']==pipeline['ARM9_sha256']
    ROOT.mkdir(parents=True);save(MANUSCRIPT,doc)
    (ROOT/'target_ARM9.bin').write_bytes(target);save(ROOT/'runtime_plan.json',plan)
    extras=[str(Path(__file__)),str(MANUSCRIPT),str(runtime_path),str(font_path),str(pipeline_path),
        'translations/duel_editorial_release_v1.json','dk4tool/patch/escape_direct_formatting.py',
        'scripts/escape_direct_runtime_v1183.py','scripts/escape_direct_runtime_v1183b.py',
        'scripts/verify_escape_direct_runtime_v1184.py','scripts/verify_escape_direct_runtime_v1184b.py',
        'scripts/verify_escape_direct_runtime_v1184c.py','scripts/probe_escape_direct_fonts_v1185.py',
        'scripts/probe_escape_direct_source_v1186.py','scripts/probe_escape_direct_source_v1186c.py',str(prior_path),fonts['review_sheet'],
        'work/analysis/escape_direct_frame_v1182/original_direct_frame_contract.json',
        'work/analysis/escape_direct_runtime_v1184c/runtime_plan.json',
        *runtime['proofs']]
    config={'format':'dk4-escape-direct-formatting-v1','source_arm9_sha256':sha(arm),'target_arm9_sha256':sha(target),
        'manuscript':str(MANUSCRIPT),'font_proof':str(font_path),'source_pipeline_proof':str(pipeline_path),
        'runtime_plan':'work/analysis/escape_direct_runtime_v1184c/runtime_plan.json',
        'dependencies':{name:sha(Path(name).read_bytes()) for name in dict.fromkeys(extras)}}
    save(owned.CONFIG,config);assert owned.apply_release(arm,owned.CONFIG)[0]==target
    (ROOT/'registry_before_raw.json').write_bytes(registry_before);save(ROOT/'registry_before.json',registry)
    (ROOT/'builder_before.py').write_bytes(before);(ROOT/'builder_added_optional_stage.bin').write_bytes(block)
    assert builder.read_bytes()==before and registry_path.read_bytes()==registry_before
    builder.write_bytes(after)
    profile=deepcopy(registry['profiles']['all-routes-unified-v1166'])
    profile.update(escape_direct_formatting=owned.CONFIG,status='experimental',
        description='Complete V1166 stack plus source-proven direct escape caller and preserved status constant.',
        note='No prose or COMMON changes;122324 scope/1417 fonts/13 original source-call CPU cases; actual defeat replay and startup/exact patch pending. Historical V1166 escape formatting approval superseded; no completion credit.')
    registry['profiles'][PROFILE]=profile;save(registry_path,registry)
    save(ROOT/'registration_provenance.json',{'profile':PROFILE,'source_profile':'all-routes-unified-v1166',
        'builder_before_sha256':sha(before),'builder_after_sha256':sha(after),
        'prior_builder_restored_by_removing_exact_optional_block':True,
        'registry_before_sha256':sha(registry_before),'registry_after_sha256':sha(registry_path.read_bytes()),
        'all_previous_profiles_and_accepted_layers_preserved':True,'prose_and_COMMON_unchanged':True,
        'source_ARM9_sha256':sha(arm),'target_ARM9_sha256':sha(target),
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('V1189 experimental profile registered; no completion credit.',flush=True)


if __name__=='__main__':main()
