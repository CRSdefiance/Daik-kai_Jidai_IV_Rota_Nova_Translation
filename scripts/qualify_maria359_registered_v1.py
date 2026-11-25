"""Preserve eight production mutation rejections and caller-preservation assertions."""
from scripts.qualify_maria363_registered_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{
    'dk4tool.patch.maria363_release_v1':'dk4tool.patch.maria359_release_v1',
    'scripts.prepare_maria363_registered_v1':'scripts.prepare_maria359_registered_v1',
    "'record_count',362":"'record_count',358",
    "'speech_count',350":"'speech_count',348",
    "conf['blocks']+[253]":"conf['blocks']+[275]",
    "'scoped_name_count',28":"'scoped_name_count',17",
})
if __name__=='__main__':exec(compile(source,__file__+'::same-eight-real-production-rejections-andpure-callers','exec'),globals())
