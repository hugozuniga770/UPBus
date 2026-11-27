"""El panel Demo de punta a punta (T23): un bus simulado que ve cualquier estudiante."""
from playwright.sync_api import expect

from e2e import datos


def test_el_panel_demo_mueve_un_bus_simulado(abrir_como):
    hugo = abrir_como(datos.HUGO, celular=False)
    hugo.goto("/demo")
    hugo.get_by_label("Escenario").select_option(label="Recorrido")
    hugo.get_by_label("Ruta").select_option(label="Ruta Sur")
    hugo.get_by_label("Velocidad (veces más rápido que el real)").fill("60")
    hugo.get_by_role("button", name="Iniciar simulación").click()

    simulacion = hugo.get_by_role("listitem").filter(has_text="Recorrido · Ruta Sur · ×60")
    expect(simulacion).to_contain_text("En curso")
    # La base es nueva: el panel carga el recorrido grabado de la Ruta Sur (C-37).
    expect(simulacion).to_contain_text("Se cargó el recorrido grabado")

    ana = abrir_como(datos.ANA)
    ana.goto("/rutas")
    ana.get_by_role("button", name="Sur", exact=True).click()
    expect(ana.get_by_text("🧪 Bus simulado · última señal", exact=False)).to_be_visible()

    simulacion.get_by_role("button", name="Detener").click()
    expect(simulacion).to_contain_text("Detenida")
