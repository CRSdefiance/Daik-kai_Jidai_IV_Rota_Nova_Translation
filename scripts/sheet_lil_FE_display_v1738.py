"""Unaltered nearest-neighbor review sheet of the nine actual-context FE planes."""
from pathlib import Path
from PIL import Image, ImageDraw
from scripts.verify_village_wrap_v608 import read, save
from dk4tool.patch.grand_race_menu_release import sha

ROOT = Path('work/analysis/lil_FE_visual_v1738')
PROOF = Path('work/analysis/lil_FE_display_v1737/actual_paper_contract_and_all9_reviewed_FE_panels.json')

if __name__ == '__main__':
    assert not ROOT.exists()
    proof = read(PROOF)
    assert proof['all6_current_FE_native_actual_complete_ink_and_blank_cells_match']
    assert proof['all9_reviewed_FE_full_actual_context_native_planes_pass']
    cases = proof['reviewed_cases']
    assert len(cases) == 9
    sheet = Image.new('RGB', (720, 9 * 232), (27, 35, 41))
    draw = ImageDraw.Draw(sheet)
    for index, case in enumerate(cases):
        path = Path(case['display_preview'])
        assert sha(path.read_bytes()) == case['display_preview_sha256']
        original = Image.open(path).convert('RGB')
        assert original.size == (228, 64)
        draw.text((18, index * 232 + 10), case['id'], fill='white')
        sheet.paste(original.resize((684, 192), Image.Resampling.NEAREST), (18, index * 232 + 32))
    ROOT.mkdir(parents=True)
    path = ROOT / 'all9_actual_context_FE_previews_3x.png'
    sheet.save(path)
    save(ROOT / 'sheet_receipt.json', {'source_proof': str(PROOF), 'source_sha256': sha(PROOF.read_bytes()),
        'sheet': str(path), 'sheet_sha256': sha(path.read_bytes()),
        'unmodified_source_planes_nearest_neighbor_3x': True, 'visual_review_pending': True,
        'producer_sha256': sha(Path(__file__).read_bytes())})
    print(path)
