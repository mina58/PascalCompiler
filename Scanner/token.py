from token_types import TokenType

class Token:
    def __init__(self, lexeme: str, token_type: TokenType) -> None:
        self.lexeme = lexeme
        self.token_type = token_type


    def as_dict(self) -> dict:
        return {
            "lexeme": self.lexeme,
            "type": self.token_type
        }
    

    def __str__(self) -> str:
        return f"{self.as_dict()}"