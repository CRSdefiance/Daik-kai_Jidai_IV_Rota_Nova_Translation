"""One naturalness refinement after the complete native preview review."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.encoder import encode_relocatable_dialogue
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

OLD=Path('translations/lil_london_editorial_manuscript_v2.json')
NEW=Path('translations/lil_london_editorial_manuscript_v3.json')

if __name__=='__main__':
    assert not NEW.exists()
    doc=deepcopy(read(OLD))
    row=next(r for r in doc['records'] if r['id']=='DK4_MES_B26_R0087')
    row['previous_editorial_English_v2']=row['english']
    row['english']="{SPEAKER:02}They say he's a towering giant with three eyes and a mouth that stretches from ear to ear. He drinks human blood from a goblet!{PAD}"
    row['localization_note']='Retain the grotesque rumor andall descriptive facts in natural spoken English;mouth that stretches from ear to ear reads better than the compressed noun phrase. The goblet drinking retains the sourceblood-drinking image. Noextra person,power orrelationship isadded.'
    row['formatting_refinement_reason']='Preview review prompted a naturalness improvement;this isnot a fixed-slot shortening. Allother110 paragraphs stayexact.'
    result=encode_relocatable_dialogue(bytes.fromhex(row['source_hex']),row['english'].removesuffix('{PAD}'),get_dialogue_profile('lil-opening-editorial-native-v1'))
    assert not any(d.severity=='error' for d in result.diagnostics)
    doc.update(predecessor_manuscript=str(OLD),predecessor_manuscript_sha256=sha(OLD.read_bytes()),
        native_known68_predecessor_proof='work/analysis/lil_London_known_fonts_v1886/all68_native_macros_and_complete_font_planes.json',
        only_one_paragraph_differs_from_v2='DK4_MES_B26_R0087')
    save(NEW,doc)
    print(dict(manuscript=str(NEW),new_formatted_markup=result.formatted_markup,only_changed_record=row['id']))
