#Librerias
import arcpy
import os
import math
from arcpy import env
from arcpy.sa import *
# Script arguments
#exporte
dgn = arcpy.GetParameterAsText(0)
ruta_salida = arcpy.GetParameterAsText(1)
#generacion mdt
limite = arcpy.GetParameterAsText(2)
escala = arcpy.GetParameterAsText(3)
#calidad
raster = arcpy.GetParameterAsText(4)
marcos = arcpy.GetParameterAsText(5)
#ejecucion
export = arcpy.GetParameterAsText(6)
generar = arcpy.GetParameterAsText(7)
curvas = arcpy.GetParameterAsText(8)
control = arcpy.GetParameterAsText(9)
arcpy.env.overwriteOutput = True
def exportar(dgn, ruta_salida):
    arcpy.env.workspace = ruta_salida
    arcpy.env.overwriteOutput = True
    arcpy.management.CreateFolder(ruta_salida, 'GDB')
    arcpy.env.workspace = os.path.join(str(ruta_salida),'GDB')
    GDB_Salida = arcpy.management.CreateFileGDB(os.path.join(str(ruta_salida),'GDB'), 'restitucion')
    arcpy.conversion.CADToGeodatabase(dgn, GDB_Salida, 'datos','1000', 
                                      spatial_reference='PROJCS["MAGNA-SIRGAS_Origen-Nacional",GEOGCS["GCS_MAGNA",DATUM["D_MAGNA",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",5000000.0],PARAMETER["False_Northing",2000000.0],PARAMETER["Central_Meridian",-73.0],PARAMETER["Scale_Factor",0.9992],PARAMETER["Latitude_Of_Origin",4.0],UNIT["Meter",1.0]];-618700 -8436100 10000;-100000 10000;-100000 10000;0.001;0.001;0.001;IsHighPrecision')
    
    arcpy.env.workspace = ruta_salida
    arcpy.management.CreateFolder(ruta_salida, '1_SHAPES_ORIGINALES')
    arcpy.management.CreateFolder(ruta_salida, '2_SHAPES_EDICION')
    
    Feature_Class_Point = os.path.join(str(GDB_Salida),'datos\Point')
    Feature_Class_Polyline = os.path.join(str(GDB_Salida),'datos\Polyline')
    punto = arcpy.management.SelectLayerByAttribute(Feature_Class_Point, 'NEW_SELECTION', 'Level = 41')
    curva = arcpy.management.SelectLayerByAttribute(Feature_Class_Polyline, 'NEW_SELECTION', 'Level IN (42,43,44,45)')
    polylinea = arcpy.management.SelectLayerByAttribute(Feature_Class_Polyline, 'NEW_SELECTION', 'Level IN (1,2,16,18,19,20)')
    arcpy.conversion.FeatureClassToShapefile([punto, curva, polylinea], os.path.join(str(ruta_salida),'1_SHAPES_ORIGINALES'))
    arcpy.env.workspace = os.path.join(str(ruta_salida),'1_SHAPES_ORIGINALES')
    arcpy.management.Rename('Point_Layer1.shp', 'punto.shp')
    arcpy.management.Rename('Polyline_Layer1.shp', 'curva_nivel.shp')
    arcpy.management.Rename('Polyline_Layer2.shp', 'polylinea.shp')
    arcpy.management.CopyFeatures('punto.shp', os.path.join(str(ruta_salida),'2_SHAPES_EDICION/punto2.shp'))
    arcpy.management.CopyFeatures('curva_nivel.shp', os.path.join(str(ruta_salida),'2_SHAPES_EDICION/curva_nivel2.shp'))
    arcpy.management.CopyFeatures('polylinea.shp', os.path.join(str(ruta_salida),'2_SHAPES_EDICION/polylinea2.shp'))
    arcpy.management.Delete(os.path.join(str(ruta_salida),'GDB'))
