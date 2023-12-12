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
def unsplit(lyr_poly,Folder_Output):
    arcpy.management.UnsplitLine(in_features=lyr_poly, out_feature_class= os.path.join(Folder_Output,"curvas_merge.shp"))

if __name__ == "__main__":
    arrow = "=============================================="
    espacio= '	'
    arcpy.AddMessage("Iniciando el proceso de Conteo")
    dgn = arcpy.GetParameterAsText(0)
    ruta_salida = arcpy.GetParameterAsText(1)
    arcpy.AddMessage("Creando GDBs de trabajo")
    gdb_curvas = crearGDB(ruta_salida, "Curvas_DGN")
    gdb_errores = crearGDB(ruta_salida, "Errores_Curvas")
    dataset_name = "conteo_curvas"
    arcpy.AddMessage("Migrando DGN a GDB")
    convertirCADtoGDB(dgn, gdb_curvas, dataset_name)
    arcpy.env.workspace = os.path.join(ruta_salida,"Curvas_DGN.gdb")
    curvas_select  = arcpy.management.MakeFeatureLayer(Niveles_CNivel('conteo_curvas\Polyline'), os.path.join(ruta_salida,"curvas_merge.shp"))
    arcpy.AddMessage("Uniendo Curvas de nivel")
    curvas_merge = unsplit(curvas_select,ruta_salida)
    file = open(os.path.join(str(ruta_salida),'Reporte_Conteo_Curvas.txt'), "w")
    arcpy.AddMessage("Generando Reporte")
    file.write('\nReporte Conteo Curvas de Nivel \n' + arrow)
    file.write("\n"+ arrow +"\n" + arrow)
    file.write("\nCurvas Contabilizadas: {0} \n". format(arcpy.management.GetCount(os.path.join(ruta_salida,"curvas_merge.shp"))))
    arcpy.AddMessage("Proceso terminado")
