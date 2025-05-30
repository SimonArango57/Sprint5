import logging

# --- Configuracion del Logging ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='clinica_veterinaria.log',
    filemode='a'
)

# --- Definicion de Clases ---

class Dueno:
    """Representa a un dueño de mascota."""
    def __init__(self, nombre, telefono, direccion):
        self.nombre = nombre
        self.telefono = telefono
        self.direccion = direccion

    def __str__(self):
        """Devuelve una representacion legible del objeto Dueño."""
        return f"Nombre: {self.nombre}, Telefono: {self.telefono}, Direccion: {self.direccion}"

class Mascota:
    """Representa a una mascota."""
    def __init__(self, nombre, especie, raza, edad, dueno):
        if not isinstance(edad, int) or edad < 0:
            raise ValueError("La edad debe ser un numero entero positivo.")
        self.nombre = nombre
        self.especie = especie
        self.raza = raza
        self.edad = edad
        self.dueno = dueno  # Aqui guardamos una referencia al objeto Dueño

    def __str__(self):
        """Devuelve una representacion legible del objeto Mascota."""
        return (f"Nombre: {self.nombre}, Especie: {self.especie}, Raza: {self.raza}, Edad: {self.edad} años\n"
                f"  Dueño: {self.dueno.nombre} (Tel: {self.dueno.telefono})")

class Consulta:
    """Representa una consulta veterinaria."""
    def __init__(self, fecha, motivo, diagnostico, mascota):
        self.fecha = fecha
        self.motivo = motivo
        self.diagnostico = diagnostico
        self.mascota = mascota  # Aqui guardamos una referencia al objeto Mascota

    def __str__(self):
        """Devuelve una representacion legible del objeto Consulta."""
        return (f"Fecha: {self.fecha}\n"
                f"  Mascota: {self.mascota.nombre} (Dueño: {self.mascota.dueno.nombre})\n"
                f"  Motivo: {self.motivo}\n"
                f"  Diagnostico: {self.diagnostico}")

# --- Listas para almacenar los objetos ---

duenos_registrados = []
mascotas_registradas = []
consultas_registradas = []

# --- Funciones para la gestion de datos ---

def buscar_dueno_por_nombre(nombre_dueno):
    """Busca un objeto Dueño por su nombre."""
    for dueno in duenos_registrados:
        if dueno.nombre.lower() == nombre_dueno.lower():
            return dueno
    return None

def registrar_dueno():
    """Registra un nuevo objeto Dueño."""
    print("\n--- Registrar Dueño ---")
    nombre = input("Nombre del dueño: ").strip().title()
    telefono = input("Telefono del dueño: ").strip()
    direccion = input("Direccion del dueño: ").strip().title()

    # Verificar si el dueño ya existe por nombre y telefono
    dueno_existente = buscar_dueno_por_nombre(nombre)
    if dueno_existente and dueno_existente.telefono == telefono:
        print(f"El dueño '{nombre}' con telefono '{telefono}' ya esta registrado.")
        logging.info(f"Intento de registrar dueño existente: {nombre} ({telefono})")
        return dueno_existente

    nuevo_dueno = Dueno(nombre, telefono, direccion) # Crea un objeto Dueño
    duenos_registrados.append(nuevo_dueno)
    print(f"Dueño '{nombre}' registrado con exito.")
    logging.info(f"Dueño registrado: {nombre}")
    return nuevo_dueno

def buscar_mascota_por_nombre(nombre_mascota):
    """Busca objetos Mascota por su nombre."""
    mascotas_encontradas = [m for m in mascotas_registradas if m.nombre.lower() == nombre_mascota.lower()]
    return mascotas_encontradas