def generar_MDT(ruta_salida, limite, escala, nombre_folder):
    arcpy.env.workspace = ruta_salida
    Shape_punto2 = os.path.join(str(ruta_salida),'2_SHAPES_EDICION/punto2.shp')
    Shape_curva_nivel2 = os.path.join(str(ruta_salida),'2_SHAPES_EDICION/curva_nivel2.shp')
    Shape_polylinea2 = os.path.join(str(ruta_salida),'2_SHAPES_EDICION/polylinea2.shp')
    Shape_limite = limite
    arcpy.management.AddField(Shape_curva_nivel2, 'Elev_Ajust', 'DOUBLE', field_is_nullable='TRUE')
    arcpy.management.CalculateField(Shape_curva_nivel2, 'Elev_Ajust', '!Elevation!+0.03', 'PYTHON')
    
    arcpy.env.workspace = os.path.join(str(ruta_salida),'3_SALIDAS', nombre_folder)
    arcpy.ddd.CreateTin('TIN', spatial_reference='PROJCS["MAGNA-SIRGAS_Origen-Nacional",GEOGCS["GCS_MAGNA",DATUM["D_MAGNA",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",5000000.0],PARAMETER["False_Northing",2000000.0],PARAMETER["Central_Meridian",-73.0],PARAMETER["Scale_Factor",0.9992],PARAMETER["Latitude_Of_Origin",4.0],UNIT["Meter",1.0]];-618700 -8436100 10000;-100000 10000;-100000 10000;0.001;0.001;0.001;IsHighPrecision',
                        in_features = [[Shape_punto2,'Elevation','Mass_Points','<None>'],
                                       [Shape_polylinea2, 'Shape.Z', 'Hard_Line','<None>'],
                                       [Shape_curva_nivel2, 'Elev_Ajust', 'Hard_Line','<None>'],
                                       [Shape_limite, '<None>' ,'Soft_Clip','<None>']])
    
    dic_mitad_celda = {'1000':'CELLSIZE 0,5',
                       '2000':'CELLSIZE 1',
                       '5000':'CELLSIZE 2,5',
                       '10000':'CELLSIZE 5',
                       '25000':'CELLSIZE 12,5',
                       }
    
    dic_celda = {'1000':'1',
                 '2000':'2',
                 '5000':'5',
                 '10000':'10',
                 '25000':'25',
                 }
    
    arcpy.ddd.TinRaster('TIN', 'MDT_Mitad_Escala.tif', 'FLOAT', 'NATURAL_NEIGHBORS', dic_mitad_celda[escala], '1')
    arcpy.management.Resample('MDT_Mitad_Escala.tif', 'MDT_Escala.tif', dic_celda[escala], 'BILINEAR')
    Contour('MDT_Escala.tif', 'Contornos.shp', dic_celda[escala], '0', '1', 'CONTOUR')
    arcpy.cartography.SmoothLine('Contornos.shp', 'Contornos_Smooth.shp', 'PAEK', '4', 'FIXED_CLOSED_ENDPOINT', 'NO_CHECK')
    arcpy.management.DeleteField(Shape_curva_nivel2, 'Elev_Ajust')
    arcpy.management.Delete('Contornos.shp')
    arcpy.management.CreateFolder(os.path.join(str(ruta_salida),'3_SALIDAS', nombre_folder), 'XYZ')
    arcpy.env.workspace = os.path.join(str(ruta_salida),'3_SALIDAS', nombre_folder,'XYZ')
    arcpy.conversion.RasterToASCII(os.path.join(str(ruta_salida),'3_SALIDAS',nombre_folder, 'MDT_Escala.tif'), 'XYZ.txt')
    return
def generar_CurvasImpares(ruta_salida, raster):
    arcpy.env.workspace = ruta_salida
    arcpy.management.CreateFolder(ruta_salida, '3A_CURVAS_IMPARES')
    Shape_contornos = os.path.join(str(ruta_salida),raster,'Contornos_Smooth.shp')
    arcpy.management.CopyFeatures(Shape_contornos, os.path.join(str(ruta_salida),'3A_CURVAS_IMPARES/Contornos.shp'))
    copia_contornos = os.path.join(str(ruta_salida),'3A_CURVAS_IMPARES/Contornos.shp')
    arcpy.management.AddField(copia_contornos, 'ALTURA_1', 'TEXT', field_is_nullable='TRUE')
    arcpy.management.CalculateField(copia_contornos, 'ALTURA_1', '$feature.Contour', 'ARCADE')
    arcpy.env.workspace = os.path.join(ruta_salida,'3A_CURVAS_IMPARES')
    contornos_ly=arcpy.management.MakeFeatureLayer(copia_contornos, 'temp.shp', where_clause="ALTURA_1 LIKE '%1' Or ALTURA_1 LIKE '%3' Or ALTURA_1 LIKE '%5' Or ALTURA_1 LIKE '%7' Or ALTURA_1 LIKE '%9'")
    arcpy.conversion.FeatureClassToFeatureClass(contornos_ly, os.path.join(ruta_salida,'3A_CURVAS_IMPARES'), 'CURVAS_IMPARES.shp')
    arcpy.management.Delete('Contornos.shp')
