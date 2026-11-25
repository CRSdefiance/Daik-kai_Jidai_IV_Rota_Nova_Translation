"""Reject an awkward address-only row and document the source-bound realization beat."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

if __name__=='__main__':
    parent=Path('translations/rafael_B121_B140_visual_preferences_v4.json')
    out=Path('translations/rafael_B121_B140_visual_preferences_v5.json');assert not out.exists()
    doc=deepcopy(load(parent));del doc['records']['DK4_MES_B135_R0005']
    doc['records']['DK4_MES_B134_R0019']['reason']='Keep the speaker\'s alarmed Of all the people idiom together rather than splitting Of all/the people;no new speaker identity is supplied by a formatting note.'
    row=doc['records']['DK4_MES_B136_R0147']
    row['documented_dramatic_opening_reason']='The separate Oh... reaction localizes source そうか before Rafael acknowledges hurting Clau and decides to apologize. Retain this short realization beat because it expresses the emotional turn,then keep the auxiliary sequence and apology complete. This is an individually reviewed exception,not permission to retain routine short opening lines.'
    doc.update(previous_preferences=str(parent),previous_preferences_sha256=sha(parent.read_bytes()),
        rejected_address_only_row=dict(id='DK4_MES_B135_R0005',reason='Keeping all sorts of taverns together created an isolated Admiral. middle row. Retain the original flowing four-row paragraph;the normal continuation all sorts/of taverns is preferable to that worse layout.'),
        ten_visual_refinements_accepted_for_fresh_native_testing=True)
    doc['evidence'].update({str(p):sha(p.read_bytes()) for p in [parent,Path(__file__)]})
    save(out,doc);print('Retained the better original tavern paragraph;documented one source-bound realization beat. Ten changed layouts need fresh native review.')
