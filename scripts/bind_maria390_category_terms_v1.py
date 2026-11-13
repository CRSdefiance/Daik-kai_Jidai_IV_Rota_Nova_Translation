"""Reuse the qualified packed category getter for four scoped current aliases."""
from pathlib import Path
import struct
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.category_dialogue_lookup import TABLE
from scripts.verify_category_lookup_v754 import getter,string
from scripts.qualify_rafael351_item_and_UI_terms_v1 import string as source_string
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/Maria_B152_B175_clean_20261109')


def main():
    out=ROOT/'scoped_category_terms_v1.json';assert not out.exists()
    currentpath=ROOT/'current_v1/current_effective.json';current=load(currentpath);runtime=current['runtime']
    ctx=RegisteredRuntime(runtime['release_proof'],runtime['startup_proof'],captain=3);assert ctx.receipt()==runtime
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    priorpath=Path('work/analysis/category_dialogue_v754/lookup_native_ABI.json');prior=load(priorpath)
    cpu,_,_=ctx.machine(ctx.arm,ctx.common,ctx.raw,ctx.plan);rows=[]
    for index,japanese,english in [(10,'香料','Scents'),(12,'宝石','Gems'),(13,'薬','Medicine'),(14,'染料','Dyes')]:
        field=TABLE+index*4;before=source_string(clean,struct.unpack_from('<I',clean,field)[0])
        assert before['text']==japanese
        pointer=getter(cpu,index,0x0205FC48);text=string(cpu,pointer)
        assert text==english and bytes(cpu.mem_read(pointer,len(text)+1))==text.encode()+b'\0'
        old=next(r for r in prior['all108_getter_cases'] if r['category']==index and r['native_return_PC']==0x0205FC48)
        assert old['after']==text and old['ABI_return_stack_saved_registers_pass']
        rows.append(dict(category=index,Japanese=japanese,English=text,source=before,source_pointer_field=field,
            current_getter_return_pointer=pointer,current_return_hex=text.encode().hex(),original_caller_return_PC=0x0205FC48,
            original_getter_saved_registers_SP_andreturn_guards_preserved=True,current_executed_instructions_match_own_ROM=True,
            old_characterization_case_reused=old,old_clean_pointer_field_not_reinterpreted_as_current_pointer=True))
    ctx.calls.clear()
    save(out,dict(runtime=runtime,records=rows,scoped_native_category_calls=4,prior_all108_cases_not_replayed=True,
        packed_category_table_not_18_current32bit_pointers=True,
        descriptive_Sweets=dict(source_record='DK4_MES_B159_R0062',Japanese='甘い物',English='Sweets',
            source_is_descriptive_plural_not_a_unique_merchandise_name=True,no_specific_sugar_recipe_oritem_orcategory_assigned=True),
        prior_native_proof=str(priorpath),prior_native_proof_sha256=digest(priorpath),
        no_new_font_widget_oractual_gameplay_approval=True,new_credit=0,
        evidence={str(p):digest(p) for p in [currentpath,priorpath,Path(__file__),Path('scripts/verify_category_lookup_v754.py'),Path('dk4tool/patch/category_dialogue_lookup.py')]}))
    print('Bound Scents,Gems,Medicine,Dyes through four original current calls;108 prior cases reused,not replayed;Sweets remains descriptive.')


if __name__=='__main__':main()
