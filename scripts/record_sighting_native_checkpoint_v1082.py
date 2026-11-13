"""Approve native sighting drafts only;archive evidence without gameplay credit."""
from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from scripts.sighting_layout_v1069 import compiled,PROFILE
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/sighting_review_v1082')
SOURCE=Path('translations/sighting_editorial_manuscript_v5.json')
MANUSCRIPT=Path('translations/sighting_editorial_manuscript_v6.json')
ARCHIVE=Path('E:/Rota Nova translations/Editorial review/V1082 Sighting native review')
GENERATED=Path('E:/Rota Nova translations/Generated')


def main():
    assert not ROOT.exists() and not MANUSCRIPT.exists() and not ARCHIVE.exists()
    runtime_path=Path('work/analysis/sighting_runtime_v1076/native_runtime_verification.json')
    runtime=read(runtime_path)
    assert runtime['old_and_new_complete_scope_cases_each']==56696
    assert runtime['only_new_contract']=={'0x2053db8':[0x8540,0x8560]}
    assert runtime['all3668_modal_outputs_and_wrap_choices_exact'] and runtime['all140_status8MiB_ABI_guards_pass']
    for path,digest in runtime['all_completed_source_proofs'].items():assert sha(Path(path).read_bytes())==digest
    font_path=Path('work/analysis/sighting_fonts_v1080/native_font_proof.json');font=read(font_path)
    assert font['complete_native_font_cases']==2700 and font['changed_cases_rerendered']==180 and font['unchanged_cases_inherited_exact']==2520
    assert sha(SOURCE.read_bytes())==font['manuscript_sha256'] and sha(Path(font['matrix']).read_bytes())==font['matrix_sha256']
    assert runtime['research_ARM9_sha256']==font['research_ARM9_sha256']
    assert all(r['whole228x64_native_and_independent_font_match'] for r in font['cases'])
    prior=read(font['source_font_proof']);assert sha(Path(font['source_font_proof']).read_bytes())==font['source_font_proof_sha256']
    sheets=prior['review_sheets']+[{'path':font['new_review_sheet'],'sha256':font['new_review_sheet_sha256']}]
    for row in sheets:assert sha(Path(row['path']).read_bytes())==row['sha256']
    provider_path=Path('work/analysis/sighting_provider_v1068/provider_native_proof.json');provider=read(provider_path)
    assert len(provider['all81_original_getter_ABI_cases'])==81 and provider['owned_allocation_bytes']==9
    pilot_path=Path('work/analysis/contact_pilot_v1081/terminal_pilot_verification.json');pilot=read(pilot_path)
    assert pilot['complete_fixture_count']==1351 and pilot['terminal_frame']==10344
    assert pilot['successful_admiral_shot_not_observed_at_recorded_pauses_no_event_credit']
    doc=read(SOURCE);assert len(doc['records'])==15 and all(not r['review']['formatting'] for r in doc['records'])
    exemplar=doc['records'][0]
    unsafe=[]
    for english in (' '+exemplar['english'],exemplar['english']+' ',exemplar['english'].replace(' ','  ',1),
        exemplar['english'].replace(' ','\n',1),exemplar['english'].replace(' ','\r',1),
        exemplar['english'].replace(' ','\t',1),exemplar['english']+'{PAD}',exemplar['english']+'é',
        exemplar['english'].replace('%s','%d',1),exemplar['english']+' %s',exemplar['english']+' %',
        exemplar['english'].replace('%s','IC',1)):
        case={**exemplar,'english':english}
        try:compiled(case)
        except ValueError:unsafe.append({'english':english,'rejected':True})
        else:raise AssertionError('Unsafe native paragraph compiled')
    for patch in ({'message_id':613},{'source_family':'fleet-sighting-under-attack'},{'native_argument_count':1}):
        try:compiled({**exemplar,**patch})
        except ValueError:unsafe.append({'invalid_record_fields':patch,'rejected':True})
        else:raise AssertionError('Wrong native source contract compiled')
    assert len(unsafe)==15
    ROOT.mkdir(parents=True)
    review=ROOT/'visual_and_compiler_review.json'
    save(review,{'source_manuscript':str(SOURCE),'source_manuscript_sha256':sha(SOURCE.read_bytes()),
        'full_native_font_proof':str(font_path),'full_native_font_proof_sha256':sha(font_path.read_bytes()),
        'all_six_native_review_sheets_visually_inspected':sheets,
        'superseded627_from_the_vicinity_panels_not_approved_as_current_prose':True,
        'all_current15_paragraphs_read_aloud_against_clean_source_gloss_and_original_alternative_voice_context':True,
        'proper_compass_and_close_range_English_full_names_punctuation_letters_and_bounds_reviewed':True,
        'no_authored_alignment_manual_line_breaks_or_literal_I_plus_LF_before_macro_expansion':True,
        'fifteen_invalid_control_printf_and_source_contract_inputs_rejected':unsafe,
        'global_uppercase_weak_word_case_sensitivity_followup_remains_open':True,
        'registered_copy_ROM_patch_and_actual_scene_gates_remain_open':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    for row in doc['records']:
        compiled(row);row['review']['formatting']=True
        row['localization_note']+=' Native approval:all2700 two-argument layout/font cases,81 bearing-provider cases,full scoped selector/modal/status regressions and visual/read-aloud review pass. This does not approve registered insertion,copies,actual scene activation or the whole-game formatting audit.'
    doc.update(status='15-native-approved-source-prose-drafts;registered-copy-provider-ROM-patch-actual-pending',
        formatting_review_pending=False,consumer_layout_profile=PROFILE,
        supersedes_manuscript=str(SOURCE),supersedes_manuscript_sha256=sha(SOURCE.read_bytes()),
        native_font_proof=str(font_path),native_font_proof_sha256=sha(font_path.read_bytes()),
        native_runtime_proof=str(runtime_path),native_runtime_proof_sha256=sha(runtime_path.read_bytes()),
        native_provider_proof=str(provider_path),native_provider_proof_sha256=sha(provider_path.read_bytes()),
        visual_review=str(review),visual_review_sha256=sha(review.read_bytes()))
    save(MANUSCRIPT,doc)
    ledger_path=Path('translations/editorial_review_current_v1.json');ledger=read(ledger_path)
    assert ledger['records_editorially_completed']==1196 and ledger['records_with_source_and_prose_pass']==1234
    paths=ledger['active_source_prose_drafts']['manuscripts'];assert paths.count(str(SOURCE))==1
    paths[paths.index(str(SOURCE))]=str(MANUSCRIPT)
    ledger['newly_observed_sighting_followup'].update(manuscript=str(MANUSCRIPT),native_font_proof=str(font_path),
        native_runtime_proof=str(runtime_path),visual_review=str(review),pending_boundary_findings=0,
        status='15-native-approved;registered-copy-provider-ROM-patch-and-actual-scenes-pending',completed_entries_added=0)
    ledger['sighting_v1066']['current_manuscript']=str(MANUSCRIPT)
    ledger['contact_research_v1067'].update(status='terminal10344;1351-entire4MiB-fixtures-audited;successful-shot-not-observed-no-credit',
        terminal_proof=str(pilot_path),still_running=False)
    ledger['sighting_v1082']={'native_message_IDs':list(range(614,629)),'manuscript':str(MANUSCRIPT),
        'native_layout_and_font_cases':2700,'native_bearing_getter_cases':81,'native_runtime_proof':str(runtime_path),
        'registered_integration_and_actual_scenes_pending':True,'completed_entries_added':0}
    checkpoint='V1082 native-approves15 sighting paragraphs614-628 after2700 exact bearing/faction expansion/wrap/full-font cases and six visual/read-aloud sheets. Source preparation and already-attacked meanings,voice,full faction names and original argument order are preserved. A9-byte close-range vicinity provider passes81 native cases;two sighting tables gain balancing within unchanged212-byte public/128-byte modal spans and exact123040 staged bytes.56696 source plus56696 research selector/ABI cases,3668 prior modal outputs,238 wrong-parent5 full-word and140 whole-status guards pass. The terminal10344 cold-boot contact pilot has1351 independently audited entire4MiB fixture deltas and preserved saves;no successful-shot announcement was observed,so no20-entry event completion credit. A current-ROM 武装Latina label has a separate16-byte Armed Latina source draft;constructor/copies/integration/actual repair remain open.1196 complete,1234 source/prose;V997 current fully scene-verified,V1034 still pending. No new ROM or patch built. Sighting registered copies/provider integration/exact patch/actual scenes,global uppercase weak-word audit,remaining shared/routes/player prose/raw coverage and separate graphics audit remain open.'
    ledger['latest_checkpoint']=checkpoint;save(ledger_path,ledger)
    doc_path=Path('docs/sighting_v1082_native_checkpoint.md')
    doc_path.write_text('# V1082: native sighting review\n\n'+checkpoint+'\n\nThe frozen earlier drafts and their diagnostics remain available. Native faction stress caught a doubled period after Co.;read-aloud review replaced the unnatural from the vicinity phrasing. Complete readiness sentences preserve the source announcement without shortening the message for storage. All current paragraphs are one logical paragraph before macro expansion.\n\nThe terminal contact context explicitly restores both still-live vessels,own provisions and positive captain HP;it preserves actor identities and original RNG/result handling. The experiment is targeted headless emulator testing,not normal earned progression,a full route playthrough or hardware evidence.1351 declared deltas are independently reconstructed and native terrain is rechecked in a batch. Two ordinary capture notices exposed the mixed ship name. A normal No declined the monthly report before clean terminal stop. The successful-shot gate remains unverified.\n\nNext:registered native-copy/repack/provider integration and exact clean-input patch for the15 sighting paragraphs;then actual original sighting,attack,close-range,name/bounds/dismissal/transition verification. The successful-shot event in V1034 remains a separate open family;do not promote that20-entry batch or the canonical baseline based on this checkpoint.\n',encoding='utf8')
    for path in ('docs/translation_progress.md','docs/todo.md'):
        with Path(path).open('a',encoding='utf8') as f:f.write('\n\n## V1082: sighting native review\n\n'+checkpoint+'\n')
    with Path('docs/known_issues.md').open('a',encoding='utf8') as f:
        f.write('\n\n## V1082: open shared formatting and mixed-name findings\n\nThe native weak-word hash scan is case-sensitive;uppercase A may remain at a line end (COMMON618 evidence in sighting_layout_v1073). The current15 drafts use complete natural sentences and pass their matrix,but the global formatter issue is not repaired. Current V1034 ARM9 offset15E0A4 also contains 武装Latina,and it actually appears in an original ship-capture notice;Armed Latina fits the same16-byte allocation. Constructor/copy/integration/actual repair remain pending. The close-range bearing still reads 至近距離 in the playable ROM;the9-byte vicinity replacement is research/native-approved only. See sighting_v1082_native_checkpoint.md.\n')
    ARCHIVE.mkdir(parents=True);files=[]
    names=['native_contact_live_geometry_v1062','run_reinforcement_regional_live_v1063','drive_contact_probe_v1064',
        'research_sighting_context_v1065','prepare_sighting_prose_v1066','record_sighting_contact_checkpoint_v1067',
        'probe_close_bearing_provider_v1068','sighting_layout_v1069','probe_sighting_layout_v1070',
        'sighting_runtime_v1071','probe_sighting_balanced_layout_v1072','prepare_sighting_readiness_v1073',
        'prepare_sighting_sentence_v1074','probe_sighting_fonts_v1075','verify_sighting_runtime_v1076',
        'drive_contact_probe_v1077','inventory_armed_latina_v1078','prepare_sighting_readaloud_v1079',
        'probe_sighting_font_delta_v1080','verify_contact_pilot_v1081','record_sighting_native_checkpoint_v1082']
    paths=[Path('scripts')/(name+'.py') for name in names]+[doc_path,ledger_path,MANUSCRIPT,SOURCE,
        Path('translations/sighting_editorial_manuscript_v1.json'),Path('translations/sighting_editorial_manuscript_v2.json'),
        Path('translations/sighting_editorial_manuscript_v3.json'),Path('translations/sighting_editorial_manuscript_v4.json'),
        Path('docs/translation_progress.md'),Path('docs/todo.md'),Path('docs/known_issues.md'),
        Path(pilot['terminal_report']),Path('work/analysis/reinforcement_sniping_v1063/terminal_preservation.json')]
    for folder in ('sighting_editorial_v1065','sighting_editorial_v1066','sighting_provider_v1068','sighting_layout_v1070',
        'sighting_layout_v1072','sighting_layout_v1073','sighting_layout_v1074','sighting_fonts_v1075','sighting_runtime_v1076',
        'armed_latina_v1078','sighting_layout_v1079','sighting_fonts_v1080','contact_pilot_v1081','sighting_review_v1082'):
        paths.extend(Path('work/analysis',folder).rglob('*'))
    seen=set()
    for source in paths:
        if not source.is_file() or source.absolute() in seen:continue
        seen.add(source.absolute())
        if source.absolute().is_relative_to(Path.cwd()):relative=source.absolute().relative_to(Path.cwd())
        else:relative=Path('Generated')/source.absolute().relative_to(GENERATED)
        target=ARCHIVE/relative;target.parent.mkdir(parents=True,exist_ok=True);copy2(source,target)
        assert sha(source.read_bytes())==sha(target.read_bytes())
        files.append({'source':str(source),'archived':str(target),'sha256':sha(target.read_bytes())})
    save(ARCHIVE/'archive_manifest.json',{'files':files,'native_approved_only_no_new_ROM_or_completed_entries':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    save(ROOT/'archive_receipt.json',{'archive':str(ARCHIVE),'files':len(files),
        'manifest_sha256':sha((ARCHIVE/'archive_manifest.json').read_bytes()),'no_editorial_completion_credit':True})
    print('V1082:15 native-approved drafts,2700 complete fonts,terminal pilot audit and open findings archived.1196 complete,1234 source/prose;goal incomplete.',flush=True)


if __name__=='__main__':main()
