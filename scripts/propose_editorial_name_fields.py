"""Source-bound in-place proposals for Fernando's glyph andSamwell's explicit name component."""
from pathlib import Path
import struct
from ndspy.code import MainCodeFile
from dk4tool.patch.main_pool_cache_visibility import BASE,POOL
from dk4tool.patch.grand_race_menu_release import sha
from scripts.registered_editorial_runtime import RegisteredRuntime
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Hodram_B91_B110_name_fields_20261101')
RELEASE=Path('work/analysis/Hodram_B81_B89_release_verified_20261101/registered_release_verification.json')
STARTUP=RELEASE.with_name('own_registered_startup_verification.json')
SOURCE=Path('work/analysis/Hodram_B91_B110_clean_20261101/clean_name_fields.json')

if __name__=='__main__':
    assert not ROOT.exists();ctx=RegisteredRuntime(RELEASE,STARTUP);arm=ctx.arm;source=load(SOURCE)
    sections=MainCodeFile(arm,BASE).sections;payload=bytes(sections[3].data[:-48]);assert len(payload)==123264
    table=struct.unpack_from('<I',arm,0xCDAC0)[0];fields=[]
    specs=[(20,0,'Ｆernando','Fernando','latin-width-normalization',
        'Retain the already established Fernando Dias spelling;normalize only the mismatched full-width initial F.'),
        (22,8,'ダ','da','source-name-component-romanization',
        'Render the explicit source name componentダ as da,retaining Samwell andKhan. It is part of the full name,not a new title,rank,nationality orbiography;progressive Samwell Khan is unchanged.')]
    for actor,column,old,new,kind,reason in specs:
        field=table-BASE+32*actor+column;pointer=struct.unpack_from('<I',arm,field)[0]
        if POOL<=pointer<POOL+len(payload):
            start=arm.find(bytes(sections[3].data));assert start>=0 and arm.find(bytes(sections[3].data),start+1)<0
            at=start+pointer-POOL
        else:at=pointer-BASE
        before=old.encode('cp932');after=new.encode('ascii')
        assert arm[at:at+len(before)+1]==before+b'\0' and len(after)<=len(before)
        after+=bytes(len(before)-len(after));owners=[]
        for ident in range(207):
            for col in [0,4,8]:
                f=table-BASE+32*ident+col;p=struct.unpack_from('<I',arm,f)[0]
                if pointer<=p<pointer+len(before):owners.append(dict(actor=ident,column=col,pointer=p,field_offset=f))
        aligned_references=[dict(offset=i,pointer=struct.unpack_from('<I',arm,i)[0]) for i in range(0,len(arm)-3,4)
            if pointer<=struct.unpack_from('<I',arm,i)[0]<pointer+len(before)]
        clean=next(r for r in source['records'] if r['actor_ID']==actor)
        cleanfield=next(f for f in clean['fields'] if f['column']==column)
        fields.append(dict(actor=actor,column=column,table_field_offset=field,pointer=pointer,physical_offset=at,
            source_hex=before.hex(),target_hex=after.hex(),owned_bytes=len(before),current_text=old,target_text=new,
            source_clean_component=cleanfield,kind=kind,reason=reason,owners=owners,aligned_ARM9_references=aligned_references,
            following16_hex=arm[at+len(before):at+len(before)+16].hex(),
            original_terminator_not_reallocated_orchanged=True,review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False)))
    ROOT.mkdir(parents=True)
    save(ROOT/'owned_fields_proposal.json',dict(format='dk4-owned-name-fields-proposal-v2',runtime=ctx.receipt(),fields=fields,
        clean_name_fields=str(SOURCE),clean_name_fields_sha256=sha(SOURCE.read_bytes()),
        no_ROM_orARM9_changes_yet=True,shared_ownership_orunexpected_references_must_block_mutation=True,
        native_corrected_getters_font_planes_gameplay_andregistered_deployment_pending=True,new_credit=0,
        producer_sha256=sha(Path(__file__).read_bytes())))
    print([(f['actor'],f['column'],f['physical_offset'],f['owned_bytes'],f['owners'],f['aligned_ARM9_references']) for f in fields])
