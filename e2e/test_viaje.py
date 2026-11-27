"""El viaje en vivo de punta a punta: el bus en el mapa y «Voy a subir» (HU-05 a HU-07).

Marco ya inició su viaje de la Ruta Norte (fixture `viaje_en_curso`) y su
pantalla sigue abierta, compartiendo el GPS del bus.
"""
from playwright.sync_api import expect

from e2e import datos


def test_el_estudiante_ve_el_bus_en_vivo(viaje_en_curso, abrir_como):
    ana = abrir_como(datos.ANA)
    ana.goto("/rutas")

    expect(ana.get_by_text("🚌 Bus en vivo · última señal", exact=False)).to_be_visible()
    expect(ana.get_by_text("Viaje de las 06:40 · en curso")).to_be_visible()


def test_el_chofer_ve_en_vivo_quien_va_a_subir(viaje_en_curso, abrir_como):
    marco = viaje_en_curso
    marco.reload()
    van_a_subir = marco.get_by_role("listitem").filter(has_text="Ana · ")
    expect(van_a_subir).to_have_count(0)

    ana = abrir_como(datos.ANA)
    ana.goto("/rutas")
    ana.get_by_label("Tu parada").select_option(label="Petrol")
    ana.get_by_role("button", name="Voy a subir").click()
    expect(ana.get_by_text("Vas a subir en Petrol. El chofer ya lo sabe.")).to_be_visible()

    # Le llega a Marco sin recargar, por su canal privado (HU07-CA1).
    expect(marco.get_by_text("Ana va a subir en Petrol", exact=False)).to_be_visible()
    expect(van_a_subir).to_contain_text("Ana · Petrol")

    # Ana cancela antes de que pase el bus y desaparece de la lista de Marco (HU07-CA4).
    ana.get_by_role("button", name="Cancelar").click()
    expect(ana.get_by_role("button", name="Voy a subir")).to_be_visible()
    expect(van_a_subir).to_have_count(0)
