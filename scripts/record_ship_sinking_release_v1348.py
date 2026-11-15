"""Record the registered sinking candidate without original-scene completion."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/ship_sinking_checkpoint_v1348')
RELEASE = Path('work/analysis/ship_sinking_release_v1343')
MANUSCRIPT = Path('translations/ship_sinking_editorial_manuscript_v4.json')


def main():
    assert not ROOT.exists()
    release = read(RELEASE/'registered_release_verification.json')
    assert sha(Path(release['candidate']).read_bytes())==release['candidate_sha256']
    assert sha(Path(release['patch']).read_bytes())==release['patch_sha256']
    startup = read(RELEASE/'ordinary_startup_verification.json')
    assert startup['candidate_sha256']==release['candidate_sha256'] and len(startup['pairs'])==8
    assert startup['all8_complete_startup_title_NewGame_frames_exact']
    assert sha(Path(startup['review_sheet']).read_bytes())==startup['review_sheet_sha256']
    shop_path = RELEASE/'photographed_shop_formatting.json'
    shop = read(shop_path)
    assert shop['candidate_sha256']==release['candidate_sha256']
    assert all(r['no_authored_indent_internal_gap_or_stray_Discover'] for r in shop['entries'])
    doc = read(MANUSCRIPT)
    assert all(all(r['review'].values()) for r in doc['records']) and len(doc['records'])==16
    fonts = read(doc['native_font_proof'])
    assert len(fonts['cases'])==416 and not fonts['findings']
    ROOT.mkdir(parents=True)
    save(RELEASE/'ordinary_startup_visual_review.json',{'candidate_sha256':release['candidate_sha256'],
        'source_proof':str(RELEASE/'ordinary_startup_verification.json'),
        'source_proof_sha256':sha((RELEASE/'ordinary_startup_verification.json').read_bytes()),
        'all8_complete_frames_actually_visually_inspected':True,'review_sheet':startup['review_sheet'],
        'review_sheet_sha256':startup['review_sheet_sha256'],
        'scope':'Fixture-free no-save cold boots through title,New Game,Rafael biography/name confirmation and opening Claudio scene. Sinking events and their transitions are not covered.',
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    ledger_path = Path('translations/editorial_review_current_v1.json')
    ledger = read(ledger_path)
    before = deepcopy(ledger)
    assert (ledger['records_editorially_completed'],ledger['records_with_source_and_prose_pass'])==(1302,1395)
    assert len(ledger['reviewed_but_incomplete_COMMON_IDs'])==93
    save(ROOT/'coverage_before_native_release_checkpoint.json',before)
    ids = list(range(2058,2074))
    old = 'translations\\ship_sinking_editorial_manuscript_v1.json'
    drafts = ledger['active_source_prose_drafts']
    assert old in drafts['manuscripts'] and drafts['manuscript_record_subsets_pending'][old]==ids
    drafts['manuscripts'][drafts['manuscripts'].index(old)] = str(MANUSCRIPT)
    drafts['manuscript_record_subsets_pending'].pop(old)
    drafts['manuscript_record_subsets_pending'][str(MANUSCRIPT)] = ids
    drafts['note'] = 'Sixteen sinking notices now have source/prose/native-format approval and registered V1344 integration;original sinking events,GPU visibility,dismissals and transitions remain pending. Eight revised/eight retained.39 aftermath and38 older reviewed COMMON entries also remain incomplete;broader shared/routes/raw inventory remains open.'
    unit = next(r for r in ledger['coverage_units'] if r['id']=='Shared-ship-sinking16-source-prose')
    unit.update(status='source-prose-native-font-integrated;original-gameplay-pending',manuscript=str(MANUSCRIPT),
        registered_release_proof=str(RELEASE/'registered_release_verification.json'),
        completed_entries_added=0,full_goal_complete=False)
    ledger['latest_registered_ship_sinking_candidate'] = {**release,'status':'experimental-16-native-reviewed;original-sinking-scenes-pending',
        'manuscript':str(MANUSCRIPT),'native_font_cases':416,'source_voice_selections':412,
        'ordinary8_startup_frames_exact_and_visually_reviewed':True,
        'photographed_shop676_677_native_formatting_preserved':True,
        'original_sinking_events_GPU_dismissals_and_transitions_verified':False,'completed_entries_added':0,
        'full_goal_complete':False}
    formatting = ledger['formatting_watchlist']
    formatting['latest_photographed_shop_recheck'] = {'checkpoint':'V1348','candidate':release['candidate'],
        'candidate_sha256':release['candidate_sha256'],'proof':str(shop_path),
        'result':'676/677 exact repaired native wrapping and complete228x64 fonts pass. No fresh shop visit claimed.',
        'global_formatting_audit_complete':False}
    formatting['latest_reference_proof'] = str(shop_path)
    formatting['latest_user_screenshot_recheck'] = {'proof':str(shop_path),'candidate':release['candidate'],
        'exact_repaired676_677_bytes_preserved':True,'complete_native_wrapping_and_glyph_planes_rechecked':True,
        'new_actual_shop_activation_claimed':False,'global_formatting_audit_complete':False}
    summary = ('V1348 integrates sixteen source/prose/native-reviewed sinking reports2058-2073 into registered combined V1344:eight revisions,eight retained wordings. Source-mapped role/direct callers,412 existing actor voice selections and exactly one ship-name%s argument are preserved. Initial real-name orphan rows and long-name stress findings led to faithful idiomatic clause revisions,without authored padding/breaks.416 original native selection/substitution/macro-literal/wrap/full-font cases now pass with zero orphan/weak-end findings;all8 sheets/128 preview panels visually inspected. The actual ship-rename editor has18-byte capacity. V1335 stopped at a pre-existing40-byte atomic-append patch;V1335b verifies that registered patch,all other clean instructions and six success/intact-rejection boundaries.23/31-byte names remain extra stress,not legal-editor claims.529312 selector/ABI,7336 copies180 cache transitions13 escape pipelines pass;two memberships exactly fill188 owned bytes while every code byte,section/BSS/cache/ITCM/arena and123040 staged bytes stay unchanged. All471 manifest batches114 accepted layers,3652 unselected messages,other40 blocks,routes/graphics/fonts/components and opaque duel prefix are preserved. Exact clean-input patch reconstructs every ROM byte. Eight ordinary no-save startup/title/New Game frames match V1105 and were visually inspected;the photographed shop676/677 native formatting still passes. Original sinking events,GPU visibility,dismissals and transitions remain pending;no new completion credit. Counts1302 complete(970 revised332 retained),1395 source/prose,93 reviewed-incomplete COMMON(16 sinking39 aftermath38 older),plus broader unreviewed shared/routes/raw prose. Canonical,V997,current completed-native V1316,separate graphics/all18 plaques and later older-record re-audit remain unchanged/open;full goal active.')
    ledger['latest_checkpoint'] = summary
    ledger['research_checkpoints'].append({'id':'V1348-ship-sinking16-native-integrated',
        'candidate':release['candidate'],'manuscript':str(MANUSCRIPT),'native_font_proof':doc['native_font_proof'],
        'release_proof':str(RELEASE/'registered_release_verification.json'),'completed_entries_added':0,
        'source_prose_reviews_added':0,'original_sinking_scene_verification_pending':True,'full_goal_complete':False})
    for key in ['records_editorially_completed','records_revised_and_integrated','retained_wordings_editorially_completed',
                'records_with_source_and_prose_pass','records_with_source_prose_drafts',
                'completed_editorial_record_counts_by_file','current_integrated_candidate','current_native_relocation_reference',
                'source_pins','reviewed_but_incomplete_COMMON_IDs','unresolved_graphics_work',
                'older_record_reaudit_after_full_editorial_goal','raw_source_coverage_revisit']:
        assert ledger[key]==before[key],key
    save(ledger_path,ledger)
    pin_path = Path('translations/rom_retention_pins.json')
    pins = read(pin_path)
    path = 'E:/Rota Nova translations/Generated/out/all_routes_combined_v1344_candidate.nds'
    assert not any(r['path']==path for r in pins)
    pins.append({'path':path,'reason':'Registered sinking-editorial candidate required for pending original event,GPU,dismissal and transition verification;keep V1316 as exact parent.'})
    save(pin_path,pins)
    text = '# V1348: sixteen sinking reports integrated; original events pending\n\n'+summary+'\n\n## Exact registered release\n\n'+\
        '- Candidate: `E:/Rota Nova translations/Generated/out/all_routes_combined_v1344_candidate.nds`; SHA-256 `'+release['candidate_sha256']+'`.\n'+\
        '- Profile: `'+release['profile']+'`;full471 manifest batches/114 accepted layers. Experimental,not user accepted.\n'+\
        '- Canonical base: `out/raphael_natural_v2_accepted_base.nds`; SHA-256 `'+release['canonical_sha256']+'`. Immediate layer parent:V1316 `f27f98ab3c2d6fb56623e916c12da85355585a5d64622f9637f7c08ff9ddf8aa`.\n'+\
        '- Changed internal files relative V1316: `/COMMON/MESFILE.DK4` block22 and `/__arm9__.bin` native offsets/directory plus existing188-byte selector data. No executable code change.\n'+\
        '- Patch: `out/all_routes_combined_v1344_candidate.xdelta`; SHA-256 `'+release['patch_sha256']+'`;clean input `'+release['clean_input_sha256']+'`. Every reconstructed byte matches.\n'+\
        '- Verifiers: `verify_ship_sinking_runtime_v1329.py`, `probe_ship_sinking_fonts_v1338.py`, `verify_ship_sinking_copies_v1339.py`, `verify_ship_sinking_escape_v1340.py`, `verify_ship_sinking_release_v1345.py`, `run_ship_sinking_startup_v1346.py --verify`, `recheck_shop_formatting_v1347.py`.\n\n'+\
        '## Remaining acceptance work\n\nUse original cold-boot battery-save gameplay with disclosed prebattle prerequisites only. Capture one representative fleet-ship sinking report and one enemy sinking-by-projectile report with their proper role/gunner portraits,complete resident block/template/expanded/wrapped text,whole native/independent/actual RGB font planes,two full holds,normal dismissals and original return/outcome. Preserve actors/IDs,RNG,eligibility/results and source/disposable saves. Do not reuse a table-adjacent capture notice as sinking evidence. The V652 ordinary five-ship preparation and V1281/V1283 source-guarded prebattle locations are leads,not current verification. No during-battle health/position/result changes. Extra23/31-byte CPU stress findings remain historical,not a reason to alter code or waive a valid-name defect. Name-editor page coverage and arbitrary legacy saved names are outside the18-byte capacity proof.\n\n'+\
        'The source/prose manuscript is `translations/ship_sinking_editorial_manuscript_v4.json`;the three earlier manuscripts and failed V1335 clean-equality probe remain frozen evidence. Native approval does not promote the layer or complete this family. The final startup visual receipt resolves the frozen startup producer visual-pending field without editing it. Shop676/677 retains the photographed formatting regression;no new shop activation is claimed.\n'
    Path('docs/ship_sinking_v1348_integrated_checkpoint.md').write_text(text,encoding='utf-8')
    for name in ['translation_progress.md','known_issues.md','todo.md','editorial_review_goal.md']:
        with (Path('docs')/name).open('a',encoding='utf-8',newline='\n') as handle:
            handle.write('\n\n## V1348 sinking native/integrated checkpoint\n\n'+summary+'\n\nSee [checkpoint](ship_sinking_v1348_integrated_checkpoint.md).\n')
    save(ROOT/'checkpoint_receipt.json',{'candidate_sha256':release['candidate_sha256'],'patch_sha256':release['patch_sha256'],
        'native_approved_and_integrated_entries':16,'completed_entries_added':0,'completed':1302,'source_prose':1395,
        'reviewed_incomplete_COMMON':93,'eight_startup_frames_visually_reviewed':True,
        'canonical_whole_batchV997_and_completed_nativeV1316_references_unchanged':True,
        'original_sinking_scenes_pending':True,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('V1344 exact registered ROM/patch,native416 and eight startup controls recorded. Original sinking scenes pending;1302 complete/1395 reviewed.',flush=True)


if __name__=='__main__':
    main()
