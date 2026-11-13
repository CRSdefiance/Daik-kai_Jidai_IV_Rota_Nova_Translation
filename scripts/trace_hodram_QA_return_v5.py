"""Read original VM dispatch boundaries around the reproducible QA return fault."""
from scripts.run_reviewed_dialogue_fixture_v3 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{
    "[(0x548A8,'modal_entry'),(0x54924,'modal_paint')]":
        "[(0x548A8,'modal_entry'),(0x54924,'modal_paint'),(0x2A510,'vm_command')]",
    'if offset==0x548A8:':'if offset in (0x548A8,0x2A510):',
    "    env={**original.__dict__,'EXPECTED_FE_BODIES':fixture['expected_FE_bodies_hex']}":
        '''    adapter=checked_text(adapter,{
        "                r0,r1,r9=values[4],values[5],values[13]":
            """                r0,r1,r9=values[4],values[5],values[13]
                if target['name']=='vm_command':
                    if frame>=27000:
                        stream=struct.unpack('<I',memory(r1+4,4))[0]
                        row=dict(frame=frame,PC=values[2],kind='vm_command',CPU128_hex=cpu.hex(),
                            R0=r0,R1=r1,R2=values[6],SP=values[17],LR=values[18],
                            owner_32_hex=memory(r1,32).hex(),stream_pointer=stream,
                            command_32_hex=memory(stream,32).hex(),stack_96_hex=memory(values[17],96).hex(),
                            CPU_all4MiB_DTCM_ITCM_and_configuration_unchanged_by_callback=True)
                        self.rows.append(row)
                    assert ct.string_at(self.cpu,128)==cpu and ct.string_at(self.wram,0x400000)==raw
                    assert self.image.read(self.dtcm,0x4000)==dtcm and self.image.read(self.itcm,0x8000)==itcm
                    assert self.image.read(self.dtcm_base,4)==base_raw
                    return""",
        'if False:  # Existing native proof reused; no redundant full RAM files.':
            "if target['name']=='modal_paint' and frame>=27500:",
    })
    env={**original.__dict__,'EXPECTED_FE_BODIES':fixture['expected_FE_bodies_hex']}''',
    'per_page_full_RAM_files_omitted=True,':
        'per_page_full_RAM_files_omitted_except_final_risk_pages=True,original_VM_entry_trace_added=True,',
})
if __name__=='__main__':exec(compile(source,__file__+'::same-readonly-observer-additive-original-VM-boundaries','exec'),globals())
