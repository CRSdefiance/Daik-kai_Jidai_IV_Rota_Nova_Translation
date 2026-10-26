"""Checkpoint seven fresh rereads/native passes without completion credit."""
from pathlib import Path
from copy import deepcopy
from shutil import copy2
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.refit_contextual_spritsail_v1 import current_entries
from dk4tool.rom.nds import NdsImage
from scripts.reinforcement_sniping_layout_v1024 import compiled
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/admiral_shot_checkpoint_v2660')
OLD = Path('translations/admiral_shot_contextual_editorial_manuscript_v1.json')
DOC = Path('translations/admiral_shot_contextual_editorial_manuscript_v2.json')
FONT = Path('work/analysis/admiral_shot_fonts_v2658/native_font_proof.json')
GATE = Path('work/analysis/admiral_shot_gate_v2659/original_gate_focused_tests.json')
IDS = list(range(1924,1931))
FAMILY = 'Lookout-admiral-shot7-contextual-native-pending-transition'
SUMMARY = (
    'V2660 freshly rereads seven unfinished Lookout reports, COMMON1924-1930, from clean Japanese and the complete original event context. '
    'Each reports a successful shot at the enemy admiral and our victory. Existing English is retained with seven individual glosses and reasons: '
    'professional, exuberant, composed, clipped, familiar older-style, playful and polite emphatic voices remain distinct. '
    'No death, execution, weapon class, wound severity, reward, relationship or new rank is invented. '
    'The seven are alternative reports, not sequential replies; storage neighbors are context only. '
    'Exact source/current record references, registered compiler and owner pins reconcile. '
    'Seven complete current native228x64 font planes equal independent whole-plane and historical-reference masks; '
    'ordered first/final/interior glyphs, blank paper, x6 margins, 35-cell/four-row bounds, 16px stride and compiler-owned guards pass. '
    'All seven previews were viewed. Eight whole current original role7 speech pipelines cover every voice and original voice1 fallback; '
    'one uses unchanged actual fallback Gerhard16 and seven use isolated one-duty-byte original-setter fixtures. '
    'All executed pipeline instructions are current-exact and original actor models remain unchanged. '
    'Fourteen cold/warm copies and fourteen invalid compiler inputs pass. '
    'Original chance eligibility calls8235C(duty,7,6,0), using the physical job and adjusted actor metric, not the logical fallback speaker or bare actor stat. '
    'The preserved covering-fire snapshot has no assigned Lookout and returns zero. '
    'Three original exclusion paths, three threshold exclusions and twenty isolated post-RNG arithmetic comparisons pass with all main4MiB unchanged. '
    'Arithmetic cases stop before the shot effect and make no original RNG or actual eligibility claim. '
    'The distinct shot effect, held-message dismissal and post-shot outcome transition remain pending focused reconciliation; '
    'source disassembly and the old dispatch-only fragment do not establish that transition. '
    'Reuse exact source-bound role7/portrait and battle-result representative evidence where applicable; individual activation of every alternative is unnecessary. '
    'No new emulator run, gameplay shot, earned assignment, current startup, full-route or hardware proof is claimed. '
    'Fresh coverage is2150 reread /2143 integrated-reconciled /7pending. All2143 historical completions remain freshly reconciled. '
    'Historical completion2143(1498revised,645retained), source/prose2259 and incompleteCOMMON116 remain unchanged; '
    'these seven already belonged to source/prose2259 and gain no duplicate credit. '
    'Registered experimental cumulativeV2284 remains493batches/114accepted layers with its existing exactly reconstructable clean-input patch. '
    'ROM, runtime, registry, profile, manifest, geometry and patch are unchanged. V1492 remains promoted; all ROMs and earlier translations are preserved. '
    'Every unfinished and never-reviewed storyline, shared shop/town dialogue, random scene and remaining player-facing prose stays in scope. '
    'Separate graphics/all18 plaques, raw rejected-record coverage, SC3B109 classification and later older-record technical re-audit remain open. '
    'Full goal active; all jobs terminal.'
)

