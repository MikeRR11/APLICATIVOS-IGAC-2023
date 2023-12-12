import arcpy
import os 
# Crear GDB 
def crearGDB(path, GDB_name):
    GDB_output= arcpy.CreateFileGDB_management(out_folder_path=path,out_name=GDB_name)
    return GDB_output

#Convertir CAD a GDB: 
def convertirCADtoGDB(CAD, GDB, dataset_name):
    CAD = arcpy.conversion.CADToGeodatabase(input_cad_datasets=CAD, out_gdb_path=GDB, out_dataset_name=dataset_name, reference_scale=1000, spatial_reference='PROJCS["MAGNA-SIRGAS_Origen-Nacional",GEOGCS["GCS_MAGNA",DATUM["D_MAGNA",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",5000000.0],PARAMETER["False_Northing",2000000.0],PARAMETER["Central_Meridian",-73.0],PARAMETER["Scale_Factor",0.9992],PARAMETER["Latitude_Of_Origin",4.0],UNIT["Meter",1.0]];-618700 -8436100 10000;-100000 10000;-100000 10000;0.001;0.001;0.001;IsHighPrecision')
    return CAD 
#Crear feature class

#Filtros SQL
def Niveles_CNivel(lyr_poly):
    layercontoponimia=arcpy.management.SelectLayerByAttribute(lyr_poly,'NEW_SELECTION', where_clause="Level = 42 Or Level = 43 Or Level = 44 Or Level = 45")
    return layercontoponimia

if __name__ == "__main__":
    arcpy.AddMessage("Iniciando el proceso de revisión")
    dgn = arcpy.GetParameterAsText(0)
    curvas_impares = arcpy.GetParameterAsText(1)
    ruta_salida = arcpy.GetParameterAsText(2)
    arcpy.AddMessage("Creando GDBs de trabajo")
    gdb_curvas = crearGDB(ruta_salida, "Curvas_DGN")
    gdb_errores = crearGDB(ruta_salida, "Errores_Curvas")
    dataset_name = "validacion_CNImpares"
    arcpy.AddMessage("Migrando DGN a GDB")
    convertirCADtoGDB(dgn, gdb_curvas, dataset_name)
    arcpy.env.workspace = os.path.join(ruta_salida,"Curvas_DGN.gdb")
    curvas_revisar  = arcpy.management.CopyFeatures(Niveles_CNivel('validacion_CNImpares\Polyline'), os.path.join(ruta_salida,"curvas_filtradas.shp"))
    arcpy.AddMessage("Validando Topologías")
    arcpy.analysis.Intersect([curvas_revisar,curvas_impares], os.path.join(ruta_salida,"Errores_Curvas.gdb\Errores"), output_type = "POINT")
    if arcpy.management.GetCount(os.path.join(ruta_salida,"Errores_Curvas.gdb\Errores")) == 0: 
        arcpy.AddMessage("No se encontraron Errores de topologia")
        #arcpy.management.Delete(os.path.join(ruta_salida,"Curvas_DGN.gdb"))
        #arcpy.management.Delete(os.path.join(ruta_salida,"Errores_Curvas.gdb"))
    else:
        conteo = arcpy.management.GetCount(os.path.join(ruta_salida,"Errores_Curvas.gdb\Errores"))
        arcpy.AddMessage(f"Se encontraron {conteo} errores de topologia entre las curvas")
        #arcpy.management.Delete(os.path.join(ruta_salida,"Curvas_DGN.gdb"))
    arcpy.AddMessage("Proceso terminado")
