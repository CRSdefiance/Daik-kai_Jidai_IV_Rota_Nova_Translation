"""Expose original SDK stage-cache coverage for the actual five-section current image."""
import inspect
from ndspy.code import MainCodeFile
from scripts import probe_persistent_name_arm7_boot_overlap as original
from scripts.source_locked_derivation_v5118 import checked_text
SOURCE=checked_text(inspect.getsource(original.execute),{'len(arm9_sections) == 4':'len(arm9_sections) == 5'})
namespace=dict(original.__dict__)
exec(compile(SOURCE,__file__+'::five-section-stage-coverage','exec'),namespace)
_execute=namespace['execute']
def execute(arm9,arm7,arm7_base,repair_entry=None,expected_pool=None):
    sections=MainCodeFile(arm9,original.BASE).sections
    assert len(sections)==5 and sections[3].ramAddress==original.STAGE
    return _execute(arm9,arm7,arm7_base,repair_entry,expected_pool)
