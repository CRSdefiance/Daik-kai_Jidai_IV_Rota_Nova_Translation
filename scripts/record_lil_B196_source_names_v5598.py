"""Record the source-owned name fields without inventing gender or item identity."""
import struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B196_source_names_v5598')
SOURCE=Path('work/analysis/lil_B196_source_v5590/all36_clean_current_complete_context_with_twelve_choice_labels.json')
VOICE=Path('work/analysis/lil_B196_voices_v5591/current207_catalog_eight_voices_and_six_source_selectors.json')
NAMES=Path('work/analysis/lil_B196_names_v5594/twelve_original_progressive_and_catalogue_name_consumers.json')
EXPECTED={2:('リル','アーゴット'),6:('フリオ','エルネコ'),19:('カルロ','シナート'),20:('フェルナンド','ディアス'),25:('イファ','ソル'),173:('怪しい人','アラブ水夫')}
if __name__=='__main__':
    assert not ROOT.exists();source,voice,names=map(read,[SOURCE,VOICE,NAMES])
    assert voice['source_context_sha256']==names['source_context_sha256']==sha(SOURCE.read_bytes())
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    anchor=next(r for r in read('translations/ordinary_name_fidelity_manuscript_v1.json')['records'] if r['index']==164)
    assert anchor['table_field']==0x122000
    fields=[]
    for ident,expected in EXPECTED.items():
        first=anchor['table_field']+(ident-164)*32;parts=[]
        for delta in [0,4]:
            field=first+delta;pointer=struct.unpack_from('<I',clean,field)[0];at=pointer-0x02000000
            assert 0<=at<len(clean);raw=clean[at:clean.index(0,at)+1]
            parts.append(dict(pointer_field=field,source_pointer=pointer,source_storage_offset=at,terminated_hex=raw.hex(),Japanese=raw[:-1].decode('cp932')))
        assert tuple(r['Japanese'] for r in parts)==expected
        assert struct.unpack_from('<I',clean,first+8)[0]==0
        fields.append(dict(actor_ID=ident,source_fields=parts,third_field_null=True,
            current_progressive_name=names['progressive_nameplate_values'][str(ident)],current_catalogue_name=names['full_catalogue_values'][str(ident)]))
    native=names['native_twelve_consumer_cases']['rows']
    assert len(native)==12 and all(r['all_actor_models_and_unowned4MiB_exact'] for r in native)
    assert sum(bool(r['original_scratch_rings']) for r in native)==10
    assert all(not r['original_scratch_rings'] and not r['original_getter_writes'] for r in native if r['actor_ID']==173)
    voices={r['actor_ID']:r['original_voice_class'] for r in voice['fresh6_actor_names']['rows']}
    assert voices=={2:3,6:5,19:7,20:4,25:3,173:0}
    assert names['full_catalogue_values']==names['progressive_nameplate_values']=={
        '2':'Lil Argot','6':'Julio Erneco','19':'Carlo Sinat','20':'Ｆernando Dias','25':'Yifa Sol','173':'Suspicious Person'}
    ROOT.mkdir(parents=True)
    save(ROOT/'six_source_name_fields_twelve_current_consumers_and_literal_scope.json',dict(
        candidate=source['current_ROM'],candidate_sha256=source['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),
        source_name_fields=fields,current_native_voice_classes={str(k):v for k,v in voices.items()},
        current_progressive_and_full_catalogue_values=names['progressive_nameplate_values'],
        source_person173_first_field_is_gender_neutral_ayashii_hito=True,
        source_person173_secondary_field_Arab_sailor_not_used_to_invent_current_role_nationality_employment_or_gender=True,
        five_named_actors_have_ten_owned_scratch_name_paths_person173_has_two_readonly_paths=True,
        Fernando20_current_fullwidth_leading_F_recorded_without_unapproved_UI_rename_or_rendering_defect_claim=True,
        no_nameplate_glyph_or_actual_B196_gameplay_claim=True,
        source_explicit_Carlo_Admiral_address_kept_separate_from_uninvented_other_ranks_or_relationships=True,
        approved_money_unit_Charm_label_FI_expansion_and_source_item_effect_context_still_pending=True,
        source_price_ladder_not_used_to_guess_packed_A000_semantics=True,
        evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,VOICE,NAMES,Path('translations/ordinary_name_fidelity_manuscript_v1.json'),Path(__file__)]},
        new_emulator_runs=0,new_editorial_approval=0,new_review_credit=0,full_goal_complete=False))
    print('Six source first/secondary name fields,twelve native name consumers and six voices bound. Person173 remains gender-neutral;unused secondary field and Fernando fullwidth F recorded without new role/UI/rendering claims.')
