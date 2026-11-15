"""Tighten2015's crew scope from clean Japanese,not from fitting constraints."""
from copy import deepcopy
from dataclasses import asdict
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.ship_sinking_editorial import current_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.verify_village_wrap_v608 import read,save

OUT = Path('translations/flagship_capture_precision_manuscript_v1.json')


def main():
    assert not OUT.exists()
    old_path = Path('translations/battle_aftermath_editorial_manuscript_v3.json')
    old = read(old_path)
    row = deepcopy(next(r for r in old['records'] if r['message_id']==2015))
    rom_path = Path('out/all_routes_combined_v1344_candidate.nds')
    rom,clean = NdsImage.open(rom_path),NdsImage.open('work/clean.nds')
    arm,common = rom.read_file('/__arm9__.bin'),rom.read_file('/COMMON/MESFILE.DK4')
    entries = current_entries(common,arm)
    jp = common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),clean.read_file('/__arm9__.bin'))
    assert jp[2015].text.hex()==row['source_hex']
    assert entries[2015].text==bytes.fromhex(row['compiled_hex'])
    row.update(previous_reviewed_English=row['english'],previous_current_reference=row['current_reference'],
        current_reference={k:v for k,v in asdict(entries[2015]).items() if k!='text'},
        current_text_hex=entries[2015].text.hex(),current_English=entries[2015].text.decode('ascii'),
        english="We've captured the enemy flagship after defeating its entire crew!",
        source_meaning='All crew aboard the enemy flagship were defeated,and that ship was captured;the line does not claim defeat of every enemy vessel or crew.',
        localization_note='The earlier entire enemy crew could suggest the whole opposing fleet. Its entire crew explicitly refers to the named flagship,matching teki kikan no suifu o zen-in. The after clause makes natural English of the defeat-and-capture sequence without inventing deaths or another outcome. Preserve the courteous emphatic report without artificial archaic language.',
        context=row['context']+' Original V1353 gameplay selected sister2011 after an unforced duel capture,and returned through normal rewards/cargo to sailing. Original53D44 uses82478 logical role selection;the physical First Mate slot may be empty while existing Gerhard16 is chosen automatically.2015 is a different original voice alternative,not the next spoken record.',
        review={'source':True,'context':True,'localization':True,'naturalness':True,'formatting':False},
        status='precision-rereviewed;new-native-formatting-registered-release-and-current-candidate-gameplay-pending')
    row['unwrapped_paragraph_hex'] = row['english'].encode('ascii').hex()
    row.pop('compiled_hex')
    save(OUT,{'format':'dk4-native-common-editorial-v1','translation_policy':'natural-dialogue-v2','target_locale':'en-US',
        'encoder':'dialogue-relocatable-v1','consumer_layout_profile':'flagship-capture-precision-portrait-postmacro-v1',
        'file_path':'/COMMON/MESFILE.DK4','review_gates':['source','context','localization','naturalness','formatting'],
        'formatting_review_pending':True,'records':[row],
        'source_clean_ROM_sha256':sha(Path('work/clean.nds').read_bytes()),'current_ROM':str(rom_path),
        'current_ROM_sha256':sha(rom_path.read_bytes()),'current_COMMON_sha256':sha(common),'current_ARM9_sha256':sha(arm),
        'supersedes_one_record_from':str(old_path),'supersedes_manuscript_sha256':sha(old_path.read_bytes()),
        'actual_related_family_proof':'work/analysis/flagship_capture_verified_v1354b/actual_flagship_capture_verification.json',
        'no_new_source_review_or_completion_credit':True,'no_authored_line_breaks_or_alignment':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('2015 rereviewed against clean Japanese:only the flagship crew. One natural paragraph;native/release gates pending.',flush=True)


if __name__=='__main__':
    main()
