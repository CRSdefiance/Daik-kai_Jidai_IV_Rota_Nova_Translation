"""Distinguish the exact Hamburg parity guard from an extra visible FE row."""
from scripts import check_rafael_B261_B280_stored_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text


source = checked_text(previous.source, {
    "                        rendered['planned_native_row_comparison']=check_FE_rows(expanded,rendered)":
        """                        if text['id']=='DK4_MES_B276_R0047':
                            assert expanded==b'Your share in Hamburg rose slightly! '
                            assert text['parity_space_added'] and rendered['complete_consumed_bytes']==len(expanded)
                            assert rendered['input_bitmap_header_view_context_canaries_andcomplete_return_exact']
                            assert rendered['events'][-2:]==[dict(kind='ascii',code=32,style=15,x=x,y=12) for x in (0,6)]
                            assert rendered['events'][:-2]==old['events']
                            assert rendered['physical']==Path(old['native_plane']).read_bytes()
                            assert rendered['logical']==Path(old['native_logical_plane']).read_bytes()
                            rendered['planned_native_row_comparison']=check_FE_rows(expanded[:-1],
                                {**rendered,'events':rendered['events'][:-2]})
                            rendered['planned_native_row_comparison']['compiler_parity_and_native_wrap_guard_are_zero_ink']=True
                        else:
                            rendered['planned_native_row_comparison']=check_FE_rows(expanded,rendered)""",
})

if __name__ == '__main__':
    parent = previous.previous
    storage = dict(parent.compound_storage.__globals__)
    exec(compile(parent.storage, __file__ + '::same-compound-storage', 'exec'), storage)
    env = {**parent.prior.env, 'compound_storage': storage['compound_storage'],
           'MACROS': previous.MACROS, '__file__': __file__, '__name__': 'stored_B261_B280'}
    exec(compile(source, __file__ + '::exact-zero-ink-parity-scope', 'exec'), env)
    env['main']()
