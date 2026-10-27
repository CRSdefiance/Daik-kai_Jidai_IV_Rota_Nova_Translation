"""Register eight new source/prose reviews without completing native gates."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/battle_victory_source_v1394')
MANUSCRIPT = Path('translations/battle_victory_editorial_manuscript_v1.json')
IDS = list(range(2130,2138))


if __name__=='__main__':
    assert not ROOT.exists()
    doc = read(MANUSCRIPT)
    assert [r['message_id'] for r in doc['records']]==IDS
    assert doc['revised']==2 and doc['retained']==6
    assert sha(Path(doc['source_context']).read_bytes())==doc['source_context_sha256']
    assert all(all(r['review'][g] for g in ['source','context','localization','naturalness'])
        and not r['review']['formatting'] for r in doc['records'])
    ledger_path = Path('translations/editorial_review_current_v1.json')
    ledger = read(ledger_path)
    before = deepcopy(ledger)
    assert (ledger['records_editorially_completed'],ledger['records_with_source_and_prose_pass'])==(1307,1395)
    completed = [n for f in ledger['completed_editorial_families'] for n in f.get('native_message_IDs',[])]
    pending = ledger['reviewed_but_incomplete_COMMON_IDs']
    assert len(completed)==len(set(completed))==1306 and len(pending)==len(set(pending))==88
    assert not set(IDS).intersection(set(completed)|set(pending))
    ROOT.mkdir(parents=True)
    save(ROOT/'coverage_before_source_review.json',before)
    ledger['records_with_source_and_prose_pass'] += 8
    ledger['records_with_source_prose_drafts'] = ledger['records_with_source_and_prose_pass']
    ledger['source_prose_reviewed_counts_by_file']['/COMMON/MESFILE.DK4'] += 8
    ledger['reviewed_but_incomplete_COMMON_IDs'] = sorted(pending+IDS)
    drafts = ledger['active_source_prose_drafts']
    drafts['native_message_IDs'] = sorted(drafts['native_message_IDs']+IDS)
    assert str(MANUSCRIPT) not in drafts['manuscripts']
    drafts['manuscripts'].append(str(MANUSCRIPT))
    drafts['manuscript_record_subsets_pending'][str(MANUSCRIPT)] = IDS
    drafts['status'] = '8-victory16-sinking34-aftermath38-older-reviewed-entries-open'
    drafts['note'] = ('Eight victory alternatives have source/context/prose review only,two proposed revisions '
        'and six justified retentions. Native layout/font,bounds,registered integration and original transitions '
        'remain pending. Sixteen sinking,34 aftermath and38 older reviewed COMMON entries remain incomplete;'
        'broader shared/routes/raw prose remains open.')
    unit = 'Shared-battle-victory8-source-prose'
    assert unit not in {r['id'] for r in ledger['coverage_units']}
    ledger['coverage_units'].append({'id':unit,'status':'source-context-prose-reviewed-native-release-gameplay-pending',
        'native_message_IDs':IDS,'manuscript':str(MANUSCRIPT),'source_context':doc['source_context'],
        'completed_entries_added':0,'full_goal_complete':False})
    summary = ('V1394 source/context/prose-reviews eight battle victory reports2130-2137:two proposed revisions '
        'and six justified retentions. Drafts preserve the admiral address,collective victory,and distinct '
        'conversational/formal/excited voices without inventing the destruction of every enemy vessel. '
        '2132 genuine IC plus plural tachi is faithfully grammatical we,not a name or singular I. '
        '2136 becomes We won! We did it,Admiral! and2137 uses the natural formal Admiral,we have won! '
        'Original72168/72170 selects role1/53D44/table02117EE0;206 existing NPC voice selections pass. '
        'Earlier original V1364 capture playback visibly shows2131 from Gerhard16,automatically selected with '
        'the physical First Mate slot empty. V1392 stopped before evidence output at an assumed formatted/compiled '
        'byte equality;V1392b verifies the original formatter adds exactly one leading cell. This is a probe '
        'assumption correction,not a demonstrated game defect. New full native font/layout,copy/cache/escape '
        'regressions,registered ROM/exact patch and representative scene/transition gates stay open. '
        'Counts1307 complete(975 revised332 retained),1403 source/prose;96 reviewed-incomplete COMMON'
        '(8 victory16 sinking34 aftermath38 older),plus broader shared/routes/raw prose. '
        'The Carronade pilot V1388 ends normally at11880 and its full45-byte fixture/input/RAM/PNG/save audit '
        'passes V1390;no sinking occurs and no original firing defect is inferred. Closed-sails new fire versus '
        'already airborne shots remains an unresolved test interpretation. Sixteen sinking entries stay open '
        'while other editorial work proceeds. Registered V1364/exact patch,canonical,V997,all graphics/all18 '
        'plaques and the later older-record re-audit remain unchanged/open;full goal active.')
    ledger['latest_checkpoint'] = summary
    ledger['research_checkpoints'].append({'id':'V1394-battle-victory8-source-prose','manuscript':str(MANUSCRIPT),
        'source_context':doc['source_context'],'completed_entries_added':0,'source_prose_reviews_added':8,
        'full_goal_complete':False})
    pilot_path = Path('work/analysis/carronade_verified_v1390/terminal_carronade_verification.json')
    pilot = read(pilot_path)
    assert pilot['terminal_frame']==11880 and pilot['no_sinking_notice_or_new_translation_completion_credit']
    ledger['research_checkpoints'].append({'id':'V1390-Carronade-pilot-no-sinking-credit',
        'proof':str(pilot_path),'proof_sha256':sha(pilot_path.read_bytes()),'completed_entries_added':0,
        'finding':'No sinking;all direct enemy health,crew,actor/ID,RNG and result edits excluded. Firing/closed-sails interpretation remains unresolved.',
        'source_prose_reviews_added':0,'full_goal_complete':False})
    pending = ledger['reviewed_but_incomplete_COMMON_IDs']
    assert len(pending)==len(set(pending))==len(drafts['native_message_IDs'])==96
    assert not set(completed).intersection(pending) and len(set(completed)|set(pending))==1402
    assert sum(ledger['source_prose_reviewed_counts_by_file'].values())==1403
    for key in ['records_editorially_completed','records_revised_and_integrated','retained_wordings_editorially_completed',
        'completed_editorial_record_counts_by_file','current_integrated_candidate','current_native_relocation_reference',
        'source_pins','unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal','raw_source_coverage_revisit']:
        assert ledger[key]==before[key],key
    save(ledger_path,ledger)
    document = Path('docs/battle_victory_v1394_source_checkpoint.md')
    assert not document.exists()
    document.write_text('# V1394 victory dialogue source and prose review\n\n'+summary+
        '\n\n## Exact evidence and remaining gates\n\n'
        'Manuscript: `'+str(MANUSCRIPT)+'`. Source/context: `'+doc['source_context']+'`. '
        'All eight entries are mutually exclusive voices of one report,not consecutive spoken lines. '
        'Immediate attack-confirmation and defeat neighbors remain evidence only and are not newly reviewed.\n\n'
        'The eight drafts are one logical paragraph each,with no authored alignment or line breaks. '
        'No printf argument is added. Review the original first-person macro pipeline and the whole native '
        'font plane for every voice,including the exact leading engine cell. Earlier2131 scene evidence is '
        'context,not new native/transition approval. Existing selector/runtime ownership is fully allocated;'
        'do not assume another membership fits or grow the123040-byte staged payload. Determine whether '
        'these short paragraphs need any new scoped formatter membership before planning runtime changes. '
        'Then finish payload/copy/cache/escape/shop regression,registered full-stack ROM and exact clean-input '
        'patch,ordinary cold boots and representative original victory/reward/return verification. '
        'The separate graphics audit and all18 plaques stay open.\n',encoding='utf-8')
    for name in ['translation_progress.md','known_issues.md','todo.md','editorial_review_goal.md']:
        with (Path('docs')/name).open('a',encoding='utf-8',newline='\n') as handle:
            handle.write('\n\n## V1394 victory source review\n\n'+summary+
                '\n\nSee [checkpoint](battle_victory_v1394_source_checkpoint.md).\n')
    save(ROOT/'source_review_receipt.json',{'manuscript':str(MANUSCRIPT),'manuscript_sha256':sha(MANUSCRIPT.read_bytes()),
        'completed':1307,'source_prose':1403,'source_prose_reviews_added':8,'completed_entries_added':0,
        'draft_revisions':2,'draft_retained':6,'reviewed_incomplete_COMMON':96,
        'native_formatting_registered_release_and_original_gameplay_pending':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Eight new source/prose reviews registered:1403 reviewed,1307 complete;96 reviewed COMMON entries remain incomplete.',flush=True)
