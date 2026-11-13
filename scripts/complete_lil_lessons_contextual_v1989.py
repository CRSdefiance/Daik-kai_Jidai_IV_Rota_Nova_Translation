"""Reconcile lesson64 after one registered correction; preserve historical totals."""
from copy import deepcopy
import os
from pathlib import Path
from shutil import copy2
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.register_lil_lookout_v1985 import ROOT as RELEASE, PROFILE
from scripts.approve_lil_lookout_v1984 import DOC, MAP, ACTUAL
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_lessons_contextual_completion_v1989')
FINAL = Path('translations/lil_lessons_contextual_final_review_v1.json')
ROM = Path('out/all_routes_combined_v1986_candidate.nds')
OLD = Path('translations/lil_lessons_final_review_v1.json')
DRAFT = Path('translations/lil_lessons_editorial_manuscript_v6.json')
CHOICES = Path('translations/lil_lesson_choices_editorial_draft_v3.json')
INHERITANCE = Path('work/analysis/lil_lessons_native_checkpoint_v1979b/all60_source_bound_native_font_inheritance.json')
LEDGER = Path('translations/editorial_review_current_v1.json')
HANDOFF = Path('docs/editorial_handoff_current.md')
GUIDE = Path('E:/Rota Nova translations/Guide screenshots/V1986 Lil Lookout affiliation verified')

