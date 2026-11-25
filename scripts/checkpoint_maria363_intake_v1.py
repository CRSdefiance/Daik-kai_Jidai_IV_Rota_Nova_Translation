"""Publish the next disjoint clean-only intake without changing registered credit."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v10 import checkpoint

ROOT = Path('work/Maria_B216_B252_clean_20261110')


def main():
    packetpath, selectionpath = ROOT/'clean_source_packet.json', ROOT/'source_selection_v1.json'
    releasepath = Path('work/maria321_B196_B215_release_v1/registered_release_verification.json')
    packet, selection, release = map(load,[packetpath,selectionpath,releasepath])
    assert (selection['source_objects'],selection['complete_exchanges']) == (363,37)
    assert selection['consumer_counts'] == {'ordinary-speech':266,'typed-menu-caption':12,'physical-style-alternative':85}
    assert packet['selected_blocks'] == list(range(216,253))
    assert selection['all_exact_clean_source_positions_rechecked'] and selection['exact_disjoint_credited_keys']
    assert selection['no_current_English_read_orapproval'] and selection['no_meanings_drafts_orlocalization_approval_yet']
    assert selection['registered_parent_sha256'] == release['candidate_sha256']
    evidence = {str(p):digest(p) for p in [packetpath,selectionpath,releasepath,Path(__file__)]}
    summary = ('Maria321 is registered and credited once:22,707 integrated;3,191 native story objects remain. '
        'The next363 clean-only objects are selected in37 complete SC3 groups B216–B252:266 ordinary bodies,85 physical style alternatives and12 captions. '
        'All source positions are exact,unique anddisjoint from prior credit. Current English isunread;clean meanings,independent drafts,contextual comparisons,names/terms andallfive gates remain pending. '
        'No new credit orROM;no worker islive. Registered5836b998,main andfull scope areunchanged.')
    document = 'docs/editorial_Maria363_B216_B252_intake_20261110.md'
    text = f'''# Maria363 B216–B252 clean-only intake — November 10, 2026

{summary}

[Registered Maria321](editorial_Maria321_B196_B215_registered_20261110.md) remains the current cumulative testing release:721 manifest entries,114 accepted layers,56 checks,exact clean-input patch,own startup and24 protected getters. Candidate SHA256:`{release['candidate_sha256']}`. This turn integrated andcredited that earlier321 once,then selected this separate uncredited intake. Do not restart its completed checks. Main promotion stillrequires acceptance;preserve all earlier translations,retentions,drafts,ROMs andevidence.

`work/Maria_B216_B252_clean_20261110/clean_source_packet.json` contains37 complete clean groups with363 exact source objects andtheir full command/block context. `source_selection_v1.json` rechecks each clean block/position,proves unique/disjoint source membership andbinds the registered parent. It reuses the qualified SC3_v13 native census rather than replaying inventory. Numeric block adjacency doesnot prove chronological orunconditional activation. No current story English hasbeen extracted;no prose,name ordisplay approval isclaimed.

Next read complete Japanese exchanges andrelevant surrounding source,including speaker/role controls,situations,relationships andemotional progression. Save every source meaning andindependent natural American English draft before current-English comparison. Preserve meaning,facts,voice,humor andcultural context;do not invent relationships,ranks orstory details. Use approved Rafael,Hodram,Joakim,Maria,Camille andother source-bound names. Review labels anddistinct native name consumers aspart oflocalization. Then compare whole conversations,retain working English withindividual reasons andreview earlier translation wherever its contextual pass remains unfinished.

Write logical paragraphs;use validated consumer-specific formatting toplace ordinary wraps. Audit premature rows,phrase/question-tag continuity,page boundaries andglyph consistency without shortening good prose. Preserve all controls/substitutions andbind complete style/menu aliases. Changed text requires fresh formatting,glyph/bounds/allocation/pagination checks anddirect review ofevery generated page. Reuse compatible technical proofs;use representative gameplay fordistinct behavior/concrete risks andclearly identify offline-only/unvisited content. No exhaustive natural playthrough isrequired. Integrate reviewed batches once necessary checks pass.

Integrated22,707 =13,576 revisions+9,131 retentions;historical source/prose/draft22,710. Native story remainder3,191 =Maria1,386+Lil1,805 includes this uncredited363. Shared/player-facing inventories remain separate. Preserve full story/town/shop/random/player-prose/name/wrap/glyph scope,earlier unfinished contextual passes andearly Rafael/tutorial priority. Retain the Market allocation/pointers,six-section ARM9,ASCII right bounds,source25v2,inherited B164R99 correction andall earlier assets. No guide photos. Deferred artwork andlater older-record technical re-audit remain separate. No cleanup,promotion,commit orpush occurred;no worker islive. Full goal remains active.
'''
    checkpoint(mutation=ROOT/'intake_progress_checkpoint_v1',batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0,current_batch='Maria363 B216–B252 clean-only intake;meanings andindependent drafts pending.',
            current_batch_not_yet_integrated=True,current_batch_registered_andcredited_once=False,
            all_current_batch_fifth_gates_pending=True,proposed_revisions=0,justified_retentions=0,
            native_job_live=False,native_sessions=[],stored_job_live=False,stored_sessions=[],registered_build_live=False,
            registered_cumulative_build_live=False,current_batch_evidence=evidence,guide_photos=False,
            next_action='Read37 complete Japanese groups andsurroundings;seal363 clean meanings andindependent drafts before current-English comparison.'),
        new_entries={'Maria_SC3_B216_B252_clean_20261110':dict(new_credit=0,source_objects=363,complete_exchanges=37,
            source_speech_objects=266,physical_style_alternatives=85,typed_choice_labels=12,clean_source_selected=True,
            all_five_review_gates_pending=True,clean_meanings_andindependent_drafts_pending=True,current_English_not_read=True,
            registered_integration_pending=True,evidence=evidence,full_goal_complete=False)},
        summary=summary,document=document,document_text=text,completed=22707,
        protected={'translations/release_stack.json':release['registry_sha256'],release['candidate']:release['candidate_sha256'],
            release['manifest']:release['manifest_sha256'],release['patch']:release['patch_sha256'],release['canonical_base']:release['canonical_sha256']})
    save(ROOT/'intake_checkpoint.json',dict(document=document,evidence=evidence,new_credit=0,
        no_batch_worker_live=True,current_English_not_read=True,full_goal_complete=False))
    print('Published363 clean-only objects in37 complete groups;meanings/drafts/allgates pending;22707 integrated unchanged.')


if __name__ == '__main__':
    main()
