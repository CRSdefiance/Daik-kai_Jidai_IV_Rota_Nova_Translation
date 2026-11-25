"""Check Hamburg's original choice with fixed inherited menu margins."""
from pathlib import Path

SOURCE = Path('scripts/calibrate_lil_speyer_choice_v1939.py')

if __name__ == '__main__':
    text = SOURCE.read_text(encoding='utf-8')
    changes = {
        'lil_Speyer_choice_calibration_v1939':'lil_Hamburg_choice_calibration_v1964',
        'work/analysis/lil_Speyer_choice_v1927/original_choice_decoder_VM_geometry_and_native_pixels.json':
            'work/analysis/lil_Hamburg_choice_v1958/original_choice_decoder_VM_geometry_and_native_pixels.json',
        'work/analysis/lil_Speyer_original_navigation_v1934/closed_original_scene_context.json':
            'work/analysis/lil_Hamburg_arrival_navigation_v1933/closed_original_scene_context.json',
    }
    for old,new in changes.items():
        assert text.count(old) == 1,old
        text = text.replace(old,new)
    exec(compile(text,str(SOURCE),'exec'),{'__name__':'__main__','__file__':__file__})
