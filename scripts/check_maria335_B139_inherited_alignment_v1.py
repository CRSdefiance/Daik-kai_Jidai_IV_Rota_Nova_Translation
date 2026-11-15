"""Reject drift in the exact inherited25/26-byte native-command alignment binding."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.rebuild_maria335_B137_B151_reviewed_v2 import rebuild_block
from scripts.meaning_maria335_B137_B151_v1 import ROOT
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest


def main():
    out=ROOT/'inherited_alignment_guard_v1.json';assert not out.exists()
    docpath=ROOT/'formatting_v1/formatting_input.json';planpath=ROOT/'plan_native_v4/automatic_plans.json'
    rebuiltpath=ROOT/'reconstruction_v2/reconstruction.json'
    doc,plan,rebuilt=map(load,[docpath,planpath,rebuiltpath])
    group=next(g for g in rebuilt['groups'] if g['block']==139)
    assert group['source_current_andclean_block_inverse_exact']
    binding=group['inherited_source_alignment_pad_binding']
    assert binding['id']=='DK4_MES_B139_R0177' and binding['full_clean_andparent_inverses_still_exact']
    image=NdsImage.open(doc['current_ROM']);source=NdsImage.open('work/clean.nds')
    arm=image.read_file('/__arm9__.bin')
    clean=IlnkContainer.parse(source.read_file(doc['file_path'])).blocks[139]
    current=IlnkContainer.parse(image.read_file(doc['file_path'])).blocks[139]
    rows=[deepcopy(r) for r in doc['records'] if r['block']==139]
    for row in rows:row['current_record_index']=row['current_reference']['record_index']
    plans={r['id']:r for r in plan['records']};inventory,_,_=scoped_inventory();rejected=[]
    for name in ['different-record','different-clean-body','different-current-body','nonzero-clean-padding','different-offset']:
        records=deepcopy(rows);a=bytearray(clean);b=bytearray(current)
        row=next(r for r in records if r['id']=='DK4_MES_B139_R0177')
        if name=='different-record':row['id']='UNBOUND_RECORD'
        elif name=='different-clean-body':row['source_hex']=row['source_hex'][:-2]+'41'
        elif name=='different-current-body':row['current_hex']=row['current_hex'][:-2]+'41'
        elif name=='nonzero-clean-padding':a[2085]=0x41
        elif name=='different-offset':row['source_reference']['offset']+=2
        try:rebuild_block(arm,bytes(a),bytes(b),records,plans,inventory,[])
        except (AssertionError,KeyError,ValueError):rejected.append(name)
        else:raise AssertionError('Unbound alignment input was accepted: '+name)
    assert len(rejected)==5
    save(out,dict(exact_binding=binding,reconstruction=str(rebuiltpath),reconstruction_sha256=digest(rebuiltpath),
        rejected_unbound_cases=rejected,all_five_negative_controls_rejected=True,clean_andparent_native_command_end=2086,
        source_raw_string_not_expanded_orchanged=True,original_source_NUL_padding_only_used_for_complete_inverse=True,
        complete_clean_parent_archive_andserialized_NDS_inverses_already_pass=True,actual_gameplay=False,new_credit=0,
        evidence={str(p):digest(p) for p in [docpath,planpath,rebuiltpath,Path(__file__),Path('scripts/rebuild_maria335_B137_B151_reviewed_v2.py')]}))
    print('Exact inherited command alignment is bound; five drift/ownership negative controls rejected.')


if __name__=='__main__':main()
