from PyPDF2 import PdfFileReader
from googletrans import Translator
# from translate import Translator
import pandas as pd

file = open("Religion and the Rise of Capitalism - R H Tawney.pdf", 'rb')
reader = PdfFileReader(file)
num_pages = reader.numPages
start_num = 0
end_num = 500
print(f"Totla page: {num_pages}")
for p in range(num_pages):
    print(f"Page No: {p}")
    page = reader.getPage(p)
    text = page.extractText()

    translator = Translator()
    try:
        result = translator.translate(str(text), src='en', dest='ur')
        print(result.text)

        with open("Religion and the Rise of Capitalism - R H Tawney.docx", "a") as f:
            f.write(result.text)
            f.close()
    except Exception as e:
        print(e)
        with open("Religion and the Rise of Capitalism - R H Tawney.docx", "a") as f:
            f.write(f"\n\nContent is missing on page number {p+1}\n\n")
            f.close()
