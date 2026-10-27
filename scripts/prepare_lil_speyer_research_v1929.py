"""V1909-derived Speyer research image; all unowned files/components preserved."""
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_name_catalog_glyphs_v278 import raster,expected_pixels
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/lil_Speyer_research_v1929')
PARENT = Path('out/all_routes_combined_v1909_candidate.nds')
ROM = ROOT/'lil_Speyer_V1909_derived_RESEARCH_ONLY.nds'
PLAN = Path('work/analysis/lil_Speyer_relocation_v1928/nested_source_relocation_research.json')
FONT = Path('work/analysis/lil_Speyer_fonts_v1922/all57_native_macros_and_complete_font_planes.json')

if __name__ == '__main__':
    assert not ROOT.exists()
    plan,font = map(read,(PLAN,FONT))
    assert plan['all57_texts_two_choice_labels_and48_relative_operands_preserved']
    assert plan['all240_relocated_native_skip_cases_match_original_target_mapping']
    assert sha(PARENT.read_bytes()) == plan['candidate_sha256'] == font['candidate_sha256']
    assert plan['manuscript_sha256'] == font['manuscript_sha256']
    assert len(font['cases']) == 57 and not font['failures'] and font['native_macro_calls'] == 456
    parent,image = NdsImage.open(PARENT),NdsImage.open(PARENT)
    arm = image.read_file('/__arm9__.bin')
    container = IlnkContainer.parse(parent.read_file('/data/SC2.DK4'))
    fonts = {r['id']:r for r in font['cases']}
    parity = []
    for spec in plan['blocks']:
        number = spec['block']
        assert number in (25,128)
        assert sha(container.blocks[number]) == spec['source_block_sha256']
        target = Path(spec['research_block']).read_bytes()
        assert sha(target) == spec['research_block_sha256']
        assert spec['inverse_restoration_recovers_every_original_logical_byte']
        for row in spec['text_records']:
            raw = bytes.fromhex(row['target_hex'])
            assert raw[:1] == bytes.fromhex(fonts[row['id']]['encoded_hex'])[:1]
            expanded = raw[1:].replace(b'FI',b'Lil').replace(b'FA',b'Argot').replace(b'FO',b'Argot Co.')
            pixels,events,kanji = raster(arm,expanded)
            assert pixels == expected_pixels(arm,kanji,events)
            assert sha(pixels) == fonts[row['id']]['native_font_plane_sha256']
            parity.append(dict(id=row['id'],parity_space_added=row['parity_space_added'],
                complete_final_target_native_plane_equals_reviewed_plane=True,native_plane_sha256=sha(pixels)))
        container.blocks[number] = target
    assert len(parity) == 57
    image.replace_file('/data/SC2.DK4',container.to_bytes())
    ROOT.mkdir(parents=True)
    image.save(ROM)
    result = NdsImage.open(ROM)
    assert [p for _,p,data in parent.iter_files() if result.read_file(p)!=data] == ['/data/SC2.DK4']
    for path,data in parent.iter_components():assert result.read_file(path)==data,path
    before,after = (IlnkContainer.parse(v.read_file('/data/SC2.DK4')).blocks for v in(parent,result))
    assert len(before)==len(after)==336
    assert [n for n,(a,b) in enumerate(zip(before,after,strict=True)) if a!=b] == [25,128]
    growth = {str(n):len(after[n])-len(before[n]) for n in(25,128)}
    save(ROOT/'research_image_receipt.json',dict(parent=str(PARENT),parent_sha256=sha(PARENT.read_bytes()),
        research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),ARM9_sha256=sha(arm),
        SC2_sha256=sha(result.read_file('/data/SC2.DK4')),COMMON_sha256=sha(result.read_file('/COMMON/MESFILE.DK4')),
        only_changed_file='/data/SC2.DK4',only_changed_blocks=[25,128],block_growth_bytes=growth,
        all334_other_SC2_blocks_every_other_file_and_native_component_exact=True,
        all57_final_targets_complete_native_planes_equal_reviewed_planes=True,final_target_parity_cases=parity,
        registered_candidate=False,not_for_user_handoff_or_new_parent=True,
        original_scene_controls_and_revised_actual_and_reference_approval_pending=True,
        source_relocation_plan=str(PLAN),source_relocation_plan_sha256=sha(PLAN.read_bytes()),
        native_font_proof=str(FONT),native_font_proof_sha256=sha(FONT.read_bytes()),
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    (ROOT/'RESEARCH_ONLY.txt').write_text('Unregistered V1909-derived Speyer test image. Only SC2 B25/B128 change. Not a release or construction parent. Source-control/live/reference/registered-release approval remains pending.\n',encoding='utf-8')
    print(dict(research_ROM_sha256=sha(ROM.read_bytes()),only_changed_blocks=[25,128],growth=growth,
        all57_final_native_planes_exact=True,registered=False))
