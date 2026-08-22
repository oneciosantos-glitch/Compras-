"""Instalador do Sistema de Controle de Compras - Versao Streamlit

Este UNICO arquivo instala automaticamente TUDO:
1. Cria todos os arquivos do sistema (app.py, models.py, database.py, seed.py, requirements.txt)
2. Instala os pacotes Python necessarios (streamlit, sqlalchemy)
3. Cria o banco de dados e popula com dados iniciais
4. Inicia o sistema no navegador

Como usar:
    python instalar_sistema.py

Requisitos:
    - Python 3.8 ou superior instalado no computador
    - Acesso a internet (para baixar os pacotes na primeira vez)
"""

import subprocess
import sys
import os
import textwrap

# Caminho da pasta onde este script esta
PASTA_SISTEMA = os.path.dirname(os.path.abspath(__file__))


# ============================================================
# CONTEUDO DOS ARQUIVOS DO SISTEMA
# ============================================================



# ============================================================
# IMAGENS DOS MATERIAIS (base64 de PNGs pre-gerados)
# Cada chave e um sub-grupo de material/EPI.
# Decodificadas e salvas em PASTA_SISTEMA/imagens/ pelo instalador.
# ============================================================
IMAGENS_BASE64 = {
    "AGUA_SANITARIA_E_ALVEJANTES":
        "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"
        "RU5ErkJggg==",
    "AVENTAIS_E_MACACOES":
        "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"
        "5ox0/x+XNfyN3bIVogAAAABJRU5ErkJggg==",
    "CALCADOS_DE_PROTECAO":
        "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",
    "CAPACETES_E_PROTECAO_CABECA":
        "iVBORw0KGgoAAAANSUhEUgAAAPAAAADICAYAAADWfGxSAAAdL0lEQVR4nO3deXwTZf4H8M8cuZNe"
        "9AZaSqnQKlWUU4GCLCAiCx4cW1BRVBSvdfEAWVhX14sfKKgsi4i6KyCgAh6U2xaRWkEuAQGBUuQo"
        "tPSmbc6Z3x8lIUnTNGlLMxO+79err1eOmXmeJ80nzzMzyTyM5VScCB/xCeem+7osIaRprH/Ev+nr"
        "skxjAabQEhI4jYXZa4Ddw+vPJwMhpGn8yZ3HADtvgEJLSOA0lkXW3xUIIa3HOYOedmddAkzhJUR6"
        "vIW4Xg/svgIhJPAayiRjLogVAUCRWDgdACyn4ii8hEiUe05ZTw8SQqTJnlF7Zj0OoQkh8sAHugLE"
        "P4rEwqFXuwzLqbiNV7sM0jIYURSnATR8lrrWCK47CrJ00RBaRgIR3kCWS3xHAZa4QIco0OUT7xz7"
        "wKLo84+SSCtRdjgvifAoEguHmgtiaTgtQXQQS94+Rv1RVDaA/3p43gagBEAOgCy3558GUHU1K0qu"
        "DgqwRPnZ+zYWwKcBCABeBDAGQBmAn/ytD/XC0kP7wNeOagCHL99OCmRFSMuhHjg4vO90+yMAP3pY"
        "Rgcg9fLtgqtdIdI6KMDBobEh9Puo2wcuBfAVgNzWqBS5+ugo9LWhRQ5S0XtEemgfmBAZoyF0cHDe"
        "B94P4N1AVYS0LgqwvD18lZ8nEkdDaEJkjAIsUaaTMZL60oTU6kPqUIAJkTE6jSRhxvzojeqORQH/"
        "QYMxP5p6X4miHljiAh2eQJdPvKMAy0CgQkThlT46jSQT9jC1xpCagisfFGCZoXARZzSEJkTGKMCE"
        "yBidRiJExqgHJkTGKMCEyBgFmBAZowATImMUYEJkjI5CEyJj1AMTImMUYEJkjAJMiIxRgAmRMQow"
        "ITJGASZExug0EiEyRj0wITJGASZExq6tS+owGihCMsHp/gRW1RUMFwFRtEC0FUO0nIStJgfWqq8g"
        "Ws97XF0d9xk4/Z0uj9We6gPB/Hu9ZVllCjSJeZ7rIZoh2opgq90Fa8UnsNXuaHZ5zWmn17q6sKH6"
        "WDQAQNvxCBguyod1rrCUzYe18nO/y3LGaXqDD3sUnLrH5fIFiEIVRFsJRMtJCObfYb74ql/1krNr"
        "pgfmtAOhTdoLZfRscLohYPg4gFGBYfVgFUngtLdDGfkqftj/p8OFRUK5+/oMGwZO96d623132Yis"
        "oydshX5VhlGC4duBN9wNdbtvcN74YklLldfcdnpjs0EITS2d7M86zt750LjhvY+Nm5paliLscajb"
        "fQdePwoM3xZglACjBsNFgVV2AacbBi70KXHWnJqvmlpHubkmAszphkDddpWjxzh37lz5Aw888HFU"
        "VNRzOp3uyS5duswcNWrUgk8//TR3xdqKvHVbLfvrbcMwqu4N42b8+PG9Vn5jabRLWbRo0TaGYR7l"
        "OO6xnj17vn78+PEi+3PJXV9qs2Jjb5dJt5tSXku007mu7n88zzsCVZPfBTFR3FT7c+Hh4c86b2Pd"
        "unW/uq8/bdq0esHypSwAYBVJUEb+EwADAHj//fe/T0xMfEmtVj/RuXPnv8+YMWNNSUnJJVGEOH+J"
        "bx8SwSDoh9AMGwZV7H9g/6wqLy+v6du379vG6lPWN1/UjBmSoeqqURcpz54/X3r0xNbztioLNGpe"
        "4b4d3jDacdtkMllVKhUPAImJiW3yL/QoEsUDIsNcfnc1YNI4Vcb8V3UTBOGE+EfxzGJ0+tzxnDo8"
        "k8v5afvhAX0UqU0pr6Xa6V5Xb+3Jzw2be6X80HrP3zFAkf7lh4annR9jleomlcXp7gCYurdrWVlZ"
        "zbPPPrti8gTVwGcnaYZGR14MOX1uQcnid5bkJnWdHe5tO8Em6E8jKUIfcnlzvfHGG1mlJQU1O9aE"
        "zExsx0baH+/UgY3t1IGNHT5IcRPg+nqwigRwml6O+/PmzdvyzDPPDNJoNAoAGDw0MzX3l+eP39qd"
        "T7Ev4+n1FC8/zjBgOkTvcdnBS01NjZv9imlTRm8+tSnlNaed3urqMx+30eSyONf94cgIhX72DM24"
        "ug8xEcmJbMxTD5qHVFY9Wzt2hLJXsL6f3QX9EJrTDXa5v2rVql9emKy+0/lN3RjeMAZw6lyXLVuW"
        "d/zolmL7/dGjR3f/Mgs7/aoY49pZi6IoHs2v27dtSnkt0U4pE61nHLfDw8O1S5etngRVL9HeK9uF"
        "GBjNord118y8x0E/hGaVnRy3q6urTadOnSq5+87Q7v5sgw+5Mpw9ceJE8YEDB85qkaUBRgCoe0PV"
        "YrDRbMm2KhW+vaac+haX+0eOHDnPXE5tU8priXbaTZ48OWPy5PrHqiwVS2G68ExTNtnssmzVW2C1"
        "GgWeV7MAMGTo8OuB4RBsRlEwH2QE40+wVq6GYPK4Wx+0gr4Hdh5WVlVVGbUaRpUQz7bxdX1W3Q2s"
        "0jFSxerVq/ckJbBRsYZN4YJgdYzT7r5nfLeNOZYDPmwRrLoblFGvuTz6ySef7LiuIxfb1PKa205f"
        "/O9L049Pzqj5b0tu09eyBEsBio5Pq7bZbILzciynZnhNdyjDn4Y2MRu12sU1ng7+BaugD7AoVDhu"
        "6/V6tUHH1D+K4oUiZIzL/TVr1uz98xDlzaKtDOZLuY430/Dhw9O//V6zt6HtTJ48OWPJ58YJ+usu"
        "QpuwFayio+O511577butW7cennCv6ramltfcdjpr6MjwI4880uLh9aesEPZ/hhUf9tjz738vyMnP"
        "zy/2tL2odvdqN+x+Zo/ZAmtL11WKgn4ILZiPg9PUdUR6vV4VEZmgBSoaWcuOA2+4x3GvsLCwIi8v"
        "L/9fz+pHAwBjXMchpD8AQKVS8WExo1QVlV/UhIYwWm9bNZvN1qKioqrc3NwTCxcuzMnJyTn60hT1"
        "XQP6qFKbWl7z2lnfw+NUGfP/qfV6ZLil+FPWyEEF3Y+eeLnw7VlTN+/5LaIgpcuAqClTpgzs27ev"
        "Yx/i+hvvjpv9wWvr/v6sZuTVq7U0BP1RaGv1JpcjuneNGJ3+x9lFJe19GF7yugEu3zaKi4sLFQTh"
        "w4aWHzduQo/V65ftnjhG2c/99Vy0aNG2xx9/fKn9vlIBPqoNa+jVjUte9z/98/168p05bdPLa047"
        "Pf7vGzg67WUjPm27Jcq6riMbN2emJhOoRVFJVuX2n787mpCwuzQhISUCACIjI/VrN1p2z3hGHfQB"
        "DvohtKX8YxhrKyz2+9OnT7/z+5/bHvJlXT5krF9l9evXLyVnV+xvDT3/8FhlRuWRsMWVR8IWXzwQ"
        "tvBwTsjsT9/VTe7Xk+/c3PKa0045UIRmQhE2Ee5v2eg2TMi9d3I94iMvRtgfKywsrCgpEy61chUD"
        "IugDLNrKcenMZEEQBBGoO4J734Nbbqywjq5iuHCAUYNVdgSvGwJ17PtQhIwDADCsDrx+uGM7K1as"
        "2OVpXy0tLW2WfRmGYZguXcdGnykUSv2tZ3PLa2o75YJhQ6GOeRfWyLxaPmyyyCpT6r4iyrWBMvwJ"
        "8NrejmW//vrrfbFRHr5ZEoSCfh8YAFTCRtWODfec7Nz9w8jo6GhDbFx8KOI8j0yXrfw5z1xmFh94"
        "YFwfhtU4Hl+7du3e+4Yre3w8V/uY6xqFMFafsKp1yTwAjB8/odfKJe/mvfAUXH+F0AhePwLNKW/q"
        "Y+o7m9LOv4xS9nF/rqFTOwBQc+p22IwNHqvzm79lhbdJ0QBvNbi9nTt3npw9e/aGJx9QDG5woSAS"
        "9D2w3U3J25J+Xt/1zEsvPvVVVlbWgXPnzpWbTCbrpUuXTPn5+cWbNm069MILL3z591fXfFVjFM28"
        "09Fgs9lsXb9+/cHhgxTdPG2bNWU5PgjT0tLifz1+/R/+1q+lyvO3nf7WM+O+qtf3HrQV+LteUziX"
        "Zb30HbZ89/zRpUuX5u3fv//02bNny2tqasxWq1UoLi6uys7OPvLkk08u69u379udO9bG//UR1R2t"
        "UcdAY0RRnAYAVUfD3wx0ZVpDrVE0L11tzt24zfrrgcO206XlwiWeZ7ioNkxIxwQ2+vbbFKn3DVf0"
        "io9hw0Y+fOnd7Fzrb0DdQaeTP4W+Y9AzGk/b/fvs2i/f+9i00X5/+2rDTI0ayu53Vs20P/bwWGXG"
        "PC9HW5tb3o1pXEJT2gkAv+fbzjvX1ZttXxpmdLuB6+D+eEWlWNO+Z4XjRw1DByjSv/iP7mn35Zpa"
        "1ulzQsm6rZZ9uw/YCn773Xa2pEysKqsQaywW0RoWyujSUri2I4cqbpk4RtVPwYPzZftyZehcNh24"
        "BgNMSDCwBzjoTyMREsyumX1gQoIRBZgQGaMAEyJjFGBCZIwCTIiMUYAJkTE6jUSIjFEPTIiMyerH"
        "DKzyOhiSd3l+UjRDsBbBVrsT5rIlsNb86OO6IkShFqL1DKw1P8Fcugg2U8O/wmP5OCjDJ4HXDQSr"
        "7AiGDYEoVEIwn4S1Ohvmso8gWF2vux6ScgwMX3+WAW9MJfNgLPqH12UYVgNF6Hgo9EPAqruC5SIg"
        "ilaI1mIIlnxYL2XDUvllvfrYadstg8Jwl8tjVfk9IZiO1m93o69fIWzGPTCXfwZr9TY/1ndnQ8Xh"
        "iHqPtmZb5SR4emBGCVbRDoqQe6BLXIciy7R6sx00sCIYVgtWeR2UYQ9Ck7hNOFc+6KKnJZVhE2Ho"
        "tB+qyBfAabqD4SIAhgfDRYDT3AJV5PPQJO0XjNzEmuY2Z95Hpg2vvGNqcIYBXnc7DMm/QhM7F7x+"
        "KFg+vm6WAlYPVpkEXjcI6ph/4ccDQw6fLxLL67WaC4NCP6Tedt9fMSrraL7gx0wT9tcvGYqQ0dAl"
        "fIMzVVMu+L6+K5sNQpuulS4/T5JOW6VH1gH2NttBSvr0Nl9svjW3sXUNBsNT999//xLx8kEAjlOw"
        "iqi3hc3brQedl1eGTYQmbj7AqAAAGzZsOJienv6KWq1+Ij09/ZX169cfBACeV7Ex183X/nLi/mP2"
        "dSuPpSAmkm32LAZ2vH4odAlfOXp1bzMwrPymMi8ru/4MDIqQuxuc+eGLb61+zTTRu3fvN0pLS6vt"
        "zyWn/yNi8XLl976s39iMDFJoq5TJagjtyUNjlBnvvqKeIAhHxTMXZhSj00rHc5o2E7hteT8czujN"
        "pza8LjuhuuZrU+HpH6riEzJCAKBTp5Tov4zRLx7cz3gDALB8PDSxsx3r7du37/TIkSMX9O8pdFm0"
        "Uv1ocodTMfl/TCg6cez74uSUG6MAoO/guUmfLcjKGz2spDcA/L7dcGUWA85Qry5DM/j0lQu19X65"
        "447hwqCNXwz3GRhqqwus/3pePWZwP76rVnNOeabwbOmxk5vPWyot0Kjqz8CgcLr6h/vMDyeLehWJ"
        "4t5GZ5q48tofFqtLV1dFRDwCAFCr1Yq12Um7MkcduU2nvfyJ52V9ObRVqhw9sP0K/VL+q7uGvzvx"
        "8mwHIpMQtbvebAdLV1t2NLauVgNVZOj5EOdnTp9jSi+WCpdEUYQifJKj5wWAt956a33njta4ZR9o"
        "nkxNYdoqFSLfJdkSH6Wc59h5U6lU/EXzpLLCC0K557a418S3/4EybBIYzm0GhosFNRs+0740dgTf"
        "JyIMerUKyk4dmNhhA7mbFvxL/dC4kfytzttg+PYuV7CYN2/eltraWsfleIbckZn6027rcX9e+6g2"
        "cHn9KiuNtUdO2Ap9WV9qbZXDn52sh9Du3D9ERVEUf/dxH4fl4x23i4uLqy5cuFBpEyAAgEI30GXZ"
        "LVu2HP7rI6ph7hdxF41bXH6Devvtg7t8tMKc408bGsO77cutWrXql789pvRrBgZl6DjUm/nhyGaX"
        "mR9Wr2d8nGmCBae5GcqQK1fTPHr06PlDhw6dUyuZBude8oX02io9QRVgTuNhtoNGhkYMq4MydCx4"
        "XV/HY6+//vq6yAjGEN2GCQEAVnnlGs6VlZW1JSUllwb04eoNy0VbBQRruePjMTk5OSon19bgRe6a"
        "glNduei7YwaGO3i/ZmBQhF65+od95geNuM5x4YDw8HCtkR1q9HZt5cmTJ2d8vNI8ISytHIaknLoD"
        "egB27959asSIEe8nJyKmSyc2vvH1K+H8p43/QHJtlbIgCTALTtMNmpg3XB795JNPdqQksbGe1rC/"
        "gUK7FELbdjEABoWFhRVTpkxZNn/+/K1TH1M6rjDHsFf2WWtqaswGPaOJCGP0HqsiVjs+MEJDQ7Un"
        "TwseL0DeVJ5mYPDl0rF2nKYbONV1jvurV6/ek9SejYrSbag388OmbVYfZppwlZKSEj1p4rD+ny/Q"
        "PM2y/u9XfvaV5cdnZhn/C0i/rVIg6wC79gLbXHpK+2wH4+9W3Obr9nieZ7Uam3LuTPX4x+9XDrI/"
        "LgpVjmW0Wq1So0aDc3cwrM5xu6KioqaySmz2KSVn7jMw6HXwawYGZehfXO6vWbNm74jB/M2irQym"
        "qh0uMz+sy9Y1ePU656PIHTp0mPb111/vA4CQkBDNSy/PH3qyaOA5b/XwZUYGqbRVymQdYGdms9l6"
        "5syZslWrVv0ycODAObNmzfr6hceVd2X0rj/UBereQBzHPZaWljZr586dJwEgKirKMGfuotGdu46M"
        "cV5WMOc7boeEhGg02jYe9+0YLhQMF+a4f+LEieIQg/dZGvxlMznOTkGv16vaRCb6sX3OZV/VPvPD"
        "XYP4uovn1X7r2IdXqVR8eNzdqgovH0APjVFklB0yLN6XVfrWdeF/TXR+jjU8JGzdYfV6XWr7+u5/"
        "772qflBqbZUqWQfY+VNcpVI9kdyx/cvPPTNuVbj6R8O3n2qff/lpldcr8z94H9f/x1Vn/qmselBn"
        "Npts9se73fZOXFaOYp/9vqU622W93n0GJZWWi/UuHM7rBrnc37x5829J7dko9+Waw3rJdfL5u0aM"
        "Tj99TvDpSysK/e0u3wizz/wwOLM6OSytEprYOS7Ljxs3ocfajdbdvmw7LrIkXLDVOIalHTt2jPrv"
        "KssPvqzbEKm2VUpkdRrJ0+mXiWMUGaUH9YtLD+oXn9+rX3hwq272kjnqybd1Zzv7cuqGYUQmMfZM"
        "dFXR/xwHMeLj48P2F4zNrzWKFlEUYSpdDKvV5Bhyvfjii3f88DNzxGX74KGO/Ktj2yaTybpw4cKc"
        "AX24NF/aAdH1fxDa5bzjwI4m5i3H48bSxTDWlrvMwJC9s+0hX147Raj/Mz9s2xX3m7fXz3G6hosC"
        "y2kd+7xVVVXGgjNCcWOvv7f6BrKtUv+zk3UP3JL42g9Uoig4XplHHn2u74pvbLkAIFjOoTh/msn+"
        "3M0335zQ6ZaVYSKfJoBRgVOlQt/+c3Dqmxzbe+6551ZeLD576eFxigHNrdt/llq2vvyWaQVQN9NE"
        "xalHXWZgGPNQ9o2VwpgqhgsHw2rAKjtCYRgKbfy/oQzLBFC3b+78XWBfZ35ITR8XfaZQ9DrTBKto"
        "D238ey6PrV+//qC+GTMkSrWtUiP7b2K1FMGcj4qi78xhMX9WAXVHU48VDtssCJtElgWjtnyk2fKt"
        "cKzfkNlJKpWK79t/WCdgWL3tmM1m69/+9rdVCxcuzJkzUzU+LpoJa+m6Km0bVNuzRp1M7fmR0wwM"
        "Szwuu3zVz3nGUqv4wAMj+zDslV3ItWvX7r1nGN/jo/9Tu838cBrG6uNWta6TY+aHFR/OzXvebaYJ"
        "bzMq5OXl5c+fP3/L1Ee54R4XaGT9yvwM2Gr3BKytzz2q9GtWjUCiHtgJV/Oey9f+Jjw4tXdWtnWf"
        "/f4tHT9O+eS91F1vv/3Ghl27dhWUlpZWW61WobS0tHrXrl0Fb775ZlZycvLLiz9csH32DFXmw2Ob"
        "3/s2JD0pOyn3u7RGZ2CY+drar2qNolnpNKS8MvMD73HmB9Suc5n54WB+V68zTVgsFltRUVHV999/"
        "f2TKlCnL+vfvPzstxdTu8fuVf2pK2waNrXl97yGhQIptlRrHhd3LDhlkcWH3YyeF871G1Diu6j9x"
        "jCLjnVkqn+aW9WXdnftsJ+6YUOuYfKfnTVzyhqWaac7LFBaJ5Us+t2Rn/2T9reC0WFx1Saw16BlN"
        "h/ZM1IA+fNqkcYoB8TFMuLe6VFSJNUl9qh0/ahjSn09f8W+1y3eh2/WofqqmVjQBwOMTFIPemKaq"
        "NyNZrRHm5WstuZt+sP564IhwuqxcrJuBIYIJSUpgogfeyqfeeyffKy6aCbvn0dp3c36yOWZ+OLZd"
        "1+DMD7PmmL784FOLY+aHnC+0MzVqKJ1fP2cKHlxYCKNNTWHb/nkIf8v99yrqzY7g/vp7s3Wldka3"
        "69kOgWpreiqb4GlZqQi/vsp1Zga5BJgQciXANIQmRMbomliEyBj1wITIGAWYEBmjABMiYxRgQmSM"
        "AkyIjNFRaEJkjHpgQmSMAkyIjFGACZExCjAhMkYBJkTGKMCEyBidRiJExqgHJkTGKMCEyBgFmBAZ"
        "owATImN0WdkgEpleM7fxpepc/FU79WrWhbQOCrCM+RPYxtalQMsTnUaSoagbaxsK7nI/NpPpfMce"
        "6OL9GgqyjFAPLCMNBNef0Da0niPM9jIoyPJAAZYBD8FtamgbUi/MFGR5oKPQEucW3uVo+fC6cynD"
        "y3CdSAAFWMI8hLc1UYhlgIbQEhTg4Dqzl51JQ2ppoqPQEhN9k1Eq4XW2HE77xkX71BRiiaAhtIRI"
        "NLx2jvq41ZMEEAVYmqQWXjup1uuaRQGWCKdeTeohWQ5QLywVFGAJkFF47SjEEkEBDjC5h0Du9Zc7"
        "CrB0yKX3tZNbfYMSnUYKoJhuJrkNnd0tB5AZfZNx7oW9Kjq1FADUAxMiYxTgAAmC3tduOeDSHtKK"
        "KMCEyBgFOACCtbcK1nZJGQU4sOQ+fLYLlnbIDv0aKTgpAfQGcAOAdgB0AGwAqgAUAzgCYBeAikBV"
        "kLQMOo0UfFIBPAggxO1xBQA1gCgAaQBMALa3dOH0Pmpd1AO3stibzVfz6PMNAJ4AwFy+XwFgLYBD"
        "AMwAwgHEALgJgKWFy14OIDP2ZvPc83uUdE64lVCAg4cWwEO4Et5aAHMAlDgtc+Hy36+tWzVytdBB"
        "rODRH4DG6f4GuIaXBCEKcPC43u3+7oDUgrQqCnDwiHG6bQZQGqiKkNZDR6GDh9bptjFgtQC9l1oT"
        "9cDBo8bptipgtSCtigIcPC443VYBiAhURUjroQAHj0Nu928JSC1Iq6IAB48fUHfu124ogDYBqgtp"
        "JRTg4FED4FMA9iNIWgDPA+iJuu9CK1D3NcobAEwA0Kv1q0haGn0Tq5UV7lZMjbvFMhd1Mx209Ncp"
        "DwBYgLrvQhsAhAKY2MCyp1q47Eygrn0tvF3iBZ1GCj6/AZiJK79Gao/6v0Y6jLqwtzh6H7Uu6oGD"
        "kxl1+8Q/BLoi5OqifeDAygx0BVpIsLRDdijAAXDuFz4o9xODtV1SRgEmRMYowAHi1FvJffiZCVDv"
        "GygUYEJkjE4jBdDZXdzUtj1sV+uccGvIBOraEeiKXKuoB5YOuQ2l5VbfoEQBDjC5915yr7/cUYAl"
        "wCkEcunVaOgsERRgiZBRiCm8EkIBliaphliq9bpm0VFoCTmzk53arqdgv/C71I5MO8J7ZidLva9E"
        "UA8sMW7hkEqPR+GVKPo1kgTZQ3K5N7aHJxC9MQVX4qgHlrAA98YUXhmgAEuchxBf7SC7lEHhlTYa"
        "QsuA25AacA1xSwyt630oUHDlgQIsIx6CDDQ9zB57cgquvNBpJBk6/TMzFQDa9xLnuj3V5OG1fZtE"
        "XqgHljH30HkItM/rEnmiAAcRCuW1h45CEyJjFGBCZIwCTIiMUYAJkTGn00iBrAYhpCmoByZExijA"
        "hMgYBZgQGaMAEyJjFGBCZIyOQhMiY9QDEyJjFGBCZIwCTIiMUYAJkTEKMCEyRgEmRMboNBIhMkY9"
        "MCEyxhbkMm8CQIdbxemBrgwhpHH2rBbkMm9SD0yIjFGACZExFqjrigEaRhMidc7DZ8CpB6YQEyJt"
        "7uEFAN7T6aMOt4rTT+64shAhJLCSbrvSsTpn1mUf2Dm0zisQQgLHOYvuHWu9g1gUYkKkw1t4AYDJ"
        "/xENfgfLPcA0rCbk6vMnd14D7GljhJDW01in2WiAnVGYCbn6/Bnp/j/yOuwgp4lG2AAAAABJRU5E"
        "rkJggg==",
    "CERAS_E_ENCERADEIRAS":
        "iVBORw0KGgoAAAANSUhEUgAAAPAAAADICAYAAADWfGxSAAAd5UlEQVR4nO3deXwTZf4H8M/kvnsf"
        "aaFUoBzlLkcBi0W5RFBwEYSC4AFUYT32hweIul54sLrLrqtYWVxcAVkWOVQOOQQUoRxyC4htOdtS"
        "Si/Sprnn90eaNEmTpilJkynf9+vVV5PJzOSZaT59nswk82WKvkti0UTqMZcWNHVeQkjzFG9u925T"
        "52W8BZhCS0jweAtzowF2Da8v/xkIIc3jS+7cBthxBRRaQoLHWxZ5vi5ACGk5jhl093bWKcAUXkJC"
        "T2MhbtADuy5ACAk+T5lkCr9tywJAwtjLCwCg6LskCi8hIco1pzx3EwkhocmWUVtm3Q6hCSHcIAh2"
        "A24XCWMvjwp2G1pS0XdJ3we7DbcDhmXZ+QANnwPldguuKwpyYNAQugXc7uEFaB8EGgU4QOiFW4/2"
        "ReDY3wOzbJO/lES8SLz/Cr1gXSSMvTyq8Nu2NJz2MzqIFRyfwzr6eRqAxstjtvslAOYDYGH9u30A"
        "IBxALYCnXJYFADOAMgB7AGxx87jNbgBfAMgAMNNDez8DsL/uthqA7XjJYQAfN7qlJKAowH4WwN43"
        "DkA/WEMzCNbwevI0AAuAFwFMAlAB4IDL467/OPbV/dhMB3APrP8wrjlMz6j7zQLoA0AOoKYpG5B4"
        "/xXqhf2M3gNzgwnAJQD3AWDqfv/uZZkaAGfrbt/h4/MNhDW8ALABQEHdbQbA4Lr2/ABrBzDAx3UT"
        "P6IAc8cWWIM4BdZh7JbGZ4ccQNe62xddHvsIwIq6nwyXx9QAHq27fQrAtw6PdQcQAeAkgF1101yX"
        "Jy2IhtDccRjAQwBGArgC4HQj834E63vgcgBfo/79q427ITQAiAD8EYCkbtnPYB0q29xZ9/sAgKK6"
        "dnQAEA/nYTZpIXQUmjssALYBeATAZi/zegqoNzMAJMIa/k9c1iEFkFZ3e67LcnfC+o/CK3qd+Rf1"
        "wNyyC/VDV6Gf152O+h52LYA8l8cHwNpDfwNgvUMbltYttx7OvTVpARTg4PrI4fYJAH8L4vOqHaZN"
        "qfuxWQ+gR93tMw7TjbAGvQuAVAC/+r2lpFEU4OB43IfHPM1rRP3Bpqas19vjG+t+PPnGw/T3vDwn"
        "CSA6Ck0Ih1GA/ezqN23ogwoe0L7xPwowIRxGp5EC4MqmxO/bjiukLzQ4uLIpkXrfAKAeOEDoBVuP"
        "9kXgUIADiF64tA8CjU4jBZjtBXy7DakpuC2DAtxC6AVNAoGG0IRwGAWYEA6j00iEcBj1wIRwGAWY"
        "EA6jABPCYRRgQjiMAkwIh9FRaEI4jHpgQjiMAkwIh1GACeEwCjAhHEYBJoTDKMCEcBidRiKEw6gH"
        "JoTDKMCEcBhdUieAGL4UinYPQxY/HKKwbuCJIsGyRlj0N2CsvoDa6z+i5soGmHXWypxCZUckjtjn"
        "fcWsGRc3JHpZhgVrqoWptgi6soPQ5C+HoeqMm/mcxQ78N2QJo52mFe4YAqPGcz1xSVQ6lB2egDiq"
        "H/jiGIA1w2LSwKIvh7HmAoyaPFScftv7dhGfUQ8cINK4oWhz7yFE9X4P0vjh4EvVYPhi8AQKCOTJ"
        "kMbdjcgef8bR0rvPlpRbKn1Zt9kCS8eJJdmNz8WAEcggVHaEMnkq4jK/t5QxQ280tgRPGAZp/PAG"
        "0784PHpL3lVTsbtlVB1nIz5zI+RtHoBAmgCGJwTDl4AvjoFQ1Rky9b1QdnyKfX9ldZPKjxLfUIAD"
        "QBo/HHGDV1t7IwBFRUWV06dP/zwmJuZPcrl8bpcuXV4dP378xytWrNi/YXdF7s7D+hPu1pOTk7OX"
        "YZhZrj8CgcBjeG3LKJXKPz7yyCPL2bqjk3yBkBfW/S3LnqN6j4XB5W3GgeE1rFo6derU9E0/6XNd"
        "pwvkyYjo8RoABgDw0Ucf/dCuXbuXJBLJU507d35l4cKFG8rKyqpZFuyyTTXbG99rpDloCO1nPGEY"
        "Yvp/DDDW/42VlZXajIyM97VVl0wvT1NOGtpH3kMirhAVl+0rzz+391rNZT0k3YUea/1mjZRmLspW"
        "TfOlDdZl5NO0uu36q3n7NG1ThqgAoGNKSuykjeJlQ9PQ3d1y8qQJ9tt6vd4kFosFANCuXbuoIn3f"
        "6yx7jmWYurQCkKlHgWGsL6GKigrts88+u2b6aOndsxcqR0WHVaoKSz8rWzJ/xf5u97wX4Uv7SdPR"
        "aSQ/U7afAZ4wzH7/nXfe2VJ2/aL2279Evto2lh9tm36Hmh9/h5ofP7y/qDdg3f9u/wRs43+bxpaR"
        "iiGOEJeIHR8quoHy8pvm6gglT+E4XSBrC0nUAPv9JUuW7HzmmWeGSaVSIQCMGpvV9fDZ+Xn9uwpT"
        "bPPwJTFOTxsVJlS89phisi3kyWpe3ONq00iNdl7tuCGSdHqN+R8Nof3M9T3k2rVrj8z5g/w+x/C2"
        "JIE0wX67tLRUU1JSctNshsV1PkXSQ0B954pVq1blnj+5s9R2f+LEif2+22855LiMSVtovx0RESFb"
        "+dX6J0SRA1hbr2yjlDHSD55WeatdTJqBhtB+JlR0tN+uqanRX7p0qWzM4Kh+zVlXdnZ2ZnZ2w7e7"
        "mourceOXPzW6LE8ghyxhNCQxg+zTFi1atDlSxVNGh/NUrvMrHIbP+fn5padOnSrkVW6TAvcDsAbU"
        "Ej5MZzT9ZBIKrAnVXtuFMKPOIhBKeAAw6t4x3YAxMJv0rLHqNKMvy0X1lY0wVJ5szuaTJqAe2M94"
        "ovpsaDQanUzMiBNj+FH+fI61u2r3zV+q+cLdY9nZ2ZmrtmuntRtXYH0vDgbFxcVVc+bMWfX3v/99"
        "19wJsjGuy4gjekOotI+MsX79+qNJ8fwYlWFnhMViso97//DQ1D4//GI4ZbtvqrmEgp9frjGbzU49"
        "Ol8gZiRRfRHWaS4Sh+2AqNtSrbuDY+TWUYD9zGK4ab+tUCgkcikjae66PB2FnjlzptvweiIQCHhS"
        "kVn01izl1MfGyIa5Pm4dPtfbsGHDsXvTxWkWQyVqSg7YwzlmzJieO49JjjnOKyxbpVz+1sCjn3zy"
        "8Z6CgoJSuJHY5Q+yg1VzjxpNrMmXdhPvKMB+ZqzOs99WKBTiqNgk2a2sL2uENLNgXewy15/3nlLO"
        "cDd/Tk7OXj6fPzs1NfW1Q4cOXQCAmJgY5YdLciam9nsgrsECDB/ytuPtd4uLi6tyc3MLRqaL+wCA"
        "oWQr3/aYWCwWxHYcJ75Zw2odVzGix+V+KcbXOr8+t/uOvj0S38nKylq2b9++PMd5eqaPV/9znXbz"
        "LewK4gYdhfYzbfFOp6O594+b2PPq9eVlTRlGu/sbsGC9HIVu+NjDw0R3vTnrxtSi07NKDb0PmUUi"
        "MR8ABo5drN78z7Tjw9IsvW3zyuIy7eerAUCtVodZLJbPPD3f5ClT+29e/dUvk4dLhjhO75DIV7/+"
        "hCILMOJG1fabueu3/ZbU5mB5UnJKJABER0crth7Q/fLcw7JxjewC4iPqgf3sZsEK1GqrjLb7CxYs"
        "uO9AnvrXlm4HjwHTRlUcW/b7KvuwNSEhITxP/4cCnYG1t891+OzNkCFDUg7mxZwBAGXyZKjaT7ef"
        "87aJDuOpxg4W9I+Rl0XaphUXF1eVa9jq5m4PcY8C7GcWQyWKD8yxWCwWFrAevZ3+/PZehvAJGp4o"
        "AgxfAqHiDsjUIxDTbwmU7SYFtD2mKzlilrXYu+mZT/4pY8New37AeqRanniffd41a9YcdveeOzU1"
        "9TXbPAzDMN3TH44tumEp5wnDEJ32AcIyfqpVdZzFCpUpYPhi8MWRCEvJhjQm3b7uTZs2HY+N4NWf"
        "ICd+QaeRAqFih3j7FxMvpI1ZGh0bG6uMVyeExauXup11zcbc3Jv5OvbBTMkg18c8nUYCgMJdI6Gv"
        "OO61KcbqC7hxYashpv0YMQCkpKTEXjGN2GFhf2SViWMYhi+1z7tx48ZjY+8U9//7c6rZzmu5AW1l"
        "gUkW3l4AAFOnTkv/96J/5HYdhPsAICouRYq4RR7bcOjQoQuLFy/e9ui9ohFeG0x8Qj1wgHRS/nTH"
        "9qW9rr74/B+/3rJly6mioqJKvV5vqq6u1hcUFJRu37791xdeeGHdGx+s/7pWzxp8Xf/4+RWLTuWb"
        "LjZlXuOlT5w+jTX9if8buPOw/rgiaaJ9msFgMG3duvX0yAHWg1cN1nF9m/2ffWpqasL58i6Xawo3"
        "Y8vqF39buXJl7okTJ64UFhZWarVag8lkspSWlmp27959bu7cuasyMjLe7xCvS8geJ7vX1+0kjWNY"
        "lp0PAAXrYt8NdmNao1o9a/h6j27/7qOGk2cvmK5UVLPVAj74UWE8VXI8P/bOnsKuD2RI0uMieeEA"
        "kF9ovjbyufJXm7Luje9FLOzRQZDsusyUEZLMt2crnT4/ffQ3Y/7EVyrfs91P6yzs8L+3w+fPeKvq"
        "b/tOGs4AgFAAwZHPo/+qkDJSuPHelzXrln2j/d52/9vFEa+GKRj5zsOG4yfzTRd/u2wqLL9p0dys"
        "YbUGE2sKk/PknZL4iaMHivtOHi4dIuCD7269xHftH7q+AKAAE8JJtgDTaSRCOIzeAxPCYRRgQjiM"
        "AkwIh1GACeEwCjAhHEYBJoTD6DQSIRxGPTAhHBYyX2YQKVOQNPqA9xlZM/L+V/+9dHfLFf00Gdri"
        "nU7T4gctg6LtgwAAs64UF77p2mDVDF8K1R1TIFOPgDi8O/h1lRTMuhswVhdAW7IH1ZfXw1R7ze9t"
        "rpsRFlMtTLWF0JXmojLvXzBUNv5NRPWd/3H6RhEAXN42GIab593O7+65WdYE1myAxVgJU80V6CqO"
        "Q3PhK+grG15C2l/bXJX/BUp/medlnb7vD8D3fQIAkuiBCE+ZCUlUf+vVNlkLLEYNzPoyGKsvwKD5"
        "HWUn3/T63C2Ncz2w2QJLlylljVYluCZ/8fLeEyaPFzC/UWW5OWh2xTzHabL4u5E85ihi0hZDrh4B"
        "gUMlBaEiGbL4exDd600cLxt29nqF75UUvLXZigFPIINImQJV+0eQeM9OSzn/bo/VFHiicMjUDSsp"
        "rDw6dkt+odltJQW3z8oIwBPIIJAmQBKdjvCUbLQduQfSHjlankDe1NU48bbNa3bq9r66rGall5b5"
        "tD+A5u2T8E5Pos0930LRdjwEskQwPJG1uoQkBqKwLpAnjkZYp7nsX1ZrQ666RMgGuDlVCWzS0tKS"
        "TpWPPMuyaNIbe7l6BBKG/Nd+nePGKils3FOVu+uIwW+VFByXc1dNIbLnO5a9x41u/xkp244DwxM1"
        "mD516tT0b/YZGlRS8PbcgwYNenfVqlUHbY8ldp0gM3VZd73WKNJ7W745f6emtMmX/QH4vk+EimRE"
        "9XodTakusfzb2pCrLhEyQ2h3Jg+XZL41S+5TVQKbWX/88507V2w/NqK/IK2x+XiicMQN/LRBJYWa"
        "ykuml7JkkzL7SHpIRKWia2Ul5flnfrimuWSAONVzJYXmttm6nHiaVrdFfzXvJ03blLvqqyl8I12W"
        "2dvUoJqCsl391wFdKylcM/a/zrKnnSopeH/u8/rzF+cWrvn3haOTH3slDQA6pfaP/fLgS4fS8GYf"
        "sZBxu9238nfy3qam7w/A930iTxjdoLrEI6PEdz/xkmxUdNgNVeGNT8r++uLn+3sMfz8kq0vYe2Br"
        "ZYAg/rjtLH1fzmg0mgGgW7duCfn6By6YLSzrqeoBy7II6/Co20oKa95QvTRuiGhQuAIKiQiiZDUv"
        "flhfYe/3npQ/9uBdosH+bLPjclIxxOGia07XbbZWU7BUO65DIGsLSXT9FS+WLFmys7a21n6pnFFj"
        "s7oeOWfM8/W5e3Xkt+8r/0daWckF+4XrJk7J7vPpt+LNgdpmf+yP5u4Td9UlFs6QTVZHMZFCAQTJ"
        "8by4R0caRnbSPdf9/gxxetBzwjpfIy1kh9DNtWLFiv22208+89qQLQcshxubX6Z2vkjE2rVrjzw5"
        "Xnpfm1heUCopAIBAmmi/ba+mYGGdrr1s7WmcKyn8dsK5ksLmA6xTJYUmY81gyr+zfydYIpEIy5BR"
        "WlXN1jRrfbeoKfsDaN4+MWmv2m/bq0tEpbutLrF4jjzkqkuE7BDa0+VkbhasRMnhZz0ud/To0UuH"
        "9m1qNyBjXFLHjh1jrwkm/mw2f22Bh39WImXDSgqjXwj3ayUFb222sV6jagyksYPt06zVFBhldJhz"
        "NQXHoaKtkgJTscWpkgIiR+iMpj0mocD3v7NR85vT0LtDSueYA79uPfdAAvo6Tr/VbW6ML/sDaN4+"
        "qSnehQi31SV0rKHyNKO7cQCay+uhrwjN6hKc64H/t1u/b2FOTaMXNv9l+9vX2bqLys15ZuFdm/az"
        "Hs978ET1w2eNRqOTihlxYjTPr5UUvLU5Ozs786sdumkdJlxG/MClcK2m8NSDUqdqCpLI3hCpXCop"
        "xPFilLodDSop7DlWX0nBFxaTc2erUqmkBYXma01dvil/J0983R9A8/eJsfoi8vYtcFNdQsJIo/sh"
        "osvTSBq5G9Ken2ndHRwLtpAN8K1UJSgtOltTfH69DrAevKhWTivzdETaYqiy31YoFBJFCFRSAOqr"
        "Kbz+hHzqjNESp2oKynYPO827YcOGYyMHiNLMhgrUXNvvVElh13GZUyWFpuIJnIoXoqqqqra6lq11"
        "nc+f29yYxvYHcGv7hH/9P8plbw5otLpEm64TZEeqnz5qNCGkqkuE7BAaACYPF2e+ObN5RzcNBe9L"
        "LZ0eZHk8PjPnmQWZxSVHy1Tt0OB9rUGTB6nY2uHWV1K42WB9gWxzTk7O3jlz5qzq3Llz/IoVKx4b"
        "MGDAHbZqCl9/qjkLfF8/M8OHMulB+11bJYXn3lBOBADdtc18ZcJdAKyVFOJSxolv1qzTquSMTxUi"
        "RGFdnO6fO3euOEnGJLmb91b+Tu74tD8Av+yTYakX++UXLix+7annd5wpjLjYpefQmDlz5tydkZFh"
        "f4/Va+CD6o9feXvzs5OkIXNx+pDtgW+VUVOAa+fW6AFrtYH23Ua6PQ2gLd7hdP/+cRN7Ft6wlLVA"
        "E51Mukd414bXSt7QnnhcbjDozbbpgx74QP3DMf5x2315/N1OR05tlRQmvVrVIeXhMsSkve+03slT"
        "pvXflmv4xafGMHwo2oy139XpdMbdu3f/1j6Br/Z5w5qpqfsD8N8+6ZDIV//5cVnWf1/Vv/z00K0P"
        "H1k3tuLyxd/LbY9HR0crth30cV8GWOicRnJ7nqdp7Wq4mHW6Pn+xxGQyWABAKBQ2uCIiy7Ko/P1z"
        "1NY4V1LI/V39a0u3GSzAgGUSlEWxpb996VRNId/4UEGt3mJkWdbpQE1TDBkyJOVgftwZX9oc2e15"
        "COXt7A8vXbp0T42mwpCeKujs722+1f1xq/tEmTwFqvbTwYJxamuUilHdN5DXP1p2w6m6RIWm4ekr"
        "Oo0UIMaaK7h+7stGr7lsNlTi6v5sp0oKM17a2csUOVHDt1dSaA95wkjEDfgIquTJAW+34dKnTtUU"
        "Zj35p4yNP5n28wRyKNrUH79paiWFHgOtlRQae06eQAZJVD/ED8pBVLcX7dMPHTp04eWXX94wZYR4"
        "aJiCad7nKm+Rp/0BWI9U38o+4YvCENf/b4jKPFAblpLNilS26hJRiOj8FGSxA+3r3rRp0/GY8NCq"
        "LhGy74Ebq0pwefsw6MqbdmxGl/+hxNhpqlkokni8JjFbtl287fMJF/o9kBMdGxurVKsTwtTqHLfz"
        "/ndTbm7l7wZ2/F0inyop+NJmY3UBSvO3GGI7jrVXUyg0j9whbxPHMnyp/fTOxo0bj40ZLOr/16fl"
        "LpUUrqGmIt8kj+hgr6Sw/K0ludnjJM6f8PfS5q+++urQ7Nmz/9Mp0dTm/yYrHnQ3j7+2uTGe9oeF"
        "3c2q2tzfoLqEL/uk25111SXiU6SI93xlZVt1iekjhSFVXYKTPfCEhTcXnS4wX2zKvKbaa7h+9nOv"
        "Rw47Kvbese3jHldfnNd4JYU3P9zwda3B90oKvrQZAPQX/+lUTWHGzHkDTZEP2YuD2SopDO8ndFtJ"
        "wVCy1amSQl5l6mVPz2WxWFitVmu4evVqxc8//5y3ZMmSnb169XojKytr2dCehl5fvKKY5+ljlI3x"
        "dZsb425/7DpiPK5Krq8t1Zx9Un31O3y38oUmVZdoH6dLmHW/JKSqS9gv7H5+TWTQL+xeUGS+Nnre"
        "zSZVJfh6kWph9/b8ZHfLvf6EbNqU4eJMx/nf/bJ27YotOvsRq+gwnurnT8M+dF1vrZ41bPjRsH/P"
        "UePJs5fMVyqrLdUCPsOPUjGqdvH82ME9BF3HDhbZKyn4q82Th4kz35gpczqSe+y8KX/ynzX2agp9"
        "Ogk6yMSM+OdTRnslhdzPwj1WUli8qnbd8u909kO2G95VvZqazE9y12YeA0YsYoRhckaeEMOL6tGe"
        "nzxhqPjOzkn8Nq7rDcQ2N3d/rHlDOf/xd6r/div7JFzByHceMR4/lW+6eP6KubBCwzpUl2DkKW35"
        "ifemi/pOukccMtUlOk0ud67MEAoBJoQ0jS3AnBxCE0Ks6JpYhHAY9cCEcBgFmBAOowATwmEUYEI4"
        "jAJMCIfRUWhCOIx6YEI4jAJMCIdRgAnhMAowIRxGASaEwyjAhHAYnUYihMOoByaEwyjAhHAYBZgQ"
        "DqMAE8JhIXtZWeK7rlOrGlykz5Ozq8LmBbItpGVQgDnMl8B6W5YCzU10GomDUqfd9BTc1T6sJsvx"
        "ji3QZ1aqKMgcQj0wh3gIri+h9bScPcy256AgcwMFmAPcBLe5ofWkQZgpyNxAR6FDnEt4V8P/4XXl"
        "9ByNDNdJCKAAhzA34W1JFGIOoCF0CApycB3ZnjuLhtShiY5Ch5huj2hCJbyOVsPhvfGvXyopxCGC"
        "htAhJETDa2Nvj0s7SRBRgENTqIXXJlTbdduiAIcIh14t1EOyGqBeOFRQgEMAh8JrQyEOERTgION6"
        "CLjefq6jAIcOrvS+Nlxrb6tEp5GCqPv0aq4NnV2tBpDV7RHNh6f/o6BTS0FAPTAhHEYBDpJW0Pva"
        "rAactoe0IAowIRxGAQ6C1tpbtdbtCmUU4ODi+vDZprVsB+fQt5FaJxGAgQC6A2gDQA7ADEADoBTA"
        "OQCHAVQFq4HEP+g0UuvTFcAMACqX6UIAEgAxAFIB6AH85O8np9dRy6IeuIX1mFETyKPP3QE8BYCp"
        "u18FYCOAXwEYAEQAiAPQG4DRz8+9GkBWjxk1H576Qk7nhFsIBbj1kAF4DPXhrQXwAYAyh3lK6n5O"
        "tmzTSKDQQazW4y4AUof72+AcXtIKUYBbj24u938JSitIi6IAtx5xDrcNAMqD1RDScugodOshc7it"
        "C1orQK+llkQ9cOuhdbgtDlorSIuiALceJQ63xQAig9UQ0nIowK3Hry73+walFaRFUYBbjx9hPfdr"
        "MwpAVJDaQloIBbj10AJYAcB2BEkG4HkAA2D9LLQQ1o9RdgcwDUB6yzeR+Bt9EquFnVwhm9fzUe2H"
        "sFY68PfHKU8B+BjWz0IrAYQBeNTDvJf8/NxZgHX7/Lxe0gg6jdT6nAHwKuq/jdQWDb+NdBbWsPsd"
        "vY5aFvXArZMB1vfEPwa7ISSw6D1wcGUFuwF+0lq2g3MowEFw4t/SVvk+sbVuVyijABPCYRTgIHHo"
        "rbg+/MwCqPcNFgowIRxGp5GC6Pjnknm9H9cF6pxwS8gCrNsR7IbcrqgHDh1cG0pzrb2tEgU4yLje"
        "e3G9/VxHAQ4BDiHgSq9GQ+cQQQEOERwKMYU3hFCAQ1OohjhU23XboqPQIeTYcvG8Pk/obRd+D7Uj"
        "0/bwHlsupt43RFAPHGJcwhEqPR6FN0TRt5FCkC0kdb2xLTzB6I0puCGOeuAQFuTemMLLARTgEOcm"
        "xIEOstNzUHhDGw2hOcBlSA04h9gfQ+sG/xQouNxAAeYQN0EGmh9mtz05BZdb6DQSBx39l2geAKTN"
        "NHzo8lCzh9e2dRJuoR6Yw1xD5ybQTV6WcBMFuBWhUN5+6Cg0IRxGASaEwyjAhHAYBZgQDqPTSIRw"
        "GPXAhHAYBZgQDqMAE8JhFGBCOIwCTAiH0VFoQjiMemBCOIwCTAiHUYAJ4TAKMCEcRgEmhMMowIRw"
        "GJ1GIoTDqAcmhMN4h3P47wJA/2zzgmA3hhDinS2rh3P471IPTAiHUYAJ4TAeYO2KARpGExLqHIfP"
        "gEMPTCEmJLS5hhcABO5OH/XPNi849Cnv3QYPEEKCYsCTFnvH6phZp/fAjqF1XIAQEjyOWXTtWBsc"
        "xKIQExI6GgsvADAHlzIeP4LlGmAaVhMSeL7krtEAu1sZIaTleOs0vQbYEYWZkMDzZaT7/w+Ynsf/"
        "pY7NAAAAAElFTkSuQmCC",
    "CINTOS_E_ARNES":
        "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"
        "PT3d/wdJtXRzFO81swAAAABJRU5ErkJggg==",
    "DESODORIZADORES":
        "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"
        "gg==",
    "DETERGENTES_E_DESINFETANTES":
        "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"
        "gg==",
    "ESPONJAS_E_BUCHAS":
        "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"
        "FjEAAAAASUVORK5CYII=",
    "LIMPADORES_MULTIUSO":
        "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"
        "Cel+nRnp/j9ueJBVjNCCMgAAAABJRU5ErkJggg==",
    "LUVAS":
        "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"
        "+obT0/0/z/Jo9zOb3y8AAAAASUVORK5CYII=",
    "MASCARAS":
        "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",
    "OCULOS_DE_PROTECAO":
        "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",
    "OUTROS_LIMPEZA":
        "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"
        "EMdryUz3/wEeq62nbkMLowAAAABJRU5ErkJggg==",
    "PANOS_E_FLANELAS":
        "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",
    "SABOES_E_SABONETES":
        "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"
        "gtrdRF46RlwAAAAASUVORK5CYII=",
    "SACOS_DE_LIXO":
        "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"
        "Nu8AAAAASUVORK5CYII=",
    "SINALIZACAO_E_OUTROS_EPI":
        "iVBORw0KGgoAAAANSUhEUgAAAPAAAADICAYAAADWfGxSAAAeQ0lEQVR4nO3deXgT1d4H8O9k35ru"
        "LWUrpXShQJHK5rVsgiigsiiIpaCI7KIionLdvRcQFZULiFwWwRe5iIiisgkKKBd6QbGVTYstIJQC"
        "Jd2btNnm/SMkNGnSpm3S5LS/z/P0eTKTmTnnpP32nMwkc7iK1yJ5uEnx+tUF7m5LCGkY7eutFru7"
        "LVdXgCm0hPhOXWGuNcCO4a3PfwZCSMPUJ3dOA1z9ABRaQnynriwK6rsDIaTpVM+gs7ezdgGm8BLi"
        "f2oLcY0e2HEHQojvucokV/5qBA8AyjeuLQCAitciKbyE+CnHnAqcrSSE+CdrRq2ZdTqEJoSwQeTr"
        "CpD6Ub5x7R5vl1HxWuReb5dBPIPjef5FgIbP/q4pguuIguy/aAjNEF+E15flEvdRgP2cr0Pk6/JJ"
        "7WzvgXne7S8lkSaievO6X4RH+ca1e8pfjaDhtB+ik1hsW4+ao6gDADY6ed4EQAPgIIBdDs/PAVDm"
        "zYoS76AA+6l69r51BXAOADOA5wGMA1AE4Gh960O9sP+h98AtRwWAszcfx/iyIsRzqAduHpZXe7wW"
        "wGEn2ygBdL75+IK3K0SaBgW4eahrCL0clvfAhQC+AHCkKSpFvI/OQrcMHjlJRX8j/ofeAxPCMBpC"
        "Nw/V3wNnAXjfVxUhTYsCzLbHvfw88XM0hCaEYRRgP1X2SrhffWjC3+pDLCjAhDCMLiP5sdKXw/aq"
        "/3nD519oKH05jHpfP0U9sJ/zdXh8XT6pHQWYAb4KEYXX/9FlJEZYw9QUQ2oKLjsowIyhcJHqaAhN"
        "CMMowIQwjC4jEcIw6oEJYRgFmBCGUYAJYRgFmBCGUYAJYRidhSaEYdQDE8IwCjAhDKMAE8IwCjAh"
        "DKMAE8IwCjAhDKPLSIQwjHpgQhhGASaEYUzfUkfUoS+kd0yDKLo3BKpw8GYz+KpS8BWFMGtyYSrI"
        "hm7PG7btheFxUD97zLZc9b+Pof3qWZfPA0D5hrEw/LHfbp3ykXWQJI8BAJjLr6NkYYLLOqomboI4"
        "aYTdutL3+8B0PbvGtnXVz5na9gl84TcIgtrVun91FdtmQ//L5ka3ozpOLIfk9jSIE4ZC2LobOEUI"
        "YDKALy+ASZML458Hoc/aBnPpVY+WK1C3grTPFIjiBkIY2hGcTA2+shQmzXkY/zyIqoy1LstkCbM9"
        "sPTOmQiYtguS5NEQBLYBhBJwYhkEqggIIxMhThoOSeoc/o2Dui9cHWNDpv7Qs3u0m2orJzt5wV/7"
        "zxtPuXq+oIIvTVheMs/Zc5w8COKEu2usX6EbuStbY8qvrVx36+eJfaye3Kn9ePNJfY25gxvaDnHc"
        "XVA/nwnFyHchThwKgToKnEgKTqqCIDQG4vjBkA//B47I7z57tdxc7Klypb0fQ+D8TMjueg6idj0t"
        "/zQEInCKEIja3Q7ZoHlQPpdpruw+SVvLy8EEJgMsCI2BYvibAMcBAJYvX/5DdHT0CzKZbGZCQsLL"
        "L7300pcajaacB/gV/6v6rjFlpaSktM9Q3nuWB+p9lk+SPBoQSmqsnzBhQp/PTxszGlMvd5QsSUb7"
        "IOGLHMdNdfzZsmXLccftr127VursOA1phzhxKFSTP4dAFQEAuHLlSvGkSZPWh4eHz1UqlbMTExNf"
        "GTVq1MoNGzYc+SyzNGP3OUOWJ8qV9n4MitHvAyIpAGDPnj2nkpOTX5fJZDOTk5Nf37179ykAEIml"
        "gqjxyxQnotLPOTsOK5gcQks6DwMElqoXFRVpn3766S1TUySDnrxPek+48rr68o0Vmo8mrTvSKe3t"
        "YE+U9/izr9+589W9v94XL0ypVz1vG2d7XFVVZZRKpSIAiI6ODr2g7n2dRxbPAZwn6uhK1kz1W47r"
        "LH/k4+3Wbdq0KWP37t2nJo9TDnbcvr7t4ORBUD78b4Cz9A/FxcXa1NTUJbqCi8Z/DJSNGxIr7qYQ"
        "XZXkleUXZn+7/6oh2wBZe5G4seUK1FFQ3H+ruZmZmZdGjhy5sl9bPnFVumxqbMilyNwdE6/nRH9f"
        "EJvUPRwAUqe/G/PJlN0ZD7XT9HXj5fQ7th6Y53lmfrib/9WtwlRi1aIhsvFtArgQiYAXdQzmImd2"
        "qxza5+c5XR/qIulza1/nL4Kr5w0GgwkAunTp0vpkxKjzJjPPu7rcVqOOQe0giu5je/6DDz7Yr9Pp"
        "DNbloaPTOh+9ZPjTfr+66ufsp377CCI7Q37/Yrtts7Ozr82cOXPTuC7ivoNjRF0b2w5pn8fByQJt"
        "+yxatGhX4ZUL2l3pyhfGdRHfESKDSiaCJDaYazWsk+i25cPlk8d3Ff+tseVK+k6x9bwA8NZbb+1O"
        "CDJFbRqjmN05TNBGIuBFiUHG1qEnloVYt5FKpSJN0uSi/DJTsa//ruvzY8XkENpcfNn2ODg4WLHp"
        "s+1TuPZ9eWuvbKWWcvIPR8gbPAfuhg0bbO8Hp817td+X2XyNYacr0h4P24b4APDpp59m/Hl8X4F1"
        "eezYsT2/zOaOOd3ZSziJAqoJG8CJZLZ1lZWVhnHjxq2OlGiD3h0qT3fcpyHtECfav2/dunXrz3Pv"
        "kA6PDhSEuVvXBpXbaaDdMfbv33/26b7SYRKh/UiTz/leWH35riF3J647oT/obt38CZMB1v+xD0Z9"
        "pdm6PHTYiC4hs/YIgt64zAfM2gfF8DchatO90eWcOHHi4i8/7PgLADp16hSR025cntEMc137AYCk"
        "x1jb45ycnIKTJ0/mSc/tklvXBQcHK6pihlbqTTA2uqJuUox6D8LweLt1zzzzzGe/n866un6kYrpS"
        "wkkd92lIO4RhcbZ9Kioqqi5evKgZ1Vncsz51bVC5oR1t+5SWluo0Gk35gA6izo7H5nUlMGuLbd1Y"
        "bGxs+MELxjP1qZ+/YDLA5sILuPL5CxUmk8kuTAKxjBO37wVZ/6egnnMIxtFrtc5OgtTHyS1vXufN"
        "Zh4AZs57uf/nv+NoXfuI2vawC8r27dtPxAQJwsPz9gabTUbbH87ohyf02JdjONmoCrpJ2nMCpCn2"
        "73s/++yz46tXrz60aLD84a4RwhrXmxraDk5+a/hcVlZWqRBz0nZqQai7dW1wubIA2z5arVYfIOXk"
        "IXJO5bQQg9bWvQcGBiouFJsLnG7n55gMMACoTm4M2DSz14kPV648mJub6/TFj+jzkOL7tk+faEwv"
        "p7l4tkLz8xeVgOXkybWESRozX/sZaUmPh+2Wv/zyy1/vSxCn8NoiVOUesf3TGTFiRPLOS8pfG1o3"
        "dwkjEqEY+a7dupycnIJp06b93+jO4l6P3SYZ4Gy/hraD15XY9lGpVDKVBDLUQ4PLrSyz7aNQKCRy"
        "EVz+9+YkCtvjkpISbWkVz+QlJWYDDAD3h+T2TMlckLBobOd9vRJaL0pLS1tz+PDhP6tv03XgmKil"
        "Ryp3NqYc8Y9vyc0mk6UXfnbBgMtaqcblxgIhJN3H2Bbz8/NLMjIyckfEiXsAAH/2W9v7L6lUKgq5"
        "fZS0xIt/PJxYbnnfK7aNPlFVVWUcN27cR6GCctX798gnerodphu3rsyoVCppaFT0rbTUpTHlanJt"
        "+6nVarlcHVrjzDZgGSFw8iDbck5OToFayrlfRz/C/JcZ4kK4qCVDZGlABQoqvi09/O43f7Rv/Uth"
        "+47xIQAQFham+voPwy8vpkpHOmsjj1ttd/4a8DAW/InCjP9Uhd2ZLouKigo0hA011djq5r7iToNs"
        "1z4BICoqKtBsNv/bVf3Hp6X32rHo/36Z2F3Sr676OVPXPsqR70AYmWj3/HPPPff5qawTV/akKxeo"
        "JJA7O0Zj2qH//TuIom9dlblv9Njkv0pWadwZRjemXMO5gxC1u932XN/+g2M02l3ljsNocadBdsfY"
        "t2/fmQ5BgnAWM8BkDyztOQGyPo/ZrjNahSs59egEQa8o7obtMkF+fn6JRseXN7ZM4U9vyYwGvRkA"
        "xGKx0NV20pSHXT3lVL9+/eIOlUR55QSKtMfDkPa0P7G8ffv2EytWrPjhzUGyscmRwvYu921EOyqP"
        "rkNlebHtks+CBQuGHyppe9qtOjem3Iy1MBqqbEPs559//t6fLnO/2+0gFEM+cK5tsaqqyrhq1aqD"
        "AzuIkupVsJ9gMsCcLBDKMcsgePJ/OumdM3hheDw4kQycMhSy1FkQd7jDtu2OHTsyWykFgbUczi3m"
        "oksoPvqJvtZ6SZSQdLnPtrxly5bjzj4FlZSU9KptH47jkgaNj7hcai5sbB3t6iJVQTnmfbt1Fy5c"
        "0EyZMmXjffHilCdSJHd5qx28rhhFm6eZzTdP/gUHByseXvp997LEcWWcIhicWA5haEdIEu+B6qEV"
        "kN7+iEfKNZdcwfXtf6+yPpeSktI+bvaWID4iycyJpBBGdkbApE/trlDMnTv3s4KreeWTe0gGNuR1"
        "9jUmP4llFdw2Xo62S1w+f+zYsfNvv/32nhnJopofqG0A4U/vygx9001iicxpDyzp9oDde82vvvrq"
        "19Gdxb3W3C+fZr9lHiqv5RhlkbEiAJiQnt7nPzPfy5gXi+HVt5o+ffqA6dOnO61LyfKBMF52ff6L"
        "kyjBSZR26zp06BBaVFS0zNU+Vcc/Qfm2OY1uxzN9pcMlOXulPy4afT5p2pqwiIiIgFZRrQMxeY3T"
        "cjfv/V+G7rSBnzTpgTsaW670xFr5/uumc/2mLYmRSqWifoOHdcLgYTXK1Ov1xmeffXbrqlWrDr5z"
        "t2xClIoLcvW6+DMme2D96W/w3crn/ti0aVNGVlbWpby8vGKtVqs3Go3mgoKCsgMHDvw+e/bsT1NT"
        "U5fEB+haz+ktudcT5ZpL81F6eJ3LM9rSamdP9Xq9cffu3aeGx4l6ONuW/2On7Z9nUlJS69OCrn/V"
        "py5DPqlYmHnVdKE++9Rl02+Gw8/s0W30VDu6lR2MOTyvy+UX5j75xa5du05euXKluKqqylheXl6V"
        "m5tb8N13352eP3/+tlc++uoLnYHXe6rcHpc/jls/Oen4ksWL9hw/fvxCYWFhhdFoNBcWFlYcP378"
        "wuLFi3fFxsb+fc1HK39aMkSWxmrvCwAcz/MvAoDmhcDFdW3sTy6VmjW7zxkzf71qunCmwJxXqDWX"
        "FVdBazDxxkAZp+wcJmzzQILo9ondJf3EAth6zHMa89U71pW/Yl1+9DbJgKVDZemunn93qCzd8TLL"
        "Kz9Ubl31s36fdTlcyanPzg5YCgAPbdW+b/1QgEQI0R9zAt4LkHByOPHawcptK4/p91qXDzyqfEUm"
        "4iTVy6/N/knKl25rJezgqk3XK/iSpJVlz7lzLKv0ZHHqB/fKH21sO7pVe3+tM/D6/5wyHPkux/jb"
        "qeumS4U6vlws5IRhCk7dMUgQMbCDqPOYJHGfKBUX5Mly88v54vUn9AcOXjSeuVBkLijT87oACSfv"
        "ECwIHxAtSnq8h3hg6wCBRz4v39RCl5QsABgOMCEtmTXAzF9GIqQlY/I9MCHEggJMCMMowIQwjAJM"
        "CMMowIQwjAJMCMPoMhIhDKMemBCGMf1lBk8QRsQjZP4vdW9oNqHghaB6H1+gjoL8jicgjr8LwrCO"
        "EMjUMFeWwqw5D332D9AdWQNzac17lDvWqzJjPcq+eNpuG1nKeAQ8cusLAuXbn4Hu6DqEvpoDQYD9"
        "nTvroj3wPip2ver69eB58AYdzMWXYTh/FLr/fgRjvsv73Te43VbimDsgv3MGxNG9IQiIAG82ga8s"
        "g1mrgelGLkzXs1Gx61WX+7cU1AO7ycTDHLW03PlXg1yQ9Z2MkAUnoRjyPMTte0Jwc4YAwc0ZAhSD"
        "5yPwxZNm/W2T67wjx8Ysw6H5+6pqnXFh/r6qTRuzDIfqU0er5cf0e/7xo97lLBbgOHASBYQR8ZD1"
        "eRTqp340X40acsPZpo1tt7zfbATN3Atp9zEQBLW9OeuGHIKACIgiO0PaZQRk/Z/ia61vC0EBdrB6"
        "9epDzr6DKhKJ6h3egAf/Bc6NGQLaTPiXIrPtJI/NEKB5MxYRSsE8a92Dg4Ptuu6dO3f+5ti+F198"
        "0WkYrK9HQEDAkxMnTlxnvTG2UCQWyO9/2/z9eZNdN9zYdgtDY6C6759uzbrx4XF9o2bdaA5a/BDa"
        "mUe7iwe8c7e0xj2S3SUIbA3VyHdsy9YZAlLbmBJXPCKdGht8PjJ3e9r1nOiDthkC+s94L2bD5F0Z"
        "Y9rc8MgMAadnKZdaH3NyZY3n7+4oSv50jGyOO8eyvB5IrzB8WXXl5I9lbZIHqAGgU1xcxPisgDWD"
        "Y7RdAc+0W9JlRI1ZN6b0EA2ada/kngjlFfWlax9oPkxfcyQu/V0mv0XkaS3+LLTTe0o53P2+vmR3"
        "PGHrgQDLDAHxQcaoT0bKZ4uFEAE8EgINrUU/v2dC0kYAlhu0FXV9oij/r0XFrVRckDv1cnZzTJ53"
        "0iYX9/pyVYarchUiSNWGfLt7R18u4wo1WnN5iJxTeaLdAiezbvxzkHi8ZQoVHh2DuMjpQdqhpRkz"
        "dQ92FvVpqX+3VjSE9gJJnP1N0/bv33/2qd7iYWKHGQJM5/bXmCHg40zDQe/XsOEEQW1sjwsKCsqu"
        "XbtWauItN7v3RLtNxZds662zbgiinc+6sXyYtMGzbjQXNIR24Oo2NrpjG1G2dbZbxxCGxdoeW2cI"
        "6N9e4XKGAIEiiAMsMwQcumg6syAVoxpaf2/hpEpIu94PScdU27qFCxfuDJVzAeEKTg14pt363y2z"
        "bogkMgFgmXUDGAGzoZI3XvmNM54/gspft8GYl+nlFrOBemA3bT5pPDz3u6qN7mwrcJwhQMLJg13O"
        "EFBhP0NACe9XMwRMnz59wMYsQ3r4wmtQP7IW4Djk5+eXzJo169Nly5Z9P7ev2Db7tifabdKcx+XP"
        "5juddUMS3RuKgc8gZO5h8A99rOUaOetGc0A9sIPVq1cfmjFjhtPLNWndRKnO1jsyV5ZBoLCcY1Eo"
        "FBK5uLYZAm6dYCopKdGWMTBDgEgkEiiEJsmSIZIJj3UXD7Su91S7FVkfB3xy6KefdT2mlt87bFiX"
        "jh07hjvuH9l3rGLrr9kn7sxenOw4RG9JqAd2YlKyaMC1eco1jj/vD5U+6s7+phs5tsf1nSEgwDpD"
        "gNn+3nkcV22qPttK+1+f0Wh0a+K1+li9evUhoVA4LSkp6dVjx46dB4Dw8PCAd5evHtu53+jI6tt6"
        "pN03jQj6s2f3X+YnLHwwcV/P+Cins250Gzgm6r0MfaNm3WAdBdgL9OcO2C337T84psjJzeUl8fZz"
        "ae/bt+9Mh0AuHAB4bZHdc0FBQQoe9qedq8/BCwAajaZcJPD87zS9q6D/D8P+ekPw+USlXl9lm5Xi"
        "9ifei9pzUZxpXfZEu6uLCxFELR4sSdv1QNnfXwra8fCZt+8p+is323b/7LCwMNU32SY3PkbXfDE5"
        "wbdHJ0p2cRmiMcfU/vffNWcIyBP8bredQATFoGdt5VlnCBgQLUzieR6mikIYbuTajtGnT5+YUj2n"
        "q34McXRvuzofO3bsfJAMqtomhLa1z0UbXb0eHHiunflyRMmRjbahQevWrYNOt3kkV2fgDZ5qt6zn"
        "BMj6TAYPzq5eYXKoR8ahVysU2M26Uajjy339N+STv1vHABPPMZdcwdVtL9jNEJDw5NYgRFpmCBC1"
        "6oygyVsgbnubbR/rDAGPdhcNtK6rPLrW9vuJjo4OffC5ZclcYBteoAiG/G9TIes+2rb/119/nZWX"
        "l1fco5Ugxptt446ukFqnWwWAJ2bPTd161nwE8Ey7OXkQ1GOXQ/z0Lzp56ixeFGGZdUOgDIWi/5OQ"
        "xPzNtu+OHTsyI1Vco2fdYFmLffPvSm2zIRR+0A+GSyfcOo745zXy7wr4cwOmv22ZIWDIsE4YUvsM"
        "AW8NltjNEKD9cQUuqlKudh30UCsAmDhlZl9gZo1jnDp1Km/q1Kkb74kVdvf2DAOmGzkoyvxWH5Ly"
        "gBQA4uLiInJbDd9n5vfwAg6cJ9oNACHt4uVo906N/ayss25M6yr0yKwbrKIA18M9n1YuXJhgntA9"
        "UtDBne27X1wbt+7Rr4+WdZ9acteQuxNjY2PD1Wq1vLS0VJeTk1Owf//+Mx9++OHBa/mXyxbfJUl7"
        "rFrvCwAwmxDyzaMRC7d+ujdxSHp4z549oyMjI9VCoVBQVFSk/e233y5v3779xPr16w/HBBgil97t"
        "3km2RvvvMilSHrAtTpwxr++eJTszh3cS9mhsu6tOfo0jfxn+KAhOKerWrVubsLCwgODgYIVEIhEV"
        "FRVVnDp1Km/btm2/rFmz5qeuoab2s3vJPDLrBqtsN3a/Nk/ZYm/s/meh+Wrqhkq3ZkPYO0H2krsB"
        "tsov54s3ZBkPHLpoOnOhmC8o1/M6lYSTdwjiwvu3FyZN7i4aGBXA1frZ3r05pqzPzxiPZF4zXyzQ"
        "8qVmM8yBMk6RFCZoOzxOmJLWVZQqqeVySkkVr01YqbN9qWFIR2HyplFSp5+Fdnw9JiWLBrw9RGL3"
        "2fDjV8w592+pfMu63Ku1IPab8bIXPdHuy6W8Zk+OKTPzqvnC2RvmvEIdX1ZcyWsNZhgDpZwyMUzQ"
        "5v544e0TuonsZt1oSSKXVtjPzNCSA0wIa6wBppNYhDCsxX8biRCWUQ9MCMMowIQwjAJMCMMowIQw"
        "jAJMCMPoLDQhDKMemBCGUYAJYRgFmBCGUYAJYRgFmBCGUYAJYRhdRiKEYdQDE8IwCjAhDKMAE8Iw"
        "CjAhDKO7UjYjrT+oXFr3VhZXnpHN82ZdSNOgADOsPoGta18KNJvoMhKD2iyrchXczfU4TFr1BWug"
        "856WUpAZQj0wQ1wEtz6hdbWfLczWMijIbKAAM8BJcBsaWldqhJmCzAY6C+3nHMK7GZ4PryO7MmoZ"
        "rhM/QAH2Y07C25QoxAygIbQf8nFwq7OWnUZDav9EZ6H9TNt/6f0lvNVtRrX3xpefklCI/QQNof2I"
        "n4bXylYfh3oSH6IA+yd/C6+Vv9arxaIA+4lqvZq/h2QzQL2wv6AA+wGGwmtFIfYTFGAfYz0ErNef"
        "dRRg/8FK72vFWn2bJbqM5EPtlhtYGzo72gwgre2/9EsvzRHTpSUfoB6YEIZRgH2kGfS+VpsBu/aQ"
        "JkQBJoRhFGAfaK69VXNtlz+jAPsW68Nnq+bSDubQt5Gan1gAAwF0BBAAgAegA1ABoADAVQBf+ahu"
        "xMPoMlLzcheABwFwDuvFANQAogB0hRcDTH9HTYuG0E2s/Qqjt84+hwMYg1vhPQjgZQBPAXgdwNew"
        "9MLeshmwax9pAjSEbj664dY/ZC2Az2EZPgPAdQB7ABwCMK7pq0a8hXrg5iPQYdnZ71YHYGMT1IU0"
        "EQpw81FY7bECwHRYTmjR77gZoyF083EagAGWE1aA5WRV15vrLgP4E8DPAC75pHbEK+gsdPNxA5b3"
        "veNh3+uKAcTc/LkblhB/AsDorYrQ31LToR64eTkMS087AEAXAGFOtukJy0mtb5uwXsRLKMDNz1UA"
        "n918rAYQD0ugY6ttkwIKcLNAJziat1JYhszvw9LrWql8Ux3iaRTg5qMvgFTU/BQWAJhhCbNVSZPU"
        "iHgdDaGbDwWAhwAMBvAjgLMANACkAHrDfgid1eS1I15BAW5iF2cL50WvNC2FZaYDb3yLJxLA2Fqe"
        "vwBgnxfKTQMs7fPCsYkLdBmp+ciE5aOT0QBaw/I+VwHL71gL4AqAEwD+C8DkrUrQ31HToh64+SgE"
        "cMDXlSBNi05i+VaaryvgIc2lHcyhAPvAhVmCZvk+sbm2y59RgAlhGAXYR6r1VqwPP9MA6n19hQJM"
        "CMPoMpIPnZ/JzYtZxXvzmrC3pQGWdvi6Ii0V9cD+g7WhNGv1bZYowD7Geu/Fev1ZRwH2A9VCwEqv"
        "RkNnP0EB9hMMhZjC60cowP7JX0Psr/VqsaqdhfZlNQgA5M7g5nX8iLfeGN3fzkzbwps7g3pff0E9"
        "sJ9xCIe/9HgUXj9F30byQ9aQ3OyNreHxRW9MwfVz1AP7MR/3xhReBlCA/ZyTEHs7yHZlUHj9Gw2h"
        "GeAwpAbsQ+yJoXWNfwoUXDZQgBniJMhAw8PstCen4LKFLiMxKGe6JWSxq3nHuXgbPLy2HpOwhXpg"
        "hjmGzkmg3d6XsIkC3IxQKFseOgtNCMMowIQwjAJMCMMowIQwjC4jEcIw6oEJYRgFmBCGUYAJYRgF"
        "mBCGUYAJYRidhSaEYdQDE8IwCjAhDKMAE8IwCjAhDKMAE8IwCjAhDKPLSIQwjHpgQhgmyH6CWwwA"
        "8Wv5Bb6uDCGkbtasZj/BLaYemBCGUYAJYZgAsHTFAA2jCfF31YfPQLUemEJMiH9zDC8AiJxdPopf"
        "yy/4Y8qtjQghvpWw7lbHWj2zdu+Bq4e2+g6EEN+pnkXHjrXGSSwKMSH+o7bwAgD3++Nw+RksxwDT"
        "sJoQ76tP7moNsLODEUKaTl2dZp0Bro7CTIj31Wek+/8Em5mrq/SB5wAAAABJRU5ErkJggg==",
    "VASSOURAS_E_RODOS":
        "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",
}

