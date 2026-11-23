"""Stage Hodram's port lesson over the registered cumulative ROM."""

from collections import Counter
from inspect import getsource
import json
from pathlib import Path

from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import preview_hodram_baltic_trade_20261121 as preview
from scripts import register_refit_sailing_parallel_routes_20261121 as parent
from scripts.stage_hodram_alexandria_tutorial_20261121 import compiler, plan_progressive
from scripts.source_locked_derivation_v5118 import checked_text


base, native = parent.base, parent.native
ROOT = Path('work/analysis/hodram_baltic_trade_20261121')
ROM, PROOF = ROOT / 'Hodram_Baltic_Trade_STAGED.nds', ROOT / 'stored_proof.json'
OUTPUT = ROOT / 'contextual_review.json'
SCENE, BLOCK = '/data/SC1.DK4', 43


def review_rows(original, stored):
    receipt, planned = map(base.load, (preview.dialogue.REVIEW, preview.PROOF))
    assert receipt['candidate_sha256'] == planned['candidate_sha256'] == base.digest(parent.ROM)
    assert planned['draft_sha256'] == base.digest(preview.dialogue.REVIEW)
    assert base.digest(planned['sheet']['path']) == planned['sheet']['sha256']
    layout_revision = 'DK4_MES_B43_R0039'
    rows = []
    for item in receipt['records']:
        row = item | dict(route=1, kind='progressive', current_reference=item['registered_reference'],
                          source_hex=item['source_reference']['exact_stored_hex'],
                          current_hex=item['registered_reference']['exact_stored_hex'])
        for block, side in ((original, 'source'), (stored, 'current')):
            ref = row[f'{side}_reference']
            body = bytes.fromhex(row[f'{side}_hex'])
            assert ref['block_sha256'] == native.digest(block)
            assert block[ref['offset']:ref['offset'] + len(body)] == body
            assert body[0] == row['source_selector']
        if row['id'] == layout_revision:
            row.update(english="The world's largest trade network is the fastest way to build the world's strongest fleet.",
                       protected_phrases=["The world's largest trade network", "the world's strongest fleet"],
                       decision='revision',
                       localization_note='Hodram sums up the lesson. Keep the largest trade network and strongest fleet together. '
                                         'The comparison and quickest path remain, without the split after the possessive.',
                       review=row['review'] | {'formatting': False})
        row['finding'] = 'prose and wrap' if row['decision'] == 'revision' else 'retention'
        rows.append(row)
    assert len(rows) == 9
    return rows, planned, layout_revision


def main():
    assert not ROOT.exists()
    release = base.load(parent.RELEASE)
    assert release['candidate_sha256'] == base.digest(parent.ROM)
    assert release['clean_input_sha256'] == base.digest(native.CLEAN)
    assert release['registry_sha256'] == base.digest(base.REGISTRY)
    clean, target = map(base.NdsImage.open, (native.CLEAN, parent.ROM))
    before = native.files(target)
    arm, clean_arm = before[native.ARM], clean.read_file(native.ARM)
    archive, source_archive = [native.IlnkContainer.parse(data) for data in (before[SCENE], clean.read_file(SCENE))]
    old, original = archive.blocks[BLOCK], source_archive.blocks[BLOCK]
    rows, planned, layout_revision = review_rows(original, old)
    inventory, _, _ = native.scoped_inventory()
    source = checked_text(getsource(compiler.rebuild_function), {'workflow.plan_progressive': 'plan_progressive'})
    namespace = compiler.env | {'plan_progressive': plan_progressive}
    exec(compile(source, __file__ + '::relocation', 'exec'), namespace)
    new, commands, plans = namespace['rebuild_function']()(rows, original, old, inventory, clean_arm, arm, None)
    assert len(plans) == 5 and len(plans[layout_revision]['lines']) == 3
    for entry in planned['tested']:
        assert json.loads(json.dumps(plans[entry['id']])) == entry['automatic_plan']
    assert all(plan['expected_native_pages'] == 1 for plan in plans.values())
    archive.blocks[BLOCK] = new
    payload = archive.to_bytes()
    archive.blocks[BLOCK] = old
    assert archive.to_bytes() == before[SCENE]
    target.replace_file(SCENE, payload)
    after = native.files(target)
    assert before.keys() == after.keys() and {p for p in before if before[p] != after[p]} == {SCENE}
    guard = base.load(base.REGISTRY)['profiles'][release['profile']]['source25_multiarchive_guard']
    percent = bind_registered_story_percent_guard(guard)(native.files(clean), after)
    assert percent['total_exact_source_bound_relocated_leading25_count'] == 7
    assert not any(percent['source_bound_new_command_counts'].values())
    # The isolated story block does not own selected name catalogue entries.
    catalogue = base.load(parent.MANIFEST)['relocations'][native.ARM]['reviewed_name_integration']['catalog']
    def catalogue_owners(files):
        banks = [native.IlnkContainer.parse(files[f'/data/SC{i}.DK4']).blocks for i in range(4)]
        return compiler.stage.progressive.native.catalogue(arm, catalogue, banks)
    assert catalogue_owners(before) == catalogue_owners(after)
    image = bytes(target.rom.save())
    target.replace_file(SCENE, before[SCENE])
    assert bytes(target.rom.save()) == parent.ROM.read_bytes()
    ROOT.mkdir()
    ROM.write_bytes(image)
    base.save(OUTPUT, dict(translation_policy='natural-dialogue-v2', encoder='dialogue-relocatable-v1',
        target_locale='en-US', source_packet=str(preview.dialogue.REVIEW), source_packet_sha256=base.digest(preview.dialogue.REVIEW),
        previous_sha256=release['candidate_sha256'], previous_registry_sha256=release['registry_sha256'],
        decisions=dict(Counter(row['decision'] for row in rows)), records=rows, new_editorial_credit=0))
    base.save(PROOF, dict(candidate_sha256=base.digest(ROM), predecessor_sha256=release['candidate_sha256'],
        manuscript_sha256=base.digest(OUTPUT), clean_sha256=release['clean_input_sha256'],
        groups=[dict(route=1, file_path=SCENE, block=BLOCK, before=native.digest(old), after=native.digest(new),
                     source=native.digest(original), commands=commands, plans=plans)],
        changed_blocks={SCENE: [BLOCK]}, whole_parent_inverse=True, source25=percent, stored_check_only=True))
    print('Staged five revised panels with exact stored commands, unchanged catalogue and whole-ROM inverse.')


if __name__ == '__main__':
    main()
