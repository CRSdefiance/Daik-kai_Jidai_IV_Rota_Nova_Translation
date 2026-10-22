"""Preserve complete31 paragraphs in the smallest fitting existing24-block range."""

from copy import deepcopy
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch import barmaid_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script import common_message_table as parser
from scripts.context_barmaid_dialogue_v779 import ROOT as SOURCE, CURRENT
from scripts.prepare_recruitment_common_v772 import local_entries
from scripts.verify_village_wrap_v608 import read, save

ROOT = owned.ROOT
MANUSCRIPT = Path('translations/barmaid_editorial_manuscript_v2.json')


def main():
    closure = read(ROOT/'latent996_caller_closure.json')
    assert closure['retained_latent996_context_classified']
    assert len(closure['all114_original_town_getter_and_main_NPC_guard_cases']) == 114
    assert not read(SOURCE/'layouts_v1/name_token_findings.json')['unresolved_prose_or_layout_findings']
    assert read(ROOT/'scope_proof.json')['cases'] == 34343
    doc = deepcopy(read('translations/barmaid_editorial_manuscript_v1.json'))
    for row in doc['records']:
        assert not row['review']['formatting']
        if row['message_id'] == 996:
            assert not row['review']['context']
            row['review']['context'] = True
            row['context'] = 'Original latent city58 barmaid speech. Two original caller chains,all114 native town/NPC guards and three classified source scan coincidences establish the source context. No initialized catalog city/actor pairing selects996;retain wording and original dispatch without claiming ordinary activation.'
            row['localization_note'] = 'Retain this natural source-faithful wording. V780 closes its original context as latent speech;normal activation remains unclaimed. No city or NPC catalog is altered.'
        row['review']['formatting'] = True
        row['status'] = 'native-reviewed-production-integration-and-gameplay-pending'
        if row['message_id'] in (989, 999):
            row['localization_note'] += ' Five sampled weak-ending diagnostics are exactly player-name initials,proved by expanded-byte origins with a literal-prose negative. Preserve every name byte;no English article warning is waived.'
    doc.update({'context_closure': str(ROOT/'latent996_caller_closure.json'),
                'first_name_contract': str(SOURCE/'captain_first_name_bound.json'),
                'typed_name_layout_proof': str(SOURCE/'layouts_v1/name_token_findings.json'),
                'status': 'native-reviewed-production-integration-and-gameplay-pending'})
    for key, path in (('source_clean_COMMON_sha256', 'work/clean.nds'),
                       ('source_canonical_COMMON_sha256', 'out/raphael_natural_v2_accepted_base.nds')):
        doc[key] = sha(NdsImage.open(path).read_file('/COMMON/MESFILE.DK4'))
    save(MANUSCRIPT, doc)
    rom = NdsImage.open(CURRENT)
    common, arm = rom.read_file('/COMMON/MESFILE.DK4'), rom.read_file('/__arm9__.bin')
    patched, _ = owned.runtime_transform(arm)
    authored = {r['message_id']: owned.compile_text(r) for r in doc['records']}
    c, a, fields, mapping = owned.plan(common, patched, authored)
    digest = sha(a[parser.DIRECTORY_OFFSET:parser.TABLE_OFFSET])
    before = parser.common_message_entries(common, arm, clean=False)
    after = local_entries(digest)(c, a, clean=False)
    assert all(y.text == authored.get(x.message_id, x.text) for x, y in zip(before, after, strict=True))
    blocks = [IlnkContainer.parse(v).blocks for v in (common, c)]
    assert all(x == y for i, (x, y) in enumerate(zip(*blocks, strict=True)) if i not in range(12, 36))
    for n in (1854, 1865):
        x, y = before[n], after[n]
        assert blocks[0][x.block][x.block_offset:x.copy_end] == blocks[1][y.block][y.block_offset:y.copy_end]
    assert all(before[n].text == after[n].text for n in (676, 677))
    (ROOT/'COMMON_RESEARCH_ONLY.bin').write_bytes(c)
    (ROOT/'COMBINED_ARM9_RESEARCH_ONLY.bin').write_bytes(a)
    save(ROOT/'prospective_common_repack.json', {
        'source_ROM_sha256': sha(CURRENT.read_bytes()), 'source_COMMON_sha256': sha(common), 'source_ARM9_sha256': sha(arm),
        'target_COMMON_sha256': sha(c), 'target_ARM9_sha256': sha(a), 'directory_sha256': digest,
        'metadata_fields': fields, 'complete2336_selection_map': mapping, 'selected31': sorted(authored),
        'all3637_other_strings_and17_other_blocks_exact': True, 'opaque1854_1865_and_user676_677_exact': True,
        'manuscript_sha256': sha(MANUSCRIPT.read_bytes()), 'producer_sha256': sha(Path(__file__).read_bytes()),
        'production_parser_and_registry_unchanged': True})
    print('31 complete paragraphs fit existing24 blocks12-35;3637 other strings,tails and prior formatting repairs exact.', flush=True)


if __name__ == '__main__':
    main()
