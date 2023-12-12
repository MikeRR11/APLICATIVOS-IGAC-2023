import arcpy
import os
# Script arguments
GDB_input = arcpy.GetParameterAsText(0)
#GDB_input ='D:/22_IGAC/2. Proyectos/3. Desarrollos/4. Migracion_modelo/1_insumos/Carto10000_15162_RS_20160126.gdb'
GDB_output = arcpy.GetParameterAsText(1)
#GDB_output ='D:/22_IGAC/2. Proyectos/3. Desarrollos/4. Migracion_modelo/1_insumos/GDB_NUEVO_MODELO/CBasica_V2.5.gdb'
arcpy.env.workspace=GDB_input
#global Variable:
i=0 #contador
# Showing templates
sep= '######################################'
arrow= '--'
hasht= '##'
#------- Migracion Superficies de Agua-------------#
#--------------------------------------------------#
arcpy.AddMessage("\n{0} ...INICIANDO PROCESO DE MIGRACION... {1}.".format(sep, sep))
arcpy.AddMessage("{0}{1}{2}\n".format(sep, sep,sep))
arcpy.AddMessage("{0} Nombres Geográficos... ".format(hasht))
#activeeditsesion()
edit = arcpy.da.Editor(GDB_output)
edit.startEditing(False, True)
edit.startOperation()
#Impresion de registros migrados 
def registrosmigrados(x, ly_migrado):
    arcpy.AddMessage("    Han sido migrados {0} registros al Feature {1}.".format(x, ly_migrado))

def filtrarsolonombres(lyr_poly):
    layercontoponimia=arcpy.management.SelectLayerByAttribute(lyr_poly,'NEW_SELECTION', where_clause="NOMBRE_GEOGRAFICO IS NOT NULL and NOMBRE_GEOGRAFICO NOT LIKE '' AND NOMBRE_GEOGRAFICO NOT LIKE ' '")
    return layercontoponimia
