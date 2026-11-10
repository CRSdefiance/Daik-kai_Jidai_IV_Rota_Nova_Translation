"""Derive exact B51 production references, including canonical-source lifecycles."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read, save

if __name__ == '__main__':
    root = Path('work/analysis/Hodram_B51_reference_binding_v8586')
    assert not root.exists()
    result = derive('dk4tool/patch/hodram_B50_references_v1.py', 'dk4tool/patch/hodram_B51_references_v1.py', {
        'B50': 'B51', 'hodram_B50_reconstruction_v1': 'hodram_B51_reconstruction_v1',
        "doc['blocks']==[50]": "doc['blocks']==[51]",
        "prior['block']==50": "prior['block']==51",
        'current[50],original[50]': 'current[51],original[51]',
        "target=reconstruct(old,japanese,group,prior,doc['records'],[])": "target=reconstruct(old,japanese,group,prior,doc['records'],source['operands_requiring_adjustment_when_resizing'])",
        "source['groups'][0]['all_original_source_commands']": "source['all_original_source_commands']",
        "len(group['command_map'])==12 and len(cleantexts)==len(oldtexts)==len(texts)==3": "len(group['command_map'])==20 and len(cleantexts)==len(oldtexts)==len(texts)==5",
        'all12 commands and3 speech identities': 'all20 commands and5 speech identities',
        "not group['relative_fixups'] and not group['relocated_skip_cases']": "len(group['relative_fixups'])==8 and sum(len(r['cases']) for r in group['relocated_skip_cases'])==40",
        'zero relative sites andno query ormenu': 'all eight relative sites/forty cases andno menu',
        "len({r['id'] for r in rows})==3": "len({r['id'] for r in rows})==5",
        'three disjoint canonical speech identities': 'five disjoint canonical speech identities',
        "reference_['block']==50": "reference_['block']==51",
        'block=50': 'block=51',
        'blocks[50]=target': 'blocks[51]=target',
        'a!=b]==[50]': 'a!=b]==[51]',
        'inverse[50]=old': 'inverse[51]=old',
        'editorial_references=3,speeches=3,typed_choices=0,commands=12,relative_sites=0': 'editorial_references=5,speeches=5,typed_choices=0,commands=20,relative_sites=8,query_sites=2',
    })
    from dk4tool.patch.hodram_B51_references_v1 import reconstruct_and_bind
    paths = dict(relocation='work/analysis/Hodram_B51_references_v8572/source_current_final_map.json',
        current='work/analysis/Hodram_B51_current_v8559/current_effective.json', source_controls='work/analysis/Hodram_B51_source_controls_v8555/source_controls.json')
    data = {key: read(path) for key, path in paths.items()}
    docpath = Path('translations/hodram_B51_editorial_manuscript_v5.json')
    doc = read(docpath)
    reference = NdsImage.open(doc['reference_ROM'])
    clean = NdsImage.open('work/clean.nds')
    def require(value, message):
        if not value:
            raise ValueError('B51 production reference: ' + message)
    positives = []
    for lifecycle in ['direct-current', 'canonical-source-current-ROM']:
        parent = NdsImage.open(doc['current_ROM'])
        if lifecycle == 'canonical-source-current-ROM':
            wrapper = NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
            wrapper.rom = deepcopy(parent.rom)
            parent = wrapper
        before = bytes(parent.rom.save())
        value = reconstruct_and_bind(parent, clean, reference, doc, data, require)
        assert bytes(parent.rom.save()) == before and value['target_archive'] == reference.read_file('/data/SC1.DK4')
        assert value['summary']['editorial_references'] == 5 and value['summary']['relative_sites'] == 8
        positives.append(dict(lifecycle=lifecycle, target_block_sha256=sha(value['target_block']), target_archive_sha256=sha(value['target_archive']),
            summary=value['summary'], caller_image_unchanged=True, atomic_commits=0))
    assert positives[0]['target_archive_sha256'] == positives[1]['target_archive_sha256']
    root.mkdir(parents=True)
    save(root / 'production_reference_binding.json', dict(derivation=result, positive_lifecycles=positives,
        all_five_source_current_final_refs_all20commands8relatives2queries_andunowned_files_components_bound=True,
        complete_source_current_block_archive_andwhole_inmemory_ROM_inverses_exact=True,
        no_source_path_shortcut_orpartial_files_only_ROM_lifecycle=True, no_ROM_write_atomic_commit_orcompletion_credit=True,
        new_credit=0, full_goal_complete=False, evidence={str(p): sha(Path(p).read_bytes()) for p in [*paths.values(), docpath, Path(__file__), Path('dk4tool/patch/hodram_B51_references_v1.py')]}))
    print('B51 production references: five exact source/current/final identities, all20commands/eight relatives/two queries and whole-image inverses pass in both lifecycles; zero ROM commits.')
