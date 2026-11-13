"""Bind complete clean control headers to the existing unchanged native role receipt."""
from copy import deepcopy
from pathlib import Path
import struct
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/Maria_B216_B252_clean_20261110')


def main():
    out=ROOT/'formatting_v1/role_bindings_v2.json';assert not out.exists()
    oldpath=ROOT/'formatting_v1/role_bindings.json';docpath=ROOT/'formatting_v1/formatting_input.json'
    packetpath=ROOT/'clean_source_packet.json';old,doc,packet=map(load,[oldpath,docpath,packetpath])
    assert old['runtime']==doc['runtime']
    rows={r['id']:r for r in doc['records']};blocks={g['block']:bytes.fromhex(g['clean_block_hex']) for g in packet['groups']}
    result=deepcopy(old);counts={'ordinary-speech':0,'4100-style-alternative':0}
    for role in result['source_records']:
        row=rows[role['id']];ref=row['source_reference'];raw=bytes.fromhex(row['source_hex']);block=blocks[row['block']]
        assert role['source_reference']==ref and role['source_selector']==row['source_selector']
        assert block[ref['offset']:ref['offset']+len(raw)]==raw
        role['original_source_kind']=role['kind']
        if row.get('native_object_kind')=='4100-style-alternative':
            assert role['kind']=='physical-style-alternative'
            at=row['source_command_offset'];whole=bytes.fromhex(row['source_object_hex'])
            assert block[at:at+len(whole)]==whole and whole[:20].hex()==row['source_header_hex']
            assert whole[:2]==b'\0A' and whole[19]==row['source_selector']
            offsets=struct.unpack_from('<8H',whole,2)
            assert row['source_style_indices']==[i for i,v in enumerate(offsets) if at+20+v==ref['offset']]
            role.update(kind='4100-style-alternative',source_header_hex=row['source_header_hex'],
                source_style_indices=row['source_style_indices'],virtual_prefix_not_in_stored_body=True)
        else:
            assert role['kind']=='ordinary-speech' and block[ref['offset']-5:ref['offset']+1].hex()==row['source_complete_preamble_hex']
            role['source_complete_preamble_hex']=row['source_complete_preamble_hex']
        counts[role['kind']]+=1
    assert counts=={'ordinary-speech':6,'4100-style-alternative':85}
    assert result['native_roles']==old['native_roles']
    result.update(complete_original_preamble_orstyle_header_bindings=True,role_dispatch_receipt_reused_without_new_assignments=True,
        original_schema_projection=str(oldpath),original_schema_projection_sha256=digest(oldpath),
        native_preflight_schema_failure_preserved=True,no_prose_plan_ROM_or_role_assignment_changes=True,
        evidence={**old['evidence'],**{str(p):digest(p) for p in [oldpath,docpath,packetpath,Path(__file__)]}})
    save(out,result);print('Bound6 ordinary and85 virtual-style controls to exact clean headers; original native roles unchanged.')


if __name__=='__main__':main()
