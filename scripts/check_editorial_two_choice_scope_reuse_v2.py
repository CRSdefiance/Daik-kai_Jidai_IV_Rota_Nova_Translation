"""Observe full original menu labels within the exact object, retaining native behavior."""
from scripts import check_editorial_two_choice_scope_reuse_v1 as prior
from scripts.check_editorial_compiled_pages_scope_reuse_v1 import qualified_current_native_context
from scripts.source_locked_derivation_v5118 import checked_text


def complete_bounded_label_reader(adapter):
    return checked_text(adapter,{
        "        label = bytes(cpu.mem_read(pointer, 32)).split(b'\\0')[0]":
        "        assert text <= pointer < text + len(object_bytes)\n        window = bytes(cpu.mem_read(pointer, text + len(object_bytes) - pointer))\n        assert b'\\0' in window\n        label = window.split(b'\\0')[0]",
    })


source=checked_text(prior.source,{
    "adapter=load(PRECEDENT)['source_owned_VM_adapter']":
        "adapter=complete_bounded_label_reader(load(PRECEDENT)['source_owned_VM_adapter'])",
    'source_owned_VM_adapter=adapter,':
        'source_owned_VM_adapter=adapter,observer_reads_complete_NUL_terminated_labels_within_original_object=True,no_native_provider_orcaption_wording_change=True,',
})
env={**vars(prior),**globals(),'__file__':__file__}
exec(compile(source,__file__+'::same-menu-VM-and-full-caption-pixels-object-bounded-observer','exec'),env)
