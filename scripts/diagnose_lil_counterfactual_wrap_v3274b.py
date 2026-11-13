"""Compare equivalent complete counterfactuals without relaxing display QA."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.dialogue.lil_B122_B127_profile_v2 import profile_for
from dk4tool.dialogue.lil_B122_B127_layout_v1 import audit_relocatable_dialogue_record
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
if __name__=='__main__':
    root=Path('work/analysis/lil_counterfactual_wrap_v3274b');assert not root.exists()
    doc=read('translations/lil_B122_B127_editorial_manuscript_v1.json');row=next(r for r in doc['records'] if r['id']=='DK4_MES_B122_R0128')
    im=NdsImage.open(doc['current_ROM']);p=profile_for(im.read_file('/__arm9__.bin'),IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[122])
    bodies=[
        "His ties to the English Crown... Things wouldn't have ended this way without them. I think he wanted to get along with us...",
        "Those ties to the English Crown... Things wouldn't have ended this way without them... I think he wanted to get along with us...",
        "This wouldn't have happened if he hadn't been tied to the English Crown... I think he wanted to get along with us...",
        "But for his ties to the English Crown, none of this would've happened... I think he wanted to get along with us...",
        "Without his ties to the English Crown, things would've been different... I think he wanted to get along with us..."]
    cases=[]
    for body in bodies:
        qa=audit_relocatable_dialogue_record(bytes.fromhex(row['source_hex']),'{SPEAKER:09}'+body,p)
        bad=[i for i in qa['issues'] if i['severity'] in ['warning','error'] and i['code']!='line-break-count']
        cases.append(dict(body=body,qa=qa,unresolved=bad));print(body,qa['visible_lines'],bad,flush=True)
    root.mkdir(parents=True);save(root/'equivalent_counterfactual_layout_comparisons.json',dict(cases=cases,no_prose_or_ROM_change=True,producer_sha256=sha(Path(__file__).read_bytes())))
