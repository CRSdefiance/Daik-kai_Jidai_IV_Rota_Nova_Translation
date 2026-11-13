"""Add sixteen source/prose reviews, preserving all unfinished release gates."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/ship_sinking_source_v1327')
MANUSCRIPT = Path('translations/ship_sinking_editorial_manuscript_v1.json')
IDS = list(range(2058,2074))


def main():
    assert not ROOT.exists()
    doc = read(MANUSCRIPT)
    assert [r['message_id'] for r in doc['records']]==IDS
    assert all(all(r['review'][g] for g in ['source','context','localization','naturalness']) and not r['review']['formatting'] for r in doc['records'])
    assert sum(r['editorial_decision']=='revise' for r in doc['records'])==4
    assert sha(Path(doc['source_context']).read_bytes())==doc['source_context_sha256']
    ledger_path = Path('translations/editorial_review_current_v1.json')
    ledger = read(ledger_path)
    before = deepcopy(ledger)
    assert (ledger['records_editorially_completed'],ledger['records_with_source_and_prose_pass'])==(1302,1379)
    completed = [n for f in ledger['completed_editorial_families'] for n in f.get('native_message_IDs',[])]
    pending = ledger['reviewed_but_incomplete_COMMON_IDs']
    assert len(completed)==len(set(completed))==1301 and len(pending)==len(set(pending))==77
    assert not set(IDS).intersection(set(completed)|set(pending))
    ROOT.mkdir(parents=True)
    save(ROOT/'coverage_before_source_review.json',before)
    ledger['records_with_source_and_prose_pass'] += 16
    ledger['records_with_source_prose_drafts'] = ledger['records_with_source_and_prose_pass']
    ledger['source_prose_reviewed_counts_by_file']['/COMMON/MESFILE.DK4'] += 16
    ledger['reviewed_but_incomplete_COMMON_IDs'] = sorted(pending+IDS)
    drafts = ledger['active_source_prose_drafts']
    drafts['native_message_IDs'] = sorted(drafts['native_message_IDs']+IDS)
    assert str(MANUSCRIPT) not in drafts['manuscripts']
    drafts['manuscripts'].append(str(MANUSCRIPT))
    drafts['manuscript_record_subsets_pending'][str(MANUSCRIPT)] = IDS
    drafts['status'] = '16-sinking39-aftermath38-older-reviewed-entries-open'
    drafts['note'] = 'Sixteen sinking alternatives have source/context/prose review only:four revisions,twelve justified retentions. Native-name expansion,layout/font/bounds,registered integration and original scene transitions remain pending.39 aftermath and38 older reviewed COMMON entries also remain incomplete;broader shared/routes/raw prose remains unreviewed.'
    unit_id = 'Shared-ship-sinking16-source-prose'
    assert unit_id not in {r['id'] for r in ledger['coverage_units']}
    ledger['coverage_units'].append({'id':unit_id,'status':'source-context-prose-reviewed-native-release-gameplay-pending',
        'native_message_IDs':IDS,'manuscript':str(MANUSCRIPT),'source_context':doc['source_context'],
        'completed_entries_added':0,'full_goal_complete':False})
    summary = ('V1327 source/context/prose-reviews sixteen ship-sinking notices2058-2073:four revisions,twelve justified retained wordings. Clean Japanese preserves ongoing sinking2059,completed/passive losses,address to the admiral,clipped urgent2067 and differing youthful/formal reports. All16 preserve exactly one original ship-name%s argument. Two distinct source consumers are proven:role1/53D44/table021179C0 for a fleet loss and gun-position actor55DC4/direct53F0C/table02117A80 for an enemy sunk by original projectile damage.412 existing-actor voice selections and the original virtual ship-name getter pass read-only CPU checks;no actual sinking or result is injected or claimed. The adjacent crew-exhaustion cleanup table02117AC0 is capture2074-2081,not enemy sinking. Counts1302 complete(970 revised332 retained),1395 source/prose;93 reviewed-incomplete COMMON(16 sinking39 aftermath38 older),plus broader unreviewed shared/routes/raw prose and40 inventoried-only hazard neighbors. All new native-formatting,font/bounds/name stress,repacking,registered ROM/exact patch and representative original gameplay gates remain open. V1316/canonical/V997 remain unchanged;full editorial and separate graphics/all18 plaques audits stay open. V1324b archives87 completed-fire release evidence files with three terminal capture reports/RAM/PNGs verified;all235 ROMs retained under preview only.')
    ledger['latest_checkpoint'] = summary
    ledger['research_checkpoints'].append({'id':'V1327-ship-sinking16-source-prose','manuscript':str(MANUSCRIPT),
        'source_context':doc['source_context'],'completed_entries_added':0,'source_prose_reviews_added':16,'full_goal_complete':False})
    formatting = ledger['formatting_watchlist']
    proof = Path('work/analysis/powder_fire_release_v1315/photographed_shop_formatting.json')
    check = read(proof)
    assert all(r['no_authored_indent_internal_gap_or_stray_Discover'] for r in check['entries'])
    formatting['latest_photographed_shop_recheck'] = {'checkpoint':'V1327','candidate':check['candidate'],
        'candidate_sha256':check['candidate_sha256'],'proof':str(proof),
        'result':'676/677 exact native wrapping and complete228x64 fonts pass;the reported large gap and stray Discover remain absent. No fresh shop activation claimed.',
        'global_formatting_audit_complete':False}
    formatting['latest_reference_proof'] = str(proof)
    formatting['latest_user_screenshot_recheck'] = {'proof':str(proof),'candidate':check['candidate'],
        'exact_repaired676_677_bytes_preserved':True,'complete_native_wrapping_and_glyph_planes_rechecked':True,
        'new_actual_shop_activation_claimed':False,'global_formatting_audit_complete':False}
    pending = ledger['reviewed_but_incomplete_COMMON_IDs']
    assert len(pending)==len(set(pending))==len(drafts['native_message_IDs'])==93
    assert not set(completed).intersection(pending) and len(set(completed)|set(pending))==1394
    assert sum(ledger['source_prose_reviewed_counts_by_file'].values())==1395
    for key in ['records_editorially_completed','records_revised_and_integrated','retained_wordings_editorially_completed',
                'completed_editorial_record_counts_by_file','current_integrated_candidate','current_native_relocation_reference',
                'latest_registered_powder_fire_candidate','source_pins','unresolved_graphics_work',
                'older_record_reaudit_after_full_editorial_goal','raw_source_coverage_revisit']:
        assert ledger[key]==before[key],key
    save(ledger_path,ledger)
    Path('docs/ship_sinking_v1327_source_checkpoint.md').write_text('# V1327: sinking dialogue source and prose review\n\n'+summary+
        '\n\n## Exact evidence and next gates\n\nManuscript: `'+str(MANUSCRIPT)+'`. Source/context: `'+doc['source_context']+'`. Neither adjacent voice alternatives nor their neighboring storage records are consecutive spoken dialogue. Source instruction windows and complete clean/current record references are retained in the context packet.\n\n'+
        'The sixteen approved prose drafts are one logical paragraph apiece. Do not prewrap before native substitution and speech macro expansion. Preserve the single C-string ship-name argument and the original role/direct parent distinctions. Both new table memberships fit the existing188-byte selector bank at exactly188 encoded bytes without changing code or allocations. This capacity observation is not native runtime verification. Next:source-guarded runtime/payload plan,exhaustive scope/ABI guards,all voices and full names including player-edited bounds,complete native font previews,copies/cache/escape/shop regressions,registered full-stack integration and exact clean-input patch,ordinary cold boots and representative original sinking scenes/dismissals. No actor ID,RNG,event eligibility or result injection is authorized.\n',encoding='utf-8')
    for name in ['translation_progress.md','known_issues.md','todo.md','editorial_review_goal.md']:
        with (Path('docs')/name).open('a',encoding='utf-8',newline='\n') as handle:
            handle.write('\n\n## V1327 sinking source review\n\n'+summary+'\n\nSee [checkpoint](ship_sinking_v1327_source_checkpoint.md).\n')
    save(ROOT/'source_review_receipt.json',{'manuscript':str(MANUSCRIPT),'manuscript_sha256':sha(MANUSCRIPT.read_bytes()),
        'completed':1302,'source_prose':1395,'source_prose_reviews_added':16,'completed_entries_added':0,
        'draft_revisions':4,'draft_retained':12,'reviewed_incomplete_COMMON':93,
        'native_formatting_registered_release_and_original_gameplay_pending':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('16 source/prose reviews registered:1395 reviewed,1302 complete;93 reviewed COMMON entries remain incomplete.',flush=True)


if __name__=='__main__':
    main()
