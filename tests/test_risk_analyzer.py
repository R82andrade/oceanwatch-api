from app.services.risk_analyzer import RiskAnalyzer


def test_risco():
    resultado = RiskAnalyzer.analisar(
        altura_onda=5.0,
        velocidade_vento=30.0
    )

    assert resultado == "RISCO"


def test_atencao():
    resultado = RiskAnalyzer.analisar(
        altura_onda=2.5,
        velocidade_vento=20.0
    )

    assert resultado == "ATENCAO"


def test_normal():
    resultado = RiskAnalyzer.analisar(
        altura_onda=1.6,
        velocidade_vento=20.2
    )

    assert resultado == "NORMAL"


def test_onda_abaixo_de_2_e_normal():
    resultado = RiskAnalyzer.analisar(
        altura_onda=1.99,
        velocidade_vento=20.0
    )

    assert resultado == "NORMAL"


def test_onda_exatamente_2_e_atencao():
    resultado = RiskAnalyzer.analisar(
        altura_onda=2.0,
        velocidade_vento=20.0
    )

    assert resultado == "ATENCAO"


def test_onda_exatamente_4_e_atencao():
    resultado = RiskAnalyzer.analisar(
        altura_onda=4.0,
        velocidade_vento=20.0
    )

    assert resultado == "ATENCAO"


def test_vento_abaixo_de_25_e_normal():
    resultado = RiskAnalyzer.analisar(
        altura_onda=1.0,
        velocidade_vento=24.99
    )

    assert resultado == "NORMAL"


def test_vento_exatamente_25_e_atencao():
    resultado = RiskAnalyzer.analisar(
        altura_onda=1.0,
        velocidade_vento=25.0
    )

    assert resultado == "ATENCAO"


def test_vento_exatamente_40_e_atencao():
    resultado = RiskAnalyzer.analisar(
        altura_onda=1.0,
        velocidade_vento=40.0
    )

    assert resultado == "ATENCAO"
