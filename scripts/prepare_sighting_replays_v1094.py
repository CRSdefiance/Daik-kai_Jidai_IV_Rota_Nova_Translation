"""Create explicit successors for terminal fixed-schedule encounter checks."""
from pathlib import Path


def main():
    source = Path('scripts/run_sighting_gameplay_v1093.py')
    target = Path('scripts/run_sighting_gameplay_v1094.py')
    assert not target.exists()
    body = source.read_text(encoding='utf-8')
    body = body.replace('sighting_gameplay_v1093_', 'sighting_gameplay_v1094_').replace(
        'sighting_v1093_1086_', 'sighting_v1094_1086_')
    before = "    assert not any('battle_fixture' in c for c in commands)\n"
    assert body.count(before) == 1
    body = body.replace(before, before + """    commands += [
        {'until':5110,'duration':1,'battle_fixture':{'sighting_context':'compassReady8'}},
        {'until':5210,'buttons':['B'],'duration':8},
        {'until':5310,'duration':1},
        {'until':5410,'duration':1},
        {'until':5510,'buttons':['A'],'duration':8},
        {'until':5610,'duration':1},
        {'until':5710,'buttons':['A'],'duration':8},
        {'stop':True}]
""")
    target.write_text(body, encoding='utf-8')
    source = Path('scripts/verify_sighting_compass_v1092.py')
    target = Path('scripts/verify_sighting_compass_v1094.py')
    assert not target.exists()
    body = source.read_text(encoding='utf-8')
    body = body.replace('sighting_compass_v1092', 'sighting_compass_v1094').replace(
        'sighting_v1088b_1086_compassReady8', 'sighting_v1094_1086_compassReady8').replace(
        'sighting_gameplay_v1088b_compassReady8', 'sighting_gameplay_v1094_compassReady8')
    body = body.replace("report['frames']==5610", "report['frames']==5710").replace(
        '((5210,614),(5310,614),(5410,1917),(5510,1917))',
        '((5310,614),(5410,614),(5510,1917),(5610,1917))').replace(
        '((5210,5310),(5410,5510))', '((5310,5410),(5510,5610))').replace(
        'raw[5610]', 'raw[5710]').replace("'terminal_frame':5610", "'terminal_frame':5710")
    target.write_text(body, encoding='utf-8')
    print('Created fixed-schedule replay and exact timing successor; original scripts preserved.')


if __name__ == '__main__':
    main()
