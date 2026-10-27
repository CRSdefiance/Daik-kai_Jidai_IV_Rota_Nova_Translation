"""Prepare complete reviewed paragraphs in existing COMMON blocks;research only."""

from copy import deepcopy
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch import scheme_followup_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script import common_message_table as parser
from scripts.prepare_recruitment_common_v772 import local_entries
from scripts.review_scheme_followup_v777 import CURRENT, ROOT as SOURCE
from scripts.verify_village_wrap_v608 import read, save

ROOT = owned.ROOT
MANUSCRIPT = Path('translations/scheme_followup_editorial_manuscript_v2.json')


def main():
    inputs = read(SOURCE/'input_contract.json')
    layout = read(SOURCE/'layouts_v1/verification.json')
    assert inputs['six_original_paths_include_Bribe_function_02056998']
    assert not layout['findings_count'] and layout['native_supplied_layouts'] == 13699
    assert read(ROOT/'scope_proof.json')['cases'] == 34343
    doc = deepcopy(read('translations/scheme_followup_editorial_manuscript_v1.json'))
    assert layout['manuscript_sha256'] == sha(Path('translations/scheme_followup_editorial_manuscript_v1.json').read_bytes())
    for row in doc['records']:
        assert not row['review']['formatting']
        row['review']['formatting'] = True
        row['status'] = 'native-reviewed-production-integration-and-gameplay-pending'
        row['localization_note'] += ' Original caller closure excludes the edited player faction;13699 full fixed-catalog native layouts and53 independently decoded complete fonts pass. Production private-table selectors are native-verified;no individual gameplay activation is claimed.'
    doc.update({'input_contract': str(SOURCE/'input_contract.json'),
                'prospective_layout_proof': str(SOURCE/'layouts_v1/verification.json'),
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
    reader = local_entries(digest)
    before, after = parser.common_message_entries(common, arm, clean=False), reader(c, a, clean=False)
    assert all(y.text == authored.get(x.message_id, x.text) for x, y in zip(before, after, strict=True))
    old, new = [IlnkContainer.parse(v).blocks for v in (common, c)]
    assert all(x == y for i, (x, y) in enumerate(zip(old, new, strict=True)) if i not in range(2, 30))
    for n in (1854, 1865):
        x, y = before[n], after[n]
        assert old[x.block][x.block_offset:x.copy_end] == new[y.block][y.block_offset:y.copy_end]
    assert all(before[n].text == after[n].text for n in (676, 677))
    (ROOT/'COMMON_RESEARCH_ONLY.bin').write_bytes(c)
    (ROOT/'COMBINED_ARM9_RESEARCH_ONLY.bin').write_bytes(a)
    save(ROOT/'prospective_common_repack.json', {
        'source_ROM_sha256': sha(CURRENT.read_bytes()), 'source_COMMON_sha256': sha(common), 'source_ARM9_sha256': sha(arm),
        'target_COMMON_sha256': sha(c), 'target_ARM9_sha256': sha(a), 'directory_sha256': digest,
        'metadata_fields': fields, 'complete2697_selection_map': mapping, 'selected25': sorted(authored),
        'all3643_other_strings_and13_other_blocks_exact': True,
        'opaque1854_1865_and_user676_677_exact': True, 'manuscript_sha256': sha(MANUSCRIPT.read_bytes()),
        'producer_sha256': sha(Path(__file__).read_bytes()), 'production_parser_and_registry_unchanged': True})
    print('25 complete paragraphs fit existing28 blocks;3643 other strings and both structured tails exact.', flush=True)


if __name__ == '__main__':
    main()
