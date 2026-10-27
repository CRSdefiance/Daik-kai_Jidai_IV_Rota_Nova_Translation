"""Fresh full-exchange B24 reread; retain13 proven current wordings, no ROM change."""
from copy import deepcopy
import os
from pathlib import Path
from dk4tool.dialogue.encoder import encode_relocatable_dialogue
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_B24_contextual_retention_v1975')
OLD = Path('translations/lil_trade_routes_officers_final_review_v1.json')
OUT = Path('translations/lil_trade_routes_officers_contextual_retention_review_v1.json')
LEDGER = Path('translations/editorial_review_current_v1.json')
HANDOFF = Path('docs/editorial_handoff_current.md')
ROM = Path('out/all_routes_combined_v1971_candidate.nds')
REASONS = [
    'Camille opens with an encouraging proposal. Keep signing naturally includes this pace/keep it up; more towns and one percent share in each preserve the explicit per-town contract minimum and the fleet\'s own routes. The two sentences lead directly into Lil\'s term question.',
    'Lil echoes precisely the unfamiliar term from Camille\'s proposal. Trade routes? is a natural short question and keeps her knowledge gap without supplying a new explanation.',
    'Camille answers her question and connects the already-mentioned routes with having a surveyor. Aboard fits the fleet setting and does not invent a separate assistant or an automatic-travel instruction.',
    'Lil\'s ふーん is a brief noncommittal acknowledgment here. Huh. with a period preserves that beat before Camille shifts to staffing; it does not turn it into a second request for explanation.',
    'Camille realizes the fleet lacks people once another specialist is needed. The surveyor too, more people and experienced companions preserve that staffing progression and leave room for Lil\'s following sailor misunderstanding. No personal entourage is invented.',
    'Lil offers a practical tavern solution in a conditional question. Sailors preserves 水夫 and lets Camille correct the category in the next speech; hire some reads naturally in the tavern recruitment context.',
    'Camille explicitly corrects ordinary sailors to the officers who command them and broadens the need to diverse talents as the fleet grows. Officers is the established party-member term, with no invented naval commission or new rank.',
    'Lil asks how to search, not merely where. Them points clearly to the companions just described and keeps her direct practical voice.',
    'Camille admits reliance on luck and then offers a possible strategy. Might preserves uncertainty; bigger cities is a natural generic comparison within their travels and does not guarantee finding anyone.',
    'Lil thoughtfully repeats the search category with an ellipsis. Big cities... keeps the source hesitation and flows into Camille\'s suggested destinations.',
    'Camille suggests a Mediterranean city as their first goal, names both Genoa and Istanbul, and marks the local seafaring population as hearsay. The two short sentences retain every fact and his helpful, conversational voice.',
    'Lil combines recruiting with signing town contracts en route. Two birds with one stone is the ordinary American equivalent of 一石二鳥 and preserves her brisk realization without a new mechanic.',
    'Camille enthusiastically praises Lil and confirms her plan. That\'s our FI! Exactly! keeps both approving beats and the real runtime captain-name substitution; our is a group expression, with no invented kinship or romantic relationship.',
]

