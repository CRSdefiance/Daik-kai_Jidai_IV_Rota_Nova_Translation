"""Bind clean actor name fields and actual current consumers without inferred biography."""
import struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B197_source_names_v5653')
SOURCE=Path('work/analysis/lil_B197_source_v5647/all24_clean_current_complete_context_with_three_choice_labels.json')
VOICE=Path('work/analysis/lil_B197_voices_v5648/current207_catalog_eight_voices_and_two_source_selectors.json')
NAMES=Path('work/analysis/lil_B197_names_v5652/four_original_progressive_and_catalogue_name_consumers.json')
EXPECTED={21:('イアン','ドゥーコフ'),169:('妖艶な女','インド')}
if __name__=='__main__':
    assert not ROOT.exists();source,voice,names=map(read,[SOURCE,VOICE,NAMES])
    assert voice['source_context_sha256']==names['source_context_sha256']==sha(SOURCE.read_bytes())
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin');anchor=next(r for r in read('translations/ordinary_name_fidelity_manuscript_v1.json')['records'] if r['index']==164)
    assert anchor['table_field']==0x122000;fields=[]
    for ident,expected in EXPECTED.items():
        first=anchor['table_field']+(ident-164)*32;parts=[]
        for delta in [0,4]:
            field=first+delta;pointer=struct.unpack_from('<I',clean,field)[0];at=pointer-0x02000000
            assert 0<=at<len(clean);raw=clean[at:clean.index(0,at)+1]
            parts.append(dict(pointer_field=field,source_pointer=pointer,source_storage_offset=at,terminated_hex=raw.hex(),Japanese=raw[:-1].decode('cp932')))
        assert tuple(r['Japanese'] for r in parts)==expected and struct.unpack_from('<I',clean,first+8)[0]==0
        fields.append(dict(actor_ID=ident,source_fields=parts,third_field_null=True,current_progressive_name=names['progressive_nameplate_values'][str(ident)],current_catalogue_name=names['full_catalogue_values'][str(ident)]))
    native=names['native_four_consumer_cases']['rows'];assert len(native)==4 and all(r['all_actor_models_and_unowned4MiB_exact'] for r in native)
    assert sum(bool(r['original_scratch_rings']) for r in native)==2
    assert all(not r['original_scratch_rings'] and not r['original_getter_writes'] for r in native if r['actor_ID']==169)
    voices={r['actor_ID']:r['original_voice_class'] for r in voice['fresh2_actor_names']['rows']};assert voices=={21:1,169:0}
    assert names['full_catalogue_values']==names['progressive_nameplate_values']=={'21':'Ian Dukov','169':'Alluring Woman'}
    ROOT.mkdir(parents=True);save(ROOT/'two_source_name_fields_four_current_consumers_and_literal_scope.json',dict(candidate=source['current_ROM'],candidate_sha256=source['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),
        source_name_fields=fields,current_native_voice_classes={str(k):v for k,v in voices.items()},current_progressive_and_full_catalogue_values=names['progressive_nameplate_values'],
        source169_primary_field_explicitly_says_woman_and_supports_female_pronoun=True,
        source169_secondary_India_field_not_consumed_by_current_name_and_not_promoted_to_citizenship_biography_or_supernatural_identity=True,
        Ian21_explicit_FE_name_is_not_player_captain_Lil_and_contains_no_FI_macro=True,
        source_handsome_man_address_and_wish_for_a_man_like_Ian_do_not_establish_an_existing_romance_or_new_relationship=True,
        source_Admiral_address_explicit_only_when_spoken_and_no_other_rank_kinship_or_employment_invented=True,
        celestial_maiden_identity_remains_character_question_then_self_dismissal_not_narrator_confirmation=True,
        Indian_classic_book_title_author_religious_canon_and_item_identity_not_invented=True,
        two_named_actor_scratch_paths_and_two_readonly_role_paths_currently_guarded=True,no_actual_B197_nameplate_or_new_UI_glyph_credit=True,
        evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,VOICE,NAMES,Path('translations/ordinary_name_fidelity_manuscript_v1.json'),Path(__file__)]},
        new_emulator_runs=0,new_editorial_approval=0,new_review_credit=0,full_goal_complete=False))
    print('Ian Dukov/Alluring Woman source names and voices1/0 bound.Four native consumers pass.Source女 supports she;unused India field does not certify biography or celestial identity.No credit.')
