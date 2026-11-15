"""Publish the next disjoint clean-only intake without changing completed credit."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v10 import checkpoint

ROOT = Path('work/Maria_B196_B215_clean_20261110')


def main():
    packet_path = ROOT/'clean_source_packet.json'
    selection_path = ROOT/'source_selection_v1.json'
    release_path = Path('work/maria305_B176_B195_release_v1/registered_release_verification.json')
    packet, selection, release = map(load,[packet_path,selection_path,release_path])
    assert (selection['source_objects'],selection['complete_exchanges']) == (321,18)
    assert selection['consumer_counts'] == {'physical-style-alternative':21,'ordinary-speech':296,'typed-menu-caption':4}
    assert selection['all_exact_clean_source_positions_rechecked'] and selection['exact_disjoint_credited_keys']
    assert selection['no_current_English_read_orapproval'] and selection['no_meanings_drafts_orlocalization_approval_yet']
    assert selection['registered_parent_sha256'] == release['candidate_sha256']
    evidence = {str(p):digest(p) for p in [packet_path,selection_path,release_path,Path(__file__)]}
    summary = ('Maria305 remains registered and credited once: 22,386 integrated, 3,512 native story objects remaining. '
        'The next 321 clean-only objects are selected in 18 complete SC3 groups B196–B215: 296 ordinary bodies, '
        '21 physical style alternatives and four captions. Every clean position is exact and disjoint from prior credit. '
        'Current English has not been read; meanings, independent drafts, comparisons, names/terms and all five gates remain pending. '
        'No new credit or ROM; no worker is live. Main and full scope remain unchanged.')
    document = 'docs/editorial_Maria321_B196_B215_intake_20261110.md'
    text = f'''# Maria321 B196–B215 clean-only intake — November 10, 2026

{summary}

[The registered Maria305 checkpoint](editorial_Maria305_B176_B195_registered_20261110.md) remains authoritative for the cumulative testing ROM, exact clean-input patch, 720 entries/114 accepted layers/55 release checks, startup/protected getters and once-only credit. Candidate SHA-256: `{release['candidate_sha256']}`. Reuse the completed checks; preserve every prior translation, justified retention, draft, ROM and evidence file. Main promotion requires user acceptance.

New work root: `work/Maria_B196_B215_clean_20261110`. `clean_source_packet.json` contains 18 complete clean groups and all their commands, with 321 exact source objects from the qualified SC3_v12 residual inventory. `source_selection_v1.json` rechecks complete clean blocks and each source position, proves unique/disjoint source membership and binds the registered parent. The existing native inventory was reused, not replayed. Groups are196–204,206,208–215;205/207 are already covered. Numeric adjacency does not establish chronology or unconditional activation. No current story English was extracted, and no translation, retention, name or display finding is approved yet.

Next read the complete Japanese exchanges and relevant source surroundings, speaker/role controls and relationships. Save all clean meanings and independent natural American English drafts before consulting current English. Then compare complete conversations, preserving wording that works with individual reasons and revising meaning, voice, humor, phrase continuity and speaker labels where needed. Use approved names and source-supported facts; preserve native controls and runtime substitutions. This batch includes three families of physical style alternatives and two menu objects, whose exact aliases/consumers must be bound before display approval. No future roster/voice assignment is implied by this intake.

Use substantial reviewed batches, logical paragraphs and validated consumer-specific wrapping. Changed records receive fresh formatting and complete generated-page visual review. Reuse completed native/storage/display proofs only when their relevant dependencies match; use representative gameplay for distinct behavior and concrete risks. Clearly identify offline-only and unvisited conditional content. Integrate through the registered cumulative workflow after necessary checks, retaining the Market allocation/pointers, ASCII bounds, source25 v2, earlier name/font/graphics layers and inherited B164R99 correction.

Integrated22,386 =13,405 revisions+8,981 retentions; historical source/prose/draft22,389. Native story remainder3,512 =Maria1,707+Lil1,805 includes these uncredited321; shared/player-facing inventories remain separate. Full storyline/town/shop/random/player-prose/name/wrap/glyph scope, earlier unfinished contextual passes and early Rafael/tutorial priority remain active. No guide photos. Deferred graphics artwork and the later older-record technical re-audit remain separate. No cleanup, promotion, commit or push occurred.
'''
    checkpoint(mutation=ROOT/'intake_progress_checkpoint_v1',batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0,current_batch='Maria321 B196–B215 clean-only intake; meanings and independent drafts pending.',
            current_batch_not_yet_integrated=True,current_batch_registered_andcredited_once=False,
            all_current_batch_fifth_gates_pending=True,proposed_revisions=0,justified_retentions=0,
            native_job_live=False,native_sessions=[],stored_job_live=False,stored_sessions=[],registered_build_live=False,
            registered_cumulative_build_live=False,current_batch_evidence=evidence,guide_photos=False,
            next_action='Read18 complete Japanese groups and relevant surroundings; seal321 meanings and independent drafts before current-English comparison.'),
        new_entries={'Maria_SC3_B196_B215_clean_20261110':dict(new_credit=0,source_objects=321,complete_exchanges=18,
            source_speech_objects=296,physical_style_alternatives=21,typed_choice_labels=4,clean_source_selected=True,
            all_five_review_gates_pending=True,clean_meanings_andindependent_drafts_pending=True,current_English_not_read=True,
            registered_integration_pending=True,evidence=evidence,full_goal_complete=False)},
        summary=summary,document=document,document_text=text,completed=22386,
        protected={'translations/release_stack.json':release['registry_sha256'],release['candidate']:release['candidate_sha256'],
            release['manifest']:release['manifest_sha256'],release['patch']:release['patch_sha256'],release['canonical_base']:release['canonical_sha256']})
    save(ROOT/'intake_checkpoint.json',dict(document=document,evidence=evidence,new_credit=0,
        no_batch_worker_live=True,current_English_not_read=True,full_goal_complete=False))
    print('Published321 clean-only objects in18 complete groups; meanings/drafts/allgates pending;22386 integrated unchanged.')


if __name__ == '__main__':
    main()
