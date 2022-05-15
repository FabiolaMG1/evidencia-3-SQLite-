import datetime
import sqlite3
import sys
from sqlite3 import Error


def registrar1(articulos, opcion):
    global Nombre, fecha_converter
    fecha_registro = input("Dime una fecha (dd/mm/aaaa): ")
    fecha_converter = datetime.datetime.strptime(fecha_registro, "%d/%m/%Y").date()
    fecha_actual = datetime.datetime.combine(fecha_converter, datetime.datetime.min.time())
    Nombre = input("Digita el nombre del cliente: ")
    try:
        with sqlite3.connect("evidencia3.db") as conn:
            monto_total = 0
            print("Registrar")
            contador = max(articulos, default=0)+1
            while opcion != '0':
                mi_cursor = conn.cursor()

                descripcion = input(f"Escribe la descripcion del servicio {contador}: ")
                descripcionEq = input(f"Digita la descripcion del equipo: ")
                cantidad = int(input("Digita para cuantos equipos requieres el servicio: "))
                precio = float(input(f"Escribe el costo del servicio para cada equipo: $"))

                valores = {"folio": contador, "descripcion": descripcion,"cantidad": cantidad,
                        "precio": precio,"descripcion_eq":descripcionEq, "fecha_Registro": fecha_actual, "nombre":Nombre }#aqui agragar nombreC,desEq
                compra = (contador, descripcion.upper(), descripcionEq.upper(), cantidad, precio, cantidad*precio, fecha_converter,Nombre)

                monto_total = monto_total+cantidad*precio

                if contador in articulos:
                    articulos[contador].append(compra)
                    mi_cursor.execute("INSERT INTO ARTICULOS VALUES(:folio, :descripcion, :descripcion_eq, :cantidad, :precio)", valores)

                else:
                    articulos[contador] = []
                    articulos[contador].append(compra)
                    mi_cursor.execute("INSERT INTO VENTAS VALUES(:folio, :fecha_Registro, :nombre)", valores)
                    mi_cursor.execute("INSERT INTO ARTICULOS VALUES(:folio, :descripcion, :descripcion_eq, :cantidad, :precio)", valores)
                opcion = input("Escribe si deseas continuar (1-Continuar registrando/0-Dejar de registar: ")
            print(f"N° {contador}\t Cliente: {Nombre}\t Fecha: {fecha_converter}\n")
            print(f" SERVICIO\t EQUIPO\t PRECIO Y CANTIDAD\t SUBTOTAL")
            print("*"*80)
            for i in articulos[contador]:
                print(f"{i[1]}\t {i[2]}\t {i[3]}X ${i[4]}\t\t ${i[5]}\n")
            print("\nSubtotal: $",monto_total)
            Iva = monto_total*0.16
            print(f"El iva es de: ${Iva}")
            montoApagar = monto_total+Iva
            print(f"El monto total a pagar es de: ${montoApagar}")
            input("<<ENTER>>")
            print("Registro agregado exitosamente")
    except Error as e:
        print(e)
    except:
        print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
    finally:
        if (conn):
            conn.close()

    return articulos, opcion


def Consultar(articulos):
    total = 0
    print("\n\tConsulta tus ventas\n")
    buscar = int(input("Introduce el numero de venta a buscar: "))
    if buscar in articulos:
        c=0
        for consulta in articulos[buscar]:
            c += 1
            if c == 1:
                print(f"\n Cliente: {consulta[7]}\t Fecha: {consulta[6]}\n")
                print(f"FOLIO\t SERVICIO\t EQUIPO\t PRECIO Y CANTIDAD\t SUBTOTAL")
                print("*"*80)
            print(f"{consulta[0]}\t {consulta[1]}\t {consulta[2]}\t {consulta[3]}X ${consulta[4]}\t ${consulta[5]}\n")
            total = total+consulta[5]
        print("\nSubtotal: $",total)
        Iva = total*0.16
        print(f"El iva es de: ${Iva}")
        montoApagar = total+Iva
        print(f"El monto total a pagar es de: ${montoApagar}")
    else:
        print("\n\tNo se ha encontrado dicho numero de venta")
    input("<<ENTER>>")
    return articulos


