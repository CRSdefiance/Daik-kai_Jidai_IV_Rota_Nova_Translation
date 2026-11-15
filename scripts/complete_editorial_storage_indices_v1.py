"""Bind the rebuilder's current-index alias from exact inventoried storage bytes."""
import argparse
from copy import deepcopy
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--inputs',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    a=p.parse_args();assert not a.out.exists()
    original=a.inputs/'storage_manuscript.json';doc=load(original)
    image=NdsImage.open(doc['current_ROM']);assert sha(Path(doc['current_ROM']).read_bytes())==doc['current_ROM_sha256']
    blocks=IlnkContainer.parse(image.read_file(doc['file_path'])).blocks
    count=0
    for row in doc['records']:
        if row['kind']=='typed-choice-label' or row.get('native_object_kind')=='4100-style-alternative':continue
        at=row['current_reference']['offset'];block=blocks[row['block']]
        index=block[:at].count(b'\0');assert index==row['current_reference']['record_index']
        if 'current_record_index' in row:assert row['current_record_index']==index
        else:row['current_record_index']=index;count+=1
        raw=bytes.fromhex(row['current_hex']);assert block[at:at+len(raw)+1]==raw+b'\0'
    doc.update(storage_current_index_aliases_added=count,previous_storage_manuscript=str(original),
        previous_storage_manuscript_sha256=sha(original.read_bytes()),no_prose_compiled_bytes_native_orreview_gate_changes=True)
    a.out.mkdir();target=a.out/'storage_manuscript.json';save(target,doc)
    plan=load(a.inputs/'compiled_plans.json');plan.update(manuscript=str(target),manuscript_sha256=sha(target.read_bytes()))
    planpath=a.out/'compiled_plans.json';save(planpath,plan)
    for filename in ['native_pages.json','styles.json','menus.json']:
        prior=a.inputs/filename;value=deepcopy(load(prior));value.update(manuscript=str(target),manuscript_sha256=sha(target.read_bytes()),
            previous_metadata_bridge=str(prior),previous_metadata_bridge_sha256=sha(prior.read_bytes()))
        if 'plan' in value:value.update(plan=str(planpath),plan_sha256=sha(planpath.read_bytes()))
        save(a.out/filename,value)
    packet=a.inputs/'packet.json';save(a.out/'packet.json',load(packet))
    print('Bound',count,'exact current-record index aliases; all prose/native results unchanged.')

if __name__=='__main__':main()