if __name__ == '__main__':
    assert not ROOT.exists() and not DOC.exists()
    lp = Path('translations/editorial_review_current_v1.json')
    prior_audit_path = Path('work/analysis/editorial_handoff_verification_v2655/verified_handoff.json')
    prior_audit = read(prior_audit_path)
    ledger = read(lp)
    assert sha(lp.read_bytes()) == prior_audit['ledger_sha256']
    fresh = ledger['contextual_story_natural_dialogue_pass_v1871']
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release']) == (2143,2143,0)
    assert set(IDS) <= set(ledger['reviewed_but_incomplete_COMMON_IDs'])
    doc = deepcopy(read(OLD)); font,gate = read(FONT),read(GATE)
    assert font['manuscript_sha256'] == sha(OLD.read_bytes())
    assert len(font['cases']) == 7 and len(font['all8_original_role7_speech_pipelines']) == 8
    assert len(font['all14_cold_warm_copies']) == len(font['invalid_compiler_inputs_rejected']) == 14
    assert font['findings'] == [] and font['all_executed_pipeline_instructions_current_ROM_byte_exact']
    assert len(gate['exclusion_cases']) == len(gate['threshold_cases']) == 3 and len(gate['post_RNG_arithmetic_cases']) == 20
    assert sha(Path(font['review_sheet']).read_bytes()) == font['review_sheet_sha256']
    for case in font['cases']:
        assert sha(Path(case['preview']).read_bytes()) == case['preview_sha256']
    image = NdsImage.open(doc['current_ROM'])
    arm,common = image.read_file('/__arm9__.bin'),image.read_file('/COMMON/MESFILE.DK4')
    entries = current_entries(common,arm)
    manifest_path = Path(doc['current_ROM']).with_suffix('.manifest.json')
    manifest = read(manifest_path)
    stage = manifest['relocations']['/COMMON/MESFILE.DK4']['reinforcement_sniping_editorial']
    cp = Path(stage['release_config']); config = read(cp); mp = Path(config['manuscript'])
    assert sha(cp.read_bytes()) == stage['release_config_sha256']
    assert sha(mp.read_bytes()) == config['manuscript_sha256']
    assert set(IDS) <= set(stage['proof']['reviewed_native_IDs'])
    for row in doc['records']:
        n = row['message_id']; assert compiled(row) == entries[n].text
        row['review']['formatting'] = True
        row.update(status='current-native-formatting-checked;distinct-transition-and-final-reconciliation-pending',
            current_native_case=next(c for c in font['cases'] if c['message_ID'] == n),
            new_current_visit=False,completion_credit_added=0)
    doc.update(formatting_review_pending=False,current_native_font_proof=str(FONT),current_native_font_proof_sha256=sha(FONT.read_bytes()),
        focused_original_gate_proof=str(GATE),focused_original_gate_proof_sha256=sha(GATE.read_bytes()),
        all_seven_native_previews_viewed=True,prior_contextual_draft=str(OLD),prior_contextual_draft_sha256=sha(OLD.read_bytes()),
        status='contextual-and-current-native-checked;distinct-transition-pending',
        distinct_post_shot_transition_pending=True,current_native_and_representative_transition_reconciliation_pending=True)
    validate_natural_dialogue_batch(doc)
    releasepath = Path('work/analysis/refit_spritsail_release_v2285b/registered_release_verification.json')
    release = read(releasepath)
    assert sha(Path(doc['current_ROM']).read_bytes()) == release['candidate_sha256'] == doc['current_ROM_sha256']
    assert sha(arm) == release['ARM9_sha256'] and sha(common) == release['COMMON_sha256']
    assert sha(manifest_path.read_bytes()) == release['manifest_sha256']
    assert sha(Path(release['patch']).read_bytes()) == release['patch_sha256'] and release['whole_ROM_reconstruction_byte_exact']
    docs = [Path('docs')/name for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']]
    assert docs[0].read_text().startswith('# Current editorial handoff - V2654')
    ROOT.mkdir(parents=True)
    for path in [lp,*docs]: copy2(path,ROOT/(path.name+'.before'))
    save(DOC,doc)
    existing = {(r['file_path'],r['id']) for r in fresh['record_keys']}
    selected = [dict(file_path='/COMMON/MESFILE.DK4',id=f'COMMON_MESSAGE_{n}') for n in IDS]
    assert all((r['file_path'],r['id']) not in existing for r in selected)
    fresh['integrated_record_keys'] = deepcopy(fresh['record_keys'])
    fresh['pending_record_keys'] = selected
    fresh['record_keys'].extend(selected)
    fresh['record_IDs'].extend(r['id'] for r in selected)
    pending = dict(id=FAMILY,records=7,record_keys=selected,manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),
        native_font_proof=str(FONT),focused_original_gate_proof=str(GATE),
        pending='Distinct shot effect,held-message dismissal and post-shot outcome transition;then final registered reconciliation.',
        source_prose_and_completed_credit_added=0,no_new_emulator_runs=True)
    fresh.update(fresh_pass_records_explicitly_reread=2150,fresh_pass_records_integrated=2143,
        fresh_pass_records_pending_native_actual_release=7,latest_contextual_manuscript=str(DOC),
        latest_pending_contextual_family=FAMILY,pending_contextual_families=[pending],
        coverage_note='2150fresh contextual rereads include2143reconciled historical completions and7unfinished Lookout reports pending distinct transition/final reconciliation. Source/prose2259 and incompleteCOMMON116 unchanged. All never-reviewed prose and the full objective remain in scope.')
    active = ledger['active_source_prose_drafts']
    active['manuscripts'].append(str(DOC)); active['manuscript_record_subsets_pending'][str(DOC)] = IDS
    active['note'] = fresh['coverage_note']
    ledger['latest_checkpoint'] = SUMMARY
    ledger['admiral_shot_contextual_v2660'] = dict(summary=SUMMARY,**pending,goal_turn_classification='progress',full_goal_complete=False)
    ledger['formatting_watchlist']['admiral_shot_contextual_v2660'] = dict(status='current-native-pass;distinct-shot-transition-pending',manuscript=str(DOC),native_font_proof=str(FONT),no_runtime_or_geometry_change=True)
    save(lp,ledger)
    section = '## V2660: Lookout shot7 contextual and native pass;transition pending\n\n'+SUMMARY+'\n\nManuscript: '+DOC.as_posix()+'. Native proof: '+FONT.as_posix()+'. Focused gate tests: '+GATE.as_posix()+'. Prior completed historical-set audit: '+prior_audit_path.as_posix()+'.\n\n'
    for i,path in enumerate(docs):
        first,rest = path.read_text().split('\n',1)
        path.write_text(('# Current editorial handoff - V2660' if i == 0 else first)+'\n\n'+section+rest,newline='\n')
    evidence_paths = [OLD,DOC,FONT,GATE,Path(font['review_sheet']),releasepath,prior_audit_path,
        Path(doc['source_context_packet']),Path(doc['native_context_proof']),Path(doc['fresh_ordinary_supplement']),
        Path(__file__),Path('scripts/review_admiral_shot_context_v2657.py'),
        Path('scripts/verify_admiral_shot_fonts_v2658.py'),Path('scripts/probe_admiral_shot_gate_v2659.py')]
    save(ROOT/'checkpoint_receipt.json',dict(checkpoint='V2660',summary=SUMMARY,
        fresh_reread=2150,fresh_integrated=2143,fresh_pending=7,completed_credit_added=0,new_revisions=0,
        incomplete_COMMON=116,source_prose=2259,historical_completed=2143,
        prior_ledger_audit=str(prior_audit_path),prior_ledger_sha256=prior_audit['ledger_sha256'],
        evidence={str(p):sha(p.read_bytes()) for p in evidence_paths},
        updated_files={str(p):sha(p.read_bytes()) for p in [lp,*docs]},
        candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],patch=release['patch'],patch_sha256=release['patch_sha256'],
        no_ROM_registry_profile_manifest_or_patch_change=True,new_emulator_runs=0,
        goal_turn_classification='progress',all_jobs_terminal=True,full_goal_complete=False))
    print('V2660:2150reread/2143reconciled/7pending;seven complete native checks;116incompleteCOMMON and full goal remain open. ROM/patch unchanged.')
