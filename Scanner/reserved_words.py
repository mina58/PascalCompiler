from Scanner.token_types import TokenType


reserved_words = {
    "array": TokenType.ArrayKeyword, #unused
    "begin": TokenType.BeginKeyword,
    "case": TokenType.CaseKeyword, #unused
    "const": TokenType.ConstKeyword,
    "do": TokenType.DoKeyword,
    "downto": TokenType.DowntoKeyword, #unused
    "else": TokenType.ElseKeyword,
    "end": TokenType.EndKeyword,
    "false": TokenType.FalseKeyword,
    "file": TokenType.FileKeyword, #unused
    "for": TokenType.ForKeyword,
    "function": TokenType.FunctionKeyword,
    "goto": TokenType.GotoKeyword, #unused
    "if": TokenType.IfKeyword,
    "label": TokenType.LabelKeyword, #unused
    "main": TokenType.MainKeyword, #unused and not in description
    "nil": TokenType.NilKeyword,  #unused and not in description
    "of": TokenType.OfKeyword, #unused
    "packed": TokenType.PackedKeyword, #unused
    "procedure": TokenType.ProcedureKeyword,
    "program": TokenType.ProgramKeyword,
    "read": TokenType.ReadKeyword,
    "readln": TokenType.ReadlnKeyword,
    "real": TokenType.RealKeyword,
    "record": TokenType.RecordKeyword, #unused
    "repeat": TokenType.RepeatKeyword,
    "set": TokenType.SetKeyword, #unused
    "string": TokenType.StringKeyword,
    "then": TokenType.ThenKeyword,
    "to": TokenType.ToKeyword,
    "true": TokenType.TrueKeyword,
    "type": TokenType.TypeKeyword,
    "until": TokenType.UntilKeyword,
    "var": TokenType.VarKeyword,
    "while": TokenType.WhileKeyword,
    "with": TokenType.WithKeyword, #unused
    "write": TokenType.WriteKeyword,
    "writeln": TokenType.WritelnKeyword,
    "define": TokenType.DefineKeyword, #unused and not in description
    "extern": TokenType.ExternKeyword, #unused and not in description
    "external": TokenType.ExternalKeyword, #unused and not in description
    "module": TokenType.ModuleKeyword, #unused and not in description
    "otherwise": TokenType.OtherwiseKeyword, #unused and not in description
    "private": TokenType.PrivateKeyword, #unused and not in description
    "public": TokenType.PublicKeyword, #unused and not in description
    "static": TokenType.StaticKeyword, #unused and not in description
    "univ": TokenType.UnivKeyword, #unused and not in description
    "boolean": TokenType.BooleanKeyword,
    "char": TokenType.CharKeyword,
    "integer": TokenType.IntegerKeyword,
    "forward": TokenType.ForwardKeyword, #unused and not in description
    "not": TokenType.NotKeyword, #unused
    "and": TokenType.AndKeyword,
    "or": TokenType.OrKeyword,
    "in": TokenType.InKeyword, #unused
    "div": TokenType.DivKeyword, #unused
    "mod": TokenType.ModKeyword,  #unused
    "uses": TokenType.UsesKeyword
}

