"""Preserve v1 and revise three overlong paragraphs without losing source facts."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

OLD=Path('translations/lil_london_editorial_manuscript_v1.json')
NEW=Path('translations/lil_london_editorial_manuscript_v2.json')
CHANGES={
    'DK4_MES_B26_R0087':("They say he's a towering giant with three eyes and a mouth from ear to ear, and he drinks human blood from a goblet!",
        'Retain the rumor,giant,three eyes,ear-to-ear mouth,human blood andgoblet inone natural sentence;removing redundant wording resolves the five-row paragraph without cutting facts.'),
    'DK4_MES_B26_R0461':("Did you hear? Pedro Valdes is now commander in chief of Spain's navy. He's one of the strongest commanders they've ever had.",
        'Keep the inquiry,newappointment,full name,naval command andhistorical comparison incompact natural speech;the native four-row limit isseparate fromold fixed allocation.'),
    'DK4_MES_B26_R0566':("I'll follow English policy to the New World. You'll follow Dutch policy south, through Africa to India and Asia.",
        'Retain both national policies andevery named destination,including India;remove redundant follow/expanding wording rather than erase geography.'),
}

if __name__=='__main__':
    assert not NEW.exists()
    doc=deepcopy(read(OLD))
    doc.update(predecessor_manuscript=str(OLD),predecessor_manuscript_sha256=sha(OLD.read_bytes()),
        body_only_research='work/analysis/lil_London_body_probe_v1881b/body_only_prose_layout_research.json')
    changed=[]
    for r in doc['records']:
        if r['id'] not in CHANGES:continue
        english,note=CHANGES[r['id']]
        r['previous_editorial_English']=r['english']
        r['english']=f"{{SPEAKER:{r['source_presentation_prefix_hex'].upper()}}}"+english+'{PAD}'
        r['localization_note']=note
        r['formatting_refinement_reason']='Resolve observed five-row body-only research overflow withallsource facts preserved;fullscene controls/fonts/FE/actual gates remainpending.'
        changed.append(r['id'])
    assert set(changed)==set(CHANGES)
    save(NEW,doc)
    print(dict(successor=str(NEW),naturally_refined_paragraphs=changed,full_native_display_review_pending=True))
