from pathlib import Path
HTML = Path(__file__).resolve().parents[1] / 'frontend' / 'index.html'
def html(): return HTML.read_text(encoding='utf-8')
def test_v52930_profile_selection_persists_on_home_return():
    s=html()
    assert 'function restoreHomeSelection()' in s
    assert 'localStorage.getItem("allroads-start-profile")' in s
    assert 'restoreHomeSelection();' in s
    assert 'aria-current' in s
    assert "content:'✓  SÉLECTIONNÉ'" in s
    assert 'outline:4px solid #19a86f' in s
def test_v52930_vehicle_selection_is_stronger_and_persistent():
    s=html()
    assert 'rgba(20,145,112,.16)' in s
    assert 'allroads-vehicles-v52-active-' in s
    assert 'localStorage.setItem(activeKey(profile),id)' in s
    assert 'localStorage.getItem(activeKey(profile))' in s
