import myutil
import os
import re

if __name__ == '__main__':
    # El diccionario a trabajar
    dicc = {}

    # Nos cambiamos de directorio a donde se deben dejar los pdfs
    os.chdir('./pdf_files/')
    os.system('touch demo.txt')

    # Recorre todos los archivos de la carpeta
    for file in os.listdir('.'):

        # Solo se procesan los archivos .pdf
        if file.endswith('.pdf'):
            
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

                # Se imprime la falla
                else:
                    print(u'\n=== File: {0} | no válido ==='.format(file))

            else:
                print(u'\n=== File: {0} | no válido ==='.format(file))
    # print(myutil.getEdpData())

