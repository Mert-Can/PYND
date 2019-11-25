
"""This is the quotemodel module
    This module includes a class QuoteModel that defines 
    a QuoteModel object which contains body and author fields
    of a quote. The class overrides the correct methods to 
    instantiate the class and print the model contents 
    as: ”body text” - author 
"""

class QuoteModel:
    def __init__(self, body, author):

        """
        Parameters:
        body : str (the body text of a quote)
        author: str (the name of the author of a quote)
        """
        self.body = body
        self.author = author

        print(body + " - " + author)