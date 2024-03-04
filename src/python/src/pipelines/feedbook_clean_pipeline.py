from datetime import datetime
import re
import logging
from typing import Literal, Dict, List
from itemadapter import ItemAdapter

class FeedbookCleanPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        ## cleaning price
        cleaned_price, currency = self.clean_price(adapter['price'])
        adapter['price'] = cleaned_price
        adapter['currency'] = currency

        ## split item__subtitle on two values
        item__blocks = adapter['authors']
        if len(item__blocks) >= 2:
            authors_block = ' '.join(item__blocks[1::])
        else:
            authors_block = item__blocks[0]

        ## set correct authors, translators
        roles = self.split_roles(authors_block)
        adapter['authors'] = roles.get('author')
        adapter['translators'] = roles.get('translator')

        ## clearify id to avoid colisions i - /item/ b - /book/
        book_id: str = adapter['book_id']
        if '/item/' in adapter['book_url']:
            book_id = f'i{book_id}'
        elif '/book/' in adapter['book_url']:
            book_id = f'b{book_id}'
        adapter['book_id'] = book_id

        ## parse to int fields
        fields_to_convert = ['series_number', 'epub_isbn', 'paper_isbn', 'page_count']
        for field in fields_to_convert:
            adapter[field] = self.StrToInt(adapter[field])[0]
        
        ## parse publication date
        adapter['publication_date'] = self.parse_publication_date(adapter['publication_date'])

        ## set filename
        adapter['image_name'] = adapter['image_link'][0].split('/')[-1].split('?')[0]
        
        ## replace empty categories with None
        if not adapter['categories']:
            adapter['categories'] = None

        if adapter['translators'] == 'null':
            adapter['translator'] == None

        return item

    def clean_price(self, price_str: str) -> (tuple[Literal['Free'], None] | tuple[float, str]):
        """Decodes a price string into its currency and value components.

            Args:
                price_str (str): A string representing a price. It should be in the format 
                    "Buy for [currency_symbol][price_value]", e.g., "Buy for $9.99" or it will return ("Free", None).

            Returns:
                tuple: A tuple containing the currency symbol and the price value.
                    - If the price string matches the expected format, returns (currency, price_value).
                    - If the price string is None or does not match the expected format, returns ("Free", None).
        """
        if price_str is None or price_str == "Download":
            return "Free", None  
        match = re.search(r'Buy for ([^\d]+)(\d+\.\d+)', price_str)
        if match is None:
            return "Free", None  

        currency = match.group(1)
        price_value = float(match.group(2))
        
        if currency.startswith('\\u'):
            currency = currency.encode('utf-8').decode('unicode-escape')
        return price_value, currency
    
    def split_roles(self, line: str) -> Dict[str, List[str]]:
        """
        !!! IMPORTANT: dict keys ALWAYS in lowercase and in singular noun ('author' not 'authors')
        Splits the input line containing author names and roles and returns a dictionary 
        mapping roles to lists of corresponding authors.

        Args:
            line (str): The input string containing author names and roles.

        Returns:
            Dict[str, List[str]]: A dictionary where keys are roles and values are lists 
            of corresponding authors.

        Example:
            >>> line = "Written by John Doe (Author), Jane Smith (Translator)"
            >>> split_roles(line)
            {'author': ['John Doe'], 'translator': ['Jane Smith']}
        """
        roles_dictionary: Dict[str, List[str]] = {}
        if isinstance(line, list):
            line = line[0]

        text = line.split('by')[1]
        name_role = text.split(') ,')
        for value in name_role:
            name, role  = value.split('(')
            role = role.replace(')', '').strip().lower()
            if role in roles_dictionary:
                roles_dictionary[role].append(name.strip())
            else:
                roles_dictionary[role] = [name.strip()]
        return roles_dictionary
    
    def StrToInt(self, *args: str) -> list[int | None]:
        """
        Converts a list of string inputs to a list of integers.

        Args:
            args (str): List of string arguments to be converted to integers.

        Returns:
            list[int | None]: List of converted integer values or None if input is None.
        """
        converted_values = []
        for arg in args:
            if arg:
                converted_values.append(int(arg))
            else:
                converted_values.append(arg)
        return converted_values
    
    def parse_publication_date(self, date_str: str) -> str:
        """
        Parses the publication date string into ISO 8601 format.

        Args:
            date_str (str): The input string representing the publication date.

        Returns:
            str: The publication date string in ISO 8601 format.
        """
        try:
            parsed_date = datetime.strptime(date_str, "%B %d, %Y")
        except ValueError:
            try:
                parsed_date = datetime.fromisoformat(date_str)
            except ValueError as e:
                logging.warning(f"Failed to parse publication date: {e}")
                return None
        
        return parsed_date.isoformat() if parsed_date else None