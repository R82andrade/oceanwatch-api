class RiskAnalyzer:

    @staticmethod
    def analisar(
        altura_onda: float,
        velocidade_vento: float
    ) -> str:

        if (
            altura_onda > 4
            or velocidade_vento > 40
        ):
            return "RISCO"

        if (
            altura_onda >= 2
            or velocidade_vento >= 25
        ):
            return "ATENCAO"

        return "NORMAL"
