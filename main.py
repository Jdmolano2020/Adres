from sql_app import crud
from sql_app.database import SessionLocal
from sql_app.schemas import Persona, PersonaIncial


def leer_personas(skip: int = 0, limit: int = 100):
    try:
        db = SessionLocal()
        personas = crud.get_personas(db, skip=skip, limit=limit)
        return personas
    finally:
        db.close()


def leer_persona(id_registro: int):
    try:
        db = SessionLocal()
        persona = crud.get_persona(db, id_registro=id_registro)
        return persona
    finally:
        db.close()


def borar_persona(id_registro: int):
    try:
        db = SessionLocal()
        borrado = crud.delete_persona(db, id_registro=id_registro)
        if borrado:
            print("Borrado Exitoso")
    finally:
        db.close()


def crear_persona(nueva_persona: Persona):
    try:
        db = SessionLocal()
        persona = crud.create_persona(db, persona=nueva_persona)
        return persona
    finally:
        db.close()


def actualizar_persona(id_registro: int, actual_persona: Persona):
    try:
        db = SessionLocal()
        persona = crud.update_persona(
            db, id_registro, nueva_persona=actual_persona)
        return persona
    finally:
        db.close()


nuevo = PersonaIncial(
    id_fuente=1,
    codigo_unico_fuente=1,
    documento="9397047",
    primer_nombre="JUAN",
    segundo_nombre="DANIEL",
    primer_apellido="MOLANO D",
    segundo_apellido="CASTRO",
    sexo="Hombre",
    edad=50,
    fecha_nacim_anio_=1972,
    fecha_nacim_mes_=9,
    fecha_nacim_dia_=8,
    etnia=None,
    fecha_ocur_anio_=None,
    fecha_ocur_mes_=None,
    fecha_ocur_dia_=None,
    codigo_dane_departamento_=None,
    departamento=None,
    codigo_dane_municipio_=None,
    municipio=None,
    pre_resp_farc=None,
    pre_resp_eln=None,
    pre_resp_gg=None,
    pre_resp_param=None,
    pre_resp_bc=None,
    pre_resp_fp=None,
    pre_resp_ae=None,
    DF_=None,
    SE_=None,
    RU_=None,
    in_=None)
# print("Insertar Persona")
# crear_persona(nuevo)
# print("Tabla Personas")
# personas = leer_personas()
# print(type(personas))
# for persona in personas:
#    print(persona)
# actualizar_persona(57, nuevo)
print("Registro Persona")
persona = leer_persona(57)
print(persona)
borar_persona(57)
