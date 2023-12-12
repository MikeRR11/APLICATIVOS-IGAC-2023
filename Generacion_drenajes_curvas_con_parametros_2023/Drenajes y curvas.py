import arcpy, os ,sys

entradaDEM= sys.argv[1]
resultadosCarpeta = sys.argv[2]
valorCeldas = sys.argv[3]
eliminacionSegmentos= sys.argv[4]
suavisar = sys.argv[5]
longitud = sys.argv[6]
Tolerancia = sys.argv[7]
Distancia_entre_curvas = sys.argv[8]
Flujo_Fozado = sys.argv[9]
Metodologia_direccion_de_flujo = sys.argv[10]
flujo= sys.argv[11]


arcpy.env.workspace=resultadosCarpeta
######################################################################################
rutaDrenajes = resultadosCarpeta+os.sep+os.path.basename(entradaDEM).replace(".tif","")+"_Dreanajes.shp"
rutaCurvas = resultadosCarpeta+"/"+os.path.basename(entradaDEM).replace(".tif","")+"_Curvas.shp"

arcpy.AddMessage("Rellenado vacios")
RellenoSalida = arcpy.sa.Fill(entradaDEM)
################################
arcpy.AddMessage("Direccion de drenaje")
direccionDrenajes = arcpy.sa.FlowDirection(in_surface_raster=RellenoSalida, force_flow=Flujo_Fozado,flow_direction_type=Metodologia_direccion_de_flujo)
###############################
arcpy.AddMessage("acumulacion de flujo")
acumulacionFlujo= arcpy.sa.FlowAccumulation(direccionDrenajes, "", "FLOAT")
####################################################
arcpy.AddMessage("Reduccion de Red de Drenajes")

acumulacionFlujoRestringida= arcpy.sa.SetNull(acumulacionFlujo, "1", "Value < " + valorCeldas)
#############################
arcpy.AddMessage("Orden de la red")
ordenDrenajes = arcpy.sa.StreamOrder(acumulacionFlujoRestringida, direccionDrenajes, flujo)

##############################

arcpy.AddMessage("Conversion de raster a Shape")
Drenajes=arcpy.sa.StreamToFeature(ordenDrenajes, direccionDrenajes, resultadosCarpeta+"/"+os.path.basename(entradaDEM).replace(".tif","")+"_Dreanajes.shp", "SIMPLIFY")
arcpy.AddMessage(resultadosCarpeta+os.sep+os.path.basename(entradaDEM).replace(".tif","")+"_Dreanajes.shp")
arcpy.AddMessage("Creacion de curvas de nivel")
arcpy.sa.Contour(RellenoSalida, resultadosCarpeta+"/"+os.path.basename(entradaDEM).replace(".tif","")+"_Curvas.shp", Distancia_entre_curvas, "0", "1")

DrenajesCorregidos=arcpy.Dissolve_management(Drenajes,rutaDrenajes.replace(".shp","_DEF.shp"),"GRID_CODE","","SINGLE_PART","UNSPLIT_LINES")
arcpy.Delete_management(Drenajes)
arcpy.Rename_management(DrenajesCorregidos,rutaDrenajes)

if eliminacionSegmentos=="true":
    #!shape.length@meters!
    arcpy.AddMessage("Eliminando Segmentos cortos")
    arcpy.AddField_management(Drenajes,"Longitud","DOUBLE")
    arcpy.CalculateField_management(Drenajes,"Longitud","!shape.length@meters!","PYTHON")
    arcpy.MakeFeatureLayer_management(Drenajes, "BorrarDrenajes", """ "Longitud" < {} AND "GRID_CODE"=1 """.format(longitud))
    #arcpy.AddMessage(""" "Longitud" < {} AND "GRID_CODE"=1 """.format(longitud))
    #arcpy.AddMessage(""" "Longitud" < 150 AND "GRID_CODE"=1 """)
    arcpy.DeleteFeatures_management("BorrarDrenajes")

if suavisar == "true":
    arcpy.AddMessage("Suavisando Curvas y Drenajes")
    arcpy.SmoothLine_cartography(rutaDrenajes,rutaDrenajes.replace(".shp","Suavisados.shp"),"PAEK", Tolerancia+" Meters", "FIXED_CLOSED_ENDPOINT", "FLAG_ERRORS")
    arcpy.SmoothLine_cartography(rutaCurvas,rutaCurvas.replace(".shp","Suavisados"),"PAEK", Tolerancia+" Meters", "FIXED_CLOSED_ENDPOINT", "FLAG_ERRORS")
    

    