_IMAGEM_SUBGRUPO = {
    "AGUA SANITARIA 1L": "AGUA_SANITARIA_E_ALVEJANTES.png",
    "AGUA SANITARIA 2L": "AGUA_SANITARIA_E_ALVEJANTES.png",
    "AGUA SANITARIA 5L": "AGUA_SANITARIA_E_ALVEJANTES.png",
    "ALVEJANTE COM CLORETOS 5L": "AGUA_SANITARIA_E_ALVEJANTES.png",
    "ALVEJANTE OXIGENADO 2L": "AGUA_SANITARIA_E_ALVEJANTES.png",
    "AMACIANTE DE ROUPAS 2L": "OUTROS_LIMPEZA.png",
    "AMACIANTE DE ROUPAS 5L": "OUTROS_LIMPEZA.png",
    "ARNES DE SEGURANCA COM CINTO": "CINTOS_E_ARNES.png",
    "AVENTAL DE LONA 70CM": "AVENTAIS_E_MACACOES.png",
    "AVENTAL DE PVC 70CM": "AVENTAIS_E_MACACOES.png",
    "AVENTAL DESCARTAVEL 70CM PACOTE C/ 10": "AVENTAIS_E_MACACOES.png",
    "BACIA PLASTICA 10L": "OUTROS_LIMPEZA.png",
    "BALDE PLASTICO 10L": "OUTROS_LIMPEZA.png",
    "BALDE PLASTICO 20L": "OUTROS_LIMPEZA.png",
    "BLOCO DESODORIZADOR VASO SANITARIO": "DESODORIZADORES.png",
    "BOTA DE BORRACHA CANO ALTO 39": "CALCADOS_DE_PROTECAO.png",
    "BOTA DE BORRACHA CANO ALTO 40": "CALCADOS_DE_PROTECAO.png",
    "BOTA DE BORRACHA CANO ALTO 41": "CALCADOS_DE_PROTECAO.png",
    "BOTA DE BORRACHA CANO ALTO 42": "CALCADOS_DE_PROTECAO.png",
    "BOTA DE BORRACHA CANO ALTO 43": "CALCADOS_DE_PROTECAO.png",
    "BOTA DE SEGURANCA COM BIQUEIRA ACO 39": "CALCADOS_DE_PROTECAO.png",
    "BOTA DE SEGURANCA COM BIQUEIRA ACO 40": "CALCADOS_DE_PROTECAO.png",
    "BOTA DE SEGURANCA COM BIQUEIRA ACO 41": "CALCADOS_DE_PROTECAO.png",
    "BOTA DE SEGURANCA COM BIQUEIRA ACO 42": "CALCADOS_DE_PROTECAO.png",
    "BOTA DE SEGURANCA COM BIQUEIRA ACO 43": "CALCADOS_DE_PROTECAO.png",
    "BOTA DE SEGURANCA COM BIQUEIRA ACO 44": "CALCADOS_DE_PROTECAO.png",
    "BUCHA DE ACO 8 UNIDADES": "ESPONJAS_E_BUCHAS.png",
    "BUCHA VEGETAL UNIDADE": "ESPONJAS_E_BUCHAS.png",
    "CABO PARA VASSOURA E RODO": "VASSOURAS_E_RODOS.png",
    "CAPACETE DE SEGURANCA AZUL": "CAPACETES_E_PROTECAO_CABECA.png",
    "CAPACETE DE SEGURANCA BRANCO": "CAPACETES_E_PROTECAO_CABECA.png",
    "CAPACETE DE SEGURANCA VERMELHO": "CAPACETES_E_PROTECAO_CABECA.png",
    "CAPUZ PARA CAPACETE": "CAPACETES_E_PROTECAO_CABECA.png",
    "CERA EM PASTA 1KG": "CERAS_E_ENCERADEIRAS.png",
    "CERA LIQUIDA PARA PISO 5L": "CERAS_E_ENCERADEIRAS.png",
    "CINTO DE SEGURANCA TIPO PARAQUEDISTA": "CINTOS_E_ARNES.png",
    "COLETE REFLETIVO G": "SINALIZACAO_E_OUTROS_EPI.png",
    "COLETE REFLETIVO GG": "SINALIZACAO_E_OUTROS_EPI.png",
    "COLETE REFLETIVO M": "SINALIZACAO_E_OUTROS_EPI.png",
    "CONE COM FITA REFLETIVA": "SINALIZACAO_E_OUTROS_EPI.png",
    "CONE DE SINALIZACAO 50CM": "SINALIZACAO_E_OUTROS_EPI.png",
    "CONE DE SINALIZACAO 75CM": "SINALIZACAO_E_OUTROS_EPI.png",
    "DESINFETANTE CONCENTRADO 1L": "DETERGENTES_E_DESINFETANTES.png",
    "DESINFETANTE FLORAL 2L": "DETERGENTES_E_DESINFETANTES.png",
    "DESINFETANTE LAVANDA 5L": "DETERGENTES_E_DESINFETANTES.png",
    "DESODORIZADOR BANHEIRO 300ML": "DESODORIZADORES.png",
    "DESODORIZADOR DE AMBIENTE 2L": "DESODORIZADORES.png",
    "DESODORIZADOR DE AMBIENTE 500ML": "DESODORIZADORES.png",
    "DETERGENTE EM PO 1KG": "DETERGENTES_E_DESINFETANTES.png",
    "DETERGENTE LIQUIDO NEUTRO 500ML": "DETERGENTES_E_DESINFETANTES.png",
    "DETERGENTE LIQUIDO NEUTRO 5L": "DETERGENTES_E_DESINFETANTES.png",
    "ESCORREDOR DE LOUCA": "OUTROS_LIMPEZA.png",
    "ESCOVA DE CHAO COM CABO": "OUTROS_LIMPEZA.png",
    "ESCOVA DE PIA UNIDADE": "OUTROS_LIMPEZA.png",
    "ESPATIFOR 500ML": "OUTROS_LIMPEZA.png",
    "ESPONJA DE ACO PACOTE C/ 6": "ESPONJAS_E_BUCHAS.png",
    "ESPONJA DUPLA FACE PACOTE C/ 3": "ESPONJAS_E_BUCHAS.png",
    "FILTRO PARA MASCARA P2 PAR": "MASCARAS.png",
    "FILTRO PARA MASCARA QUIMICO PAR": "MASCARAS.png",
    "FITA ZEBRADA 50M": "SINALIZACAO_E_OUTROS_EPI.png",
    "FLANELA PARA PISO 50X70CM": "PANOS_E_FLANELAS.png",
    "LIMPADOR DE ALUMINIO 500ML": "OUTROS_LIMPEZA.png",
    "LIMPADOR DE BANHEIRO 500ML": "LIMPADORES_MULTIUSO.png",
    "LIMPADOR DE COZINHA 500ML": "LIMPADORES_MULTIUSO.png",
    "LIMPADOR DE INOX 500ML": "OUTROS_LIMPEZA.png",
    "LIMPADOR DE PISO 5L": "LIMPADORES_MULTIUSO.png",
    "LIMPADOR DE VIDROS 500ML": "LIMPADORES_MULTIUSO.png",
    "LIMPADOR DESENGORDURANTE 5L": "LIMPADORES_MULTIUSO.png",
    "LIMPADOR MULTIUSO 500ML": "LIMPADORES_MULTIUSO.png",
    "LIMPADOR MULTIUSO 5L": "LIMPADORES_MULTIUSO.png",
    "LUSTRA MOVEIS 500ML": "LIMPADORES_MULTIUSO.png",
    "LUSTRA PISO 5L": "CERAS_E_ENCERADEIRAS.png",
    "LUVAS ANTICORTE NIVEL 5 G": "LUVAS.png",
    "LUVAS ANTICORTE NIVEL 5 M": "LUVAS.png",
    "LUVAS DE BORRACHA G": "LUVAS.png",
    "LUVAS DE BORRACHA M": "LUVAS.png",
    "LUVAS DE LATEX G 50UN": "LUVAS.png",
    "LUVAS DE LATEX M 50UN": "LUVAS.png",
    "LUVAS DE PROCEDIMENTO G 100UN": "LUVAS.png",
    "LUVAS DE PROCEDIMENTO M 100UN": "LUVAS.png",
    "LUVAS DE PROCEDIMENTO P 100UN": "LUVAS.png",
    "LUVAS DE VAQUETA G": "LUVAS.png",
    "LUVAS DE VAQUETA M": "LUVAS.png",
    "LUVAS TRICOTADAS COM PALMAS G": "LUVAS.png",
    "LUVAS TRICOTADAS COM PALMAS M": "LUVAS.png",
    "MACACAO BRANCO G": "AVENTAIS_E_MACACOES.png",
    "MACACAO BRANCO GG": "AVENTAIS_E_MACACOES.png",
    "MACACAO BRANCO M": "AVENTAIS_E_MACACOES.png",
    "MACACAO DESCARTAVEL G": "AVENTAIS_E_MACACOES.png",
    "MACACAO DESCARTAVEL GG": "AVENTAIS_E_MACACOES.png",
    "MACACAO DESCARTAVEL M": "AVENTAIS_E_MACACOES.png",
    "MASCARA CIRURGICA CAIXA C/ 50": "MASCARAS.png",
    "MASCARA PFF2 CAIXA C/ 10": "MASCARAS.png",
    "MASCARA PFF2 UNIDADE": "MASCARAS.png",
    "MASCARA SEMI-FACIAL REUTILIZAVEL": "MASCARAS.png",
    "OCULOS DE PROTECAO AMBIDENTRO": "OCULOS_DE_PROTECAO.png",
    "OCULOS DE PROTECAO ESCURO": "OCULOS_DE_PROTECAO.png",
    "OCULOS DE PROTECAO TRANSPARENTE": "OCULOS_DE_PROTECAO.png",
    "PA DE LIXO PLASTICA": "VASSOURAS_E_RODOS.png",
    "PANO DE CHAO ALGODAO 50X50CM": "PANOS_E_FLANELAS.png",
    "PANO DE CHAO TNT 50X50CM": "PANOS_E_FLANELAS.png",
    "PANO DE PRATO ALGODAO 40X40CM": "PANOS_E_FLANELAS.png",
    "PLACA DE SINALIZACAO PISO MOLHADO": "SINALIZACAO_E_OUTROS_EPI.png",
    "PROTECAO LABIAL FPS 30": "SINALIZACAO_E_OUTROS_EPI.png",
    "PROTECAO SOLAR FPS 50 120ML": "SINALIZACAO_E_OUTROS_EPI.png",
    "PROTETOR AURICULAR CONCHA": "CAPACETES_E_PROTECAO_CABECA.png",
    "PROTETOR AURICULAR PLUG CAIXA C/ 100": "CAPACETES_E_PROTECAO_CABECA.png",
    "PROTETOR AURICULAR PLUG UNIDADE": "CAPACETES_E_PROTECAO_CABECA.png",
    "REMOVEDOR DE MANCHAS 500ML": "OUTROS_LIMPEZA.png",
    "REMOVEDOR DE OLEOS 5L": "OUTROS_LIMPEZA.png",
    "RODO COM CABO 60CM": "PANOS_E_FLANELAS.png",
    "RODO DE PISO COM CABO 60CM": "VASSOURAS_E_RODOS.png",
    "RODO DE PISO COM CABO 90CM": "VASSOURAS_E_RODOS.png",
    "SABAO EM BARRA 200G": "SABOES_E_SABONETES.png",
    "SABAO EM PO 1KG": "SABOES_E_SABONETES.png",
    "SABAO EM PO 5KG": "SABOES_E_SABONETES.png",
    "SABAO LIQUIDO PARA PISO 5L": "DETERGENTES_E_DESINFETANTES.png",
    "SABONETE EM BARRA 90G": "SABOES_E_SABONETES.png",
    "SABONETE LIQUIDO 500ML": "SABOES_E_SABONETES.png",
    "SACO DE LIXO 30X40 BRANCO 50UN": "SACOS_DE_LIXO.png",
    "SACO DE LIXO 30X40 PRETO 50UN": "SACOS_DE_LIXO.png",
    "SACO DE LIXO 50X70 BRANCO 25UN": "SACOS_DE_LIXO.png",
    "SACO DE LIXO 50X70 PRETO 25UN": "SACOS_DE_LIXO.png",
    "SACO DE LIXO 60X90 PRETO 15UN": "SACOS_DE_LIXO.png",
    "SACO DE LIXO 70X110 PRETO 10UN": "SACOS_DE_LIXO.png",
    "TALABARTE DUPLO": "CINTOS_E_ARNES.png",
    "TALABARTE SIMPLES": "CINTOS_E_ARNES.png",
    "VASSOURA DE CHAO C/ CABO": "VASSOURAS_E_RODOS.png",
    "VASSOURA DE COCO C/ CABO": "VASSOURAS_E_RODOS.png",
    "VASSOURA DE PIA C/ CABO": "VASSOURAS_E_RODOS.png",
}


