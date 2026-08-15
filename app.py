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

ARQ_MODELS_PY = r'''from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
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


class GrupoCliente(Base):
    __tablename__ = "grupos_cliente"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(200), nullable=False, unique=True)
'''

ARQ_DATABASE_PY = r'''import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")

SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

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

ARQ_SEED_PY = r'''from database import get_session, init_db
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
                session.add(Material(nome=nome, tipo="material", grupo="Material de Limpeza", ativo=True))
        session.commit()

        for item in materiais_epi:
            nome = item[0]
            existe = session.query(Material).filter_by(nome=nome).first()
            if not existe:
                session.add(Material(nome=nome, tipo="epi", grupo="EPI", ativo=True))
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

ARQ_APP_PY = r'''import os
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

# ============================================================
# CONFIGURACAO DA PAGINA
# ============================================================
st.set_page_config(
    page_title="Sistema de Controle de Compras",
    page_icon="🛒",
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

# Inicializar banco na primeira execucao
if "db_initialized" not in st.session_state:
    init_db()
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


def badge_situacao_html(situacao):
    cor = COR_SITUACAO.get(situacao, "#6b7280")
    return f'<span class="badge" style="background-color:{cor}">{situacao}</span>'


def formatar_moeda(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


# ============================================================
# PAGINA: DASHBOARD (HOME)
# ============================================================
def pagina_dashboard():
    st.title("📊 Painel de Controle")
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
            st.metric("📋 Total de Pedidos", orcamentos_unicos)
        with col2:
            st.metric("📦 Total de Itens", total_itens)
        with col3:
            st.metric("💰 Valor Total", formatar_moeda(valor_total))
        with col4:
            st.metric("✅ Pedidos Entregues", sit_counts.get("Entregue", 0))

        st.markdown("---")

        # Cards por situacao
        col_s1, col_s2, col_s3, col_s4 = st.columns(4)
        with col_s1:
            st.markdown(f"""
            <div class="metric-card">
                <h4 style="color:#1e40af; margin:0;">📋 Pedidos: Orcamento Realizado</h4>
                <h2 style="color:#1e40af; margin:5px 0;">{sit_counts.get('Orcamento realizado', 0)}</h2>
            </div>
            """, unsafe_allow_html=True)
        with col_s2:
            st.markdown(f"""
            <div class="metric-card">
                <h4 style="color:#ca8a04; margin:0;">📧 Pedidos: Enviado ao Financeiro</h4>
                <h2 style="color:#ca8a04; margin:5px 0;">{sit_counts.get('Enviado ao financeiro', 0)}</h2>
            </div>
            """, unsafe_allow_html=True)
        with col_s3:
            st.markdown(f"""
            <div class="metric-card">
                <h4 style="color:#16a34a; margin:0;">💰 Pedidos: Pagos</h4>
                <h2 style="color:#16a34a; margin:5px 0;">{sit_counts.get('Pago', 0)}</h2>
            </div>
            """, unsafe_allow_html=True)
        with col_s4:
            st.markdown(f"""
            <div class="metric-card">
                <h4 style="color:#0891b2; margin:0;">🚚 Pedidos: Entregues</h4>
                <h2 style="color:#0891b2; margin:5px 0;">{sit_counts.get('Entregue', 0)}</h2>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # Top 10 clientes por valor
        st.subheader("🏆 Top 10 Clientes por Valor")
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
                st.markdown(f"**{i}.** {cliente} — {formatar_moeda(total)}")
        else:
            st.info("Nenhum orcamento registrado ainda.")

    finally:
        session.close()


# ============================================================
# PAGINA: LISTAR ORCAMENTOS
# ============================================================
def pagina_orcamentos():
    st.title("📋 Orcamentos")

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
                f"{orc_id} — {primeiro.cliente} — {MESES.get(primeiro.mes, primeiro.mes)}/{primeiro.ano}"
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
                    anexos.append(f"📎 Orcamento: {primeiro.arquivo_orcamento}")
                if primeiro.arquivo_comprovante:
                    anexos.append(f"📎 Comprovante: {primeiro.arquivo_comprovante}")
                if anexos:
                    st.markdown("\n".join(anexos))

                # Botoes
                col_b1, col_b2, col_b3, col_b4, col_b5 = st.columns(5)
                with col_b1:
                    if st.button("✏️ Editar", key=f"edit_{orc_id}"):
                        st.session_state["editar_orcamento_id"] = orc_id
                        st.session_state["pagina_atual"] = "Editar Orcamento"
                        st.rerun()
                with col_b2:
                    if st.button("🖨️ Imprimir", key=f"print_{orc_id}"):
                        st.session_state["imprimir_orcamento_id"] = orc_id
                        st.session_state["pagina_atual"] = "Imprimir"
                        st.rerun()
                with col_b3:
                    if st.button("🔄 Avancar Situacao", key=f"avancar_{orc_id}"):
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
                    if st.button("⏪ Voltar Situacao", key=f"voltar_{orc_id}"):
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
                    if st.button("🗑️ Excluir", key=f"delete_{orc_id}"):
                        st.session_state[f"confirmar_excluir_{orc_id}"] = True
                        st.rerun()

                # Confirmacao de exclusao
                if st.session_state.get(f"confirmar_excluir_{orc_id}", False):
                    st.warning(f"⚠️ Tem certeza que deseja excluir o orcamento {orc_id}? Esta acao nao pode ser desfeita!")
                    col_conf1, col_conf2 = st.columns(2)
                    with col_conf1:
                        if st.button("✅ Sim, Excluir", key=f"confirm_yes_{orc_id}"):
                            for item in itens:
                                session.delete(item)
                            session.commit()
                            st.success("Orcamento excluido com sucesso!")
                            st.session_state[f"confirmar_excluir_{orc_id}"] = False
                            st.rerun()
                    with col_conf2:
                        if st.button("❌ Cancelar", key=f"confirm_no_{orc_id}"):
                            st.session_state[f"confirmar_excluir_{orc_id}"] = False
                            st.rerun()

    finally:
        session.close()


# ============================================================
# PAGINA: NOVO ORCAMENTO
# ============================================================
def pagina_novo_orcamento():
    st.title("➕ Novo Orcamento")

    # Inicializar session_state para itens
    if "novos_itens" not in st.session_state:
        st.session_state["novos_itens"] = []

    clientes = obter_clientes_ativos()
    if not clientes:
        st.error("Nenhum cliente cadastrado. Cadastre clientes primeiro!")
        return

    clientes_nomes = [c.nome for c in clientes]

    # Selecionar cliente
    cliente_selecionado = st.selectbox("🏢 Selecione o Cliente", [""] + clientes_nomes, key="novo_cliente")

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
    st.subheader("📦 Itens do Orcamento")

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
        opcoes_materiais.append(f"── {grupo} ──")
        for nome in nomes:
            opcoes_materiais.append(nome)

    col_mat, col_qtd, col_val, col_btn = st.columns([3, 1, 1, 1])
    with col_mat:
        material_sel = st.selectbox("Material", [""] + opcoes_materiais, key="novo_material_sel")
    with col_qtd:
        qtd = st.number_input("Quantidade", min_value=1, value=1, step=1, key="novo_qtd")
    with col_val:
        valor_unit = st.number_input("Valor Unit. (R$)", min_value=0.0, value=0.0, step=0.01, format="%0.2f", key="novo_valor_unit")
    with col_btn:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("➕ Adicionar Item", key="btn_add_item"):
            # Validar que o material selecionado nao e um cabecalho de grupo
            if material_sel and not material_sel.startswith("──"):
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
        st.subheader(f"📋 Itens Adicionados ({len(st.session_state['novos_itens'])})")

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
                if st.button("🗑", key=f"remove_item_{idx}"):
                    itens_para_remover.append(idx)

        # Remover itens (fora do loop para nao alterar indices durante iteracao)
        if itens_para_remover:
            for idx in sorted(itens_para_remover, reverse=True):
                st.session_state["novos_itens"].pop(idx)
            st.rerun()

        # Total geral
        total_geral = sum(i["valor_total"] for i in st.session_state["novos_itens"])
        st.markdown(f"### 💰 Total do Orcamento: {formatar_moeda(total_geral)}")

    # Upload de arquivos
    st.markdown("---")
    st.subheader("📎 Anexos")
    col_up1, col_up2 = st.columns(2)
    with col_up1:
        arquivo_orc = st.file_uploader("Arquivo do Orcamento", type=["pdf", "png", "jpg", "jpeg", "doc", "docx", "xls", "xlsx"], key="novo_arq_orc")
    with col_up2:
        arquivo_comp = st.file_uploader("Comprovante", type=["pdf", "png", "jpg", "jpeg", "doc", "docx", "xls", "xlsx"], key="novo_arq_comp")

    # Botao salvar
    st.markdown("---")
    if st.session_state["novos_itens"]:
        if st.button("💾 Salvar Orcamento", type="primary", use_container_width=True):
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
                st.success(f"✅ Orcamento {orc_id} salvo com sucesso!")

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
    st.title("✏️ Editar Orcamento")

    orc_id = st.session_state.get("editar_orcamento_id")
    if not orc_id:
        st.warning("Nenhum orcamento selecionado para edicao. Volte a lista de orcamentos e clique em Editar.")
        if st.button("📋 Ir para Orcamentos"):
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
        st.subheader("📦 Itens")

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
                    if st.button("🗑", key=f"edit_remove_{idx}_{orc_id}"):
                        item["remover"] = True
                        st.rerun()

        # Adicionar novo item ao orcamento existente
        st.markdown("---")
        st.subheader("➕ Adicionar Novo Item")

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
                opcoes.append(f"── {grupo} ──")
                for nome in nomes:
                    opcoes.append(nome)

            col_a1, col_a2, col_a3, col_a4 = st.columns([3, 1, 1, 1])
            with col_a1:
                mat_add = st.selectbox("Material", [""] + opcoes, key=f"add_mat_{orc_id}")
            with col_a2:
                qtd_add = st.number_input("Qtd", min_value=1, value=1, step=1, key=f"add_qtd_{orc_id}")
            with col_a3:
                val_add = st.number_input("Valor Unit.", min_value=0.0, value=0.0, step=0.01, format="%0.2f", key=f"add_val_{orc_id}")
            with col_a4:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("➕ Adicionar", key=f"btn_add_exist_{orc_id}"):
                    if mat_add and not mat_add.startswith("──"):
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
        st.markdown(f"### 💰 Total: {formatar_moeda(total)}")

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
            if st.button("💾 Salvar Alteracoes", type="primary", use_container_width=True, key=f"save_edit_{orc_id}"):
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
                    st.success("✅ Orcamento atualizado com sucesso!")

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
            if st.button("❌ Cancelar", use_container_width=True, key=f"cancel_edit_{orc_id}"):
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
    st.title("🖨️ Imprimir Orcamento")

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
            anexos_html += f'<p>📎 Arquivo Orcamento: {primeiro.arquivo_orcamento}</p>'
        if primeiro.arquivo_comprovante:
            anexos_html += f'<p>📎 Comprovante: {primeiro.arquivo_comprovante}</p>'

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
                <h1>🛒 Sistema de Controle de Compras</h1>
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
                    🖨️ Imprimir
                </button>
            </div>
        </body>
        </html>
        """

        st.components.v1.html(html_impressao, height=800, scrolling=True)

        # Botao para baixar HTML
        st.download_button(
            "📥 Baixar HTML para Impressao",
            data=html_impressao,
            file_name=f"orcamento_{orc_id}.html",
            mime="text/html",
        )

        if st.button("🔙 Voltar para Orcamentos"):
            st.session_state["imprimir_orcamento_id"] = None
            st.session_state["pagina_atual"] = "Orcamentos"
            st.rerun()

    finally:
        session.close()


# ============================================================
# PAGINA: CADASTROS
# ============================================================
def pagina_cadastros():
    st.title("📝 Cadastros")

    tab_clientes, tab_materiais, tab_grupos = st.tabs(["🏢 Clientes", "📦 Materiais", "👥 Grupos de Cliente"])

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
        with st.expander("➕ Novo Material", expanded=False):
            col_nm1, col_nm2, col_nm3 = st.columns(3)
            with col_nm1:
                novo_mat_nome = st.text_input("Nome do Material", key="novo_mat_nome")
            with col_nm2:
                novo_mat_tipo = st.selectbox("Tipo", ["material", "epi"], format_func=lambda x: "Material de Limpeza" if x == "material" else "EPI", key="novo_mat_tipo")
            with col_nm3:
                novo_mat_grupo = st.text_input("Grupo", placeholder="Ex: Detergentes e Desinfetantes", key="novo_mat_grupo")

            if st.button("➕ Adicionar Material", key="btn_add_material"):
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
                            col_m1, col_m2, col_m3, col_m4 = st.columns(4)
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
                                st.info(f"Tipo: {tipo_label}")
                                if not m.ativo:
                                    if st.button("\U0001f5d1 Excluir", key=f"excl_mat_{m.id}"):
                                        tem_compras = session.query(Compra).filter_by(material=m.nome).first()
                                        if tem_compras:
                                            st.warning("Material tem compras vinculadas. Nao e possivel excluir.")
                                        else:
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
            if st.button("➕ Adicionar Grupo", key="btn_add_grupo"):
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
                    with st.expander(f"👥 {g.nome}"):
                        col_g1, col_g2 = st.columns(2)
                        with col_g1:
                            novo_nome_g = st.text_input("Novo Nome", value=g.nome, key=f"ren_grupo_{g.id}")
                            if st.button(f"✏️ Renomear", key=f"btn_ren_grupo_{g.id}"):
                                if novo_nome_g.strip() and novo_nome_g.strip().upper() != g.nome:
                                    g.nome = novo_nome_g.strip().upper()
                                    session.commit()
                                    st.success("Nome atualizado!")
                                    st.rerun()
                        with col_g2:
                            if st.button(f"🗑️ Excluir", key=f"exc_grupo_{g.id}"):
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
    st.title("✏️ Editar Item")

    # Selecionar item por ID
    item_id = st.number_input("ID do Item", min_value=1, step=1, key="editar_item_id_input")

    if st.button("🔍 Buscar Item"):
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
            if st.button("💾 Salvar", type="primary", key="save_edit_item"):
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
                        st.success("✅ Item atualizado com sucesso!")
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
            if st.button("❌ Cancelar", key="cancel_edit_item"):
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
        st.markdown("## 🛒 Sistema de Compras")
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
        st.markdown("""
        <div style='color: rgba(255,255,255,0.6); font-size: 0.8em;'>
            Sistema de Controle de Compras<br>
            Versao Streamlit 1.0
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
        try:
            sys.path.insert(0, PASTA_SISTEMA)
            from seed import popular_dados
            print("  Verificando novos dados...")
            popular_dados()
            print("  \u2705 Novos clientes/materiais adicionados (sem duplicar existentes).")
        except Exception as e:
            print(f"  \u26a0\ufe0f Nao foi possivel verificar novos dados: {e}")
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
