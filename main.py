import myutil
import os
import re
import pandas as pd

if __name__ == '__main__':

    # Nos cambiamos de directorio a donde se deben dejar los pdfs
    os.chdir('./pdf_files/')
    os.system('rm s_*')
    os.system('rm signature.pdf')
    os.system('touch demo.txt')

    # Arreglos que almacenarán los datos
    proyecto = []
    fase = []
    valor = []
    corrVal = []
    nedpVal = []
    fileName = []

    # Recorre todos los archivos de la carpeta
    for file in os.listdir('.'):

        # Solo se procesan los archivos .pdf
        if file.endswith('.pdf') and not file.startswith('s_'):
            
            # Solo tiene sentido procesar "largos" mayores que 6 letras
            if len(file) > 6:
                # Obtenemos el correlativo. Típico A1, A2, A3, etc.
                correlativo = re.findall("\(\w+\)", file)[0]
                correlativo = correlativo.replace(')', '').replace('(', '')
                
                # Obtenemos el Nro de EDP
                nedp = re.findall("EP\d{1}", file)[0]

                # Se obtienen los datos de la EDP                
                filedata = myutil.getEdpData(file)

                # Si es válido, se procede
                if filedata['estado'] == 'OK':
                    print(
                        u"\nProyecto: {0} \t| Fase: {1} \t| Monto: {2} \t| Correlativo: {3} \t| N°: {4}".format(
                            filedata["proyecto"],
                            filedata["fase"],
                            filedata["valor"],
                            correlativo,
                            nedp
                        )
                    )
                    fileName.append(file)
                    proyecto.append(filedata["proyecto"])
                    fase.append(filedata["fase"])
                    valor.append(filedata["valor"])
                    corrVal.append(correlativo)
                    nedpVal.append(nedp)

                    # Ejecución de función que firma el archivo
                    # Se crea el pdf vacío
                    #os.system('touch signature.pdf')
                    #os.system('ls -al')
                    myutil.signFile(file)
                    os.system('rm signature.pdf')


                # Se imprime la falla
                else:
                    print(u'\n=== File: {0} | no válido ==='.format(file))

            else:
                print(u'\n=== File: {0} | no válido ==='.format(file))
    # print(myutil.getEdpData())

    # Ya fuera del loop, creamos el diccionario y posteriormente
    # el dataframe
    data = {
        "file" : fileName,
        "proyecto" : proyecto,
        "fase" : fase,
        "valor" : valor,
        "corrVal" : corrVal,
        "nedpVal" : nedpVal
    }
    df = pd.DataFrame(data)
    df.to_csv('data.csv')
    print("Analisis finalizado...")
    print(df)