def LeerFecha_SQL():
    separador = '*'
    print("\nConsulta de reportes\n")
    while True:
        try:
            fecha_consultar = input("Dime la fecha a buscar (dd/mm/aaaa): ")
            Fecha_consultar = datetime.datetime.strptime(fecha_consultar, "%d/%m/%Y").date()
            break
        except:
            print("Error al capturar la fecha, Vuelva capturar....")
    try:
        with sqlite3.connect("evidencia3.db", detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
            mi_cursor = conn.cursor()
            criterios = {"fecha": Fecha_consultar}
            mi_cursor.execute("SELECT v.ID_VENTAS,a.DESCRIPCION_SERV,a.DESCRIPCION_EQ,a.CANTIDAD,a.PRECIO,a.PRECIO*a.CANTIDAD AS TOTAL,v.FECHA,v.NOMBRE_CLIENTE FROM ARTICULOS as a,VENTAS as v WHERE a.ID_VENTAS=v.ID_VENTAS AND DATE(v.FECHA)=:fecha;", criterios)
            registros = mi_cursor.fetchall()
            print()
            print(f"FOLIO\t SERVICIO\t EQUIPO\t PRECIO X CANTIDAD\t SUBTOTAL\t IVA\t TOTAL\t FECHA\t CLIENTE\t ")
            print("*"*90)
            for folio, DescripcionS,DescripcionE, cantidad, precio, subtotal, fecha_registro, cliente in registros:
                print(f"{folio}\t {DescripcionS}\t {DescripcionE}\t {cantidad}x${precio}\t  ${subtotal}\t ${subtotal*.16}\t ${subtotal+(subtotal*.16)}\t {fecha_registro.strftime('%d/%m/%Y')}\t {cliente}")
    except sqlite3.Error as e:
        print(e)
    except Exception:
        print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
    finally:
        if (conn):
            conn.close()
            input("<<ENTER>>")


def LeerRangoFecha_SQL():
    separador = '*'
    print("\nConsulta de reportes\n")
    while True:
        try:
            fechai = input("Dime desde que fecha buscar (dd/mm/aaaa): ")
            fechaf = input("Dime hasta que fecha buscar (dd/mm/aaaa): ")
            reporte_fechai = datetime.datetime.strptime(fechai, "%d/%m/%Y").date()
            reporte_fechaf = datetime.datetime.strptime(fechaf, "%d/%m/%Y").date()
            break
        except:
            print("Error al capturar la fecha, Vuelva capturar....")
    try:
        with sqlite3.connect("evidencia3.db", detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
            mi_cursor = conn.cursor()
            criterios = {"fechaInicio": reporte_fechai, "fechaFin": reporte_fechaf}
            mi_cursor.execute("SELECT ID_VENTAS,NOMBRE_CLIENTE FROM VENTAS WHERE DATE(FECHA)<=:fechaFin and DATE(FECHA)>=:fechaInicio;", criterios)
            registros = mi_cursor.fetchall()
            print()
            print(f"FOLIO\t CLIENTE\t ")
            print("*"*30)
            for folio, cliente in registros:
                print(f"{folio}\t  {cliente}")
    except sqlite3.Error as e:
        print(e)
    except Exception:
        print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
    finally:
        if (conn):
            conn.close()
            input("<<ENTER>>")

def Leer_SQL(articulos):
    try:
        with sqlite3.connect("evidencia3.db", detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
            mi_cursor = conn.cursor()
            mi_cursor.execute("SELECT v.ID_VENTAS,a.DESCRIPCION_SERV,a.DESCRIPCION_EQ,a.CANTIDAD,a.PRECIO,a.PRECIO*a.CANTIDAD AS TOTAL,v.Fecha FROM ARTICULOS as a,VENTAS as v where a.ID_VENTAS=v.ID_VENTAS order by v.ID_ventas")
            registros = mi_cursor.fetchall()
            for registro in registros:
                if registro[0] in articulos:
                    articulos[registro[0]].append(registro)
                else:
                    articulos[registro[0]] = [registro]
    except Error as e:
        print(e)
    except:
        print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
    return articulos


articulos = {}
Leer_SQL(articulos)
while True:
    print("\n\tMenu prinicpal servicios tecnicos")
    print("1-Registrar una venta")
    print("2-Consultar una venta")
    print("3-Obtener un reporte de ventas para una Fecha en específico")
    print("4-Obtener folio y nombre de ventas en un rango de fechas")
    print("X-Salir ")
    opcion = input("Elige una opcion: ")
    if opcion == '1':
        registrar1(articulos, opcion)
    elif opcion == '2':
        Consultar(articulos)
    elif opcion == '3':
        LeerFecha_SQL()
    elif opcion == '4':
        LeerRangoFecha_SQL()
    elif opcion == 'X':
        print("\nSaliendo...\n")
        break
    else:
        print("\n\nError vuelve a intentarlo\n\n")
        input("<<ENTER>>")
