# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Direccion de Gestion de Información Geografica
# Created on: 2023-06-22
# Created by: Juan Pablo Merchán Puentes - Diego Rugeles (Supervisor Desarrollo DGIG)
# # Usage: ModelosDigitalesDeTerrenos
# Description:
# ---------------------------------------------------------------------------
# Importe librerias

#Resolucion 0471 2020 IGAC, mirar exactitud de MT

#crear capa de puntos de control, 20 puntos, con xy z, la z la dejo cercana al modelo digital, hacer excel tambien para comparar los calculos,, tiene que dar lo mismo, mandar excel, puntos, y toolbox. crear puntos, crear columna de alturas
#Luego en geoprocesos crea campos de coordenadas, crear coordenas xy, eso lo paso a excel, toda la tabla, y luego el excel, luego cargar a arcgis online, y añadir coordenada en Z y esas modificarlas.

from tokenize import Double
import arcpy
import os
import math
from arcpy.sa import *
shp_fotocontrol = arcpy.GetParameterAsText(0)
ruta_raster = arcpy.GetParameterAsText(1)
ruta_salida = arcpy.GetParameterAsText(2)

arcpy.env.overwriteOutput = True

def RMSE (fotocontrol, ruta_raster, ruta_salida):
    
    file = open(os.path.join(str(ruta_salida),'Report_RMSE.txt'), "w") 
    #variables de entorno
    arrow = "=============================================="
    espacio= '	'
    
    Foto_2 = arcpy.MakeFeatureLayer_management(fotocontrol, os.path.join(str(ruta_salida),'ly_2_temp.shp'))#Capa falsa- punto
    
    arcpy.management.AddField(Foto_2, 'altura', 'double') #Agregar Campo
    arcpy.management.CalculateGeometryAttributes(Foto_2, [['altura','POINT_Z']], 'METERS') #Calculo distacia punto z

    Puntos_Validacion= ExtractValuesToPoints(Foto_2, ruta_raster, os.path.join(str(ruta_salida),"Puntos_Raster.shp"))
    
    
    arcpy.AddField_management(Puntos_Validacion, 'Z_RMSE', 'double')
    arcpy.CalculateField_management(Puntos_Validacion, 'Z_RMSE', '(!altura!-!RASTERVALU!)**(2)','PYTHON3')
    #arcpy.Delete_management(Foto_2)
    cont_id = 0
    with arcpy.da.SearchCursor(Puntos_Validacion, ['Z_RMSE']) as cursor:
        file.write('\nPositional Accuracy Report\n' + arrow +
                   '\n\nSpatial Reference Information\n'+
                   str(arcpy.Describe(fotocontrol).spatialReference.Name)+'\n'+arrow+
                   '\n\nPoint'+espacio+espacio+espacio+'delta Z')
        
        suma_z = 0
        
        for row in cursor:
            file.write('\n'+ str(cont_id+1) + espacio +espacio +espacio +
                       str(math.sqrt(row[0])) )
            
            suma_z += row[0]
            cont_id = cont_id+1
            
        n = str(arcpy.management.GetCount(Puntos_Validacion))
        
        
        rmse_z = suma_z/float(n)
        arcpy.AddMessage('El numerador antes de la raiz es ' + str(round(rmse_z, 2)))

        rmse_r = math.sqrt(rmse_z)
        rmse_e =rmse_r*1.96




        arcpy.AddMessage('El RMSE total es: ' + str(round(rmse_r, 2)))
        file.write('\n\n' + arrow + '\nError Report Section'+
                   '\nReport Units: '+espacio+espacio+espacio+'Meters'+
                   '\nConfidence Level: '+espacio+espacio+'95%'+
                   '\nNumber of observations: '+espacio+n+
                   '\nRMSE: '+espacio+espacio+espacio+espacio+ str(round(rmse_r, 2))+
                   '\n95% accuracy: '+espacio+espacio+espacio+ str(round(rmse_e, 2)))
    file.close()
if __name__ == '__main__':
    # Script arguments
    RMSE(shp_fotocontrol,ruta_raster, ruta_salida)