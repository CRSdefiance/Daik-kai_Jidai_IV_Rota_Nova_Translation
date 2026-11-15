"""Bind B173's crown,tomb and native names without upgrading reported knowledge."""
import struct
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B173_terms_v4418')
SOURCE=Path('work/analysis/lil_B173_source_v4411/all11_clean_current_complete_context.json')
NAMES=Path('work/analysis/lil_B173_names_v4416/four_original_name_consumers_and_owned_scratch_paths.json')
CONTROL=Path('work/analysis/lil_B173_controls_v4417/two_resources_one_predicate_four_spans_two_A000s_and_single_end.json')
EARLIER=Path('translations/lil_recruits_julian_contextual_final_review_v1.json')
ITEM=Path('translations/all_item_names_arm9_v1.json')
SITE=Path('translations/historic_site_names_v2.json')
JULIAN=Path('work/analysis/lil_B172_names_v4369/six_original_name_consumers_and_owned_scratch_paths.json')

def pointer_strings(old,current,field):
    strings=[]
    for binary in [old,current]:
        pointer=struct.unpack_from('<I',binary,field)[0];offset=pointer-0x02000000
        assert 0<=offset<len(binary)
        value=binary[offset:binary.index(b'\0',offset)]
        strings.append(dict(pointer=pointer,file_offset=offset,bytes=len(value),hex=value.hex(),text=value.decode('cp932')))
    return strings

