"""Extend exact source25 bindings across named archives; keep the original detector."""
import inspect
from pathlib import Path
from types import FunctionType
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.script import format_safety as original
from dk4tool.script import format_safety_relocated_v1 as prior
from scripts.audit_story_glyph_consistency import load
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(inspect.getsource(prior.qualified_source_records),{
    'def qualified_source_records(':'def qualified_route_records(',
    "receipt['clean_SC0_sha256']":"receipt['clean_archive_sha256']",
    'len(clean)==len(final)==343':"len(clean)==len(final)==receipt['block_count']",
})
env=dict(prior.qualified_source_records.__globals__)
exec(compile(source,__file__+'::same-exact-control-record-binding-per-declared-archive','exec'),env)
qualified_route_records=env['qualified_route_records']

def checked_receipt(spec):
    path=Path(spec['path']);assert sha(path.read_bytes())==spec['sha256']
    value=load(path)
    for p,h in value['evidence'].items():assert sha(Path(p).read_bytes())==h
    assert value['original_failure_andall_rejections_verified']
    return value

def reject_with_receipt(source_files,current_files,receipt):
    old=checked_receipt(receipt['prior_receipt'])
    mappings={'/data/SC0.DK4':prior.qualified_source_records(source_files['/data/SC0.DK4'],current_files['/data/SC0.DK4'],old)}
    extra=[]
    for route in receipt['additional_routes']:
        path=route['file_path'];assert path in source_files and path not in mappings
        mappings[path]=qualified_route_records(source_files[path],current_files[path],route)
        extra.extend(dict(file_path=path,block=b,target_index=i) for b,i in sorted(mappings[path]))
    adapters={}
    for path,mapping in mappings.items():
        namespace={**original.story_percent_findings.__globals__,'source_records':mapping}
        exec(compile(prior.SOURCE,__file__+'::unchanged-detector-exact-per-archive-source-records','exec'),namespace)
        adapters[path]=namespace['story_percent_findings']
    def findings(source,current):
        for path,adapter in adapters.items():
            if source is source_files[path] and current is current_files[path]:return adapter(source,current)
        return original.story_percent_findings(source,current)
    guard=FunctionType(original.reject_story_percent_commands.__code__,
        {**original.reject_story_percent_commands.__globals__,'story_percent_findings':findings})
    report=guard(source_files,current_files)
    mapping=mappings['/data/SC0.DK4']
    report.update(exact_source_bound_relocated_leading25_count=len(mapping),
        relocated_source25_records=[dict(block=b,target_index=i) for b,i in sorted(mapping)],
        original_four_archive_printf_checks_and_nonleading_rejections_preserved=True,
        checked_detector_source_sha256=sha(prior.SOURCE.encode('utf-8')),
        exact_prior_relocation_receipt=receipt['prior_receipt'],
        additional_exact_source_bound_relocated_leading25_count=len(extra),additional_relocated_source25_records=extra,
        total_exact_source_bound_relocated_leading25_count=sum(map(len,mappings.values())))
    return report

def bind_registered_story_percent_guard(spec):
    receipt=checked_receipt(spec)
    def guard(source_files,current_files):
        report=reject_with_receipt(source_files,current_files,receipt)
        report['exact_relocation_receipt']=spec
        return report
    return guard
