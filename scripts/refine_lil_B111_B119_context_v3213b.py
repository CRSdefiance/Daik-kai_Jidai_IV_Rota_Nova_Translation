"""Keep the mixed-region company macro as an explicit unresolved source binding."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B111_B119_clean_context_v3213b')
OLD=Path('work/analysis/lil_B111_B119_clean_context_v3213/all182_complete_clean_exchange_context_notes.json')
if __name__=='__main__':
    assert not ROOT.exists()
    doc=deepcopy(read(OLD));b=next(b for b in doc['blocks'] if b['block']==115)
    old="Preserve sourceFOmacroforeachregion'sactualspeakeractor;do notassumeLil'scompany isMaria's semanticcompany because thehistoricalLondon modelhasLilcaptain."
    new="Preserve sourceFO asaruntime macro. Theactualcaptain/route/providerbinding,notportraitidentityalone,determinesitsexpansion. Do notforceMaria'scompany orLil'scompany beforetheoriginalentry andmacrosemantics areproved;thephysicalsourcewordsandMaria03selectoraretheobservations,whileintendedroute/eligibilityremainunclassified."
    assert b['context_notes'].count(old)==1
    b['context_notes']=b['context_notes'].replace(old,new)
    doc.update(previous_context_notes=str(OLD),previous_context_notes_sha256=sha(OLD.read_bytes()),
        macro_company_identity_not_inferred_from_speaker_portrait=True,
        producer_sha256=sha(Path(__file__).read_bytes()))
    ROOT.mkdir(parents=True);save(ROOT/'all182_complete_clean_exchange_context_notes.json',doc)
    print('Clean-context successor keepsB115FOcaptain/route semantics explicitlyunbound;no proposedEnglishorcredit.')
