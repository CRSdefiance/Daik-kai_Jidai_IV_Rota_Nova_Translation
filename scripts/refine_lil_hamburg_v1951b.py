"""Faithful concision for one five-row FE draft; preserve the first manuscript."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

OLD=Path('translations/lil_hamburg_recruitment_editorial_manuscript_v1.json')
NEW=Path('translations/lil_hamburg_recruitment_editorial_manuscript_v2.json')

if __name__=='__main__':
    assert not NEW.exists()
    probe=read('work/analysis/lil_Hamburg_body_probe_v1951/body_only_prose_layout_research.json')
    assert [r['id']for r in probe['rows']if'error'in r]==['DK4_MES_B74_R0312']
    doc=deepcopy(read(OLD))
    row=next(r for r in doc['records']if r['id']=='DK4_MES_B74_R0312')
    row['previous_editorial_English']=row['english']
    row['english']='{SPEAKER:FE}In battle, set your course and sail direction as usual. Guns fire automatically when an enemy enters range.{PAD}'
    row['localization_note']+=' As usual concisely preserves the normal-sailing control comparison;both course/sail direction andthe automatic-fire/range condition remain. This resolves the conservative five-row research overflow without trimming source facts orclaiming FE geometry approval.'
    doc.update(predecessor_manuscript=str(OLD),predecessor_manuscript_sha256=sha(OLD.read_bytes()),
        body_only_refinement_proof='work/analysis/lil_Hamburg_body_probe_v1951/body_only_prose_layout_research.json')
    save(NEW,doc)
    print(dict(successor=str(NEW),refined_id=row['id'],all_source_facts_preserved=True,FE_geometry_still_pending=True))
