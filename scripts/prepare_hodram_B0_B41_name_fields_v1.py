"""Prepare three exclusive source-bound surname fixes; do not create a ROM."""
import inspect
import struct
from pathlib import Path

from ndspy.code import MainCodeFile
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.main_pool_cache_visibility import BASE,POOL
from dk4tool.patch.owned_name_fields_v2 import plan_arm9_name_fields
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.gloss_hodram_B0_B41_clean_v1 import ROOT
from scripts.prove_lil_B167_names_v4124b import names
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.source_locked_derivation_v5118 import checked_text

OUT=ROOT/'name_field_inputs_v1'
SPECS=[
    (55,'Ｆlahven','Flahven','latin-width-normalization',
     'Retain David Flahven; replace only the full-width Latin F in the existing surname. The native progressive and full-name getters both expose this mismatched glyph.'),
    (56,'ザルツギッター','Salzgitter','source-surname-romanization',
     'Romanize the explicit surname ザルツギッター as Salzgitter, retaining Georg. Do not change it to George or add a birthplace, title or historical identity.'),
    (57,'カムロ','Kamuro','source-surname-romanization',
     'Romanize the explicit surname カムロ as Kamuro, retaining Nagayoshi. Add no kanji interpretation, warrior rank or real-world biography.'),
]


def main():
    assert not OUT.exists()
    bound_path=ROOT/'scoped_names_current_v1.json';bound=load(bound_path)
    runtime=bound['runtime'];ctx=RegisteredRuntime(runtime['release_proof'],runtime['startup_proof'],captain=runtime['captain'])
    assert ctx.receipt()==runtime
    assert digest(bound['target_candidate'])==bound['target_candidate_sha256']
    target_parent=NdsImage.open(bound['target_candidate'])
    assert target_parent.read_file('/__arm9__.bin')==ctx.arm
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    arm=ctx.arm;sections=MainCodeFile(arm,BASE).sections;payload=bytes(sections[3].data[:-48])
    assert len(payload)==123264
    staged=arm.find(bytes(sections[3].data));assert staged>=0 and arm.find(bytes(sections[3].data),staged+1)<0
    table=struct.unpack_from('<I',arm,0xCDAC0)[0]
    clean_table=struct.unpack_from('<I',clean,0xCDAC0)[0]
    clean_rows=[];proposal_rows=[];actors=[s[0] for s in SPECS]
    for actor,old,new,kind,reason in SPECS:
        row=next(r for r in bound['records'] if r['actor_ID']==actor)
        fields=[]
        for f in row['source_andcurrent_fields']:
            src=f['source'];pointer=src['pointer'];column=f['column'];at=clean_table-BASE+32*actor+column
            assert pointer==struct.unpack_from('<I',clean,at)[0]
            raw=bytes.fromhex(src['hex'])
            if pointer:assert clean[pointer-BASE:pointer-BASE+len(raw)+1]==raw+b'\0'
            fields.append(dict(column=column,source_ARM9_field_offset=at,pointer_hex=clean[at:at+4].hex(),
                pointer=pointer,offset=pointer-BASE if pointer else None,hex=raw.hex(),text=src['text'],
                byte_length=len(raw),status='printable-static-string' if pointer else 'source-null-component-no-text'))
        clean_rows.append(dict(actor_ID=actor,fields=fields))
        column=4;field=table-BASE+32*actor+column;pointer=struct.unpack_from('<I',arm,field)[0]
        at=staged+pointer-POOL if POOL<=pointer<POOL+len(payload) else pointer-BASE
        before=old.encode('cp932');after=new.encode('ascii')
        assert arm[at:at+len(before)+1]==before+b'\0' and len(after)<=len(before)
        owners=[]
        for ident in range(207):
            for col in (0,4,8):
                f=table-BASE+32*ident+col;p=struct.unpack_from('<I',arm,f)[0]
                if pointer<=p<pointer+len(before):owners.append(dict(actor=ident,column=col,pointer=p,field_offset=f))
        references=[dict(offset=i,pointer=struct.unpack_from('<I',arm,i)[0]) for i in range(0,len(arm)-3,4)
            if pointer<=struct.unpack_from('<I',arm,i)[0]<pointer+len(before)]
        assert owners==[dict(actor=actor,column=4,pointer=pointer,field_offset=field)]
        assert references==[dict(offset=field,pointer=pointer)]
        proposal_rows.append(dict(actor=actor,column=4,table_field_offset=field,pointer=pointer,physical_offset=at,
            source_hex=before.hex(),target_hex=(after+bytes(len(before)-len(after))).hex(),owned_bytes=len(before),
            current_text=old,target_text=new,source_clean_component=next(f for f in fields if f['column']==4),
            kind=kind,reason=reason,owners=owners,aligned_ARM9_references=references,
            following16_hex=arm[at+len(before):at+len(before)+16].hex(),original_terminator_not_reallocated_orchanged=True,
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False)))
    source=checked_text(inspect.getsource(names),{
        'for ident in [2,4,13,23,109]:':'for ident in ACTORS:',
        "            print(dict(actor=ident,consumer=kind,text=value,rings=len(rings),writes=len(writes)),flush=True)":"            assert value == data.decode('cp932')",
        'all_ten_original_consumers_and_owned_or_readonly_memory_paths_exact=True':
            'all_requested_original_consumers_and_owned_or_readonly_memory_paths_exact=True',
    })
    OUT.mkdir()
    clean_path=OUT/'clean_name_fields.json';save(clean_path,dict(records=clean_rows,source_ARM9_sha256=digest('work/clean.nds') if False else __import__('hashlib').sha256(clean).hexdigest(),
        source_static_fields_rebound_without_new_constructor_permutations=True,new_credit=0))
    proposal=dict(format='dk4-owned-name-fields-proposal-v2',runtime=runtime,fields=proposal_rows,
        clean_name_fields=str(clean_path),clean_name_fields_sha256=digest(clean_path),
        target_registered_candidate=bound['target_candidate'],target_registered_candidate_sha256=bound['target_candidate_sha256'],
        target_ARM9_exact_to_qualified_runtime=True,no_ROM_orARM9_changes_yet=True,
        native_corrected_getters_font_planes_gameplay_andregistered_deployment_pending=True,
        all_alias_owners_andaligned_references_exclusive=True,new_credit=0,producer_sha256=digest(__file__))
    _,proof=plan_arm9_name_fields(arm,proposal,clean)
    save(OUT/'owned_fields_proposal.json',proposal)
    save(OUT/'proposed_plan.json',proof)
    save(OUT/'current_name_bindings.json',dict(runtime=runtime,actors=actors,
        current_names=dict(rows=[r for row in bound['records'] if row['actor_ID'] in actors for r in row['current_consumers']]),
        source_owned_current_adapter=source,source_owned_current_adapter_sha256=__import__('hashlib').sha256(source.encode()).hexdigest(),
        original84_getter_receipt=str(bound_path),original84_getter_receipt_sha256=digest(bound_path),new_credit=0))
    print(dict(proposed_fields=len(proposal_rows),owned_bytes=proof['owned_span_bytes'],changed_bytes=proof['changed_bytes'],
        whole_ARM9_inverse=proof['complete_parent_inverse_exact'],no_ROM_created=True))


if __name__=='__main__':main()
