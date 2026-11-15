"""Record nine completed Market entries and preserve all remaining goal scope."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.prepare_market_replies_v753 import CONFIG, MANUSCRIPT, ROOT
from scripts.record_memory_streams_v682 import copy
from scripts.verify_village_wrap_v608 import read, save

ROM=Path('out/all_routes_combined_v753_candidate.nds')
LEDGER=Path('translations/editorial_review_current_v1.json')
DOC=Path('docs/market_replies_v753_checkpoint.md')
ARCHIVE=Path('E:/Rota Nova translations/Editorial review/V753 Market replies')


def main():
    native,registered,gameplay,patch=(read(ROOT/name) for name in ('native_review.json','registered_verification.json','gameplay_verification.json','patch_proof.json'))
    manifest=read(ROM.with_suffix('.manifest.json'));doc=read(MANUSCRIPT);config=read(CONFIG)
    assert manifest['candidate_sha256']==sha(ROM.read_bytes())==registered['candidate_sha256']==gameplay['candidate_sha256']==patch['candidate_sha256']
    assert len(native['all9_complete_font_planes'])==9 and registered['all7336_complete_ARM946_warm_cold_copies']
    assert len(gameplay['actual_complete_dialogue_holds'])==17 and len(gameplay['cross_frame_menu_blink_phase_controls'])==3
    assert {r['message_id'] for r in gameplay['actual_complete_dialogue_holds']}=={747,748,762,763}
    assert patch['whole_ROM_byte_exact'] and all(registered['rejection_controls'].values())
    ledger=read(LEDGER);assert ledger['records_editorially_completed']==93 and ledger['records_revised_and_integrated']==62
    save(ROOT/'editorial_ledger_at_V752.json',ledger)
    image=NdsImage.open(ROM);entries=common_message_entries(image.read_file('/COMMON/MESFILE.DK4'),image.read_file('/__arm9__.bin'),clean=False)
    family='Market-investment-and-transaction-replies'
    ledger['completed_editorial_families'].append({'id':family,'native_message_IDs':[r['message_id'] for r in doc['records']],
        'records':[{'message_id':r['message_id'],'decision':'revised-and-integrated' if r['decision']=='revise' else 'retain-wording',
            'manuscript':str(MANUSCRIPT),'complete_source_context_and_native_font_verified':True,
            'actual_gameplay_display_verified':r['message_id'] in (747,748,762,763),
            'integrated_reference':{'block':entries[r['message_id']].block,'record':entries[r['message_id']].record_index,'offset':entries[r['message_id']].block_offset}} for r in doc['records']],
        'integrated_ROM_sha256':manifest['candidate_sha256'],'proof':str(ROOT/'proof.json')})
    ledger.update({'records_editorially_completed':102,'records_revised_and_integrated':68,
        'retained_wordings_editorially_completed':34,'records_with_source_and_prose_pass':102,
        'records_with_source_prose_drafts_including730_pending_naturalness':103,
        'latest_checkpoint':'V753 nine Market replies completed:6 revised,3 retained. All7336 native copies pass; four actual dialogue IDs and investment state verified.730 and wider Market/shared/routes remain open.'})
    ledger['coverage_units'][0]['completed_families'].append(family)
    ledger['coverage_units'][0]['next']='Resolve full category arguments730; review Market750-752,754-761 and767 onward, including false stock/referral placeholders, then the wider shared prose, Lil and every other route. These IDs are a next packet, not the whole remaining-game inventory.'
    ledger['current_native_relocation_reference']={'profile':manifest['profile'],'blocks':[7,8,9,10],
        'exact310_message_map':str(ROOT/'registered_verification.json'),'all3659_unselected_text_bytes_exact':True,
        'historical_manuscript_reference_offsets_are_pinned_to_their_own_input_builds':True}
    ledger['findings'].extend([
        {'id':'COMMON-762-763-investment-praise-and-no-share-condition','native_message_IDs':[762,763],
            'status':'source-native-and-actual-gameplay-verified-integrated-V753',
            'detail':'Restore the trade-without-share restriction, admiring generosity and omitted flattery. Both native share branches and actual zero/positive-share scenes verified.'},
        {'id':'COMMON-765-invented-investment-cause','native_message_id':765,
            'status':'source-context-and-native-font-reviewed-integrated-V753',
            'detail':'Remove Since you are investing, absent from Japanese. Preserve extra market-share favor and reassurance. Whole bonus eligibility and actual765 activation are not claimed.'}])
    ledger['current_integrated_candidate']={'path':str(ROM),'sha256':manifest['candidate_sha256'],'profile':manifest['profile'],
        'MESFILE_sha256':config['target_common_sha256'],'ARM9_sha256':config['target_arm9_sha256'],
        'patch_sha256':patch['patch_sha256'],'status':'experimental','manifest':str(ROM.with_suffix('.manifest.json')),
        'initial_source_pins_retained_as_V743_reference_not_overwritten':True}
    assert ledger['active_source_prose_drafts']['native_message_IDs']==[730]
    save(LEDGER,ledger)
    category=read(ROOT/'category730_open_investigation.json')
    category.pop('other_five_menu_callers_must_keep_compact_strings',None)
    category['other_five_getter_branch_matches_require_preservation_and_full_caller_classification']=True
    category['several_known_menu_consumers_make_a_global_getter_change_inappropriate']=True
    save(ROOT/'category730_open_investigation.json',category)
    controls=sum(map(len,gameplay['whole_frame_unchanged_controls'].values()))
    DOC.write_text(f'''# V753: Market investment and transaction replies

Nine entries747-749,753 and762-766 complete editorial review: six revised and three retained wordings. Cumulative coverage is102 completed entries,68 revised and34 retained. Category730, further Market/shared prose, every route and remaining player-facing prose remain open. The graphics audit remains separately unfinished.

## Source and English

747 retains natural thanks and the effective-use promise.748 restores the startled objection that available money is insufficient and the request to return after earning more.749 restores the full-holds warning and instruction to buy less.753 retains the natural funds warning.762 restores the inability to trade without a share and the merchant's admiring generosity;763 restores omitted praise that the player differs from the others.764 restores the blunt charity refusal and pay-to-see condition.765 removes the invented investment cause and retains the additional share favor and reassurance.766 retains the idiomatic farewell. The clean Japanese, exact canonical/current input bytes, source gloss, reasons and per-record v2 gates are in the frozen manuscript.

Nine original literal/immediate loads and direct portrait calls are proven. Eleven original native decision fragments per clean/current build cover zero/positive share, insufficient/threshold/sufficient funds, zero/positive supplied investment amount and the paid-viewing price test. These are bounded source fragments with supplied registers/input amount; they do not claim full transactions or earned progress.765's complete bonus eligibility and actual activation are not claimed.

## Faithful allocation and native verification

The original block9 repacker lacked157 terminal padding bytes. The English was not cut to fit. The established V707/V708 whole-selection relocation method repacks310 messages545-854 into the same four native blocks7-10. Their new sizes are4076,4014,4050,4043, each within the original4096-byte cache limit. All3659 unselected message texts, including packed752 and earlier62 revisions, remain byte-exact. Physical NUL owners and some block boundaries move; logical IDs and complete selections are preserved. All37 other blocks remain exact. Metadata fields alone change in ARM9: no executable, font, section, staged pool, allocator or cache grows. The exact new directory hash is allowlisted; no arbitrary directory bypass is enabled.

All3668 messages receive complete ARM946 warm and cold copies:7336 checks verify first/final bytes, NULs, output guards, stack/return and native cache header/block paths. Host open/read boundaries supply exact file bytes; this is native loader verification, not physical disk I/O or a playthrough. Nine full native font planes and every generated line are independently matched against decoded game fonts and visually inspected. All18340 parent/ID dispatch cases remain unchanged. Source-context spans, rejection controls,470 batches,114 accepted layers,675 graphics and final release guards pass. The clean-input patch reconstructs every ROM byte exactly.

## Actual emulator tests

Six terminal7501-frame cold boots pair V752/V753 across an ordinary zero-share case with no fixture, a declared two-byte one-percent-share fixture, and a declared two-byte zero-wallet fixture. Isolated save destinations are used; protected original and disposable donor files retain their exact hashes. All other main RAM bytes are unchanged at fixture insertion. Seventeen whole text holds verify762/763/747/748, their blank paper and every outside pixel. Complete unique resident block9 bytes match the actual ROM.

{controls} same-frame whole-screen controls match. Two later Trade highlight controls match complete baseline screens at the corresponding animation phase. One Market-caption control at V753 frame6400 matches the entire baseline frame6401 exactly; a dedicated6360-6440 capture proves the neighboring phase and reproduces the original baseline6400. No UI pixels are masked to accept these phase controls. Amount-entry windows, subsequent return and navigation remain verified. Three pre/during/post state traces match baseline: positive investment debits2684 coins and adds2684 to the original investment accumulator only after blocking thanks747 closes. Low funds change neither. Immediate market share/growth values are recorded without inventing a bonus. Other five entries receive source/native-font coverage, not claimed actual activations.

An ordinary4000-frame New Game cold boot without save or fixtures matches all seven V752 baseline frames through intro, captain selection and story. No hardware or complete-route playthrough is claimed.

## Artifacts

- Candidate: `{ROM}`
- SHA256: `{manifest['candidate_sha256']}`
- Profile: `all-routes-unified-v753` (experimental)
- Patch: `{ROM.with_suffix('.xdelta')}`
- Patch SHA256: `{patch['patch_sha256']}`
- Clean source SHA256: `{patch['clean_source_sha256']}`
- Canonical base remains `out/raphael_natural_v2_accepted_base.nds`, SHA256 `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
- Changed internal file: `/COMMON/MESFILE.DK4`; ARM9 changes are the explicit directory/native-offset metadata map.

ROM/patch, evidence and labeled fixture screenshots are on E. Canonical promotion still requires explicit user acceptance. No live producer/harness/config dependency was edited. The extra caption capture resolves a concrete visual comparison risk. The one-block allocation failures are superseded research, not distributed builds.

## Next work

730 still needs a dedicated full-category argument path with verified read-only ownership. Several menu consumers and other branch matches prevent blindly changing the shared getter; the old171E48-172464 tail is runtime-owned, and C1A0 is a mutable bitmap. No bytes for730 were changed. Its research packet is not a completed translation. Continue Market750-752,754-761 and767 onward, including false stock/referral placeholders, then the wider shared inventory and every route. Original18 plaque objects, Online exclusions, preserved brown marks, graphics audit and later older-record follow-up remain unchanged.
''',encoding='utf-8')
    reports=('native_context.json','native_review.json','registered_verification.json','gameplay_verification.json','patch_proof.json','source_context_packet.json')
    save(ROOT/'proof.json',{'candidate':str(ROM),'candidate_sha256':manifest['candidate_sha256'],'profile':manifest['profile'],
        'reviewed_IDs':[r['message_id'] for r in doc['records']],'revised_IDs':native['revised_IDs'],'retained_wordings':native['retained_wording_IDs'],
        'verification_reports':{str(ROOT/f):sha((ROOT/f).read_bytes()) for f in reports},
        'all9_previews_actual_text_amount_and_return_screens_visually_inspected':True,
        'all3659_unselected_texts_prior62_revisions470_batches114_layers675_graphics_exact':True,
        'canonical_original_saves_harness_preserved_no_promotion':True,'editorial_ledger_sha256':sha(LEDGER.read_bytes()),
        '730_more_Market_shared_routes_and_graphics_audit_still_open':True,'full_goal_complete':False})
    summary=f'\n\n## V753: Market investment and transaction replies\n\nNine reviewed entries:6 revised,3 retained. Source restores investment praise/no-share condition, complete errors and removes an invented765 investment cause. The established whole-selection relocation preserves3659 unselected texts and cache limits. All7336 native copies,9 complete font planes,11 source decision fragments per build and final guards pass. Six paired Market cold boots verify17 complete762/763/747/748 holds and original post-thanks cash/investment state;{controls} same-frame controls and3 exact phase-matched controls pass. Ordinary New Game matches7 V752 frames. Registered470/114 combined V753 and exact clean patch preserve675 graphics and earlier prose. Total102 reviewed,68 revised,34 retained;730, further Market/shared/routes and graphics audit remain open. See [V753 checkpoint](market_replies_v753_checkpoint.md).\n'
    for name in ('todo.md','translation_progress.md','known_issues.md','release_build.md'):
        path=Path('docs')/name;text=path.read_text(encoding='utf-8');assert '## V753: Market investment and transaction replies' not in text
        path.write_text(text.rstrip()+summary,encoding='utf-8')
    save('out/editorial_review_latest.json',{**ledger['current_integrated_candidate'],'details':str(DOC),'full_goal_complete':False})
    shots=Path('E:/Rota Nova translations/Screenshots/Test fixtures/V753 Market replies')
    for number in (747,748,762,763):
        row=next(r for r in gameplay['actual_complete_dialogue_holds'] if r['message_id']==number)
        copy(Path(row['capture']['path']),shots/f'COMMON_{number}_controlled.png')
    save(shots/'provenance.json',{'candidate_sha256':manifest['candidate_sha256'],
        'ordinary_zero_share762_and747_as_well_as_declared_two_byte_share_and_wallet_fixtures':True,
        'earned_fixture_progress_not_claimed':True,'gameplay_proof':str(ROOT/'gameplay_verification.json'),
        'files':{p.name:sha(p.read_bytes()) for p in shots.glob('*.png')}})
    files=[DOC,LEDGER,MANUSCRIPT,CONFIG,Path('dk4tool/patch/market_replies_editorial.py'),ROOT/'proof.json',ROOT/'editorial_ledger_at_V752.json',
        *(ROOT/f for f in (*reports,'all9_previews_2x.png','category730_open_investigation.json','inputs_invest_probe.json')),
        *ROOT.glob('native_copies_block_*.json'),*(Path('scripts')/f for f in ('verify_market_context_v753.py','prepare_market_replies_v753.py',
            'verify_market_native_copies_v753.py','verify_market_release_v753.py','native_market_fixture_v753.py','run_market_capture_v753.py','verify_market_gameplay_v753.py')),Path(__file__)]
    for path in files:copy(path,ARCHIVE/path.name)
    save(ARCHIVE/'provenance.json',{'candidate_sha256':manifest['candidate_sha256'],
        'files':{p.name:sha(p.read_bytes()) for p in ARCHIVE.iterdir() if p.is_file() and p.name!='provenance.json'},'full_goal_complete':False})
    assert all(sha((ARCHIVE/name).read_bytes())==digest for name,digest in read(ARCHIVE/'provenance.json')['files'].items())
    print('V753 recorded:102 reviewed,68 revised,34 retained;full editorial goal remains active.',flush=True)


if __name__=='__main__':main()
