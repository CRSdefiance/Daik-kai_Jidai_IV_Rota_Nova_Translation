"""Enable documented ordinary stylus input for the genuine-save market replay."""
from scripts.run_market_goods_info_fix_checks_v2 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{
    "mode+'_run_v2'":"mode+'_run_v3'",
    "    donor=parent.get('battery_save_preloaded')":
        "    if any('touch' in event for event in parent['scripted_input_schedule']):command+=['--touchscreen']\n    donor=parent.get('battery_save_preloaded')",
})
exec(compile(source,__file__+'::same-source-save-andcontroller-stylus-schedule-documented-touch-option','exec'),globals())