if __name__ == '__main__':
    assert not ROOT.exists() and not OUT.exists()
    old = read(OLD)
    digest = sha(ROM.read_bytes())
    assert digest == 'c4c998e446b7ac410d2294563fc4e5d5181cef6938c25254b1bd3679492efa20'
    image, clean, previous = map(NdsImage.open,(ROM,'work/clean.nds',old['candidate']))
    arm = image.read_file('/__arm9__.bin')
    assert arm == previous.read_file('/__arm9__.bin')
    now = IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[24]
    earlier = IlnkContainer.parse(previous.read_file('/data/SC2.DK4')).blocks[24]
    japanese = IlnkContainer.parse(clean.read_file('/data/SC2.DK4')).blocks[24]
    assert now == earlier
    assert image.read_file('/COMMON/MESFILE.DK4') == previous.read_file('/COMMON/MESFILE.DK4')
    mapping = read(old['reference_map'])
    assert sha(now) == mapping['target_block_sha256'] and sha(arm) == mapping['required_runtime_ARM9_sha256']
    visual = read(old['final_proof'])
    assert visual['all13_actual_panels_both_sheets_and_normal_return_viewed']
    for path, expected in visual['proofs'].items(): assert sha(Path(path).read_bytes()) == expected,path
    actual_path = Path(old['records'][0]['actual_proof'])
    actual = read(actual_path)
    profile = get_dialogue_profile('lil-opening-editorial-native-v1')
    rows = []
    for index, row in enumerate(old['records']):
        source = bytes.fromhex(row['source_hex'])
        current = bytes.fromhex(row['current_text_hex'])
        ja, at = row['source_reference']['offset'], row['current_reference']['offset']
        assert japanese[ja:ja+len(source)] == source and japanese[ja+len(source)] == 0
        assert now[at:at+len(current)] == current and now[at+len(current)] == 0
        assert japanese[ja-5:ja+1] == now[at-5:at+1] == bytes.fromhex(row['source_complete_preamble_hex'])
        compiled = encode_relocatable_dialogue(source,row['english'],profile)
        assert compiled.encoded.hex() == row['compiled_hex']
        assert current in (compiled.encoded,compiled.encoded+b' ')
        assert all(d.code in row.get('qa_waivers',[]) for d in compiled.diagnostics if d.severity == 'warning')
        assert source.count(b'FI') == row['english'].count('{MACRO:FI}')
        rows.append(dict(id=row['id'],file_path='/data/SC2.DK4',block=24,
            source_reference=deepcopy(row['source_reference']),source_hex=source.hex(),
            clean_Japanese=source[1:].decode('cp932'),current_reference=deepcopy(row['current_reference']),
            current_text_hex=current.hex(),current_stored_English=current[1:].decode('cp932'),
            english=row['english'],speaker=row['speaker'],source_meaning=row['source_meaning'],
            complete_preamble_hex=row['source_complete_preamble_hex'],editorial_decision='retain-wording',
            retained_wording_justification=REASONS[index],
            context='All13 speeches reread together: contracts andone-percent trade routes lead tosurveyor staffing,Lil\'s sailor/officer misunderstanding,uncertain recruitment advice,Mediterranean destinations,her two-purpose plan andCamille\'s approving praise. Source mechanics,questions,hearsay,pauses anddistinct voices remain intact.',
            fresh_review=dict(source=True,context=True,localization=True,naturalness=True,formatting=True),
            formatting_basis='Exact current B24,ARM9 andCOMMON bytes equal the independently verified V1841 scene. Re-encoding matches stored target andcompiler-owned parity;inherit the existing13 native planes104 macro cases26 actual holds. No new gameplay or later technical re-audit claimed.',
            inherited_actual_holds=deepcopy(row['actual_holds']),new_gameplay_visit_claimed=False))
    assert len(rows) == len(REASONS) == 13
    raw = LEDGER.read_bytes()
    ledger = read(LEDGER)
    before = deepcopy(ledger)
    fresh = ledger['contextual_story_natural_dialogue_pass_v1871']
    ids = [r['id'] for r in rows]
    assert not set(ids) & set(fresh['record_IDs'])
    assert fresh['fresh_pass_records_explicitly_reread'] == fresh['fresh_pass_records_integrated'] == 302
    assert fresh['historical_completed_records_outside_reconciled_fresh_pass'] == 1529
    family = next(f for f in ledger['completed_editorial_families'] if f['id'] == 'Lil-trade-routes-officers13')
    assert set(family['record_IDs']) == set(ids)
    ROOT.mkdir(parents=True)
    (ROOT/'ledger_before.json').write_bytes(raw)
    (ROOT/'handoff_before.md').write_bytes(HANDOFF.read_bytes())
    save(OUT,dict(format='dk4-contextual-retention-reconciliation-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        family='Lil-trade-routes-officers13',record_IDs=ids,records=rows,revised_count=0,retained_count=13,
        source_clean_ROM='work/clean.nds',source_clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),
        clean_B24_sha256=sha(japanese),current_B24_sha256=sha(now),ARM9_sha256=sha(arm),
        current_candidate=str(ROM),current_candidate_sha256=digest,
        original_review=str(OLD),original_review_sha256=sha(OLD.read_bytes()),
        original_gameplay_scope=old['actual_scope'],inherited_native_and_actual_evidence_bound_to_unchanged_bytes=True,
        no_new_ROM_patch_or_gameplay_required_for_unchanged_text=True,no_historical_completion_count_added=True,
        older_record_technical_reaudit_remains_deferred=True,
        evidence={str(p):sha(p.read_bytes()) for p in (OLD,Path(old['reference_map']),Path(old['final_proof']),actual_path)},
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    fresh['record_IDs'] += ids
    fresh.update(fresh_pass_records_explicitly_reread=315,fresh_pass_records_integrated=315,
        historical_completed_records_outside_reconciled_fresh_pass=1516,latest_final_review=str(OUT),
        latest_contextual_retention_review=str(OUT),latest_reconciled_historical_family='Lil-trade-routes-officers13',
        coverage_note='Stockholm51,London111,Speyer59,Hamburg81 andearlier trade-route/officer13 are explicitly reread andintegrated/reconciled. B24wording retained with13individual reasons andexact current/source evidence;historical totals unchanged. Other1516historical completions require reconciliation.')
    fresh['reconciled_families'].append(dict(id='Lil-trade-routes-officers13',records=13,final_review=str(OUT),
        historical_reconciliation_only=True,new_revisions=0,justified_retentions=13))
    family['contextual_v1871_reconciliation'] = dict(review=str(OUT),review_sha256=sha(OUT.read_bytes()),
        all13_wordings_retained=True,entire_clean_Japanese_exchange_explicitly_reread=True,current_candidate=str(ROM))
    ledger['coverage_units'].append(dict(id='Lil-trade-routes-officers13-contextual-v1975',file_path='/data/SC2.DK4',blocks=[24],
        record_IDs=ids,status='fresh-contextual-reconciliation-complete-unchanged-native-target',final_review=str(OUT),
        historical_entries_reconciled=13,source_prose_reviews_added=0,completed_entries_added=0,new_ROM_changes=0,
        actual_coverage='Inherited13speech26hold actual sample;no new gameplay visits. Exact B24/runtime/COMMON inheritance checked.',
        full_goal_complete=False))
    summary = ('V1975 fresh B24contextual reconciliation:all13 clean-Japanese speeches reread asoneexchange;13justified retentions,no ROM change ornew historical completion count. '
        'Fresh pass315 explicitly reread andintegrated/reconciled;1516 historical completions still needreconciliation. Historical total1831(1362revised469retained),source/prose1947,116incomplete COMMON andall remaining prose stayopen. '
        'RegisteredV1971 andexact clean-input patch unchanged. Inherit prior13 native planes104 macro cases26 actual holds onlyafter exact B24/ARM9/COMMON/source checks;no newgameplay claim. Graphics/all18plaques andlaterolder-record technical re-audit remainseparate;fullgoalactive.')
    ledger['latest_checkpoint'] = summary
    ledger['research_checkpoints'].append(dict(id='V1975-B24-fresh-contextual-retentions',proof=str(ROOT/'reconciliation_receipt.json'),
        completed_entries_added=0,source_prose_reviews_added=0,historical_entries_reconciled=13,full_goal_complete=False))
    for key in ('records_editorially_completed','records_revised_and_integrated','retained_wordings_editorially_completed',
        'records_with_source_and_prose_pass','completed_editorial_record_counts_by_file','source_prose_reviewed_counts_by_file',
        'current_integrated_candidate','unresolved_graphics_work','reviewed_but_incomplete_COMMON_IDs','older_record_reaudit_after_full_editorial_goal'):
        assert ledger[key] == before[key],key
    assert len(set(fresh['record_IDs'])) == len(fresh['record_IDs']) == 315
    assert ledger['records_editorially_completed']-fresh['fresh_pass_records_integrated'] == 1516
    assert ledger['goal_status'] == 'active' and not ledger['full_goal_complete']
    pending = LEDGER.with_name('editorial_review_current_v1975_pending.json')
    assert not pending.exists() and LEDGER.read_bytes() == raw
    save(pending,ledger)
    os.replace(pending,LEDGER)
    text = HANDOFF.read_text(encoding='utf-8').replace('# Current editorial handoff - V1974','# Current editorial handoff - V1975',1)
    text = text.replace('Fresh V1871 contextual pass:302 explicitly reread andintegrated(Stockholm51 +London111 +Speyer59 +Hamburg81). Prior1529 completions require explicit reconciliation.',
        'Fresh V1871 contextual pass:315 explicitly reread andintegrated/reconciled(Stockholm51 +London111 +Speyer59 +Hamburg81 +trade-route/officer13 retained). Prior1516 completions require explicit reconciliation.')
    text = text.replace('116 COMMON entries remain incomplete;1529 historical completions needexplicit reconciliation.',
        '116 COMMON entries remain incomplete;1516 historical completions needexplicit reconciliation.')
    anchor = '## Hamburg B74 complete - V1974'
    assert text.count(anchor) == 1
    chapter = ('## Earlier B24 fresh contextual retention pass - V1975\n\n'+summary+'\n\n'
        f'- Review:{OUT.as_posix()};receipt:{ROOT.as_posix()}/reconciliation_receipt.json. Each of13 records contains exact clean/current references,Japanese text,current English andan individual retention reason. Existing historical review andall ROMs preserved.\n'
        '- Retain onepercent per-town contracts,surveyor benefit,officer/sailor distinction,uncertain large-city recruitment,Genoa/Istanbul,hearsay,two-birds idiom andCamille\'s FI praise. Lil remainsbrief/practical;Camille remainshelpful/enthusiastic. No invented navalrank,relationship orrecruitment guarantee.\n'
        '- No renderer/layout/code/ROM change. Exact B24,ARM9 andCOMMON equalthe prior V1841 actual/native proof;315fresh pass count includes these13,while1831historical total staysunchanged. Do notrepeat equivalent tests without a concrete newrisk.\n\n')
    HANDOFF.write_text(text.replace(anchor,chapter+anchor),encoding='utf-8')
    for name in ('translation_progress.md','todo.md','editorial_review_goal.md'):
        with (Path('docs')/name).open('a',encoding='utf-8') as stream:
            stream.write('\n\n## V1975 B24 fresh contextual retentions\n\n'+summary+'\n\nReview: translations/lil_trade_routes_officers_contextual_retention_review_v1.json.\n')
    save(ROOT/'reconciliation_receipt.json',dict(review=str(OUT),review_sha256=sha(OUT.read_bytes()),
        clean_B24_sha256=sha(japanese),current_B24_sha256=sha(now),ARM9_sha256=sha(arm),current_candidate=str(ROM),candidate_sha256=digest,
        explicit_fresh_reread_added=13,justified_retentions=13,new_revisions=0,new_historical_completions=0,
        fresh_contextual_reread_integrated_after=315,historical_outside_reconciled_fresh_pass=1516,
        historical_completed_unchanged=1831,source_prose_reviewed_unchanged=1947,no_new_gameplay_claim=True,
        ledger_sha256=sha(LEDGER.read_bytes()),handoff_sha256=sha(HANDOFF.read_bytes()),
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    assert sha(ROM.read_bytes()) == digest
    print(dict(fresh_reread_retained=13,fresh_total=315,historical_outside_fresh=1516,historical_total_unchanged=1831,ROM_unchanged=True))
