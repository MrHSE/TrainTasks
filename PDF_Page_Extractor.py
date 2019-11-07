import PyPDF4

pages = input("Введите страницы, которые вы хотите скопировать: ").split()
fileinput = input("Введите название файла, из которого вы хотите извлечь страницы: ")
name = str(input("Введите название нового файла: "))
reader = PyPDF4.PdfFileReader(open(fileinput + '.pdf', 'rb'))
writer = PyPDF4.PdfFileWriter()
for page in pages:
    writer.addPage(reader.getPage(int(page) - 1))

outputStream = open(name + '.pdf', 'wb')
writer.write(outputStream)
outputStream.close()
