#Librerias
import arcpy
import os
from arcpy import env
from arcpy.sa import *

arcpy.env.overwriteOutput = True

# Script arguments
divipola = arcpy.GetParameterAsText(0)
escala = arcpy.GetParameterAsText(1)
fecha_toma = arcpy.GetParameterAsText(2)
dgn = arcpy.GetParameterAsText(3)
limite = arcpy.GetParameterAsText(4)
raster = arcpy.GetParameterAsText(5)
xyz = arcpy.GetParameterAsText(6)
curvas = arcpy.GetParameterAsText(7)
excel = arcpy.GetParameterAsText(8)
ruta_salida = arcpy.GetParameterAsText(9)

def generar_carpeta(divipola, escala, fecha_toma, dgn, limite, raster, xyz, curvas, excel, ruta_salida):
    arcpy.env.workspace = ruta_salida
    arcpy.env.overwriteOutput = True

    #diccionario para nombre de los archivos segun escala
    dic_nom = {'1000':'1',
               '2000':'2',
               '5000':'5',
               '10000':'10',
               '25000':'25',
               }

    #nombres de las carpetas
    nombre_folderp = 'MDT' + str(dic_nom[escala]) + '_' + str(divipola) + '_' + str(fecha_toma)
    nombre_folder_dgn = 'MDT' + str(dic_nom[escala]) + '_' + 'DGN' + '_' + str(divipola) + '_' + str(fecha_toma)
    nombre_folder_limite = 'MDT' + str(dic_nom[escala]) + '_' + 'LIMITE' + '_' + str(divipola) + '_' + str(fecha_toma)
    nombre_folder_xyz = 'MDT' + str(dic_nom[escala]) + '_' + 'XYZ' + '_' + str(divipola) + '_' + str(fecha_toma)
    nombre_folder_curvas = 'MDT' + str(dic_nom[escala]) + '_' + 'CURVAS_IMPARES' + '_' + str(divipola) + '_' + str(fecha_toma)

    #carpeta principal
    arcpy.management.CreateFolder(ruta_salida, nombre_folderp)

    #carpeta limite
    arcpy.management.CreateFolder(os.path.join(str(ruta_salida) ,str(nombre_folderp)), nombre_folder_limite)

    #curvas impares carpeta y shp
    if curvas != '':
        arcpy.management.CreateFolder(os.path.join(ruta_salida,nombre_folderp), nombre_folder_curvas)
        arcpy.management.Copy(curvas, os.path.join(ruta_salida,nombre_folderp, nombre_folder_curvas,nombre_folder_curvas))

    
    #nombres finales
    raster_final = os.path.join(str(ruta_salida) ,str(nombre_folderp), nombre_folderp)
    limite_final = os.path.join(str(ruta_salida) ,str(nombre_folderp), nombre_folder_limite, nombre_folder_limite)
    xyz_final = os.path.join(str(ruta_salida) ,str(nombre_folderp), nombre_folder_xyz)
    dgn_final = os.path.join(str(ruta_salida),nombre_folderp, nombre_folder_dgn)

    
    #copia y renombra
    arcpy.management.Copy(raster, raster_final)
    arcpy.management.Copy(limite, limite_final)
    arcpy.management.Copy(xyz, xyz_final)
    arcpy.management.Copy(dgn, dgn_final)

    #renombra archivos xyz
    directorio = os.path.join(str(ruta_salida),nombre_folderp, nombre_folder_xyz)
    contenido = os.listdir(directorio)
    archivos = []
    
    for archivo in contenido:
        archivos.append(archivo)

    os.rename(os.path.join(xyz_final,str(archivos[0])),os.path.join(xyz_final,nombre_folder_xyz + '.prj'))
    os.rename(os.path.join(xyz_final,str(archivos[1])),os.path.join(xyz_final,nombre_folder_xyz + '.txt'))
    os.rename(os.path.join(xyz_final,str(archivos[2])),os.path.join(xyz_final,nombre_folder_xyz + '.txt.xml'))
 

    #renombra archivos dgn
    directorio = os.path.join(str(ruta_salida),nombre_folderp, nombre_folder_dgn)
    contenido = os.listdir(directorio)
    archivos = []
    
    for archivo in contenido:
        archivos.append(archivo)

    n = len(archivos)
    
    if int(n) == 1:
        for a in archivos:
            os.rename(os.path.join(dgn_final,a),os.path.join(dgn_final,nombre_folder_dgn +'.dgn' ))
    else:
        for a in archivos:
            os.rename(os.path.join(dgn_final,a),os.path.join(dgn_final,nombre_folder_dgn + '_P'+str(int(archivos.index(a))+1) +'.dgn' ))
    
    #nombre excel
    final_excel = 'Verificacion_de_la_Precision_' + nombre_folderp

    #copia y renombra el excel
    arcpy.management.Copy(excel, os.path.join(ruta_salida,nombre_folderp,final_excel))
    
if __name__ == "__main__":
    arcpy.AddMessage('___________________________')
    arcpy.AddMessage('Verificando los datos ingresados')

    if len(fecha_toma) != 8:
        arcpy.AddMessage('LA FECHA DEBE CONTENER 8 CARACTERES EN FORMATO AAAAMMDD EJ. 04/JULIO/2023 --> 20230704')
    else:
        if escala == '1000' or escala == '2000':
            if len(divipola) != 8:
                arcpy.AddMessage('EL CODIGO DIVIPOLA DEBE CONTENER 8 CARACTERES PARA LA ESCALA SELECCIONADA')
            else:
                arcpy.AddMessage('Generando Carpetas')
                generar_carpeta(divipola, escala, fecha_toma, dgn, limite, raster, xyz, curvas, excel, ruta_salida)
                arcpy.AddMessage('Finalizado')
        else:
            if len(divipola) != 5:
                arcpy.AddMessage('EL CODIGO DIVIPOLA DEBE CONTENER 5 CARACTERES PARA LA ESCALA SELECCIONADA')
            else:
                arcpy.AddMessage('Generando Carpetas')
                generar_carpeta(divipola, escala, fecha_toma, dgn, limite, raster, xyz, curvas, excel, ruta_salida)
                arcpy.AddMessage('finalizado')
