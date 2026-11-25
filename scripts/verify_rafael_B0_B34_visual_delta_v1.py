"""Bind four fresh layouts to the exact baseline and pack all final pages once."""
from pathlib import Path
from types import FunctionType
from scripts import verify_rafael_B281_B300_visual_delta_v1 as previous
from scripts.plan_rafael_B0_B34_v1 import FORMATTING, ROOT


FINAL=ROOT/'final_native_pages_v1.json'
FINAL_SHEETS=ROOT/'body_review_sheets_v1'
DELTA=ROOT/'visual_delta_inputs_v1'
env={**vars(previous),'__file__':__file__,
    'ORIGINAL':ROOT/'initial_plan_v1/automatic_plans.json',
    'PLAN':ROOT/'refined_plan_v3/automatic_plans.json','FORMATTING':FORMATTING,
    'FIRST_NATIVE':ROOT/'native_pages_v1/compiled_native_pages.json',
    'DELTA':DELTA,'DELTA_MANUSCRIPT':DELTA/'changed_manuscript.json',
    'DELTA_PLAN':DELTA/'changed_plans.json','FRESH':ROOT/'visual_delta_native_v1/compiled_native_pages.json',
    'FINAL':FINAL,'SHEETS':ROOT/'visual_delta_sheets_v1'}
env['inputs']=FunctionType(previous.inputs.__code__,env)


if __name__=='__main__':
    FunctionType(previous.combine.__code__,env)()
    pack=FunctionType(previous.body.__code__,{**previous.body.__globals__,
        'read_image':lambda path,expected:previous.read_image(Path(path),expected)})
    pack(FINAL_SHEETS,FINAL)
