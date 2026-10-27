"""Source/context and natural American English review; native gates remain open."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.powder_fire_layout_v1304 import IDS, PROFILE, paragraph
from scripts.verify_village_wrap_v608 import read,save

OUT = Path('translations/powder_fire_editorial_manuscript_v1.json')
CONTEXT = Path('work/analysis/powder_fire_context_v1303c/source_and_actual_binding.json')
REVIEW = {
    2052:("The powder in the gun battery has ignited! There's a fire!",
          'Reports that powder in the armed gun battery ignited and caused a fire.',
          'Replace the stiff gun-platform wording with the established gun battery concept;preserve both ignition and the resulting fire.'),
    2053:("The powder in the gun battery has caught fire!",
          'A briefer polite report that powder in the gun battery ignited and a fire has started.',
          'Caught fire naturally carries both ignition and fire onset without the redundant English fragment A fire.'),
    2054:("The gunpowder's caught fire in the battery!",
          'A rough casual alarm that the gun battery powder ignited and is now on fire.',
          'Use a spoken contraction and urgent complete sentence;do not add an explosion or destroyed guns.'),
    2055:("The powder in the gun battery is on fire!",
          'An older speaker exclaims that gun battery powder has ignited and there is a fire.',
          'Keep a natural urgent report without manufacturing archaic English from the Japanese ending.'),
    2056:("Fire! The gunpowder in the battery is burning!",
          'A youthful panicked cry that powder in the gun battery caught fire.',
          'Front-load the alarm in idiomatic English while retaining the gunpowder and battery location.'),
    2057:("The powder in the gun battery has ignited! A fire has broken out!",
          'A formal emphatic report that gun battery powder ignited and caused a fire.',
          'Use the conventional phrase a fire has broken out for the formal report;do not invent magazine storage,casualties or sinking.')
}


def main():
    assert not OUT.exists()
    context = read(CONTEXT)
    assert context['original_table'] == 0x02117980
    assert context['raw8_voice_table'] == [2052,2053,0xFFFFFFFF,0xFFFFFFFF,2054,2055,2056,2057]
    assert context['all8_effective_voice_selections'] == [2052,2053,2052,2052,2054,2055,2056,2057]
    assert context['actual_old_wording_holds'][0]['source_selected_message_ID'] == 2053
    assert context['actual_old_wording_holds'][0]['original_direct_parent'] == 0x02053F40
    rom_path = Path('out/all_routes_combined_v1266_candidate.nds')
    rom = NdsImage.open(rom_path)
    arm,common = rom.read_file('/__arm9__.bin'),rom.read_file('/COMMON/MESFILE.DK4')
    canonical = NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    base = common_message_entries(canonical.read_file('/COMMON/MESFILE.DK4'),canonical.read_file('/__arm9__.bin'),clean=False)
    records = []
    for old in context['records']:
        row = deepcopy(old)
        number = row['message_id']
        english,meaning,note = REVIEW[number]
        row.update(id=f'COMMON_MESSAGE_{number}',source_family='gun_battery_powder_fire',
            consumer='original-direct-portrait-speech-after-native-selection-and-printf-macro-expansion',
            speaker='Original actor returned by55DC4 for the affected ship gun position;voice alternative from17980',
            context='Original755D8 unforced powder-fire check may set mobile flag0E bit0. After5652C succeeds,75600-75610 obtain the affected gun-position actor through55DC4 and call53F0C with table02117980. Actual Gerhard16/voice1 selects2053. This is a ship gun-battery fire,not a shore fort,guaranteed explosion or sinking.',
            source_meaning=meaning,english=english,localization_note=note,
            editorial_decision='revise',canonical_source_hex=base[number].text.hex(),
            native_argument_count=0,native_argument_kind='none',source_native_macros=[],
            original_native_entry=0x02053F0C,original_native_parent=0x02053F40,source_table=0x02117980,
            review={'source':True,'context':True,'localization':True,'naturalness':True,'formatting':False},
            status='source-context-prose-reviewed;native-formatting-release-and-revised-gameplay-pending')
        row.pop('already_source_reviewed')
        row.pop('already_complete')
        payload = paragraph(row)
        row['unwrapped_paragraph_hex'] = payload.hex()
        row['source_current_text_is_old_wording_not_proposed_release'] = True
        records.append(row)
    assert tuple(row['message_id'] for row in records) == IDS
    save(OUT,{'format':'dk4-native-common-editorial-v1','translation_policy':'natural-dialogue-v2','target_locale':'en-US',
        'encoder':'dialogue-relocatable-v1','consumer_layout_profile':PROFILE,'file_path':'/COMMON/MESFILE.DK4',
        'review_gates':['source','context','localization','naturalness','formatting'],'formatting_review_pending':True,
        'status':'6-source-context-prose-reviewed;native-formatting-release-and-revised-gameplay-pending',
        'source_clean_ROM_sha256':sha(Path('work/clean.nds').read_bytes()),'current_ROM':str(rom_path),
        'current_ROM_sha256':sha(rom_path.read_bytes()),'current_COMMON_sha256':sha(common),'current_ARM9_sha256':sha(arm),
        'source_context':str(CONTEXT),'source_context_sha256':sha(CONTEXT.read_bytes()),
        'source_native_voice_fallbacks_preserved':True,'no_authored_line_breaks_or_alignment':True,
        'no_new_ROM_native_layout_or_revised_gameplay_approval':True,'records':records,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Six natural-English fire alerts source/context/prose reviewed;native formatting,registered release and revised gameplay remain pending.',flush=True)


if __name__ == '__main__':
    main()
