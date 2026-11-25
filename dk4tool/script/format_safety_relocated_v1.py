"""Apply the original story-percent test with exact relocated speaker offsets."""
import inspect
from pathlib import Path
from types import FunctionType
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.script import format_safety as original
from scripts.audit_story_glyph_consistency import load
from scripts.source_locked_derivation_v5118 import checked_text

SOURCE=checked_text(inspect.getsource(original.story_percent_findings),{
    "old = original[segment] if segment < len(original) else b''":
        "old = source_records.get((block,segment),original[segment] if segment < len(original) else b'')",
})

def qualified_source_records(source,current,receipt):
    assert sha(source)==receipt['clean_SC0_sha256']
    clean,final=[IlnkContainer.parse(x).blocks for x in [source,current]]
    assert len(clean)==len(final)==343
    mapping={}
    for row in receipt['relocated_source25_records']:
        b=row['block'];before,after=clean[b],final[b]
        assert sha(before)==row['clean_block_sha256'] and sha(after)==row['target_block_sha256']
        a,z=row['source_offset'],row['target_offset'];assert a>=5 and z>=5
        old,new=bytes.fromhex(row['source_hex']),bytes.fromhex(row['target_hex'])
        head=bytes.fromhex(row['complete_preamble_hex'])
        assert len(head)==6 and head[:2]==b'\0@' and head[-1:]==b'%'
        assert before[a-5:a+1]==after[z-5:z+1]==head
        assert before[a:a+len(old)+1]==old+b'\0' and after[z:z+len(new)+1]==new+b'\0'
        assert old.startswith(b'%') and new.startswith(b'%') and b'%' not in new[1:]
        old_index=before[:a].count(b'\0');new_index=after[:z].count(b'\0')
        assert old_index==row['source_index'] and new_index==row['target_index'] and old_index!=new_index
        assert before.split(b'\0')[old_index]==old and after.split(b'\0')[new_index]==new
        key=(b,new_index);assert key not in mapping;mapping[key]=old
    return mapping

def reject_with_receipt(source_files,current_files,receipt):
    path='/data/SC0.DK4'
    mapping=qualified_source_records(source_files[path],current_files[path],receipt)
    env={**original.story_percent_findings.__globals__,'source_records':mapping}
    exec(compile(SOURCE,__file__+'::same-original-detector-exact-relocated-source-records','exec'),env)
    def findings(source,current):
        if source is source_files[path] and current is current_files[path]:
            return env['story_percent_findings'](source,current)
        return original.story_percent_findings(source,current)
    guard=FunctionType(original.reject_story_percent_commands.__code__,
        {**original.reject_story_percent_commands.__globals__,'story_percent_findings':findings})
    report=guard(source_files,current_files)
    report.update(exact_source_bound_relocated_leading25_count=len(mapping),
        relocated_source25_records=[dict(block=b,target_index=i) for b,i in sorted(mapping)],
        original_four_archive_printf_checks_and_nonleading_rejections_preserved=True,
        checked_detector_source_sha256=sha(SOURCE.encode('utf-8')))
    return report

def bind_registered_story_percent_guard(spec):
    path=Path(spec['path'])
    assert sha(path.read_bytes())==spec['sha256']
    receipt=load(path)
    for ref,digest in receipt['evidence'].items():assert sha(Path(ref).read_bytes())==digest
    assert receipt['original_failure_andall_rejections_verified']
    def guard(source_files,current_files):
        report=reject_with_receipt(source_files,current_files,receipt)
        report['exact_relocation_receipt']=spec
        return report
    return guard
