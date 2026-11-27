"""Los chats de punta a punta (HU-14, HU-15): cada mensaje llega en vivo a la otra pantalla."""
from playwright.sync_api import expect

from e2e import datos


def test_el_chat_directo_llega_en_vivo_en_los_dos_sentidos(viaje_en_curso, abrir_como):
    valeria = abrir_como(datos.VALERIA)
    valeria.goto("/rutas")
    valeria.get_by_label("Tu parada").select_option(label="Sevilla")
    valeria.get_by_role("button", name="Voy a subir").click()
    expect(valeria.get_by_text("Vas a subir en Sevilla. El chofer ya lo sabe.")).to_be_visible()

    valeria.get_by_role("button", name="Chat con el chofer").click()
    chat_de_valeria = valeria.get_by_role("region", name="Chat con el chofer")
    chat_de_valeria.get_by_label("Mensaje para el chofer").fill("Ya estoy en la parada")
    chat_de_valeria.get_by_role("button", name="Enviar").click()
    expect(chat_de_valeria.get_by_text("Ya estoy en la parada")).to_be_visible()

    # Marco abre el chat de Valeria y ve su mensaje con su nombre (HU14-CA1).
    marco = viaje_en_curso
    marco.reload()
    marco.get_by_role("button", name="Chat con Valeria").click()
    chat_de_marco = marco.get_by_role("region", name="Chat con Valeria")
    expect(chat_de_marco.get_by_role("article").filter(has_text="Ya estoy en la parada")).to_contain_text("Valeria")

    # Responde con un botón rápido y a Valeria le llega sin recargar (HU14-CA3).
    chat_de_marco.get_by_role("button", name="Ya llego").click()
    expect(chat_de_valeria.get_by_role("article").filter(has_text="Ya llego")).to_contain_text("Marco")

    # Lo que escribe Valeria con el chat abierto también le llega a Marco en vivo.
    chat_de_valeria.get_by_label("Mensaje para el chofer").fill("Tengo polera azul")
    chat_de_valeria.get_by_role("button", name="Enviar").click()
    expect(chat_de_marco.get_by_text("Tengo polera azul")).to_be_visible()


def test_el_chat_de_la_ruta_llega_a_sus_miembros(abrir_como):
    rosa = abrir_como(datos.ROSA)
    rosa.goto("/rutas")
    chat_de_rosa = rosa.get_by_role("region", name="Chat de Ruta Norte")
    chat_de_rosa.get_by_role("button", name="Elegir Ruta Norte y abrir el chat").click()
    chat_de_rosa.get_by_placeholder("Escribe en la ruta").fill("¿Alguien más sube en Petrol?")
    chat_de_rosa.get_by_role("button", name="Enviar").click()
    expect(chat_de_rosa.get_by_text("¿Alguien más sube en Petrol?")).to_be_visible()

    # Ana elige la misma ruta, ve lo que ya se escribió y contesta (HU15-CA1).
    ana = abrir_como(datos.ANA)
    ana.goto("/rutas")
    chat_de_ana = ana.get_by_role("region", name="Chat de Ruta Norte")
    chat_de_ana.get_by_role("button", name="Elegir Ruta Norte y abrir el chat").click()
    expect(chat_de_ana.get_by_role("article").filter(has_text="¿Alguien más sube en Petrol?")).to_contain_text("Rosa")
    chat_de_ana.get_by_placeholder("Escribe en la ruta").fill("Yo, en cinco minutos")
    chat_de_ana.get_by_role("button", name="Enviar").click()

    # A Rosa le llega sin recargar.
    expect(chat_de_rosa.get_by_role("article").filter(has_text="Yo, en cinco minutos")).to_contain_text("Ana")
