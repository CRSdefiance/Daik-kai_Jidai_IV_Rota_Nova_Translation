"""Register the twelve scoped wrap corrections with the established cumulative publisher."""

from inspect import getsource
from pathlib import Path
from types import SimpleNamespace
from xml.etree import ElementTree

from scripts import register_lil_ceramics_wrap_20261111 as prior
from scripts import replay_historical_story_wraps_20261111 as replay
from scripts import stage_historical_story_wraps_20261111 as stage
from scripts import verify_historical_story_wraps_storage_20261111 as storage
from scripts.source_locked_derivation_v5118 import checked_text


base = stage.base
parent = SimpleNamespace(ROM=prior.ROM, MANIFEST=prior.MANIFEST, RELEASE=prior.RELEASE, CLEAN=stage.CLEAN)
PROFILE = 'all-routes-historical-story-wraps-v1-20261111'
CHECK = 'registered_historical_story_wraps_and_complete_parent_inverse'
ROOT = Path('out/historical_story_wraps_registered_20261111_v1')
ROM = ROOT / 'Translation_DS_All_Routes_Story_Wraps_20261111_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261111_story_wraps_candidate')
PATCH, VERIFICATION = PACKAGE/'translation.xdelta', PACKAGE/'verification'
REVIEW, RELEASE = (VERIFICATION/name for name in ('registered_review.json','registered_release_verification.json'))
QA = stage.ROOT/'repository_qa.xml'
DOC = Path('docs/editorial_historical_story_wraps_registered_20261111.md')
VIEWED = ['dfaa4f21caca05820e587de5d618f1075e3f4f91a0701c8f4afe83f3668afdb5',
          'da68226d1f57c48ed3b25275ebcfb62bcb6c1eef77365f8287d756b641121bad',
          '21cd511a7173b62708b949d9f8a89d378d0ec3093d08b04d1cb70728f03db9a3']


def verify_inputs():
    old, proof, setup, live, startup, draft, commands = map(base.load,
        (parent.RELEASE, stage.PROOF, replay.SETUP, replay.LIVE, replay.STARTUP, stage.REVIEW, storage.PROOF))
    assert base.digest(stage.REVIEW)==proof['review_sha256'] and base.digest(stage.PROOF)==setup['proof_sha256']
    assert base.digest(parent.CLEAN)==old['clean_input_sha256'] and base.digest(parent.MANIFEST)==old['manifest_sha256']
    assert base.digest(parent.ROM)==old['candidate_sha256']==proof['candidate_sha256']==live['parent_sha256']==commands['parent_sha256']
    assert base.digest(replay.ROM)==setup['candidate_sha256']==live['candidate_sha256']==startup['candidate_sha256']==commands['candidate_sha256']
    assert startup['cold_boot'] and not startup['savestate'] and len(startup['original_protected_name_getters'])==24
    assert len(startup['exact_matching_frames'])==6 and startup['complete_deployed_payload_exact']
    assert live['natural_Lil_New_Game'] and live['Carlo_initialized_in_Lil_entry'] and live['original_body_plane_only']
    assert len(live['observed'])==4 and sum(map(len,live['unchanged_sampled_frames'].values()))==8
    assert len(commands['owned_records'])==12 and commands['all_command_extents_offsets_branches_and_preambles_exact']
    assert commands['original_catalogue_helper_route_masks_and_entries_verified']
    assert proof['checked_complete_native_pages']==24 and proof['checked_original_processor_alignments']==96
    assert [base.digest(row['path']) for row in proof['sheets']]==[row['sha256'] for row in proof['sheets']]==VIEWED
    for dependencies in (live['evidence'],startup['evidence'],commands['dependencies']):
        assert all(base.digest(path)==digest for path,digest in dependencies.items())
    suites=list(ElementTree.parse(QA).iter('testsuite'))
    tests=sum(int(row.get('tests',0)) for row in suites)
    assert tests==56 and not any(int(row.get(key,0)) for row in suites for key in ('errors','failures','skipped'))
    return old,proof,live,draft,tests


def reconstruct(old, proof, draft):
    image=base.NdsImage.open(parent.ROM)
    before=prior.files(image)
    for path,raw in stage.transform(image,draft['records']):
        record=proof['archives'][path]
        assert stage.sha(raw)==record['sha256'] and stage.sha(before[path])==record['source_sha256']
        assert raw==Path(record['path']).read_bytes()
        image.replace_file(path,raw)
    after=prior.files(image)
    assert after.keys()==before.keys()
    assert {name for name in after if before[name]!=after[name]}==set(proof['archives'])
    assert bytes(image.rom.save())==replay.ROM.read_bytes()
    prior.verify_runtime(after[stage.ARM],old)
    for path in proof['archives']:
        image.replace_file(path,before[path])
    assert bytes(image.rom.save())==parent.ROM.read_bytes()


