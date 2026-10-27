"""Exact15-message repack and source-owned two-caller static dispatch."""
import struct
from pathlib import Path
from ndspy.code import MainCodeFile
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.duel_bark_editorial import current_entries
from dk4tool.patch.duel_editorial import owned_entries,COMPONENT,COMPONENT_SHA
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from dk4tool.patch.common_single_cache_v861 import SINGLE
from dk4tool.script.common_message_table import common_message_entries,DIRECTORY_OFFSET,TABLE_OFFSET
from scripts.duel_special_dispatch_v1217 import helper,front,HELPER,HELPER_END,FRONT,FRONT_END
from scripts.duel_special_layout_v1216 import IDS,PROFILE,compiled
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/duel_special_native_v1218')
SOURCE_COMMON='bf95c202ec1715e6f0e61f529e6d22e0e13b3559a451be3c3e5dae3a63827b0c'
SOURCE_ARM='13478d94d189bf0fa89b4af2e29147ca8fc7a0567651fb1238e75265071d479d'


def plan(common,arm,doc):
    assert sha(common)==SOURCE_COMMON and sha(arm)==SOURCE_ARM
    assert doc['translation_policy']=='natural-dialogue-v2' and doc['target_locale']=='en-US'
    assert doc['consumer_layout_profile']==PROFILE and tuple(r['message_id'] for r in doc['records'])==IDS
    clean=NdsImage.open('work/clean.nds');accepted=NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    assert sha(Path('work/clean.nds').read_bytes())==doc['source_clean_ROM_sha256']
    jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),clean.read_file('/__arm9__.bin'))
    canonical=common_message_entries(accepted.read_file('/COMMON/MESFILE.DK4'),accepted.read_file('/__arm9__.bin'),clean=False)
    before=current_entries(common,arm);source=IlnkContainer.parse(common)
    component=COMPONENT.read_bytes();assert sha(component)==COMPONENT_SHA and len(component)==1480
    assert source.blocks[21][:1484]==component+bytes(4)
    authored={}
    for row in doc['records']:
        n=row['message_id'];assert row['source_hex']==jp[n].text.hex() and row['canonical_source_hex']==canonical[n].text.hex()
        assert row['current_text_hex']==before[n].text.hex() and all(row['review'][g] for g in ('source','context','localization','naturalness'))
        assert row['native_argument_count']==0 and not row['source_native_macros']
        value=compiled(row);assert row['compiled_hex']==value.hex() and b'\n' not in value;authored[n]=value
    assert {before[n].block for n in authored}=={22,23}
    rebuilt=list(source.blocks);target=bytearray(arm);fields=[];groups={}
    for block in (22,23):
        numbers=[r.message_id for r in before if r.block==block];groups[block]=numbers
        assert numbers==list(range(numbers[0],numbers[-1]+1));body=bytearray()
        for n in numbers:
            row=before[n];payload=source.blocks[block][row.block_offset:row.copy_end]
            assert 0<len(payload)<512 and payload.startswith(row.text+b'\0')
            if n in authored:
                assert not set(payload[len(row.text)+1:])-{0,32};payload=authored[n]+b'\0'
            at=TABLE_OFFSET+n*2;struct.pack_into('<H',target,at,len(body));fields.append([at,2]);body.extend(payload)
        assert 0<len(body)<=8192;rebuilt[block]=bytes(body)
        at=DIRECTORY_OFFSET+block*4;struct.pack_into('<HH',target,at,numbers[0],len(body));fields.append([at,4])
    dispatch=read('work/analysis/duel_special_dispatch_v1217/owned_dispatch_proof.json')
    assert dispatch['source_ARM9_sha256']==sha(arm) and dispatch['exact_live_single_slot_return0_BX_prefix_preserved']
    h,ha,hn=helper();f,fa,fn=front(1480)
    assert h.hex()==dispatch['helper_hex'] and f.hex()==dispatch['target_front_hex']
    assert arm[HELPER-0x02000000:HELPER_END-0x02000000].hex()==dispatch['source_tail_hex']
    assert arm[FRONT-0x02000000:FRONT_END-0x02000000].hex()==dispatch['source_front_hex']
    target[HELPER-0x02000000:HELPER_END-0x02000000]=h;target[FRONT-0x02000000:FRONT_END-0x02000000]=f
    c,a=IlnkContainer(rebuilt).to_bytes(),bytes(target);directory=sha(a[DIRECTORY_OFFSET:TABLE_OFFSET])
    after=owned_entries(c,a,directory)
    assert all(y.text==authored.get(x.message_id,x.text) for x,y in zip(before,after,strict=True))
    assert all(rebuilt[b]==source.blocks[b] for b in range(41) if b not in groups)
    for block,numbers in groups.items():
        for n in numbers:
            if n not in authored:
                x,y=before[n],after[n];assert source.blocks[block][x.block_offset:x.copy_end]==rebuilt[block][y.block_offset:y.copy_end]
    ranges=[[HELPER-0x02000000,64],[FRONT-0x02000000,108]];restored=bytearray(a)
    for at,size in [*fields,*ranges]:restored[at:at+size]=arm[at:at+size]
    assert bytes(restored)==arm and a[:0x800]==arm[:0x800]
    assert a[0x535E0:0x535E8]==arm[0x535E0:0x535E8]==SINGLE
    old,new=map(lambda v:MainCodeFile(v,0x02000000),(arm,a));shape=lambda o:[(s.ramAddress,len(s.data),s.bssSize) for s in o.sections]
    assert shape(old)==shape(new) and cache_plan(arm)==cache_plan(a)
    assert all(old.sections[i].data==new.sections[i].data for i in (1,2,3,4)) and len(new.sections[3].data)-48==123040
    return c,a,{'source_COMMON_sha256':sha(common),'source_ARM9_sha256':sha(arm),'target_COMMON_sha256':sha(c),'target_ARM9_sha256':sha(a),
        'directory_sha256':directory,'changed_records':[f'COMMON_MESSAGE_{n}' for n in IDS],'native_IDs':list(IDS),
        'metadata_fields':fields,'owned_ARM9_fields':ranges,'repacked_native_groups':groups,
        'repacked_block22_23_lengths':[len(rebuilt[b]) for b in (22,23)],
        'new_code_prefix':{'block':21,'component_bytes':1480,'component_sha256':COMPONENT_SHA},
        'helper_assembly':ha,'front_assembly':fa,'helper_front_code_bytes':[hn,fn],
        'single_slot_return0_and_all_COMMON_CODE_LOCKS_unchanged':True,
        'all3653_unselected_texts_and_all39_other_blocks_and_opaque_prefix_exact':True,
        'all_other_ARM9_bytes_restore_exact_sections_BSS_cache_arena_ITCM_staged123040_unchanged':True,
        'original_native_fonts_copies_and_actual_special_activation_pending':True,'full_goal_complete':False}


def main():
    assert not ROOT.exists();rom=NdsImage.open('out/all_routes_combined_v1206_candidate.nds')
    manuscript=Path('translations/duel_special_editorial_manuscript_v1.json')
    c,a,proof=plan(rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin'),read(manuscript))
    ROOT.mkdir(parents=True);cp=ROOT/'target_COMMON_RESEARCH_ONLY.bin';ap=ROOT/'target_ARM9_RESEARCH_ONLY.bin';cp.write_bytes(c);ap.write_bytes(a)
    save(ROOT/'native_payload_plan.json',{**proof,'target_COMMON':str(cp),'target_ARM9':str(ap),
        'manuscript':str(manuscript),'manuscript_sha256':sha(manuscript.read_bytes()),'producer_sha256':sha(Path(__file__).read_bytes())})
    print('15 special calls packed in existing blocks22/23;64-byte helper and108-byte front stay within owned spans;verification pending.',flush=True)


if __name__=='__main__':main()
