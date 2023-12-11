## CODIGO PARA PASAR DE MDB A GDB

import arcpy 
import os

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

def registrosmigrados(x, ly_migrado):
 arcpy.AddMessage("    Han sido migrados {0} registros al Feature {1}.".format(x, ly_migrado))

arcpy.AddMessage("\n{0} ...INICIANDO PROCESO DE MIGRACION de MDB a GDB... {1}.".format(sep, sep))
arcpy.AddMessage("{0}{1}{2}\n".format(sep, sep,sep))
arcpy.AddMessage("{0} Nombres Geográficos... ".format(hasht))
edit = arcpy.da.Editor(GDB_output)
edit.startEditing(False, True)
edit.startOperation()
i=0

lista_mdbs = os.listdir(GDB_input)

for a in lista_mdbs:
        if a.endswith(".mdb"):
            mdb = os.path.join(GDB_input,a)
            arcpy.env.workspace=mdb
            featureclasses = arcpy.ListFeatureClasses()

            for fc in featureclasses: 
             
             arcpy.management.RepairGeometry(fc,True)
             arcpy.AddMessage ("Geometria arreglada de: {0}".format(str(fc)))

            #     # Definir el código de proyección personalizado
            #     sr = 'PROJCS["PCS_MAGNA_Ant_Betania",GEOGCS["GCS_MAGNA",DATUM["D_MAGNA",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",1121903.562],PARAMETER["False_Northing",1127263.005],PARAMETER["Central_Meridian",-75.0],PARAMETER["Scale_Factor",1.0],PARAMETER["Latitude_Of_Origin",5.74597389],UNIT["Meter",1.0]]'
               
            #     arcpy.management.DefineProjection(fc,sr)
            #     arcpy.AddMessage ("Capa reproyectada: {0}".format(str(fc)))

            arcpy.AddMessage("MDB a Migrar" + mdb)
            edit = arcpy.da.Editor(GDB_output)
            edit.startEditing(False, True)
            edit.startOperation()
            i=0
            # arcpy.AddMessage("\n Migrando IB")
            # with arcpy.da.SearchCursor(os.path.join(mdb,'IB'),['SHAPE@','IDE','ENT_GEO','ATRIB','TOPONIMO','ATRIB']) as sCur:
            #     with arcpy.da.InsertCursor(os.path.join(GDB_output, 'IB'),['SHAPE@','IDE','ENT_GEO','ATRIB','TOPONIMO','VIGENCIA']) as iCur:
            #         i=0
            #         for row in sCur:
            #             i = i+1
            #             row_list= list(row)
            #             row_list[0]= row[0].projectAs('9377')
            #             #row_list[5] = int(a[-11:-7])
            #             row=tuple(row_list)
            #             iCur.insertRow(row)
            # registrosmigrados(i, "IB")
            arcpy.AddMessage("\n Migrando CEA")
            with arcpy.da.SearchCursor(os.path.join(mdb,'CEA'),['SHAPE@','IDE','ENT_GEO','ATRIB','TOPONIMO','ATRIB']) as sCur:
                with arcpy.da.InsertCursor(os.path.join(GDB_output, 'CEA'),['SHAPE@','IDE','ENT_GEO','ATRIB','TOPONIMO','VIGENCIA']) as iCur:
                    i=0
                    for row in sCur:
                        i = i+1
                        row_list= list(row)
                        row_list[0]= row[0].projectAs('9377')
                        #row_list[5] = int(a[-11:-7])
                        row=tuple(row_list)
                        iCur.insertRow(row)
            registrosmigrados(i, 'CEA')
            #arcpy.AddMessage("\n Migrando IB_P")
            # with arcpy.da.SearchCursor(os.path.join(mdb,'IB_P'),['SHAPE@','IDE','ENT_GEO','ORDEN','ATRIB','TOPONIMO','ATRIB']) as sCur:
            #     with arcpy.da.InsertCursor(os.path.join(GDB_output, 'IB_P'),['SHAPE@','IDE','ENT_GEO','ORDEN','ATRIB','TOPONIMO','VIGENCIA']) as iCur:
            #         i=0
            #         for row in sCur:
            #             i = i+1
            #             row_list= list(row)
            #             row_list[0]= row[0].projectAs('9377')
            #             #row_list[6] = int(a[-11:-7])
            #             row=tuple(row_list)
            #             iCur.insertRow(row)
            # registrosmigrados(i, "IB_P")
            arcpy.AddMessage("\n Migrando CDV_P")
            with arcpy.da.SearchCursor(os.path.join(mdb,'CVD_P'),['SHAPE@','IDE','ENT_GEO','ORDEN','ATRIB','TOPONIMO','ATRIB']) as sCur:
                with arcpy.da.InsertCursor(os.path.join(GDB_output, 'CVD_P'),['SHAPE@','IDE','ENT_GEO','ORDEN','ATRIB','TOPONIMO','VIGENCIA']) as iCur:
                    i=0
                    for row in sCur:
                        i = i+1
                        row_list= list(row)
                        row_list[0]= row[0].projectAs('9377')
                        #row_list[6] = int(a[-11:-7])
                        row=tuple(row_list)
                        iCur.insertRow(row)
            registrosmigrados(i, "CDV_P")
            arcpy.AddMessage("\n Migrando NOMENCLATURA")
            with arcpy.da.SearchCursor(os.path.join(mdb,'NOMENCLATURA'),['SHAPE@','NOM_C','OBSERVA']) as sCur:
                with arcpy.da.InsertCursor(os.path.join(GDB_output, 'NOMENCLATURA'),['SHAPE@','NOM_C','OBSERVA']) as iCur:
                    i=0
                    for row in sCur:
                        i = i+1
                        row_list= list(row)
                        row_list[0]= row[0].projectAs('9377')
                        #row_list[3] = int(a[-11:-7])
                        row=tuple(row_list)
                        iCur.insertRow(row)
            registrosmigrados(i, "Nomenclatura")
            edit.stopOperation()
            edit.stopEditing(True)
        else:
            pass 

arcpy.AddMessage("{0} ¡Proceso finalizado con exito!:".format(arrow))
