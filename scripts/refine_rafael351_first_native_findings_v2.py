"""Preserve failed preference attempts and choose coherent clause boundaries without shortening."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from dk4tool.patch.grand_race_menu_release import sha

if __name__=='__main__':
    parent=Path('translations/rafael_B121_B140_visual_preferences_v2.json')
    out=Path('translations/rafael_B121_B140_visual_preferences_v3.json');assert not out.exists()
    doc=deepcopy(load(parent));p=doc['records']
    p['DK4_MES_B121_R0100'].update(line_phrases=['give you','Please wait a moment!'],
        ordinary_boundaries=[['you','in']],reason='Keep give you and the full Please wait a moment sentence together;you/in is a normal continuation of the gift clause,not a question tag. Reject the prior sparse I\'ve nothing opening.')
    p['DK4_MES_B123_R0171'].pop('one_page')
    p['DK4_MES_B123_R0171'].update(page_clause="I'm confident we can meet them on equal terms. Or better.",
        line_phrases=['to Africa.'],reason='The attempted four-row version stranded to before Africa. Keep the direction phrase together and turn before the complete confidence sentence;do not shorten the speech or waive its weak ending.')
    p['DK4_MES_B129_R0024'].pop('one_page')
    p['DK4_MES_B129_R0024'].update(page_clause='when {MACRO:FO} expands into Africa and the New World.',
        reason='No prose-preserving four-row solution exists under the qualified guards/phrase rules. Keep the full future expansion condition and both destination regions together on page2;preserve the original paragraph.')
    p['DK4_MES_B128_R0089'].update(line_phrases=['Touch the flagship to stop.'])
    doc.update(previous_preferences=str(parent),previous_preferences_sha256=sha(parent.read_bytes()),
        failed_one_page_attempts_preserved='work/analysis/Rafael351_automatic_plans_v3_20261105/automatic_plans.json',
        source_prose_macros_andnative_geometry_unchanged=True)
    doc['evidence'].update({str(x):sha(x.read_bytes()) for x in [parent,Path(__file__)]})
    save(out,doc);print('Preserved failed four-row attempts;three coherent page clauses and complete sail-stop instruction,with exact prose unchanged.')
