import random
from docx import Document
from QuoteEngine.quotemodel import QuoteModel
#from pdftotext import PDF
import pandas as pd
class Ingestor:
    @staticmethod
    def parse(filepath):
        with open(filepath) as f:
            quotes = f.readlines()
        return quotes

    def split_ext(self, filepath):
        ext = filepath.split('.')[-1]
        print(ext)

    def get_quotes(self, files):
        quotes = []
        for f in files:
            quotes = quotes.extend(Ingestor.parse(f))
        
        return quotes


quotes = Ingestor.parse('./_data/DogQuotes/DogQuotesTXT.txt')

print(quotes)
quote_objts = []

for q in quotes:
    parts = q.split('-')
    if len(parts) == 2:
        q_objt = QuoteModel(parts[0], parts[1])

        quote_objts.append(q_objt)

quote = random.choice(quote_objts)
print(quote.body + ' - ' + quote.author)

#Ingestor.split_ext(Ingestor, './_data/DogQuotes/DogQuotesPDF.pdf')
 