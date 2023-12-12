import os
import pandas as pd
import io
from io import StringIO
import re
import csv

def extraer_fecha(valor_fecha):
    model= re.compile(r'(\d{4}\.\d{2}\.\d{2})')
    match_date = model.search(valor_fecha)
    return match_date.group(1) if match_date else None

def archivos_GSI(file_path,txt_file_path,txt_file_path_error ):#file_path,txt_file_path,txt_file_path_error
    dataframes = []
    lista_errores = []
    
    for archivo in os.listdir(file_path):
            ruta_completa = os.path.join(file_path, archivo)
            print(f'Archivo: {archivo}')
            df = pd.read_csv(ruta_completa, sep=' ', skiprows=1, header=None, names=['Column1', 'Column2', 'Column3', 'Column4', 'Column5', 'Column6','Column7'])
            df_process=pd.DataFrame()
            df_process_2=pd.DataFrame()
            #df.to_excel(txt_file_path)
            
            
            indices_principio = df[df['Column1'].str.contains(r'\+?\.\.\.\.\.\.1')].index
            #indices_final = df[df['Column3'].str.contains(r'Final linea')].index
            for indice_principio in indices_principio:
                indice_siguiente_principio = indice_principio  + 1
                indice_siguiente_final = indice_principio - 1
                if indice_siguiente_principio < len(df):
                    nuevo_valor = df.loc[indice_siguiente_principio, 'Column1']
                    nuevo_valor_zinicial = df.loc[indice_siguiente_principio, 'Column2']
                    nuevo_valor_final = df.loc[indice_siguiente_final, 'Column1']
                    nuevo_valor_distancia = df.loc[indice_siguiente_final, 'Column3']
                    nuevo_valor_zfinal = df.loc[indice_siguiente_final, 'Column4']
                    #nuevo_valor_z = df.loc[indice_siguiente_principio, 'Column6']                     
                    df_process.loc[indice_principio, 'Principio_Linea'] = nuevo_valor
                    df_process.loc[indice_principio, 'Fin_Linea'] = nuevo_valor_final
                    df_process.loc[indice_principio, 'distancia(m)'] = nuevo_valor_distancia
                    df_process.loc[indice_principio, 'desnivel_final'] = nuevo_valor_zfinal
                    df_process.loc[indice_principio, 'desnivel_inicial'] = nuevo_valor_zinicial
            if len(indices_principio) > 1 :
                df_process['Principio_Linea'] = df_process['Principio_Linea'].str.split('+', n=1).str[1]
                df_process['Fin_Linea'] = df_process['Fin_Linea'].str.split('+', n=1).str[1]
                #df_process['desnivel_final'] = df_process['desnivel_final'].str[:]
                df_process['signo'] = df_process['desnivel_final'].str.extract(r'([+-])')
                df_process['desnivel_inicial'] = df_process['desnivel_inicial'].str.split('+', n=1).str[1]
                df_process['desnivel_inicial'] = pd.to_numeric(df_process['desnivel_inicial'])
                df_process['distancia(m)'] = df_process['distancia(m)'].str.split('+', n=1).str[1]
                df_process['desnivel_final'] = df_process['desnivel_final'].str.split(r'([+-])', n=1).str[2]
                # Utiliza la función str.slice para obtener los primeros len - 4 caracteres
                df_process['nueva_columna'] = df_process['desnivel_final'].str.slice(0, -4)

                # Agrega un punto después del cuarto carácter desde el final
                df_process['nueva_columna'] += '.' + df_process['desnivel_final'].str.slice(-4)
                df_process['desnivel_final'] = pd.to_numeric(df_process['nueva_columna'])
                df_process['desnivel(m)'] =df_process['desnivel_final'] - df_process['desnivel_inicial']
                df_process['Consistencia'] = df_process.apply(lambda row: 'INICIO ERRADO' if row['desnivel(m)'] != row['desnivel_final'] else 'INICIO EN CERO', axis=1)
                df_process['desnivel(m)'] = df_process['signo']+(df_process['desnivel_final'] - df_process['desnivel_inicial']).astype(str)
                df_process['Nombre Archivo'] = archivo
                orden_columnas = ['Principio_Linea', 'Fin_Linea','desnivel(m)','distancia(m)','Consistencia','Nombre Archivo']
                df_process = df_process[orden_columnas]
                dataframes.append(df_process)
            else:
                lista_errores.append(archivo)
    # Concatenar todos los DataFrames en uno solo
    df_resultado = pd.concat(dataframes, ignore_index=True)
    df_resultado.to_excel(txt_file_path+'/'+'Table_GSI.xlsx')
    with open(txt_file_path_error+ '/'+'Error_GSI.txt', 'w') as archivo:
        archivo.write("Archivos error, revisar los siguientes archivos:\n")
        # Escribe cada elemento de la lista en una línea del archivo
        for list in lista_errores:
            archivo.write(str(list) + '\n')

