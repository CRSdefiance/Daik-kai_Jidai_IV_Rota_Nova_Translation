"""Close source730's draft and record full names with unchanged menu evidence."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_category_dialogue_v754 import CONFIG, MANUSCRIPT, ROOT
from scripts.record_memory_streams_v682 import copy
from scripts.verify_village_wrap_v608 import read, save

ROM=Path('out/all_routes_combined_v754_candidate.nds')
LEDGER=Path('translations/editorial_review_current_v1.json')
DOC=Path('docs/category_dialogue_v754_checkpoint.md')
ARCHIVE=Path('E:/Rota Nova translations/Editorial review/V754 Full category forecast')


def main():
    native,abi,registered,gameplay,patch=(read(ROOT/name) for name in ('native_review.json','lookup_native_ABI.json','registered_verification.json','gameplay_verification.json','patch_proof.json'))
    manifest=read(ROM.with_suffix('.manifest.json'));doc=read(MANUSCRIPT);config=read(CONFIG);row=doc['records'][0]
    assert manifest['candidate_sha256']==sha(ROM.read_bytes())==registered['candidate_sha256']==gameplay['candidate_sha256']==patch['candidate_sha256']
    assert len(native['all18_complete_dialogue_font_planes'])==18 and len(abi['all108_getter_cases'])==108
    assert len(abi['all18_original_Square_caption_planes_exact'])==18 and len(registered['native_copy_cases'])==120
    assert len(gameplay['actual_complete_category730_holds'])==6 and sum(map(len,gameplay['whole_two_screen_unchanged_menu_and_return_controls'].values()))==51
    assert patch['whole_ROM_byte_exact'] and all(registered['rejections'].values())
    ledger=read(LEDGER);assert ledger['records_editorially_completed']==102 and ledger['records_revised_and_integrated']==68
    assert ledger['active_source_prose_drafts']['native_message_IDs']==[730]
    save(ROOT/'editorial_ledger_at_V753.json',ledger)
    family='Square-full-category-forecast730'
    ledger['completed_editorial_families'].append({'id':family,'native_message_IDs':[730],
        'records':[{'message_id':730,'decision':'revised-and-integrated','manuscript':str(MANUSCRIPT),
            'complete_source_and_all18_full_argument_font_planes_verified':True,
            'all_menu_getter_words_and18_Square_caption_planes_exact':True,
            'three_actual_argument_classes_and_return_verified':True}],
        'integrated_ROM_sha256':manifest['candidate_sha256'],'proof':str(ROOT/'proof.json')})
    ledger.update({'records_editorially_completed':103,'records_revised_and_integrated':69,
        'records_with_source_and_prose_pass':103,'records_with_source_prose_drafts':103,
        'latest_checkpoint':'V754 completes730 with all18 full category arguments, unchanged compact menus and actual Seasonings/Precious Metals/Medicine scenes. Further Market/shared/routes and graphics audit remain open.'})
    assert ledger['retained_wordings_editorially_completed']==34
    ledger.pop('records_with_source_prose_drafts_including730_pending_naturalness',None)
    ledger['active_source_prose_drafts']={'native_message_IDs':[],'manuscripts':[],
        'note':'The earlier730-746 source packet is complete; the broader unreviewed Market/shared/routes inventory is not complete.'}
    ledger['coverage_units'][0]['completed_families'].append(family)
    ledger['coverage_units'][0]['next']='Review Market750-752,754-761 and767 onward, including false stock/referral placeholders; continue wider shared prose, Lil and every other route. These IDs are the next packet, not the whole remaining-game inventory.'
    ledger['findings'].append({'id':'COMMON-730-full-category-arguments','native_message_id':730,
        'status':'source-all18-native-arguments-compact-menu-raster-and-actual-gameplay-verified-integrated-V754',
        'detail':'Complete Seasonings, Delicacy, Precious Metals, Jewelry, Medicine and Sundries arguments. Original730 returnPC alone selects full names; all compact UI strings and Square pixels are exact. Existing table/code/name slots suffice without allocation growth.'})
    ledger['current_integrated_candidate']={'path':str(ROM),'sha256':manifest['candidate_sha256'],'profile':manifest['profile'],
        'MESFILE_sha256':config['target_common_sha256'],'ARM9_sha256':config['target_arm9_sha256'],
        'patch_sha256':patch['patch_sha256'],'status':'experimental','manifest':str(ROM.with_suffix('.manifest.json')),
        'initial_source_pins_retained_as_V743_reference_not_overwritten':True}
    save(LEDGER,ledger)
    master_path=Path('translations/town_events_editorial_manuscript_v1.json');master=read(master_path)
    for r in master['records']:
        if r['message_id']==730:
            for key in ('english','speaker','context','source_meaning','localization_note','decision','review'):r[key]=row[key]
            r.update({'status':'reviewed-and-integrated-V754-see-release-manuscript-and-proof','integrated_evidence':str(ROOT/'proof.json')})
    master['status']='all17-records-reviewed-and-integrated-across-V750-V754-see-individual-proofs';save(master_path,master)
    DOC.write_text(f'''# V754: full category names in the forecast

COMMON730 completes editorial review. Cumulative coverage is103 entries:69 revised and34 retained. The earlier730-746 source packet is now complete. Further Market/shared prose, every route, remaining player-facing prose and the separate graphics audit remain open. The full goal stays active.

## Natural English and complete arguments

> {row['english'].removesuffix('{PAD}')}

The source predicts one unspecified good within the named category will catch on soon, rather than every good in the category. The new paragraph preserves certainty and future sense in natural merchant language. Full arguments replace Cond., Delic., Metals, Jewels, Med and Goods only in this dialogue: Seasonings, Delicacy, Precious Metals, Jewelry, Medicine and Sundries. Other already complete category words remain unchanged. The clean Japanese category table binds all18 names; the existing UI category-name capitalization is retained. Actual shop/menu captions retain their original shorter words.

## Owned storage and schema

The global18-word table at ARM9 file11B444 is now an explicit private packed lookup: high8 bits hold the compact string's byte offset into the140-byte family at15A090; low24 bits hold the full pointer minus01800000. Getter C5BA0 decodes the appropriate value. Only original730 caller returnPC0205FC48 selects full names. Every other caller uses compact names. Future tools must call the native getter or use the pinned decoded maps, rather than interpret these words as raw pointers.

The complete compact family plus Seasonings, Precious Metals and Sundries fits138 bytes by sharing the complete Metals suffix. Existing read-only Delicacy/Jewelry/Medicine strings supply the other expansions. The old nested Square category helpers are consolidated without changing their Delicacy/Jewelry overrides. Existing code slots, two duplicate Fleet label slots and the already-unreferenced Dock B slot hold the decoder. The three Fleet header owners now point to the complete immutable Fleet suffix in Create Fleet. Exact source Japanese slots, all byte-aligned/unaligned data-pointer owners, every branch into the replaced code, source helper bytecode and the single table owner are checked. No mutable caption buffer or runtime-owned name tail is reused.

No section, staged payload, startup/cache wrapper, allocator, font, graphics palette or view grows. The decoder preserves the tested original negative/sentinel return values and caller ABI. Ownership reports list every changed span and restore all other bytes exactly. All3667 other message texts and40 other COMMON blocks remain byte-exact; only730's native offset changes. Earlier68 revisions,675 graphics and the full470-batch/114-layer stack are preserved.

## Native and actual visual verification

-108 original getter/caller cases:18 categories for five menu callers and the original730 caller; caller return, stack and saved registers pass.
-18 complete native Square caption planes and their contexts are byte-exact, including all768 palette indices; four fallback surfaces are also exact.
-36 negative/sentinel cases preserve original returns. Three Fleet header fields give complete Fleet bytes through the actual native printf routine, including the unaligned immutable suffix.
-18 executions of the unchanged original730 caller reach its original direct portrait call with the complete full-name pointer.
-18 complete native dialogue font planes match every glyph, first/last letter, blank cell and bound. All fit two readable lines and all previews were visually inspected. All18340 wrapper dispatch cases remain unchanged.
-120 guarded warm/cold native copies across block9 and its boundaries, seven rejection controls and final release guards pass. The clean-input patch reconstructs the entire ROM byte for byte.

Six terminal6501-frame cold boots pair V753/V754. Declared fixtures change only an original town trend pair and SDK seed, selecting actual runtime product categories. Static resource category byte6 differs from some initialized objects; fixtures therefore read the actual product category byte exactly as original5FC40 does. Products14/38/75 yield Seasonings/Precious Metals/Medicine. Six complete4600/4800 holds match every glyph and blank-paper pixel. Every outside pixel, including the compact Cond. Shop/Metals Shop/Med Shop captions, portraits, borders and palettes, matches baseline. Entire resident cache blocks are exact. All51 complete menu/return/control pairs match without phase masking. Other15 argument classes have native font/caller coverage, not claimed physical visits. Exact UI RNG draw count and earned trend creation are not claimed.

An ordinary4000-frame New Game cold boot uses no save or fixture and matches all seven V753 frames through intro, captain selection and story. Protected original and disposable donor saves retain their original hash. These are targeted emulator tests, not a hardware test or full-route playthrough.

## Artifacts

- Candidate: `{ROM}`
- SHA256: `{manifest['candidate_sha256']}`
- Profile: `all-routes-unified-v754` (experimental)
- Patch: `{ROM.with_suffix('.xdelta')}`
- Patch SHA256: `{patch['patch_sha256']}`
- Clean input SHA256: `{patch['clean_source_sha256']}`
- Canonical base remains `out/raphael_natural_v2_accepted_base.nds`, SHA256 `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
- Changed internal file: `/COMMON/MESFILE.DK4`; ARM9 changes are the owned lookup code/data, three Fleet-label pointers and730 native offset.

ROM/patch, exact reconstruction proof, native evidence and labeled fixture screenshots are on E. No live producer/harness/config dependency was edited. The initial owner count was corrected to the actual three Fleet owners; Dock B has no word-pointer owner. An internal branch inside the old helper is explicitly accounted for. Earlier research files without these completed guards are superseded. Canonical promotion still requires explicit user acceptance.

## Next work

Continue Market750-752,754-761 and767 onward, including false stock/referral placeholders; then wider shared prose, Lil and every other route. The source packet being closed here is only one part of the editorial goal. Graphics audit/original18 objects, Online exclusions, preserved brown marks and later older-record follow-up remain unchanged.
'''.replace('\n+-','\n- '),encoding='utf-8')
    reports=('lookup_ownership.json','lookup_native_ABI.json','native_review.json','registered_verification.json','gameplay_verification.json','patch_proof.json','source_context_packet.json')
    save(ROOT/'proof.json',{'candidate':str(ROM),'candidate_sha256':manifest['candidate_sha256'],'profile':manifest['profile'],
        'reviewed_IDs':[730],'revised_IDs':[730],'retained_wordings':[],
        'verification_reports':{str(ROOT/name):sha((ROOT/name).read_bytes()) for name in reports},
        'all18_previews_and_three_actual_full_category_screens_visually_inspected':True,
        'all3667_unselected_texts_prior68_revisions470_batches114_layers675_graphics_preserved':True,
        'canonical_source_saves_and_original_harness_preserved_no_promotion':True,
        'editorial_ledger_sha256':sha(LEDGER.read_bytes()),'full_goal_complete':False})
    summary='\n\n## V754: full category forecast730\n\nOne revision completes730 and the earlier730-746 packet. All18 full category arguments fit two complete native lines;108 native caller cases,36 sentinels,18 unchanged Square caption planes,four fallbacks and120 guarded copies pass. Existing owned lookup/code/string slots preserve compact menus without any section/cache growth. Six paired cold boots verify Seasonings/Precious Metals/Medicine, six whole text holds, unchanged compact captions and51 whole menu/return controls. Ordinary New Game matches7 V753 frames. Registered470/114 combined V754 and exact clean patch preserve earlier prose and675 graphics. Total103 reviewed,69 revised,34 retained;broader Market/shared/routes and graphics audit remain open. See [V754 checkpoint](category_dialogue_v754_checkpoint.md).\n'
    for name in ('todo.md','translation_progress.md','known_issues.md','release_build.md'):
        path=Path('docs')/name;text=path.read_text(encoding='utf-8');assert '## V754: full category forecast730' not in text
        path.write_text(text.rstrip()+summary,encoding='utf-8')
    save('out/editorial_review_latest.json',{**ledger['current_integrated_candidate'],'details':str(DOC),'full_goal_complete':False})
    shots=Path('E:/Rota Nova translations/Screenshots/Test fixtures/V754 Category forecast')
    seen=set()
    for r in gameplay['actual_complete_category730_holds']:
        if r['category'] in seen:continue
        seen.add(r['category']);copy(Path(r['capture']['path']),shots/f'COMMON730_category_{r["category"]}_controlled.png')
    save(shots/'provenance.json',{'candidate_sha256':manifest['candidate_sha256'],'original_trend_and_seed_fixtures':True,
        'earned_trend_not_claimed':True,'gameplay_proof':str(ROOT/'gameplay_verification.json'),
        'files':{p.name:sha(p.read_bytes()) for p in shots.glob('*.png')}})
    files=[DOC,LEDGER,MANUSCRIPT,CONFIG,Path('dk4tool/patch/category_dialogue_lookup.py'),Path('dk4tool/patch/category_dialogue_editorial.py'),
        ROOT/'proof.json',ROOT/'editorial_ledger_at_V753.json',*(ROOT/name for name in (*reports,'all18_dialogue_previews_2x.png','inputs_trends.json','actual_fixture_products.json')),
        *(Path('scripts')/name for name in ('verify_category_lookup_v754.py','prepare_category_dialogue_v754.py','verify_category_release_v754.py','native_category_trend_fixture_v754.py','run_category_capture_v754.py','verify_category_gameplay_v754.py')),
        Path('scripts/build_integrated_release.py'),Path('translations/release_stack.json'),Path(__file__)]
    for path in files:copy(path,ARCHIVE/path.name)
    save(ARCHIVE/'provenance.json',{'candidate_sha256':manifest['candidate_sha256'],
        'files':{p.name:sha(p.read_bytes()) for p in ARCHIVE.iterdir() if p.is_file() and p.name!='provenance.json'},'full_goal_complete':False})
    assert all(sha((ARCHIVE/name).read_bytes())==digest for name,digest in read(ARCHIVE/'provenance.json')['files'].items())
    print('V754 recorded:103 reviewed,69 revised,34 retained;730 resolved,broader goal active.',flush=True)


if __name__=='__main__':main()
