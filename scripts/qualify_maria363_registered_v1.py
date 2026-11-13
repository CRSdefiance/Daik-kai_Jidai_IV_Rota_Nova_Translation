"""Retain eight production rejections and caller-preservation guards."""
from scripts.qualify_maria321_registered_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text
source = checked_text(previous, {
    'dk4tool.patch.maria321_release_v1':'dk4tool.patch.maria363_release_v1',
    'scripts.prepare_maria321_registered_v2':'scripts.prepare_maria363_registered_v1',
    "'record_count',320":"'record_count',362",
    "'speech_count',316":"'speech_count',350",
    "conf['blocks']+[216]":"conf['blocks']+[253]",
    "'scoped_name_count',23":"'scoped_name_count',28",
})
if __name__ == '__main__':
    exec(compile(source,__file__+'::same-eight-production-rejections-andpure-callers','exec'),globals())
