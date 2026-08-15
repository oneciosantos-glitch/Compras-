from database import get_session, init_db
from models import Cliente, Material, GrupoCliente


def popular_dados():
    session = get_session()
    try:
        # --- GRUPOS DE CLIENTE ---
        grupos = [
            "SMART FIT",
            "SELF FIT",
            "ASSAI/ATACADAO/NOVO ATACAREJO",
            "GRUPO MATEUS",
            "OUTROS",
        ]
        for nome in grupos:
            existe = session.query(GrupoCliente).filter_by(nome=nome).first()
            if not existe:
                session.add(GrupoCliente(nome=nome))
        session.commit()

        # --- CLIENTES ---
        clientes_lista = [
            # SMART FIT
            "SMART FIT - MATRIZ",
            "SMART FIT - FILIAL 01",
            "SMART FIT - FILIAL 02",
            "SMART FIT - FILIAL 03",
            "SMART FIT - FILIAL 04",
            "SMART FIT - FILIAL 05",
            "SMART FIT - FILIAL 06",
            "SMART FIT - FILIAL 07",
            "SMART FIT - FILIAL 08",
            "SMART FIT - FILIAL 09",
            "SMART FIT - FILIAL 10",
            "SMART FIT - FILIAL 11",
            "SMART FIT - FILIAL 12",
            "SMART FIT - FILIAL 13",
            "SMART FIT - FILIAL 14",
            "SMART FIT - FILIAL 15",
            "SMART FIT - FILIAL 16",
            "SMART FIT - FILIAL 17",
            "SMART FIT - FILIAL 18",
            "SMART FIT - FILIAL 19",
            "SMART FIT - FILIAL 20",
            "SMART FIT - FILIAL 21",
            "SMART FIT - FILIAL 22",
            "SMART FIT - FILIAL 23",
            "SMART FIT - FILIAL 24",
            # SELF FIT
            "SELF FIT - MATRIZ",
            "SELF FIT - FILIAL 01",
            "SELF FIT - FILIAL 02",
            "SELF FIT - FILIAL 03",
            "SELF FIT - FILIAL 04",
            "SELF FIT - FILIAL 05",
            "SELF FIT - FILIAL 06",
            "SELF FIT - FILIAL 07",
            "SELF FIT - FILIAL 08",
            "SELF FIT - FILIAL 09",
            "SELF FIT - FILIAL 10",
            "SELF FIT - FILIAL 11",
            "SELF FIT - FILIAL 12",
            "SELF FIT - FILIAL 13",
            "SELF FIT - FILIAL 14",
            "SELF FIT - FILIAL 15",
            "SELF FIT - FILIAL 16",
            "SELF FIT - FILIAL 17",
            "SELF FIT - FILIAL 18",
            "SELF FIT - FILIAL 19",
            "SELF FIT - FILIAL 20",
            "SELF FIT - FILIAL 21",
            "SELF FIT - FILIAL 22",
            "SELF FIT - FILIAL 23",
            "SELF FIT - FILIAL 24",
            # ASSAI / ATACADAO / NOVO ATACAREJO
            "ASSAI - MATRIZ",
            "ASSAI - FILIAL 01",
            "ASSAI - FILIAL 02",
            "ASSAI - FILIAL 03",
            "ASSAI - FILIAL 04",
            "ASSAI - FILIAL 05",
            "ASSAI - FILIAL 06",
            "ASSAI - FILIAL 07",
            "ASSAI - FILIAL 08",
            "ASSAI - FILIAL 09",
            "ASSAI - FILIAL 10",
            "ATACADAO - MATRIZ",
            "ATACADAO - FILIAL 01",
            "ATACADAO - FILIAL 02",
            "ATACADAO - FILIAL 03",
            "ATACADAO - FILIAL 04",
            "ATACADAO - FILIAL 05",
            "ATACADAO - FILIAL 06",
            "ATACADAO - FILIAL 07",
            "ATACADAO - FILIAL 08",
            "ATACADAO - FILIAL 09",
            "ATACADAO - FILIAL 10",
            "NOVO ATACAREJO - MATRIZ",
            "NOVO ATACAREJO - FILIAL 01",
            "NOVO ATACAREJO - FILIAL 02",
            "NOVO ATACAREJO - FILIAL 03",
            "NOVO ATACAREJO - FILIAL 04",
            "NOVO ATACAREJO - FILIAL 05",
            "NOVO ATACAREJO - FILIAL 06",
            "NOVO ATACAREJO - FILIAL 07",
            "NOVO ATACAREJO - FILIAL 08",
            "NOVO ATACAREJO - FILIAL 09",
            "NOVO ATACAREJO - FILIAL 10",
            # GRUPO MATEUS
            "MATEUS - MATRIZ",
            "MATEUS - FILIAL 01",
            "MATEUS - FILIAL 02",
            "MATEUS - FILIAL 03",
            "MATEUS - FILIAL 04",
            "MATEUS - FILIAL 05",
            "MATEUS - FILIAL 06",
            "MATEUS - FILIAL 07",
            "MATEUS - FILIAL 08",
            "MATEUS - FILIAL 09",
            "MATEUS - FILIAL 10",
            "MATEUS SUPERMERCADO - FILIAL 01",
            "MATEUS SUPERMERCADO - FILIAL 02",
            "MATEUS SUPERMERCADO - FILIAL 03",
            "MATEUS SUPERMERCADO - FILIAL 04",
            "MATEUS SUPERMERCADO - FILIAL 05",
            "MATEUS ATACADO - FILIAL 01",
            "MATEUS ATACADO - FILIAL 02",
            "MATEUS ATACADO - FILIAL 03",
            "MATEUS ATACADO - FILIAL 04",
            "MATEUS ATACADO - FILIAL 05",
            # OUTROS
            "CLIENTE AVULSO",
            "DISTRIBUIDORA CENTRAL",
            "FORNECEDOR EXTERNO",
            "POSTO DE COMBUSTIVEL XYZ",
            "HOTEL PARAISO",
            "RESTAURANTE SABOR DA TERRA",
            "CLINICA SAUDE VIDA",
            "ESCOLA FUTURO BRILHANTE",
            "CONDOMINIO RESIDENCIAL PARK",
            "EMPRESA DE LIMPEZA TOTAL",
            "INDUSTRIA ALIMENTOS NATURAIS",
            "SUPERMERCADO BOM PRECO",
            "PADARIA NOSSO PAO",
        ]
        for nome in clientes_lista:
            existe = session.query(Cliente).filter_by(nome=nome).first()
            if not existe:
                session.add(Cliente(nome=nome, ativo=True))
        session.commit()

        # --- MATERIAIS DE LIMPEZA ---
        materiais_limpeza = [
            # Detergentes e Desinfetantes
            ("DETERGENTE LIQUIDO NEUTRO 5L", "Detergentes e Desinfetantes"),
            ("DETERGENTE LIQUIDO NEUTRO 500ML", "Detergentes e Desinfetantes"),
            ("DETERGENTE EM PO 1KG", "Detergentes e Desinfetantes"),
            ("DESINFETANTE LAVANDA 5L", "Detergentes e Desinfetantes"),
            ("DESINFETANTE FLORAL 2L", "Detergentes e Desinfetantes"),
            ("DESINFETANTE CONCENTRADO 1L", "Detergentes e Desinfetantes"),
            ("SABAO LIQUIDO PARA PISO 5L", "Detergentes e Desinfetantes"),
            # Água Sanitária e Alvejantes
            ("AGUA SANITARIA 5L", "Agua Sanitaria e Alvejantes"),
            ("AGUA SANITARIA 2L", "Agua Sanitaria e Alvejantes"),
            ("AGUA SANITARIA 1L", "Agua Sanitaria e Alvejantes"),
            ("ALVEJANTE COM CLORETOS 5L", "Agua Sanitaria e Alvejantes"),
            ("ALVEJANTE OXIGENADO 2L", "Agua Sanitaria e Alvejantes"),
            # Sabões e Sabonetes
            ("SABAO EM PO 1KG", "Saboes e Sabonetes"),
            ("SABAO EM PO 5KG", "Saboes e Sabonetes"),
            ("SABAO EM BARRA 200G", "Saboes e Sabonetes"),
            ("SABONETE LIQUIDO 500ML", "Saboes e Sabonetes"),
            ("SABONETE EM BARRA 90G", "Saboes e Sabonetes"),
            # Limpadores Multiuso
            ("LIMPADOR MULTIUSO 500ML", "Limpadores Multiuso"),
            ("LIMPADOR MULTIUSO 5L", "Limpadores Multiuso"),
            ("LIMPADOR DE PISO 5L", "Limpadores Multiuso"),
            ("LIMPADOR DE VIDROS 500ML", "Limpadores Multiuso"),
            ("LIMPADOR DE COZINHA 500ML", "Limpadores Multiuso"),
            ("LIMPADOR DE BANHEIRO 500ML", "Limpadores Multiuso"),
            ("LIMPADOR DESENGORDURANTE 5L", "Limpadores Multiuso"),
            ("LUSTRA MOVEIS 500ML", "Limpadores Multiuso"),
            # Esponjas e Buchas
            ("ESPONJA DUPLA FACE PACOTE C/ 3", "Esponjas e Buchas"),
            ("ESPONJA DE ACO PACOTE C/ 6", "Esponjas e Buchas"),
            ("BUCHA VEGETAL UNIDADE", "Esponjas e Buchas"),
            ("BUCHA DE ACO 8 UNIDADES", "Esponjas e Buchas"),
            # Panos e Flanelas
            ("PANO DE CHAO ALGODAO 50X50CM", "Panos e Flanelas"),
            ("PANO DE CHAO TNT 50X50CM", "Panos e Flanelas"),
            ("PANO DE PRATO ALGODAO 40X40CM", "Panos e Flanelas"),
            ("FLANELA PARA PISO 50X70CM", "Panos e Flanelas"),
            ("RODO COM CABO 60CM", "Panos e Flanelas"),
            # Vassouras e Rodos
            ("VASSOURA DE PIA C/ CABO", "Vassouras e Rodos"),
            ("VASSOURA DE CHAO C/ CABO", "Vassouras e Rodos"),
            ("VASSOURA DE COCO C/ CABO", "Vassouras e Rodos"),
            ("RODO DE PISO COM CABO 60CM", "Vassouras e Rodos"),
            ("RODO DE PISO COM CABO 90CM", "Vassouras e Rodos"),
            ("CABO PARA VASSOURA E RODO", "Vassouras e Rodos"),
            ("PÁ DE LIXO PLÁSTICA", "Vassouras e Rodos"),
            # Sacos de Lixo
            ("SACO DE LIXO 30X40 PRETO 50UN", "Sacos de Lixo"),
            ("SACO DE LIXO 50X70 PRETO 25UN", "Sacos de Lixo"),
            ("SACO DE LIXO 60X90 PRETO 15UN", "Sacos de Lixo"),
            ("SACO DE LIXO 70X110 PRETO 10UN", "Sacos de Lixo"),
            ("SACO DE LIXO 30X40 BRANCO 50UN", "Sacos de Lixo"),
            ("SACO DE LIXO 50X70 BRANCO 25UN", "Sacos de Lixo"),
            # Ceras e Enceradeiras
            ("CERA LIQUIDA PARA PISO 5L", "Ceras e Enceradeiras"),
            ("CERA EM PASTA 1KG", "Ceras e Enceradeiras"),
            ("LUSTRA PISO 5L", "Ceras e Enceradeiras"),
            # Desodorizadores
            ("DESODORIZADOR DE AMBIENTE 500ML", "Desodorizadores"),
            ("DESODORIZADOR DE AMBIENTE 2L", "Desodorizadores"),
            ("DESODORIZADOR BANHEIRO 300ML", "Desodorizadores"),
            ("BLOCO DESODORIZADOR VASO SANITARIO", "Desodorizadores"),
            # Outros Produtos de Limpeza
            ("AMACIANTE DE ROUPAS 5L", "Outros Produtos de Limpeza"),
            ("AMACIANTE DE ROUPAS 2L", "Outros Produtos de Limpeza"),
            ("REMOVEDOR DE MANCHAS 500ML", "Outros Produtos de Limpeza"),
            ("REMOVEDOR DE OLEOS 5L", "Outros Produtos de Limpeza"),
            ("LIMPADOR DE ALUMINIO 500ML", "Outros Produtos de Limpeza"),
            ("LIMPADOR DE INOX 500ML", "Outros Produtos de Limpeza"),
            ("ESCORREDOR DE LOUCA", "Outros Produtos de Limpeza"),
            ("BALDE PLASTICO 10L", "Outros Produtos de Limpeza"),
            ("BALDE PLASTICO 20L", "Outros Produtos de Limpeza"),
            ("BACIA PLASTICA 10L", "Outros Produtos de Limpeza"),
            ("ESCOVA DE CHAO COM CABO", "Outros Produtos de Limpeza"),
            ("ESCOVA DE PIA UNIDADE", "Outros Produtos de Limpeza"),
            ("ESPATIFOR 500ML", "Outros Produtos de Limpeza"),
        ]

        # --- EPIs ---
        materiais_epi = [
            # Luvas
            ("LUVAS DE PROCEDIMENTO M 100UN", "Luvas"),
            ("LUVAS DE PROCEDIMENTO G 100UN", "Luvas"),
            ("LUVAS DE PROCEDIMENTO P 100UN", "Luvas"),
            ("LUVAS DE LATEX M 50UN", "Luvas"),
            ("LUVAS DE LATEX G 50UN", "Luvas"),
            ("LUVAS DE BORRACHA M", "Luvas"),
            ("LUVAS DE BORRACHA G", "Luvas"),
            ("LUVAS DE VAQUETA M", "Luvas"),
            ("LUVAS DE VAQUETA G", "Luvas"),
            ("LUVAS ANTICORTE NIVEL 5 M", "Luvas"),
            ("LUVAS ANTICORTE NIVEL 5 G", "Luvas"),
            ("LUVAS TRICOTADAS COM PALMAS M", "Luvas"),
            ("LUVAS TRICOTADAS COM PALMAS G", "Luvas"),
            # Máscaras
            ("MASCARA PFF2 UNIDADE", "Mascaras"),
            ("MASCARA PFF2 CAIXA C/ 10", "Mascaras"),
            ("MASCARA CIRURGICA CAIXA C/ 50", "Mascaras"),
            ("MASCARA SEMI-FACIAL REUTILIZAVEL", "Mascaras"),
            ("FILTRO PARA MASCARA P2 PAR", "Mascaras"),
            ("FILTRO PARA MASCARA QUIMICO PAR", "Mascaras"),
            # Óculos de Proteção
            ("OCULOS DE PROTECAO TRANSPARENTE", "Oculos de Protecao"),
            ("OCULOS DE PROTECAO ESCURO", "Oculos de Protecao"),
            ("OCULOS DE PROTECAO AMBIDENTRO", "Oculos de Protecao"),
            # Capacetes e Proteção Cabeça
            ("CAPACETE DE SEGURANCA BRANCO", "Capacetes e Protecao Cabeca"),
            ("CAPACETE DE SEGURANCA AZUL", "Capacetes e Protecao Cabeca"),
            ("CAPACETE DE SEGURANCA VERMELHO", "Capacetes e Protecao Cabeca"),
            ("CAPUZ PARA CAPACETE", "Capacetes e Protecao Cabeca"),
            ("PROTETOR AURICULAR PLUG UNIDADE", "Capacetes e Protecao Cabeca"),
            ("PROTETOR AURICULAR PLUG CAIXA C/ 100", "Capacetes e Protecao Cabeca"),
            ("PROTETOR AURICULAR CONCHA", "Capacetes e Protecao Cabeca"),
            # Calçados de Proteção
            ("BOTA DE SEGURANCA COM BIQUEIRA ACO 39", "Calcados de Protecao"),
            ("BOTA DE SEGURANCA COM BIQUEIRA ACO 40", "Calcados de Protecao"),
            ("BOTA DE SEGURANCA COM BIQUEIRA ACO 41", "Calcados de Protecao"),
            ("BOTA DE SEGURANCA COM BIQUEIRA ACO 42", "Calcados de Protecao"),
            ("BOTA DE SEGURANCA COM BIQUEIRA ACO 43", "Calcados de Protecao"),
            ("BOTA DE SEGURANCA COM BIQUEIRA ACO 44", "Calcados de Protecao"),
            ("BOTA DE BORRACHA CANO ALTO 39", "Calcados de Protecao"),
            ("BOTA DE BORRACHA CANO ALTO 40", "Calcados de Protecao"),
            ("BOTA DE BORRACHA CANO ALTO 41", "Calcados de Protecao"),
            ("BOTA DE BORRACHA CANO ALTO 42", "Calcados de Protecao"),
            ("BOTA DE BORRACHA CANO ALTO 43", "Calcados de Protecao"),
            # Aventais e Macacões
            ("AVENTAL DE PVC 70CM", "Aventais e Macacoes"),
            ("AVENTAL DE LONA 70CM", "Aventais e Macacoes"),
            ("AVENTAL DESCARTAVEL 70CM PACOTE C/ 10", "Aventais e Macacoes"),
            ("MACACAO BRANCO M", "Aventais e Macacoes"),
            ("MACACAO BRANCO G", "Aventais e Macacoes"),
            ("MACACAO BRANCO GG", "Aventais e Macacoes"),
            ("MACACAO DESCARTAVEL M", "Aventais e Macacoes"),
            ("MACACAO DESCARTAVEL G", "Aventais e Macacoes"),
            ("MACACAO DESCARTAVEL GG", "Aventais e Macacoes"),
            # Cintos e Arnês
            ("CINTO DE SEGURANCA TIPO PARAQUEDISTA", "Cintos e Arnes"),
            ("TALABARTE SIMPLES", "Cintos e Arnes"),
            ("TALABARTE DUPLO", "Cintos e Arnes"),
            ("ARNES DE SEGURANCA COM CINTO", "Cintos e Arnes"),
            # Sinalização e Outros EPIs
            ("CONE DE SINALIZACAO 75CM", "Sinalizacao e Outros EPIs"),
            ("CONE DE SINALIZACAO 50CM", "Sinalizacao e Outros EPIs"),
            ("FITA ZEBRADA 50M", "Sinalizacao e Outros EPIs"),
            ("PLACA DE SINALIZACAO PISO MOLHADO", "Sinalizacao e Outros EPIs"),
            ("CONE COM FITA REFLETIVA", "Sinalizacao e Outros EPIs"),
            ("COLETE REFLETIVO M", "Sinalizacao e Outros EPIs"),
            ("COLETE REFLETIVO G", "Sinalizacao e Outros EPIs"),
            ("COLETE REFLETIVO GG", "Sinalizacao e Outros EPIs"),
            ("PROTECAO SOLAR FPS 50 120ML", "Sinalizacao e Outros EPIs"),
            ("PROTECAO LABIAL FPS 30", "Sinalizacao e Outros EPIs"),
        ]

        for nome, grupo in materiais_limpeza:
            existe = session.query(Material).filter_by(nome=nome).first()
            if not existe:
                session.add(Material(nome=nome, tipo="material", grupo=grupo, ativo=True))
        session.commit()

        for nome, grupo in materiais_epi:
            existe = session.query(Material).filter_by(nome=nome).first()
            if not existe:
                session.add(Material(nome=nome, tipo="epi", grupo=grupo, ativo=True))
        session.commit()

        print("Dados iniciais populados com sucesso!")
        print(f"  - {len(grupos)} grupos de cliente")
        print(f"  - {len(clientes_lista)} clientes")
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
