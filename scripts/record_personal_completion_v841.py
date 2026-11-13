"""Close the25-comment editorial family with source-bound sampled actual evidence."""

from copy import deepcopy
from pathlib import Path
from shutil import copy2

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch import personal_chatter_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.prepare_personal_release_v838 import MANUSCRIPT
from scripts.verify_personal_gameplay_v841 import ROOT,ROM,CAP,CASES
from scripts.verify_refit_release_v708 import files
from scripts.verify_village_wrap_v608 import read,save

LEDGER=Path('translations/editorial_review_current_v1.json')
REVIEW=Path('translations/personal_chatter_editorial_final_review_v1.json')
DOC=Path('docs/personal_chatter_v841_completion.md')
ARCHIVE=Path('E:/Rota Nova translations/Editorial review/V841 Deck personal comments completion')
GUIDE=Path('E:/Rota Nova translations/Screenshots/Guide candidates/V841 Deck personal comments')


def reference(e):
    return {k:getattr(e,k) for k in ('message_id','block','table_offset','block_offset','copy_end','record_index','start','end')}


def main():
    assert not REVIEW.exists() and not DOC.exists() and not ARCHIVE.exists() and not GUIDE.exists()
    ledger,doc=read(LEDGER),read(MANUSCRIPT)
    assert ledger['records_editorially_completed']==646 and ledger['records_with_source_and_prose_pass']==674
    validate_natural_dialogue_batch(doc)
    assert all(all(r['review'].values()) for r in doc['records'])
    gameplay=read(ROOT/'actual_gameplay_verification.json')
    assert len(gameplay['actual_complete_dialogue_holds'])==10
    assert {r['message_id'] for r in gameplay['actual_complete_dialogue_holds']}=={1365,1366,1367,1375,1379}
    assert len(gameplay['scoped_normal_return_state_controls'])==3 and all(r['all_equal'] for r in gameplay['scoped_normal_return_state_controls'])
    assert sha(Path(gameplay['review_sheet']).read_bytes())==gameplay['review_sheet_sha256']
    assert gameplay['candidate_sha256']==sha(ROM.read_bytes())
    gameplay.update(visual_review_pending=False,visual_review={
        'all10_complete_actual_holds_opened_in_final_sheet':True,
        'all_five_individual_speaker_frames_and_all_three_normal_town_returns_opened':True,
        'Janus_story_Claudio_counting_and_both_complete_multiline_rows_read':True,
        'actual_odd15_character_first_row_and_complete_Sneaking_at_x16_reviewed':True,
        'synthetic_Emilio_room_occupant_is_explicit_not_an_owned_recruitment_claim':True})
    save(ROOT/'actual_gameplay_verification.json',gameplay)
    fonts=read('work/analysis/personal_chatter_v837/native_projection_and_font_proof.json')
    assert not fonts['visual_review_pending'] and len(fonts['all25_compiled_visible_word_and_native_font_cases'])==25
    assert len(fonts['all144_visible_width_phase_cases'])==144
    context=read(ROOT/'ordinary_Cabin_context_verification.json')
    assert len(context['all25_original_Cabin_role_helper_selections'])==25
    before_rom=NdsImage.open('out/all_routes_combined_v834_candidate.nds')
    rom=NdsImage.open(ROM)
    before,after=files(before_rom),files(rom)
    assert before.keys()==after.keys() and {p for p in before if before[p]!=after[p]}=={'/COMMON/MESFILE.DK4','/__arm9__.bin'}
    c,a,stage=owned.apply_release(before['/COMMON/MESFILE.DK4'],before['/__arm9__.bin'],owned.CONFIG)
    assert c==after['/COMMON/MESFILE.DK4'] and a==after['/__arm9__.bin']
    entries=owned.current_entries(c,a)
    copies=read('work/analysis/personal_chatter_v838/native_copy_proof.json')
    assert len(copies['all3668_native_IDs_warm_and_cold7336_complete_copies'])==3668
    prior_release=Path('work/analysis/personal_chatter_v838/registered_release_verification.json')
    release=read(prior_release)
    startup=read('work/analysis/personal_chatter_v838/ordinary_startup_verification.json')
    assert startup['all7_full_screen_pairs_exact'] and not startup['visual_review_pending']
    assert sha(ROM.read_bytes())==release['candidate_sha256']==startup['candidate_sha256']
    assert sha(ROM.with_suffix('.xdelta').read_bytes())==release['patch_sha256']
    assert sha(Path(release['exact_clean_input_patch_reconstruction']).read_bytes())==release['candidate_sha256']
    assert sha(Path('work/clean.nds').read_bytes())==doc['source_clean_ROM_sha256']==release['clean_input_sha256']
    registry=read('translations/release_stack.json');manifest=read(ROM.with_suffix('.manifest.json'))
    assert manifest['profile']=='all-routes-unified-v838' and len(manifest['batches'])==471
    assert len(registry['accepted_layers'])==114 and manifest['base_sha256']==registry['canonical_baseline']['sha256']
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    closure=ROOT/'registered_release_completion.json'
    save(closure,{'candidate':str(ROM),'candidate_sha256':release['candidate_sha256'],
        'immutable_original_registered_release_proof':str(prior_release),'original_proof_sha256':sha(prior_release.read_bytes()),
        'actual_gameplay_proof':str(ROOT/'actual_gameplay_verification.json'),
        'actual_gameplay_proof_sha256':sha((ROOT/'actual_gameplay_verification.json').read_bytes()),
        'ordinary_Cabin_context_proof':str(ROOT/'ordinary_Cabin_context_verification.json'),
        'fresh_late_stage_replay_and_all_other_components_exact':True,
        'patch_sha256':release['patch_sha256'],'exact_reconstruction_fresh_hash_matches':True,
        'all471_batches114_accepted_layers_and_canonical_preserved':True,
        'all25_native_fonts144_phase_cases7336_native_copies_and7_startup_controls_pass':True,
        'actual_comment_and_normal_return_gates_closed_by_scoped_evidence':True,
        'historical_pending_proofs_preserved_without_mutation':True,'canonical_not_promoted':True,
        'whole_goal_complete':False})
    save(ROOT/'editorial_ledger_before_completion.json',ledger)
    existing={n for f in ledger['completed_editorial_families'] for n in f.get('native_message_IDs',[])}
    assert not existing.intersection(owned.IDS)
    native={r['message_id']:r for r in fonts['all25_compiled_visible_word_and_native_font_cases']}
    records=[]
    for row in doc['records']:
        n=row['message_id']
        assert entries[n].text==owned.compiled(row) and native[n]['text_hex']==entries[n].text.hex()
        records.append({**deepcopy(row),'authored_context':row['context'],
            'context':'Independent actor-specific Deck comment. Ordinary healthy/normal-mood Cabin type12 or role16 reaches1361+actor through the original role helpers. The original leisure animation also uses the same family. Full normal selector and actual display are sampled separately;storage neighbors belong to other actors.',
            'completed_candidate_reference':str(ROM),'before_reference':row['current_reference'],
            'before_text_hex':row['current_text_hex'],'current_reference':reference(entries[n]),
            'current_text_hex':entries[n].text.hex(),
            'decision':'revised-and-integrated' if row['editorial_decision']=='revise' else 'retained-and-editorially-reviewed',
            'generated_native_lines':native[n]['generated_visible_lines'],
            'native_font_canvas_sha256':native[n]['canvas_sha256'],
            'actual_display_holds':[r for r in gameplay['actual_complete_dialogue_holds'] if r['message_id']==n],
            'all_source_native_copy_font_and_visible_bounds_gates_pass':True,
            'individual_actual_visit_not_claimed_when_actual_holds_list_empty':True})
    assert sum(r['editorial_decision']=='revise' for r in records)==18
    final={'format':'dk4-editorial-family-final-review-v1',
        'status':'25-source-context-editorial-native-and-representative-actual-verified',
        'candidate':str(ROM),'candidate_sha256':release['candidate_sha256'],
        'source_manuscript':str(MANUSCRIPT),'source_manuscript_sha256':sha(MANUSCRIPT.read_bytes()),
        'registered_release_proof':str(closure),'actual_gameplay_proof':str(ROOT/'actual_gameplay_verification.json'),
        'native_visible_font_proof':'work/analysis/personal_chatter_v837/native_projection_and_font_proof.json',
        'native_ordinary_Cabin_helper_proof':str(ROOT/'ordinary_Cabin_context_verification.json'),
        'actual_scope':gameplay['scope'],'records':records,
        'separate_Samwell_middle_name_Japanese_glyph_finding_still_open':True,
        'full_editorial_goal_complete':False,'separate_graphics_goal_complete':False}
    save(REVIEW,final)
    family={'id':'Shared-Deck-personal-comments1361-1385','native_message_IDs':list(owned.IDS),
        'records':records,'final_review':str(REVIEW),'documentation':str(DOC),'actual_verification_scope':gameplay['scope']}
    ledger['completed_editorial_families'].append(family)
    ledger['records_editorially_completed']=671
    ledger['records_revised_and_integrated']=485
    ledger['retained_wordings_editorially_completed']=186
    ledger['completed_editorial_record_counts_by_file']['/COMMON/MESFILE.DK4']=670
    ledger['reviewed_but_incomplete_COMMON_IDs']=[n for n in ledger['reviewed_but_incomplete_COMMON_IDs'] if n not in owned.IDS]
    assert ledger['reviewed_but_incomplete_COMMON_IDs']==[750,751,752]
    ledger['active_source_prose_drafts']={'native_message_IDs':[750,751,752],
        'manuscripts':['work/analysis/market_contract_v758/unmapped_750_752_prose_DRAFT.json'],
        'status':'three-older-context-unmapped-drafts',
        'note':'Deck25 completes in V838 with V841 actual verification. These three drafts are not the full remaining scope;all unreviewed shared/route/player prose and raw-source coverage remain.'}
    ledger['previous_current_integrated_candidate_V834']=deepcopy(ledger['current_integrated_candidate'])
    candidate={'path':str(ROM),'sha256':release['candidate_sha256'],'profile':'all-routes-unified-v838',
        'MESFILE_sha256':sha(c),'ARM9_sha256':sha(a),'patch':str(ROM.with_suffix('.xdelta')),
        'patch_sha256':release['patch_sha256'],'manifest':str(ROM.with_suffix('.manifest.json')),
        'status':'experimental-Deck25-editorially-native-and-representative-gameplay-verified',
        'details':str(DOC),'full_goal_complete':False}
    ledger['current_integrated_candidate']=candidate
    ledger['source_pins']['current']=deepcopy(candidate)
    ledger['next_integrated_profile_for_goal_continuation']=candidate['profile']
    ledger['native_relocation_reference_before_Deck_completion']=deepcopy(ledger['current_native_relocation_reference'])
    ledger['current_native_relocation_reference']={'candidate':str(ROM),'COMMON_sha256':sha(c),'ARM9_sha256':sha(a),
        'parser':'dk4tool.patch.personal_chatter_editorial.current_entries','release_config':owned.CONFIG,
        'source_locked_directory_and_all3668_selections_verified':True}
    ledger['previous_pending_integrated_candidate_V838']=ledger.pop('pending_integrated_candidate')
    ledger['personal_chatter_v841']={'status':final['status'],'final_review':str(REVIEW),
        'documentation':str(DOC),'actual_scope':gameplay['scope'],'registered_release_proof':str(closure),
        'actual_gameplay_proof':final['actual_gameplay_proof'],'full_goal_complete':False}
    for key in ('personal_chatter_v835','personal_chatter_v836','personal_chatter_v838'):
        ledger[key]['completed_by_final_review']=str(REVIEW)
        ledger[key]['remaining_gates']=[]
        ledger[key]['historical_no_completion_credit_superseded_by_completed_family']=family['id']
    for finding in ledger['findings']:
        if finding.get('id') in ('Deck-personal-comment-bare-LF-first-letter-phase-v836','Deck-personal-comment-parent-visible-crop-v837'):
            finding.update(status='integrated-and-native-plus-representative-actual-verified',completed_by_family=family['id'],actual_proof=final['actual_gameplay_proof'])
    ledger['findings'].append({'id':'Deck-widget-RTTI-class-label-erratum-v841',
        'status':'documented-from-exact-native-RTTI-records',
        'detail':'The body widget021314E8 is CDeckCabinInfoView and its parent02130EF0 is CDeckPersonnelView. Earlier nearby-name labels were mistaken;owned offsets,canvas,palette,code and glyph/crop evidence are unchanged. Native blitter reads a byte-sized format,so animated1404h flags are preserved.',
        'proof':str(ROOT/'native_view_identity_erratum.json'),'no_additional_entry_credit':True})
    ledger['formatting_watchlist']['Deck_personal_comment_phase_research'].update(
        status='integrated-and-actual-odd15-character-line-Sneaking-continuation-verified',
        actual_proof=final['actual_gameplay_proof'],scope='The original Deck comment consumer. All25 native bodies and144 phase cases pass;actual odd-row Emilio is a declared one-byte Cabin fixture. The global audit stays open.')
    ledger['formatting_watchlist']['Deck_personal_comment_visible_crop'].update(actual_comment_display_pending=False,
        actual_proof=final['actual_gameplay_proof'],sampled_original_crop_loss_detected=True)
    ledger['coverage_units'].append({'id':family['id'],'status':'completed','native_message_IDs':list(owned.IDS),
        'final_review':str(REVIEW),'scope':'25 independent comment bodies;name-header finding,other shared prose,routes and graphics remain open.'})
    checkpoint=('V841 completes25 Deck personal comments1361-1385 in registered V838:18 revisions and7 justified retentions. '
        'All25 native full-font/crop cases,144 phase cases,25 ordinary Cabin helper aliases and7336 original warm/cold copies pass. '
        'Ten actual complete bitmap/RGB holds cover five revised IDs:Janus1365,Claudio1366,Julio1367,Emilio1375 andCharles1379. '
        'Janus/Claudio/Charles use normal assignments to real Cabin12;Julio uses only two declared elapsed counters;Emilio uses one declared Cabin-occupant byte,with faction21 and every other RAM byte preserved. '
        'The15-character Mmm,delicious first row retains the full Sneaking continuation at x16. All three normal town-return checks preserve scoped funds,calendar,31 roles,owned companion records and actual ship models. '
        'Registered V838 and exact clean-input patch retain471 batches,114 accepted layers,3643 other COMMON strings,all graphics/scripts/HELP/ARM7/overlays and fixed123040 staged bytes;seven ordinary startup frames pass. '
        'Native RTTI/widget labels and animated image-header flag assumptions are corrected from original code without changing earlier bytes or captures. '
        '671 entries complete (485 revised/186 retained),674 source/prose reviewed;three older750-752 drafts and all remaining unreviewed shared/route/player prose/raw-source work remain. '
        'Samwell middle-name glyph,older record re-audit and separate graphics/all18 plaques stay open;canonical not promoted;full goal active.')
    ledger['latest_checkpoint']=checkpoint
    ledger['research_checkpoints'].append({'id':'V841-Deck-personal-comments-complete','documentation':str(DOC),
        'proof':str(closure),'actual_proof':final['actual_gameplay_proof'],'completed_entries_added':25,
        'previous_goal_turn_classification':'progress:V838 registered integration,exact patch,native copies and startup',
        'this_goal_turn_classification':'progress:ordinary Cabin source path,ten complete actual holds,three normal returns and25-entry completion',
        'whole_goal_complete':False})
    before_ledger=read(ROOT/'editorial_ledger_before_completion.json')
    assert sum(ledger['completed_editorial_record_counts_by_file'].values())==671
    assert sum(ledger['source_prose_reviewed_counts_by_file'].values())==674
    assert ledger['unresolved_graphics_work']==before_ledger['unresolved_graphics_work']
    assert ledger['older_record_reaudit_after_full_editorial_goal']==before_ledger['older_record_reaudit_after_full_editorial_goal']
    assert not ledger['full_goal_complete']
    save(LEDGER,ledger);save('out/editorial_review_latest.json',candidate)
    DOC.write_text('# V841: Deck personal-comment editorial completion in V838\n\n'+checkpoint+'\n\n'
        '## Actual verification scope\n\n'+gameplay['scope']+'\n\n'
        'Both original source branches were mapped:normal healthy/normal-mood Cabin role12 or role16 uses1361+actor,as does the transient leisure path. '
        'The25 ordinary helper probes are controlled numeric-selector tests,not25 actual scene visits. Actual selections,room occupants,complete252x36 native body planes,independent words,and216x36 visible ink/blank pixels are checked for every sampled hold. '
        'The original parent projection preserves all other drawing commands,frame and palette;old144x24 crops lose verified text on the longer samples.\n\n'
        'Back cancels proposed assignments;Finish confirms them. The first unsuccessful activity attempts backed out and therefore left sailors unassigned. '
        'The later assignments and normal cancel/return behavior are verified from the actual31-byte occupant bank. The earlier V838 long sailing attempt ran out of food and was excluded. '
        'The V840 assumption that Charles had an odd first line failed:his line has28 characters. Its failed verifier is preserved;V841 adds the real15-character Emilio case instead of changing the English or weakening the odd-row gate. '
        'The actual animated bitmap header is1404h;original01FF9344 reads the format with LDRB. Exact native flag bits are preserved. '
        'Exact RTTI identifies the body as CDeckCabinInfoView and its parent as CDeckPersonnelView;earlier adjacent-name labels are corrected in a separate erratum.\n\n'
        '## Release and progress\n\n'
        f'- Candidate: `E:/Rota Nova translations/Generated/out/{ROM.name}`\n- SHA-256: `{candidate["sha256"]}`\n'
        f'- Profile: `{candidate["profile"]}`;experimental,canonical not promoted.\n'
        f'- Canonical base: `out/raphael_natural_v2_accepted_base.nds`;SHA-256 `{manifest["base_sha256"]}`.\n'
        f'- Exact clean-input patch: `{ROM.with_suffix(".xdelta").name}`;SHA-256 `{candidate["patch_sha256"]}`.\n'
        f'- Clean input SHA-256: `{release["clean_input_sha256"]}`.\n'
        f'- Final per-record review: `{REVIEW}`.\n- Release closure: `{closure}`.\n\n'
        'Only COMMON and ARM9 native selection metadata/two crop-size words differ from V834. No executable code,section,BSS,cache,arena,staged payload,route or graphics change is added. '
        'Fresh late-stage replay,all-other-component comparison,dependency hashes,ROM/patch/reconstruction hashes and inherited manifest checks pass. '
        'The original pending V838 verification remains immutable;the V841 closure adds actual evidence. Human cold-boot acceptance is still required before canonical promotion.\n\n'
        'Every generated ROM,patch,proof and capture is on E:. Five native guide-candidate screenshots retain exact source hashes and fixture provenance. '
        'The wider editorial goal,three older context drafts,raw-source revisit,Samwell name-header lead and separate graphics audit remain unfinished.\n',encoding='utf-8')
    paragraph='\n\n## V841: Deck personal comments complete\n\n'+checkpoint+' See [V841 evidence](personal_chatter_v841_completion.md).\n'
    for name in ('docs/translation_progress.md','docs/editorial_review_goal.md','docs/todo.md','docs/known_issues.md'):
        with Path(name).open('a',encoding='utf-8') as f:f.write(paragraph)
    GUIDE.mkdir(parents=True)
    guide=[]
    for case,frame,number,name in [('Rafael',10220,1367,'Julio'),('Rafael',14500,1365,'Janus'),
        ('Rafael',15500,1366,'Claudio'),('Charles',4800,1379,'Charles'),('Emilio',4200,1375,'Emilio_SYNTHETIC_OCCUPANT')]:
        source=CAP/CASES[case][0]/f'frame_{frame:06d}_navigation.png'
        target=GUIDE/f'V838_Deck_{name}_COMMON{number}.png';copy2(source,target)
        assert sha(source.read_bytes())==sha(target.read_bytes())
        guide.append({'source':str(source),'guide_copy':str(target),'sha256':sha(target.read_bytes()),
            'frame':frame,'case':case,'message_id':number,'native_size':[256,384],
            'fixture':'one Cabin-occupant byte;foreign faction21 retained;not earned recruitment' if case=='Emilio'
                else 'two elapsed counters for native leisure animation' if number==1367 else 'normal Cabin assignment,no new role or timing fixture',
            'historical_isolated_donor_no_earned_fleet_or_progression_claim':True})
    save(GUIDE/'capture_provenance.json',{'candidate':candidate,'proof':final['actual_gameplay_proof'],
        'guide_candidates_not_a_complete_published_guide':True,'captures':guide})
    sources=set()
    for folder in ('work/analysis/personal_chatter_v839','work/analysis/personal_chatter_v840','work/analysis/personal_chatter_v841'):
        sources.update(p for p in Path(folder).rglob('*') if p.is_file())
    sources.update(map(Path,(str(LEDGER),str(REVIEW),str(DOC),str(MANUSCRIPT),owned.CONFIG,
        'translations/release_stack.json','out/editorial_review_latest.json','scripts/build_integrated_release.py',
        'scripts/native_deck_elapsed_fixture_v839.py','scripts/run_deck_elapsed_adapter_v839.py',
        'scripts/run_personal_activity_v839.py','scripts/run_personal_cabin_v840.py',
        'scripts/native_emilio_cabin_fixture_v841.py','scripts/run_emilio_cabin_adapter_v841.py',
        'scripts/run_personal_emilio_v841.py','scripts/verify_personal_gameplay_v840.py',
        'scripts/verify_personal_gameplay_v841.py','scripts/verify_personal_cabin_context_v841.py',
        'scripts/record_personal_completion_v841.py','docs/translation_progress.md','docs/editorial_review_goal.md',
        'docs/todo.md','docs/known_issues.md',str(prior_release),'work/analysis/personal_chatter_v838/ordinary_startup_verification.json')))
    sources.update(map(Path,read(owned.CONFIG)['dependencies']))
    sources.update((ROM.with_suffix('.manifest.json'),ROM.with_suffix('.xdelta')))
    archived=[]
    for source in sorted(sources):
        target=ARCHIVE/source.absolute().relative_to(Path.cwd());target.parent.mkdir(parents=True,exist_ok=True)
        copy2(source,target);assert sha(source.read_bytes())==sha(target.read_bytes())
        archived.append({'source':str(source),'archive':str(target),'sha256':sha(target.read_bytes())})
    for folder,frames in CASES.values():
        for name in ('capture_report.json','navigation_command_journal.json'):
            source=CAP/folder/name;target=ARCHIVE/'captures'/folder/name
            target.parent.mkdir(parents=True,exist_ok=True);copy2(source,target)
            assert sha(source.read_bytes())==sha(target.read_bytes())
            archived.append({'source':str(source),'archive':str(target),'sha256':sha(target.read_bytes())})
    save(ROOT/'archive_manifest.json',{'archive':str(ARCHIVE),'all_copies_hash_verified':True,'files':archived,
        'guide_candidates':str(GUIDE),'ROM_and_all_original_captures_already_on_E':True,'whole_goal_complete':False})
    print('Deck25 complete:671 total,485 revised,186 retained;674 source/prose reviewed and3 older reviewed drafts pending. Full goal and separate graphics audit remain open.',flush=True)


if __name__=='__main__':
    main()
