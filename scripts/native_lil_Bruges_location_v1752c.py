"""Source terrain uses original overlay0 at01FFA000; prior base-section assumption rejected."""
import inspect
from pathlib import Path
from ndspy.code import loadOverlayTable
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts import native_lil_Bruges_location_v1752 as previous
from scripts import native_village_contexts_v618 as terrain
from scripts.prepare_lil_lessons_research_v1739 import ROM
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_Bruges_location_v1752c')
REQUEST=previous.REQUEST

def source_bound_terrain(arm,points):
    current=NdsImage.open(ROM); clean=NdsImage.open('work/clean.nds')
    assert current.read_file('/__arm9__.bin')==arm
    original=clean.read_file('/__arm9__.bin')
    assert arm[0x69B5C:0x69E00]==original[0x69B5C:0x69E00]
    def overlay(rom):
        return loadOverlayTable(rom.rom.arm9OverlayTable,lambda _,fid:rom.rom.files[fid])[0]
    current_overlay,clean_overlay=overlay(current),overlay(clean)
    assert current_overlay.ramAddress==clean_overlay.ramAddress==0x01FFA000
    assert bytes(current_overlay.data)==bytes(clean_overlay.data)
    assert len(current_overlay.data)==6208
    # The existing helper itself loads the exact selected ROM overlay and clean world data.
    source=inspect.getsource(terrain.terrain_queries)
    anchor="NdsImage.open('out/all_routes_combined_v604_candidate.nds')"
    assert source.count(anchor)==1
    source=source.replace(anchor,'NdsImage.open(CURRENT_RESEARCH_ROM)')
    env={**terrain.__dict__,'CURRENT_RESEARCH_ROM':ROM}
    exec(compile(source,__file__,'exec'),env)
    result=env['terrain_queries'](arm,points)
    result.update(current_ROM_bound_instead_of_unavailable_V604=True,
        original_collision_and_ITCM_decoder_exact_to_clean=True,
        helper_source_sha256=sha(Path(terrain.__file__).read_bytes()),
        scoped_adapter_source_sha256=sha(source.encode()))
    return result

def apply_fixture(arm,raw,request):
    original=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    ranges=[(0x69B5C,0x69E00),(0xCB1A8,0xCB1B4),(0x2E58C,0x2E598),
            (0x36C70,0x36C94),(0x2C1C4,0x2C204),(0x34674,0x3468C),(0xCD6B8,0xCD6CC)]
    assert all(arm[a:b]==original[a:b] for a,b in ranges)
    source=inspect.getsource(previous.apply_fixture)
    anchor="reference=NdsImage.open('out/all_routes_combined_v604_candidate.nds').read_file('/__arm9__.bin')"
    assert source.count(anchor)==1
    source=source.replace(anchor,'reference=arm').replace('terrain=terrain_queries(reference,points)',
                                                           'terrain=source_bound_terrain(arm,points)')
    env={**previous.__dict__,'__file__':__file__,'source_bound_terrain':source_bound_terrain}
    exec(compile(source,__file__,'exec'),env)
    after,proof=env['apply_fixture'](arm,raw,request)
    proof['source_exact_getter_and_terrain_ranges']=ranges
    proof['failed_predecessor_missing_V604_reference_no_mutation_or_fixture_applied']=True
    return after,proof

if __name__=='__main__':
    assert not ROOT.exists()
    raw=Path('E:/Rota Nova translations/Generated/work/emulation_v193/lil_lesson_navigation_v1745_RESEARCH_ONLY/frame_030230_arm9_ram.bin').read_bytes()
    after,proof=apply_fixture(NdsImage.open(ROM).read_file('/__arm9__.bin'),raw,REQUEST)
    ROOT.mkdir(parents=True);save(ROOT/'location_only_preflight.json',proof)
    print({'owned_bytes':len(proof['owned_bytes']),'changed_bytes':len(proof['changes']),'target':proof['target_map_point']})
