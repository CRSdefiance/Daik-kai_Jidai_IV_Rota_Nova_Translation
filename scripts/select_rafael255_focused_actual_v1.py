"""Choose whole useful exchanges anddistinct native display/control risks for two focused coldboots."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save

OUT=Path('translations/rafael255_focused_actual_selection_v1.json')

def speech(block,index):return dict(speech=f'DK4_MES_B{block}_R{index:04d}')
def menu(block,offset):return dict(menu=dict(block=block,source_command_offset=offset))
def style(block,offset):return dict(style=dict(block=block,source_command_offset=offset,expected_style=4))

if __name__=='__main__':
    assert not OUT.exists()
    sequence=[style(113,10),speech(113,29),speech(113,33),speech(113,37),speech(114,24),menu(114,296),
        speech(114,96),menu(114,534),speech(114,185),speech(118,7),speech(118,19),speech(118,23),speech(118,26),menu(118,370),
        speech(118,55),speech(118,58),speech(118,62),style(119,16),speech(119,33),speech(119,36),speech(119,39),menu(119,336),
        speech(119,66),speech(119,70)]
    controls=[];captures=[];menubases=[]
    for index,action in enumerate(sequence):
        if 'menu' not in action:continue
        base=4000+(index-1)*240;selected=1 if action['menu']['block']==119 else 0
        for delta,button in [(60,'DOWN'),(120,'DOWN'),(180,'UP')]+([] if selected==1 else [(210,'UP')]):
            controls.append(dict(start=base+delta,duration=5,buttons=[button]))
        captures.extend(base+delta for delta in [20,90,150,195,225])
        menubases.append(dict(**action['menu'],open_A_frame=base,accepted_index=selected,ordinary_accept_A_frame=base+240))
    save(OUT,dict(format='dk4-disclosed-native-dialogue-fixture-selection-v2',fixtures=[
        dict(name='Julio_names_andtown',purpose='Complete Julio granddaughter/shield exchange,complete cross misunderstanding,nearby town/church leads andvillager exchange;all eleven newly scoped public names,source uncertainty,multi-page geography andsect-leader prose. Selected native commands after ordinary New Game only.',
            speech_blocks=[101,112,109,111,117],speech_ids=[f'DK4_MES_B{b}_R{i:04d}' for b,i in [
                (116,60),(102,14),(120,36),(116,29),(120,64),(120,72),(115,52),(115,56),(115,59),(110,23)]]),
        dict(name='dynamic_styles_panels_andmenus',purpose='Complete two native eight-slot objects withordinary role1 fallback;dynamic role0 headers;repaired FE final period andfour-row bean premise;four complete three-choice menus,allcursor states andordinary acceptance. Flat QA sequence,not original branches orstats.',
            sequence=sequence,extra_inputs=controls,capture_extra=sorted(captures),planned_menu_controls=menubases)
        ],all243_speech_variants_and12_captions_already_reviewed_in_complete_source_exchanges=True,
        new_source_objects=0,original_location_natural_activation_earned_chronology_fullroute_andhardware_unvisited=True,guide_photos=False,new_credit=0))
    print('Selected complete exchanges/new public names andfour menu/dynamic/style/FE/pagination risks;two initialized coldboots,allother content remains offline-only.')