def arvchivos_DAT(file_path,txt_file_path,txt_file_path_error):
    dataframes = []
    lista_errores = []
    for archivo in os.listdir(file_path):
            ruta_completa = os.path.join(file_path, archivo)
            print(f'Archivo: {archivo}')
            # Después de cargar el DataFrame df
            df = pd.read_csv(ruta_completa, sep='|', skiprows=1, header=None, names=['Column1', 'Column2', 'Column3', 'Column4', 'Column5', 'Column6', 'Column7'])
            df_process=pd.DataFrame()
            df_process_2=pd.DataFrame()

            #Identificar Ajustes,Principio Linea,Final linea
            conteo_ajustes = df['Column3'].str.contains(r'Ajustes').sum()
            conteo_principio = df['Column3'].str.contains(r'Principio Linea').sum()
            conteo_final = df['Column3'].str.contains(r'Final linea').sum()
            if conteo_principio == conteo_final:
                pattern = r'(\d+\.\d+)'
                # Encontrar la primera ocurrencia de 'Ajustes'
                indice_ajustes = df[df['Column3'].str.contains(r'Ajustes')].index[0] if conteo_ajustes > 0 else ('Revisar conteo_ajuste')#Fecha
                
                indices_principio = df[df['Column3'].str.contains(r'Principio Linea')].index
                indices_final = df[df['Column3'].str.contains(r'Final linea')].index
                for indice_principio in indices_principio:
                    indice_siguiente_principio = indice_principio  + 1
                    if indice_siguiente_principio < len(df):
                        nuevo_valor = df.loc[indice_siguiente_principio, 'Column3']
                        nuevo_valor_z = df.loc[indice_siguiente_principio, 'Column6']                     
                        df_process.loc[indice_principio, 'Principio_Linea'] = nuevo_valor
                        df_process.loc[indice_principio, 'Z_inicial'] = nuevo_valor_z
                for indice_final in indices_final:
                    indice_anterior_fin = indice_final - 1
                    if indice_anterior_fin < len(df):
                        nuevo_valor_fin = df.loc[indice_anterior_fin, 'Column3'] 
                        nuevo_valor_Z_fin = df.loc[indice_anterior_fin, 'Column6'] 
                        nuevo_valor_in_fin = df.loc[indice_anterior_fin, 'Column4'] 
                        nuevo_valor_end_fin = df.loc[indice_anterior_fin, 'Column5']  
                        df_process_2.loc[indice_anterior_fin, 'Fin_Linea'] = nuevo_valor_fin
                        df_process_2.loc[indice_anterior_fin, 'Z_Final'] = nuevo_valor_Z_fin  
                        df_process_2.loc[indice_anterior_fin, 'Distiancia_inicial'] = nuevo_valor_in_fin  
                        df_process_2.loc[indice_anterior_fin, 'Distancia_final'] = nuevo_valor_end_fin
                        
                        df_process_2['Distiancia_inicial'] = df_process_2['Distiancia_inicial'].str.extract(pattern)
                        df_process_2['Distancia_final'] = df_process_2['Distancia_final'].str.extract(pattern)
                        df_process_2['Z_Final'] = df_process_2['Z_Final'].str.extract(pattern)

                df_process_2['Z_Final'] = pd.to_numeric(df_process_2['Z_Final'], errors='coerce')
                df_process_2['Distiancia_inicial'] = pd.to_numeric(df_process_2['Distiancia_inicial'], errors='coerce')
                df_process_2['Distancia_final'] = pd.to_numeric(df_process_2['Distancia_final'], errors='coerce')
                df_process_2['Distance(m)']= (df_process_2['Distancia_final'] + df_process_2['Distiancia_inicial'])/1000 

                df_process['Distance(m)'] = df_process_2['Distance(m)'].values
                df_process['Z_Final'] = df_process_2['Z_Final'].values 
                df_process['Fin_Linea'] = df_process_2['Fin_Linea'].values
                
                df_process['Z_inicial'] = df_process['Z_inicial'].str.extract(pattern)
                df_process['Z_inicial'] = pd.to_numeric(df_process['Z_inicial'], errors='coerce')
                df_process['Desnivel_Observado'] = df_process['Z_Final'] - df_process['Z_inicial']
                df_process['Consistencia'] = df_process.apply(lambda row: 'INICIO ERRADO' if row['Desnivel_Observado'] != row['Z_Final'] else 'INICIO EN CERO', axis=1)
                df_process['Principio_Linea'] = df_process['Principio_Linea'].str.replace(r'\s+', '-', regex=True)
                # Eliminar todo lo que está antes del primer '-' y después del último '-'
                df_process['Principio_Linea'] = df_process['Principio_Linea'].str.split('-', n=1).str[1].str.rsplit('-', n=1).str[0]
                # Eliminar los últimos cinco caracteres
                df_process['Principio_Linea'] = df_process['Principio_Linea'].str[:-5]

                df_process['Principio_Linea'] = df_process['Principio_Linea'].str.replace(r'-', ' ', regex=True)


                df_process['Fin_Linea'] = df_process['Fin_Linea'].str.replace(r'\s+', '-', regex=True)
                # Eliminar todo lo que está antes del primer '-' y después del último '-'
                df_process['Fin_Linea'] = df_process['Fin_Linea'].str.split('-', n=1).str[1].str.rsplit('-', n=2).str[0]
                # Eliminar los últimos cinco caracteres
                df_process['Fin_Linea'] = df_process['Fin_Linea'].str[:-5]

                df_process['Fin_Linea'] = df_process['Fin_Linea'].str.replace(r'-', ' ', regex=True)

                #Fecha
                if indice_ajustes is not None:
                    indice_siguiente_fila = indice_ajustes + 1
                    if indice_siguiente_fila < len(df):
                        df_process['Fecha'] = df.loc[indice_siguiente_fila, 'Column3'] 

                # Expresión regular para extraer la fecha
                regex_fecha =  re.compile(r'(\d{4}\.\d{2}\.\d{2})')
                # Aplicar la expresión regular para extraer la fecha en una nueva columna
                df_process['Fecha'] = df_process['Fecha'].str.extract(regex_fecha)
                #df_process['Fecha'] = df_process['Fecha'].str.replace(r'.', '/', regex=True)
                df_process['Nombre Archivo'] = archivo
                orden_columnas = ['Fecha', 'Principio_Linea', 'Fin_Linea','Desnivel_Observado','Distance(m)','Consistencia','Nombre Archivo']
                df_process = df_process[orden_columnas]
                #df_process = df_process.dropna(subset=['Principio_Linea'])    
                #df.to_excel(txt_file_path)
                print(df)
                # Anexar el DataFrame de esta iteración a la lista
                dataframes.append(df_process)
            else:
                lista_errores.append(archivo)
    # Concatenar todos los DataFrames en uno solo
    df_resultado = pd.concat(dataframes, ignore_index=True)
    df_resultado.to_excel(txt_file_path+'/'+'Table_DAT.xlsx')
    with open(txt_file_path_error, 'w') as archivo:
        archivo.write("Archivos error, el posible error es que no se cierra el punto(Fin_linea):\n")
        # Escribe cada elemento de la lista en una línea del archivo
        for list in lista_errores:
            archivo.write(str(list) + '\n')