codeblock = """rec=0 
def autoIncrement(): 
    global rec 
    pStart = 1  
    pInterval = 1 
    if (rec == 0):  
        rec = pStart  
    else:  
        rec += pInterval  
    return rec"""
def Control_Calidad(ruta_salida, raster, limite, marcos):
    arcpy.env.workspace = ruta_salida
    arcpy.management.CreateFolder(ruta_salida, '4_CONTROL_CALIDAD')
    arcpy.management.CreateFolder(os.path.join(ruta_salida, '4_CONTROL_CALIDAD'), 'temp01')
    shp_puntos = os.path.join(ruta_salida,'1_SHAPES_ORIGINALES','punto.shp')
    arcpy.management.DeleteIdentical(shp_puntos, 'SHAPE')
    #verificar puntos dentro del limite
    select = arcpy.management.SelectLayerByLocation(shp_puntos, 'INTERSECT', limite, '', 'NEW_SELECTION', '')
    arcpy.management.CopyFeatures(select, os.path.join(str(ruta_salida),'4_CONTROL_CALIDAD/temp01/puntos_restitucion.shp'))
    arcpy.management.CreateRandomPoints(os.path.join(ruta_salida, '4_CONTROL_CALIDAD', 'temp01'), 'puntos_aleatorios', 
                                        os.path.join(str(ruta_salida),'4_CONTROL_CALIDAD','temp01','puntos_restitucion.shp'),"", 25, '1 Meters', "", "")
    
    arcpy.env.workspace = os.path.join(ruta_salida,'4_CONTROL_CALIDAD', 'temp01')
    select = arcpy.management.SelectLayerByLocation('puntos_restitucion.shp', 'INTERSECT', 'puntos_aleatorios', '0,2 Meters', 'NEW_SELECTION', 'NOT_INVERT')
    arcpy.management.CreateFolder(os.path.join(ruta_salida,'4_CONTROL_CALIDAD'), 'PUNTOS_CC')
    ly_intersect = arcpy.MakeFeatureLayer_management(select, os.path.join(ruta_salida,'4_CONTROL_CALIDAD','PUNTOS_CC','puntos_restitucion_select.shp'))
    arcpy.conversion.FeatureClassToFeatureClass(ly_intersect, os.path.join(ruta_salida,'4_CONTROL_CALIDAD','PUNTOS_CC'), 'puntos_CC.shp')
    mdt = os.path.join(raster,'MDT_Escala.tif')
    ExtractValuesToPoints(os.path.join(ruta_salida,'4_CONTROL_CALIDAD','PUNTOS_CC','puntos_CC.shp'), mdt, os.path.join(ruta_salida,'4_CONTROL_CALIDAD','PUNTOS_CC','puntos_raster.shp'))
    n_puntos_cc = arcpy.management.GetCount(os.path.join(ruta_salida, '4_CONTROL_CALIDAD','PUNTOS_CC','puntos_CC.shp'))
    if int(str(n_puntos_cc)) >= 25:
        arcpy.management.AddFields(os.path.join(ruta_salida, '4_CONTROL_CALIDAD','PUNTOS_CC','puntos_CC.shp'), [['Pto_No','SHORT'],
                                                                                                                ['CNorteTerr', 'DOUBLE'],
                                                                                                                ['CEsteTerr', 'DOUBLE'],
                                                                                                                ['CNorteMod', 'DOUBLE'],
                                                                                                                ['CEsteMod', 'DOUBLE'],
                                                                                                                ['HTerr','DOUBLE'],
                                                                                                                ['HMod', 'DOUBLE']])
        
        expression = "autoIncrement()"
        arcpy.management.CalculateField(os.path.join(ruta_salida,'4_CONTROL_CALIDAD','PUNTOS_CC','puntos_raster.shp'), 'Pto_No', expression, 'PYTHON3', codeblock)
        arcpy.management.CalculateField(os.path.join(ruta_salida,'4_CONTROL_CALIDAD','PUNTOS_CC','puntos_raster.shp'), 'HMod', '$feature.RASTERVALU', 'ARCADE')
        arcpy.management.CalculateField(os.path.join(ruta_salida,'4_CONTROL_CALIDAD','PUNTOS_CC','puntos_raster.shp'), 'HTerr', '$feature.Elevation', 'ARCADE')
        arcpy.management.CalculateGeometryAttributes(os.path.join(ruta_salida,'4_CONTROL_CALIDAD','PUNTOS_CC','puntos_raster.shp'), [['CNorteTerr','POINT_Y'],
                                                                                                                                     ['CEsteTerr','POINT_X'],
                                                                                                                                     ['CNorteMod','POINT_Y'],
                                                                                                                                     ['CEsteMod','POINT_X']])
        
        arcpy.management.CreateFolder(os.path.join(ruta_salida, '4_CONTROL_CALIDAD'), 'MARCOS')
        arcpy.management.CopyFeatures(marcos, os.path.join(str(ruta_salida),'4_CONTROL_CALIDAD/MARCOS/marcos.shp'))
        
        arcpy.analysis.SpatialJoin(os.path.join(ruta_salida,'4_CONTROL_CALIDAD','PUNTOS_CC','puntos_raster.shp'), 
                                   os.path.join(str(ruta_salida),'4_CONTROL_CALIDAD','MARCOS','marcos.shp'),
                                   os.path.join(ruta_salida,'4_CONTROL_CALIDAD','PUNTOS_CC','puntos_CC_reporte_modelo.shp'), 
                                   'JOIN_ONE_TO_MANY', 'KEEP_ALL', "", 'INTERSECT', "", "")
        
        arcpy.management.CreateFolder(os.path.join(ruta_salida, '4_CONTROL_CALIDAD'), 'EXCEL')
        puntos_cc_reporte_modelo = os.path.join(ruta_salida,'4_CONTROL_CALIDAD','PUNTOS_CC','puntos_CC_reporte_modelo.shp')
        puntos_cc_reporte = os.path.join(ruta_salida,'4_CONTROL_CALIDAD','PUNTOS_CC','puntos_raster.shp')
        arcpy.management.DeleteIdentical(puntos_cc_reporte, 'SHAPE')
        arcpy.management.DeleteField(puntos_cc_reporte, ['Entity','Handle','Level','Layer','LvlDesc','LyrFrzn','LyrLock','LyrOn','LvlPlot','Color',
                                                         'EntColor','LyrColor','Linetype','EntLinetyp','LyrLnType','Class','GGroup','CadModel','CadModelID',
                                                         'Fill','LineWt','EntLineWt','LyrLineWt','RefName','LTScale','QrotW','QrotX','QrotZ','DocName',
                                                         'DocPath','DocType','DocVer','DocUpdate','DocId','Angle','ScaleX','ScaleY','ScaleZ','RASTERVALU'])
        
        arcpy.management.DeleteField(puntos_cc_reporte_modelo, ['Join_Count','TARGET_FID','JOIN_FID','Entity','Handle','Level','Layer','LvlDesc','LyrFrzn','LyrLock',
                                                                'LyrOn','LvlPlot','Color','EntColor','LyrColor','Linetype','EntLinetyp','LyrLnType','Class','GGroup','CadModel',
                                                                'CadModelID','Fill','LineWt','EntLineWt','LyrLineWt','RefName','LTScale','QrotW','QrotX','QrotZ','DocName',
                                                                'DocPath','DocType','DocVer','DocUpdate','DocId','Angle','ScaleX','ScaleY','ScaleZ','RASTERVALU'])
        arcpy.conversion.TableToExcel(puntos_cc_reporte_modelo, os.path.join(ruta_salida, '4_CONTROL_CALIDAD', 'EXCEL','puntos_CC_reporte_modelo.xls'), "", "")
        arcpy.conversion.TableToExcel(puntos_cc_reporte, os.path.join(ruta_salida, '4_CONTROL_CALIDAD', 'EXCEL','puntos_CC_reporte.xls'), "", "")
        arcpy.management.Rename(puntos_cc_reporte, 'puntos_CC_reporte.shp')
        arcpy.management.Delete(os.path.join(ruta_salida, '4_CONTROL_CALIDAD','PUNTOS_CC','puntos_CC.shp'))
    else:
        arcpy.AddMessage('No se genero el minimo de puntos aleatorios, verifique que el shape "punto.shp" de la carpeta "1_SHAPES ORIGINALES" tenga como minimo 25 puntos y vuelva a correr el paso de "Control de calidad"')
