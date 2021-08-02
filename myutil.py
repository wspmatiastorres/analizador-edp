import slate3k as slate
import re
#import fitz

# 
def getEdpData(pdfpath = "./pdf_files/a.pdf"):
    with open(pdfpath, "rb") as f:
        fulltxt = slate.PDF(f)

    try:
        # Desde la página 1 se sacan los montos
        worktext = fulltxt[0][fulltxt[0].find("Total Factura"):]
        worktext = worktext.replace("\n", " ")
        worktext = " ".join(worktext.split())
        worktext = worktext.replace(",", ".")

        # Regular expression to find numbers
        qtylist = re.findall("\d+\.\d+", worktext)

        # Desde la página 2 se saca el proyecto y el número de fase
        infotext = fulltxt[1]
        infotext = infotext.replace("\n", " ")
        infotext = " ".join(infotext.split())

        # Regular expression to find info (1ero proyecto)
        infolist = re.findall("Proyecto : \w+", infotext)
        proyecto = infolist[0].replace("Proyecto : ", "")

        infolist = re.findall("Fase : \d+", infotext)
        fase = infolist[0].replace("Fase : ", "")

        return {
            'valor' : qtylist[-1]
            , 'proyecto' : proyecto
            , 'fase' : int(fase)
            , 'error' : None
            , 'estado' : 'OK'
            , 'file' : pdfpath}
    except:
        return {
            'valor' : None
            , 'proyecto' : None
            , 'fase' : None
            , 'error' : "Error en la extracción de los datos"
            , 'estado' : 'NOTOK'
            , 'file' : pdfpath}

# Principal program
if __name__ == "__main__":
    print(getEdpData())