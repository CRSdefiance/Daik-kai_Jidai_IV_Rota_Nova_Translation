"""Match instructional terminology to the current duty selector andmenu labels."""
import struct
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.registered_editorial_runtime import RegisteredRuntime
from scripts.bind_hodram_B191_B210_identities import cstring
from dk4tool.patch.crew_role_labels import FIELD,ORIGINAL,ENGLISH,JAPANESE,LABELS
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

ROOT=Path('work/analysis/Rafael_early_tutorial_B42_B43_clean_20261104')
RELEASE=Path('work/analysis/Hodram_B171_B190_release_verified_20261104/registered_release_verification.json')

if __name__=='__main__':
    output=ROOT/'native_identity_and_UI_terms_v1.json';assert not output.exists()
    ctx=RegisteredRuntime(RELEASE,RELEASE.with_name('own_registered_startup_verification.json'))
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    canonical=NdsImage.open('out/raphael_natural_v2_accepted_base.nds').read_file('/__arm9__.bin')
    names_path=Path('work/analysis/Rafael_early_tutorial_B42_B43_names_20261104/names.json');names=load(names_path)
    assert names['runtime']==ctx.receipt() and names['actors']==[0,4,5,6]
    assert len(names['clean_names']['rows'])==len(names['current_names']['rows'])==8
    assert struct.unpack_from('<I',ctx.arm,FIELD)[0]==ENGLISH
    assert struct.unpack_from('<I',canonical,FIELD)[0] in [ORIGINAL,ENGLISH]
    assert ctx.arm[0x86314:FIELD]==canonical[0x86314:FIELD]
    roles=[]
    for index in [0,1,4,5,6,7]:
        source_field=ORIGINAL-0x02000000+index*4
        pointer=struct.unpack_from('<I',clean,source_field)[0]
        raw=cstring(clean,pointer);assert raw.decode('cp932')==JAPANESE[index]
        assert ctx.arm[source_field:source_field+4]==clean[source_field:source_field+4]
        assert cstring(ctx.arm,pointer)==raw
        current_pointer=struct.unpack_from('<I',ctx.raw,ENGLISH-0x02000000+4*index)[0]
        value=cstring(ctx.raw,current_pointer)
        expected=(LABELS[index]+(' ' if len(LABELS[index])%2 else '')).encode('ascii')
        assert value==expected
        roles.append(dict(index=index,Japanese=JAPANESE[index],English=LABELS[index],source_pointer=pointer,
            source_hex=raw.hex(),current_pointer=current_pointer,current_hex=value.hex(),
            original_selector_code_exact_to_accepted_canonical=True))
    radial_path=Path('translations/common_radial_obj_labels_v3.json');radial=load(radial_path)
    button=next(r for r in radial['records'] if r['id']=='DK4_COMMON_OBJ_DECK_VIEW');assert button['text']=='Deck View'
    headings_path=Path('translations/common_submenus_arm9_v1.json');headings=[]
    for r in load(headings_path)['records']:
        if r['id'] not in ['DK4_DECK_HEADING_A','DK4_DECK_HEADING_B','DK4_DECK_HEADING_C']:continue
        at=r['offset'];text=ctx.arm[at:ctx.arm.index(0,at)].decode('ascii');assert text=='Deck'
        headings.append(dict(id=r['id'],offset=at,current_text=text))
    assert len(headings)==3
    deck_path=Path('translations/deck_explanations_manuscript_v1.json')
    tooltip=next(r for r in load(deck_path)['records'] if r['id']=='DECK_EXPLANATION_ADJUTANT')
    assert tooltip['japanese'].startswith('副官') and 'adjutant' in tooltip['english']
    save(output,dict(runtime=ctx.receipt(),source_actor_bindings=str(names_path),source_actor_bindings_sha256=sha(names_path.read_bytes()),
        actors=[0,4,5,6],ordinary_name_consumers=8,names_andvoice_getters_checked=True,UI_duty_terms=roles,
        deck_menu_button=button,deck_screen_headings=headings,
        source_UI_term_decisions=dict(航海士='navigator',副官='First Mate',甲板画面='Deck View when naming the menu choice',自動移動='automatic movement; bind the actual destination-control label before using it as a button name'),
        priority_followup_findings=[dict(id='early-tutorial-FirstMate-adjutant-consistency',source_Japanese='副官',
            current_duty_selector='First Mate',existing_tooltip_manuscript='An adjutant lets you send negotiation documents from the guild.',
            reference=str(deck_path),record_id=tooltip['id'],finding='Instructional prose andthe visible duty label use different terms. Align new tutorial prose to First Mate;review the existing tooltip in the shared tutorial priority.',
            revision_not_applied=True)],
        source_selector00_complete_preamble_reuse_andRafael_macro_layout_checks_still_pending=True,
        intrinsic_name_getters_not_actual_Rafael_gameplay_orwhole_preamble_proof=True,
        declared_Hodram_registered_snapshot_used_for_ordinary_identity_andUI_metadata_only=True,
        radial_button_reference_is_registered_asset_text_not_new_graphics_review=True,
        no_current_story_English_extracted=True,no_new_ROM_orcompletion_credit=True,new_credit=0,guide_photos=False,
        evidence={str(p):sha(p.read_bytes()) for p in [names_path,radial_path,headings_path,deck_path,Path('dk4tool/patch/crew_role_labels.py'),Path('work/analysis/crew_roles_v326/native_proof.json'),Path(__file__)]}))
    print('Bound Rafael/Janus/Claudio/Julio,exact duty labels andDeck View menu wording. Queued one First Mate/adjutant consistency finding.')
