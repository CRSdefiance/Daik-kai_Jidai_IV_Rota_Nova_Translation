"""Drop obsolete row-count notes only after the current full QA no longer emits that warning."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue import lil_B168_layout_v3 as codec
from dk4tool.dialogue.lil_B168_profile import profile_for
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B168_QA_notes_v4184b')
INPUT=Path('translations/lil_B168_editorial_manuscript_v5.json')
OUTPUT=Path('translations/lil_B168_editorial_manuscript_v6.json')
if __name__=='__main__':
    assert not ROOT.exists() and not OUTPUT.exists();doc=deepcopy(read(INPUT));im=NdsImage.open(doc['current_ROM']);arm=im.read_file('/__arm9__.bin');b=IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[168];removed=[];active=[]
    for r in doc['records']:
        p=profile_for(arm,b,'FE-paper' if r['kind']=='system-FE' else 'progressive');result=codec.encode_relocatable_dialogue(bytes.fromhex(r['source_hex']),r['english'],p)
        assert result.encoded.hex()==r['compiled_hex'];warn=[d.code for d in result.diagnostics if d.severity=='warning']
        if r.get('qa_waivers')==['line-break-count'] and 'line-break-count' not in warn:
            removed.append(dict(id=r['id'],previous_reason=r['qa_waiver_reason']));r.pop('qa_waivers');r.pop('qa_waiver_reason')
        if r.get('qa_waivers'):assert r['qa_waivers']==['line-break-count'] and 'line-break-count' in warn;active.append(r['id'])
        q=codec.audit_relocatable_dialogue_record(bytes.fromhex(r['source_hex']),r['english'],p)
        assert not [i for i in q['issues'] if i['severity'] in ['warning','error'] and not(i['severity']=='warning' and i['code']=='line-break-count' and r.get('qa_waiver_reason'))]
    assert len(removed)==1 and len(active)==20
    doc.update(previous_manuscript=str(INPUT),previous_manuscript_sha256=sha(INPUT.read_bytes()))
    ROOT.mkdir(parents=True);save(OUTPUT,doc);save(ROOT/'current_only_narrow_row_count_notes.json',dict(input=str(INPUT),input_sha256=sha(INPUT.read_bytes()),output=str(OUTPUT),output_sha256=sha(OUTPUT.read_bytes()),removed_obsolete_notes=removed,active_current_row_count_note_IDs=active,no_words_compiled_bytes_metrics_guards_or_other_waivers_changed=True,no_credit_ROM_registry_change=True))
    print('Current QA:20 active narrow row-count notes;one obsolete note removed;all words and bytes unchanged.')