def main():
    file_path_DAT = 'C:\\Users\\Juanm\\Documents\\Proyectos_IGAC\\Automatizacion_geodesia\\DAT_2016\\2016'
    file_path_GSI = 'C:\\Users\\Juanm\\Documents\\Proyectos_IGAC\\Automatizacion_geodesia\\GSI_2008\\2008'
    txt_file_path = 'C:/Users/Juanm/Documents/Proyectos_IGAC/Automatizacion_geodesia/DAT_2016/pruebas'
    txt_file_path_error = 'C:/Users/Juanm/Documents/Proyectos_IGAC/Automatizacion_geodesia/DAT_2016/pruebas'
    #ruta_completa = 'C:/Users/Juanm/Documents/Proyectos_IGAC/Automatizacion_geodesia/DAT_2016/archivos_problemas/160727MM.DAT'
    #arvchivos_DAT(file_path_DAT,txt_file_path,txt_file_path)
    archivos_GSI(file_path_GSI,txt_file_path,txt_file_path_error )
    # dataframes = []
    # lista_errores = []
    # for archivo in os.listdir(file_path):
    #         ruta_completa = os.path.join(file_path, archivo)
    #         print(f'Archivo: {archivo}')
    #         # Después de cargar el DataFrame df
    #         df = pd.read_csv(ruta_completa, sep='|', skiprows=1, header=None, names=['Column1', 'Column2', 'Column3', 'Column4', 'Column5', 'Column6', 'Column7'])
    #         df_process=pd.DataFrame()
    #         df_process_2=pd.DataFrame()

    #         #Identificar Ajustes,Principio Linea,Final linea
    #         conteo_ajustes = df['Column3'].str.contains(r'Ajustes').sum()
    #         conteo_principio = df['Column3'].str.contains(r'Principio Linea').sum()
    #         conteo_final = df['Column3'].str.contains(r'Final linea').sum()
    #         if conteo_principio == conteo_final:
    #             pattern = r'(\d+\.\d+)'
    #             # Encontrar la primera ocurrencia de 'Ajustes'
    #             indice_ajustes = df[df['Column3'].str.contains(r'Ajustes')].index[0] if conteo_ajustes > 0 else ('Revisar conteo_ajuste')#Fecha
                
    #             indices_principio = df[df['Column3'].str.contains(r'Principio Linea')].index
    #             indices_final = df[df['Column3'].str.contains(r'Final linea')].index
    #             for indice_principio in indices_principio:
    #                 indice_siguiente_principio = indice_principio  + 1
    #                 if indice_siguiente_principio < len(df):
    #                     nuevo_valor = df.loc[indice_siguiente_principio, 'Column3']
    #                     nuevo_valor_z = df.loc[indice_siguiente_principio, 'Column6']                     
    #                     df_process.loc[indice_principio, 'Principio_Linea'] = nuevo_valor
    #                     df_process.loc[indice_principio, 'Z_inicial'] = nuevo_valor_z
    #             for indice_final in indices_final:
    #                 indice_anterior_fin = indice_final - 1
    #                 if indice_anterior_fin < len(df):
    #                     nuevo_valor_fin = df.loc[indice_anterior_fin, 'Column3'] 
    #                     nuevo_valor_Z_fin = df.loc[indice_anterior_fin, 'Column6'] 
    #                     nuevo_valor_in_fin = df.loc[indice_anterior_fin, 'Column4'] 
    #                     nuevo_valor_end_fin = df.loc[indice_anterior_fin, 'Column5']  
    #                     df_process_2.loc[indice_anterior_fin, 'Fin_Linea'] = nuevo_valor_fin
    #                     df_process_2.loc[indice_anterior_fin, 'Z_Final'] = nuevo_valor_Z_fin  
    #                     df_process_2.loc[indice_anterior_fin, 'Distiancia_inicial'] = nuevo_valor_in_fin  
    #                     df_process_2.loc[indice_anterior_fin, 'Distancia_final'] = nuevo_valor_end_fin
                        
    #                     df_process_2['Distiancia_inicial'] = df_process_2['Distiancia_inicial'].str.extract(pattern)
    #                     df_process_2['Distancia_final'] = df_process_2['Distancia_final'].str.extract(pattern)
    #                     df_process_2['Z_Final'] = df_process_2['Z_Final'].str.extract(pattern)

    #             df_process_2['Z_Final'] = pd.to_numeric(df_process_2['Z_Final'], errors='coerce')
    #             df_process_2['Distiancia_inicial'] = pd.to_numeric(df_process_2['Distiancia_inicial'], errors='coerce')
    #             df_process_2['Distancia_final'] = pd.to_numeric(df_process_2['Distancia_final'], errors='coerce')
    #             df_process_2['Distance(m)']= (df_process_2['Distancia_final'] + df_process_2['Distiancia_inicial'])/1000 

    #             df_process['Distance(m)'] = df_process_2['Distance(m)'].values
    #             df_process['Z_Final'] = df_process_2['Z_Final'].values 
    #             df_process['Fin_Linea'] = df_process_2['Fin_Linea'].values
                
    #             df_process['Z_inicial'] = df_process['Z_inicial'].str.extract(pattern)
    #             df_process['Z_inicial'] = pd.to_numeric(df_process['Z_inicial'], errors='coerce')
    #             df_process['Desnivel_Observado'] = df_process['Z_Final'] - df_process['Z_inicial']
    #             df_process['Consistencia'] = df_process.apply(lambda row: 'INICIO ERRADO' if row['Desnivel_Observado'] != row['Z_Final'] else 'INICIO EN CERO', axis=1)
    #             df_process['Principio_Linea'] = df_process['Principio_Linea'].str.replace(r'\s+', '-', regex=True)
    #             # Eliminar todo lo que está antes del primer '-' y después del último '-'
    #             df_process['Principio_Linea'] = df_process['Principio_Linea'].str.split('-', n=1).str[1].str.rsplit('-', n=1).str[0]
    #             # Eliminar los últimos cinco caracteres
    #             df_process['Principio_Linea'] = df_process['Principio_Linea'].str[:-5]

    #             df_process['Principio_Linea'] = df_process['Principio_Linea'].str.replace(r'-', ' ', regex=True)


    #             df_process['Fin_Linea'] = df_process['Fin_Linea'].str.replace(r'\s+', '-', regex=True)
    #             # Eliminar todo lo que está antes del primer '-' y después del último '-'
    #             df_process['Fin_Linea'] = df_process['Fin_Linea'].str.split('-', n=1).str[1].str.rsplit('-', n=2).str[0]
    #             # Eliminar los últimos cinco caracteres
    #             df_process['Fin_Linea'] = df_process['Fin_Linea'].str[:-5]

    #             df_process['Fin_Linea'] = df_process['Fin_Linea'].str.replace(r'-', ' ', regex=True)

    #             #Fecha
    #             if indice_ajustes is not None:
    #                 indice_siguiente_fila = indice_ajustes + 1
    #                 if indice_siguiente_fila < len(df):
    #                     df_process['Fecha'] = df.loc[indice_siguiente_fila, 'Column3'] 

    #             # Expresión regular para extraer la fecha
    #             regex_fecha =  re.compile(r'(\d{4}\.\d{2}\.\d{2})')
    #             # Aplicar la expresión regular para extraer la fecha en una nueva columna
    #             df_process['Fecha'] = df_process['Fecha'].str.extract(regex_fecha)
    #             #df_process['Fecha'] = df_process['Fecha'].str.replace(r'.', '/', regex=True)
    #             df_process['Nombre Archivo'] = archivo
    #             orden_columnas = ['Fecha', 'Principio_Linea', 'Fin_Linea','Desnivel_Observado','Distance(m)','Consistencia','Nombre Archivo']
    #             df_process = df_process[orden_columnas]
    #             #df_process = df_process.dropna(subset=['Principio_Linea'])    
    #             #df.to_excel(txt_file_path)
    #             print(df)
    #             # Anexar el DataFrame de esta iteración a la lista
    #             dataframes.append(df_process)
    #         else:
    #             lista_errores.append(archivo)
    # # Concatenar todos los DataFrames en uno solo
    # df_resultado = pd.concat(dataframes, ignore_index=True)
    # df_resultado.to_excel(txt_file_path)
    # with open(txt_file_path_error, 'w') as archivo:
    #     archivo.write("Archivos error, el posible error es que no se cierra el punto(Fin_linea):\n")
    #     # Escribe cada elemento de la lista en una línea del archivo
    #     for list in lista_errores:
    #         archivo.write(str(list) + '\n')
if __name__ == "__main__":
    main()