ARQ_MODELS_PY = r'''
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from database import Base


class Compra(Base):
    __tablename__ = "compras"

    id = Column(Integer, primary_key=True, autoincrement=True)
    orcamento_id = Column(String(50), nullable=True)
    cliente = Column(String(200), nullable=False)
    material = Column(String(200), nullable=False)
    quantidade = Column(Float, nullable=False, default=1)
    valor_unitario = Column(Float, nullable=False, default=0)
    valor_total = Column(Float, nullable=False, default=0)
    situacao = Column(String(50), nullable=False, default="Orcamento realizado")
    mes = Column(String(2), nullable=False, default="01")
    ano = Column(String(4), nullable=False, default="2024")
    observacao = Column(String(500), nullable=True)
    arquivo_orcamento = Column(String(500), nullable=True)
    arquivo_comprovante = Column(String(500), nullable=True)
    data_criacao = Column(DateTime, nullable=True)
    data_atualizacao = Column(DateTime, nullable=True)


class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(200), nullable=False, unique=True)
    ativo = Column(Boolean, nullable=False, default=True)


class Material(Base):
    __tablename__ = "materiais"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(200), nullable=False, unique=True)
    tipo = Column(String(50), nullable=False, default="material")
    grupo = Column(String(200), nullable=True)
    ativo = Column(Boolean, nullable=False, default=True)
    imagem = Column(String(500), nullable=True)


class GrupoCliente(Base):
    __tablename__ = "grupos_cliente"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(200), nullable=False, unique=True)
'''

