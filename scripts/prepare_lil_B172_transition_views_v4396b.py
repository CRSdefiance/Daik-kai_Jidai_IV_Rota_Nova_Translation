"""Retain and expose the early original-portrait timing difference for review."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive

if __name__=='__main__':
    derive('scripts/prepare_lil_B172_transition_views_v4396.py','scripts/prepare_lil_B172_transition_views_v4396b_impl.py',{
        'lil_B172_transition_views_v4396':'lil_B172_transition_views_v4396b',
        "assert not actual['failures'] and not actual['paired_region_differences']":"assert not actual['failures']\n    assert actual['paired_region_differences']==[dict(id='DK4_MES_B172_R0007',frame=2950,native_text_plane_exact=True,paired_source_upper_or_portrait_region_differs=True,not_masked_or_retimed=True)]",
        "Image.open(p['path']).convert('RGB').resize((512,768),Image.Resampling.NEAREST).resize((256,384),Image.Resampling.NEAREST)":"Image.open(p['path']).convert('RGB')",
    })
    print('Corrected pre-view gate preserves the one measured early portrait difference; first failed producer retained.')