if __name__ == "__main__":
    if export == 'true':
        shp_originales = os.path.exists(os.path.join(str(ruta_salida),'1_SHAPES_ORIGINALES')) #verifica si ya existe la carpeta con los shapes originales
        shp_edicion = os.path.exists(os.path.join(str(ruta_salida),'2_SHAPES_EDICION')) #verifica si ya existe la carpeta con los shapes originales
        if str(shp_originales) == 'True' or str(shp_edicion) == 'True':
            arcpy.AddMessage('Ya existen los directorios 1_SHAPES_ORIGINALES Y/O 2_SHAPES_EDICION, ')
            arcpy.AddMessage('por favor indique otra ruta de salida o elimine todos los archivos con el mismo nombre de la ruta de salida')
        
        else: 
            arcpy.AddMessage('________________________')
            arcpy.AddMessage('Exportando el DGN a Shapefile')
            exportar(dgn, ruta_salida)
            arcpy.AddMessage('Finalizado')
    
    if generar == 'true':
        shp_edicion = os.path.exists(os.path.join(str(ruta_salida),'2_SHAPES_EDICION')) #verifica si ya existe la carpeta con los shapes edicion
        
        if str(shp_edicion) == 'False': #si no existe manda mensaje
            arcpy.AddMessage('No existe la carpeta con los Shapes de edicion "2_SHAPES_EDICION", verifique su existencia dentro de la carpeta ingresada en "ruta_salida" y de no existir se recomienda volver a correr el paso 1 "Exportar"')
        
        else: #si existe se puede ejecutar la funcion pasa a revisar la carpeta
            arcpy.AddMessage('________________________')
            arcpy.AddMessage('Generando MDT')
            existe = os.path.exists(os.path.join(str(ruta_salida),'3_SALIDAS')) #verifica si ya existe la carpeta
            
            if str(existe) == 'True': #revisa las carpetas existentes en salidas
                directorio = os.path.join(str(ruta_salida),'3_SALIDAS')
                contenido = os.listdir(directorio)
                carpetas = []
                numero =[]
                
                for carpeta in contenido: #recorre el listado y extrae el numero
                    carpetas.append(carpeta)
                    nombre = str(carpeta)
                    numero.append(int(nombre[7:]))               
                
                max = numero[0]
                for x in numero: #verifica el maximo
                    if x > max:
                        max = x
                
                folder = max + 1
                nombre_folder = 'RASTER_'+str(folder) #nombre del nuevo folder para el raster
                arcpy.management.CreateFolder(os.path.join(str(ruta_salida),'3_SALIDAS'), nombre_folder) #crea el nombre del folder para almacernar el raster
                generar_MDT(ruta_salida, limite, escala, nombre_folder)
            
            else:
                nombre_folder = 'RASTER_1'
                arcpy.management.CreateFolder(os.path.join(str(ruta_salida)),'3_SALIDAS')
                arcpy.management.CreateFolder(os.path.join(str(ruta_salida),'3_SALIDAS'), nombre_folder)
                generar_MDT(ruta_salida, limite, escala,nombre_folder)
            arcpy.AddMessage('Finalizado')
    
    if curvas == 'true':
        shp_contornos = os.path.exists(raster) #verifica si existe el shape de contornos del raster
        if str(shp_contornos) == 'False':
            arcpy.AddMessage('No existe el shapefile con los contornos para generar las curvas impares, verifique la carpeta introducida en el parametro "raster"')
        
        else:    
            arcpy.AddMessage('________________________')
            arcpy.AddMessage('Generando Curvas Impares')
            generar_CurvasImpares(ruta_salida, raster)
        arcpy.AddMessage('Finalizado')
    if control == 'true':
        carpeta = os.path.exists(os.path.join(ruta_salida, '1_SHAPES_ORIGINALES', 'punto.shp')) #verifica si existe el shape de puntos original
        if str(carpeta) == 'True':
            n_puntos = arcpy.management.GetCount(os.path.join(ruta_salida, '1_SHAPES_ORIGINALES', 'punto.shp'))
            arcpy.AddMessage(str(type(int(str(n_puntos))))+'zz')
            arcpy.AddMessage(str((int(str(n_puntos))))+'zz')
            
            if int(str(n_puntos)) >= 25:
                arcpy.AddMessage('________________________')
                arcpy.AddMessage('Realizando el Control de Calidad')
                Control_Calidad(ruta_salida, raster, limite, marcos)
                arcpy.AddMessage('Finalizado')
            else:
                arcpy.AddMessage('Se tiene menos de 25 puntos en la capa punto.shp, por lo cual no se puede realizar el control de calidad. Verifique la cantidad de puntos existentes.')
        else:
            arcpy.AddMessage('No existe el shape "punto.shp" proveniente del paso 1 "exportar de dgn a shp", verifique la existencia del shape dentro de la carpeta "1_SHAPES_ORIGINALES"')
