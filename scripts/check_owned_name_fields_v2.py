"""Check complete reviewed owner groups using unchanged native name/font consumers."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(Path('scripts/check_owned_name_fields.py').read_text(encoding='utf-8'), {
    'from dk4tool.patch.owned_name_fields_v2 import plan_arm9_name_fields':
    'from dk4tool.patch.owned_name_fields_v3 import plan_arm9_name_fields',
    "actors=sorted({r['actor'] for r in proposal['fields']})":
    "actors=sorted({o['actor'] for r in proposal['fields'] for o in r['owners']})",
    "if field['actor']==row['actor_ID']:wanted=wanted.replace(field['current_text'],field['target_text'])":
    "if row['actor_ID'] in {o['actor'] for o in field['owners']}:wanted=wanted.replace(field['current_text'],field['target_text'])",
    "'control-target','unreviewed']":
    "'control-target','unreviewed','missing-alias-review','unreviewed-alias','wrong-clean-alias','wrong-alias-field','duplicate-alias']",
    "        else:f['review']['source']=False":
    """        elif kind=='missing-alias-review':f['reviewed_aliases']=[]
        elif kind=='unreviewed-alias':f['reviewed_aliases'][0]['review']['localization']=False
        elif kind=='wrong-clean-alias':f['reviewed_aliases'][0]['source_clean_component']['hex']='00'
        elif kind=='wrong-alias-field':f['reviewed_aliases'][0]['table_field_offset']+=4
        elif kind=='duplicate-alias':f['reviewed_aliases'].append(deepcopy(f['reviewed_aliases'][0]))
        else:f['review']['source']=False""",
    "Path('dk4tool/patch/owned_name_fields_v2.py'),Path(__file__)":
    "Path('dk4tool/patch/owned_name_fields_v2.py'),Path('dk4tool/patch/owned_name_fields_v3.py'),Path(__file__)",
})
exec(compile(source, __file__ + '::same-native-cases-complete-reviewed-owner-groups', 'exec'), globals())