ARQ_DATABASE_PY = r'''
import os
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")

SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    pool_pre_ping=True,
)


# Garantir modo WAL e durabilidade maxima em cada conexao
@event.listens_for(engine, "connect")
def _set_sqlite_pragmas(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.execute("PRAGMA synchronous=FULL")
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def init_db():
    """Cria todas as tabelas no banco de dados."""
    from models import Compra, Cliente, Material, GrupoCliente  # noqa: F401
    Base.metadata.create_all(bind=engine)


def get_session():
    """Retorna uma nova sessao do banco."""
    return SessionLocal()
'''

ARQ_SEED_PY = r'''
from database import get_session, init_db
from models import Cliente, Material, GrupoCliente


def _remover_clientes_ficticios(session):
    """Remove clientes ficticios (FILIAL XX) que restaram de versoes anteriores."""
    import re as _re
    ficticios = []
    for grupo in ["ASSAI", "ATACADAO", "MATEUS", "SELF FIT", "SMART FIT"]:
        if grupo == "ASSAI":
            for i in range(1, 21):
                ficticios.append(f"{grupo} - FILIAL {i:02d}")
        elif grupo == "ATACADAO":
            for i in range(1, 21):
                ficticios.append(f"{grupo} - FILIAL {i:02d}")
        elif grupo == "MATEUS":
            for i in range(1, 21):
                ficticios.append(f"GRUPO MATEUS - FILIAL {i:02d}")
                ficticios.append(f"MATEUS - FILIAL {i:02d}")
                ficticios.append(f"CD MATEUS - FILIAL {i:02d}")
        elif grupo == "SELF FIT":
            for i in range(1, 21):
                ficticios.append(f"{grupo} - FILIAL {i:02d}")
                ficticios.append(f"SELFIT - FILIAL {i:02d}")
        elif grupo == "SMART FIT":
            for i in range(1, 21):
                ficticios.append(f"{grupo} - FILIAL {i:02d}")
                ficticios.append(f"SMARTFIT - FILIAL {i:02d}")
    removidos = 0
    for nome in ficticios:
        cliente = session.query(Cliente).filter_by(nome=nome).first()
        if cliente:
            session.delete(cliente)
            removidos += 1
    # Tambem remove qualquer cliente cujo nome combine com padrao FILIAL XX
    todos = session.query(Cliente).all()
    padrao = _re.compile(r'.+- FILIAL \d+$', _re.IGNORECASE)
    for c in todos:
        if padrao.match(c.nome):
            session.delete(c)
            removidos += 1
    if removidos > 0:
        session.commit()
        print(f"  - {removidos} cliente(s) ficticio(s) removido(s)")
    return removidos



# Mapeamento de material para imagem (sub-grupo)
_IMAGEM_SUBGRUPO = {
    "AGUA SANITARIA 1L": "AGUA_SANITARIA_E_ALVEJANTES.png",
    "AGUA SANITARIA 2L": "AGUA_SANITARIA_E_ALVEJANTES.png",
    "AGUA SANITARIA 5L": "AGUA_SANITARIA_E_ALVEJANTES.png",
    "ALVEJANTE COM CLORETOS 5L": "AGUA_SANITARIA_E_ALVEJANTES.png",
    "ALVEJANTE OXIGENADO 2L": "AGUA_SANITARIA_E_ALVEJANTES.png",
    "AMACIANTE DE ROUPAS 2L": "OUTROS_LIMPEZA.png",
    "AMACIANTE DE ROUPAS 5L": "OUTROS_LIMPEZA.png",
    "ARNES DE SEGURANCA COM CINTO": "CINTOS_E_ARNES.png",
    "AVENTAL DE LONA 70CM": "AVENTAIS_E_MACACOES.png",
    "AVENTAL DE PVC 70CM": "AVENTAIS_E_MACACOES.png",
    "AVENTAL DESCARTAVEL 70CM PACOTE C/ 10": "AVENTAIS_E_MACACOES.png",
    "BACIA PLASTICA 10L": "OUTROS_LIMPEZA.png",
    "BALDE PLASTICO 10L": "OUTROS_LIMPEZA.png",
    "BALDE PLASTICO 20L": "OUTROS_LIMPEZA.png",
    "BLOCO DESODORIZADOR VASO SANITARIO": "DESODORIZADORES.png",
    "BOTA DE BORRACHA CANO ALTO 39": "CALCADOS_DE_PROTECAO.png",
    "BOTA DE BORRACHA CANO ALTO 40": "CALCADOS_DE_PROTECAO.png",
    "BOTA DE BORRACHA CANO ALTO 41": "CALCADOS_DE_PROTECAO.png",
    "BOTA DE BORRACHA CANO ALTO 42": "CALCADOS_DE_PROTECAO.png",
    "BOTA DE BORRACHA CANO ALTO 43": "CALCADOS_DE_PROTECAO.png",
    "BOTA DE SEGURANCA COM BIQUEIRA ACO 39": "CALCADOS_DE_PROTECAO.png",
    "BOTA DE SEGURANCA COM BIQUEIRA ACO 40": "CALCADOS_DE_PROTECAO.png",
    "BOTA DE SEGURANCA COM BIQUEIRA ACO 41": "CALCADOS_DE_PROTECAO.png",
    "BOTA DE SEGURANCA COM BIQUEIRA ACO 42": "CALCADOS_DE_PROTECAO.png",
    "BOTA DE SEGURANCA COM BIQUEIRA ACO 43": "CALCADOS_DE_PROTECAO.png",
    "BOTA DE SEGURANCA COM BIQUEIRA ACO 44": "CALCADOS_DE_PROTECAO.png",
    "BUCHA DE ACO 8 UNIDADES": "ESPONJAS_E_BUCHAS.png",
    "BUCHA VEGETAL UNIDADE": "ESPONJAS_E_BUCHAS.png",
    "CABO PARA VASSOURA E RODO": "VASSOURAS_E_RODOS.png",
    "CAPACETE DE SEGURANCA AZUL": "CAPACETES_E_PROTECAO_CABECA.png",
    "CAPACETE DE SEGURANCA BRANCO": "CAPACETES_E_PROTECAO_CABECA.png",
    "CAPACETE DE SEGURANCA VERMELHO": "CAPACETES_E_PROTECAO_CABECA.png",
    "CAPUZ PARA CAPACETE": "CAPACETES_E_PROTECAO_CABECA.png",
    "CERA EM PASTA 1KG": "CERAS_E_ENCERADEIRAS.png",
    "CERA LIQUIDA PARA PISO 5L": "CERAS_E_ENCERADEIRAS.png",
    "CINTO DE SEGURANCA TIPO PARAQUEDISTA": "CINTOS_E_ARNES.png",
    "COLETE REFLETIVO G": "SINALIZACAO_E_OUTROS_EPI.png",
    "COLETE REFLETIVO GG": "SINALIZACAO_E_OUTROS_EPI.png",
    "COLETE REFLETIVO M": "SINALIZACAO_E_OUTROS_EPI.png",
    "CONE COM FITA REFLETIVA": "SINALIZACAO_E_OUTROS_EPI.png",
    "CONE DE SINALIZACAO 50CM": "SINALIZACAO_E_OUTROS_EPI.png",
    "CONE DE SINALIZACAO 75CM": "SINALIZACAO_E_OUTROS_EPI.png",
    "DESINFETANTE CONCENTRADO 1L": "DETERGENTES_E_DESINFETANTES.png",
    "DESINFETANTE FLORAL 2L": "DETERGENTES_E_DESINFETANTES.png",
    "DESINFETANTE LAVANDA 5L": "DETERGENTES_E_DESINFETANTES.png",
    "DESODORIZADOR BANHEIRO 300ML": "DESODORIZADORES.png",
    "DESODORIZADOR DE AMBIENTE 2L": "DESODORIZADORES.png",
    "DESODORIZADOR DE AMBIENTE 500ML": "DESODORIZADORES.png",
    "DETERGENTE EM PO 1KG": "DETERGENTES_E_DESINFETANTES.png",
    "DETERGENTE LIQUIDO NEUTRO 500ML": "DETERGENTES_E_DESINFETANTES.png",
    "DETERGENTE LIQUIDO NEUTRO 5L": "DETERGENTES_E_DESINFETANTES.png",
    "ESCORREDOR DE LOUCA": "OUTROS_LIMPEZA.png",
    "ESCOVA DE CHAO COM CABO": "OUTROS_LIMPEZA.png",
    "ESCOVA DE PIA UNIDADE": "OUTROS_LIMPEZA.png",
    "ESPATIFOR 500ML": "OUTROS_LIMPEZA.png",
    "ESPONJA DE ACO PACOTE C/ 6": "ESPONJAS_E_BUCHAS.png",
    "ESPONJA DUPLA FACE PACOTE C/ 3": "ESPONJAS_E_BUCHAS.png",
    "FILTRO PARA MASCARA P2 PAR": "MASCARAS.png",
    "FILTRO PARA MASCARA QUIMICO PAR": "MASCARAS.png",
    "FITA ZEBRADA 50M": "SINALIZACAO_E_OUTROS_EPI.png",
    "FLANELA PARA PISO 50X70CM": "PANOS_E_FLANELAS.png",
    "LIMPADOR DE ALUMINIO 500ML": "OUTROS_LIMPEZA.png",
    "LIMPADOR DE BANHEIRO 500ML": "LIMPADORES_MULTIUSO.png",
    "LIMPADOR DE COZINHA 500ML": "LIMPADORES_MULTIUSO.png",
    "LIMPADOR DE INOX 500ML": "OUTROS_LIMPEZA.png",
    "LIMPADOR DE PISO 5L": "LIMPADORES_MULTIUSO.png",
    "LIMPADOR DE VIDROS 500ML": "LIMPADORES_MULTIUSO.png",
    "LIMPADOR DESENGORDURANTE 5L": "LIMPADORES_MULTIUSO.png",
    "LIMPADOR MULTIUSO 500ML": "LIMPADORES_MULTIUSO.png",
    "LIMPADOR MULTIUSO 5L": "LIMPADORES_MULTIUSO.png",
    "LUSTRA MOVEIS 500ML": "LIMPADORES_MULTIUSO.png",
    "LUSTRA PISO 5L": "CERAS_E_ENCERADEIRAS.png",
    "LUVAS ANTICORTE NIVEL 5 G": "LUVAS.png",
    "LUVAS ANTICORTE NIVEL 5 M": "LUVAS.png",
    "LUVAS DE BORRACHA G": "LUVAS.png",
    "LUVAS DE BORRACHA M": "LUVAS.png",
    "LUVAS DE LATEX G 50UN": "LUVAS.png",
    "LUVAS DE LATEX M 50UN": "LUVAS.png",
    "LUVAS DE PROCEDIMENTO G 100UN": "LUVAS.png",
    "LUVAS DE PROCEDIMENTO M 100UN": "LUVAS.png",
    "LUVAS DE PROCEDIMENTO P 100UN": "LUVAS.png",
    "LUVAS DE VAQUETA G": "LUVAS.png",
    "LUVAS DE VAQUETA M": "LUVAS.png",
    "LUVAS TRICOTADAS COM PALMAS G": "LUVAS.png",
    "LUVAS TRICOTADAS COM PALMAS M": "LUVAS.png",
    "MACACAO BRANCO G": "AVENTAIS_E_MACACOES.png",
    "MACACAO BRANCO GG": "AVENTAIS_E_MACACOES.png",
    "MACACAO BRANCO M": "AVENTAIS_E_MACACOES.png",
    "MACACAO DESCARTAVEL G": "AVENTAIS_E_MACACOES.png",
    "MACACAO DESCARTAVEL GG": "AVENTAIS_E_MACACOES.png",
    "MACACAO DESCARTAVEL M": "AVENTAIS_E_MACACOES.png",
    "MASCARA CIRURGICA CAIXA C/ 50": "MASCARAS.png",
    "MASCARA PFF2 CAIXA C/ 10": "MASCARAS.png",
    "MASCARA PFF2 UNIDADE": "MASCARAS.png",
    "MASCARA SEMI-FACIAL REUTILIZAVEL": "MASCARAS.png",
    "OCULOS DE PROTECAO AMBIDENTRO": "OCULOS_DE_PROTECAO.png",
    "OCULOS DE PROTECAO ESCURO": "OCULOS_DE_PROTECAO.png",
    "OCULOS DE PROTECAO TRANSPARENTE": "OCULOS_DE_PROTECAO.png",
    "PA DE LIXO PLASTICA": "VASSOURAS_E_RODOS.png",
    "PANO DE CHAO ALGODAO 50X50CM": "PANOS_E_FLANELAS.png",
    "PANO DE CHAO TNT 50X50CM": "PANOS_E_FLANELAS.png",
    "PANO DE PRATO ALGODAO 40X40CM": "PANOS_E_FLANELAS.png",
    "PLACA DE SINALIZACAO PISO MOLHADO": "SINALIZACAO_E_OUTROS_EPI.png",
    "PROTECAO LABIAL FPS 30": "SINALIZACAO_E_OUTROS_EPI.png",
    "PROTECAO SOLAR FPS 50 120ML": "SINALIZACAO_E_OUTROS_EPI.png",
    "PROTETOR AURICULAR CONCHA": "CAPACETES_E_PROTECAO_CABECA.png",
    "PROTETOR AURICULAR PLUG CAIXA C/ 100": "CAPACETES_E_PROTECAO_CABECA.png",
    "PROTETOR AURICULAR PLUG UNIDADE": "CAPACETES_E_PROTECAO_CABECA.png",
    "REMOVEDOR DE MANCHAS 500ML": "OUTROS_LIMPEZA.png",
    "REMOVEDOR DE OLEOS 5L": "OUTROS_LIMPEZA.png",
    "RODO COM CABO 60CM": "PANOS_E_FLANELAS.png",
    "RODO DE PISO COM CABO 60CM": "VASSOURAS_E_RODOS.png",
    "RODO DE PISO COM CABO 90CM": "VASSOURAS_E_RODOS.png",
    "SABAO EM BARRA 200G": "SABOES_E_SABONETES.png",
    "SABAO EM PO 1KG": "SABOES_E_SABONETES.png",
    "SABAO EM PO 5KG": "SABOES_E_SABONETES.png",
    "SABAO LIQUIDO PARA PISO 5L": "DETERGENTES_E_DESINFETANTES.png",
    "SABONETE EM BARRA 90G": "SABOES_E_SABONETES.png",
    "SABONETE LIQUIDO 500ML": "SABOES_E_SABONETES.png",
    "SACO DE LIXO 30X40 BRANCO 50UN": "SACOS_DE_LIXO.png",
    "SACO DE LIXO 30X40 PRETO 50UN": "SACOS_DE_LIXO.png",
    "SACO DE LIXO 50X70 BRANCO 25UN": "SACOS_DE_LIXO.png",
    "SACO DE LIXO 50X70 PRETO 25UN": "SACOS_DE_LIXO.png",
    "SACO DE LIXO 60X90 PRETO 15UN": "SACOS_DE_LIXO.png",
    "SACO DE LIXO 70X110 PRETO 10UN": "SACOS_DE_LIXO.png",
    "TALABARTE DUPLO": "CINTOS_E_ARNES.png",
    "TALABARTE SIMPLES": "CINTOS_E_ARNES.png",
    "VASSOURA DE CHAO C/ CABO": "VASSOURAS_E_RODOS.png",
    "VASSOURA DE COCO C/ CABO": "VASSOURAS_E_RODOS.png",
    "VASSOURA DE PIA C/ CABO": "VASSOURAS_E_RODOS.png",
}

def popular_dados():
    session = get_session()
    try:
        # --- GRUPOS DE CLIENTE ---
        grupos = [
            "ASSAI",
            "ATACADAO",
            "NOVO ATACAREJO",
            "GRUPO MATEUS",
            "SMART FIT",
            "SELF FIT",
            "OUTROS",
        ]
        for nome in grupos:
            existe = session.query(GrupoCliente).filter_by(nome=nome).first()
            if not existe:
                session.add(GrupoCliente(nome=nome))
        session.commit()

        # --- REMOVER CLIENTES FICTICIOS DE VERSOES ANTERIORES ---
        _remover_clientes_ficticios(session)

        # --- CLIENTES (lista conforme screenshots do sistema) ---
        clientes_lista = [
            # ASSAI
            "ASSAI MONTESE - CE",
            "CD ASSAI PAULISTA",
            "ASSAI NATAL RN",
            "ASSAI IMBIRIBEIRA - PE",
            "ASSAI CAMARAGIBE - PE",
            "ASSAI PIEDADE",
            "ASSAI NATAL - RN",
            "ASSAI PAULISTA - PE",
            "ASSAI PAULISTA CD - PE",
            "ASSAI CAMPINA GRANDE - PB",
            "ASSAI NATAL COTEMINAS - RN",
            "ASSAI JOÃO PESSOA-PB",
            "ASSAI PAULO AFONSO-BA",
            "ASSAÍ CD FEIRA DE SANTANA - BA",
            "ASSAI VITORIA DA CONQUISTA - BA",
            "ASSAI GUANAMBI-BA",
            "ASSAI ARAPIRACA -AL",
            "ASSAI CAMACARI-BA",
            "ASSAI CARUARU-PE",
            "ASSAI MUSSURUNGA - BA",
            "ASSAI FEIRA DE SANTANA-BA",
            "ASSAÍ AV. RECIFE",
            "ASSAI JUAZEIRO - BA",
            "ASSAI SALVADOR PARALELA - BA",
            "ASSAI TOMBA - BA",
            "ASSAI MANGABEIRAS - AL",
            "ASSAI FAROL - AL",
            "ASSAI PEIXINHOS/PE",
            "ASSAI CARUARU II - PE",
            "ASSAI BOA VISTA - RR",
            "ASSAI MACAPA II - AP",
            "ASSAI MANAUS - AM",
            "ASSAI BELEM AUGUSTO MONTENEGRO - PA",
            "ASSAI BELEM ALMIRANTE BARROSO - PA",
            "ASSAI CD BELEM - PA",
            "ASSAI BELEM BATISTA CAMPOS - PA",
            "ASSAI CASTANHAL - PA",
            "ASSAI BELEM - PA",
            "ASSAI ANANINDEUA - PA",
            # ATACADAO
            "ATACADAO CARUARU",
            "ATACADAO CAMARAGIBE",
            "ATACADAO IGARASSU",
            "ATACADAO NATAL",
            "ATACADAO MACEIO - JACARECICA",
            "ATACADAO JOAO PESSOA",
            "ATACADAO MACEIO - PETROPOLIS",
            "ATACADAO SANTA RITA - PB",
            "ATACADAO JABOATAO",
            "ATACADAO IPUTINGA",
            "ATACADAO IGARASSU - PE",
            "ATACADAO CAMARAGIBE - PE",
            "ATACADAO JACARECICA-AL",
            "ATACADAO TABULEIRO DOS MARTINS-AL",
            "ATACADAO CAMPINA GRANDE-PB",
            # NOVO ATACAREJO
            "NOVO ATACAREJO CARPINA-PE",
            "NOVO ATACAREJO VITORIA DE SANTO ANTÃO-PE",
            "NOVO ATACAREJO ARCO VERDE-PE",
            "NOVO ATACAREJO STA CRUZ DO CAPIBARIBE-PE",
            "NOVO ATACAREJO BONGI-PE",
            "NOVO ATACAREJO CD VITÓRIA-PE",
            "NOVO ATACAREJO PAULISTA-PE",
            "NOVO ATACAREJO GOIANA-PE",
            "NOVO ATACAREJO GRAVATA-PE",
            "NOVO ATACAREJO ESCADA - PE",
            "NOVO ATACAREJO LIMOEIRO",
            "NOVO ATACAREJO BELO JARDIM - PE",
            "NOVO ATACAREJO RECIFE II",
            "NOVO ATACAREJO SAO LOURENÇO",
            "NOVO ATACAREJO CABO DE SANTO AGOSTINHO",
            "NOVO ATACAREJO - JABOATAO DOS GUARARAPES",
            "NOVO ATACAREJO - BEZERROS",
            "NOVO ATACAREJO - TIMBAUBA",
            "NOVO ATACAREJO - SURUBIM",
            "NOVO ATACAREJO - CARPINA II/PE",
            "NOVO ATACAREJO - AFOGADOS/PE",
            "CD NOVO ATACAREJO - MORENO/PE",
            "NOVO ATACAREJO - PEDRAS DE FOGO/PB",
            "NOVO ATACAREJO - BARREIROS/PE",
            "NOVO ATACAREJO - GUABIRABA/PE",
            "NOVO ATACAREJO - CABEDELO/PB",
            "NOVO ATACAREJO - ARARIPINA/PE",
            "NOVO ATACAREJO - OURICURI/PE",
            "NOVO ATACAREJO - VARZEA/PE",
            "NOVO ATACAREJO - DOIS UNIDOS/PE",
            "NOVO ATACAREJO - RIBEIRAO/PE",
            "NOVO ATACAREJO - CARUARU/PE",
            "NOVO ATACAREJO - ESCRITORIO RECIFE/PE",
            "NOVO ATACAREJO - SALGUEIRO/PE",
            "NOVO ATACAREJO - CAMARAGIBE/PE",
            "NOVO ATACAREJO - PAULISTA II/PE",
            "NOVO ATACAREJO OURO PRETO/PE",
            "NOVO ATACAREJO - IPOJUCA/PE",
            "NOVO ATACAREJO - TORITAMA/PE",
            # GRUPO MATEUS
            "GRUPO MATEUS - SALVADOR (ESCRITORIO)",
            "GRUPO MATEUS - RECIFE (ESCRITORIO)",
            "GRUPO MATEUS - PETROLINA",
            "CD MATEUS - CABO DE STO AGOSTINHO",
            "CD MATEUS - FEIRA DE SANTANA",
            "GRUPO MATEUS- ARACAJU/SE",
            "GRUPO MATEUS - SERRARIA/AL",
            "GRUPO MATEUS - PRADO/AL",
            "GRUPO MATEUS - VITORIA DA CONQUISTA/BA",
            "CD MATEUS - SAO GONCALO/BA",
            "GRUPO MATEUS PEIXINHOS/PE",
            "GRUPO MATEUS AREIAS/PE",
            "GRUPO MATEUS - ITABUNA/BA",
            "GRUPO MATEUS - TABULEIRO/AL",
            "GRUPO MATEUS - ANTARES/AL",
            "GRUPO MATEUS - TEIXEIRA DE FREITAS/BA",
            "GRUPO MATEUS - PORTO SEGURO/BA",
            "GRUPO MATEUS - SANTO AMARO/PE",
            "GRUPO MATEUS - BONGI/PE",
            "GRUPO MATEUS - JANGA/PE",
            "GRUPO MATEUS - CAXANGA/PE",
            "GRUPO MATEUS - MARANGUAPE/PE",
            "GRUPO MATEUS - ALTIPLANO/PB",
            "GRUPO MATEUS - CASA CAIADA/PE",
            "GRUPO MATEUS - EUNAPOLIS/BA",
            "GRUPO MATEUS - CAMPINA GRANDE/PB",
            "GRUPO MATEUS - CABEDELO/PB",
            "GRUPO MATEUS - GUARABIRA/PB",
            "GRUPO MATEUS - CARUARU KENNEDY/PE",
            "GRUPO MATEUS UNIVERSITARIO - CARUARU/PE",
            "GRUPO MATEUS - NOSSA SENHORA DA GLORIA",
            "GRUPO MATEUS - CASA FORTE/PE",
            "GRUPO MATEUS VALENTINA - JOAO PESSOA/PB",
            "GRUPO MATEUS - BOA VIAGEM/PE",
            # SMART FIT
            "SMARTFIT IGARASSU/PE",
            "SMARTFIT CARUARU/PE",
            "SMARTFIT ERNESTO GEISEL - JOAO PESSOA/PB",
            "SMARTFIT PEIXINHOS/PE",
            "SMARTFIT BOA VIAGEM/PE",
            "SMARTFIT SHOPPING CIDADE LUZ/PB",
            "SMARTFIT - PARNAMIRIM/RN",
            "SMARTFIT NATAL IGAPO - RN",
            "SMARTFIT PONTA NEGRA - MANAUS/AM",
            "SMARTFIT FLORES - MANAUS/AM",
            "SMARTFIT TREM - MACAPA/AP",
            "SMARTFIT FLODOALDO - PORTO VELHO/RO",
            "SMARTFIT NOVA PORTO - PORTO VELHO/RO",
            "SMARTFIT NOVO ALEIXO - MANAUS/AM",
            "SMARTFIT TORQUATO TAPAJOS - MANAUS/AM",
            "SMARTFIT VIA NORTE - MANAUS/AM",
            "SMARTFIT GRANDE CIRCULAR - MANAUS/AM",
            "SMARTFIT SÃO JOSE DO OPERARIO/AM",
            "SMARTFIT CACHOEIRINHA - MANAUS/AM",
            "SMARTFIT CIDADE NOVA - MANAUS/AM",
            "SMARTFIT ALVORADA - MANAUS/AM",
            "SMARTFIT - SHOPPING CIDADE LESTE/AM",
            "SMART FIT MANOA - AM",
            "SMART FIT PARQUE MOISAICO - AM",
            "SMART FIT SANTANA - AP",
            # SELF FIT
            "SELFIT VIEIRA ALVES/AM",
            "SELFIT DB PONTA NEGRA/AM",
            "SELFIT MANAUS PLAZA/AM",
            # OUTROS
            "UNIMED CARUARU COOP DE TRABALHO MEDICO",
            "LSF JUAZEIRO DO NORTE-CE",
            "CELISTICS - JABOATAO (EMBRATEL)",
            "CONSTRUTORA BAGGIO",
            "EMPORIO KARLA - MANEPÁ",
            "EMPORIO KARLA - BEIRA MAR",
            "EMPORIO KARLA - PAU AMARELO",
            "GRUPO A B ARAUJO/PE",
            "CAMIL ALIMENTOS/PE",
            "FG SERVICES EIRELI ME",
            "IGREJA EVANGELICA ASSEMBLEIA DE DEUS",
            "UNIMED CARUARU",
            "BOAS COMPRAS",
            "MAIS DISTRIBUIDORA",
            "GALINDO DISTRIBUIDORA E REPRESENTAÇÕES",
            "MV INFORMATICA NORDESTE LTDA",
            "SIGLIA MARIA BARBOSA - ME",
            "ACLF",
            "NORTH WAY SHOPPING",
            "HIPER BOM - PAULISTA/PE",
            "CLINICA LUCILO MARANHAO - PE",
            "LWART SOLUCOES - IGARASSU/PE",
            "ACLF - PAULISTA/PE",
            "ACLF - CARUARU/PE",
            "FG FACILITIES LTDA",
            "AURORA ALIMENTOS - CABO/PE",
            "FS SERVICOS DE JARDINAGEM LTDA",
            "ESCRITORIO MINEIRAO - SALVADOR/BA",
            "AS PARALELA CONSTRUCOES SPE LTDA",
            "SHOPPING DIFUSORA - CARUARU",
            "CONDOMINIO SHOPPING DIFUSORA",
            "CABINE PECAS E ACESSORIOS LTDA-PE",
        ]
        # Remover duplicatas mantendo a ordem
        vistos = set()
        clientes_unicos = []
        for nome in clientes_lista:
            if nome not in vistos:
                vistos.add(nome)
                clientes_unicos.append(nome)

        for nome in clientes_unicos:
            existe = session.query(Cliente).filter_by(nome=nome).first()
            if not existe:
                session.add(Cliente(nome=nome, ativo=True))
        session.commit()

        # --- MATERIAIS DE LIMPEZA ---
        materiais_limpeza = [
            # Detergentes e Desinfetantes
            ("DETERGENTE LIQUIDO NEUTRO 5L",),
            ("DETERGENTE LIQUIDO NEUTRO 500ML",),
            ("DETERGENTE EM PO 1KG",),
            ("DESINFETANTE LAVANDA 5L",),
            ("DESINFETANTE FLORAL 2L",),
            ("DESINFETANTE CONCENTRADO 1L",),
            ("SABAO LIQUIDO PARA PISO 5L",),
            # Agua Sanitaria e Alvejantes
            ("AGUA SANITARIA 5L",),
            ("AGUA SANITARIA 2L",),
            ("AGUA SANITARIA 1L",),
            ("ALVEJANTE COM CLORETOS 5L",),
            ("ALVEJANTE OXIGENADO 2L",),
            # Saboes e Sabonetes
            ("SABAO EM PO 1KG",),
            ("SABAO EM PO 5KG",),
            ("SABAO EM BARRA 200G",),
            ("SABONETE LIQUIDO 500ML",),
            ("SABONETE EM BARRA 90G",),
            # Limpadores Multiuso
            ("LIMPADOR MULTIUSO 500ML",),
            ("LIMPADOR MULTIUSO 5L",),
            ("LIMPADOR DE PISO 5L",),
            ("LIMPADOR DE VIDROS 500ML",),
            ("LIMPADOR DE COZINHA 500ML",),
            ("LIMPADOR DE BANHEIRO 500ML",),
            ("LIMPADOR DESENGORDURANTE 5L",),
            ("LUSTRA MOVEIS 500ML",),
            # Esponjas e Buchas
            ("ESPONJA DUPLA FACE PACOTE C/ 3",),
            ("ESPONJA DE ACO PACOTE C/ 6",),
            ("BUCHA VEGETAL UNIDADE",),
            ("BUCHA DE ACO 8 UNIDADES",),
            # Panos e Flanelas
            ("PANO DE CHAO ALGODAO 50X50CM",),
            ("PANO DE CHAO TNT 50X50CM",),
            ("PANO DE PRATO ALGODAO 40X40CM",),
            ("FLANELA PARA PISO 50X70CM",),
            ("RODO COM CABO 60CM",),
            # Vassouras e Rodos
            ("VASSOURA DE PIA C/ CABO",),
            ("VASSOURA DE CHAO C/ CABO",),
            ("VASSOURA DE COCO C/ CABO",),
            ("RODO DE PISO COM CABO 60CM",),
            ("RODO DE PISO COM CABO 90CM",),
            ("CABO PARA VASSOURA E RODO",),
            ("PA DE LIXO PLASTICA",),
            # Sacos de Lixo
            ("SACO DE LIXO 30X40 PRETO 50UN",),
            ("SACO DE LIXO 50X70 PRETO 25UN",),
            ("SACO DE LIXO 60X90 PRETO 15UN",),
            ("SACO DE LIXO 70X110 PRETO 10UN",),
            ("SACO DE LIXO 30X40 BRANCO 50UN",),
            ("SACO DE LIXO 50X70 BRANCO 25UN",),
            # Ceras e Enceradeiras
            ("CERA LIQUIDA PARA PISO 5L",),
            ("CERA EM PASTA 1KG",),
            ("LUSTRA PISO 5L",),
            # Desodorizadores
            ("DESODORIZADOR DE AMBIENTE 500ML",),
            ("DESODORIZADOR DE AMBIENTE 2L",),
            ("DESODORIZADOR BANHEIRO 300ML",),
            ("BLOCO DESODORIZADOR VASO SANITARIO",),
            # Outros Produtos de Limpeza
            ("AMACIANTE DE ROUPAS 5L",),
            ("AMACIANTE DE ROUPAS 2L",),
            ("REMOVEDOR DE MANCHAS 500ML",),
            ("REMOVEDOR DE OLEOS 5L",),
            ("LIMPADOR DE ALUMINIO 500ML",),
            ("LIMPADOR DE INOX 500ML",),
            ("ESCORREDOR DE LOUCA",),
            ("BALDE PLASTICO 10L",),
            ("BALDE PLASTICO 20L",),
            ("BACIA PLASTICA 10L",),
            ("ESCOVA DE CHAO COM CABO",),
            ("ESCOVA DE PIA UNIDADE",),
            ("ESPATIFOR 500ML",),
        ]

        # --- EPIs ---
        materiais_epi = [
            # Luvas
            ("LUVAS DE PROCEDIMENTO M 100UN",),
            ("LUVAS DE PROCEDIMENTO G 100UN",),
            ("LUVAS DE PROCEDIMENTO P 100UN",),
            ("LUVAS DE LATEX M 50UN",),
            ("LUVAS DE LATEX G 50UN",),
            ("LUVAS DE BORRACHA M",),
            ("LUVAS DE BORRACHA G",),
            ("LUVAS DE VAQUETA M",),
            ("LUVAS DE VAQUETA G",),
            ("LUVAS ANTICORTE NIVEL 5 M",),
            ("LUVAS ANTICORTE NIVEL 5 G",),
            ("LUVAS TRICOTADAS COM PALMAS M",),
            ("LUVAS TRICOTADAS COM PALMAS G",),
            # Mascaras
            ("MASCARA PFF2 UNIDADE",),
            ("MASCARA PFF2 CAIXA C/ 10",),
            ("MASCARA CIRURGICA CAIXA C/ 50",),
            ("MASCARA SEMI-FACIAL REUTILIZAVEL",),
            ("FILTRO PARA MASCARA P2 PAR",),
            ("FILTRO PARA MASCARA QUIMICO PAR",),
            # Oculos de Protecao
            ("OCULOS DE PROTECAO TRANSPARENTE",),
            ("OCULOS DE PROTECAO ESCURO",),
            ("OCULOS DE PROTECAO AMBIDENTRO",),
            # Capacetes e Protecao Cabeca
            ("CAPACETE DE SEGURANCA BRANCO",),
            ("CAPACETE DE SEGURANCA AZUL",),
            ("CAPACETE DE SEGURANCA VERMELHO",),
            ("CAPUZ PARA CAPACETE",),
            ("PROTETOR AURICULAR PLUG UNIDADE",),
            ("PROTETOR AURICULAR PLUG CAIXA C/ 100",),
            ("PROTETOR AURICULAR CONCHA",),
            # Calcados de Protecao
            ("BOTA DE SEGURANCA COM BIQUEIRA ACO 39",),
            ("BOTA DE SEGURANCA COM BIQUEIRA ACO 40",),
            ("BOTA DE SEGURANCA COM BIQUEIRA ACO 41",),
            ("BOTA DE SEGURANCA COM BIQUEIRA ACO 42",),
            ("BOTA DE SEGURANCA COM BIQUEIRA ACO 43",),
            ("BOTA DE SEGURANCA COM BIQUEIRA ACO 44",),
            ("BOTA DE BORRACHA CANO ALTO 39",),
            ("BOTA DE BORRACHA CANO ALTO 40",),
            ("BOTA DE BORRACHA CANO ALTO 41",),
            ("BOTA DE BORRACHA CANO ALTO 42",),
            ("BOTA DE BORRACHA CANO ALTO 43",),
            # Aventais e Macacoes
            ("AVENTAL DE PVC 70CM",),
            ("AVENTAL DE LONA 70CM",),
            ("AVENTAL DESCARTAVEL 70CM PACOTE C/ 10",),
            ("MACACAO BRANCO M",),
            ("MACACAO BRANCO G",),
            ("MACACAO BRANCO GG",),
            ("MACACAO DESCARTAVEL M",),
            ("MACACAO DESCARTAVEL G",),
            ("MACACAO DESCARTAVEL GG",),
            # Cintos e Arnes
            ("CINTO DE SEGURANCA TIPO PARAQUEDISTA",),
            ("TALABARTE SIMPLES",),
            ("TALABARTE DUPLO",),
            ("ARNES DE SEGURANCA COM CINTO",),
            # Sinalizacao e Outros EPIs
            ("CONE DE SINALIZACAO 75CM",),
            ("CONE DE SINALIZACAO 50CM",),
            ("FITA ZEBRADA 50M",),
            ("PLACA DE SINALIZACAO PISO MOLHADO",),
            ("CONE COM FITA REFLETIVA",),
            ("COLETE REFLETIVO M",),
            ("COLETE REFLETIVO G",),
            ("COLETE REFLETIVO GG",),
            ("PROTECAO SOLAR FPS 50 120ML",),
            ("PROTECAO LABIAL FPS 30",),
        ]

        for item in materiais_limpeza:
            nome = item[0]
            existe = session.query(Material).filter_by(nome=nome).first()
            if not existe:
                imagem = _IMAGEM_SUBGRUPO.get(nome)
                session.add(Material(nome=nome, tipo="material", grupo="Material de Limpeza", ativo=True, imagem=imagem))
        session.commit()

        for item in materiais_epi:
            nome = item[0]
            existe = session.query(Material).filter_by(nome=nome).first()
            if not existe:
                imagem = _IMAGEM_SUBGRUPO.get(nome)
                session.add(Material(nome=nome, tipo="epi", grupo="EPI", ativo=True, imagem=imagem))
        session.commit()

        print("Dados iniciais populados com sucesso!")
        print(f"  - {len(grupos)} grupos de cliente")
        print(f"  - {len(clientes_unicos)} clientes")
        print(f"  - {len(materiais_limpeza)} materiais de limpeza")
        print(f"  - {len(materiais_epi)} EPIs")

    except Exception as e:
        session.rollback()
        print(f"Erro ao popular dados: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    init_db()
    popular_dados()
'''

