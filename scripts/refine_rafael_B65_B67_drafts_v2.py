"""Preserve Charlotte personal gratitude while keeping the first draft frozen."""
from copy import deepcopy
from pathlib import Path
from scripts.draft_rafael_B65_B67 import ROOT, DRAFTS, NOTES
from scripts.seal_source_drafts_v1 import seal
from scripts.audit_story_glyph_consistency import load, save
from dk4tool.patch.grand_race_menu_release import sha

if __name__ == '__main__':
    drafts, notes = deepcopy(DRAFTS), deepcopy(NOTES)
    drafts[67][4] = "Oh... {MACRO:FI}, you're always so kind to me. I..."
    notes[67,23] = 'Preserve Charlotte personal gratitude and trailing thought; do not turn the recipient into an unspecified collective.'
    prior = ROOT/'B65_B67_92_logical_English_drafts_v1.json'
    output = ROOT/'B65_B67_92_logical_English_drafts_v2.json'
    seal(ROOT/'source_identity_event_andterm_checkpoint_v1.json', output, drafts, notes, Path(__file__))
    data = load(output)
    data.update(previous_draft=str(prior), previous_draft_sha256=sha(prior.read_bytes()),
        whole_exchange_refinements={'DK4_MES_B67_R0023': 'Personal me, not unspecified us, receives Charlotte gratitude.'},
        earlier_English_still_unconsulted=True)
    save(output, data)
