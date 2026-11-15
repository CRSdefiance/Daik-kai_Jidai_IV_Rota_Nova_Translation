"""Choose a representative initialized sequence from all direct actors and display findings."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.plan_rafael_B0_B34_v1 import FORMATTING, ROOT
from scripts.source_locked_derivation_v5118 import checked_text
from scripts import prepare_rafael_B221_B240_actual_v1 as builder

SELECTION=ROOT/'focused_selection_v1.json'
ROLES=ROOT/'direct_selectors_v1.json'


def prepare():
    assert not SELECTION.exists() and not ROLES.exists()
    doc=load(FORMATTING); rows=doc['records']; byid={r['id']:r for r in rows}
    actors=sorted({r['source_selector'] for r in rows})
    assert len(actors)==39 and max(actors)<207
    ids={next(r['id'] for r in rows if r['source_selector']==actor) for actor in actors}
    prefs=load(ROOT/'ordinary_visual_preferences_v7.json')
    ids.update(prefs['records'])
    # Include the entire poem exchange and Aziza's final autobiographical arc.
    ids.update(r['id'] for r in rows if r['block']==25 or
        (r['block']==26 and r['source_reference']['record_index']>=228))
    ids.update(f'DK4_MES_B{block}_R{index:04d}' for block,index in
        [(0,48),(0,55),(5,52),(9,13),(9,40),(16,6),(20,78),(21,5),(26,33),(26,96),(26,124)])
    assert ids<=byid.keys()
    selected=[r for r in rows if r['id'] in ids]
    assert {r['source_selector'] for r in selected}==set(actors)
    save(ROLES,dict(runtime=doc['runtime'],source_records=[],native_roles=dict(rows=[]),
        all_source_selectors_direct_ordinary_actor_IDs=True,no_dynamic_roles_in_this_batch=True,
        no_roster_or_voice_mutation=True,new_credit=0))
    save(SELECTION,dict(format='dk4-disclosed-native-dialogue-fixture-selection-v2',
        fixtures=[dict(name='rafael_residual_battles_and_recruitment',
            sequence=[dict(speech=r['id']) for r in selected],
            purpose='Observe all 39 unchanged progressive headers, source-glyph repairs, wrap refinements, the complete poem and page turn, and Aziza\'s final keepsake/recruitment exchange.')],
        chosen_fixture_path_is_a_display_sequence_not_original_branch_routing=True,
        original_conditional_activation_andfull_catalogue_UI_unvisited=True,
        owned_middle_fields_have_separate_native_proof_andcandidate_startup_pending=True,
        guide_photos=False,new_credit=0,evidence={str(p):digest(p) for p in (FORMATTING,Path(__file__))}))
    print('Selected',len(selected),'utterances across all 39 actors; no menus or personality-role mutations.')


source=checked_text(builder.source,{
    "stored['style_records']":"stored.get('style_records',[])",
})

if __name__=='__main__':
    import sys
    if sys.argv[1:]==['--prepare']:prepare()
    else:exec(compile(source,__file__+'::same-source-command-initialized-display-sequence','exec'),globals())