def derive():
    source=getsource(prior.main)
    refs=source[source.index('    refs ='):source.index('    review =')]
    metadata=source[source.index("    manifest['changed_records']"):source.index('    assert len(manifest[\'batches\']) == 781')]
    readme=source[source.index("    (PACKAGE / 'README.md')"):source.index("    base.save(PACKAGE / 'checksums.json'")]
    document=source[source.index('    base.replace_checked(DOC,'):source.index('    lead =')]
    edits={
        'release_stack.lil_ceramics.pending.json':'release_stack.story_wraps.pending.json',
        'editorial_review_current.lil_ceramics.pending.json':'editorial_review_current.story_wraps.pending.json',
        "== 780 and len(manifest['checks']) == 115":"== 781 and len(manifest['checks']) == 116",
        '(stage.PROOF, replay.LIVE, replay.STARTUP, QA)':'(stage.PROOF, storage.PROOF, replay.LIVE, replay.STARTUP, QA)',
        refs: "    records = [row | dict(review=row['review'] | {'formatting': True}, registered_reference=dict(\n"
              "        block=row['block'], file_path=row['file_path'], offset=row['current_reference']['offset'],\n"
              "        bytes=len(bytes.fromhex(row['target_hex'])), candidate_sha256=sha, raw_hex=row['target_hex'])) for row in draft['records']]\n",
        'release_stack_before_lil_ceramics.json':'release_stack_before_story_wraps.json',
        'verified_visible_gallery_captions_predecessor=predecessor, lil_ceramics_wrap_release=str(REVIEW)':'verified_lil_ceramics_predecessor=predecessor, historical_story_wraps_release=str(REVIEW)',
        'Contextual revision and full-width reflow of the Hamburg ceramics exchange.':'Twelve scoped dialogue revisions and reflows across the four routes.',
        metadata: "    for row in draft['records']:\n"
                  "        changes = manifest['changed_records'][row['file_path']]\n"
                  "        if row['id'] not in changes:\n"
                  "            changes.append(row['id'])\n"
                  "    manifest['historical_story_wraps_registered_successor_pipeline'] = dict(predecessor=predecessor,\n"
                  "        driver=str(Path(__file__)), driver_sha256=base.digest(__file__), review=str(REVIEW),\n"
                  "        review_sha256=base.digest(REVIEW), archives=proof['archives'], affected_blocks=proof['blocks'],\n"
                  "        original_native_extents_and_terminators_preserved=True, complete_parent_inverse_exact=True)\n",
        "== 781 and len(manifest['checks']) == 116\n":"== 782 and len(manifest['checks']) == 117\n",
        'registered_manifest_entries=781, passing_release_checks=116':'registered_manifest_entries=782, passing_release_checks=117',
        'changed_internal_files=[stage.FILE]':'changed_internal_files=sorted(proof[\'archives\'])',
        'prose_revisions=2, justified_retentions=15':'prose_revisions=3, justified_retentions=9',
        'revised_complete_pages=5, unchanged_scene_panels=12,\n                                       initialized_Lil_entry=True, natural_Hamburg_activation=False':'revised_complete_pages=4, surrounding_identical_frames=8,\n                                       natural_Lil_New_Game=True, representative_Carlo_initialized_at_entry=True',
        'The Hamburg ceramics exchange is registered with five retrospective display revisions.':'The twelve historical story wraps are registered.',
        'lil_ceramics_retrospective_20261111':'historical_story_wraps_retrospective_20261111',
        'existing_credit_preserved=17, prose_revisions=2, wrap_only_changes=3':'existing_credit_preserved=12, prose_revisions=3, wrap_only_changes=9',
        readme:"    (PACKAGE / 'README.md').write_text(package_notes(sha, release), encoding='utf-8', newline='\\n')\n",
        "['fixture_ROMs']":"['carlo_ROMs']",
        'Preserve Hamburg ceramics release and verification.':'Preserve the historical story wrap release and verification.',
        document:'    base.replace_checked(DOC, checkpoint_notes().encode())\n',
        'The Hamburg ceramics exchange is registered.':'The twelve historical story wraps are registered.',
        '781 entries, 114 accepted layers, 116 checks':'782 entries, 114 accepted layers, 117 checks',
    }
    return checked_text(source,edits)


def package_notes(sha, release):
    return f'''# Historical story wraps candidate

The [local ROM](../../{ROM.as_posix()}) contains twelve scoped corrections across all four routes. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{sha}` byte for byte from Japanese SHA-256 `{release['clean_input_sha256']}`. All original native boundaries and control bytes are preserved. Ordinary Lil New Game and an initialized Carlo scene verified four revised pages. A separate cold boot and 56 targeted tests passed.
'''


def checkpoint_notes():
    return f'''# Twelve historical story wraps registered

The [registered review](../{REVIEW.as_posix()}) covers twelve remaining leads from the earlier thirteen-record wrap inventory. Nine keep the existing English and change the line breaks. Three also revise wording, including Fernando’s permit explanation, Yifa’s martial-arts rumor and the injured sailor’s appeal to Maria. Lil’s earlier B218 correction remains present. The review records each complete surrounding exchange and the exact source, previous and registered positions. Every original terminator, actor selector, command offset and branch remains intact.

All 24 before-and-after native pages and 96 processor alignments passed, and all revised pages were visually checked. Paired ordinary Lil New Game runs displayed the three opening changes. A separate staged Lil-entry replay displayed Carlo’s revised line. Eight sampled surrounding frames matched exactly. Eight changes were checked offline in this pass. The original Carlo event trigger and hardware remain unvisited. A separate cumulative cold boot and 56 targeted tests passed.

The [local candidate and clean-input patch](../{PACKAGE.as_posix()}/README.md) include the previous registered layers. The dialogue ledger still credits 27,697 reviews. The 279 shared-text keys, remaining UI and name review, other wrap and glyph leads, and representative town and random-scene coverage remain open. The deferred artwork and later older-record technical re-audit remain separate.

The [broader wrap scan](../translations/editorial_checkpoints/SharedText_20261110_v1/current_progressive_wrap_triage_v1.json) flags 843 candidate bodies in the four current archives, including ten possible question-tag splits. These are storage heuristics. Confirm their typed owners and complete exchanges before assigning findings or changing text.
'''


def main():
    env=vars(prior)|globals()
    exec(compile(derive(),__file__+'::same-cumulative-publication-contract','exec'),env)
    env['main']()


if __name__=='__main__':
    main()
