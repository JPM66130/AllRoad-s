from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
HTMLS=[ROOT/'frontend'/'index.html', ROOT/'api'/'frontend'/'index.html']

def test_v52936_report_is_between_stats_and_driving_actions():
    for p in HTMLS:
        s=p.read_text(encoding='utf-8')
        driving=s.split('data-panel="driving"',1)[1].split('data-panel="incident"',1)[0]
        assert driving.index('class="ar51-stats"') < driving.index('id="ar52934-incident-report"') < driving.index('class="ar51-driving-actions"')
        assert 'class="ar52936-report-square"' in driving
        assert '📋 Rapport d’incident</button>' not in driving

def test_v52936_landscape_has_five_non_overlapping_grid_cells():
    for p in HTMLS:
        s=p.read_text(encoding='utf-8')
        assert 'grid-template-columns:112px minmax(205px,.72fr) 38px minmax(300px,1.25fr) minmax(72px,.34fr)!important' in s
        assert '.ar52936-return{position:static!important' in s
        assert '.ar52936-report-square{width:38px!important;height:38px!important' in s

def test_v52936_ready_indicator_is_discrete_checkmark():
    for p in HTMLS:
        s=p.read_text(encoding='utf-8')
        assert 'class="ar52936-report-ready"' in s
        assert '.ar52936-report-square.has-report .ar52936-report-ready{display:block}' in s

def test_v52936_version_and_launcher():
    assert (ROOT/'VERSION_DEMO.txt').read_text(encoding='utf-8').strip() == 'V52.9.102'
    launchers=list(ROOT.glob('*LANCER_ALLROADS_V52_9_*.bat'))
    assert len(launchers)==1
    assert launchers[0].name=='AA_LANCER_JEPALYS.bat'


def test_v52937_portrait_two_row_layout():
    html=(ROOT/'frontend/index.html').read_text(encoding='utf-8')
    assert 'allroads-v52937-portrait-driving-bar' in html
    assert 'grid-template-rows:48px 54px' in html
    assert '.ar52936-report-square{grid-column:1!important;grid-row:2!important' in html
    assert '.ar51-driving-actions{grid-column:2 / 6!important;grid-row:2!important' in html
    assert '.ar52936-return{grid-column:6!important;grid-row:2!important' in html
    assert 'max-height:150px!important;height:150px!important' in html
