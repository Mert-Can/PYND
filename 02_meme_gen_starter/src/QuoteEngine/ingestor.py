import abc
from docx import Document
from pdftotext import PDF
import pandas as pd
from QuoteEngine.quotemodel import QuoteModel
import random
import os


"""This is the ingestor module
This module under the QuoteEngine package which manages the processing of quotes.

This module contains and abstract base class IngestorInterface that defines 
a class method, can_ingest, to verify if the file type is compatible with the ingestor class.
Also, it defines an abstract method, parse, for parsing the file content (i.e., splitting each row) 
and outputting it to a Quote object.

This module also contains various sub classes that inherits from the IngestorInterface
These classes include:

TextIngestor: to process .txt files and extract quotes
DocxIngestor: to process .docx files and extract quotes
PDFIngestor: to process .pdf files and extract quotes
CSVIngestor: to process .csv files and extract quotes

Ingestor: This class encapsulates all the ingestors (i.e TextIngestor, DocxIngestor, PDFIngestor, CSVIngestor) 
          to provide one interface to load any supported file type

Example:

quotes = Ingestor.parse(filepath)

# filepath refers to the input path to the quote file

print(quotes)

#prints out a list of quotes objects.
"""

class IngestorInterface(abc.ABC):
    def __init__(self):
        super().__init__()

    def can_ingest(self, path):
        """
        This method checks the file extension for an input path
        and returns True of the extension corresponds to the 
        type of ingestor class.

        Parameter:
        path : str, (Path of input file with lines os quotes )

        return:
        boolean (True or Flase)
        """
        ext = path.split('.')[-1]
        return True if self.extension == ext else False

    
    @abc.abstractmethod
    def parse(self, path):
        pass


class TextIngestor(IngestorInterface):

    """This s the TextIngestor class
    This class ingests .txt files
    """
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

    """This s the DocxIngestor class
    This class ingests .docx files
    """

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

    """This s the PDFIngestor class
    This class ingests .pdf files
    """

    extension = 'pdf'
    def __init__(self):
        super().__init__()

    def parse(self, path):
        quotes =[]
        # Load your PDF
        with open(path, "rb") as f:
            pdf = PDF(f)
        # Save all text to a txt file.
        with open('./output.txt', 'w') as f:
            f.write("\n\n".join(pdf))
        with open("./output.txt", 'r') as txt:
            for line in txt:
                quote = line.split("-")
                quotes.append(QuoteModel(quote[0], quote[1]))
        os.remove("./output.txt")
        return quotes

class CSVIngestor(IngestorInterface):
    
    """This s the CSVIngestor class
    This class ingests .csv files
    """
    extension = 'csv'
    def __init__(self):
        super().__init__()
        
    def parse(self, path):
        df = pd.read_csv(path, dtype=str)
        quotes = df.values.tolist()

        quotes_list = []

        # append quotes to list of quotes
        for q in quotes:
            q_objt = QuoteModel(q[0], q[1])
            quotes_list.append(q_objt)

        return quotes_list

class Ingestor(IngestorInterface):

    """This is the Ingestor class
    This class encapsulates all the ingestors
    """

    def __init__(self):
        super().__init__()
    
    @staticmethod
    def parse(path):

        """
        This method accepts a file path as input and returns 
        a list of QuoteModel objects

        Parameters:
        path: str, (Path to input quote file) 

        return:
        quotes: List[QuoteModel], List of QuoteModel objects
        """

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
        """
        This method loops through a list of all types of quote files and 
        ingest each file with the Ingestor.parse method then adds quotes to 
        a list of QuoteModule objects.

        parameters:
        files : List[str] , list of paths to quote files

        return:
        quotes : List[Quote]
        """
        quotes = []
        for f in files:
            quotes.extend(Ingestor.parse(f))
        
        return quotes
