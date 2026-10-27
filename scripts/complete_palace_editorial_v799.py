"""Close the reviewed Palace family;retain the full editorial/graphics goals."""

from copy import deepcopy
from pathlib import Path
import shutil

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch import palace_editorial as prose
from dk4tool.patch import palace_label_boundaries as labels
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save

ROOT=labels.ROOT
DOC=Path('docs/palace_editorial_v799_checkpoint.md')
LEDGER=Path('translations/editorial_review_current_v1.json')
METADATA=Path('translations/palace_editorial_manuscript_v4.json')
ARCHIVE=Path('E:/Rota Nova translations/Editorial review/V799 Palace completion and menu boundaries')
GUIDE=Path('E:/Rota Nova translations/Strategy Guide/Screenshots/V799 Palace verified')
IDS=tuple(range(1146,1177))


def main():
    assert not DOC.exists() and not METADATA.exists() and not ARCHIVE.exists()
    registered=read(ROOT/'registered_verification.json');actual=read(ROOT/'actual_family_verification.json')
    geometry=read(ROOT/'actual_menu_geometry_verification.json')
    assert registered['candidate_sha256']==actual['candidate_sha256']==geometry['candidate_sha256']
    assert len(actual['sixteen_actual_holds'])==16 and geometry['total_actual_rows']==12
    assert actual['seven_startup_whole_frames_exact'] and actual['all_original_donor_saves_unchanged']
    assert read('work/analysis/palace_gameplay_v798/treasure_gameplay_verification.json')['item_reclaimed_all_persistent_objects_match_post_fixture_start']
    prior_cancel=read(prose.ROOT/'contract_gameplay_verification.json')
    assert prior_cancel['quote_extra_blank_page_removed_one_A_reaches1157']
    assert prior_cancel['cash_models_actors_towns_items_goods_couriers_exact_initial_to_return']
    rom=NdsImage.open(registered['candidate']);common=rom.read_file('/COMMON/MESFILE.DK4');arm=rom.read_file('/__arm9__.bin')
    entries=labels.current_entries(common,arm);blocks=IlnkContainer.parse(common).blocks
    assert sha(Path(registered['candidate']).read_bytes())==registered['candidate_sha256']
    native=read(prose.ROOT/'production_layout.json');assert native['native_layouts']==323 and native['full_font_planes']==40 and not native['findings']
    assert native['COMMON_sha256']==sha(common)
    assert read('work/analysis/palace_runtime_v796/scope_proof.json')['cases']==35320
    assert read('work/analysis/palace_runtime_v796/status_contracts.json')['count']==140
    # Exact component preservation transfers the prior native/prose evidence;
    # the later patch changes only menu labels and six pointer fields.
    old=NdsImage.open('out/all_routes_combined_v797_candidate.nds')
    assert common==old.read_file('/COMMON/MESFILE.DK4')
    assert labels.plan(old.read_file('/__arm9__.bin'))[0]==arm
    prior=read('translations/palace_editorial_manuscript_v3.json')
    correction=read(ROOT/'guard_speaker_context_erratum.json')
    assert correction['clean_Japanese']=='衛兵' and correction['English']=='Guard'
    context=read('work/analysis/palace_editorial_v795/native_context.json')
    corrected=deepcopy(prior)
    for row in corrected['records']:
        n=row['message_id'];cases=[r for r in context['all31_original_message_call_fragments'] if r['id']==n]
        assert cases and entries[n].text==prose.compiled(row)
        speakers={r['speaker'] for r in cases}
        assert len(speakers)==1
        guard=speakers=={context['minister_role11_actor121']}
        assert guard or speakers=={context['ruler_role6_actor127']}
        row['speaker']='Original Palace guard,building role11(actor121 in Istanbul)' if guard else 'Original Palace ruler,building role6(actor127 in Istanbul)'
        row['context']=('Original source fragments '+', '.join(hex(r['source_fragment']) for r in cases)+
            ' bind this native message to '+row['speaker']+'. Original Palace contract capacity,Market-letter,'
            'defense and treasure-loan/return branches determine context,not adjacent storage. Source role11 '
            'is Guard:clean name衛兵;the earlier Minister assumption is superseded. Original name and amount '
            'providers remain in source argument order. Full31 source/native coverage and representative '
            'actual family samples are recorded in the V799 completion proof;not every individual branch '
            'or cultural speaker was separately activated.')
        row['localization_note']=row['localization_note'].replace('minister administrative','guard official').replace('Minister','Guard').replace('minister','guard')
        row['status']='editorially-complete-full-source-native-and-actual-family-samples'
    corrected.update({'metadata_only_correction_of':'translations/palace_editorial_manuscript_v3.json',
        'metadata_only_correction_source_sha256':sha(Path('translations/palace_editorial_manuscript_v3.json').read_bytes()),
        'source_context_erratum':str(ROOT/'guard_speaker_context_erratum.json'),
        'all_English_source_meanings_and_compiled_ROM_bytes_unchanged':True,
        'historical_registered_v3_and_research_v2_remain_immutable_for_reconstruction':True,
        'status':'completed-Palace-editorial-family;full-goal-incomplete'})
    assert [(r['message_id'],r['english'],r['source_meaning']) for r in corrected['records']]==[(r['message_id'],r['english'],r['source_meaning']) for r in prior['records']]
    validate_natural_dialogue_batch(corrected);save(METADATA,corrected)
    actual_ids=sorted({r['id'] for r in actual['sixteen_actual_holds']}|{r['message_id'] for r in prior_cancel['actual_repaired_holds']})
    assert len(actual_ids)==17
    map_path=ROOT/'complete_current_message_map_v799.json'
    save(map_path,{'candidate_sha256':registered['candidate_sha256'],'COMMON_sha256':sha(common),'ARM9_sha256':sha(arm),
        'current_exact3668_entry_selection_map':[{**vars(e),'text':{'sha256':sha(e.text),'bytes':len(e.text)},
            'complete_payload_sha256':sha(blocks[e.block][e.block_offset:e.copy_end])} for e in entries],
        'native_repacked_blocks_and_copies_proof':str(prose.ROOT/'registered_verification.json'),
        'mapping_inventory_does_not_claim_new_activation_of_all3668_messages':True})
    evidence_paths=[ROOT/'registered_verification.json',ROOT/'actual_family_verification.json',
        ROOT/'actual_menu_geometry_verification.json',ROOT/'newgame_regression.json',ROOT/'source_ownership.json',
        ROOT/'guard_speaker_context_erratum.json',prose.ROOT/'registered_verification.json',
        prose.ROOT/'production_layout.json',prose.ROOT/'contract_gameplay_verification.json',
        Path('work/analysis/palace_gameplay_v798/treasure_gameplay_verification.json'),METADATA]
    proof={'candidate':registered['candidate'],'candidate_sha256':registered['candidate_sha256'],
        'completed_COMMON_IDs':list(IDS),'revised':29,'retained':2,'corrected_metadata':str(METADATA),
        'six_additional_menu_labels':list(labels.LABELS),'complete_source_native_actual_evidence':{str(p):sha(p.read_bytes()) for p in evidence_paths},
        'actual_distinct_COMMON_IDs_across_samples':actual_ids,'native_cases_cover_all31':True,
        'not_all_branches_cultures_prices_or_voices_individually_activated':True,
        'source_guard_identity_corrected_without_changing_shipped_names_or_prose':True,
        'registered_ROM_and_clean_patch_exact':True,'native_and_actual_verification_complete_at_family_scope':True,
        'no_full_route_hardware_monthly_payment_or_graphics_completion_claim':True,'full_goal_complete':False}
    save(ROOT/'Palace_family_completion.json',proof)
    ledger=read(LEDGER);assert ledger['records_editorially_completed']==496 and ledger['records_with_source_and_prose_pass']==530
    assert ledger['records_revised_and_integrated']==359 and ledger['retained_wordings_editorially_completed']==137
    done={r['message_id'] for f in ledger['completed_editorial_families'] for r in f['records']};assert not done.intersection(IDS)
    save(ROOT/'editorial_ledger_before_completion_v799.json',ledger)
    family_name='Palace-contracts-Market-letters-defense-and-treasure-loans1146-1176'
    family={'id':family_name,'native_message_IDs':list(IDS),'records':[]}
    for row in corrected['records']:
        family['records'].append({k:row[k] for k in ('message_id','decision','english','source_meaning','speaker','context','source_hex')})
        family['records'][-1].update({'native_and_gameplay_family_evidence':str(ROOT/'Palace_family_completion.json'),
            'full_source_native_coverage_and_actual_consumer_family_samples':True,'individual_branch_activation_not_claimed':True})
    ledger['completed_editorial_families'].append(family)
    ledger['records_editorially_completed']=527;ledger['records_revised_and_integrated']=388
    ledger['retained_wordings_editorially_completed']=139
    active=ledger['active_source_prose_drafts'];active['native_message_IDs']=[n for n in active['native_message_IDs'] if n not in IDS]
    assert active['native_message_IDs']==[750,751,752]
    active['manuscripts']=[p for p in active['manuscripts'] if 'palace_editorial_manuscript' not in p]
    active['status']='750-752-context-unmapped'
    active['note']='Palace31 complete at full source/native and actual-family scope in V799.750-752 remain context-unmapped. Wider shared text,all route scenes and help/other prose remain unfinished.'
    ledger['additional_completed_player_facing_label_families']=[{'id':'six-Palace-menu-labels',
        'manuscript':'translations/palace_menu_labels_manuscript_v1.json','records':list(labels.LABELS),
        'proof':str(ROOT/'actual_menu_geometry_verification.json'),'counted_separately_from_COMMON_totals':True}]
    for finding in ledger['findings']:
        if finding['id']=='Palace-Contract-Cstring-no-NUL':
            finding.update({'status':'corrected-integrated-all-six-actual-menu-fonts-and-bounds-verified-V799',
                'repair_proof':str(ROOT/'actual_menu_geometry_verification.json')})
        elif finding['id']=='Palace1162-insufficient-funds-meaning':
            finding.update({'status':'corrected-integrated-actual-low-funds-quote-and-Guard-warning-verified-V799',
                'repair_proof':str(ROOT/'actual_family_verification.json')})
    ledger['palace_speaker_context_erratum']={'evidence':str(ROOT/'guard_speaker_context_erratum.json'),
        'correction':'Ruler role6/actor127;Guard role11/actor121 in Istanbul. Clean role11 name is衛兵. Earlier Minister terminology and earlier role4 ruler lookup are superseded.',
        'reviewed_metadata':str(METADATA),'historical_manuscripts_preserved':True,'English_and_ROM_unchanged_by_metadata_correction':True}
    ledger['palace_next_source_packet']['completion_credit']=31
    ledger['palace_next_source_packet']['completed_proof']=str(ROOT/'Palace_family_completion.json')
    ledger['palace_next_source_packet']['reviewed_metadata']=str(METADATA)
    ledger['palace_next_source_packet']['next']='Palace family complete;review shared1177 onward and map older750-752,then all routes and remaining prose.'
    ledger['current_native_relocation_reference']=str(map_path)
    ledger['current_integrated_candidate']={'path':registered['candidate'],'sha256':registered['candidate_sha256'],
        'profile':registered['profile'],'MESFILE_sha256':registered['COMMON_sha256'],'ARM9_sha256':registered['ARM9_sha256'],
        'patch_sha256':registered['patch_sha256'],'manifest':str(Path(registered['candidate']).with_suffix('.manifest.json')),
        'status':'experimental-Palace-editorial-family-and-menu-boundaries-verified','details':str(DOC),
        'supplemental_verification':str(ROOT/'Palace_family_completion.json'),
        'remaining_in_this_registered_batch':'Palace31 and six menu labels complete at reviewed source/native plus actual-family scope. Wider shared prose,older750-752 contexts,all route review and help/other prose remain incomplete.',
        'full_goal_complete':False}
    ledger['coverage_units'][0]['completed_families'].append(family_name)
    ledger['coverage_units'][0]['next']='Review shared1177 onward from clean Japanese and original native context;map750-752,then Lil and remaining route scenes and help/other prose. Preserve the separate unfinished graphics audit.'
    ledger['formatting_watchlist']['latest_reference_proof']=str(ROOT/'registered_verification.json')
    ledger['formatting_watchlist']['reference_case']+=' V799 preserves every COMMON byte from V797,including repaired676/677 and arrival346-348. Six Palace menu strings now have owned NULs;all six actual font masks and bounds pass at original native positions. No new shop676/677 activation claimed.'
    ledger['older_record_reaudit_after_full_editorial_goal']={'status':'pending-after-full-editorial-goal',
        'note':'Keep the requested follow-up to revisit old record-based checks. V799 concrete examples include stale Guild tail now used for India,an ambiguous cannon-tail last zero,nonterminated exact-capacity Contract,and a name-pointer record that must be dereferenced before Japanese decoding.'}
    summary=('V799 completes31 Palace COMMON entries(29 revised/2 retained) and six separately counted menu labels. '
        'Full31 source/native review,323 layouts,40 fonts,5076 complete copies and representative actual families pass. '
        'Seventeen distinct COMMON IDs are actually sampled across V797/V798/V799;not every individual branch is claimed played. '
        'Paid contract deducts2842 and grants1percent share;low funds quote1149 then Guard1162 returns to menu without charge. '
        'Recommendation grants trade and is consumed;introduction refusal retains the letter and funds. '
        'Defense charges3000;original whole-Town transaction replays match. Treasure loan/reclaim matches original transfers. '
        'Twelve actual menu rows prove all six complete font masks and bounds from original native geometry. '
        'Seven startup frames match;clean-input patch reconstructs exactly. '
        'Role11 is Guard(衛兵),not Minister;V4 corrects metadata with English/ROM unchanged. '
        '527 COMMON complete(388 revised/139 retained),530 source-prose reviewed,three older reviewed contexts750-752 pending. '
        'Wider shared text,all route scenes,other prose and separate graphics audit remain unfinished;full goal active.')
    ledger['latest_checkpoint']=summary
    ledger['research_checkpoints'].append({'id':'V799-Palace31-and-six-menu-labels-complete',
        'documentation':str(DOC),'new_editorially_completed_COMMON':31,'additional_completed_UI_labels':6,
        'new_ROM':True,'full_goal_complete':False})
    save(LEDGER,ledger);save('out/editorial_review_latest.json',ledger['current_integrated_candidate'])
    save(Path(registered['candidate']).with_suffix('.verification.json'),{**proof,'latest_editorial_counts':{
        'COMMON_complete':527,'revised':388,'retained':139,'source_prose_reviewed':530,'older_contexts_pending':[750,751,752]},
        'separate_graphics_audit_incomplete':True,'canonical_promotion':False})
    DOC.write_text('# V799: Palace editorial completion and menu boundaries\n\n'+summary+'\n\n'
        '## Registered experimental candidate\n\n'
        f"ROM: `{registered['candidate']}`\n\nSHA-256: `{registered['candidate_sha256']}`\n\n"
        f"Patch SHA-256: `{registered['patch_sha256']}`\n\n"
        'Profile `all-routes-unified-v799` retains all470 batches and114 accepted layers,all earlier profiles '
        'and pinned dependencies. Canonical parent remains `out/raphael_natural_v2_accepted_base.nds`, '
        'SHA-256 `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`. '
        'Only ARM9 changes from V797;every COMMON byte,route and graphic is unchanged. '
        'The clean-input xdelta reconstructs the exact candidate. No canonical promotion.\n\n'
        '## What was verified\n\n'
        'Three V799 cold boots exercise expanded menus/loan and reclaim/Market letters/defense, '
        'ordinary paid contract,and isolated insufficient funds. A separate ordinary New Game run '
        'matches seven whole frames. Sixteen complete body-font holds cover the sampled Palace scenes. '
        'The earlier V797 cancellation sample supplies the seventeenth distinct activated ID and '
        'removed-blank-page proof;its paragraph/dispatcher components remain exact. '
        'V798 independently verifies full loan/reclaim persistent-object transfers. '
        'The current17 actually sampled IDs are '+', '.join(map(str,actual_ids))+'.\n\n'
        'All31 paragraphs have clean Japanese/context/prose review,323 production layouts,40 independent '
        'font planes,35320 selector/ABI cases,140 status-output guards,and5076 complete warm/cold copies. '
        'Those counts describe native coverage;they do not mean every culture,voice,rare-item price '
        'or refusal branch was played. Native original transaction prefixes independently reproduce '
        'the full108-byte city records after paid contract and military contribution. '
        'Unrelated daily random world objects are not globally approved. No calendar month elapsed '
        'in loan tests,so recurring payout or full-route/hardware playthrough is not claimed.\n\n'
        '## Menu boundary repair\n\n'
        'The inherited eight-byte Contract string had no room for its NUL and read adjacent RTTI '
        'and Military Investment data. Six source menu pointers now address complete strings inside '
        'existing typed C-string spans. The following vtable zero/RTTI/method words are preserved. '
        'Labels are Contract,Military Investment,Recommendation,Introduction,Lend Item,Reclaim. '
        'Reclaim means requesting one\'s own loaned item back;the adjacent Lend Item action supplies '
        'the item context. Both letter types remain distinct. Twelve actual rows across4-,5- and3-row '
        'menus match every native font pixel and blank row,including first/final letters. '
        'Positions come from the original descriptor\'s virtual width,margin and rectangle methods '
        'and its live UI object,not from the tested glyphs. A final registered build guard checks '
        'all six complete NUL-terminated labels inside their owned spans.\n\n'
        '## Source metadata correction\n\n'
        'Role11/actor121 is the Guard:clean name pointer121A80 resolves to215B9F0,衛兵. '
        'Earlier Minister terminology was an assumption. `palace_editorial_manuscript_v4.json` '
        'corrects the reviewed speaker/context metadata while preserving every English paragraph, '
        'source gloss and compiled byte from immutable registered V3. Ruler role6/actor127 remains '
        'the actual King in these Istanbul scenes. Historical source/production artifacts stay intact '
        'for reconstruction;the new metadata and ledger are authoritative for editorial context.\n\n'
        '## Remaining goal scope\n\n'
        'Shared1177 onward,older750-752 contexts,all route-scene review and help/other prose remain '
        'unfinished. Alchemy Book2828 and the observed Rocco sailing-guide prose remain wider-review '
        'leads. The independent graphics audit and18 plaques stay open;the accepted material style '
        'is not a completion claim. Online low-resolution bodies stay excluded;brown marks and '
        'approved names remain unchanged. Keep the requested older-record audit follow-up after '
        'the full editorial goal. V799 is experimental until explicit user cold-boot acceptance; '
        'canonical acceptance is not inferred from automated verification.\n',encoding='utf-8')
    for name in ('known_issues','todo','translation_progress','editorial_review_goal'):
        p=Path('docs')/(name+'.md');p.write_text(p.read_text(encoding='utf-8')+'\n\n## V799: Palace31 and six menu labels complete\n\n'+summary+
            ' See [V799 checkpoint](palace_editorial_v799_checkpoint.md).\n',encoding='utf-8')
    GUIDE.mkdir(parents=True,exist_ok=True);guide=[]
    chosen=[r for r in actual['sixteen_actual_holds'] if r['id'] in (1153,1176,1154,1160,1155,1174,1159,1149,1162)]
    for row in chosen:
        source=Path(row['capture']['path']);dest=GUIDE/f"COMMON{row['id']}_verified.png"
        assert not dest.exists();shutil.copy2(source,dest);assert sha(source.read_bytes())==sha(dest.read_bytes())
        guide.append({'id':row['id'],'source_capture':str(source),'path':str(dest),'sha256':sha(dest.read_bytes())})
    for frame in (4400,7400,11800):
        source=Path('E:/Rota Nova translations/Generated/work/emulation_v193/palace_v799_expanded_menu')/f'frame_{frame:06d}_navigation.png'
        dest=GUIDE/f'Palace_menu_{frame:06d}_verified.png';assert not dest.exists();shutil.copy2(source,dest)
        assert sha(source.read_bytes())==sha(dest.read_bytes());guide.append({'menu_frame':frame,'path':str(dest),'sha256':sha(dest.read_bytes())})
    save(GUIDE/'provenance.json',{'screenshots':guide,'candidate_sha256':registered['candidate_sha256'],
        'disclosed_location_headquarters_inventory_and_letter_fixtures_where_applicable':True,
        'guide_images_are_actual_captures_not_mockups':True,'candidate_experimental':True,'full_goal_complete':False})
    files=[DOC,LEDGER,METADATA,Path('translations/release_stack.json'),Path('translations/palace_menu_labels_manuscript_v1.json'),
        Path('translations/palace_label_boundaries_release_v1.json'),Path('dk4tool/patch/palace_label_boundaries.py'),
        Path('scripts/build_integrated_release.py')]
    files+=list(ROOT.glob('*.json'))+list(ROOT.glob('*.png'))
    files+=[Path('scripts')/n for n in ('prepare_palace_labels_v799.py','register_palace_labels_v799.py',
        'native_palace_fixture_v799.py','run_palace_capture_v799.py','verify_palace_labels_release_v799.py',
        'verify_palace_menu_geometry_v799.py','verify_palace_families_v799.py','complete_palace_editorial_v799.py')]
    copies=[]
    for source in sorted(set(files)):
        assert not source.is_absolute();dest=ARCHIVE/source;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,dest)
        assert sha(source.read_bytes())==sha(dest.read_bytes());copies.append({'source':str(source),'copy':str(dest),'sha256':sha(dest.read_bytes())})
    receipt={'copies':copies,'all_copies_SHA256_exact':True,'guide_candidates':guide,'full_goal_complete':False}
    save(ROOT/'archive_receipt.json',receipt);save(ARCHIVE/'archive_receipt.json',receipt)
    print(f'Palace31+6 labels complete;527 COMMON total,530 source/prose,three older contexts pending. {len(copies)} exact archive copies;{len(guide)} guide screenshots. Full goal active.',flush=True)


if __name__=='__main__':main()
