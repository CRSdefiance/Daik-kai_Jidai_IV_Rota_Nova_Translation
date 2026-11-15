"""Prepare an immutable B48 audit from the source-locked progressive audit and FE oracle."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive

if __name__=='__main__':
    source=Path('scripts/audit_Rafael_B47_actual_v7999.py').read_text(encoding='utf-8')
    changes={
        'B47':'B48', 'R53':'R347', 'R0053':'R0347',
        'Rafael_B47_actual_v7999':'Rafael_B48_actual_v8051',
        'Rafael_B47_scene_fixtures_v7997':'Rafael_B48_scene_fixtures_v8049',
        'Rafael_B47_scene_runs_v7998':'Rafael_B48_scene_runs_v8050',
        'Rafael_B47_source_name_planes_v7986/15_complete_source_pages4_names16_literal_alignments_all_progressive.json':'Rafael_B48_source_name_planes_v8037/91_complete_source_pages9_names36_literal_alignments4_FE.json',
        'Rafael_B47_pages_v7985/15_complete_native_paragraphs16_pages60_compiled_alignments.json':'Rafael_B48_pages_refined_v8038/91_final_native_paragraphs92_pages4_fresh360_reused_alignments.json',
        'Rafael_B47_stored_v7990/all15_stored_bodies32_fresh28_reused_alignments16_exact_viewed_pages.json':'Rafael_B48_stored_v8042/all91_stored_bodies192_fresh172_reused_alignments92_exact_viewed_pages.json',
        'Rafael_B47_current_v7980/all15_complete_source_current_refs_before_new_English_manuscript.json':'Rafael_B48_current_v8028/all91_complete_source_current_refs_before_new_English_manuscript.json',
        'Rafael_B47_source_paths_v7978/625_source_result_compositions_six_text_paths_two_exclusive_alternatives.json':'Rafael_B48_source_paths_v8025/500_source_result_compositions32_text_paths_two_exclusive_pairs.json',
        '16001':'40001', '16000':'40000', '32002':'80002',
        "stored['all15_native_ink_planes_exact_to_already_viewed']":"stored['all91_native_ink_planes_exact_to_already_viewed']",
        'len(expected)==58 and len(records)==15':'len(expected)==173 and len(records)==91',
        "record=records[at];actor=record['source_selector'];assert actor in [0,4,5,6]":"record=records[at];actor=record['source_selector'];assert actor in [0,4,5,6,7,8,13,75,113,254]\n            is_FE=actor==254",
        "models=[model_page(arm,fnt,p) for p in model['pages']]\n            np=next(n for n in font['name_planes'] if n['actor_ID']==actor)\n            pixels=Path(np['native_plane']).read_bytes();assert sha(pixels)==np['native_plane_sha256']\n            nameink={(i%216,i//216) for i,b in enumerate(pixels) if b}":"models=[FE_model(p,version) if is_FE else model_page(arm,fnt,p) for p in model['pages']]\n            np=None if is_FE else next(n for n in font['name_planes'] if n['actor_ID']==actor)\n            if np is not None:\n                pixels=Path(np['native_plane']).read_bytes();assert sha(pixels)==np['native_plane_sha256']\n                nameink={(i%216,i//216) for i,b in enumerate(pixels) if b}\n            else:nameink=set()",
        "def masks(image):\n    pixels=image.crop((16,296,232,360)).get_flattened_data()\n    return {c:{(i%216,i//216) for i,v in enumerate(pixels) if v==c} for c in COLORS}":"def masks(image,width=216):\n    pixels=image.crop((16,296,16+width,360)).get_flattened_data()\n    return {c:{(i%width,i//width) for i,v in enumerate(pixels) if v==c} for c in COLORS}\ndef FE_model(page,version):\n    if version=='clean_Japanese':\n        physical=Path(page['physical_plane']).read_bytes();assert sha(physical)==page['physical_plane_sha256']\n    else:\n        logical=Path(page['native_plane']).read_bytes();assert len(logical)==228*48 and sha(logical)==page['native_plane_sha256']\n        physical=bytearray(228*64)\n        for y in range(48):\n            for x in range(228):physical[(y//12*16+y%12)*228+x]=int(bool(logical[y*228+x]))\n        physical=bytes(physical);assert sha(physical)==page['physical_plane_sha256']\n    assert len(physical)==228*64\n    return {COLORS[0]:{(i%228,i//228) for i,b in enumerate(physical) if b==(15 if version=='clean_Japanese' else 1)},\n        COLORS[1]:set(),COLORS[2]:{(i%228,i//228) for i,b in enumerate(physical) if b==14} if version=='clean_Japanese' else set()}",
        "image=im,masks=masks(im))":"image=im,masks=masks(im),FE_masks=masks(im,228))",
        "photo['masks'][color]^expected_mask[color]":"photo['FE_masks' if is_FE else 'masks'][color]^expected_mask[color]",
        "found={(x-16,y-276) for y in range(276,289) for x in range(14,18+np['original_pair_flush_width']) if photo['image'].getpixel((x,y))==(98,97,98)}":"found={(x,y) for y in range(276,289) for x in range(14,244) if photo['image'].getpixel((x,y))==(98,97,98)} if is_FE else {(x-16,y-276) for y in range(276,289) for x in range(14,18+np['original_pair_flush_width']) if photo['image'].getpixel((x,y))==(98,97,98)}",
        "complete_name_mask_equal=True,actual_name=np['text'],native_geometry=[216,64]":"complete_name_mask_equal=not is_FE,original_FE_absent_nameplate_preserved=is_FE,actual_name=None if is_FE else np['text'],native_geometry=[228 if is_FE else 216,64]",
        "kind='progressive',actual_name=np['text'],interval=pair":"kind='system-FE' if is_FE else 'progressive',actual_name=None if is_FE else np['text'],interval=pair",
        "complete_progressive_header_holds=sum(len(s['complete_body_holds']) for s in speeches),":"complete_progressive_header_holds=sum(len(s['complete_body_holds']) for s in speeches if s['source_selector']!=254),\n            complete_FE_absent_header_holds=sum(len(s['complete_body_holds']) for s in speeches if s['source_selector']==254),",
        'all15_source_objects_retained_butonly_observed_path_is_actual_gameplay_coverage':'all91_source_objects_retained_butonly_observed_path_is_actual_gameplay_coverage',
        "Actual scope excludes four conditional source objects;comparison/view/release pending.":"Actual scope explicitly lists every native-only conditional object;comparison/view/release pending.",
    }
    print(derive('scripts/audit_Rafael_B47_actual_v7999.py','scripts/audit_Rafael_B48_actual_v8051.py',changes))
