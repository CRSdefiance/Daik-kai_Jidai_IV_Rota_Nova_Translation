"""Scope unchanged whole-file loader/census tools to all ten resized blocks."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_Shrines_Temples_reference_tools_v3195')
LOAD_OLD=Path('scripts/verify_lil_crew_items_loader_v3139.py')
LOAD_NEW=Path('scripts/verify_lil_shrines_loader_v3195b.py')
REF_OLD=Path('scripts/verify_lil_crew_items_references_v3140.py')
REF_NEW=Path('scripts/verify_lil_shrines_references_v3196.py')

if __name__=='__main__':
    assert not any(p.exists() for p in [ROOT,LOAD_NEW,REF_NEW])
    text=LOAD_OLD.read_text(encoding='utf-8')
    for a,b in [
        ('prepare_lil_crew_items_research_v3138','prepare_lil_shrines_research_v3194'),
        ('lil_Crew_Items_loader_v3139','lil_Shrines_Temples_loader_v3195b'),
        ('lil_Crew_Items_research_v3138','lil_Shrines_Temples_research_v3194'),
        ('fourteen','ten')]:
        assert a in text
        text=text.replace(a,b)
    LOAD_NEW.write_text(text,encoding='utf-8')
    text=REF_OLD.read_text(encoding='utf-8')
    for a,b in [
        ('prepare_lil_crew_items_research_v3138','prepare_lil_shrines_research_v3194'),
        ('lil_Crew_Items_reference_census_v3140','lil_Shrines_Temples_reference_census_v3196'),
        ('lil_Crew_Items_loader_v3139','lil_Shrines_Temples_loader_v3195b'),
        ('fourteen','ten'),
        ('all268_commands4_relative_sites_and_shipped_entry_census','all421_commands114_relative_sites_and_shipped_entry_census'),
        ('all268_clean_current_target_commands_and4_relative_sites_reexecuted','all421_clean_current_target_commands_and114_relative_sites_reexecuted'),
        ('all322_other_SC2_blocks_preserved','all326_other_SC2_blocks_preserved')]:
        assert a in text
        text=text.replace(a,b)
    old='from scripts.inventory_lil_lessons_v1717 import inventory'
    assert text.count(old)==1
    text=text.replace(old,'from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory\ninventory,_,_=scoped_inventory()')
    text=text.replace('(81,82,83,84,86,88,91,92,93,94,95,96,99,100)','range(101,111)')
    old="        expected = {81:10,82:45,83:21,84:31,86:14,88:30,91:16,92:25,93:18,94:17,95:14,96:13,99:8,100:6}[number]"
    assert text.count(old)==1
    text=text.replace(old,"        expected = len(spec['command_map'])")
    text=text.replace("spec['text_records']+spec['choice_commands']","spec['text_records']+spec['actor_style_commands']+spec['choice_commands']")
    text=text.replace('(0x100,0x200,0x300,0x2100)','(0x100,0x200,0x300,0x400,0x4100,0x2200)')
    old="        assert len(spec['relative_skip_fixups']) == {81:0,82:4,83:0,84:0,86:0,88:0,91:0,92:0,93:0,94:0,95:0,96:0,99:0,100:0}[number]"
    assert text.count(old)==1
    text=text.replace(old,"        assert len(spec['relative_skip_fixups']) == sum(c['word'] in [0x100,0x200,0x300,0x400] for c in spec['command_map'])")
    text=text.replace("typed_choice_count=len(spec['choice_commands']),","typed_choice_count=len(spec['choice_commands']),typed_actor_style_count=len(spec['actor_style_commands']),")
    text=text.replace("==268","==421").replace("==4\n","==114\n").replace("==20\n","==570\n")
    text=text.replace("native_commands_each=268,relative_sites=4,target_native_skip_cases=20","native_commands_each=421,relative_sites=114,target_native_skip_cases=570")
    REF_NEW.write_text(text,encoding='utf-8')
    for path in [LOAD_NEW,REF_NEW]:compile(path.read_text(encoding='utf-8'),str(path),'exec')
    ROOT.mkdir(parents=True)
    save(ROOT/'reference_producers.json',dict(
        inputs={str(p):sha(p.read_bytes()) for p in [LOAD_OLD,REF_OLD]},
        successors={str(p):sha(p.read_bytes()) for p in [LOAD_NEW,REF_NEW]},
        count3_menu_alias_objects_and0400_spans_explicit=True,no_global_helper_or_predecessor_edit=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
