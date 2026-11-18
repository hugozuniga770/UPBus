# Padrón simulado

El padrón imita la lista de estudiantes de la UPB. UPBus solo lo **lee** para validar el registro (BUS-RF-01); nunca lo modifica ni guarda contraseñas en él. El único módulo que lo lee es `cuentas/padron.py`, para que lo simulado quede aislado (BUS-RC-04).

| Archivo | Qué tiene | ¿Se sube a GitHub? |
|---|---|---|
| `padron.json` | Datos **de ejemplo**: los integrantes con códigos 70001 a 70003, como administradores, Ismael (70004) y una persona ficticia inactiva (70005) | Sí |
| `padron.local.json` | La lista **real** de la clase, creada con `importar_padron` | **No.** Está en `.gitignore`, porque el repositorio es público |

Si existe `padron.local.json`, UPBus usa ese; si no, el de ejemplo. Las pruebas usan siempre `tests/datos/padron_de_prueba.json`.

## Cargar la lista de la clase

1. Descarga la lista de OneDrive como `.xlsx` (Archivo › Descargar una copia).
2. En la carpeta del proyecto:

   ```powershell
   python manage.py importar_padron "$HOME\Downloads\lista.xlsx" --administradores CODIGO_HUGO,CODIGO_SEBASTIAN,CODIGO_ANDRES
   ```

3. El comando busca las columnas «Código», «Nombre» (o «Nombres» y «Apellidos») y «Correo». Los correos que no son de la UPB (`@upb.edu`) se reemplazan por `<código>@upb.example`.

Cada integrante corre el comando en su computadora. El servidor de la demo también lo necesita.

## Formato

```json
{"codigo": "70004", "nombre": "Ismael", "correo": "ismael@upb.example", "rol": "estudiante", "activo": true}
```

`rol` es `estudiante` o `administrador`. Los choferes no están en el padrón: los crea un administrador (BUS-RF-04).
