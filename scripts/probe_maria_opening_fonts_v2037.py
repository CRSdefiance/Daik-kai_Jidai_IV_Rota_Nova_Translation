"""Source-scoped38-panel successor of the established native-plane probe."""
from pathlib import Path
SOURCE=Path('scripts/probe_hodram_opening_fonts_v2021.py')
if __name__=='__main__':
    text=SOURCE.read_text(encoding='utf-8')
    changes={
        'hodram_opening_fonts_v2021':'maria_opening_fonts_v2037',
        'translations/hodram_opening_contextual_editorial_manuscript_v1.json':'translations/maria_opening_contextual_editorial_manuscript_v1.json',
        'out/all_routes_combined_v2013_candidate.nds':'out/all_routes_combined_v2030_candidate.nds',
        'work/analysis/hodram_opening_context_v2018':'work/analysis/maria_opening_context_v2035',
        "report['no_save_savestate_or_fixtures']":"report['no_savestate_or_story_location_RNG_funds_outcome_fixture'] and report['earned_unlock_verified'] is False",
        'hodram_opening_context_v2018_V2013':'maria_opening_context_v2035_V2030',
        'get(0x7F244)==1':'get(0x7F244)==3',
        "struct.unpack_from('<I',raw,0x2796B0)[0]==1":"struct.unpack_from('<I',raw,0x2796B0)[0]==3",
        '(1,2,9,16,18,23)]==[1,2,9,16,18,23]':'(3,10,11,12,21,74)]==[3,10,11,12,21,74]',
        "get_dialogue_profile('hodram-story-live')":"get_dialogue_profile('maria-story-live')",
        'hodram-opening-editorial-native-v1-RESEARCH-ONLY':'maria-opening-editorial-native-v1-RESEARCH-ONLY',
        'frozenset({16,18,23})':'frozenset({21,74})',
        "{'FI':36,'FA':54,'FO':90,'I':12}":"{'FI':30,'FA':12,'FO':42,'I':12}",
        "{'FI':6,'FA':9,'FO':15}":"{'FI':5,'FA':2,'FO':7}",
        "{'FI':b'Hodram','FA':b'Bergstrom','FO':b'Bergstrom Fleet'}":"{'FI':b'Maria','FA':b'Li','FO':b'Li Clan'}",
        "b'Hodram Bergstrom Bergstrom Fleet'":"b'Maria Li Li Clan'",
        'captain if actor_ID==1':'captain if actor_ID==3',
        'all67_progressive_native_macros_and_complete_font_planes.json':'all38_progressive_native_macros_and_complete_font_planes.json',
        "{'FI':'Hodram','FA':'Bergstrom','FO':'Bergstrom Fleet'}":"{'FI':'Maria','FA':'Li','FO':'Li Clan'}",
    }
    for old,new in changes.items():
        assert old in text,old
        text=text.replace(old,new)
    exec(compile(text,str(SOURCE),'exec'),{'__name__':'__main__','__file__':__file__})
