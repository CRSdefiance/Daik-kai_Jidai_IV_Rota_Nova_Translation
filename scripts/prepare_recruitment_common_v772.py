"""Research-only whole-selection repack with exact source and phrase pins."""

import inspect
from pathlib import Path
from types import FunctionType

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch import tavern_continuation_editorial as previous
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script import common_message_table as parser
from scripts.context_tavern_recruitment_v771 import CURRENT
from scripts.review_tavern_recruitment_v771 import MANUSCRIPT,ARGUMENTS
from scripts.verify_recruitment_owned_v772 import ROOT
from scripts.verify_village_wrap_v608 import read,save


def local_entries(digest):
    env=dict(parser.__dict__)
    env['RELOCATED_DIRECTORY_HASHES']=parser.RELOCATED_DIRECTORY_HASHES|{digest}
    return FunctionType(parser.common_message_entries.__code__,env,argdefs=parser.common_message_entries.__defaults__)


def main():
    native=read(ROOT/'native_layout/verification.json');owned=read(ROOT/'owned_runtime_plan.json')
    assert native['complete_native_layouts']==3423 and native['manuscript_sha256']==sha(MANUSCRIPT.read_bytes())
    assert read(ROOT/'native_layout/identical_to_reviewed_v771.json')['all3423_complete_case_records_exact']
    doc=read(MANUSCRIPT);rom=NdsImage.open(CURRENT)
    common=rom.read_file('/COMMON/MESFILE.DK4');arm=(ROOT/'ARM9_RESEARCH_ONLY.bin').read_bytes()
    assert sha(arm)==owned['target_ARM9_sha256']
    clean,canonical=[NdsImage.open(p) for p in('work/clean.nds','out/raphael_natural_v2_accepted_base.nds')]
    source=parser.common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),clean.read_file('/__arm9__.bin'))
    accepted=parser.common_message_entries(canonical.read_file('/COMMON/MESFILE.DK4'),canonical.read_file('/__arm9__.bin'),clean=False)
    before=parser.common_message_entries(common,rom.read_file('/__arm9__.bin'),clean=False);authored={}
    for row in doc['records']:
        n=row['message_id'];text=row['english'].removesuffix('{PAD}')
        assert 883<=n<=907 and source[n].text.hex()==row['source_hex']
        assert accepted[n].text.hex()==row['canonical_source_hex'] and before[n].text.hex()==row['current_text_hex']
        assert text==' '.join(text.split()) and text.isascii() and all(32<=ord(c)<127 for c in text)
        assert row['source_native_arguments']==ARGUMENTS.get(n,[])
        assert row['English_argument_source_indices']==list(range(len(ARGUMENTS.get(n,[]))))
        assert text.count('%s')==len(ARGUMENTS.get(n,[])) and '%' not in text.replace('%s','')
        authored[n]=b' '+text.encode()
    env=dict(previous.__dict__);env['IDS']=tuple(range(883,908))
    c,a,fields,mapping=FunctionType(previous.plan.__code__,env)(common,arm,authored)
    digest=sha(a[parser.DIRECTORY_OFFSET:parser.TABLE_OFFSET])
    entry_reader=local_entries(digest)
    # FunctionType does not carry keyword-only defaults automatically.
    entry_reader.__kwdefaults__=dict(parser.common_message_entries.__kwdefaults__)
    after=entry_reader(c,a,clean=False)
    assert len(after)==3668
    assert all(y.text==authored.get(x.message_id,x.text) for x,y in zip(before,after,strict=True))
    old,new=[IlnkContainer.parse(value).blocks for value in(common,c)]
    assert all(x==y for i,(x,y) in enumerate(zip(old,new,strict=True)) if i not in range(2,24))
    for n in(1854,1865):
        x,y=before[n],after[n]
        assert old[x.block][x.block_offset:x.copy_end]==new[y.block][y.block_offset:y.copy_end]
    for n in(676,677):assert before[n].text==after[n].text
    (ROOT/'COMMON_RESEARCH_ONLY.bin').write_bytes(c);(ROOT/'COMBINED_ARM9_RESEARCH_ONLY.bin').write_bytes(a)
    save(ROOT/'prospective_common_repack.json',{'source_ROM_sha256':sha(CURRENT.read_bytes()),
        'source_COMMON_sha256':sha(common),'source_ARM9_sha256':sha(rom.read_file('/__arm9__.bin')),
        'target_COMMON_sha256':sha(c),'target_ARM9_sha256':sha(a),'directory_sha256':digest,
        'metadata_fields':fields,'complete2151_selection_map':mapping,'selected25':sorted(authored),
        'all3643_unselected_visible_strings_and19_unselected_blocks_exact':True,
        'opaque1854_1865_complete_native_payloads_and_user676_677_exact':True,
        'source_plan_module_sha256':sha(Path(previous.__file__).read_bytes()),
        'manuscript_sha256':sha(MANUSCRIPT.read_bytes()),'producer_sha256':sha(Path(__file__).read_bytes()),
        'production_parser_registry_ROM_and_completion_unchanged':True})
    print(f'25 complete paragraphs fit existing blocks2-23;3643 other strings exact. Research directory:{digest}',flush=True)


if __name__=='__main__':main()
