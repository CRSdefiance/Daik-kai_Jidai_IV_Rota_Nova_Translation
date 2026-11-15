"""Use the original clean parser;retain the rejected build-specific-parser attempt."""
from pathlib import Path


def main():
    target=Path('scripts/review_sighting_faction_grammar_v1098b.py')
    assert not target.exists()
    body=Path('scripts/review_sighting_faction_grammar_v1098.py').read_text(encoding='utf-8')
    body=body.replace('from dk4tool.rom.nds import NdsImage',
        'from dk4tool.rom.nds import NdsImage\nfrom dk4tool.script.common_message_table import common_message_entries')
    body=body.replace("originals=current_entries(clean.read_file('/COMMON/MESFILE.DK4'),clean.read_file('/__arm9__.bin'))",
        "originals=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),clean.read_file('/__arm9__.bin'))")
    body=body.replace("ROOT=Path('work/analysis/sighting_grammar_v1098')", "ROOT=Path('work/analysis/sighting_grammar_v1098b')")
    target.write_text(body,encoding='utf-8')
    print('Original clean-source parser selected;candidate hash guards remain unchanged.')


if __name__=='__main__':main()
