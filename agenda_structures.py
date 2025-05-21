class AgendaItem:
    def __init__(self, codigo: int, nome: str, fone_fixo: str, fone_celular: str, fone_comercial: str):
        self.codigo = codigo
        self.nome = nome
        self.fone_fixo = fone_fixo
        self.fone_celular = fone_celular
        self.fone_comercial = fone_comercial

    def __repr__(self):
        return f"AgendaItem(codigo={self.codigo}, nome='{self.nome}', fone_fixo='{self.fone_fixo}', fone_celular='{self.fone_celular}', fone_comercial='{self.fone_comercial}')"
