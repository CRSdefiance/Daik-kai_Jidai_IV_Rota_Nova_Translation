"""Probe both original andrelocated declared endwords without assuming firstend==tail."""
from pathlib import Path
if __name__=='__main__':
    source=Path('scripts/prove_lil_B152_B154_ends_v3646.py');t=source.read_text(encoding='utf-8');changes=[('prepare_lil_B152_B154_research_v3640','prepare_lil_B155_research_v3682'),('lil_B152_B154_ends_v3646','lil_B155_ends_v3686'),('n==154','n==155'),('len(cases)==8 and sum(not c[\'at_logical_tail\'] for c in cases)==2','len(cases)==4 and sum(not c[\'at_logical_tail\'] for c in cases)==2'),('eight_declared_end_decodes_and_all8_in_block_relative_destinations','four_declared_end_decodes_and_all29_in_block_relative_destinations'),('all8_declared_end_decodes','all4_declared_end_decodes'),('B154_first_end_precedes_second_end','B155_first_end_precedes_second_end'),('second_B154_declared_word','second_B155_declared_word'),('Eight declared current/target endwords','Four declared current/target endwords'),('B154 bothwords','B155 bothwords')]
    for a,b in changes:assert a in t,a;t=t.replace(a,b)
    exec(compile(t,str(source)+'::B155-both-declared-endwords','exec'),dict(__name__='__main__',__file__=__file__))
