"""Exercise all eight malformed-scope rejections without committing caller ROM changes."""
from scripts import qualify_hodram_B301_B310_registered_v1 as previous
from scripts.prepare_hodram_B311_B324_registered_v1 import CONFIG, QUALIFICATION, ROOT
from dk4tool.patch.hodram_b311_b324_release_v1 import plan_release
from scripts.source_locked_derivation_v5118 import checked_text

OUT = ROOT/'registered_semantic_checks_v1'
source = checked_text(previous.source, {
    "'record_count',233": "'record_count',399",
    "'speech_count',224": "'speech_count',386",
    "'typed_choice_count',8": "'typed_choice_count',12",
    "'style_count',151": "'style_count',235",
    "conf['blocks']+[300]": "conf['blocks']+[310]",
    "'scoped_name_count',7": "'scoped_name_count',10",
    'all 8 FE bodies': 'all 14 FE bodies',
})
env = {**previous.env, **globals(), '__file__':__file__}
exec(compile(source,__file__+'::same-eight-scope-rejections-and-caller-purity-new-scope','exec'),env)
if __name__ == '__main__':
    env['main']()
