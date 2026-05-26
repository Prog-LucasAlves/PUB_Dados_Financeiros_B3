from pydantic import BaseModel, Field, field_validator


class B3StockData(BaseModel):
    papel: str = Field(..., description="Ticker da ação, ex: WEGE3")
    tipo: str = Field(..., description="ON, PN, etc.")
    empresa: str = Field(..., description="Nome da empresa")
    setor: str = Field(..., description="Setor de atuação")
    cotacao: float = Field(..., description="Preço de fechamento da cotação")
    dt_ult_cotacao: str = Field(..., description="Data da última cotação")
    min_52_sem: float = Field(default=0.0)
    max_52_sem: float = Field(default=0.0)
    vol_med: float = Field(default=0.0, description="Volume médio negociado em 2m")
    valor_mercado: float = Field(default=0.0)
    valor_firma: float = Field(default=0.0)
    ult_balanco_pro: str = Field(default="")
    nr_acoes: int = Field(default=0)
    os_dia: float = Field(default=0.0, description="Oscilação do dia")
    pl: float = Field(default=0.0)
    lpa: float = Field(default=0.0)
    pvp: float = Field(default=0.0)
    vpa: float = Field(default=0.0)
    p_ebit: float = Field(default=0.0)
    marg_bruta: float = Field(default=0.0)
    psr: float = Field(default=0.0)
    marg_ebit: float = Field(default=0.0)
    p_ativo: float = Field(default=0.0)
    marg_liquida: float = Field(default=0.0)
    p_cap_giro: float = Field(default=0.0)
    ebit_ativo: float = Field(default=0.0)
    p_ativo_circ_liq: float = Field(default=0.0)
    roic: float = Field(default=0.0)
    div_yield: float = Field(default=0.0)
    roe: float = Field(default=0.0)
    ev_ebitda: float = Field(default=0.0)
    liquidez_corr: float = Field(default=0.0)
    ev_ebit: float = Field(default=0.0)
    cres_rec: float = Field(default=0.0)
    ativo: float = Field(default=0.0)
    disponibilidades: float = Field(default=0.0)
    ativo_circulante: float = Field(default=0.0)
    divd_bruta: float = Field(default=0.0)
    divd_liquida: float = Field(default=0.0)
    patr_liquido: float = Field(default=0.0)
    lucro_liquido_12m: float = Field(default=0.0)
    lucro_liquido_3m: float = Field(default=0.0)

    @field_validator(
        "cotacao",
        "min_52_sem",
        "max_52_sem",
        "vol_med",
        "valor_mercado",
        "valor_firma",
        "os_dia",
        "pl",
        "lpa",
        "pvp",
        "vpa",
        "p_ebit",
        "marg_bruta",
        "psr",
        "marg_ebit",
        "p_ativo",
        "marg_liquida",
        "p_cap_giro",
        "ebit_ativo",
        "p_ativo_circ_liq",
        "roic",
        "div_yield",
        "roe",
        "ev_ebitda",
        "liquidez_corr",
        "ev_ebit",
        "cres_rec",
        "ativo",
        "disponibilidades",
        "ativo_circulante",
        "divd_bruta",
        "divd_liquida",
        "patr_liquido",
        "lucro_liquido_12m",
        "lucro_liquido_3m",
        mode="before",
    )
    @classmethod
    def parse_finance_float(cls, value: int | float | str | None) -> float:
        if value is None or value == "":
            return 0.0
        if isinstance(value, (int, float)):
            return float(value)

        # Limpa formatação brasileira (ex: 1.250.000,50% -> 1250000.50)
        val_str = str(value).strip().replace("\n", "").replace(" ", "")
        val_str = val_str.replace(".", "").replace(",", ".")
        val_str = val_str.replace("%", "")

        try:
            # Caso restem múltiplos pontos por falha de replace (ex: 1.234.56 -> 1234.56)
            if val_str.count(".") > 1:
                parts = val_str.split(".")
                val_str = "".join(parts[:-1]) + "." + parts[-1]
            return float(val_str)
        except ValueError:
            return 0.0

    @field_validator("nr_acoes", mode="before")
    @classmethod
    def parse_shares(cls, value: int | float | str | None) -> int:
        if value is None or value == "":
            return 0
        if isinstance(value, int):
            return value
        if isinstance(value, float):
            return int(value)

        val_str = str(value).strip().replace(".", "").replace(",", "")
        try:
            return int(val_str)
        except ValueError:
            return 0
