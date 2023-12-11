# ---------------------------------------------------------------------------
# Direccion de Gestión de la Información Geografica
# Created on: 2023-05-24
# Created by: Michael Rojas - Diego Rugeles (Supervisor Desarrollo DGIG)
# # Usage: DataReviwer ArcGIS Pro  - GDB 2.4- 2.5  Detección de vectores duplicados en captura DGN
# Description:
# Herramienta usada para obtener vectores duplicados en captura de datos DGN
# ---------------------------------------------------------------------------
# Importar modulo arcpy
import arcpy
import os
#Parameters


## Operadores logicos

# Iteradores

DGN_Entrada = arcpy.GetParameterAsText(0) #DGN de entrada
Ruta_Salida = arcpy.GetParameterAsText(1) #Ruta de salida
R1 = arcpy.GetParameterAsText(2) #Exportar DGN
#arcpy.env.overwriteOutput = True

#Funciones -------------------------------------------------------------------------------------------------------------------------------------------------------

def CAD_to_GDB(DGN_Entrada, Ruta_Salida):
    gdb = arcpy.management.CreateFileGDB(Ruta_Salida, 'Vectores_GDB')
    cad= arcpy.conversion.CADToGeodatabase(DGN_Entrada, gdb, 'Vectores_GDB', '10000', 'PROJCS["MAGNA-SIRGAS_Origen-Nacional",GEOGCS["GCS_MAGNA",DATUM["D_MAGNA",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",5000000.0],PARAMETER["False_Northing",2000000.0],PARAMETER["Central_Meridian",-73.0],PARAMETER["Scale_Factor",0.9992],PARAMETER["Latitude_Of_Origin",4.0],UNIT["Meter",1.0]];-618700 -8436100 10000;-100000 10000;-100000 10000;0.001;0.001;0.001;IsHighPrecision')
    return cad

def GDB_to_CAD(Ruta_Salida):
    # Obtener la capa "ErrorDuplicado" en la geodatabase
    GDB_Entrada = os.path.join(Ruta_Salida, "Vectores_Duplicados.gdb", "ErrorDuplicado")
    
    # Ruta salida
    dgn_duplicado = os.path.join(Ruta_Salida, "DGN_Salida.dgn")

    # Crear una copia de la capa "ErrorDuplicado" en un archivo DGN, con la ruta de semilla especifica
    arcpy.conversion.ExportCAD(GDB_Entrada, "DGN_V8", dgn_duplicado, Seed_File=r"C:\Program Files\ArcGIS\Pro\Resources\ArcToolBox\Templates\CAD\template3d_Metric.dgn")

    return dgn_duplicado

################################

if __name__=='__main__':

    DGN = CAD_to_GDB(DGN_Entrada, Ruta_Salida)
    arcpy.env.workspace = os.path.join(Ruta_Salida,"Vectores_GDB.gdb")
    arcpy.AddMessage("\n--------------------------------------------------------------")
    arcpy.AddMessage("Creando GDB para almacenar duplicados")

    gdb = arcpy.management.CreateFileGDB(Ruta_Salida, 'Vectores_Duplicados')
    fds = arcpy.management.CreateFeatureclass(gdb, 'ErrorDuplicado',"POLYLINE")
    arcpy.management.AddField(fds, "ObjectID_Origen","LONG")
    arcpy.management.AddField(fds, "CATEGORIA","LONG")
    
    
    arcpy.AddMessage("\n--------------------------------------------------------------")
    arcpy.AddMessage("Ejecutando cursores")

    tabla_repetidos = arcpy.management.FindIdentical('Vectores_GDB/Polyline',os.path.join(Ruta_Salida, "Vectores_GDB.gdb/Tabla_repetidos"),"Shape")
    arcpy.management.JoinField('Vectores_GDB/Polyline', "OBJECTID",tabla_repetidos, "IN_FID","FEAT_SEQ")

     # Haciendo query dinamico -----------------------------------------------------------------------------------------------------------------------


    with arcpy.da.SearchCursor('Vectores_GDB/Polyline',["SHAPE@", "OID@","FEAT_SEQ"]) as cursor_1:
            for row in cursor_1:
                #arcpy.AddMessage("Analizando en el OID {0}".format(row[1]))
                with arcpy.da.SearchCursor('Vectores_GDB/Polyline',["SHAPE@","OID@","FEAT_SEQ"]) as cursor_2:
                    for row_2 in cursor_2: 
                        #arcpy.AddMessage("Error encontrado en el OID {0}".format(row_2[1]))
                        if(row[2] == row_2[2]  and  row[1] != row_2[1]):
                            arcpy.AddMessage("Error encontrado en el OID {0}".format(row_2[1]))
                            with arcpy.da.InsertCursor(os.path.join(Ruta_Salida, "Vectores_Duplicados.gdb","ErrorDuplicado"),["SHAPE@","ObjectID_Origen","CATEGORIA"]) as insertar:
                                row_list = list(row_2)
                                row_list[0] = row_2[0]
                                row_list[1] = row_2[1]
                                row=tuple(row_list)
                                insertar.insertRow(row)
        

    if R1 == 'true': # Exportar DGN
        arcpy.AddMessage("--------------------------------------------------------------")
        arcpy.AddMessage("Exportando duplicados a nuevo DGN")
        dgn_duplicado = GDB_to_CAD(Ruta_Salida)
        arcpy.AddMessage(f"Duplicados exportados a: {dgn_duplicado}")

    arcpy.AddMessage("\n--------------------------------------------------------------")
    arcpy.AddMessage("FINALIZADO")


 