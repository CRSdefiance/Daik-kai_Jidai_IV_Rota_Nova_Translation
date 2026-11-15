"""Select15 complete clean-only exchanges without exposing current story English."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v9 import checkpoint

ROOT=Path('work/Maria_B137_B151_clean_20261109')


def main():
    assert not ROOT.exists()
    packetpath=Path('work/story_source_coverage_20261109_SC3_v9/residual_clean_source_packet.json')
    censuspath=packetpath.with_name('coverage.json');releasepath=Path('work/maria337_release_v1/registered_release_verification.json')
    ledgerpath=Path('translations/editorial_review_current_v1.json')
    packet,census,release,ledger=map(load,[packetpath,censuspath,releasepath,ledgerpath])
    assert packet['source_only_not_current_English'] and census['new_exact_bindings']==337
    assert not census['inventory_failures'] and not census['legacy_source_bindings_not_exact']
    assert ledger['records_editorially_completed']==21356 and ledger['current_integrated_candidate']['sha256']==release['candidate_sha256']
    assert digest('translations/release_stack.json')==release['registry_sha256']
    assert digest(packet['source_ROM'])==packet['source_ROM_sha256']
    clean=NdsImage.open(packet['source_ROM']);archive=clean.read_file('/data/SC3.DK4')
    from dk4tool.patch.grand_race_menu_release import sha
    assert sha(archive)==packet['source_archive_sha256'] and sha(clean.read_file('/__arm9__.bin'))==packet['source_ARM9_sha256']
    bank=IlnkContainer.parse(archive).blocks
    groups=deepcopy([g for g in packet['groups'] if 137<=g['block']<=151])
    assert [g['block'] for g in groups]==list(range(137,152))
    rows=[r for g in groups for r in g['records']]
    assert len(rows)==len({r['id'] for r in rows})==335
    assert Counter(r['kind'] for r in rows)=={'ordinary-speech':333,'typed-menu-caption':2}
    oldkeys={(r['file_path'],r['id']) for r in ledger['contextual_story_natural_dialogue_pass_v1871']['integrated_record_keys']}
    assert len(oldkeys)==21356 and not oldkeys & {(r['file_path'],r['id']) for r in rows}
    for g in groups:
        block=bytes.fromhex(g['clean_block_hex']);assert block==bank[g['block']]
        for r in g['records']:
            assert not r['covered'] and not r['exact_credited_source_bindings']
            at=r['source_reference']['offset'];raw=bytes.fromhex(r['source_hex'])
            assert block[at:at+len(raw)]==raw
    ROOT.mkdir();selected=ROOT/'clean_source_packet.json'
    save(selected,{**packet,'groups':groups,'records':335,'selected_blocks':list(range(137,152)),
        'selection_parent':str(packetpath),'selection_parent_sha256':digest(packetpath),
        'source_only_not_current_English':True,'new_credit':0})
    receipt=ROOT/'source_selection_v1.json'
    save(receipt,dict(source_packet=str(selected),source_packet_sha256=digest(selected),source_objects=335,complete_exchanges=15,
        source_speeches=333,typed_captions=2,blocks=list(range(137,152)),
        exact_source_refs=[dict(id=r['id'],block=r['block'],source_reference=r['source_reference'],source_hex=r['source_hex']) for r in rows],
        all_complete_clean_blocks_andsource_positions_exact=True,disjoint_from_all21356_integrated_record_keys=True,
        native_inventory_exact_dependency_reuse_not_replayed=True,current_story_English_not_read=True,
        meanings_independent_drafts_contextual_comparisons_names_terms_andall_five_gates_pending=True,
        actual_gameplay=False,new_ROM=False,new_credit=0,full_goal_complete=False,
        evidence={str(p):digest(p) for p in [packetpath,censuspath,releasepath,ledgerpath,Path(__file__)]}))
    summary=('Maria337 remains registered and credited once:21,356 integrated,4,542 native story objects remaining. '
        'The next335 clean-only objects are selected in15 complete SC3 exchanges B137–B151:333 speeches andtwo captions. '
        'Every clean block/source reference is exact and disjoint from prior credit; no current story English was read. '
        'Meanings,independent drafts,contextual comparisons,names/terms andall five gates are pending. No new ROM or credit;no worker is live. '
        'Main and the full editorial objective are unchanged.')
    evidence={str(p):digest(p) for p in [selected,receipt,releasepath,censuspath,Path(__file__)]}
    text=f'''# Next Maria335 clean-only intake — November 9, 2026

{summary}

The completed [Maria337 registered checkpoint](editorial_Maria337_registered_20261109.md) remains authoritative for the current testing candidate, patch,717-entry/114-layer/52-check release, all five gates, gameplay evidence and once-only credit. Do not repeat those checks. Candidate SHA-256 `{release['candidate_sha256']}`. Preserve all accepted runtime/name/market/bounds/font/graphics layers. Main promotion still requires acceptance.

New work root: `work/Maria_B137_B151_clean_20261109`. `clean_source_packet.json` contains all15 complete clean blocks and335 exact source objects from the SC3_v9 residual packet. `source_selection_v1.json` binds each source reference and bytes, verifies complete clean ROM/archive/ARM9 identities and proves disjointness from all21,356 credited keys. The qualified complete native inventory is reused, not replayed. No current-English extraction, draft, translation finding, contextual gate or display approval is claimed.

Next read the Japanese exchanges in full; save their meanings and independently authored logical English paragraphs before reading current English. Then compare each individual record in whole-conversation context, retain good wording with reasons, bind names/roles/terms and preserve all speaker/layout/runtime controls. Newly changed text needs fresh formatting checks and all generated-page visual review. Reuse existing display/loader proofs only with exact relevant dependencies. Apply substantial batches and representative behavior/gameplay tests without requiring every optional activation. All prior unfinished contextual passes, remaining storylines,shared/town/shop/random dialogue andplayer-facing prose remain in scope. Early Rafael/tutorial priority is retained. Deferred graphics artwork and the later older-record technical re-audit remain separate. No guide photos,cleanup,promotion,commit orpush.
'''
    checkpoint(mutation=ROOT/'intake_progress_checkpoint_v1',batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0,current_batch='Next Maria335 clean-only intake B137–B151; meanings and drafts pending.',
            current_batch_not_yet_integrated=True,current_batch_registered_andcredited_once=False,all_current_batch_fifth_gates_pending=True,
            native_job_live=False,native_sessions=[],registered_build_live=False,registered_cumulative_build_live=False,
            guide_photos=False,current_batch_evidence=evidence,next_action='Read15 complete Japanese exchanges;seal335 meanings andindependent drafts before current-English comparison.'),
        new_entries={'Maria_SC3_B137_B151_clean_20261109':dict(new_credit=0,source_objects=335,complete_exchanges=15,source_speech_objects=333,
            typed_choice_labels=2,clean_source_selected=True,all_five_review_gates_pending=True,clean_meanings_andindependent_drafts_pending=True,
            current_English_not_read=True,registered_integration_pending=True,full_goal_complete=False,evidence=evidence)},
        summary=summary,document='docs/editorial_Maria335_B137_B151_intake_20261109.md',document_text=text,completed=21356,
        protected={'translations/release_stack.json':release['registry_sha256'],release['candidate']:release['candidate_sha256'],
            release['manifest']:release['manifest_sha256'],release['patch']:release['patch_sha256'],release['canonical_base']:release['canonical_sha256']})
    print('Selected335 clean objects in15 complete exchanges;all meanings/drafts/gates pending;zero new credit.')


if __name__=='__main__':main()