ARQ_APP_PY = r'''
import os
import datetime
import streamlit as st
from zoneinfo import ZoneInfo

# Fuso horario de Sao Paulo (Brasilia)
FUSO_BR = ZoneInfo("America/Sao_Paulo")


def agora_brasil():
    """Retorna datetime atual no fuso horario de Sao Paulo."""
    return datetime.datetime.now(FUSO_BR).replace(tzinfo=None)
from database import init_db, get_session
from models import Compra, Cliente, Material, GrupoCliente

# ============================================================
# CONSTANTES
# ============================================================
SITUACOES = [
    "Orcamento realizado",
    "Enviado ao financeiro",
    "Pago",
    "Entregue",
]

MESES = {
    "01": "Janeiro",
    "02": "Fevereiro",
    "03": "Marco",
    "04": "Abril",
    "05": "Maio",
    "06": "Junho",
    "07": "Julho",
    "08": "Agosto",
    "09": "Setembro",
    "10": "Outubro",
    "11": "Novembro",
    "12": "Dezembro",
}

ANOS = [str(y) for y in range(2023, agora_brasil().year + 2)]

COR_SITUACAO = {
    "Orcamento realizado": "#1e40af",
    "Enviado ao financeiro": "#ca8a04",
    "Pago": "#16a34a",
    "Entregue": "#0891b2",
}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

IMAGENS_DIR = os.path.join(BASE_DIR, "imagens")
os.makedirs(IMAGENS_DIR, exist_ok=True)

# ============================================================
# CONFIGURACAO DA PAGINA
# ============================================================
st.set_page_config(
    page_title="Sistema de Controle de Compras",
    page_icon="\U0001f6d2",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS customizado
st.markdown("""
<style>
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3a5f 0%, #1e40af 100%);
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    .stButton>button {
        background-color: #1e40af;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 8px 20px;
        transition: background-color 0.2s;
    }
    .stButton>button:hover {
        background-color: #1d4ed8;
        color: white;
    }
    .metric-card {
        background: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        text-align: center;
    }
    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        color: white;
        font-size: 0.8em;
        font-weight: 600;
    }
    .dataframe { font-size: 0.85em; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# MIGRACAO DO BANCO (deve ser definida ANTES da chamada)
# ============================================================
def _migrar_banco():
    """Adiciona colunas novas em bancos de dados existentes."""
    import sqlite3
    db_path = os.path.join(BASE_DIR, "database.db")
    if not os.path.exists(db_path):
        return
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        # Verificar se a coluna 'imagem' ja existe na tabela materiais
        cursor.execute("PRAGMA table_info(materiais)")
        colunas = [row[1] for row in cursor.fetchall()]
        if "imagem" not in colunas:
            cursor.execute("ALTER TABLE materiais ADD COLUMN imagem VARCHAR(500)")
            conn.commit()
    except Exception:
        pass
    finally:
        conn.close()


# Inicializar banco na primeira execucao
if "db_initialized" not in st.session_state:
    init_db()
    _migrar_banco()
    st.session_state["db_initialized"] = True


# ============================================================
# FUNCOES AUXILIARES
# ============================================================
def gerar_orcamento_id():
    """Gera um ID unico para o orcamento no formato ORC-YYYYMMDDHHMMSS-XXXXXX."""
    agora = agora_brasil()
    random_part = f"{os.urandom(3).hex()}"
    return f"ORC-{agora.strftime('%Y%m%d%H%M%S')}-{random_part}"


def salvar_arquivo(uploaded_file, prefixo):
    """Salva um arquivo enviado e retorna o caminho relativo."""
    if uploaded_file is None:
        return None
    timestamp = agora_brasil().strftime("%Y%m%d%H%M%S")
    nome_seguro = uploaded_file.name.replace(" ", "_")
    nome_arquivo = f"{prefixo}_{timestamp}_{nome_seguro}"
    caminho = os.path.join(UPLOAD_DIR, nome_arquivo)
    with open(caminho, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return nome_arquivo


def salvar_imagem_material(uploaded_file, material_nome):
    """Salva a imagem de um material e retorna o nome do arquivo."""
    if uploaded_file is None:
        return None
    nome_seguro = material_nome.replace(" ", "_").replace("/", "_")
    ext = os.path.splitext(uploaded_file.name)[1].lower()
    if ext not in ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp']:
        ext = '.png'
    nome_arquivo = f"{nome_seguro}{ext}"
    caminho = os.path.join(IMAGENS_DIR, nome_arquivo)
    with open(caminho, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return nome_arquivo


def obter_clientes_ativos():
    session = get_session()
    try:
        return session.query(Cliente).filter_by(ativo=True).order_by(Cliente.nome).all()
    finally:
        session.close()


def obter_materiais_ativos(tipo=None):
    session = get_session()
    try:
        query = session.query(Material).filter_by(ativo=True)
        if tipo:
            query = query.filter_by(tipo=tipo)
        return query.order_by(Material.grupo, Material.nome).all()
    finally:
        session.close()


def obter_grupos_cliente():
    session = get_session()
    try:
        return session.query(GrupoCliente).order_by(GrupoCliente.nome).all()
    finally:
        session.close()


def obter_imagem_material(material_nome):
    """Retorna o caminho da imagem de um material, ou None se nao existir."""
    session = get_session()
    try:
        mat = session.query(Material).filter_by(nome=material_nome).first()
        if mat and mat.imagem:
            caminho = os.path.join(IMAGENS_DIR, mat.imagem)
            if os.path.exists(caminho):
                return caminho
        return None
    finally:
        session.close()


def badge_situacao_html(situacao):
    cor = COR_SITUACAO.get(situacao, "#6b7280")
    return f'<span class="badge" style="background-color:{cor}">{situacao}</span>'


def formatar_moeda(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


# ============================================================
# PAGINA: DASHBOARD (HOME)
# ============================================================
def pagina_dashboard():
    st.title("\U0001f4ca Painel de Controle")
    st.markdown("---")

    session = get_session()
    try:
        # Totais gerais
        total_itens = session.query(Compra).filter(Compra.orcamento_id.isnot(None)).count()
        orcamentos_unicos = session.query(Compra.orcamento_id).filter(
            Compra.orcamento_id.isnot(None)
        ).distinct().count()

        # Total por situacao - CONTAR POR PEDIDOS (orcamentos), nao por itens
        sit_counts = {}
        for s in SITUACOES:
            sit_counts[s] = session.query(Compra.orcamento_id).filter(
                Compra.orcamento_id.isnot(None), Compra.situacao == s
            ).distinct().count()

        # Valor total (soma de todos os itens de todos os orcamentos)
        from sqlalchemy import func
        valor_total = session.query(func.sum(Compra.valor_total)).filter(
            Compra.orcamento_id.isnot(None)
        ).scalar() or 0

        # Colunas de metricas
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("\U0001f4cb Total de Pedidos", orcamentos_unicos)
        with col2:
            st.metric("\U0001f4e6 Total de Itens", total_itens)
        with col3:
            st.metric("\U0001f4b0 Valor Total", formatar_moeda(valor_total))
        with col4:
            st.metric("\u2705 Pedidos Entregues", sit_counts.get("Entregue", 0))

        st.markdown("---")

        # Cards por situacao
        col_s1, col_s2, col_s3, col_s4 = st.columns(4)
        with col_s1:
            st.markdown(f"""
            <div class="metric-card">
                <h4 style="color:#1e40af; margin:0;">\U0001f4cb Pedidos: Orcamento Realizado</h4>
                <h2 style="color:#1e40af; margin:5px 0;">{sit_counts.get('Orcamento realizado', 0)}</h2>
            </div>
            """, unsafe_allow_html=True)
        with col_s2:
            st.markdown(f"""
            <div class="metric-card">
                <h4 style="color:#ca8a04; margin:0;">\U0001f4e7 Pedidos: Enviado ao Financeiro</h4>
                <h2 style="color:#ca8a04; margin:5px 0;">{sit_counts.get('Enviado ao financeiro', 0)}</h2>
            </div>
            """, unsafe_allow_html=True)
        with col_s3:
            st.markdown(f"""
            <div class="metric-card">
                <h4 style="color:#16a34a; margin:0;">\U0001f4b0 Pedidos: Pagos</h4>
                <h2 style="color:#16a34a; margin:5px 0;">{sit_counts.get('Pago', 0)}</h2>
            </div>
            """, unsafe_allow_html=True)
        with col_s4:
            st.markdown(f"""
            <div class="metric-card">
                <h4 style="color:#0891b2; margin:0;">\U0001f69a Pedidos: Entregues</h4>
                <h2 style="color:#0891b2; margin:5px 0;">{sit_counts.get('Entregue', 0)}</h2>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # Top 10 clientes por valor
        st.subheader("\U0001f3c6 Top 10 Clientes por Valor")
        top_clientes = session.query(
            Compra.cliente,
            func.sum(Compra.valor_total).label("total")
        ).filter(
            Compra.orcamento_id.isnot(None)
        ).group_by(Compra.cliente).order_by(
            func.sum(Compra.valor_total).desc()
        ).limit(10).all()

        if top_clientes:
            for i, (cliente, total) in enumerate(top_clientes, 1):
                st.markdown(f"**{i}.** {cliente} \u2014 {formatar_moeda(total)}")
        else:
            st.info("Nenhum orcamento registrado ainda.")

    finally:
        session.close()


# ============================================================
# PAGINA: LISTAR ORCAMENTOS
# ============================================================
def pagina_orcamentos():
    st.title("\U0001f4cb Orcamentos")

    session = get_session()
    try:
        # Filtros
        col_f1, col_f2, col_f3, col_f4 = st.columns(4)

        with col_f1:
            clientes_lista = [""] + [c.nome for c in obter_clientes_ativos()]
            filtro_cliente = st.selectbox("Cliente", clientes_lista, key="filtro_cliente")
        with col_f2:
            filtro_situacao = st.selectbox("Situacao", [""] + SITUACOES, key="filtro_situacao")
        with col_f3:
            filtro_mes = st.selectbox("Mes", [""] + list(MESES.keys()), format_func=lambda x: MESES.get(x, "Todos") if x else "Todos", key="filtro_mes")
        with col_f4:
            filtro_ano = st.selectbox("Ano", [""] + ANOS, key="filtro_ano")

        # Query base
        query = session.query(Compra).filter(Compra.orcamento_id.isnot(None))

        if filtro_cliente:
            query = query.filter(Compra.cliente == filtro_cliente)
        if filtro_situacao:
            query = query.filter(Compra.situacao == filtro_situacao)
        if filtro_mes:
            query = query.filter(Compra.mes == filtro_mes)
        if filtro_ano:
            query = query.filter(Compra.ano == filtro_ano)

        compras = query.order_by(Compra.data_criacao.desc()).all()

        if not compras:
            st.info("Nenhum orcamento encontrado com os filtros selecionados.")
            return

        # Agrupar por orcamento_id
        orcamentos_dict = {}
        for c in compras:
            if c.orcamento_id not in orcamentos_dict:
                orcamentos_dict[c.orcamento_id] = []
            orcamentos_dict[c.orcamento_id].append(c)

        # Exibir orcamentos
        for orc_id, itens in orcamentos_dict.items():
            primeiro = itens[0]
            valor_total = sum(i.valor_total for i in itens)
            badge = badge_situacao_html(primeiro.situacao)

            with st.expander(
                f"{orc_id} \u2014 {primeiro.cliente} \u2014 {MESES.get(primeiro.mes, primeiro.mes)}/{primeiro.ano}"
            ):
                col_info1, col_info2, col_info3 = st.columns(3)
                with col_info1:
                    st.markdown(f"**Cliente:** {primeiro.cliente}")
                    st.markdown(f"**Situacao:** {badge}", unsafe_allow_html=True)
                with col_info2:
                    st.markdown(f"**Periodo:** {MESES.get(primeiro.mes, primeiro.mes)}/{primeiro.ano}")
                    st.markdown(f"**Itens:** {len(itens)}")
                with col_info3:
                    st.markdown(f"**Valor Total:** {formatar_moeda(valor_total)}")
                    st.markdown(f"**Criado em:** {primeiro.data_criacao.strftime('%d/%m/%Y %H:%M') if primeiro.data_criacao else '-'}")

                # Tabela de itens
                dados_tabela = []
                for i in itens:
                    dados_tabela.append({
                        "ID": i.id,
                        "Material": i.material,
                        "Qtd": i.quantidade,
                        "Valor Unit.": formatar_moeda(i.valor_unitario),
                        "Valor Total": formatar_moeda(i.valor_total),
                        "Situacao": i.situacao,
                        "Obs.": i.observacao or "",
                    })
                st.dataframe(dados_tabela, use_container_width=True, hide_index=True)

                # Anexos
                anexos = []
                if primeiro.arquivo_orcamento:
                    anexos.append(f"\U0001f4ce Orcamento: {primeiro.arquivo_orcamento}")
                if primeiro.arquivo_comprovante:
                    anexos.append(f"\U0001f4ce Comprovante: {primeiro.arquivo_comprovante}")
                if anexos:
                    st.markdown("\n".join(anexos))

                # Botoes
                col_b1, col_b2, col_b3, col_b4, col_b5 = st.columns(5)
                with col_b1:
                    if st.button("\u270f\ufe0f Editar", key=f"edit_{orc_id}"):
                        st.session_state["editar_orcamento_id"] = orc_id
                        st.session_state["pagina_atual"] = "Editar Orcamento"
                        st.rerun()
                with col_b2:
                    if st.button("\U0001f5a8\ufe0f Imprimir", key=f"print_{orc_id}"):
                        st.session_state["imprimir_orcamento_id"] = orc_id
                        st.session_state["pagina_atual"] = "Imprimir"
                        st.rerun()
                with col_b3:
                    if st.button("\U0001f504 Avancar Situacao", key=f"avancar_{orc_id}"):
                        idx_atual = SITUACOES.index(primeiro.situacao) if primeiro.situacao in SITUACOES else -1
                        if idx_atual < len(SITUACOES) - 1:
                            nova_sit = SITUACOES[idx_atual + 1]
                            for item in itens:
                                item.situacao = nova_sit
                                item.data_atualizacao = agora_brasil()
                            session.commit()
                            st.success(f"Situacao atualizada para: {nova_sit}")
                            st.rerun()
                        else:
                            st.warning("Orcamento ja esta na situacao final.")
                with col_b4:
                    if st.button("\u23ea Voltar Situacao", key=f"voltar_{orc_id}"):
                        idx_atual = SITUACOES.index(primeiro.situacao) if primeiro.situacao in SITUACOES else -1
                        if idx_atual > 0:
                            nova_sit = SITUACOES[idx_atual - 1]
                            for item in itens:
                                item.situacao = nova_sit
                                item.data_atualizacao = agora_brasil()
                            session.commit()
                            st.success(f"Situacao atualizada para: {nova_sit}")
                            st.rerun()
                        else:
                            st.warning("Orcamento ja esta na situacao inicial.")
                with col_b5:
                    if st.button("\U0001f5d1\ufe0f Excluir", key=f"delete_{orc_id}"):
                        st.session_state[f"confirmar_excluir_{orc_id}"] = True
                        st.rerun()

                # Confirmacao de exclusao
                if st.session_state.get(f"confirmar_excluir_{orc_id}", False):
                    st.warning(f"\u26a0\ufe0f Tem certeza que deseja excluir o orcamento {orc_id}? Esta acao nao pode ser desfeita!")
                    col_conf1, col_conf2 = st.columns(2)
                    with col_conf1:
                        if st.button("\u2705 Sim, Excluir", key=f"confirm_yes_{orc_id}"):
                            for item in itens:
                                session.delete(item)
                            session.commit()
                            st.success("Orcamento excluido com sucesso!")
                            st.session_state[f"confirmar_excluir_{orc_id}"] = False
                            st.rerun()
                    with col_conf2:
                        if st.button("\u274c Cancelar", key=f"confirm_no_{orc_id}"):
                            st.session_state[f"confirmar_excluir_{orc_id}"] = False
                            st.rerun()

    finally:
        session.close()


# ============================================================
# PAGINA: NOVO ORCAMENTO
# ============================================================
def pagina_novo_orcamento():
    st.title("\u2795 Novo Orcamento")

    # Inicializar session_state para itens
    if "novos_itens" not in st.session_state:
        st.session_state["novos_itens"] = []

    clientes = obter_clientes_ativos()
    if not clientes:
        st.error("Nenhum cliente cadastrado. Cadastre clientes primeiro!")
        return

    clientes_nomes = [c.nome for c in clientes]

    # Selecionar cliente
    cliente_selecionado = st.selectbox("\U0001f3e2 Selecione o Cliente", [""] + clientes_nomes, key="novo_cliente")

    if not cliente_selecionado:
        st.info("Selecione um cliente para comecar.")
        return

    # Periodo
    col_mes, col_ano = st.columns(2)
    with col_mes:
        mes_selecionado = st.selectbox("Mes", list(MESES.keys()), format_func=lambda x: MESES[x], index=agora_brasil().month - 1, key="novo_mes")
    with col_ano:
        ano_selecionado = st.selectbox("Ano", ANOS, index=ANOS.index(str(agora_brasil().year)) if str(agora_brasil().year) in ANOS else 0, key="novo_ano")

    # Observacao geral
    observacao_geral = st.text_area("Observacao (opcional)", key="novo_obs_geral")

    st.markdown("---")
    st.subheader("\U0001f4e6 Itens do Orcamento")

    # Tipo de material
    tipo_material = st.radio("Tipo de Material", ["material", "epi"], format_func=lambda x: "Material de Limpeza" if x == "material" else "EPI", key="novo_tipo_mat", horizontal=True)

    # Selecionar material e quantidade
    materiais = obter_materiais_ativos(tipo=tipo_material)
    if not materiais:
        st.warning("Nenhum material ativo encontrado para este tipo.")
        return

    # Agrupar materiais por grupo
    materiais_por_grupo = {}
    for m in materiais:
        if m.grupo not in materiais_por_grupo:
            materiais_por_grupo[m.grupo] = []
        materiais_por_grupo[m.grupo].append(m.nome)

    # Selectbox com grupos como optgroups
    opcoes_materiais = []
    for grupo, nomes in materiais_por_grupo.items():
        opcoes_materiais.append(f"\u2500\u2500 {grupo} \u2500\u2500")
        for nome in nomes:
            opcoes_materiais.append(nome)

    col_mat, col_img, col_qtd, col_val, col_btn = st.columns([3, 2, 1, 1, 1])
    with col_mat:
        material_sel = st.selectbox("Material", [""] + opcoes_materiais, key="novo_material_sel")
    with col_img:
        # Exibir imagem do material selecionado
        if material_sel and not material_sel.startswith("\u2500\u2500"):
            img_path = obter_imagem_material(material_sel)
            if img_path:
                st.image(img_path, width=150)
            else:
                st.caption("\U0001f4f7 Sem imagem")
        else:
            st.caption("\U0001f4f7 Selecione material")
    with col_qtd:
        qtd = st.number_input("Quantidade", min_value=1, value=1, step=1, key="novo_qtd")
    with col_val:
        valor_unit = st.number_input("Valor Unit. (R$)", min_value=0.0, value=0.0, step=0.01, format="%0.2f", key="novo_valor_unit")
    with col_btn:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("\u2795 Adicionar Item", key="btn_add_item"):
            # Validar que o material selecionado nao e um cabecalho de grupo
            if material_sel and not material_sel.startswith("\u2500\u2500"):
                item = {
                    "material": material_sel,
                    "quantidade": qtd,
                    "valor_unitario": valor_unit,
                    "valor_total": round(qtd * valor_unit, 2),
                    "observacao": "",
                }
                st.session_state["novos_itens"].append(item)
                st.success(f"Item adicionado: {material_sel}")
                st.rerun()
            else:
                st.error("Selecione um material valido.")

    # Lista de itens adicionados
    if st.session_state["novos_itens"]:
        st.markdown("---")
        st.subheader(f"\U0001f4cb Itens Adicionados ({len(st.session_state['novos_itens'])})")

        itens_para_remover = []

        for idx, item in enumerate(st.session_state["novos_itens"]):
            col_i1, col_i2, col_i3, col_i4, col_i5, col_i6 = st.columns([3, 1, 1, 1, 1, 0.5])
            with col_i1:
                st.text(item["material"])
            with col_i2:
                st.text(f"Qtd: {item['quantidade']}")
            with col_i3:
                st.text(formatar_moeda(item["valor_unitario"]))
            with col_i4:
                st.text(formatar_moeda(item["valor_total"]))
            with col_i5:
                obs_key = f"item_obs_{idx}"
                obs_val = st.text_input("Obs.", value=item.get("observacao", ""), key=obs_key, label_visibility="collapsed")
                item["observacao"] = obs_val
            with col_i6:
                if st.button("\U0001f5d1", key=f"remove_item_{idx}"):
                    itens_para_remover.append(idx)

        # Remover itens (fora do loop para nao alterar indices durante iteracao)
        if itens_para_remover:
            for idx in sorted(itens_para_remover, reverse=True):
                st.session_state["novos_itens"].pop(idx)
            st.rerun()

        # Total geral
        total_geral = sum(i["valor_total"] for i in st.session_state["novos_itens"])
        st.markdown(f"### \U0001f4b0 Total do Orcamento: {formatar_moeda(total_geral)}")

    # Upload de arquivos
    st.markdown("---")
    st.subheader("\U0001f4ce Anexos")
    col_up1, col_up2 = st.columns(2)
    with col_up1:
        arquivo_orc = st.file_uploader("Arquivo do Orcamento", type=["pdf", "png", "jpg", "jpeg", "doc", "docx", "xls", "xlsx"], key="novo_arq_orc")
    with col_up2:
        arquivo_comp = st.file_uploader("Comprovante", type=["pdf", "png", "jpg", "jpeg", "doc", "docx", "xls", "xlsx"], key="novo_arq_comp")

    # Botao salvar
    st.markdown("---")
    if st.session_state["novos_itens"]:
        if st.button("\U0001f4be Salvar Orcamento", type="primary", use_container_width=True):
            session = get_session()
            try:
                orc_id = gerar_orcamento_id()
                agora = agora_brasil()

                # Salvar arquivos
                arq_orc_nome = salvar_arquivo(arquivo_orc, "orc") if arquivo_orc else None
                arq_comp_nome = salvar_arquivo(arquivo_comp, "comp") if arquivo_comp else None

                for item in st.session_state["novos_itens"]:
                    compra = Compra(
                        orcamento_id=orc_id,
                        cliente=cliente_selecionado,
                        material=item["material"],
                        quantidade=item["quantidade"],
                        valor_unitario=item["valor_unitario"],
                        valor_total=item["valor_total"],
                        situacao="Orcamento realizado",
                        mes=mes_selecionado,
                        ano=ano_selecionado,
                        observacao=item.get("observacao", "") or observacao_geral,
                        arquivo_orcamento=arq_orc_nome,
                        arquivo_comprovante=arq_comp_nome,
                        data_criacao=agora,
                        data_atualizacao=agora,
                    )
                    session.add(compra)

                session.commit()

                # Verificar se os dados foram realmente persistidos
                count_check = session.query(Compra).filter_by(orcamento_id=orc_id).count()
                if count_check == len(st.session_state["novos_itens"]):
                    st.success(f"\u2705 Orcamento {orc_id} salvo com sucesso! ({count_check} itens)")
                else:
                    st.warning(f"\u26a0\ufe0f Orcamento {orc_id} salvo, mas verificacao encontrou {count_check} itens (esperados {len(st.session_state['novos_itens'])}).")

                # Limpar itens
                st.session_state["novos_itens"] = []
                st.rerun()

            except Exception as e:
                session.rollback()
                st.error(f"Erro ao salvar orcamento: {e}")
            finally:
                session.close()
    else:
        st.info("Adicione pelo menos um item para salvar o orcamento.")


# ============================================================
# PAGINA: EDITAR ORCAMENTO
# ============================================================
def pagina_editar_orcamento():
    st.title("\u270f\ufe0f Editar Orcamento")

    orc_id = st.session_state.get("editar_orcamento_id")
    if not orc_id:
        st.warning("Nenhum orcamento selecionado para edicao. Volte a lista de orcamentos e clique em Editar.")
        if st.button("\U0001f4cb Ir para Orcamentos"):
            st.session_state["pagina_atual"] = "Orcamentos"
            st.rerun()
        return

    session = get_session()
    try:
        itens = session.query(Compra).filter_by(orcamento_id=orc_id).order_by(Compra.id).all()
        if not itens:
            st.error("Orcamento nao encontrado.")
            return

        primeiro = itens[0]

        # Inicializar edicao no session_state
        edit_key = f"edit_itens_{orc_id}"
        if edit_key not in st.session_state:
            st.session_state[edit_key] = []
            for i in itens:
                st.session_state[edit_key].append({
                    "id": i.id,
                    "material": i.material,
                    "quantidade": i.quantidade,
                    "valor_unitario": i.valor_unitario,
                    "valor_total": i.valor_total,
                    "situacao": i.situacao,
                    "observacao": i.observacao or "",
                    "remover": False,
                })

        edit_itens = st.session_state[edit_key]

        # Info do orcamento
        st.markdown(f"**Orcamento:** {orc_id}")
        st.markdown(f"**Cliente:** {primeiro.cliente}")
        st.markdown(f"**Periodo:** {MESES.get(primeiro.mes, primeiro.mes)}/{primeiro.ano}")

        # Alterar situacao de todo o orcamento
        nova_sit = st.selectbox("Situacao do Orcamento", SITUACOES,
                                index=SITUACOES.index(primeiro.situacao) if primeiro.situacao in SITUACOES else 0,
                                key=f"edit_sit_{orc_id}")

        st.markdown("---")
        st.subheader("\U0001f4e6 Itens")

        # Editar cada item
        for idx, item in enumerate(edit_itens):
            if item.get("remover"):
                continue

            with st.container():
                col_e1, col_e2, col_e3, col_e4, col_e5, col_e6 = st.columns([3, 1, 1, 1, 1, 0.5])
                with col_e1:
                    st.text(item["material"])
                with col_e2:
                    nova_qtd = st.number_input("Qtd", value=item["quantidade"], min_value=1, step=1, key=f"edit_qtd_{idx}_{orc_id}")
                    item["quantidade"] = nova_qtd
                with col_e3:
                    novo_val = st.number_input("Val.Unit", value=item["valor_unitario"], min_value=0.0, step=0.01, format="%0.2f", key=f"edit_val_{idx}_{orc_id}")
                    item["valor_unitario"] = novo_val
                with col_e4:
                    item["valor_total"] = round(nova_qtd * novo_val, 2)
                    st.text(formatar_moeda(item["valor_total"]))
                with col_e5:
                    nova_obs = st.text_input("Obs", value=item.get("observacao", ""), key=f"edit_obs_{idx}_{orc_id}", label_visibility="collapsed")
                    item["observacao"] = nova_obs
                with col_e6:
                    if st.button("\U0001f5d1", key=f"edit_remove_{idx}_{orc_id}"):
                        item["remover"] = True
                        st.rerun()

        # Adicionar novo item ao orcamento existente
        st.markdown("---")
        st.subheader("\u2795 Adicionar Novo Item")

        tipo_add = st.radio("Tipo", ["material", "epi"], format_func=lambda x: "Material de Limpeza" if x == "material" else "EPI", key=f"add_tipo_{orc_id}", horizontal=True)
        mats_add = obter_materiais_ativos(tipo=tipo_add)

        if mats_add:
            mats_por_grupo = {}
            for m in mats_add:
                if m.grupo not in mats_por_grupo:
                    mats_por_grupo[m.grupo] = []
                mats_por_grupo[m.grupo].append(m.nome)

            opcoes = []
            for grupo, nomes in mats_por_grupo.items():
                opcoes.append(f"\u2500\u2500 {grupo} \u2500\u2500")
                for nome in nomes:
                    opcoes.append(nome)

            col_a1, col_a_img, col_a2, col_a3, col_a4 = st.columns([3, 2, 1, 1, 1])
            with col_a1:
                mat_add = st.selectbox("Material", [""] + opcoes, key=f"add_mat_{orc_id}")
            with col_a_img:
                # Exibir imagem do material selecionado
                if mat_add and not mat_add.startswith("\u2500\u2500"):
                    img_path = obter_imagem_material(mat_add)
                    if img_path:
                        st.image(img_path, width=150)
                    else:
                        st.caption("\U0001f4f7 Sem imagem")
                else:
                    st.caption("\U0001f4f7 Selecione material")
            with col_a2:
                qtd_add = st.number_input("Qtd", min_value=1, value=1, step=1, key=f"add_qtd_{orc_id}")
            with col_a3:
                val_add = st.number_input("Valor Unit.", min_value=0.0, value=0.0, step=0.01, format="%0.2f", key=f"add_val_{orc_id}")
            with col_a4:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("\u2795 Adicionar", key=f"btn_add_exist_{orc_id}"):
                    if mat_add and not mat_add.startswith("\u2500\u2500"):
                        edit_itens.append({
                            "id": None,  # novo item
                            "material": mat_add,
                            "quantidade": qtd_add,
                            "valor_unitario": val_add,
                            "valor_total": round(qtd_add * val_add, 2),
                            "situacao": nova_sit,
                            "observacao": "",
                            "remover": False,
                        })
                        st.success(f"Item adicionado: {mat_add}")
                        st.rerun()
                    else:
                        st.error("Selecione um material valido.")

        # Total
        total = sum(i["valor_total"] for i in edit_itens if not i.get("remover"))
        st.markdown(f"### \U0001f4b0 Total: {formatar_moeda(total)}")

        # Upload de novos arquivos
        st.markdown("---")
        col_up1, col_up2 = st.columns(2)
        with col_up1:
            arq_orc = st.file_uploader("Novo Arquivo Orcamento", type=["pdf", "png", "jpg", "jpeg", "doc", "docx", "xls", "xlsx"], key=f"edit_arq_orc_{orc_id}")
        with col_up2:
            arq_comp = st.file_uploader("Novo Comprovante", type=["pdf", "png", "jpg", "jpeg", "doc", "docx", "xls", "xlsx"], key=f"edit_arq_comp_{orc_id}")

        # Salvar alteracoes
        st.markdown("---")
        col_save, col_cancel = st.columns(2)
        with col_save:
            if st.button("\U0001f4be Salvar Alteracoes", type="primary", use_container_width=True, key=f"save_edit_{orc_id}"):
                try:
                    agora = agora_brasil()

                    # Salvar arquivos
                    arq_orc_nome = salvar_arquivo(arq_orc, "orc") if arq_orc else primeiro.arquivo_orcamento
                    arq_comp_nome = salvar_arquivo(arq_comp, "comp") if arq_comp else primeiro.arquivo_comprovante

                    # Atualizar itens existentes e criar novos
                    ids_restantes = []
                    for item_data in edit_itens:
                        if item_data.get("remover"):
                            # Excluir item
                            if item_data["id"]:
                                item_db = session.query(Compra).get(item_data["id"])
                                if item_db:
                                    session.delete(item_db)
                            continue

                        if item_data["id"]:
                            # Atualizar existente
                            item_db = session.query(Compra).get(item_data["id"])
                            if item_db:
                                item_db.quantidade = item_data["quantidade"]
                                item_db.valor_unitario = item_data["valor_unitario"]
                                item_db.valor_total = item_data["valor_total"]
                                item_db.situacao = nova_sit
                                item_db.observacao = item_data["observacao"]
                                item_db.arquivo_orcamento = arq_orc_nome
                                item_db.arquivo_comprovante = arq_comp_nome
                                item_db.data_atualizacao = agora
                                ids_restantes.append(item_data["id"])
                        else:
                            # Criar novo
                            nova_compra = Compra(
                                orcamento_id=orc_id,
                                cliente=primeiro.cliente,
                                material=item_data["material"],
                                quantidade=item_data["quantidade"],
                                valor_unitario=item_data["valor_unitario"],
                                valor_total=item_data["valor_total"],
                                situacao=nova_sit,
                                mes=primeiro.mes,
                                ano=primeiro.ano,
                                observacao=item_data["observacao"],
                                arquivo_orcamento=arq_orc_nome,
                                arquivo_comprovante=arq_comp_nome,
                                data_criacao=agora,
                                data_atualizacao=agora,
                            )
                            session.add(nova_compra)

                    session.commit()

                    # Verificar persistencia
                    count_check = session.query(Compra).filter_by(orcamento_id=orc_id).count()
                    st.success(f"\u2705 Orcamento atualizado com sucesso! ({count_check} itens)")

                    # Limpar session state de edicao
                    if edit_key in st.session_state:
                        del st.session_state[edit_key]
                    st.session_state["editar_orcamento_id"] = None
                    st.session_state["pagina_atual"] = "Orcamentos"
                    st.rerun()

                except Exception as e:
                    session.rollback()
                    st.error(f"Erro ao salvar: {e}")

        with col_cancel:
            if st.button("\u274c Cancelar", use_container_width=True, key=f"cancel_edit_{orc_id}"):
                if edit_key in st.session_state:
                    del st.session_state[edit_key]
                st.session_state["editar_orcamento_id"] = None
                st.session_state["pagina_atual"] = "Orcamentos"
                st.rerun()

    finally:
        session.close()


# ============================================================
# PAGINA: IMPRIMIR ORCAMENTO
# ============================================================
def pagina_imprimir_orcamento():
    st.title("\U0001f5a8\ufe0f Imprimir Orcamento")

    orc_id = st.session_state.get("imprimir_orcamento_id")
    if not orc_id:
        # Selecionar orcamento manualmente
        session = get_session()
        try:
            orc_ids = session.query(Compra.orcamento_id).filter(
                Compra.orcamento_id.isnot(None)
            ).distinct().order_by(Compra.orcamento_id.desc()).all()
            orc_ids = [o[0] for o in orc_ids]
            if not orc_ids:
                st.info("Nenhum orcamento cadastrado.")
                return
            orc_id = st.selectbox("Selecione o Orcamento", orc_ids, key="imprimir_sel")
        finally:
            session.close()

    if not orc_id:
        return

    session = get_session()
    try:
        itens = session.query(Compra).filter_by(orcamento_id=orc_id).order_by(Compra.id).all()
        if not itens:
            st.error("Orcamento nao encontrado.")
            return

        primeiro = itens[0]
        valor_total = sum(i.valor_total for i in itens)
        cor_sit = COR_SITUACAO.get(primeiro.situacao, "#6b7280")

        # Gerar HTML para impressao
        linhas_tabela = ""
        for idx, i in enumerate(itens, 1):
            linhas_tabela += f"""
            <tr>
                <td style="padding:8px;border:1px solid #ddd;text-align:center;">{idx}</td>
                <td style="padding:8px;border:1px solid #ddd;">{i.material}</td>
                <td style="padding:8px;border:1px solid #ddd;text-align:center;">{i.quantidade:.0f}</td>
                <td style="padding:8px;border:1px solid #ddd;text-align:right;">R$ {i.valor_unitario:,.2f}</td>
                <td style="padding:8px;border:1px solid #ddd;text-align:right;">R$ {i.valor_total:,.2f}</td>
                <td style="padding:8px;border:1px solid #ddd;text-align:center;font-size:0.8em;">{i.observacao or ''}</td>
            </tr>"""

        anexos_html = ""
        if primeiro.arquivo_orcamento:
            anexos_html += f'<p>\U0001f4ce Arquivo Orcamento: {primeiro.arquivo_orcamento}</p>'
        if primeiro.arquivo_comprovante:
            anexos_html += f'<p>\U0001f4ce Comprovante: {primeiro.arquivo_comprovante}</p>'

        html_impressao = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Orcamento {orc_id}</title>
            <style>
                @media print {{
                    .no-print {{ display: none; }}
                    body {{ margin: 0; }}
                }}
                body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 30px; color: #333; }}
                .header {{ text-align: center; margin-bottom: 20px; }}
                .header h1 {{ color: #1e40af; margin: 0; }}
                .header p {{ color: #666; margin: 5px 0; }}
                .info-box {{ background: #f8f9fa; border-radius: 8px; padding: 15px; margin: 15px 0; display: flex; justify-content: space-between; }}
                .info-box div {{ flex: 1; }}
                table {{ width: 100%; border-collapse: collapse; margin: 15px 0; }}
                th {{ background: #1e40af; color: white; padding: 10px; text-align: center; }}
                .total-row {{ background: #e8f0fe; font-weight: bold; }}
                .badge {{ display: inline-block; padding: 4px 12px; border-radius: 20px; color: white; font-size: 0.9em; background-color: {cor_sit}; }}
                .footer {{ margin-top: 30px; text-align: center; color: #999; font-size: 0.8em; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>\U0001f6d2 Sistema de Controle de Compras</h1>
                <p>Orcamento</p>
            </div>

            <div class="info-box">
                <div>
                    <strong>Cliente:</strong> {primeiro.cliente}<br>
                    <strong>Situacao:</strong> <span class="badge">{primeiro.situacao}</span>
                </div>
                <div>
                    <strong>Periodo:</strong> {MESES.get(primeiro.mes, primeiro.mes)}/{primeiro.ano}<br>
                    <strong>Data:</strong> {primeiro.data_criacao.strftime('%d/%m/%Y %H:%M') if primeiro.data_criacao else '-'}
                </div>
                <div>
                    <strong>ID:</strong> {orc_id}<br>
                    <strong>Itens:</strong> {len(itens)}
                </div>
            </div>

            <table>
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Material</th>
                        <th>Qtd</th>
                        <th>Valor Unit.</th>
                        <th>Valor Total</th>
                        <th>Obs.</th>
                    </tr>
                </thead>
                <tbody>
                    {linhas_tabela}
                    <tr class="total-row">
                        <td colspan="4" style="padding:10px;border:1px solid #ddd;text-align:right;"><strong>TOTAL</strong></td>
                        <td style="padding:10px;border:1px solid #ddd;text-align:right;"><strong>R$ {valor_total:,.2f}</strong></td>
                        <td style="padding:10px;border:1px solid #ddd;"></td>
                    </tr>
                </tbody>
            </table>

            {anexos_html}

            <div class="footer">
                <p>Documento gerado em {agora_brasil().strftime('%d/%m/%Y %H:%M:%S')}</p>
            </div>

            <div class="no-print" style="text-align:center;margin-top:20px;">
                <button onclick="window.print()" style="background:#1e40af;color:white;border:none;padding:12px 30px;border-radius:6px;font-size:16px;cursor:pointer;">
                    \U0001f5a8\ufe0f Imprimir
                </button>
            </div>
        </body>
        </html>
        """

        st.components.v1.html(html_impressao, height=800, scrolling=True)

        # Botao para baixar HTML
        st.download_button(
            "\U0001f4e5 Baixar HTML para Impressao",
            data=html_impressao,
            file_name=f"orcamento_{orc_id}.html",
            mime="text/html",
        )

        if st.button("\U0001f519 Voltar para Orcamentos"):
            st.session_state["imprimir_orcamento_id"] = None
            st.session_state["pagina_atual"] = "Orcamentos"
            st.rerun()

    finally:
        session.close()


# ============================================================
# PAGINA: CADASTROS
# ============================================================
def pagina_cadastros():
    st.title("\U0001f4dd Cadastros")

    tab_clientes, tab_materiais, tab_grupos = st.tabs(["\U0001f3e2 Clientes", "\U0001f4e6 Materiais", "\U0001f465 Grupos de Cliente"])

    # --- TAB: CLIENTES ---
    with tab_clientes:
        st.subheader("Clientes")

        # Adicionar novo cliente
        col_nc1, col_nc2 = st.columns([3, 1])
        with col_nc1:
            novo_cliente_nome = st.text_input("Novo Cliente", placeholder="Digite o nome do cliente", key="novo_cliente_nome")
        with col_nc2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("\U0001f4e6 Adicionar Cliente", key="btn_add_cliente"):
                if novo_cliente_nome.strip():
                    session = get_session()
                    try:
                        existe = session.query(Cliente).filter_by(nome=novo_cliente_nome.strip().upper()).first()
                        if existe:
                            st.warning("Cliente ja existe!")
                        else:
                            session.add(Cliente(nome=novo_cliente_nome.strip().upper(), ativo=True))
                            session.commit()
                            st.success(f"Cliente '{novo_cliente_nome.strip().upper()}' cadastrado!")
                            st.rerun()
                    except Exception as e:
                        session.rollback()
                        st.error(f"Erro: {e}")
                    finally:
                        session.close()
                else:
                    st.error("Digite um nome valido.")

        # Listar clientes
        filtro_ativo_c = st.selectbox("Filtro", ["Ativos", "Inativos", "Todos"], key="filtro_cliente_ativo")
        session = get_session()
        try:
            query_c = session.query(Cliente)
            if filtro_ativo_c == "Ativos":
                query_c = query_c.filter_by(ativo=True)
            elif filtro_ativo_c == "Inativos":
                query_c = query_c.filter_by(ativo=False)
            clientes = query_c.order_by(Cliente.nome).all()

            if clientes:
                for c in clientes:
                    status_icon = "\u2705" if c.ativo else "\u274c"
                    with st.expander(f"{status_icon} {c.nome}"):
                        col_c1, col_c2, col_c3 = st.columns(3)
                        with col_c1:
                            if c.ativo:
                                if st.button("\U0001f534 Desativar", key=f"desat_cliente_{c.id}"):
                                    c.ativo = False
                                    session.commit()
                                    st.success(f"Cliente '{c.nome}' desativado.")
                                    st.rerun()
                            else:
                                if st.button("\U0001f7e2 Reativar", key=f"reat_cliente_{c.id}"):
                                    c.ativo = True
                                    session.commit()
                                    st.success(f"Cliente '{c.nome}' reativado.")
                                    st.rerun()
                        with col_c2:
                            novo_nome_c = st.text_input("Novo Nome", value=c.nome, key=f"ren_cliente_{c.id}")
                            if st.button("\u270f\ufe0f Renomear", key=f"btn_ren_cliente_{c.id}"):
                                if novo_nome_c.strip() and novo_nome_c.strip().upper() != c.nome:
                                    # Verificar se o novo nome ja existe
                                    ja_existe = session.query(Cliente).filter_by(nome=novo_nome_c.strip().upper()).first()
                                    if ja_existe:
                                        st.warning("Ja existe um cliente com esse nome!")
                                    else:
                                        nome_antigo = c.nome
                                        c.nome = novo_nome_c.strip().upper()
                                        # Atualizar tambem nas compras existentes
                                        session.query(Compra).filter_by(cliente=nome_antigo).update({"cliente": c.nome})
                                        session.commit()
                                        st.success("Nome atualizado!")
                                        st.rerun()
                                elif not novo_nome_c.strip():
                                    st.error("Digite um nome valido.")
                        with col_c3:
                            if not c.ativo:
                                if st.button("\U0001f5d1 Excluir", key=f"excl_cliente_{c.id}"):
                                    # Verificar se tem compras vinculadas
                                    tem_compras = session.query(Compra).filter_by(cliente=c.nome).first()
                                    if tem_compras:
                                        st.warning("Cliente tem compras vinculadas. Nao e possivel excluir.")
                                    else:
                                        session.delete(c)
                                        session.commit()
                                        st.success("Cliente excluido!")
                                        st.rerun()
            else:
                st.info("Nenhum cliente cadastrado.")
        finally:
            session.close()

    # --- TAB: MATERIAIS ---
    with tab_materiais:
        st.subheader("Materiais")

        # Adicionar novo material
        with st.expander("\u2795 Novo Material", expanded=False):
            col_nm1, col_nm2, col_nm3 = st.columns(3)
            with col_nm1:
                novo_mat_nome = st.text_input("Nome do Material", key="novo_mat_nome")
            with col_nm2:
                novo_mat_tipo = st.selectbox("Tipo", ["material", "epi"], format_func=lambda x: "Material de Limpeza" if x == "material" else "EPI", key="novo_mat_tipo")
            with col_nm3:
                novo_mat_grupo = st.text_input("Grupo", placeholder="Ex: Detergentes e Desinfetantes", key="novo_mat_grupo")

            if st.button("\u2795 Adicionar Material", key="btn_add_material"):
                if novo_mat_nome.strip():
                    session = get_session()
                    try:
                        existe = session.query(Material).filter_by(nome=novo_mat_nome.strip().upper()).first()
                        if existe:
                            st.warning("Material ja existe!")
                        else:
                            session.add(Material(
                                nome=novo_mat_nome.strip().upper(),
                                tipo=novo_mat_tipo,
                                grupo=novo_mat_grupo.strip().upper() if novo_mat_grupo.strip() else "OUTROS",
                                ativo=True,
                            ))
                            session.commit()
                            st.success(f"Material '{novo_mat_nome.strip().upper()}' cadastrado!")
                            st.rerun()
                    except Exception as e:
                        session.rollback()
                        st.error(f"Erro: {e}")
                    finally:
                        session.close()
                else:
                    st.error("Digite um nome valido.")

        # Filtros
        col_fm1, col_fm2 = st.columns(2)
        with col_fm1:
            filtro_tipo_mat = st.selectbox("Tipo", ["Todos", "material", "epi"], format_func=lambda x: "Todos" if x == "Todos" else ("Material de Limpeza" if x == "material" else "EPI"), key="filtro_tipo_mat")
        with col_fm2:
            filtro_ativo_mat = st.selectbox("Status", ["Ativos", "Inativos", "Todos"], key="filtro_ativo_mat")

        session = get_session()
        try:
            query_m = session.query(Material)
            if filtro_tipo_mat != "Todos":
                query_m = query_m.filter_by(tipo=filtro_tipo_mat)
            if filtro_ativo_mat == "Ativos":
                query_m = query_m.filter_by(ativo=True)
            elif filtro_ativo_mat == "Inativos":
                query_m = query_m.filter_by(ativo=False)
            materiais = query_m.order_by(Material.grupo, Material.nome).all()

            if materiais:
                # Agrupar por grupo para exibicao
                grupos_dict = {}
                for m in materiais:
                    if m.grupo not in grupos_dict:
                        grupos_dict[m.grupo] = []
                    grupos_dict[m.grupo].append(m)

                for grupo, mats in grupos_dict.items():
                    st.markdown(f"**{grupo}**")
                    for m in mats:
                        status_icon = "\u2705" if m.ativo else "\u274c"
                        tipo_label = "Limpeza" if m.tipo == "material" else "EPI"
                        with st.expander(f"{status_icon} {m.nome} ({tipo_label})"):
                            # Linha 1: Imagem + acoes
                            col_img, col_m1, col_m2, col_m3, col_m4 = st.columns([2, 1, 1, 1, 1])

                            with col_img:
                                # Exibir imagem atual ou placeholder
                                if m.imagem:
                                    img_caminho = os.path.join(IMAGENS_DIR, m.imagem)
                                    if os.path.exists(img_caminho):
                                        st.image(img_caminho, width=120)
                                    else:
                                        st.caption("\U0001f4f7 Imagem nao encontrada")
                                else:
                                    st.caption("\U0001f4f7 Sem imagem")

                                # Upload de nova imagem
                                img_upload = st.file_uploader(
                                    "\U0001f4f7 Trocar imagem",
                                    type=["png", "jpg", "jpeg", "gif", "bmp", "webp"],
                                    key=f"img_mat_{m.id}",
                                    label_visibility="collapsed",
                                )
                                if img_upload:
                                    nome_arq = salvar_imagem_material(img_upload, m.nome)
                                    if nome_arq:
                                        # Remover imagem antiga se existir
                                        if m.imagem:
                                            antiga = os.path.join(IMAGENS_DIR, m.imagem)
                                            if os.path.exists(antiga):
                                                try:
                                                    os.remove(antiga)
                                                except Exception:
                                                    pass
                                        m.imagem = nome_arq
                                        session.commit()
                                        st.success("Imagem atualizada!")
                                        st.rerun()

                            with col_m1:
                                if m.ativo:
                                    if st.button("\U0001f534 Desativar", key=f"desat_mat_{m.id}"):
                                        m.ativo = False
                                        session.commit()
                                        st.success("Material desativado.")
                                        st.rerun()
                                else:
                                    if st.button("\U0001f7e2 Reativar", key=f"reat_mat_{m.id}"):
                                        m.ativo = True
                                        session.commit()
                                        st.success("Material reativado.")
                                        st.rerun()
                            with col_m2:
                                novo_nome_m = st.text_input("Novo Nome", value=m.nome, key=f"edit_nome_mat_{m.id}")
                                if st.button("\u270f\ufe0f Renomear", key=f"btn_ren_mat_{m.id}"):
                                    if novo_nome_m.strip() and novo_nome_m.strip().upper() != m.nome:
                                        ja_existe = session.query(Material).filter_by(nome=novo_nome_m.strip().upper()).first()
                                        if ja_existe:
                                            st.warning("Ja existe um material com esse nome!")
                                        else:
                                            nome_antigo = m.nome
                                            m.nome = novo_nome_m.strip().upper()
                                            # Atualizar tambem nas compras existentes
                                            session.query(Compra).filter_by(material=nome_antigo).update({"material": m.nome})
                                            session.commit()
                                            st.success("Nome do material atualizado!")
                                            st.rerun()
                                    elif not novo_nome_m.strip():
                                        st.error("Digite um nome valido.")
                            with col_m3:
                                novo_grupo_m = st.text_input("Novo Grupo", value=m.grupo or "", key=f"edit_grupo_mat_{m.id}")
                                if st.button("\U0001f4cb Alterar Grupo", key=f"btn_alt_grupo_{m.id}"):
                                    m.grupo = novo_grupo_m.strip().upper() if novo_grupo_m.strip() else "OUTROS"
                                    session.commit()
                                    st.success("Grupo atualizado!")
                                    st.rerun()
                            with col_m4:
                                opcoes_tipo = ["material", "epi"]
                                tipo_atual_idx = opcoes_tipo.index(m.tipo) if m.tipo in opcoes_tipo else 0
                                novo_tipo_m = st.selectbox(
                                    "Tipo",
                                    opcoes_tipo,
                                    index=tipo_atual_idx,
                                    format_func=lambda x: "Material de Limpeza" if x == "material" else "EPI",
                                    key=f"edit_tipo_mat_{m.id}"
                                )
                                if st.button("\U0001f527 Alterar Tipo", key=f"btn_alt_tipo_{m.id}"):
                                    if novo_tipo_m != m.tipo:
                                        m.tipo = novo_tipo_m
                                        session.commit()
                                        novo_label = "Material de Limpeza" if novo_tipo_m == "material" else "EPI"
                                        st.success(f"Tipo alterado para {novo_label}!")
                                        st.rerun()
                                    else:
                                        st.info("Tipo ja e o selecionado.")
                                if not m.ativo:
                                    if st.button("\U0001f5d1 Excluir", key=f"excl_mat_{m.id}"):
                                        tem_compras = session.query(Compra).filter_by(material=m.nome).first()
                                        if tem_compras:
                                            st.warning("Material tem compras vinculadas. Nao e possivel excluir.")
                                        else:
                                            # Remover imagem se existir
                                            if m.imagem:
                                                img_path_del = os.path.join(IMAGENS_DIR, m.imagem)
                                                if os.path.exists(img_path_del):
                                                    try:
                                                        os.remove(img_path_del)
                                                    except Exception:
                                                        pass
                                            session.delete(m)
                                            session.commit()
                                            st.success("Material excluido!")
                                            st.rerun()
            else:
                st.info("Nenhum material encontrado.")
        finally:
            session.close()

    # --- TAB: GRUPOS DE CLIENTE ---
    with tab_grupos:
        st.subheader("Grupos de Cliente")

        # Adicionar novo grupo
        col_ng1, col_ng2 = st.columns([3, 1])
        with col_ng1:
            novo_grupo_nome = st.text_input("Novo Grupo", key="novo_grupo_nome")
        with col_ng2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("\u2795 Adicionar Grupo", key="btn_add_grupo"):
                if novo_grupo_nome.strip():
                    session = get_session()
                    try:
                        existe = session.query(GrupoCliente).filter_by(nome=novo_grupo_nome.strip().upper()).first()
                        if existe:
                            st.warning("Grupo ja existe!")
                        else:
                            session.add(GrupoCliente(nome=novo_grupo_nome.strip().upper()))
                            session.commit()
                            st.success(f"Grupo '{novo_grupo_nome.strip().upper()}' cadastrado!")
                            st.rerun()
                    except Exception as e:
                        session.rollback()
                        st.error(f"Erro: {e}")
                    finally:
                        session.close()
                else:
                    st.error("Digite um nome valido.")

        # Listar grupos
        session = get_session()
        try:
            grupos = session.query(GrupoCliente).order_by(GrupoCliente.nome).all()
            if grupos:
                for g in grupos:
                    with st.expander(f"\U0001f465 {g.nome}"):
                        col_g1, col_g2 = st.columns(2)
                        with col_g1:
                            novo_nome_g = st.text_input("Novo Nome", value=g.nome, key=f"ren_grupo_{g.id}")
                            if st.button(f"\u270f\ufe0f Renomear", key=f"btn_ren_grupo_{g.id}"):
                                if novo_nome_g.strip() and novo_nome_g.strip().upper() != g.nome:
                                    g.nome = novo_nome_g.strip().upper()
                                    session.commit()
                                    st.success("Nome atualizado!")
                                    st.rerun()
                        with col_g2:
                            if st.button(f"\U0001f5d1\ufe0f Excluir", key=f"exc_grupo_{g.id}"):
                                session.delete(g)
                                session.commit()
                                st.success("Grupo excluido!")
                                st.rerun()
            else:
                st.info("Nenhum grupo cadastrado.")
        finally:
            session.close()


# ============================================================
# PAGINA: EDITAR ITEM INDIVIDUAL
# ============================================================
def pagina_editar_item():
    st.title("\u270f\ufe0f Editar Item")

    # Selecionar item por ID
    item_id = st.number_input("ID do Item", min_value=1, step=1, key="editar_item_id_input")

    if st.button("\U0001f50d Buscar Item"):
        session = get_session()
        try:
            item = session.query(Compra).get(item_id)
            if item:
                st.session_state["editar_item_id"] = item_id
                st.session_state["editar_item_data"] = {
                    "cliente": item.cliente,
                    "material": item.material,
                    "quantidade": item.quantidade,
                    "valor_unitario": item.valor_unitario,
                    "situacao": item.situacao,
                    "mes": item.mes,
                    "ano": item.ano,
                    "observacao": item.observacao or "",
                }
            else:
                st.error("Item nao encontrado.")
        finally:
            session.close()

    if "editar_item_data" in st.session_state and st.session_state.get("editar_item_id"):
        data = st.session_state["editar_item_data"]
        item_id = st.session_state["editar_item_id"]

        st.markdown(f"**Item ID:** {item_id}")
        st.markdown("---")

        # Formulario de edicao
        clientes_nomes = [c.nome for c in obter_clientes_ativos()]

        col1, col2 = st.columns(2)
        with col1:
            cliente_idx = clientes_nomes.index(data["cliente"]) if data["cliente"] in clientes_nomes else 0
            novo_cliente = st.selectbox("Cliente", clientes_nomes, index=cliente_idx, key="edit_item_cliente")
            nova_qtd = st.number_input("Quantidade", value=int(data["quantidade"]), min_value=1, step=1, key="edit_item_qtd")
            nova_sit = st.selectbox("Situacao", SITUACOES, index=SITUACOES.index(data["situacao"]) if data["situacao"] in SITUACOES else 0, key="edit_item_sit")
        with col2:
            st.text_input("Material", value=data["material"], disabled=True, key="edit_item_mat")
            novo_val_unit = st.number_input("Valor Unitario (R$)", value=data["valor_unitario"], min_value=0.0, step=0.01, format="%0.2f", key="edit_item_val")
            novo_val_total = round(nova_qtd * novo_val_unit, 2)
            st.text(f"Valor Total: {formatar_moeda(novo_val_total)}")

        col_mes, col_ano = st.columns(2)
        with col_mes:
            mes_idx = list(MESES.keys()).index(data["mes"]) if data["mes"] in MESES else 0
            novo_mes = st.selectbox("Mes", list(MESES.keys()), format_func=lambda x: MESES[x], index=mes_idx, key="edit_item_mes")
        with col_ano:
            ano_idx = ANOS.index(data["ano"]) if data["ano"] in ANOS else 0
            novo_ano = st.selectbox("Ano", ANOS, index=ano_idx, key="edit_item_ano")

        nova_obs = st.text_area("Observacao", value=data["observacao"], key="edit_item_obs")

        # Upload
        col_up1, col_up2 = st.columns(2)
        with col_up1:
            arq_orc = st.file_uploader("Arquivo Orcamento", type=["pdf", "png", "jpg", "jpeg", "doc", "docx", "xls", "xlsx"], key="edit_item_arq_orc")
        with col_up2:
            arq_comp = st.file_uploader("Comprovante", type=["pdf", "png", "jpg", "jpeg", "doc", "docx", "xls", "xlsx"], key="edit_item_arq_comp")

        st.markdown("---")
        col_save, col_cancel = st.columns(2)
        with col_save:
            if st.button("\U0001f4be Salvar", type="primary", key="save_edit_item"):
                session = get_session()
                try:
                    item = session.query(Compra).get(item_id)
                    if item:
                        item.cliente = novo_cliente
                        item.quantidade = nova_qtd
                        item.valor_unitario = novo_val_unit
                        item.valor_total = novo_val_total
                        item.situacao = nova_sit
                        item.mes = novo_mes
                        item.ano = novo_ano
                        item.observacao = nova_obs
                        item.data_atualizacao = agora_brasil()

                        if arq_orc:
                            item.arquivo_orcamento = salvar_arquivo(arq_orc, "orc")
                        if arq_comp:
                            item.arquivo_comprovante = salvar_arquivo(arq_comp, "comp")

                        session.commit()
                        st.success("\u2705 Item atualizado com sucesso!")
                        del st.session_state["editar_item_data"]
                        del st.session_state["editar_item_id"]
                    else:
                        st.error("Item nao encontrado.")
                except Exception as e:
                    session.rollback()
                    st.error(f"Erro: {e}")
                finally:
                    session.close()

        with col_cancel:
            if st.button("\u274c Cancelar", key="cancel_edit_item"):
                del st.session_state["editar_item_data"]
                del st.session_state["editar_item_id"]
                st.rerun()


# ============================================================
# NAVEGACAO PRINCIPAL
# ============================================================
def _on_nav_change():
    """Callback quando o radio de navegacao muda."""
    st.session_state["pagina_atual"] = st.session_state["nav_radio"]


def main():
    # Pagina padrao
    if "pagina_atual" not in st.session_state:
        st.session_state["pagina_atual"] = "Dashboard"

    PAGINAS_NAV = ["Dashboard", "Orcamentos", "Novo Orcamento", "Editar Orcamento", "Editar Item", "Imprimir", "Cadastros"]

    with st.sidebar:
        st.markdown("## \U0001f6d2 Sistema de Compras")
        st.markdown("---")

        # Sincroniza o radio com pagina_atual via on_change
        # O index e calculado a partir de pagina_atual para que o radio
        # reflita navegacoes vindas de botoes (Editar, Imprimir, etc.)
        idx = PAGINAS_NAV.index(st.session_state["pagina_atual"]) if st.session_state["pagina_atual"] in PAGINAS_NAV else 0
        st.radio(
            "Navegacao",
            PAGINAS_NAV,
            index=idx,
            key="nav_radio",
            on_change=_on_nav_change,
        )

        st.markdown("---")
        # Info do banco para debug
        db_path = os.path.join(BASE_DIR, "database.db")
        db_exists = os.path.exists(db_path)
        db_size = os.path.getsize(db_path) / 1024 if db_exists else 0
        st.markdown(f"""
        <div style='color: rgba(255,255,255,0.6); font-size: 0.8em;'>
            Sistema de Controle de Compras<br>
            Versao Streamlit 2.0<br>
            Banco: {'✅ ' + str(int(db_size)) + ' KB' if db_exists else '❌ Nao encontrado'}<br>
            Pasta: {BASE_DIR}
        </div>
        """, unsafe_allow_html=True)

    # Roteamento
    pagina = st.session_state["pagina_atual"]
    if pagina == "Dashboard":
        pagina_dashboard()
    elif pagina == "Orcamentos":
        pagina_orcamentos()
    elif pagina == "Novo Orcamento":
        pagina_novo_orcamento()
    elif pagina == "Editar Orcamento":
        pagina_editar_orcamento()
    elif pagina == "Editar Item":
        pagina_editar_item()
    elif pagina == "Imprimir":
        pagina_imprimir_orcamento()
    elif pagina == "Cadastros":
        pagina_cadastros()


if __name__ == "__main__":
    main()
'''