if __name__ == '__main__':
    assert not ROOT.exists() and not FINAL.exists() and not GUIDE.exists()
    draft, choices, old, mapping, actual, inheritance, release, startup = map(read,(DRAFT,CHOICES,OLD,MAP,ACTUAL,INHERITANCE,
        RELEASE/'registered_release_verification.json',RELEASE/'ordinary_startup_verification.json'))
    digest = sha(ROM.read_bytes())
    assert digest == release['candidate_sha256'] == startup['candidate_sha256'] == actual['candidate_sha256']
    assert release['all485_batches114_accepted_layers_and_prior_profiles_preserved']
    assert release['complete_reconstruction_byte_exact'] and release['registered_ROM_whole_file_byte_exact_to_actual_scene_research_ROM']
    assert startup['all8_complete_startup_title_NewGame_frames_exact'] and startup['no_battery_save_savestate_or_fixtures']
    assert actual['changed_Lookout_two_holds_complete_native_actual_ink']
    assert actual['preceding_and_following_Camille_four_holds_complete_native_actual_ink']
    assert actual['all46_original_B23_command_results_and_mapped_targets_equal']
    assert actual['one16_coordinate_byte_fixture_replay_exact'] and actual['whole_terminal_RGB_equal_original']
    assert mapping['external_references_complete'] and mapping['all55_nested_commands12_relative_sites_verified']
    assert sha(ROM.with_suffix('.manifest.json').read_bytes()) == release['manifest_sha256']
    assert sha(Path(release['patch']).read_bytes()) == release['patch_sha256']
    image, clean = map(NdsImage.open,(ROM,'work/clean.nds'))
    blocks, jp = (IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks for im in (image,clean))
    old_rows = {r['id']:r for r in old['records']}
    native_cases = {r['id']:r for r in inheritance['cases']}
    focus = {r['id']:r for r in actual['focused_glyph_groups']}
    trace = read('E:/Rota Nova translations/Generated/work/emulation_v193/lil_Lookout_revised_run_v1982_RESEARCH_ONLY/observer/commands.json')
    active = {(r['source'].get('block'),r['source'].get('instruction_offset')) for r in trace['rows']
        if r['kind'] == 'before_command' and r['source'].get('route') == 2 and r['source'].get('first_word') == 0x4000}
    selected = {r['source']['block']:r['result_words'][1] for r in trace['rows']
        if r['kind'] == 'after_command' and r['source'].get('route') == 2 and r['source'].get('first_word') == 0x2100}
    patch = mapping['text_records'][0]
    delta = patch['new_length']-patch['old_length']
    def mapped(number,offset):
        if number != 23: return offset
        assert not patch['old_offset'] < offset < patch['old_offset']+patch['old_length']
        return offset+(delta if offset >= patch['old_offset']+patch['old_length'] else 0)
    rows = []
    for reviewed in draft['records']+choices['records']:
        row = deepcopy(reviewed)
        ident, number = row['id'], row['block']
        is_choice = 'CHOICE' in ident
        old_at = row['current_reference']['offset']
        at = mapped(number,old_at)
        value = blocks[number][at:blocks[number].index(b'\0',at)]
        source, ja = bytes.fromhex(row['source_hex']), row['source_reference']['offset']
        assert jp[number][ja:ja+len(source)] == source and jp[number][ja+len(source)] == 0
        if is_choice:
            assert value.decode('ascii') == row['english'] == old_rows[ident]['english']
            ref = dict(file_path='/data/SC2.DK4',block=number,offset=at,bytes=len(value),
                choice_command_offset=mapped(number,row['command_offset']),option_index=row['option_index'])
            row['individually_selected_in_new_sample'] = selected.get(number) == row['option_index']
            row['native_choice_UI_evidence_inherited_unchanged'] = True
        else:
            assert blocks[number][at-5:at+1] == jp[number][ja-5:ja+1] == bytes.fromhex(row['source_complete_preamble_hex'])
            case = native_cases[ident]
            encoded = bytes.fromhex(case['encoded_hex'])
            assert value in (encoded,encoded+b' ')
            if ident == 'DK4_MES_B23_R0142': assert value.hex() == patch['target_hex']
            else: assert value.hex() == row['current_text_hex']
            ref = dict(file_path='/data/SC2.DK4',block=number,offset=at,bytes=len(value),header_offset=at-5,
                record_index=blocks[number][:at].count(b'\0'))
            row.update(record_index=ref['record_index'],compiled_hex=encoded.hex(),
                native_display_consumer='original_FE_modal_5473C_mode1' if value[:1] == b'\xfe' else 'original_progressive_54020',
                individually_activated_in_new_sample=(number,at-5) in active,
                new_sample_full_pixels_checked=ident in focus,
                new_sample_pixel_holds=focus[ident]['holds'] if ident in focus else [],
                historical_actual_samples=old_rows[ident].get('actual_samples',[]),
                inherited_native_source=str(INHERITANCE),current_stored_English=value[1:].decode('cp932'))
        row.update(review_input_current_reference=deepcopy(row['current_reference']),review_input_current_text_hex=row['current_text_hex'],
            current_reference=ref,current_text_hex=value.hex(),english=row['english'].removesuffix('{PAD}'),
            completed_candidate_reference=str(ROM),completed_candidate_sha256=digest,
            current_reference_map=str(MAP) if number == 23 else old_rows[ident]['reference_map'],
            status='fresh-contextual-source-native-registered-and-representative-revised-complete')
        row['review']['formatting'] = True
        row['context'] = row['context'].split('New native/')[0]+(
            'Registered V1986,exact clean-input patch,focused revised Lookout/neighbor/Brugesreturn andstartup gates pass. Other59 speech targets andfourlabels inherit exact source-bound display evidence;no newindividual conditional-path visits areclaimed.')
        if row['editorial_decision'] == 'retain-wording': row['retained_wording_justification'] = row['localization_note']
        rows.append(row)
    assert len(rows) == 64 and sum(r['editorial_decision'] == 'revise' for r in rows) == 1
    assert sum(r.get('new_sample_full_pixels_checked',False) for r in rows) == 3
    ids = {r['id'] for r in rows}
    raw = LEDGER.read_bytes()
    ledger = read(LEDGER)
    before = deepcopy(ledger)
    fresh = ledger['contextual_story_natural_dialogue_pass_v1871']
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release']) == (428,364,64)
    assert ids <= set(fresh['record_IDs'])
    family = next(f for f in ledger['completed_editorial_families'] if f['id'] == 'Lil-sailing-and-crew-lessons64')
    assert ids == set(family['record_IDs'])
    prior_changed = next(r for r in family['records'] if r['id'] == 'DK4_MES_B23_R0142')
    assert prior_changed['editorial_decision'] == 'revise'
    ROOT.mkdir(parents=True)
    (ROOT/'ledger_before.json').write_bytes(raw)
    (ROOT/'handoff_before.md').write_bytes(HANDOFF.read_bytes())
    scope = ('Fresh sailing/crew lesson64:all60 speeches/system panels andfour choice labels reread fromclean Japanese ascomplete exchanges. '
        'One revision changes Lookout affiliation fromwhich fleets other ships belong to,to who other ships belong to;63individual justified retentions preserve controls,mechanics,roles,uncertainty,humor andvoices. '
        'The changed paragraph passes one complete native/independent216x64 plane,eight macro/alignment calls andfinal parity pixels. '
        '50unchanged progressive targets,nine separate228x48 FE mode1 targets andfourtyped labels inherit exact source-bound proofs. '
        'Current-source B23has55mapped commands,12relative spans,120current/relocated native cases,exact inverse restoration and336loads/672parent modes perROM. '
        'Focused revised gameplay reexecutes theoriginal crewlesson path:the changed Lookout andtwo adjacent Camille speeches match six full native/actual holds,all46original B23results andunowned B120results remain exact,normalBrugesreturn41420 iswhole-screen identical. '
        'Other27 B23speeches execute onthis path without a fresh per-panel pixel claim;threeB23objects andotherchoice paths have inherited source/native/earlier-actual scope only. '
        'One disclosed16-byte coordinate-only Bruges fixture leaves everyother4MiB byte exact;inputs,capture hashes,readonly callbacks andhost restoration pass. No earnedtravel,event/RNG/character/outcome/funds override orhardware/full-route claim. '
        'RegisteredV1986 equals theentire tested researchROM. OnlyB23shrinks12bytes fromV1971;335otherSC2blocks,everyother file/component,COMMON,ARM9,fonts,graphics and123040staged bytes remain exact. '
        'All485batches/114accepted layers,prior profiles,19invalid-release gates,exactclean-input patch andeightfresh fixture-free startup controls pass. '
        'Fresh pass428integrated/reconciled;historical1831completions(1362revised469retained) and1947source/prose remainunchanged because these64were alreadycounted andthechanged record wasalready historically revised. '
        '1403other historical completions,116incomplete COMMON,everyremaining storyline/shared shop/town/random/playerprose,separategraphics/all18plaques andlaterolder-record technical re-audit remainopen;fullgoalactive,V1492promoted.')
    visual = ROOT/'registered_visual_and_inheritance_reconciliation.json'
    save(visual,dict(registered_ROM_whole_file_exact_tested_research_ROM=True,
        changed_Lookout_two_neighboring_Camille_panels_and_normal_Bruges_return_actually_viewed=True,
        all8_fixture_free_startup_control_frames_actually_viewed=True,
        changed_native_plane_and8_macro_calls_newly_tested=True,unchanged59targets_fourlabels_inherited_not_rerun=True,
        no_new_actual_claim_for_unvisited_conditional_objects_or_other_choice_paths=True,
        historical_unique_completion_counts_unchanged=True,
        evidence={str(p):sha(p.read_bytes()) for p in (DOC,MAP,ACTUAL,DRAFT,CHOICES,OLD,INHERITANCE,
            RELEASE/'registered_release_verification.json',RELEASE/'ordinary_startup_verification.json')},full_goal_complete=False))
    save(FINAL,dict(format='dk4-contextual-final-family-reconciliation-v1',family=family['id'],file_path='/data/SC2.DK4',blocks=[120,23],
        record_IDs=sorted(ids),records=rows,revised_count=1,retained_count=63,current_candidate=str(ROM),candidate_sha256=digest,
        historical_final_review=str(OLD),historical_final_review_sha256=sha(OLD.read_bytes()),
        historical_completion_counts_not_added_or_reclassified=True,actual_scope=scope,reference_map=str(MAP),final_proof=str(visual),
        all_fresh_contextual_source_native_reference_representative_revised_registered_gates_pass=True,full_goal_complete=False))
    family.setdefault('prior_final_review_references',[]).append(dict(path=family['final_review'],documentation=family['documentation'],
        actual_verification_scope=family['actual_verification_scope']))
    family.update(final_review=str(FINAL),documentation='docs/lil_lessons_v1989_contextual_reconciliation.md',actual_verification_scope=scope,
        contextual_v1871_reconciliation=dict(review=str(FINAL),review_sha256=sha(FINAL.read_bytes()),new_revisions=1,justified_retentions=63,
            historical_counts_unchanged=True,current_candidate=str(ROM)))
    new_by_id = {r['id']:r for r in rows}
    for historical in family['records']:
        current = new_by_id[historical['id']]
        historical.setdefault('current_reference_history',[]).append(dict(reference=deepcopy(historical['current_reference']),
            text_hex=historical['current_text_hex'],candidate=historical['completed_candidate_reference']))
        for key in ('current_reference','current_text_hex','english','completed_candidate_reference','completed_candidate_sha256'):
            historical[key] = deepcopy(current[key])
        historical.update(contextual_v1871_decision=current['editorial_decision'],contextual_v1871_reason=current['localization_note'],
            current_contextual_final_review=str(FINAL),current_reference_map=current['current_reference_map'])
        if 'source_record_index' in current:
            historical['source_record_index'] = current['source_record_index']
            historical['record_index'] = current['record_index']
        if 'current_stored_English' in current: historical['current_stored_English'] = current['current_stored_English']
        if 'current_English' in historical: historical['current_English'] = current['english']
        if 'compiled_hex' in current:
            historical['compiled_hex'] = current['compiled_hex']
            historical['formatted_markup'] = native_cases[current['id']]['formatted_markup']
            historical['native_display_consumer'] = current['native_display_consumer']
            historical['historical_actual_samples'] = deepcopy(current['historical_actual_samples'])
            historical['individually_activated_in_gameplay'] = current['individually_activated_in_new_sample']
            historical['new_sample_full_pixels_checked'] = current['new_sample_full_pixels_checked']
            historical['actual_samples'] = ([{'proof':str(ACTUAL),'holds':current['new_sample_pixel_holds'],
                'same_target_block_and_runtime_verified':True}] if current['new_sample_full_pixels_checked'] else [])
            historical['current_representative_actual_proof'] = str(ACTUAL)
            historical['actual_proof_scope'] = ('New complete pixel comparison inV1986.' if current['new_sample_full_pixels_checked'] else
                'Exact unchanged native target andhistorical display evidence inherited;current callback activation isrecorded separately,no fresh per-panel pixel claim.')
            if current['new_sample_full_pixels_checked']: historical['actual_proof'] = str(ACTUAL)
            legacy = {k:deepcopy(v) for k,v in historical.items() if k.startswith('current_native_macro_')}
            if legacy:
                historical['historical_preexisting_native_macro_probe_fields'] = legacy
                for key in legacy: historical.pop(key)
    fresh.update(fresh_pass_records_integrated=428,fresh_pass_records_pending_native_actual_release=0,
        historical_completed_records_outside_reconciled_fresh_pass=1403,latest_completed_family=family['id'],latest_final_review=str(FINAL),
        coverage_note='All428explicitly reread entries integrated/reconciled:Stockholm51,London111,Speyer59,Hamburg81,trade/officer13,opening49 andsailing/crew64. Lesson64hasonefaithful affiliation revision63retentions;historicaltotals unchanged. Other1403historical completions needexplicit reconciliation.')
    fresh['pending_historical_reconciliations'] = [p for p in fresh['pending_historical_reconciliations'] if p['id'] != family['id']]
    fresh['reconciled_families'].append(dict(id=family['id'],records=64,final_review=str(FINAL),historical_reconciliation_only=True,
        new_revisions=1,justified_retentions=63,historical_completion_counts_unchanged=True))
    unit = next(u for u in ledger['coverage_units'] if u['id'] == 'Lil-sailing-crew64-contextual-v1977')
    unit.update(status='fresh-contextual-reconciliation-complete-in-V1986',final_review=str(FINAL),historical_entries_reconciled=64,
        changed_record_integrated=True,completed_entries_added=0)
    ledger['active_source_prose_drafts'].update(status='116-reviewed-COMMON-and-broader-fresh-contextual-prose-open',
        note='Fresh lesson64 integrated/reconciledV1986 afterone affiliation fix and63retentions. No activefresh historical-route drafts. Continue allremaining routes/shared town/random/playerprose and1403historical reconciliations.')
    ledger.setdefault('integrated_candidate_reference_history',[]).append(deepcopy(ledger['current_integrated_candidate']))
    ledger['current_integrated_candidate'] = dict(path=str(ROM),sha256=digest,profile=PROFILE,MESFILE_sha256=release['COMMON_sha256'],
        ARM9_sha256=release['ARM9_sha256'],SC2_sha256=release['SC2_sha256'],patch=release['patch'],patch_sha256=release['patch_sha256'],
        manifest=str(ROM.with_suffix('.manifest.json')),status='experimental-verified-editorial-checkpoint-not-promoted',details=scope,full_goal_complete=False)
    ledger.setdefault('native_completed_reference_history',[]).append(deepcopy(ledger['current_native_relocation_reference']))
    ledger['current_native_relocation_reference'].update(candidate=str(ROM),candidate_sha256=digest,
        COMMON_sha256=release['COMMON_sha256'],ARM9_sha256=release['ARM9_sha256'],SC2_sha256=release['SC2_sha256'])
    ledger['latest_registered_editorial_candidate'] = {**release,'status':'experimental-verified-fresh-lesson64-reconciliation',
        'final_review':str(FINAL),'actual_proof':str(visual),'startup_controls_and_editorial_completion_pending':False}
    ledger['next_route_scene_editorial_packet'] = dict(current_verified_town='Bruges3',current_verified_town_context=str(ACTUAL),
        current_verified_snapshot='E:/Rota Nova translations/Generated/work/emulation_v193/lil_Lookout_revised_run_v1982_RESEARCH_ONLY/frame_041420_arm9_ram.bin',
        current_registered_candidate=str(ROM),current_registered_candidate_sha256=digest,
        next='Inventory remaining Lil storyline andshared-town/random/player dialogue fromverified town snapshots;explicitly reconcile earlier COMMON reviews. Source-first complete conversations;representative gameplay forconcrete risks. Keepallother routes in full scope.',full_goal_complete=False)
    summary = 'V1989 lesson64 fresh contextual reconciliation complete. '+scope
    ledger['latest_checkpoint'] = summary
    ledger['research_checkpoints'].append(dict(id='V1989-fresh-lesson64-reconciled',proof=str(ROOT/'completion_receipt.json'),
        completed_entries_added=0,source_prose_reviews_added=0,historical_entries_reconciled=64,changed_records_integrated=1,full_goal_complete=False))
    for key in ('records_editorially_completed','records_revised_and_integrated','retained_wordings_editorially_completed','records_with_source_and_prose_pass',
        'completed_editorial_record_counts_by_file','source_prose_reviewed_counts_by_file','unresolved_graphics_work',
        'reviewed_but_incomplete_COMMON_IDs','older_record_reaudit_after_full_editorial_goal'):
        assert ledger[key] == before[key],key
    assert ledger['records_editorially_completed'] == 1831 and len(fresh['record_IDs']) == len(set(fresh['record_IDs'])) == 428
    assert ledger['records_editorially_completed']-fresh['fresh_pass_records_integrated'] == 1403
    assert ledger['goal_status'] == 'active' and not ledger['full_goal_complete']
    GUIDE.mkdir(parents=True)
    copied = []
    for group in actual['focused_glyph_groups']:
        source = Path(group['holds'][1]['capture'])
        target = GUIDE/(group['id']+'.png')
        copy2(source,target)
        assert target.read_bytes() == source.read_bytes()
        copied.append(str(target))
    source = Path(actual['terminal_capture']['path'])
    target = GUIDE/'Bruges_return.png'
    copy2(source,target)
    assert target.read_bytes() == source.read_bytes()
    copied.append(str(target))
    pending = LEDGER.with_name('editorial_review_current_v1989_pending.json')
    assert not pending.exists() and LEDGER.read_bytes() == raw
    save(pending,ledger)
    os.replace(pending,LEDGER)
    details = (f'# V1989 sailing andcrew lesson contextual reconciliation\n\n{summary}\n\nCandidate:{ROM.as_posix()}\n\nSHA256:{digest}\n\n'
        f'Profile:{PROFILE}\n\nPatch:{release["patch"]}\n\nPatch SHA256:{release["patch_sha256"]}\n\nFinal review:{FINAL.as_posix()}\n\n'
        f'Map:{MAP.as_posix()}\n\nActual proof:{ACTUAL.as_posix()}\n\nGuide:{GUIDE}\n\n'
        'The full64-entry fresh review isdistinct fromthe one-record compiler batch. All59other speech targets/fourlabels preserve bytes andinherited geometry;onlythe Lookout body changes. '
        'Clean andcurrent record indices staydistinct(sourceR0142/currentinput141);currentreferences recomputed fromtarget bytes aftertyped spans change. '
        'The frozen1979checkpoint expected astandalone bitmap path forthe previously refinedR0166 FEpanel;1979b instead verifiesits exact compiled/storage native-plane proof. '
        'The sixlater COMMONreinforcement announcements areexplicitly scoped;no wholeCOMMONequality withV1711/V1775 claim. No equivalent oldgameplay rerun exceptthe focused original crewpath required forthe newwording.\n')
    Path('docs/lil_lessons_v1989_contextual_reconciliation.md').write_text(details,encoding='utf-8')
    for name in ('translation_progress.md','known_issues.md','todo.md','editorial_review_goal.md'):
        with (Path('docs')/name).open('a',encoding='utf-8') as stream:
            stream.write('\n\n## V1989 fresh lesson64 reconciled\n\n'+summary+'\n\nSee [reconciliation](lil_lessons_v1989_contextual_reconciliation.md).\n')
    text = HANDOFF.read_text(encoding='utf-8').replace('# Current editorial handoff - V1979','# Current editorial handoff - V1989',1)
    start = text.index('## Current coverage and registered release')
    end = text.index('## Current focused native checkpoint - V1979')
    coverage = f'''## Current coverage and registered release

- Ledger:translations/editorial_review_current_v1.json. **1831 historical completions =1362revised +469retained;1947source/prose reviewed.**
- Fresh V1871pass:428 explicitly reread andintegrated/reconciled;no activefresh route drafts. Families:Stockholm51,London111,Speyer59,Hamburg81,trade/officer13,opening49,sailing/crew64. Other1403historical completions require explicit reconciliation.
- Completed:1402COMMON +429SC2;reviewed:1518COMMON +429SC2.116COMMON remainincomplete;everyremaining storyline/shared shop/town/random/playerprose staysin scope. Earlier review isnot automaticfresh completion.
- Latestregisteredexperimental:{ROM.as_posix()},profile{PROFILE};485manifest batches/114accepted layers.
- CandidateSHA256:{digest}.
- Exactclean-input patch:{release['patch']};SHA256{release['patch_sha256']};wholeROM reconstruction exact.
- ARM9{release['ARM9_sha256']};COMMON{release['COMMON_sha256']};SC2{release['SC2_sha256']}. Staged123040bytes unchanged.
- Canonicalbaseline andclean Japanese ROM unchanged. AllROMs andearlier translations preserved. V1492 remainspromoted;no newpromotion,commit orpush.

## Fresh sailing/crew64 reconciled - V1989

{scope}

- Finalreview:{FINAL.as_posix()};fullsource/prosedrafts:{DRAFT.as_posix()} and{CHOICES.as_posix()};one-record approvedrelease:{DOC.as_posix()};map:{MAP.as_posix()}.
- Compiler:dk4tool/patch/lil_lookout_affiliation.py;config:translations/lil_lookout_affiliation_release_v1.json. Allguards precede soleSC2mutation;19negative release cases reject withoutpartial writes. FocusedRuff passes withno exclusions fornewcompiler.
- Native1980:currentB23source/target55commands,12typed relative spans,120native cases,exactinverse andfinalparity plane. B23shrinks12bytes;B120 and335otherblocks exact. Loader1981 covers336loads/cachehits and672parentmodes perROM. Originalcode/overlay entrycensus inherited throughunchanged files;not unnecessarily repeated.
- Actual1983:changedLookout andtwoadjacentCamille panels,sixfull matchingholds,46original B23results,unownedB120results,originalchoice0 andnormalBrugesreturn41420. ThewholeterminalRGB equalsprior originalcapture. Other27B23speechobjects execute withoutfresh pixelclaims;threeB23objects unvisitedonthispath. Otherbranch/wind evidence remainsinherited,no second newchoicepath.
- One16-byte coordinate-only Brugesfixture;allother4MiB bytes,inputs,snapshots,capturehashes,readonlycallbacks andhost restoration pass. No funds/event/RNG/character/choiceoutcome edits;no earnedtravel/full-route/hardware claim.
- Release:work/analysis/lil_Lookout_release_v1985/registered_release_verification.json;startup:ordinary_startup_verification.json. Guide:{GUIDE};fourfocus/returncaptures. All485batches,114acceptedlayers,priorprofiles,exactcleanpatch andeightfresh ordinary startupframes pass;viewed.
- Historicaltotals unchanged:the64entries werealready counted andR0142 wasalready historicallyrevised. Freshreview hasone revision63retentions;globalhistorical unique-record counters remain1831/1362/469.
- Alljobs terminal:run1982/session94479,builder1986/session83370,andstartup jobs. Preservefrozenfailed1979 schemaassumption andcorrect1979b proof;no unresolvedfailure remains.

'''
    text = text[:start]+coverage+text[end:]
    text = text.replace('## Current focused native checkpoint - V1979','## Historical focused native checkpoint - V1979',1)
    text = text.replace('## Active unit: earlier sailing/crew64 fresh contextual pass - V1977','## Historical lesson64 source pass - V1977 (completedV1989)',1)
    next_start = text.index('## Exact next work after Hamburg')
    next_end = text.index('## Latest completed scene: Lil trade routes and officers, SC2 B24',next_start)
    next_work = f'''## Exact next work after fresh lesson reconciliation

Continue the full fresh contextual review ofeveryremaining storyline,earlier translation,shared shop/town/randomscene andplayer-facing prose.1403historical completions still needexplicit reconciliation;116COMMON remainincomplete. Remaininguntouched route scenes arein fullscope. Usecomplete exchanges fromclean Japanese,approved names,individual retention reasons,exactsource/current refs andvalidated nativecontrols. Capture town/randomscenes broadly aspractical;focused representative tests fornew risks. Do notrepeat completed Stockhom/London/Speyer/Hamburg/earlierLil checks withoutconcrete newrisk.

Currentverifiedtown snapshot:E:/Rota Nova translations/Generated/work/emulation_v193/lil_Lookout_revised_run_v1982_RESEARCH_ONLY/frame_041420_arm9_ram.bin;entireROM exactregisteredV1986. NormalBruges3return afteroriginal crewlesson,onecoordinate-only fixture. TheolderHamburg/Speyer snapshots remainvalid runtime/source evidence within theirrecorded scope;do notclaim theirwholeROM equalsV1986. Inventory remaining nativeevent/shared town/randomdialogue withoutforcing storyoutcomes orassuming numbered nextchapters. Amsterdamdye,B25aftermath andnativecatalog Pedro デ Valdes remainseparate unresolvedleads.

Preserve allROMs andearlier translations. Unresolvedgraphics/all18plaques remainseparate/open. Retainlaterolder-record technical re-audit afterfull editorialobjective. Fullgoalactive,V1492promoted.

'''
    HANDOFF.write_text(text[:next_start]+next_work+text[next_end:],encoding='utf-8')
    save(ROOT/'completion_receipt.json',dict(final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),
        candidate=str(ROM),candidate_sha256=digest,profile=PROFILE,patch=release['patch'],patch_sha256=release['patch_sha256'],
        fresh_historical_entries_reconciled=64,new_wording_revisions_integrated=1,justified_retentions=63,new_unique_historical_completions=0,
        historical_completed_unchanged=1831,source_prose_reviewed_unchanged=1947,fresh_reread_integrated=428,
        historical_outside_reconciled_fresh_pass=1403,guide_captures=copied,
        ledger_sha256=sha(LEDGER.read_bytes()),handoff_sha256=sha(HANDOFF.read_bytes()),
        all_ROMs_and_earlier_translations_preserved=True,full_goal_remains_active=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(fresh_integrated_reconciled=428,fresh_pending=0,historical_total_unchanged=1831,
        lesson_new_revisions=1,lesson_retentions=63,all_ROMs_preserved=True,full_goal_remains_active=True))
