"""Inventory Fernan's exclusive given-name field; preserve spelling andnative allocation."""
import struct
from pathlib import Path
from ndspy.code import MainCodeFile
from dk4tool.patch.main_pool_cache_visibility import BASE,POOL
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.owned_name_fields_v2 import plan_arm9_name_fields
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load,save
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime

ROOT=Path('work/analysis/Rafael_Fernan_name_field_20261104')
RELEASE=Path('work/analysis/Rafael_B36_B41_release_verified_20261104/registered_release_verification.json')
NAMES=Path('work/analysis/Rafael_B51_B60_new_name_bindings_20261104/names.json')

if __name__=='__main__':
    assert not ROOT.exists()
    ctx=RegisteredRuntime(RELEASE,RELEASE.with_name('own_registered_startup_verification.json'),captain=0)
    names=load(NAMES);assert names['runtime']==ctx.receipt()
    consumers=[r for r in names['current_names']['rows'] if r['actor_ID']==35]
    assert len(consumers)==2 and all(r['text']=='Ｆernan Silveira' for r in consumers)
    arm=ctx.arm;clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    table,clean_table=[struct.unpack_from('<I',value,0xCDAC0)[0] for value in [arm,clean]]
    source_fields=[]
    for column in [0,4,8]:
        field=clean_table-BASE+32*35+column;pointer=struct.unpack_from('<I',clean,field)[0]
        at=pointer-BASE if pointer else None
        value=clean[at:clean.index(0,at)] if pointer else b''
        source_fields.append(dict(column=column,source_ARM9_field_offset=field,pointer=pointer,
            pointer_hex=clean[field:field+4].hex(),offset=at,hex=value.hex(),text=value.decode('cp932'),
            byte_length=len(value),status='printable-static-string' if pointer else 'null'))
    source=source_fields[0];assert source['text']=='フェルナン'
    sections=MainCodeFile(arm,BASE).sections;payload=bytes(sections[3].data[:-48]);assert len(payload)==123264
    field=table-BASE+32*35;pointer=struct.unpack_from('<I',arm,field)[0]
    stage=arm.find(bytes(sections[3].data));assert stage>=0 and arm.find(bytes(sections[3].data),stage+1)<0
    at=stage+pointer-POOL if POOL<=pointer<POOL+len(payload) else pointer-BASE
    before='Ｆernan'.encode('cp932');after=b'Fernan'+bytes(len(before)-len(b'Fernan'))
    assert arm[at:at+len(before)+1]==before+b'\0'
    owners=[]
    for actor in range(207):
        for column in [0,4,8]:
            f=table-BASE+32*actor+column;p=struct.unpack_from('<I',arm,f)[0]
            if pointer<=p<pointer+len(before):owners.append(dict(actor=actor,column=column,pointer=p,field_offset=f))
    refs=[dict(offset=i,pointer=struct.unpack_from('<I',arm,i)[0]) for i in range(0,len(arm)-3,4)
        if pointer<=struct.unpack_from('<I',arm,i)[0]<pointer+len(before)]
    reason='Keep the source-defined Fernan Silveira identity andexisting English spelling;normalize only the unintended full-width initial F in the given-name component. Both original name consumers use this field. No title,rank,relationship ornationality isadded.'
    row=dict(actor=35,column=0,table_field_offset=field,pointer=pointer,physical_offset=at,
        source_hex=before.hex(),target_hex=after.hex(),owned_bytes=len(before),current_text='Ｆernan',target_text='Fernan',
        source_clean_component=source,kind='latin-width-normalization',reason=reason,owners=owners,aligned_ARM9_references=refs,
        following16_hex=arm[at+len(before):at+len(before)+16].hex(),original_terminator_not_reallocated_orchanged=True,
        review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False))
    ROOT.mkdir();source_path=ROOT/'clean_name_fields.json'
    save(source_path,dict(source_ARM9_sha256=sha(clean),records=[dict(actor_ID=35,fields=source_fields)],
        native_clean_complete_name_binding=str(NAMES),native_clean_complete_name_binding_sha256=sha(NAMES.read_bytes()),
        source_field_read_after_current_dialogue_comparison=True,earlier_English_dialogue_unconsulted=False))
    proposal=dict(format='dk4-owned-name-fields-proposal-v2',runtime=ctx.receipt(),fields=[row],
        clean_name_fields=str(source_path),clean_name_fields_sha256=sha(source_path.read_bytes()),
        no_ROM_orARM9_changes_yet=True,shared_ownership_orunexpected_references_must_block_mutation=True,
        native_corrected_getters_font_planes_andregistered_deployment_pending=True,new_credit=0,producer_sha256=sha(Path(__file__).read_bytes()))
    target,proof=plan_arm9_name_fields(arm,proposal,clean)
    save(ROOT/'owned_fields_proposal.json',proposal);save(ROOT/'ownership_verification.json',proof)
    print('Fernan source field/exclusive owner/all621fields/interior aliases/complete inverse pass;native glyph planes pending.')
