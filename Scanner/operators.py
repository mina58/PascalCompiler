from token_types import TokenType


operators = {
    "~": TokenType.BitwiseNot,
    "not": TokenType.NotKeyword,
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
    "and": TokenType.AndKeyword,
    "or": TokenType.OrKeyword,
    "&": TokenType.BitwiseAnd,
    "|": TokenType.BitwiseOrVerticalBar,
    "!": TokenType.BitwiseOrExclamationMark,
    "in": TokenType.InKeyword,
    "div": TokenType.DivKeyword,
    "mod": TokenType.ModKeyword,
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
