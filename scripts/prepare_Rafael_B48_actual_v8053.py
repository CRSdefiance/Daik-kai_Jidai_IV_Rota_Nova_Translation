"""Bind exactly one independently native-proved source-only nineteenth cell."""
from scripts.source_locked_derivation_v5118 import derive
if __name__=='__main__':
    print(derive('scripts/audit_Rafael_B48_actual_v8051b.py','scripts/audit_Rafael_B48_actual_v8053.py',{
        'Rafael_B48_actual_v8051b':'Rafael_B48_actual_v8053',
        'Rafael_B48_source_name_planes_v8037/91_complete_source_pages9_names36_literal_alignments4_FE.json':'Rafael_B48_source_rightcell_v8052/91_source_native_pages9_name_planes_R129_actual_rightcell_bound.json',
        "pixels=Path(page['native_plane']).read_bytes()\n    assert len(pixels)==216*64":"pixels=Path(page['native_plane']).read_bytes()\n    if page.get('native_viewport_width')==228:\n        assert all(e['kind']=='cp932' for e in page['events'])\n        assert len(pixels)==228*64 and sha(pixels)==page['native_plane_sha256']\n        return {COLORS[0]:{(i%228,i//228) for i,b in enumerate(pixels) if b==1},COLORS[1]:set(),COLORS[2]:{(i%228,i//228) for i,b in enumerate(pixels) if b==15}}\n    assert len(pixels)==216*64",
        "models=[FE_model(p,version) if is_FE else model_page(arm,fnt,p) for p in model['pages']]":"models=[FE_model(p,version) if is_FE else model_page(arm,fnt,p) for p in model['pages']]\n            source_rightcell=version=='clean_Japanese' and record['id']=='DK4_MES_B48_R0129'\n            assert source_rightcell==any(p.get('native_viewport_width')==228 for p in model['pages'])",
        "photo['FE_masks' if is_FE else 'masks']":"photo['FE_masks' if is_FE or source_rightcell else 'masks']",
        "native_geometry=[228 if is_FE else 216,64]":"native_geometry=[228 if is_FE or source_rightcell else 216,64]",
    }))
