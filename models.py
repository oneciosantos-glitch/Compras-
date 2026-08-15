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


class GrupoCliente(Base):
    __tablename__ = "grupos_cliente"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(200), nullable=False, unique=True)
