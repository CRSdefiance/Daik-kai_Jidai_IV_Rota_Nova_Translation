"""Reject non-owned,altered ormissing-alignment variants before reconstruction."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load,save
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from dk4tool.script.maria303_source_alignment_v1 import source_storage_span,OWNER,SOURCE,ENGLISH

ROOT=Path('work/Maria_B58_B70_clean_20261109')

def main():
    out=ROOT/'source_alignment_qualification_v1.json';assert not out.exists()
    docpath=ROOT/'storage_inputs_v1/storage_manuscript.json';packetpath=ROOT/'storage_inputs_v1/packet.json'
    doc,packet=map(load,[docpath,packetpath]);row=next(r for r in doc['records'] if r['id']==OWNER)
    group=next(g for g in packet['groups'] if g['block']==62)
    clean,current=map(bytes.fromhex,[group['clean_block_hex'],group['current_block_hex']])
    arm=NdsImage.open(doc['current_ROM']).read_file('/__arm9__.bin');inventory,_,_=scoped_inventory()
    assert source_storage_span(arm,clean,current,row,SOURCE,ENGLISH,inventory)==SOURCE+b'\0'
    wrong=deepcopy(row);wrong['id']='unowned'
    shifted=deepcopy(row);shifted['source_reference']['offset']+=1
    changed_source=bytearray(clean);changed_source[784]=32
    changed_current=bytearray(current);changed_current[785]=32
    cases=[('wrong owner',clean,current,wrong),('shifted source',clean,current,shifted),
        ('source terminator changed',bytes(changed_source),current,row),('current terminator changed',clean,bytes(changed_current),row)]
    rejected=[]
    for name,a,b,r in cases:
        try:source_storage_span(arm,a,b,r,SOURCE,ENGLISH,inventory)
        except AssertionError:rejected.append(name)
        else:raise AssertionError('Accepted non-owned source-alignment variant: '+name)
    assert len(rejected)==4
    save(out,dict(owner=OWNER,source_body_hex=SOURCE.hex(),current_body_hex=ENGLISH.hex(),physical_source_inverse_span_hex=(SOURCE+b'\0').hex(),
        complete_native_command_extent_unchanged=38,source_meaning_body_andcontrols_unchanged=True,
        ownership_negative_cases_rejected=rejected,whole_block_archive_NDS_inverses_andstored_native_checks_still_required=True,new_credit=0,
        evidence={str(p):digest(p) for p in [docpath,packetpath,Path('dk4tool/script/maria303_source_alignment_v1.py'),Path(__file__)]}))
    print('Qualified one exact source-owned alignment span;four non-owned/modified cases rejected. No ROM change orreview credit.')

if __name__=='__main__':main()