# ============================================================
# FUNCOES DO INSTALADOR
# ============================================================

def escrever_arquivos():
    """Escreve todos os arquivos do sistema na pasta."""
    print("\n" + "=" * 60)
    print("  Criando arquivos do sistema...")
    print("=" * 60)

    arquivos = {
        "models.py": ARQ_MODELS_PY,
        "database.py": ARQ_DATABASE_PY,
        "seed.py": ARQ_SEED_PY,
        "app.py": ARQ_APP_PY,
        "requirements.txt": "streamlit\nsqlalchemy\n",
    }

    for nome, conteudo in arquivos.items():
        caminho = os.path.join(PASTA_SISTEMA, nome)
        with open(caminho, "w", encoding="utf-8") as f:
            f.write(conteudo)
        print(f"  \u2705 {nome} criado")

    return True


def instalar_pacotes():
    """Instala os pacotes Python necessarios."""
    pacotes = [
        "streamlit",
        "sqlalchemy",
    ]

    print("\n" + "=" * 60)
    print("  Instalando pacotes necessarios...")
    print("=" * 60)

    for pacote in pacotes:
        print(f"\n  Instalando {pacote}...")
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", pacote],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            print(f"  \u2705 {pacote} instalado com sucesso!")
        except subprocess.CalledProcessError:
            print(f"  \u26a0\ufe0f Tentando novamente com saida visivel...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", pacote])
                print(f"  \u2705 {pacote} instalado com sucesso!")
            except subprocess.CalledProcessError:
                print(f"  \u274c Erro ao instalar {pacote}. Tente manualmente:")
                print(f"     pip install {pacote}")
                return False

    return True



