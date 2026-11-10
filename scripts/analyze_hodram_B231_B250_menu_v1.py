"""Qualify this menu's complete pixels while recognizing its observed moving cursor band."""
from pathlib import Path
from scripts.analyze_hodram_B211_B230_menus_v1 import source as previous,menu_scopes
from scripts.audit_story_glyph_consistency import load
from scripts.approve_hodram_B231_B250_display_v2 import ROOT
from scripts.source_locked_derivation_v5118 import checked_text

BODY=ROOT/'actual_pixels_v1/focused_actual_pixels.json'

def background_band(im,blank):
    """Every non-ink pixel remains exact; a contiguous cyan stripe can enter/leave a cell."""
    ys=sorted({y for _,y in blank});cyan=[]
    for y in ys:
        colors={im.getpixel((x,y)) for x,yy in blank if yy==y}
        assert len(colors)==1 and next(iter(colors)) in {(205,198,180),(0,165,172)}
        if next(iter(colors))==(0,165,172):cyan.append(y)
    assert not cyan or cyan==list(range(min(cyan),max(cyan)+1))
    assert not cyan or min(cyan)==min(ys) or max(cyan)==max(ys)
    return bool(cyan)

source=checked_text(previous,{
    "                    cyan={point for point in blank if im.getpixel(point)==(0,165,172)}\n                    assert not cyan or cyan==blank\n                    if cyan:selected.append(option)\n                    else:assert all(im.getpixel(point)==(205,198,180) for point in blank)":
        "                    if background_band(im,blank):selected.append(option)",
    "        target=versions[-1]['object_hex']":
        """        target=versions[-1]['object_hex']
        assert len(fixture['menus'])==1 and fixture['menus'][0]['block']==243 and fixture['menus'][0]['source_command_offset']==674
        assert vm['labels']==['Try it','Leave it'] and rect==[88,64,168,128] and width==48""",
    'numeric_modal_return_register_original_story_branches_andcancellation_unvisited=True,':
        """cursor_background_model='Each complete row is native gray or cyan; one contiguous cyan band can enter or leave a cell. All non-ink pixels are checked, with no mixed row or foreign color accepted.',
        original_flat_highlight_checker_rejected_preserved=True,
        original_flat_checker_failure='Both observed complete-caption frames contain only an edge-clipped moving cyan band, not a solid 20-row highlight.',
        cursor_model_source=str(Path(__file__)),cursor_model_source_sha256=sha(Path(__file__).read_bytes()),
        numeric_modal_return_register_original_story_branches_andcancellation_unvisited=True,""",
})
if __name__=='__main__':exec(compile(source,__file__+'::exact-menu-complete-pixels-and-uniform-moving-band','exec'),globals())
