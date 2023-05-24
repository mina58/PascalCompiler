from Scanner.token_types import TokenType


operators = {
    "~": TokenType.BitwiseNot,
    "*": TokenType.MultiplyOp,
    "/": TokenType.DivideOp,
    "+": TokenType.AddOp,
    "-": TokenType.SubtractOp,
    "=": TokenType.EqualToOp,
    "<>": TokenType.NotEqualToOp,
    ">": TokenType.GreaterThanOp,
    "<": TokenType.LessThanOp,
    ">=": TokenType.GreaterThanOrEqualOp,
    "<=": TokenType.LessThanOrEqualOp,
    "&": TokenType.BitwiseAnd,
    "|": TokenType.BitwiseOrVerticalBar,
    "!": TokenType.BitwiseOrExclamationMark,
    ":=": TokenType.AssignmentOp,
    "{": TokenType.OpenBraces,
    "}": TokenType.CloseBraces,
    "(": TokenType.OpenParenthesis,
    ")": TokenType.CloseParenthesis,
    "[": TokenType.OpenSquareBracket,
    "]": TokenType.CloseSquareBracket,
    ".": TokenType.Dot,
    ";": TokenType.SemiColon,
    ":": TokenType.Colon,
    '"': TokenType.DoubleQuotations,
    "'": TokenType.SingleQuotations,
    ",": TokenType.Comma
}