def gerar_imagens_materiais():
    """Decodifica imagens base64 e salva como PNGs na pasta imagens/."""
    import base64 as _b64
    import os as _os

    pasta_imagens = _os.path.join(PASTA_SISTEMA, "imagens")
    if not _os.path.exists(pasta_imagens):
        _os.makedirs(pasta_imagens)

    print("  Gerando imagens dos materiais...")
    geradas = 0
    for nome, dados_b64 in IMAGENS_BASE64.items():
        caminho = _os.path.join(pasta_imagens, f"{nome}.png")
        if not _os.path.exists(caminho):
            try:
                img_bytes = _b64.b64decode(dados_b64)
                with open(caminho, "wb") as f:
                    f.write(img_bytes)
                geradas += 1
            except Exception as e:
                print(f"    Aviso: nao foi possivel criar {nome}.png: {e}")
    if geradas > 0:
        print(f"  {geradas} imagens de materiais geradas com sucesso!")
    else:
        print("  Todas as imagens ja existem. Nenhuma gerada.")

def criar_estrutura():
    """Cria as pastas necessarias."""
    print("\n" + "=" * 60)
    print("  Criando estrutura de pastas...")
    print("=" * 60)

    pasta_uploads = os.path.join(PASTA_SISTEMA, "uploads")
    if not os.path.exists(pasta_uploads):
        os.makedirs(pasta_uploads)
        print(f"  \u2705 Pasta 'uploads' criada")
    else:
        print(f"  \u2705 Pasta 'uploads' ja existe")

    pasta_imagens = os.path.join(PASTA_SISTEMA, "imagens")
    if not os.path.exists(pasta_imagens):
        os.makedirs(pasta_imagens)
        print(f"  \u2705 Pasta 'imagens' criada")
    else:
        print(f"  \u2705 Pasta 'imagens' ja existe")

    return True


