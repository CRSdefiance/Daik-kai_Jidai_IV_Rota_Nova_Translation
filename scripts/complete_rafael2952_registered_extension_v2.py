"""Reconcile the exact signature marker in the integrated copy using its final native proof."""
from scripts.complete_rafael2952_registered_extension_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text


source=checked_text(previous,{
    "        assert not any(v is True and 'pending' in k for k,v in row.items() if k!='registered_release_and_completion_credit_pending')":
        """        if row.get('source_signature_presentation_pending'):
            assert row['id']=='DK4_MES_B216_R0074' and row['kind']=='system-FE'
            native=load(conf['compiled_native'])
            signature=next(r for r in native['records'] if r['id']==row['id'])
            staged=signature['complete_native_English_display']['planned_native_row_comparison']
            assert signature['source_staged_FE'] and staged['complete_visible_row_origins_exact']
            assert staged['planned_visible_rows']==[[0,0,'Take care now.'],[12,36,'Jam Jack Ludwyan']]
            assert row['actual_utterance_observed_in_disclosed_fixture']
            row['source_signature_presentation_pending']=False
        assert not any(v is True and 'pending' in k for k,v in row.items() if k!='registered_release_and_completion_credit_pending')""",
})
if __name__=='__main__':
    exec(compile(source,__file__+'::same-once-only-credit-and-exact-verified-signature-marker','exec'),globals())

