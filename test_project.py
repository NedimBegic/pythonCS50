import pandas as pd
import project as m 

def test_clean_mpa_column():
    df = pd.DataFrame({"15M_MPa": ["12,3", "abc", None]})
    out = m.clean_mpa_column(df.copy(), "15M_MPa")
    assert out["15M_MPa"].tolist() == [12.3, 0.0, 0.0]


def test_clean_all_mpa_columns():
    df = pd.DataFrame({"15M_MPa": ["1"], "30M_MPa": ["2,5"]})
    out = m.clean_all_mpa_columns(df.copy())
    assert out["15M_MPa"].iat[0] == 1.0
    assert out["30M_MPa"].iat[0] == 2.5


def test_clean_shotcrete_layer():
    df = pd.DataFrame({"Shotcrete_Layer": ["7", "bad", None]})
    out = m.clean_shotcrete_layer(df.copy())
    assert out["Shotcrete_Layer"].tolist() == [7.0, 0.0, 0.0]
