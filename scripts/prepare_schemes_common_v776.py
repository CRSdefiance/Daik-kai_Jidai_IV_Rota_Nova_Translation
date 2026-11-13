"""Research repack of reviewed scheme paragraphs,without changing the registry."""

from copy import deepcopy
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch import tavern_schemes_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script import common_message_table as parser
from scripts.prepare_recruitment_common_v772 import local_entries
from scripts.verify_scheme_input_contract_v776 import ROOT
from scripts.verify_village_wrap_v608 import read,save

MANUSCRIPT=Path('translations/tavern_schemes_editorial_manuscript_v4.json')


def main():
    contract=read(ROOT/'input_contract.json')
    assert contract['editable_company_name_does_not_reach_these_original_scheme_consumers']
    assert read('work/analysis/tavern_schemes_layout_v775_v3/verification.json')['real_catalog_findings']==0
    doc=deepcopy(read('translations/tavern_schemes_editorial_manuscript_v3.json'))
    for row in doc['records']:
        assert not row['review']['formatting']
        row['review']['formatting']=True
        row['status']='source-context-native-layout-reviewed-owned-integration-and-gameplay-pending'
        row['localization_note']+=' V776 source callers,opposing-target filters and immutable name initializers prove this family cannot receive the player-edited company field. All39730 original fixed-name/catalog layouts are clean;unreachable player-name stress findings are retained separately,not waived for other consumers.'
    doc['input_contract']=str(ROOT/'input_contract.json')
    doc['status']='native-reviewed-integration-and-gameplay-pending'
    clean,canonical=[NdsImage.open(p) for p in ('work/clean.nds','out/raphael_natural_v2_accepted_base.nds')]
    doc['source_clean_COMMON_sha256']=sha(clean.read_file('/COMMON/MESFILE.DK4'))
    doc['source_canonical_COMMON_sha256']=sha(canonical.read_file('/COMMON/MESFILE.DK4'))
    save(MANUSCRIPT,doc)
    rom=NdsImage.open('out/all_routes_combined_v773_candidate.nds')
    common,arm=rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin')
    patched,_=owned.runtime_transform(arm)
    authored={r['message_id']:owned.compile_text(r) for r in doc['records']}
    c,a,fields,mapping=owned.plan(common,patched,authored)
    digest=sha(a[parser.DIRECTORY_OFFSET:parser.TABLE_OFFSET])
    reader=local_entries(digest)
    reader.__kwdefaults__=parser.common_message_entries.__kwdefaults__
    before=parser.common_message_entries(common,arm,clean=False)
    after=reader(c,a,clean=False)
    assert len(after)==3668
    assert all(y.text==authored.get(x.message_id,x.text) for x,y in zip(before,after,strict=True))
    old,new=[IlnkContainer.parse(v).blocks for v in (common,c)]
    assert all(x==y for i,(x,y) in enumerate(zip(old,new,strict=True)) if i not in range(2,30))
    for n in (1854,1865):
        x,y=before[n],after[n]
        assert old[x.block][x.block_offset:x.copy_end]==new[y.block][y.block_offset:y.copy_end]
    assert all(before[n].text==after[n].text for n in (676,677))
    (ROOT/'COMMON_RESEARCH_ONLY.bin').write_bytes(c)
    (ROOT/'COMBINED_ARM9_RESEARCH_ONLY.bin').write_bytes(a)
    save(ROOT/'prospective_common_repack.json',{'source_ROM_sha256':sha(Path('out/all_routes_combined_v773_candidate.nds').read_bytes()),
        'source_COMMON_sha256':sha(common),'source_ARM9_sha256':sha(arm),
        'target_COMMON_sha256':sha(c),'target_ARM9_sha256':sha(a),'directory_sha256':digest,
        'metadata_fields':fields,'complete2697_selection_map':mapping,'selected56':sorted(authored),
        'all3612_unselected_visible_strings_and13_blocks_exact':True,
        'opaque1854_1865_complete_payloads_and_user676_677_exact':True,
        'manuscript_sha256':sha(MANUSCRIPT.read_bytes()),'producer_sha256':sha(Path(__file__).read_bytes()),
        'production_parser_and_registry_unchanged':True})
    print('56 full paragraphs fit existing28 blocks;3612 other strings and opaque copy payloads exact. Research only.',flush=True)


if __name__=='__main__':main()
