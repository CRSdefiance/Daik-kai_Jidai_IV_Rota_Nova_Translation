"""Close the navigation run in authoritative state without claiming a new scene."""
import os
from pathlib import Path
from copy import deepcopy
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT=Path('work/analysis/lil_lessons_checkpoint_v1749')
PROOF=Path('work/analysis/lil_navigation_audit_v1748/terminal_navigation_and_nontrigger_findings.json')
LEDGER=Path('translations/editorial_review_current_v1.json')
HANDOFF=Path('docs/editorial_handoff_current.md')

if __name__=='__main__':
    assert not ROOT.exists()
    proof=read(PROOF)
    assert proof['terminal_frame']==34530 and proof['no_native_B23_entry_observed']
    assert proof['all262_callbacks_zero_errors_mismatches_host_restored_and_no_pending_command']
    raw=LEDGER.read_bytes(); doc=read(LEDGER); before=deepcopy(doc)
    assert (doc['records_editorially_completed'],doc['records_with_source_and_prose_pass'])==(1424,1632)
    ROOT.mkdir(parents=True); (ROOT/'ledger_before.json').write_bytes(raw)
    (ROOT/'handoff_before.md').write_bytes(HANDOFF.read_bytes())
    note=('V1749 closes the ordinary V1745 navigation test at34530 with normal stop,262 clean read-only '
        'callbacks,no pending command,exact replay inputs/PNG hashes/4MiB exports andrestored host/core. '
        'Sea View,Deck View andRoute Map were opened andviewed. No B23 entry orBruges arrival occurred. '
        'Original town data independently confirms Amsterdam2 andBruges3;manual course experiments and '
        'map cursor selection do not establish event eligibility. Next inspect original EV2 conditions '
        'andB23 selector before another travel run. No run remains live. Earlier V1746 native64 approval '
        'andV1744 revised wind22/44holds remain valid;all64 lesson entries remain incomplete pending '
        'other actual paths,reference approval,registered integration andexactpatch. Counts1424 complete '
        '(1076 revised348 retained),1632 source/prose. V1711 registered experimental,V1492 promoted,full '
        'editorial goal active andgraphics/all18 plaques separately unfinished.')
    doc['latest_checkpoint']=note
    doc['research_checkpoints'].append({'id':'V1749-Lil-navigation-terminal-trigger-still-unmapped',
        'proof':str(PROOF),'completed_entries_added':0,'source_prose_reviews_added':0,'full_goal_complete':False})
    doc['next_route_scene_editorial_packet']['note']=proof['next_action']+' All64 native layouts approved;wind22 actual verified;other paths,map,registered ROM andpatch remain pending.'
    doc['lil_lessons_editorial_v1720']['ordinary_navigation_terminal_proof']=str(PROOF)
    for key in ['records_editorially_completed','records_revised_and_integrated','retained_wordings_editorially_completed',
        'records_with_source_and_prose_pass','completed_editorial_record_counts_by_file','source_prose_reviewed_counts_by_file',
        'reviewed_but_incomplete_COMMON_IDs','unresolved_graphics_work','current_integrated_candidate','active_source_prose_drafts']:
        assert doc[key]==before[key]
    assert doc['goal_status']=='active' and not doc['full_goal_complete']
    temp=LEDGER.with_name('editorial_review_current_v1749_pending.json'); assert not temp.exists()
    save(temp,doc); assert read(temp)==doc and LEDGER.read_bytes()==raw; os.replace(temp,LEDGER)
    text=HANDOFF.read_text(encoding='utf-8')
    assert text.startswith('# Current editorial handoff - V1746')
    text=text.replace('# Current editorial handoff - V1746','# Current editorial handoff - V1749',1)
    start=text.index('## Live process and exact next action')
    end=text.index('## Earlier COMMON and process safeguards',start)
    text=text[:start]+'''## Process state and exact next action

ALL CURRENT JOBS ARE TERMINAL. Navigation V1745 exec35207 exited normally34530;do not resume or restart that old handle. Proof work/analysis/lil_navigation_audit_v1748/terminal_navigation_and_nontrigger_findings.json (successful producer1748b). Full inputs/PNGs/4MiB snapshots/262 callbacks verified,zero errors/mismatches,no pending command,host/core restored. No fixtures/save input. Actual Sea View,Deck View andRoute Map were opened;no B23 entry andno Bruges arrival. Amsterdam2 andBruges3 names/port points were independently read from original town models. Native Deck View opening is NOT a demonstrated B23 trigger. The navigation-only attempts do not invalidate the verified revised wind22 test.

NEXT inspect original EV2 event conditions andnative B23 selector before more manual travel. Source EV2 body begins96;action-table begin/end at header4C/50,inline boundary5C. The existing full loader proves action kind2 supplies only block index,not event reachability. Do not assume B23 is triggered by Deck View or Bruges arrival. Use authorized isolated coherent location/health/inventory fixtures if useful after proving exact ownership;do not force event/result flags. Fresh runtime test should use original eligibility/trigger andordinary choice selection.

Then verify both revised choice branches,later crew lesson,pages andtransitions;finish source-bound interpreter callers andall36 branch/reference maps;approve the scoped lesson relocation contract;register a cumulative post-layer after lil_opening_editorial;build exact clean patch;verify unchanged components/startup/shops andactual research/release byte equivalence. Only then close64. Full editorial goal remains much broader.

'''+text[end:]
    text+='\n## Latest terminal checkpoint V1749\n\n'+note+'\n\nThe1748 audit failed on its first attempt because the harness explicitly serializes buttons:[] for touch-only events. Successor1748b preserves that exact field andpasses;both executed producers are retained.\n'
    HANDOFF.write_text(text,encoding='utf-8')
    with Path('docs/lil_lessons_v1746_checkpoint.md').open('a',encoding='utf-8') as f:
        f.write('\n\n## Terminal follow-up V1749\n\n'+note+'\n')
    with Path('docs/translation_progress.md').open('a',encoding='utf-8') as f:
        f.write('\n\n## V1749 navigation terminal\n\n'+note+'\n')
    save(ROOT/'checkpoint_receipt.json', {'completed':1424,'source_prose_reviewed':1632,'new_completed':0,
        'native_layout_approved64_actual_wind22_still_valid':True,'all64_lesson_entries_still_incomplete':True,
        'all_current_jobs_terminal':True,'ordinary_navigation_proof':str(PROOF),'proof_sha256':sha(PROOF.read_bytes()),
        'ledger_sha256':sha(LEDGER.read_bytes()),'handoff_sha256':sha(HANDOFF.read_bytes()),
        'registered_candidate_unchanged_sha256':before['current_integrated_candidate']['sha256'],
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('V1749 ledger/handoff refreshed:all jobs terminal;B23 trigger investigation next;no completion credit orrelease change.')
