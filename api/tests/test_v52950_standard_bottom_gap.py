from pathlib import Path
ROOT=Path(__file__).parents[2]
HTML=(ROOT/'api'/'frontend'/'index.html').read_text(encoding='utf-8')

def test_v52950_version_launcher():
    assert (ROOT/'VERSION_DEMO.txt').read_text(encoding='utf-8').strip()=='V52.9.102'
    launchers=list(ROOT.glob('*LANCER_ALLROADS*.bat'))
    assert len(launchers)==1 and launchers[0].name=='AA_LANCER_JEPALYS.bat'

def test_v52950_standard_bottom_gap():
    assert 'id="allroads-v52950-standard-bottom-gap"' in HTML
    assert '--ar-panel-bottom-gap:6px' in HTML
    for state in ('prepare','ready','driving'):
        assert f'data-state="{state}"' in HTML
    assert 'align-content:end!important' in HTML

def test_v52950_critical_panels_not_forced_into_standard_gap_selector():
    block=HTML.split('id="allroads-v52950-standard-bottom-gap"',1)[1].split('</style>',1)[0]
    assert 'data-state="incident"' not in block
    assert 'data-state="turnaround"' not in block
