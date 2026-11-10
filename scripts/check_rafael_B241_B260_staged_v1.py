from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

parent = Path(__file__).with_name('check_rafael_B221_B240_staged_v1.py')
source = checked_text(parent.read_text(encoding='utf-8'), {
    'from scripts.plan_rafael_B221_B240_v1 import ROOT, STAGED, digest': "from scripts.draft_rafael_B249_B260_clean_v1 import OUT as ROOT\nfrom scripts.write_rafael_B221_B240_contextual_v1 import digest\nSTAGED = ROOT/'source_staged_layouts_v1.json'",
    "    'DK4_MES_B221_R0033':": "    'DK4_MES_B247_R0050': 'Charles signs the letter on its own row.',\n    'DK4_MES_B248_R0049': 'Jam signs the letter on its own row.',\n    'DK4_MES_B221_R0033':",
    'assert len(records) == 4':'assert len(records) == 2', '(912, 320)':'(912, 160)',
    'all_four_staged_pages.png':'two_staged_signatures.png', 'pages=4':'pages=2',
})
if __name__ == '__main__':
    exec(compile(source,__file__+'::two-progressive-letter-signatures','exec'),globals())