def registrar_mascota():
    """Registra un nuevo objeto Mascota y lo asigna a un Dueño."""
    print("\n--- Registrar Mascota ---")
    try:
        nombre_mascota = input("Nombre de la mascota: ").strip().title()
        especie = input("Especie de la mascota: ").strip().title()
        raza = input("Raza de la mascota: ").strip().title()
        
        edad_str = input("Edad de la mascota (años): ").strip()
        edad = int(edad_str)
        if edad < 0:
            raise ValueError("La edad no puede ser un número negativo.")

        nombre_dueno = input("Nombre del dueño de la mascota (si no existe, se creara): ").strip().title()

        dueno_asociado = buscar_dueno_por_nombre(nombre_dueno)
        if not dueno_asociado:
            print(f"El dueño '{nombre_dueno}' no esta registrado. Procediendo a registrarlo.")
            logging.warning(f"Dueño no encontrado para registrar mascota. Iniciando registro de dueño: {nombre_dueno}")
            dueno_asociado = registrar_dueno()
            if not dueno_asociado:
                print("No se pudo registrar al dueño, cancelando registro de mascota.")
                logging.error(f"Fallo al registrar dueño '{nombre_dueno}', registro de mascota cancelado.")
                return

        # Verificar si la mascota ya existe para el mismo dueño
        for m in mascotas_registradas:
            if m.nombre.lower() == nombre_mascota.lower() and m.dueno == dueno_asociado:
                print(f"La mascota '{nombre_mascota}' ya esta registrada con este dueño.")
                logging.info(f"Intento de registrar mascota existente: {nombre_mascota} (Dueño: {dueno_asociado.nombre})")
                return

        nueva_mascota = Mascota(nombre_mascota, especie, raza, edad, dueno_asociado) # Crea un objeto Mascota
        mascotas_registradas.append(nueva_mascota)
        print(f"Mascota '{nombre_mascota}' registrada con exito para {dueno_asociado.nombre}.")
        logging.info(f"Mascota registrada: {nombre_mascota} (Dueño: {dueno_asociado.nombre})")

    except ValueError as e:
        print(f"Error al registrar mascota: {e}. Por favor, verifique los datos ingresados.")
        logging.error(f"Error al registrar mascota: {e}", exc_info=True)
    except Exception as e:
        print(f"Ocurrio un error inesperado: {e}")
        logging.critical(f"Error inesperado en registrar_mascota: {e}", exc_info=True)


def registrar_consulta():
    """Registra un nuevo objeto Consulta para un objeto Mascota especifico."""
    print("\n--- Registrar Consulta ---")
    try:
        nombre_mascota = input("Nombre de la mascota para la consulta: ").strip().title()
        mascotas_disponibles = buscar_mascota_por_nombre(nombre_mascota)

        if not mascotas_disponibles:
            print(f"No se encontro ninguna mascota con el nombre '{nombre_mascota}'. Por favor, regístrela primero.")
            logging.warning(f"Intento de registrar consulta para mascota inexistente: {nombre_mascota}")
            return
        
        mascota_elegida = None
        if len(mascotas_disponibles) > 1:
            print(f"Se encontraron varias mascotas con el nombre '{nombre_mascota}':")
            for i, m in enumerate(mascotas_disponibles):
                print(f"{i+1}. Nombre: {m.nombre}, Especie: {m.especie}, Dueño: {m.dueno.nombre}")
            
            while True:
                try:
                    seleccion = int(input("Seleccione el número de la mascota correcta: ")) - 1
                    if 0 <= seleccion < len(mascotas_disponibles):
                        mascota_elegida = mascotas_disponibles[seleccion]
                        break
                    else:
                        print("Selección invalida. Intente de nuevo.")
                        logging.warning(f"Seleccion de mascota invalida durante el registro de consulta. Entrada: {seleccion+1}")
                except ValueError:
                    print("Entrada inválida. Por favor, ingrese un numero.")
                    logging.warning("Entrada no numerica para seleccion de mascota en registro de consulta.")
        else:
            mascota_elegida = mascotas_disponibles[0]

        if not mascota_elegida:
            print("No se pudo seleccionar una mascota para la consulta.")
            logging.error("Fallo al seleccionar mascota para la consulta.")
            return

        fecha = input("Fecha de la consulta (DD/MM/AAAA): ").strip()
        motivo = input("Motivo de la consulta: ").strip()
        diagnostico = input("Diagnostico: ").strip()

        nueva_consulta = Consulta(fecha, motivo, diagnostico, mascota_elegida) # Crea un objeto Consulta
        consultas_registradas.append(nueva_consulta)
        print(f"Consulta registrada con exito para '{mascota_elegida.nombre}'.")
        logging.info(f"Consulta registrada para: {mascota_elegida.nombre} (Fecha: {fecha})")

    except Exception as e:
        print(f"Ocurrio un error al registrar la consulta: {e}")
        logging.error(f"Error en registrar_consulta: {e}", exc_info=True)