# lista = os.listdir(GDB_input)
# for feature_class in lista:
#     arcpy.AddMessage(feature_class)
i=0
with arcpy.da.SearchCursor(os.path.join(GDB_input,'IB'),['SHAPE@','TOPONIMO','ENT_GEO','ATRIB','IDE','OBJECTID']) as sCur:
    with arcpy.da.InsertCursor(os.path.join(GDB_output, 'NombresGeograficos/NGeogr'),['SHAPE@','NGNPrincip','NGCategori','NGSubcateg','RuleID','OBJECTID',]) as iCur:
        for row in sCur:
            i+=1
            row_list= list(row)
            row_list[0]= row[0].projectAs('9377')
            if row_list[2] == 2325 and row_list[3] == 3680 :   ##condicionales para los tipos
                row_list[2] = 2  # Comercio industria y turismo
                row_list[3] = 1  # Industria
                row_list[4] = 2  # Comercio industria y turismo
                #row_list[6] = 2  
            elif row_list[2] == 2325 and row_list[3] == 4101 :
                row_list[2] = 2  # Comercio industria y turismo
                row_list[3] = 1  # Industria
                row_list[4] = 2  # Comercio industria y turismo
            elif row_list[2] == 2304  :
                row_list[2] = 2  # Comercio industria y turismo
                row_list[3] = 1  # Industria
                row_list[4] = 2  # Comercio industria y turismo
            elif row_list[2] == 2305  :
                row_list[2] = 2  # Comercio industria y turismo
                row_list[3] = 1  # Industria
                row_list[4] = 2  # Comercio industria y turismo
            elif row_list[2] == 2325 and row_list[3] == 4131 :
                row_list[2] = 2  # Comercio industria y turismo
                row_list[3] = 2  # Hotel
                row_list[4] = 2  # Comercio industria y turismo
            elif row_list[2] == 2325 and row_list[3] == 2320 :
                row_list[2] = 2  # Comercio industria y turismo
                row_list[3] = 3  # Comercio
                row_list[4] = 2  # Comercio industria y turismo
            elif row_list[2] == 2325 and row_list[3] == 4165 :
                row_list[2] = 3  # Cultura y ocio
                row_list[3] = 3  # Monumento
                row_list[4] = 3  # Cultura y ocio
            elif row_list[2] == 2325 and row_list[3] == 4129 :
                row_list[2] = 3  # Cultura y ocio
                row_list[3] = 4  # Iglesia
                row_list[4] = 3  # Cultura y ocio
            elif row_list[2] == 2325 and row_list[3] == 4112 :
                row_list[2] = 5  # Educación
                row_list[3] = 1  # Instituto de educación 
                row_list[4] = 5  # Educación
            elif row_list[2] == 2325 and row_list[3] == 5620 :
                row_list[2] = 6  # Minas y energia
                row_list[3] = 4  # Area petrolera
                row_list[4] = 6  # Minas y energia
            elif row_list[2] == 2325 and row_list[3] == 2302 :
                row_list[2] = 6  # Minas y energia
                row_list[3] = 3  # Area minera
                row_list[4] = 6  # Minas y energia
            elif row_list[2] == 2321:
                row_list[2] = 6  # Minas y energia
                row_list[3] = 2  # Area de extracciòn
                row_list[4] = 6  # Minas y energia
            elif row_list[2] == 2325 and row_list[3] == 4119 :
                row_list[2] = 7  # Salud y protección social
                row_list[3] = 7  # Puesto de salud
                row_list[4] = 7  # Salud y protección social
            elif row_list[2] == 2325 and row_list[3] == 3686  :
                row_list[2] = 7  # Salud y protección social
                row_list[3] = 6  # Cementerio
                row_list[4] = 7  # Salud y protección social
            elif row_list[2] == 2325 and row_list[3] == 4166  :
                row_list[2] = 8  # Seguridad y defensa
                row_list[3] = 2  # Estación de policia
                row_list[4] = 8  # Seguridad y defensa
            elif row_list[2] == 2325 and row_list[3] == 3413  :
                row_list[2] = 14  # Otro
                row_list[3] = 1  # Otro
                row_list[4] = 14  # Otro
            elif row_list[2] == 2325 and row_list[3] == 5610  :
                row_list[2] = 14  # Otro
                row_list[3] = 1  # Otro
                row_list[4] = 14  # Otro
            elif row_list[2] == 2325 and row_list[3] == 5610  :
                row_list[2] = 14  # Otro
                row_list[3] = 1  # Otro
                row_list[4] = 14  # Otro
            elif row_list[2] == 7101 and row_list[3] == 8314  :
                row_list[2] = 1  # Ambiente y desarrollo sostenible
                row_list[3] = 1  # Parque natural
                row_list[4] = 1  # Ambiente y desarrollo sostenible
            elif row_list[2] == 7101 and row_list[3] == 8302  :
                row_list[2] = 1  # Ambiente y desarrollo sostenible
                row_list[3] = 1  # Parque natural
                row_list[4] = 1  # Ambiente y desarrollo sostenible
            elif row_list[2] == 7101 and row_list[3] == 8313  :
                row_list[2] = 1  # Ambiente y desarrollo sostenible
                row_list[3] = 2  # Parque arqueologico
                row_list[4] = 1  # Ambiente y desarrollo sostenible
            elif row_list[2] == 7101 and row_list[3] == 8321  :
                row_list[2] = 1  # Ambiente y desarrollo sostenible
                row_list[3] = 3  # Santuario de flora y fauna
                row_list[4] = 1  # Ambiente y desarrollo sostenible
            elif row_list[2] == 7101 and row_list[3] == 8319  :
                row_list[2] = 1  # Ambiente y desarrollo sostenible
                row_list[3] = 4  # Reservorio natural o forestal
                row_list[4] = 1  # Ambiente y desarrollo sostenible
            elif row_list[2] == 8400 and row_list[3] == 8401  :
                row_list[2] = 1  # Ambiente y desarrollo sostenible
                row_list[3] = 5  # Costero insular
                row_list[4] = 1  # Ambiente y desarrollo sostenible
            elif row_list[2] == 8400 and row_list[3] == 8402  :
                row_list[2] = 1  # Ambiente y desarrollo sostenible
                row_list[3] = 5  # Costero insular
                row_list[4] = 1  # Ambiente y desarrollo sostenible
            elif row_list[2] == 8400 and row_list[3] == 8411  :
                row_list[2] = 1  # Ambiente y desarrollo sostenible
                row_list[3] = 5  # Costero insular
                row_list[4] = 1  # Ambiente y desarrollo sostenible
            elif row_list[2] == 8400 and row_list[3] == 8414  :
                row_list[2] = 1  # Ambiente y desarrollo sostenible
                row_list[3] = 5  # Costero insular
                row_list[4] = 1  # Ambiente y desarrollo sostenible
            elif row_list[2] == 8400 and row_list[3] == 5127  :
                row_list[2] = 1  # Ambiente y desarrollo sostenible
                row_list[3] = 5  # Costero insular
                row_list[4] = 1  # Ambiente y desarrollo sostenible                
            elif row_list[2] == 8400 and row_list[3] == 8423  :
                row_list[2] = 1  # Ambiente y desarrollo sostenible
                row_list[3] = 5  # Costero insular
                row_list[4] = 1  # Ambiente y desarrollo sostenible
            elif row_list[2] == 8400 and row_list[3] == 8424  :
                row_list[2] = 1  # Ambiente y desarrollo sostenible
                row_list[3] = 5  # Costero insular
                row_list[4] = 1  # Ambiente y desarrollo sostenible
            elif row_list[2] == 8400 and row_list[3] == 8428  :
                row_list[2] = 1  # Ambiente y desarrollo sostenible
                row_list[3] = 5  # Costero insular
                row_list[4] = 1  # Ambiente y desarrollo sostenible
            elif row_list[2] == 8400 and row_list[3] == 8429  :
                row_list[2] = 1  # Ambiente y desarrollo sostenible
                row_list[3] = 5  # Costero insular
                row_list[4] = 1  # Ambiente y desarrollo sostenible 
            elif row_list[2] == 8400 and row_list[3] == 8430  :
                row_list[2] = 1  # Ambiente y desarrollo sostenible
                row_list[3] = 5  # Costero insular
                row_list[4] = 1  # Ambiente y desarrollo sostenible     
            elif row_list[2] == 8400 and row_list[3] == 8431  :
                row_list[2] = 1  # Ambiente y desarrollo sostenible
                row_list[3] = 5  # Costero insular
                row_list[4] = 1  # Ambiente y desarrollo sostenible 
            elif row_list[2] == 8400 and row_list[3] == 8419  :
                row_list[2] = 1  # Ambiente y desarrollo sostenible
                row_list[3] = 5  # Costero insular
                row_list[4] = 1  # Ambiente y desarrollo sostenible   
            elif row_list[2] == 8400 and row_list[3] == 8422  :
                row_list[2] = 1  # Ambiente y desarrollo sostenible
                row_list[3] = 5  # Costero insular
                row_list[4] = 1  # Ambiente y desarrollo sostenible  
            elif row_list[2] == 8400 and row_list[3] == 8427  :
                row_list[2] = 1  # Ambiente y desarrollo sostenible
                row_list[3] = 6  # Oceano
                row_list[4] = 1  # Ambiente y desarrollo sostenible     
            elif row_list[2] == 8400 and row_list[3] == 8425  :
                row_list[2] = 1  # Ambiente y desarrollo sostenible
                row_list[3] = 6  # Oceano
                row_list[4] = 1  # Ambiente y desarrollo sostenible 

            elif row_list[2] == 8100 and row_list[3] == 8101  :
                row_list[2] = 1  # Ambiente y desarrollo sostenible
                row_list[3] = 7  # Orografía
                row_list[4] = 1  # Ambiente y desarrollo sostenible 
            elif row_list[2] == 8100 and row_list[3] == 8103  :
                row_list[2] = 1  # Ambiente y desarrollo sostenible
                row_list[3] = 7  # Orografía
                row_list[4] = 1  # Ambiente y desarrollo sostenible 
            elif row_list[2] == 8100 and row_list[3] == 8105  :
                row_list[2] = 1  # Ambiente y desarrollo sostenible
                row_list[3] = 7  # Orografía
                row_list[4] = 1  # Ambiente y desarrollo sostenible 
            elif row_list[2] == 8100 and row_list[3] == 8106  :
                row_list[2] = 1  # Ambiente y desarrollo sostenible
                row_list[3] = 7  # Orografía
                row_list[4] = 1  # Ambiente y desarrollo sostenible 
            elif row_list[2] == 8100 and row_list[3] == 8107  :
                row_list[2] = 1  # Ambiente y desarrollo sostenible
                row_list[3] = 7  # Orografía
                row_list[4] = 1  # Ambiente y desarrollo sostenible 
            elif row_list[2] == 8100 and row_list[3] == 8108  :
                row_list[2] = 1  # Ambiente y desarrollo sostenible
                row_list[3] = 7  # Orografía
                row_list[4] = 1  # Ambiente y desarrollo sostenible 
            elif row_list[2] == 8100 and row_list[3] == 8109  :
                row_list[2] = 1  # Ambiente y desarrollo sostenible
                row_list[3] = 7  # Orografía
                row_list[4] = 1  # Ambiente y desarrollo sostenible 
            elif row_list[2] == 8100 and row_list[3] == 8110  :
                row_list[2] = 1  # Ambiente y desarrollo sostenible
                row_list[3] = 7  # Orografía
                row_list[4] = 1  # Ambiente y desarrollo sostenible 
            elif row_list[2] == 8100 and row_list[3] == 8111  :
                row_list[2] = 1  # Ambiente y desarrollo sostenible
                row_list[3] = 7  # Orografía
                row_list[4] = 1  # Ambiente y desarrollo sostenible 
            elif row_list[2] == 8100 and row_list[3] == 8112  :
                row_list[2] = 1  # Ambiente y desarrollo sostenible
                row_list[3] = 7  # Orografía
                row_list[4] = 1  # Ambiente y desarrollo sostenible 
            elif row_list[2] == 8100 and row_list[3] == 8114  :
                row_list[2] = 1  # Ambiente y desarrollo sostenible
                row_list[3] = 7  # Orografía
                row_list[4] = 1  # Ambiente y desarrollo sostenible 
            elif row_list[2] == 8100 and row_list[3] == 8116  :
                row_list[2] = 1  # Ambiente y desarrollo sostenible
                row_list[3] = 7  # Orografía
                row_list[4] = 1  # Ambiente y desarrollo sostenible
            elif row_list[2] == 8100 and row_list[3] == 8115  :
                row_list[2] = 1  # Ambiente y desarrollo sostenible
                row_list[3] = 7  # Orografía
                row_list[4] = 1  # Ambiente y desarrollo sostenible 
            elif row_list[2] == 8100 and row_list[3] == 8117  :
                row_list[2] = 1  # Ambiente y desarrollo sostenible
                row_list[3] = 7  # Orografía
                row_list[4] = 1  # Ambiente y desarrollo sostenible 
            elif row_list[2] == 8100 and row_list[3] == 8118  :
                row_list[2] = 1  # Ambiente y desarrollo sostenible
                row_list[3] = 7  # Orografía
                row_list[4] = 1  # Ambiente y desarrollo sostenible 
            elif row_list[2] == 8100 and row_list[3] == 8918  :
                row_list[2] = 1  # Ambiente y desarrollo sostenible
                row_list[3] = 7  # Orografía
                row_list[4] = 1  # Ambiente y desarrollo sostenible 
            elif row_list[2] == 8100 and row_list[3] == 8121  :
                row_list[2] = 1  # Ambiente y desarrollo sostenible
                row_list[3] = 7  # Orografía
                row_list[4] = 1  # Ambiente y desarrollo sostenible 
            elif row_list[2] == 8100 and row_list[3] == 8122  :
                row_list[2] = 1  # Ambiente y desarrollo sostenible
                row_list[3] = 7  # Orografía
                row_list[4] = 1  # Ambiente y desarrollo sostenible 
            elif row_list[2] == 8100 and row_list[3] == 8123  :
                row_list[2] = 1  # Ambiente y desarrollo sostenible
                row_list[3] = 7  # Orografía
                row_list[4] = 1  # Ambiente y desarrollo sostenible 
            elif row_list[2] == 8100 and row_list[3] == 8125  :
                row_list[2] = 1  # Ambiente y desarrollo sostenible
                row_list[3] = 7  # Orografía
                row_list[4] = 1  # Ambiente y desarrollo sostenible 
            elif row_list[2] == 8100 and row_list[3] == 8126  :
                row_list[2] = 1  # Ambiente y desarrollo sostenible
                row_list[3] = 7  # Orografía
                row_list[4] = 1  # Ambiente y desarrollo sostenible 
            elif row_list[2] == 8100 and row_list[3] == 8127  :
                row_list[2] = 1  # Ambiente y desarrollo sostenible
                row_list[3] = 7  # Orografía
                row_list[4] = 1  # Ambiente y desarrollo sostenible 
            elif row_list[2] == 8100 and row_list[3] == 8128  :
                row_list[2] = 1  # Ambiente y desarrollo sostenible
                row_list[3] = 7  # Orografía
                row_list[4] = 1  # Ambiente y desarrollo sostenible 
            elif row_list[2] == 8100 and row_list[3] == 8129  :
                row_list[2] = 1  # Ambiente y desarrollo sostenible
                row_list[3] = 7  # Orografía
                row_list[4] = 1  # Ambiente y desarrollo sostenible 
            elif row_list[2] == 8100 and row_list[3] == 8130  :
                row_list[2] = 1  # Ambiente y desarrollo sostenible
                row_list[3] = 7  # Orografía
                row_list[4] = 1  # Ambiente y desarrollo sostenible 
            elif row_list[2] == 8100 and row_list[3] == 8136  :
                row_list[2] = 1  # Ambiente y desarrollo sostenible
                row_list[3] = 7  # Orografía
                row_list[4] = 1  # Ambiente y desarrollo sostenible 

            elif row_list[2] == 5115   :
                row_list[2] = 1  # Ambiente y desarrollo sostenible
                row_list[3] = 8  # Deposito de agua
                row_list[4] = 1  # Ambiente y desarrollo sostenible 
            elif row_list[2] == 8400 and row_list[3] == 8417  :
                row_list[2] = 1  # Ambiente y desarrollo sostenible
                row_list[3] = 8  # Deposito de agua
                row_list[4] = 1  # Ambiente y desarrollo sostenible 
            elif row_list[2] == 8400 and row_list[3] == 8403  :
                row_list[2] = 1  # Ambiente y desarrollo sostenible
                row_list[3] = 8  # Deposito de agua
                row_list[4] = 1  # Ambiente y desarrollo sostenible 
            elif row_list[2] == 8400 and row_list[3] == 8413  :
                row_list[2] = 1  # Ambiente y desarrollo sostenible
                row_list[3] = 8  # Deposito de agua
                row_list[4] = 1  # Ambiente y desarrollo sostenible 
            elif row_list[2] == 5113   :
                row_list[2] = 1  # Ambiente y desarrollo sostenible
                row_list[3] = 8  # Deposito de agua
                row_list[4] = 1  # Ambiente y desarrollo sostenible
            elif row_list[2] == 8400 and row_list[3] == 8418  :
                row_list[2] = 1  # Ambiente y desarrollo sostenible
                row_list[3] = 8  # Deposito de agua
                row_list[4] = 1  # Ambiente y desarrollo sostenible 
            elif row_list[2] == 5112  :
                row_list[2] = 1  # Ambiente y desarrollo sostenible
                row_list[3] = 8  # Deposito de agua
                row_list[4] = 1  # Ambiente y desarrollo sostenible 
            elif row_list[2] == 5114  :
                row_list[2] = 1  # Ambiente y desarrollo sostenible
                row_list[3] = 8  # Deposito de agua
                row_list[4] = 1  # Ambiente y desarrollo sostenible 
            elif row_list[2] == 8400 and row_list[3] == 8432  :
                row_list[2] = 1  # Ambiente y desarrollo sostenible
                row_list[3] = 8  # Deposito de agua
                row_list[4] = 1  # Ambiente y desarrollo sostenible 
            elif row_list[2] == 5206   :
                row_list[2] = 1  # Ambiente y desarrollo sostenible
                row_list[3] = 10  # Isla
                row_list[4] = 1  # Ambiente y desarrollo sostenible 

            elif row_list[2] == 8100 and row_list[3] == 8135  :
                row_list[2] = 1  # Ambiente y desarrollo sostenible
                row_list[3] = 12  # Paramo
                row_list[4] = 1  # Ambiente y desarrollo sostenible 
            elif row_list[2] == 8400 and row_list[3] == 8410  :
                row_list[2] = 1  # Ambiente y desarrollo sostenible
                row_list[3] = 17  # Brazo
                row_list[4] = 1  # Ambiente y desarrollo sostenible 
            elif row_list[2] == 2307  :
                row_list[2] = 4  # Deporte y recreacion
                row_list[3] = 1  # Practica deportiva
                row_list[4] = 4  # Deporte y recreacion
            elif row_list[2] == 3410  :
                row_list[2] = 9  # Transporte
                row_list[3] = 3 # Tunel
                row_list[4] = 9  # Transporte 
            elif row_list[2] == 3201  :
                row_list[2] = 9  # Transporte
                row_list[3] = 5 # Aeropuerto
                row_list[4] = 9  # Transporte 
            elif row_list[2] == 3203  :
                row_list[2] = 9  # Transporte
                row_list[3] = 8 # Helipuerto
                row_list[4] = 9  # Transporte 
            elif row_list[2] == 3402  :
                row_list[2] = 9  # Transporte
                row_list[3] = 9 # Peaje
                row_list[4] = 9  # Transporte
            elif row_list[2] == 3202  :
                row_list[2] = 9  # Transporte
                row_list[3] = 10 # Pista de aterrizaje
                row_list[4] = 9  # Transporte 
            elif row_list[2] == 3401  :
                row_list[2] = 9  # Transporte
                row_list[3] = 13 # Terminal terrestre
                row_list[4] = 9  # Transporte 
            elif row_list[2] == 7101 and row_list[3] == 8317  :
                row_list[2] = 10  # Unidad administrativa
                row_list[3] = 1  # Republica
                row_list[4] = 10  # Unidad administrativa
            elif row_list[2] == 7101 and row_list[3] == 8309  :
                row_list[2] = 10  # Unidad administrativa
                row_list[3] = 2  # Republica
                row_list[4] = 10  # Unidad administrativa
            elif row_list[2] == 7101 and row_list[3] == 8310  :
                row_list[2] = 10  # Unidad administrativa
                row_list[3] = 3  # Distrito
                row_list[4] = 10  # Unidad administrativa
            elif row_list[2] == 7101 and row_list[3] == 8301  :
                row_list[2] = 10  # Unidad administrativa
                row_list[3] = 4  # Area metropolitana
                row_list[4] = 10  # Unidad administrativa
            elif row_list[2] == 7101 and row_list[3] == 8312  :
                row_list[2] = 10  # Unidad administrativa
                row_list[3] = 5  # Municipio
                row_list[4] = 10  # Unidad administrativa
            elif row_list[2] == 7101 and row_list[3] == 8304  :
                row_list[2] = 10  # Unidad administrativa
                row_list[3] = 6  # Cabecera municipal
                row_list[4] = 10  # Unidad administrativa
            elif row_list[2] == 7101 and row_list[3] == 8326  :
                row_list[2] = 10  # Unidad administrativa
                row_list[3] = 7  # entro poblado
                row_list[4] = 10  # Unidad administrativa
            elif row_list[2] == 7101 and row_list[3] ==  8324 :
                row_list[2] = 10  # Unidad administrativa
                row_list[3] = 8  # Capital
                row_list[4] = 10  # Unidad administrativa
            elif row_list[2] == 7101 and row_list[3] == 8307  :
                row_list[2] = 10  # Unidad administrativa
                row_list[3] = 9  # Corregimiento
                row_list[4] = 10  # Unidad administrativa
            elif row_list[2] == 7101 and row_list[3] == 8311  :
                row_list[2] = 10  # Unidad administrativa
                row_list[3] =  11  # Localidad
                row_list[4] = 10  # Unidad administrativa
            elif row_list[2] == 7101 and row_list[3] == 8303  :
                row_list[2] = 10  # Unidad administrativa
                row_list[3] = 12  # barrio
                row_list[4] = 10  # Unidad administrativa
            elif row_list[2] == 7101 and row_list[3] == 8327  :
                row_list[2] = 10  # Unidad administrativa
                row_list[3] = 13  # Sector
                row_list[4] = 10  # Unidad administrativa
            elif row_list[2] == 7101 and row_list[3] == 8322  :
                row_list[2] = 10  # Unidad administrativa
                row_list[3] = 14  # Vereda
                row_list[4] = 10  # Unidad administrativa
            elif row_list[2] == 7101 and row_list[3] == 8328  :
                row_list[2] = 10  # Unidad administrativa
                row_list[3] = 15  # Comuna
                row_list[4] = 10  # Unidad administrativa
            elif row_list[2] == 7101 and row_list[3] == 8305  :
                row_list[2] = 11 # Vivivenda ciudad y territorio
                row_list[3] = 1  # Cacerio
                row_list[4] = 11  # Vivivenda ciudad y territorio
            elif row_list[2] == 7101 and row_list[3] == 8350  :
                row_list[2] = 11  # Vivivenda ciudad y territorio
                row_list[3] = 2  # Urbanizacion
                row_list[4] = 11  # Vivivenda ciudad y territorio
            elif row_list[2] == 7101 and row_list[3] == 8318  :
                row_list[2] = 11 # Vivivenda ciudad y territorio
                row_list[3] = 3  # Reserva indigena
                row_list[4] = 11  # Vivivenda ciudad y territorio
            elif row_list[2] == 7101 and row_list[3] == 8320  :
                row_list[2] = 11  # Vivivenda ciudad y territorio
                row_list[3] = 3  # Reserva indigena
                row_list[4] = 11  # Vivivenda ciudad y territorio
            elif row_list[2] == 7101 and row_list[3] == 8306  :
                row_list[2] = 11 # Vivivenda ciudad y territorio
                row_list[3] = 4  # Territorios Colectivos de Comunidades Negras
                row_list[4] = 11  # Vivivenda ciudad y territorio

            elif row_list[2] == 2306 :
                row_list[2] = 11  # Vivivenda ciudad y territorio
                row_list[3] = 6  # Sitio de interez
                row_list[4] = 11  # Vivivenda ciudad y territorio
            elif row_list[2] == 2309  :
                row_list[2] = 11 # Vivivenda ciudad y territorio
                row_list[3] = 6  # Sitio de interez
                row_list[4] = 11  # Vivivenda ciudad y territorio
            elif row_list[2] == 7101 and row_list[3] == 8351  :
                row_list[2] = 11  # Vivivenda ciudad y territorio
                row_list[3] = 6   # Sitio de interez
                row_list[4] = 11  # Vivivenda ciudad y territorio
            else:
                pass
            row=tuple(row_list)
            iCur.insertRow(row)
registrosmigrados(i, "Nombre_Geografico")

edit.stopOperation()
edit.stopEditing(True)
arcpy.AddMessage("{0} ¡Proceso finalizado con exito!:".format(arrow))
