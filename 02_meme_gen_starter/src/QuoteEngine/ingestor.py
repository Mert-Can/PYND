import abc
from docx import Document
#from pdftotext import PDF
import pandas as pd
from QuoteEngine.quotemodel import QuoteModel
import random

class IngestorInterface(abc.ABC):
    def __init__(self):
        super().__init__()

    def can_ingest(self, path):
        ext = path.split('.')[-1]
        return True if self.extension == ext else False

    
    @abc.abstractmethod
    def parse(self, path):
        pass


class TextIngestor(IngestorInterface):
    extension = 'txt'
    def __init__(self):
        super().__init__()

    def parse(self, path):
        with open(path) as f:
            quotes = f.readlines()

        quotes_list = []

        for q in quotes:
            parts = q.split('-')
            if len(parts) == 2:
                q_objt = QuoteModel(parts[0], parts[1])
                quotes_list.append(q_objt)
        return quotes_list

class DocxIngestor(IngestorInterface):
    extension = 'docx'
    def __init__(self):
        super().__init__()

    def parse(self, path):
        quotes = [q.text for q in Document(path).paragraphs]

        quotes_list = []

        for q in quotes:
            parts = q.split('-')
            if len(parts) == 2:
                q_objt = QuoteModel(parts[0], parts[1])
                quotes_list.append(q_objt)
        return quotes_list

class PDFIngestor(IngestorInterface):
    extension = 'pdf'
    def __init__(self):
        super().__init__()

    def parse(self, path):
        #with open(path) as f:
            #pdftext = PDF(f)
        pass

class CSVIngestor(IngestorInterface):
    extension = 'csv'
    def __init__(self):
        super().__init__()
        
    def parse(self, path):
        df = pd.read_csv(path, dtype=str)
        quotes = df.values.tolist()

        quotes_list = []

        for q in quotes:
            q_objt = QuoteModel(q[0], q[1])
            quotes_list.append(q_objt)

        return quotes_list

class Ingestor(IngestorInterface):
    def __init__(self):
        super().__init__()
    
    @staticmethod
    def parse(path):
        if TextIngestor().can_ingest(path):
            return TextIngestor().parse(path)

        if DocxIngestor().can_ingest(path):
            return DocxIngestor().parse(path)

        if PDFIngestor().can_ingest(path):
            return PDFIngestor().parse(path)

        if CSVIngestor().can_ingest(path):
            return CSVIngestor().parse(path)

    @staticmethod
    def get_quotes(files):
        quotes = []
        for f in files:
            quotes.extend(Ingestor.parse(f))
        
        return quotes
