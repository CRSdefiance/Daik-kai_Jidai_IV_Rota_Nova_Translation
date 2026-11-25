"""V1945-derived B74 research image with separate final FE/progressive planes."""
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_name_catalog_glyphs_v278 import raster, expected_pixels
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_Hamburg_research_v1961')
PARENT = Path('out/all_routes_combined_v1945_candidate.nds')
ROM = ROOT/'lil_Hamburg_V1945_derived_RESEARCH_ONLY.nds'
PLAN = Path('work/analysis/lil_Hamburg_relocation_v1960/nested_source_relocation_research.json')
FONT = Path('work/analysis/lil_Hamburg_font_approval_v1959/all79_complete_native_font_and_macro_reconciliation.json')

if __name__ == '__main__':
    assert not ROOT.exists()
    plan, font = map(read,(PLAN,FONT))
    assert plan['all79_texts_two_choice_labels_and20_relative_operands_preserved']
    assert plan['all100_relocated_native_skip_cases_match_original_target_mapping']
    assert sha(PARENT.read_bytes()) == plan['candidate_sha256'] == font['candidate_sha256']
    assert plan['manuscript_sha256'] == font['manuscript_sha256']
    assert len(font['cases']) == 79 and not font['failures'] and font['native_macro_calls'] == 632
    parent, image = NdsImage.open(PARENT), NdsImage.open(PARENT)
    arm = image.read_file('/__arm9__.bin')
    container = IlnkContainer.parse(parent.read_file('/data/SC2.DK4'))
    fonts = {r['id']:r for r in font['cases']}
    # Reuse the exact proven mode1 renderer setup, not a progressive bitmap.
    fe_source = Path('scripts/probe_lil_london_FE_v1896.py')
    setup = fe_source.read_text(encoding='utf-8').split('    ROOT.mkdir(parents=True)')[0]
    for old,new in {
        'from dk4tool.dialogue.lil_london_profile import profile_for':'from dk4tool.dialogue.lil_hamburg_profile import profile_for',
        "ROOT=Path('work/analysis/lil_London_FE_v1896')":"ROOT=Path('work/analysis/lil_Hamburg_FE_parity_context_v1961')",
        'translations/lil_london_editorial_manuscript_v3.json':'translations/lil_hamburg_recruitment_editorial_manuscript_v3.json',
        'work/analysis/lil_London_context_navigation_v1891/closed_original_B26_context.json':
            'work/analysis/lil_Hamburg_arrival_navigation_v1933/closed_original_scene_context.json',
        ".blocks[26],'FE-paper'":".blocks[74],'FE-paper'",
    }.items():
        assert setup.count(old) == 1,old
        setup = setup.replace(old,new)
    env = {'__name__':'__main__','__file__':__file__}
    exec(compile(setup,str(fe_source),'exec'),env)
    render_fe = env['render']
    parity = []
    assert len(plan['blocks']) == 1
    spec = plan['blocks'][0]
    assert spec['block'] == 74
    assert sha(container.blocks[74]) == spec['source_block_sha256']
    target = Path(spec['research_block']).read_bytes()
    assert sha(target) == spec['research_block_sha256']
    assert spec['inverse_restoration_recovers_every_original_logical_byte']
    for row in spec['text_records']:
        raw = bytes.fromhex(row['target_hex'])
        case = fonts[row['id']]
        assert raw[:1] == bytes.fromhex(case['encoded_hex'])[:1]
        body = raw[1:].replace(b'FI',b'Lil').replace(b'FA',b'Argot').replace(b'FO',b'Argot Co.')
        if raw[0] == 254:
            pixels, physical, events = render_fe(body)
            assert sha(pixels) == case['native_plane_sha256']
            assert pixels == Path(case['native_plane']).read_bytes()
            consumer = 'original_FE_modal_5473C_mode1'
        else:
            pixels, events, kanji = raster(arm,body)
            assert pixels == expected_pixels(arm,kanji,events)
            assert sha(pixels) == case['native_font_plane_sha256']
            consumer = 'original_progressive_54020'
        parity.append(dict(id=row['id'],consumer=consumer,parity_space_added=row['parity_space_added'],
            complete_final_target_native_plane_equals_reviewed_plane=True,native_plane_sha256=sha(pixels)))
    assert len(parity) == 79
    container.blocks[74] = target
    image.replace_file('/data/SC2.DK4',container.to_bytes())
    ROOT.mkdir(parents=True)
    image.save(ROM)
    result = NdsImage.open(ROM)
    assert [p for _,p,data in parent.iter_files() if result.read_file(p) != data] == ['/data/SC2.DK4']
    for path,data in parent.iter_components(): assert result.read_file(path) == data,path
    before, after = (IlnkContainer.parse(v.read_file('/data/SC2.DK4')).blocks for v in (parent,result))
    assert len(before) == len(after) == 336
    assert [n for n,(a,b) in enumerate(zip(before,after,strict=True)) if a != b] == [74]
    growth = {'74':len(after[74])-len(before[74])}
    save(ROOT/'research_image_receipt.json',dict(parent=str(PARENT),parent_sha256=sha(PARENT.read_bytes()),
        research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),ARM9_sha256=sha(arm),
        SC2_sha256=sha(result.read_file('/data/SC2.DK4')),COMMON_sha256=sha(result.read_file('/COMMON/MESFILE.DK4')),
        only_changed_file='/data/SC2.DK4',only_changed_blocks=[74],block_growth_bytes=growth,
        all335_other_SC2_blocks_every_other_file_and_native_component_exact=True,
        all79_final_targets_complete_native_planes_equal_reviewed_planes=True,final_target_parity_cases=parity,
        registered_candidate=False,not_for_user_handoff_or_new_parent=True,
        revised_actual_and_reference_approval_pending=True,
        source_relocation_plan=str(PLAN),source_relocation_plan_sha256=sha(PLAN.read_bytes()),
        native_font_proof=str(FONT),native_font_proof_sha256=sha(FONT.read_bytes()),
        inherited_FE_renderer_source=str(fe_source),inherited_FE_renderer_source_sha256=sha(fe_source.read_bytes()),
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    (ROOT/'RESEARCH_ONLY.txt').write_text('Unregistered V1945-derived B74 image. Source/native fonts approved; revised actual/reference/release checks pending. Not a construction parent.\n',encoding='utf-8')
    print(dict(research_ROM_sha256=sha(ROM.read_bytes()),only_changed_blocks=[74],growth=growth,all79_final_native_planes_exact=True))
