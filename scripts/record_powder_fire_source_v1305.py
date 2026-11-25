"""Register six source/prose reviews without native/release/completion credit."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.powder_fire_layout_v1304 import IDS, paragraph
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/powder_fire_source_v1305')
MANUSCRIPT = Path('translations/powder_fire_editorial_manuscript_v1.json')


def main():
    assert not ROOT.exists()
    doc = read(MANUSCRIPT)
    assert tuple(row['message_id'] for row in doc['records']) == IDS
    assert all(all(row['review'][gate] for gate in ['source','context','localization','naturalness'])
        and not row['review']['formatting'] for row in doc['records'])
    assert all(paragraph(row).hex() == row['unwrapped_paragraph_hex'] for row in doc['records'])
    context = read(doc['source_context'])
    assert sha(Path(doc['source_context']).read_bytes()) == doc['source_context_sha256']
    assert context['actual_old_wording_holds'][0]['source_selected_message_ID'] == 2053
    ledger_path = Path('translations/editorial_review_current_v1.json')
    ledger = read(ledger_path)
    before = deepcopy(ledger)
    assert (ledger['records_editorially_completed'],ledger['records_with_source_and_prose_pass']) == (1296,1373)
    complete = [n for family in ledger['completed_editorial_families'] for n in family.get('native_message_IDs',[])]
    assert len(complete) == len(set(complete)) == 1295
    pending = ledger['reviewed_but_incomplete_COMMON_IDs']
    assert len(pending) == len(set(pending)) == 77 and not set(IDS).intersection(set(complete)|set(pending))
    ROOT.mkdir(parents=True)
    save(ROOT/'coverage_before_source_review.json',before)
    ledger['records_with_source_and_prose_pass'] += 6
    ledger['source_prose_reviewed_counts_by_file']['/COMMON/MESFILE.DK4'] += 6
    ledger['reviewed_but_incomplete_COMMON_IDs'] = sorted(pending+list(IDS))
    drafts = ledger['active_source_prose_drafts']
    drafts['native_message_IDs'] = sorted(drafts['native_message_IDs']+list(IDS))
    assert str(MANUSCRIPT) not in drafts['manuscripts']
    drafts['manuscripts'].append(str(MANUSCRIPT))
    drafts['manuscript_record_subsets_pending'][str(MANUSCRIPT)] = list(IDS)
    drafts['status'] = '6-powder-fire39-aftermath38-older-reviewed-entries-open'
    drafts['note'] = 'Six new powder-fire drafts are source/context/prose reviewed only;native layout,registered integration and revised gameplay remain pending.39 other aftermath and38 older reviewed COMMON entries remain incomplete. Broader shared/routes/raw prose remains unreviewed.'
    # This legacy counter stopped tracking new reviews. Reconcile to exact unique
    # reviewed IDs, rather than propagate its stale1267 value or add completion.
    old_legacy = ledger['records_with_source_prose_drafts']
    assert old_legacy == 1267
    ledger['records_with_source_prose_drafts'] = ledger['records_with_source_and_prose_pass']
    ledger['legacy_source_draft_counter_reconciliation_v1305'] = {
        'previous_stale_value':old_legacy,'exact_current_unique_source_prose_count':1379,
        'COMMON_unique_reviewed':1378,'SC2_unique_reviewed':1,
        'reason':'Historical recorders used this as an alias of source/prose review,but later increments stopped;reconciled from exact completed and reviewed-incomplete IDs.',
        'does_not_add_any_completion_credit':True}
    unit_id = 'Shared-powder-fire6-source-prose'
    assert unit_id not in {unit['id'] for unit in ledger['coverage_units']}
    ledger['coverage_units'].append({'id':unit_id,'status':'source-context-prose-reviewed-native-release-gameplay-pending',
        'native_message_IDs':list(IDS),'manuscript':str(MANUSCRIPT),'source_context':doc['source_context'],
        'completed_entries_added':0,'full_goal_complete':False})
    summary = ('V1305 source/context/prose-reviews six powder-fire alerts2052-2057 under natural-dialogue-v2. Natural English replaces the stiff gun-platform phrasing while preserving ignition,fire and gun-battery location;no explosion,magazine,casualties or sinking is invented. Original755D8/75610 uses an unforced powder-fire check,55DC4 gun-position actor and direct53F0C/table02117980;two FFFFFFFF voice slots retain original2052 fallback. Actual old2053 is identified at7210 from Gerhard16/voice1 in the original staffed Sao Tome test. Touch7310 dismissed it and exposed an old fire-extinguished notice,so only7210 is a genuine old-fire hold. Both test runs ended normally with donor saves unchanged. Prebattle24-owned-byte fixture changes16 actual bytes for location,existing Charles/Gerhard duties and native-capacity124 sailors;no actor attributes,defenses,shares,RNG or result edits. Town100 naturally fell to99;no surrender occurred. Counts remain1296 complete(964 revised332 retained);1379 source/prose reviewed,83 reviewed-incomplete COMMON(6 fire+39 aftermath+38 older). Legacy stale draft counter1267 is reconciled to exact unique1379 source/prose entries,not new completions. Native wrapping/font/glyph/bounds,copies,registered ROM/exact patch and revised original gameplay for the new six remain open. A further56 neighboring ship-result/ram entries are inventoried only,including full-width I2099;no review credit. V1266/canonical/V997 and separate graphics/all18 plaques remain unchanged;full goal active.')
    ledger['latest_checkpoint'] = summary
    ledger['research_checkpoints'].append({'id':'V1305-powder-fire6-source-prose','manuscript':str(MANUSCRIPT),
        'source_context':doc['source_context'],'completed_entries_added':0,'source_prose_reviews_added':6,'full_goal_complete':False})
    pending = ledger['reviewed_but_incomplete_COMMON_IDs']
    assert len(pending) == len(set(pending)) == len(drafts['native_message_IDs']) == 83
    assert not set(complete).intersection(pending) and len(set(complete)|set(pending)) == 1378
    assert sum(ledger['source_prose_reviewed_counts_by_file'].values()) == 1379
    for key in ['records_editorially_completed','records_revised_and_integrated','retained_wordings_editorially_completed',
                'completed_editorial_record_counts_by_file','current_integrated_candidate','current_native_relocation_reference',
                'latest_registered_aftermath_candidate','source_pins','unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal','raw_source_coverage_revisit']:
        assert ledger[key] == before[key],key
    save(ledger_path,ledger)
    Path('docs/powder_fire_v1305_source_checkpoint.md').write_text('# V1305: powder-fire source and English review\n\n'+summary+
        '\n\n## Evidence and next gates\n\nManuscript: `'+str(MANUSCRIPT)+'`. Source binding: `'+doc['source_context']+'`. Broader inventory: `work/analysis/battle_hazards_inventory_v1302/source_current_packet.json`.\n\n'+
        'The actual image contains old wording and is not a finalized guide screenshot. The revised six have no native-layout or gameplay approval yet. Add only the proven direct-parent53F40/table17980 membership to the existing bounded selector;inspect its188-byte table capacity before changing it. Keep172-byte code allocation and the full123040 staged bytes unchanged. Then verify native selection/printf/macro/wrapping and complete fonts,both original fallback slots,all old selectors/copies/status paths,register/rebuild the full combined stack,verify exact clean-input patch/startup and replay original powder fire with normal dismissal.\n\n'+
        'Retain failed research:V1296 included a larger AI span with existing changed callers and stopped;V1296b guards only the actual model getters. V1303 initially assumed the two voice holes were duplicate IDs;the source contains FFFFFFFF fallbacks. V1303b also treated touch7310 as a second hold;native cache bytes disprove it. V1303c records the corrected direct caller and single genuine old-wording hold. No guard was relaxed to claim a new translation complete.\n',encoding='utf-8')
    for name in ['translation_progress.md','known_issues.md','todo.md','editorial_review_goal.md']:
        with (Path('docs')/name).open('a',encoding='utf-8',newline='\n') as handle:
            handle.write('\n\n## V1305 powder-fire source review\n\n'+summary+'\n\nSee [checkpoint](powder_fire_v1305_source_checkpoint.md).\n')
    save(ROOT/'source_review_receipt.json',{'manuscript':str(MANUSCRIPT),'manuscript_sha256':sha(MANUSCRIPT.read_bytes()),
        'completed':1296,'source_prose':1379,'source_prose_reviews_added':6,'completed_entries_added':0,
        'reviewed_incomplete_COMMON':83,'legacy_counter_before':1267,'legacy_counter_reconciled_to_exact_source_prose':1379,
        'native_formatting_registered_release_and_revised_gameplay_pending':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Six new source/prose reviews:1379 reviewed,1296 complete;83 reviewed COMMON entries remain incomplete.',flush=True)


if __name__ == '__main__':
    main()
