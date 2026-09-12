from pathlib import Path

def _html():
    return (Path(__file__).resolve().parents[1] / "frontend" / "index.html").read_text(encoding="utf-8")

def test_turnaround_click_opens_result_panel():
    html=_html()
    assert "document.getElementById('ar51-more')?.addEventListener" in html
    assert "ar52921OpenTurnaround();" in html
    assert "p.dataset.panel==='turnaround'" in html

def test_positive_zone_requires_forward_safe_access():
    html=_html()
    assert "Zone de retournement sûre disponible · 280 m" in html
    assert "devant le véhicule, avant le blocage" in html
    assert "accès validé en marche avant" in html
    assert "Bus 13 m / 19 t" in html
    assert 'id="ar51-guide-turnaround"' in html
    assert "Suivre vers la zone" in html

def test_positive_guidance_and_recalculation_keep_safety_contract():
    html=_html()
    assert "Continuez en marche avant · zone sûre avant le blocage" in html
    assert "Zone atteinte · recalculer le trajet" in html
    assert "Trajet recalculé · blocage exclu" in html
    assert "blockage_excluded:true" in html
