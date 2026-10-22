"""Three source-verified opcode slots sharing one unchanged original handler."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts import observe_graphic_paints_v669 as parent
from scripts.verify_village_wrap_v608 import read, save


class Observer(parent.Observer):
    def __init__(self, core, folder, capacity=500000):
        super().__init__(core, folder, capacity)
        indices = sorted({target['instruction_index'] for target in self.source['targets']})
        assert indices == [0x921, 0x927, 0x92F]
        self.extra_slots = []
        for index in indices:
            slot = core._handle + self.source['interpreter_table']['RVA'] + index * 8
            if slot != self.slot:
                assert self.image.qword(slot) == self.original
                self.extra_slots.append({'index': index, 'slot': slot, 'original_handler': self.original})

    def install(self):
        super().install()
        for item in self.extra_slots:
            assert self.image.qword(item['slot']) == self.original
            self.native.pointer(item['slot'], self.code_address)

    def close(self):
        if not self.closed:
            for item in self.extra_slots:
                self.native.pointer(item['slot'], self.original)
        super().close()
        assert all(self.image.qword(item['slot']) == self.original for item in self.extra_slots)

    def save(self):
        super().save()
        path = self.folder / 'paint_observer.json'
        value = read(path)
        value.update(additional_host_slots=self.extra_slots,
                     all_three_original_slot_pointers_restored_before_filter_free=True,
                     private_wrapper_sha256=sha(Path(__file__).read_bytes()))
        save(path, value)