def criar_banco():
    """Cria o banco de dados e popula com dados iniciais."""
    print("\n" + "=" * 60)
    print("  Configurando banco de dados...")
    print("=" * 60)

    db_path = os.path.join(PASTA_SISTEMA, "database.db")

    if os.path.exists(db_path):
        print("  \u26a0\ufe0f Banco de dados ja existe.")
        print("  Se voce quer resetar completamente, delete o arquivo database.db")
        print("  e execute este instalador novamente.")
        print("  Os pedidos ja cadastrados serao mantidos se o banco nao for deletado.")
        print("  Os novos clientes/materiais serao adicionados automaticamente (sem duplicar).")

        # PASSO 1: Migracao - adicionar coluna imagem se nao existir
        try:
            import sqlite3 as _sq3
            _conn = _sq3.connect(db_path)
            _cur = _conn.cursor()
            # Verificar se a coluna imagem existe
            _cur.execute("PRAGMA table_info(materiais)")
            _colunas = [col[1] for col in _cur.fetchall()]
            if 'imagem' not in _colunas:
                print("  Adicionando coluna imagem ao banco existente...")
                _cur.execute("ALTER TABLE materiais ADD COLUMN imagem VARCHAR(500)")
                _conn.commit()
                print("  \u2705 Coluna imagem adicionada com sucesso!")
            _conn.close()
        except Exception as e:
            print(f"  \u26a0\ufe0f Nao foi possivel migrar o banco: {e}")

        # PASSO 2: Atualizar imagens de materiais existentes que estao sem imagem
        try:
            import sqlite3 as _sq3
            _conn = _sq3.connect(db_path)
            _cur = _conn.cursor()
            _cur.execute("SELECT nome FROM materiais WHERE imagem IS NULL OR imagem = ''")
            _sem_img = [r[0] for r in _cur.fetchall()]
            _atualizados = 0
            for _nome in _sem_img:
                _img = _IMAGEM_SUBGRUPO.get(_nome)
                if _img:
                    _cur.execute("UPDATE materiais SET imagem = ? WHERE nome = ?", (_img, _nome))
                    _atualizados += 1
            if _atualizados > 0:
                _conn.commit()
                print(f"  \u2705 {_atualizados} materiais existentes receberam imagem.")
            _conn.close()
        except Exception as e:
            print(f"  \u26a0\ufe0f Nao foi possivel atualizar imagens de materiais existentes: {e}")

        # PASSO 3: Verificar e adicionar novos dados
        try:
            sys.path.insert(0, PASTA_SISTEMA)
            from seed import popular_dados
            print("  Verificando novos dados...")
            popular_dados()
            print("  \u2705 Novos clientes/materiais adicionados (sem duplicar existentes).")
        except Exception as e:
            print(f"  \u26a0\ufe0f Nao foi possivel verificar novos dados: {e}")

        # PASSO 4: Gerar arquivos de imagem
        gerar_imagens_materiais()
        return True

    try:
        # Adicionar a pasta do sistema ao path
        sys.path.insert(0, PASTA_SISTEMA)

        from database import init_db
        from seed import popular_dados

        print("  Criando tabelas...")
        init_db()
        print("  \u2705 Tabelas criadas com sucesso!")

        print("  Populando dados iniciais...")
        popular_dados()
        print("  \u2705 Dados iniciais inseridos com sucesso!")

        gerar_imagens_materiais()

    except Exception as e:
        print(f"  \u274c Erro ao configurar banco: {e}")
        return False

    return True

def iniciar_sistema():
    """Inicia o sistema Streamlit."""
    print("\n" + "=" * 60)
    print("  Iniciando o Sistema de Controle de Compras...")
    print("=" * 60)
    print()
    print("  O sistema vai abrir no seu navegador automaticamente.")
    print("  Para parar o sistema, feche esta janela ou pressione Ctrl+C.")
    print()
    print("=" * 60)

    app_path = os.path.join(PASTA_SISTEMA, "app.py")

    try:
        subprocess.run(
            [sys.executable, "-m", "streamlit", "run", app_path, "--server.headless=true"],
            cwd=PASTA_SISTEMA,
        )
    except KeyboardInterrupt:
        print("\n  Sistema encerrado pelo usuario.")
    except Exception as e:
        print(f"\n  \u274c Erro ao iniciar sistema: {e}")
        print("  Tente iniciar manualmente com:")
        print(f"     cd '{PASTA_SISTEMA}'")
        print("     streamlit run app.py")


def main():
    print()
    print("\u2554" + "\u2550" * 58 + "\u2557")
    print("\u2551     SISTEMA DE CONTROLE DE COMPRAS - INSTALADOR          \u2551")
    print("\u2551     Versao Streamlit                                     \u2551")
    print("\u255a" + "\u2550" * 58 + "\u255d")
    print()

    # Passo 1: Escrever arquivos do sistema
    if not escrever_arquivos():
        print("\n  \u26a0\ufe0f Falha ao criar arquivos do sistema.")
        input("  Pressione Enter para sair...")
        return

    # Passo 2: Instalar pacotes
    if not instalar_pacotes():
        print("\n  \u26a0\ufe0f Instalacao de pacotes falhou. Verifique os erros acima.")
        input("  Pressione Enter para sair...")
        return

    # Passo 3: Criar estrutura
    if not criar_estrutura():
        print("\n  \u26a0\ufe0f Falha ao criar estrutura de pastas.")
        input("  Pressione Enter para sair...")
        return

    # Passo 4: Criar banco
    if not criar_banco():
        print("\n  \u26a0\ufe0f Falha ao configurar banco de dados.")
        input("  Pressione Enter para sair...")
        return

    # Passo 5: Iniciar
    print("\n  \u2705 Tudo pronto! Iniciando o sistema...\n")
    iniciar_sistema()


if __name__ == "__main__":
    main()
