import re

KEYWORDS = {
    "यदि": "IF",
    "प्रवेश": "INPUT",
    "तदा": "THEN",
    "अथ": "ELSE",
    "अथयदि": "ELSEIF",
    "निर्गम": "PRINT",
    "किन्चित्काल": "WHILE",
    "चक्र": "FOR",
    "तथा": "AND",      # Logical AND
    "अथवा": "OR",       # Logical OR
    "न": "NOT",          # Logical NOT
    "अन्यतर": "XOR"      # Logical XOR
}


TOKENS = [
    ("MULTI_COMMENT", r"/\*[\s\S]*?\*/"),   
    ("SINGLE_COMMENT", r"//.*"),            
    ("STRING", r'"[^"]*"'),
    ("LBRACK", r"\["),
    ("RBRACK", r"\]"),
    ("COMMA", r","),
    ("NUMBER", r"\d+"),
    ("ID", r"[a-zA-Z_\u0900-\u097F][a-zA-Z0-9_\u0900-\u097F]*"),
    ("PLUS", r"\+"),
    ("MINUS", r"-"),
    ("MUL", r"\*"),
    ("DIV", r"/"),
    ("EQ", r"="),
    ("GT", r">"),
    ("LT", r"<"),
    ("LPAREN", r"\("),
    ("RPAREN", r"\)"),
    ("LBRACE", r"\{"),
    ("RBRACE", r"\}"),
    ("SEMI", r";"),
]

def tokenize(code):
    tokens = []
    i = 0

    while i < len(code):
        if code[i].isspace():
            i += 1
            continue

        match = None

        for token_type, pattern in TOKENS:
            regex = re.compile(pattern)
            match = regex.match(code, i)

            if match:
                value = match.group(0)

                # Skip comments entirely—do not add them to the tokens list
                if token_type == "SINGLE_COMMENT" or token_type == "MULTI_COMMENT":
                    i = match.end()
                    break

                # Check if the matched string is a reserved keyword
                if value in KEYWORDS:
                    tokens.append((KEYWORDS[value], value))
                else:
                    tokens.append((token_type, value))

                i = match.end()
                break

        if not match:
            raise Exception(f"Invalid character: {code[i]}")

    return tokens