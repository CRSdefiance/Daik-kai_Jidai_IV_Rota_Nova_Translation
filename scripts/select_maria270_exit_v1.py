"""Extend only the representative host-exit test, preserving the broad observations."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/Maria_B37_B50_clean_20261109')
def main():
    out=ROOT/'exit270_selection_v1.json';assert not out.exists()
    original=ROOT/'representative270_selection_v1.json'
    selection=load(original)
    ids=['DK4_MES_B40_R0016','DK4_MES_B40_R0019']
    assert set(ids)<=set(selection['selected_speech_ids'])
    save(out,dict(fixtures=[dict(name='maria270_exit',frames=10001,
        sequence=[dict(speech=ident) for ident in ids],
        purpose='Focused two-page-to-next-speech and source-complete host cleanup/ordinary resupply/departure QA. Longer ordinary A schedule tests the exit without replaying all63 broad utterances. No new distinct story coverage or natural branch activation.')],
        no_production_text_orengine_change=True,all_broad_observations_preserved=True,
        natural_activation=False,guide_photos=False,new_credit=0,
        evidence={str(p):digest(p) for p in [original,Path(__file__)]}))
    print('Selectedtwo existing utterances/three pages forfocused host exit;no new editorial credit.')

if __name__=='__main__':main()
