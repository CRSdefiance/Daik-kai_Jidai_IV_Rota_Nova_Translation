"""Keep the source pirate organization and enemy reference unexpanded."""
from copy import deepcopy
from pathlib import Path
from scripts.draft_rafael_B71_B75 import ROOT, DRAFTS, NOTES
from scripts.seal_source_drafts_v1 import seal
from scripts.audit_story_glyph_consistency import load, save
from dk4tool.patch.grand_race_menu_release import sha

if __name__ == '__main__':
    drafts, notes = deepcopy(DRAFTS), deepcopy(NOTES)
    drafts[71][2] = 'Oh! So the Kurushima pirates are gone!'
    drafts[75][18] = 'Listen carefully. From now on, you Portuguese will be under the protection of our Invincible Armada.'
    drafts[75][19] = 'You can trade in peace only because we fight the enemy day and night. Remember that.'
    notes[71,13] = 'Keep the fallen Kurushima organization in view; do not turn its defeat into an assertion that a named individual is dead.'
    notes[75,98] = 'The imperial protection boast is Simon claim, not a narrator guarantee; preserve the explicitly named Invincible Armada.'
    notes[75,102] = 'Keep the unspecified enemy as in source; do not assert that the opponents are specifically Portugal own enemies.'
    prior = ROOT/'B71_B75_116_logical_English_drafts_v1.json'
    output = ROOT/'B71_B75_116_logical_English_drafts_v2.json'
    seal(ROOT/'source_identity_event_andterm_checkpoint_v1.json', output, drafts, notes, Path(__file__))
    data = load(output)
    data.update(previous_draft=str(prior), previous_draft_sha256=sha(prior.read_bytes()),
        whole_exchange_refinements={
            'DK4_MES_B71_R0013': 'Organization, without a death assertion.',
            'DK4_MES_B75_R0098': 'Natural phrasing of the explicit protection boast.',
            'DK4_MES_B75_R0102': 'Unspecified enemy, without a new shared-enemy assertion.'},
        earlier_English_still_unconsulted=True)
    save(output, data)