if __name__=='__main__':
    assert not ROOT.exists()
    source,names,control,earlier,julian=map(read,[SOURCE,NAMES,CONTROL,EARLIER,JULIAN])
    assert names['source_context_sha256']==control['source_context_sha256']==sha(SOURCE.read_bytes())
    current,clean=NdsImage.open(source['current_ROM']),NdsImage.open('work/clean.nds')
    now,jp=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks for im in [current,clean]]
    old_arm,arm=clean.read_file('/__arm9__.bin'),current.read_file('/__arm9__.bin')
    bindings=[]
    for index in [40,47,95,113]:
        row=next(r for r in earlier['records'] if r['block']==78 and r['source_record_index']==index)
        sr,ref=row['source_reference'],row['integrated_reference'];raw,value=bytes.fromhex(row['source_hex']),bytes.fromhex(row['integrated_hex'])
        assert '新羅の金冠' in row['source_Japanese'] and 'Silla Gold Crown' in row['english'] and all(row['review'].values())
        assert jp[78][sr['offset']:sr['offset']+len(raw)]==raw and jp[78][sr['offset']+len(raw)]==0
        assert now[78][ref['offset']:ref['offset']+len(value)]==value and now[78][ref['offset']+len(value)]==0
        bindings.append(dict(id=row['id'],clean_reference=sr,clean_hex=raw.hex(),current_reference=ref,current_hex=value.hex(),
            reviewed_English=row['english'],final_review=str(EARLIER),final_review_sha256=sha(EARLIER.read_bytes())))
    item=next(r for r in read(ITEM)['records'] if r['id']=='DK4_ITEM_POINTER_137');at=item['offset']
    assert old_arm[at:at+4].hex()==item['source_hex'].lower() and arm[at:at+4].hex()==item['replacement_hex'].lower()
    itemstrings=pointer_strings(old_arm,arm,at)
    assert [s['text'] for s in itemstrings]==['新羅の金冠','Silla Gold Crown'] and item['english']=='Silla Gold Crown'
    site=next(r for r in read(SITE)['records'] if r['site_id']==17)
    sitestrings=pointer_strings(old_arm,arm,site['pointer_field'])
    assert site['japanese']=='武寧王陵' and site['english']=='Tomb of King Muryeong'
    assert [s['text'] for s in sitestrings]==[site['japanese'],site['english']]
    assert sitestrings[0]['file_offset']==site['source_offset'] and sitestrings[0]['hex']==site['source_hex']
    previous=NdsImage.open(julian['candidate'])
    for path in ['/__arm9__.bin','/COMMON/MESFILE.DK4','/data/EV2.DK4','/GRP/KANJI.FNT']:
        assert current.read_file(path)==previous.read_file(path)
    assert julian['approved_prose_names']['26']=='Julian' and julian['full_catalogue_values']['26']=='Julian Lopes'
    assert names['approved_prose_names']=={'2':'Lil','202':'Reika'}
    assert names['progressive_nameplate_values']==names['full_catalogue_values']=={'2':'Lil Argot','202':'Reika'}
    by={r['source_record_index']:r for r in source['records']}
    for index,phrases in {6:['新羅の金冠','知ってる人'],13:['聞いてみよう','聞いたことない'],17:['聞いたことはある','どうかした'],
        20:['探してる','キレイなんですって'],24:['キレイらしい','さっきも同じこと'],28:['ひょっとして','ユリアン'],
        32:['よく覚えてない','口がうまい男','武寧王陵','行ったみたい'],36:['武寧王陵'],
        40:['この近く','遺跡','そこにあるって話','聞いたこと'],44:['ユリアン','もう先に','負けない']}.items():
        assert all(p in by[index]['source_Japanese'] for p in phrases),index
    ROOT.mkdir(parents=True)
    save(ROOT/'current_crown_tomb_Reika_and_uncertain_Julian_lead_reconciliation.json',dict(
        candidate=source['current_ROM'],candidate_sha256=source['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),
        approved_B173_prose_names={'2':'Lil','202':'Reika'},native_full_names_preserved={'2':'Lil Argot','202':'Reika'},
        spoken_Julian_name_binding=dict(previous_native_name_proof=str(JULIAN),proof_sha256=sha(JULIAN.read_bytes()),
            approved_spoken_name='Julian',full_catalogue_name='Julian Lopes',ARM9_COMMON_EV2_font_exact_to_current=True,surname_not_added_to_source_given_name=True),
        exact_completed_B78_crown_bindings=bindings,chosen_crown_title='Silla Gold Crown',chosen_site_title='Tomb of King Muryeong',
        exact_global_item_pointer_binding=dict(batch=str(ITEM),batch_sha256=sha(ITEM.read_bytes()),id=item['id'],pointer_field_offset=at,
            source_pointer_hex=item['source_hex'],current_pointer_hex=item['replacement_hex'],source_string=itemstrings[0],current_string=itemstrings[1]),
        exact_global_historic_site_pointer_binding=dict(batch=str(SITE),batch_sha256=sha(SITE.read_bytes()),id=site['id'],site_id=17,
            pointer_field_offset=site['pointer_field'],source_string=sitestrings[0],current_string=sitestrings[1],
            source_and_current_ARM9_hashes=[sha(old_arm),sha(arm)],exact_current_bytes_bind_title_not_historical_pending_formatting_flags=True),
        direct_pointer_strings_not_new_item_or_historic_site_UI_or_full_SourceItems_catalogue_review=True,
        Reika_CA202_original_readonly_name_paths_not_literal_text_or_invented_relationship=True,
        guarded_knowledge_recent_other_question_beauty_and_crown_location_remain_secondhand=True,
        woman_does_not_remember_name_smooth_talking_man_only_tentatively_connected_to_Julian=True,
        man_apparently_went_to_named_tomb_not_confirmed_present_location=True,
        source_calls_site_a_nearby_ruin_no_distance_coordinate_or_geographic_exposition_added=True,
        Lil_conclusion_and_competitive_vow_not_verified_narration_or_hostility=True,
        B172_qualified_date_reply_and_B78_later_acquisition_transfer_not_imported=True,
        no_source_FI_FA_FO_macros=True,SourceItems_LocalProduct_graphics_and_older_record_reaudit_stay_open=True,
        evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,NAMES,CONTROL,EARLIER,ITEM,SITE,JULIAN,Path(__file__)]},
        new_emulator_runs=0,source_prose_or_completion_credit_added=0,no_ROM_registry_ledger_change=True,full_goal_complete=False))
    print('Bound Reika/Lil,spoken Julian,Silla Gold Crown and Tomb of King Muryeong to exact current strings. Uncertain identity/location and Lil inference preserved. No credit.')
