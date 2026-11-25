"""Select source-ordered native display cases and complete small town exchanges,without natural-event claims."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/Maria_B58_B70_clean_20261109')

def main():
    out=ROOT/'display_selection_v1.json';assert not out.exists()
    rebuiltpath=ROOT/'reconstruction_v2/reconstruction.json';storedpath=ROOT/'stored_v1/stored_native_verification.json'
    rebuilt,stored=map(load,[rebuiltpath,storedpath]);doc=load(rebuilt['manuscript'])
    assert stored['reconstruction_sha256']==digest(rebuiltpath) and len(stored['records'])==299
    bodies=[r for r in doc['records'] if r['kind']!='typed-choice-label']
    bykey={(r['block'],r['source_record_index']):r for r in bodies}
    def records(block,indices):return [dict(speech=bykey[(block,i)]['id']) for i in indices]
    def between(block,low,high):return records(block,[r['source_record_index'] for r in bodies if r['block']==block and low<=r['source_record_index']<=high])
    def whole(block):return [dict(speech=r['id']) for r in bodies if r['block']==block]
    def menu(block):
        row=next(r for r in doc['records'] if r['kind']=='typed-choice-label' and r['block']==block)
        return dict(menu=dict(block=block,source_command_offset=row['source_command_offset']))
    story=between(58,81,214)+records(59,[44,49,53,56,60])+records(61,[23,101,105,109,112])+between(70,4,37)
    town=(records(60,[39,43])+[menu(60)]+records(60,[73,76,79])+
        records(64,[4,8,12])+[menu(64)]+records(64,[26,30,33,37,41,45,49,53,57,60,64,68,71,74,77,82,85])+
        whole(65)+whole(66))
    specs=[]
    for name,sequence,purpose in [
        ('Maria303_rescue_glyphs',story,'Representative complete rescue segment with labeled FE boy voices and fear comparisons; corrected I/F introductions; both reclaimed one-page explanations and named/FE transitions. Separate source segments share the disclosed Hangzhou QA host, not original locations or earned chronology.'),
        ('Maria303_town_menus',town,'Both typed menus/default selection0 and normal A return; all formerly Japanese sailor speeches in the belief branch; full tomato and banana/unknown-seed exchanges, including the corrected meal payer. Original stat/item/story effects are not simulated; disbelief and other menu results remain offline-only.')]:
        ids=[a['speech'] for a in sequence if 'speech' in a];assert len(ids)==len(set(ids))
        menus=sum('menu' in a for a in sequence)
        specs.append(dict(name=name,sequence=sequence,purpose=purpose,selection_source_utterances=len(ids),
            selection_expected_pages=len(ids),frames=4001+(len(ids)+menus)*240+6000,capture_extra=[],extra_inputs=[]))
    selected={a['speech'] for s in specs for a in s['sequence'] if 'speech' in a}
    assert sum('menu' in a for s in specs for a in s['sequence'])==2
    assert {'DK4_MES_B59_R0056','DK4_MES_B61_R0023','DK4_MES_B61_R0105','DK4_MES_B70_R0034','DK4_MES_B66_R0066','DK4_MES_B66_R0070'}<=selected
    assert len(load(rebuilt['native'])['records'])==299
    save(out,dict(fixtures=specs,selected_speech_ids=sorted(selected),
        unvisited_body_ids=sorted({r['id'] for r in bodies}-selected),
        expected_menu_observation='default selection0 and normal A return;other selection/cancel/conditional outcomes offline-only',
        all_source_speeches_are_one_page=True,original_static_controls_copied_complete=True,
        source_conditions_outcomes_stat_item_effects_not_simulated=True,natural_activation=False,earned_chronology=False,
        actual_gameplay_pending=True,new_credit=0,guide_photos=False,
        evidence={str(p):digest(p) for p in [rebuiltpath,storedpath,Path(__file__)]}))
    print([(s['name'],s['selection_source_utterances'],s['frames']) for s in specs])

if __name__=='__main__':main()
