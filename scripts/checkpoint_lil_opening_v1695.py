"""Record49 new route prose reviews and scoped negative research;goal stays active."""
import json
import os
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/editorial_checkpoint_v1695')
LEDGER=Path('translations/editorial_review_current_v1.json')
DRAFT=Path('translations/lil_opening_editorial_manuscript_v1.json')
PACKET=Path('work/analysis/lil_opening_editorial_v1694/complete_opening_source_context.json')
NEGATIVE=Path('work/analysis/close_sighting_negative_v1693/terminal_negative_close_range_proof.json')
REFERENCES=Path('work/analysis/unmapped_shop_references_v1688b/broader_native_and_script_reference_inventory.json')


if __name__=='__main__':
    assert not ROOT.exists()
    raw=LEDGER.read_bytes();ledger=read(LEDGER);doc,packet,negative,refs=map(read,(DRAFT,PACKET,NEGATIVE,REFERENCES))
    assert ledger['records_editorially_completed']==1375 and ledger['records_with_source_and_prose_pass']==1519
    assert ledger['source_prose_reviewed_counts_by_file']=={'/COMMON/MESFILE.DK4':1518,'/data/SC2.DK4':1}
    assert len(ledger['reviewed_but_incomplete_COMMON_IDs'])==144
    ids=[r['id'] for r in doc['records']];assert len(ids)==len(set(ids))==49
    assert not ledger.get('reviewed_but_incomplete_route_record_IDs')
    assert all(r['review']=={'source':True,'context':True,'localization':True,'naturalness':True,'formatting':False} for r in doc['records'])
    assert doc['strict_build_validation_rejects_draft_until_formatting_review']
    assert packet['all49_native_speech_commands_exhaustively_accounted_for']
    assert packet['all90_native_command_offsets_words_and_extents_preserved']
    assert negative['no_close_range_Armed_Latina_or_editorial_completion_credit']
    assert refs['source_prose_reviews_added']==refs['completed_entries_added']==0
    probe=read(PACKET.parent/'allocation_probe_NOT_visual_approval.json');assert (probe['encodes'],probe['pending'])==(13,36)
    ROOT.mkdir(parents=True)
    (ROOT/'ledger_before.json').write_bytes(raw)
    handoff=Path('docs/editorial_handoff_current.md');(ROOT/'handoff_before.md').write_bytes(handoff.read_bytes())
    summary=('V1695 adds49 clean-source/context/prose reviews for the complete Lil Amsterdam opening,SC2 B22:43 proposed revisions and6 retained wordings. '
        'All49 original native speech commands and90 command offsets/words/extents are accounted for in clean/current3000-byte blocks. '
        'Current R0026/R0182 still say Kamil;drafts use approved Camille. Restore city contracts,tax-exemption explanation,preparation orders and omitted clauses. '
        'No ROM changed and no entries completed.13 drafts encode in the historical fixed profile;36 fail a mixture of capacity,literal-macro or pair-phase gates. '
        'No warnings waived,no guard weakened,no prose shortened merely to fit. Formatting,source-bound literal-macro/phase review,relocation if needed,native glyphs,registered integration/patch and actual complete-scene transitions remain. '
        '1375 complete(1033 revised342 retained),1568 source/prose reviewed;144 reviewed-incomplete COMMON plus49 route drafts and broader untouched prose. '
        'V1693 terminal5512 close-range test independently replays3 exact17-byte fixtures and audits all captured4MiB RAM and unchanged saves. '
        'The original game selected Dock at Syracuse?,then normal B No returned to directly viewed Sea View. No sighting/vicinity/Armed Latina UI credit. '
        'Null mobile pointer for an unloaded fleet is not inactivity proof;original fleet eligibility getter returns1. Next sighting context must avoid the port. '
        'V1688b production-script750/752 matches are validated CS-size fields;alternate CS0101 test header remains unclassified.750-752 stay context-unmapped. '
        'Current registered ROM is unchanged V1676 experimental,V1492 promoted. Full editorial goal remains active;separate graphics/all18 plaques remain open.')
    ledger['records_with_source_and_prose_pass']=1568
    ledger['records_with_source_prose_drafts']=1568
    ledger['source_prose_reviewed_counts_by_file']['/data/SC2.DK4']=50
    ledger['reviewed_but_incomplete_route_record_IDs']={'/data/SC2.DK4':ids}
    ledger['active_source_prose_drafts']['manuscripts'].append(str(DRAFT))
    ledger['active_source_prose_drafts']['route_record_subsets_pending']={str(DRAFT):ids}
    ledger['active_source_prose_drafts']['status']='144-reviewed-COMMON-and49-Lil-opening-route-drafts-open'
    ledger['active_source_prose_drafts']['note']='Earlier144 COMMON remain pending.49 new Lil opening prose drafts have no formatting/integration/gameplay completion credit. Broader shared/routes/player prose remains untouched.'
    for unit in ledger['coverage_units']:
        if unit['id']=='all-route-scenes':
            assert unit['status']=='not-started'
            unit.update(status='in-progress',first_editorial_scene='Lil Amsterdam opening,SC2 B22',source_context=str(PACKET),
                        source_prose_manuscript=str(DRAFT),reviewed_route_records=49,completed_route_records=1,
                        note='The earlier1 completed SC2 native message remains separate;these49 opening records are reviewed but incomplete. Every other route scene stays in scope.')
    ledger['coverage_units'].append({'id':'Lil-Amsterdam-opening49-source-prose','file_path':'/data/SC2.DK4','block':22,'record_IDs':ids,
        'status':'source-context-prose-reviewed;formatting-native-integration-actual-pending','manuscript':str(DRAFT),'source_context':str(PACKET),
        'proposed_revisions':43,'proposed_retentions':6,'completed_entries_added':0,'full_goal_complete':False})
    checkpoint={'summary':summary,'source_context':str(PACKET),'manuscript':str(DRAFT),'negative_actual_proof':str(NEGATIVE),
        'unmapped_shop_reference_proof':str(REFERENCES),'new_completed_entries':0,'source_prose_reviews_added':49,'full_goal_complete':False}
    ledger['lil_opening_editorial_v1695']=checkpoint
    ledger['latest_checkpoint']=summary
    assert not ledger['full_goal_complete']
    temporary=LEDGER.with_name('editorial_review_current_v1695_pending.json');assert not temporary.exists()
    save(temporary,ledger);assert read(temporary)==ledger and LEDGER.read_bytes()==raw
    os.replace(temporary,LEDGER)
    text='# V1695 Lil opening editorial and source-context checkpoint\n\n'+summary+'\n\n## Next steps\n\n'
    text+=('- Preserve the complete49-line manuscript and original49 speakers/commands. Audit source speech expansion before choosing a modern live route formatter. '
        'The old profile rejects literal uppercase I/F and several pair-phase boundaries;do not disable those guards or silently rewrite correct English to avoid them. '
        'Capacity failures require a complete independently reviewed relocation map or another source-proven allocation solution.\n'
        '- Generate and inspect every formatted/native glyph page,then register the full cumulative profile,reconstruct the exact patch,and cold-boot the entire opening through the Bruges transition. No scene completion until those gates pass.\n'
        '- Keep earlier144 COMMON,all other routes and remaining player prose open. Close-range label testing needs an original open-water context rather than the Syracuse port trigger. '
        'Armed Latina actual UI and successful Lookout-shot contexts remain separate. Do not replay completed hot-spring Search work.\n'
        '- No live emulator jobs remain. The V1690 run is terminal5512;negative proofV1693 records its exact limits.\n\n'
        '## Current integrated ROM\n\n'
        'Profile all-routes-unified-v1676,out/all_routes_combined_v1676_candidate.nds. '
        'Physical E:/Rota Nova translations/Generated/out/all_routes_combined_v1676_candidate.nds. '
        'ROM SHA256337edf22ab6ee96536aadb15fb461652149b157e8d9bd1ef60db998f97608510;'
        'patch SHA2564609fc580635481203103b4be3eee4690c70bbef98e41121ab679c40484e802f. '
        '473 manifest batches and114 accepted layers. Canonical construction baseline remains out/raphael_natural_v2_accepted_base.nds '
        'SHA2563cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe. '
        'V1492 remains the user-promoted checkpoint;later work remains experimental.\n\n'
        '## Evidence\n\n'
        f'- Ledger:translations/editorial_review_current_v1.json.\n- Source/current full opening:{PACKET}.\n- Prose draft:{DRAFT}.\n'
        f'- Close-range terminal negative audit:{NEGATIVE}.\n- Shop reference inventory:{REFERENCES}.\n'
        '- Last25 completed entries:work/analysis/editorial_completion_v1686/completion_receipt.json.\n'
        '- Last registered release:work/analysis/search_reports_release_v1675/registered_release_verification.json.\n'
        '- Full prior handoff retained in work/analysis/editorial_checkpoint_v1695/handoff_before.md.\n\n'
        '## Persistent requirements\n\n'
        'Use natural-dialogue-v2,natural faithful en-US,and Rafael/Joakim/Maria/Camille. Keep all generated ROMs;E: holds ROMs and guide captures. '
        'Four low-resolution Online bodies remain excluded,two brown marks preserved,and accepted plaque texture/borders do not complete the18-entry graphics audit. '
        'Do not modify executed producers/proofs;use explicit successors. sources/ is read-only. No subagents authorized. '
        'Read mandatory repository protocols before author/build. Python C:/Python314/python.exe,PYTHONUTF8=1,PYTHONPATH=.;.deps. '
        'out/work-analysis junction toE;archive lexical paths without resolving junctions. The earlier commit/push/promotion request was already fulfilled forV1492;no new promotion is authorized by automated testing. '
        'The full editorial goal stays active;older-record re-audit remains queued after it.\n')
    Path('docs/lil_opening_v1695_editorial_checkpoint.md').write_text(text,encoding='utf-8')
    handoff.write_text(text.replace('# V1695 Lil opening editorial and source-context checkpoint','# Current editorial handoff - V1695',1),encoding='utf-8')
    for name in ('docs/editorial_review_goal.md','docs/translation_progress.md','docs/known_issues.md','docs/todo.md'):
        with Path(name).open('a',encoding='utf-8') as f:f.write('\n\n## V1695 Lil opening49 source/prose review\n\n'+summary+'\n\nSee [V1695 checkpoint](lil_opening_v1695_editorial_checkpoint.md).\n')
    save(ROOT/'checkpoint_receipt.json',{'before_ledger_sha256':sha(raw),'after_ledger_sha256':sha(LEDGER.read_bytes()),
        'source_prose_before':1519,'source_prose_after':1568,'completed_entries_unchanged':1375,'COMMON_pending_unchanged':144,
        'new_route_pending_records':49,'evidence':{str(p):sha(p.read_bytes()) for p in (DRAFT,PACKET,NEGATIVE,REFERENCES)},
        'ROM_unchanged':'337edf22ab6ee96536aadb15fb461652149b157e8d9bd1ef60db998f97608510','no_live_jobs':True,
        'full_goal_complete':False,'producer_sha256':sha(Path(__file__).read_bytes())})
    print('V1695 saved:49 new route prose reviews;1568 reviewed,1375 complete.144 COMMON+49 route drafts remain pending;full goal active.')
