"""Resolve real2218 orphan;document original conservative foraging quantity bounds."""
from copy import deepcopy
from pathlib import Path
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/search_reports_revision_v1665')
SOURCE = Path('translations/search_reports_editorial_manuscript_v1.json')
OUT = Path('translations/search_reports_editorial_manuscript_v2.json')

if __name__ == '__main__':
    assert not ROOT.exists() and not OUT.exists()
    doc = deepcopy(read(SOURCE))
    old = next(r for r in doc['records'] if r['message_id'] == 2218)
    assert old['english'] == "The expedition's back. Doesn't look like they found anything worthwhile."
    old['english'] = "The expedition's back. Looks like they found nothing worthwhile."
    old['localization_note'] += ' Native research1663c stranded worthwhile on a third line. This equally faithful casual sentence retains the return,tentative report and nothing worthwhile while avoiding that orphan;no authored line break or fact was added.'
    rom, clean = NdsImage.open(doc['current_ROM']), NdsImage.open('work/clean.nds')
    arm, original = rom.read_file('/__arm9__.bin'), clean.read_file('/__arm9__.bin')
    cs = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    spans = []
    for lo, hi in [(0x34F6C,0x34FC0),(0xAB7AC,0xAB800),(0x79958,0x79BEC),(0x79EEC,0x79F74),(0x519D4,0x51A28)]:
        assert arm[lo:hi] == original[lo:hi]
        spans.append({'start':0x02000000+lo,'end_exclusive':0x02000000+hi,'clean_code_hex':original[lo:hi].hex(),
                      'instructions':[f'{i.address:08X} {i.mnemonic} {i.op_str}' for i in cs.disasm(original[lo:hi],0x02000000+lo)]})
    ROOT.mkdir(parents=True)
    bounds = ROOT/'original_forage_quantity_bounds.json'
    save(bounds, {'candidate':doc['current_ROM'],'candidate_sha256':doc['current_ROM_sha256'],'source_code_spans':spans,
        'derivation':['34F6C examines at most five existing ship models.',
            'AB7AC counts at most31 layout slots of type9 in each model;each contributes zero or one. The fleet total is at most155.',
            '79958 returns one of0,1,2,3,4 according to location.',
            '79F08 requests original RNG(region+2),adds1 and multiplies by5 and the fleet slot total:water<=155*5*6=4650.',
            '79F24 requests original RNG(region+1),adds1 and multiplies by5 and the same total:food<=155*5*5=3875.',
            'These conservative limits allow even layouts that may be unavailable in ordinary play. Both quantities fit four full-width decimal digits.'],
        'conservative_water_max':4650,'conservative_food_max':3875,'maximum_original_digits_each':4,
        'above_bounds_CPU_cases_are_stress_only_and_never_source_reachable_forage_claims':True,
        'stress_cases_still_require_complete_native_fonts_and_bounds_no_dropped_characters':True,
        'no_runtime_value_change_or_weakened_real_scene_layout_gate':True})
    doc.update(revised_from_manuscript=str(SOURCE),revised_from_sha256=sha(SOURCE.read_bytes()),
               source_quantity_bounds=str(bounds),source_quantity_bounds_sha256=sha(bounds.read_bytes()),
               consumer_layout_profile='Search-role1-role7-postmacro-and-original-loss-modal-v1',
               formatting_review_pending=True,status='source-prose-revised-after-native-orphan;native-formatting-still-pending')
    for row in doc['records']:
        if row['message_id'] >= 2229:
            row['source_quantity_contract']={'argument_order':['water','food'],'original_formatter':'ABF50-positive-full-width-CP932-decimal',
                                            'conservative_maxima':[4650,3875],'original_max_digits_each':4}
    save(OUT,doc)
    save(ROOT/'revision_receipt.json',{'source_manuscript':str(SOURCE),'source_sha256':sha(SOURCE.read_bytes()),
        'manuscript':str(OUT),'manuscript_sha256':sha(OUT.read_bytes()),'revised_IDs':[2218],
        'source_quantity_bounds':str(bounds),'source_prose_reviews_added':0,'completed_entries_added':0,'full_goal_complete':False})
    print('2218 natural sentence revised to remove real orphan;source foraging maxima4650 water/3875 food documented. Native recheck pending;no new coverage credit.')
