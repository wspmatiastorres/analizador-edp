import slate3k as slate
import re
from reportlab.pdfgen import canvas
from PyPDF2 import PdfFileWriter, PdfFileReader
import io

# Función que genera la página de firma
def createSignPage():
    # Creación del canvas
    c = canvas.Canvas("./signature.pdf")

    # Imagen de fondo
    # c.drawImage("./img/signature.png", 0, 0, 595, 825)

    # Texto
    c.setFont("Helvetica", 40)
    c.drawString(110, 300, "Firma")
    c.save()


# Función que procesa el documento
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

# Función que firma el documento
def signFile(pdfpath = "./pdf_files/a.pdf"):
    print("\t-> "+pdfpath)

    createSignPage()
    signature_path = './signature.pdf'
    out_path = "s_"+pdfpath
 
    # read the existing PDF
    signed_pdf = PdfFileReader(open(signature_path, "rb"))
    existing_pdf = PdfFileReader(open(pdfpath, "rb"))
    output = PdfFileWriter()
 
    for i in range(len(existing_pdf.pages)):
        page = existing_pdf.getPage(i)
        if i == 0:
            # Primer elemento. Se pega la firma
            page.mergePage(signed_pdf.getPage(0))
        output.addPage(page)
 
    outputStream = open(out_path, "wb")
    output.write(outputStream)
    outputStream.close()

# Principal program
if __name__ == "__main__":
    print(getEdpData())