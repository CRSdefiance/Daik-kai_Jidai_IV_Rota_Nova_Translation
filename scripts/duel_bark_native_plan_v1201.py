"""Source-locked16-reaction COMMON21 repack and exact native front successor."""
import struct
from pathlib import Path
from ndspy.code import MainCodeFile
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from dk4tool.patch.escape_direct_entries import current_entries
from dk4tool.patch.duel_editorial import owned_entries,COMPONENT,COMPONENT_SHA
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries,DIRECTORY_OFFSET,TABLE_OFFSET
from scripts.duel_bark_layout_v1200 import IDS,PROFILE,compiled
from scripts.duel_bark_front_v1201 import assemble,ADDRESS,END
from scripts.duel_cache_front_v1142 import assemble as prior_front
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/duel_bark_native_v1201')
SOURCE_COMMON='7f2d52592e5a88cca3fbf72f3a3474e822da5574fa8df564168d4699c1c375ba'
SOURCE_ARM='f7b408583816b4f71db0e85f04e0409d5464ce1c8ca1e343643a17350b8e04ce'


def plan(common,arm,doc):
    assert sha(common)==SOURCE_COMMON and sha(arm)==SOURCE_ARM
    assert doc['translation_policy']=='natural-dialogue-v2' and doc['target_locale']=='en-US'
    assert doc['consumer_layout_profile']==PROFILE and tuple(r['message_id'] for r in doc['records'])==IDS
    clean=NdsImage.open('work/clean.nds');accepted=NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    assert sha(Path('work/clean.nds').read_bytes())==doc['source_clean_ROM_sha256']
    jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),clean.read_file('/__arm9__.bin'))
    canonical=common_message_entries(accepted.read_file('/COMMON/MESFILE.DK4'),accepted.read_file('/__arm9__.bin'),clean=False)
    before=current_entries(common,arm);source=IlnkContainer.parse(common)
    component=COMPONENT.read_bytes();assert len(component)==1480 and sha(component)==COMPONENT_SHA
    prefix=component+bytes(4);assert source.blocks[21][:1484]==prefix
    authored={}
    for row in doc['records']:
        n=row['message_id'];assert row['source_hex']==jp[n].text.hex() and row['canonical_source_hex']==canonical[n].text.hex()
        assert row['current_text_hex']==before[n].text.hex() and all(row['review'][g] for g in ('source','context','localization','naturalness'))
        assert not row['source_native_macros'] and row['native_argument_count']==0
        value=compiled(row);assert value.hex()==row['compiled_hex'] and b'\n' not in value
        authored[n]=value
    assert [r.message_id for r in before if r.block==21]==list(range(1931,1977))
    body=bytearray(prefix);target=bytearray(arm);fields=[]
    for n in range(1931,1977):
        row=before[n];payload=source.blocks[21][row.block_offset:row.copy_end]
        assert 0<len(payload)<512 and payload.startswith(row.text+b'\0')
        if n in authored:
            assert not set(payload[len(row.text)+1:])-{0,32}
            payload=authored[n]+b'\0'
        at=TABLE_OFFSET+n*2;struct.pack_into('<H',target,at,len(body));fields.append([at,2]);body.extend(payload)
    assert 0<len(body)<=8192
    at=DIRECTORY_OFFSET+21*4;struct.pack_into('<HH',target,at,1931,len(body));fields.append([at,4])
    blocks=list(source.blocks);blocks[21]=bytes(body)
    old=prior_front(len(component))[0]+bytes(4)
    assert arm[ADDRESS-0x02000000:END-0x02000000]==old
    front,assembly=assemble(len(component));target[ADDRESS-0x02000000:END-0x02000000]=front
    c,a=IlnkContainer(blocks).to_bytes(),bytes(target)
    directory=sha(a[DIRECTORY_OFFSET:TABLE_OFFSET]);after=owned_entries(c,a,directory)
    assert len(after)==len(before)==3668
    assert all(y.text==authored.get(x.message_id,x.text) for x,y in zip(before,after,strict=True))
    assert all(blocks[i]==source.blocks[i] for i in range(41) if i!=21)
    for n in range(1931,1977):
        if n not in authored:
            x,y=before[n],after[n]
            assert blocks[21][y.block_offset:y.copy_end]==source.blocks[21][x.block_offset:x.copy_end]
    restored=bytearray(a)
    for at,size in [*fields,[ADDRESS-0x02000000,108]]:restored[at:at+size]=arm[at:at+size]
    assert bytes(restored)==arm and a[:0x800]==arm[:0x800]
    oldcode,newcode=map(lambda v:MainCodeFile(v,0x02000000),(arm,a))
    shape=lambda o:[(s.ramAddress,len(s.data),s.bssSize) for s in o.sections]
    assert shape(oldcode)==shape(newcode) and cache_plan(arm)==cache_plan(a)
    assert all(oldcode.sections[i].data==newcode.sections[i].data for i in (1,2,3,4))
    assert len(newcode.sections[3].data)-48==123040
    return c,a,{'source_COMMON_sha256':sha(common),'source_ARM9_sha256':sha(arm),
        'target_COMMON_sha256':sha(c),'target_ARM9_sha256':sha(a),'directory_sha256':directory,
        'changed_records':[f'COMMON_MESSAGE_{n}' for n in IDS],'native_IDs':list(IDS),
        'metadata_fields':fields,'owned_ARM9_fields':[[ADDRESS-0x02000000,108]],
        'new_code_prefix':{'component_bytes':1480,'component_sha256':COMPONENT_SHA},
        'front_assembly':assembly,'source_front_bytes104_target108_owned108':True,
        'only_new_front_memberships':[0x02117560,0x021175C0],
        'all3652_unselected_texts_all40_other_blocks_and_opaque1484_prefix_exact':True,
        'sections_BSS_arenas_cache_ITCM_and_entire123040_staged_bytes_exact':True,
        'all_other_ARM9_bytes_restore_exact':True,'repacked_block21_bytes':len(body),
        'native_font_scope_copy_and_actual_gameplay_pending':True,'full_goal_complete':False}


def main():
    assert not ROOT.exists()
    rom=NdsImage.open('out/all_routes_combined_v1189_candidate.nds')
    doc_path=Path('translations/duel_bark_editorial_manuscript_v1.json');doc=read(doc_path)
    c,a,proof=plan(rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin'),doc)
    ROOT.mkdir(parents=True);cp=ROOT/'target_COMMON_RESEARCH_ONLY.bin';ap=ROOT/'target_ARM9_RESEARCH_ONLY.bin'
    cp.write_bytes(c);ap.write_bytes(a)
    save(ROOT/'native_payload_plan.json',{**proof,'target_COMMON':str(cp),'target_ARM9':str(ap),
        'manuscript':str(doc_path),'manuscript_sha256':sha(doc_path.read_bytes()),
        'producer_sha256':sha(Path(__file__).read_bytes())})
    print('16 reactions packed in COMMON21;front108/108;all other text/allocations exact;native verification pending.',flush=True)


if __name__=='__main__':main()