def mostrar_mascotas():
    """Muestra todas las mascotas registradas usando su metodo __str__."""
    print("\n--- Listado de Mascotas ---")
    if not mascotas_registradas:
        print("No hay mascotas registradas aun.")
        logging.info("Intento de mostrar mascotas: No hay mascotas registradas.")
        return

    for mascota in mascotas_registradas:
        print(mascota) 
        print("-" * 30)
    logging.info("Mascotas listadas con exito.")

def ver_historial_consultas():
    """Muestra el historial de consultas de un objeto Mascota en particular."""
    print("\n--- Historial de Consultas de Mascota ---")
    try:
        nombre_mascota = input("Ingrese el nombre de la mascota para ver su historial: ").strip().title()
        mascotas_disponibles = buscar_mascota_por_nombre(nombre_mascota)

        if not mascotas_disponibles:
            print(f"No se encontro ninguna mascota con el nombre '{nombre_mascota}'.")
            logging.warning(f"Intento de ver historial de consulta para mascota inexistente: {nombre_mascota}")
            return
        
        mascota_elegida = None
        if len(mascotas_disponibles) > 1:
            print(f"Se encontraron varias mascotas con el nombre '{nombre_mascota}':")
            for i, m in enumerate(mascotas_disponibles):
                print(f"{i+1}. Nombre: {m.nombre}, Especie: {m.especie}, Dueño: {m.dueno.nombre}")
            
            while True:
                try:
                    seleccion = int(input("Seleccione el número de la mascota correcta: ")) - 1
                    if 0 <= seleccion < len(mascotas_disponibles):
                        mascota_elegida = mascotas_disponibles[seleccion]
                        break
                    else:
                        print("Seleccion invalida. Intente de nuevo.")
                        logging.warning(f"Seleccion de mascota invalida durante la visualizacion del historial. Entrada: {seleccion+1}")
                except ValueError:
                    print("Entrada invalida. Por favor, ingrese un numero.")
                    logging.warning("Entrada no numerica para seleccion de mascota en historial de consultas.")
        else:
            mascota_elegida = mascotas_disponibles[0]

        if not mascota_elegida:
            print("No se pudo seleccionar una mascota para ver su historial.")
            logging.error("Fallo al seleccionar mascota para ver historial de consulta.")
            return

        print(f"\n--- Historial de '{mascota_elegida.nombre}' (Dueño: {mascota_elegida.dueno.nombre}) ---")
        
        consultas_mascota = [c for c in consultas_registradas if c.mascota == mascota_elegida]

        if not consultas_mascota:
            print(f"No hay consultas registradas para '{mascota_elegida.nombre}' aun.")
            logging.info(f"No hay consultas registradas para {mascota_elegida.nombre}.")
            return

        for consulta in consultas_mascota:
            print(consulta) # Consulta se llama automaticamente
            print("-" * 20)
        logging.info(f"Historial de consultas listado para {mascota_elegida.nombre}.")

    except Exception as e:
        print(f"Ocurrio un error al ver el historial de consultas: {e}")
        logging.error(f"Error en ver_historial_consultas: {e}", exc_info=True)

# --- Menú Principal ---

def menu_principal():
    """Muestra el menu principal de la aplicacion."""
    logging.info("Inicio de la aplicacion Amigos Peludos")
    while True:
        print("\n--- Menu Principal Amigos Peludos ---")
        print("1. Registrar mascota")
        print("2. Registrar consulta")
        print("3. Listar mascotas")
        print("4. Ver historial de consultas de una mascota")
        print("5. Salir")

        opcion = input("Seleccione una opcion: ").strip()

        if opcion == '1':
            registrar_mascota()
        elif opcion == '2':
            registrar_consulta()
        elif opcion == '3':
            mostrar_mascotas()
        elif opcion == '4':
            ver_historial_consultas()
        elif opcion == '5':
            print("¡Gracias por preferir Amigos Peludos! Hasta pronto.")
            logging.info("Cierre de la aplicacion 'Amigos Peludos'.")
            break
        else:
            print("Opcion no valida. Por favor, intente de nuevo.")
            logging.warning(f"Opcion de menu invalida seleccionada: '{opcion}'")

# --- Ejecucion del programa ---
if __name__ == "__main__":
    menu_principal()