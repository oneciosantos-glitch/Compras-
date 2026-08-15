import os
import datetime
import streamlit as st
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

ANOS = [str(y) for y in range(2023, datetime.datetime.now().year + 2)]

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
    agora = datetime.datetime.now()
    random_part = f"{os.urandom(3).hex()}"
    return f"ORC-{agora.strftime('%Y%m%d%H%M%S')}-{random_part}"


def salvar_arquivo(uploaded_file, prefixo):
    """Salva um arquivo enviado e retorna o caminho relativo."""
    if uploaded_file is None:
        return None
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
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
        total_orcamentos = session.query(Compra).filter(Compra.orcamento_id.isnot(None)).count()
        orcamentos_unicos = session.query(Compra.orcamento_id).filter(
            Compra.orcamento_id.isnot(None)
        ).distinct().count()

        # Total por situacao
        sit_counts = {}
        for s in SITUACOES:
            sit_counts[s] = session.query(Compra).filter(
                Compra.orcamento_id.isnot(None), Compra.situacao == s
            ).count()

        # Valor total
        from sqlalchemy import func
        valor_total = session.query(func.sum(Compra.valor_total)).filter(
            Compra.orcamento_id.isnot(None)
        ).scalar() or 0

        # Colunas de metricas
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📋 Total de Orcamentos", orcamentos_unicos)
        with col2:
            st.metric("📦 Total de Itens", total_orcamentos)
        with col3:
            st.metric("💰 Valor Total", formatar_moeda(valor_total))
        with col4:
            st.metric("✅ Itens Entregues", sit_counts.get("Entregue", 0))

        st.markdown("---")

        # Cards por situacao
        col_s1, col_s2, col_s3, col_s4 = st.columns(4)
        with col_s1:
            st.markdown(f"""
            <div class="metric-card">
                <h4 style="color:#1e40af; margin:0;">📋 Orcamento Realizado</h4>
                <h2 style="color:#1e40af; margin:5px 0;">{sit_counts.get('Orcamento realizado', 0)}</h2>
            </div>
            """, unsafe_allow_html=True)
        with col_s2:
            st.markdown(f"""
            <div class="metric-card">
                <h4 style="color:#ca8a04; margin:0;">📧 Enviado ao Financeiro</h4>
                <h2 style="color:#ca8a04; margin:5px 0;">{sit_counts.get('Enviado ao financeiro', 0)}</h2>
            </div>
            """, unsafe_allow_html=True)
        with col_s3:
            st.markdown(f"""
            <div class="metric-card">
                <h4 style="color:#16a34a; margin:0;">💰 Pago</h4>
                <h2 style="color:#16a34a; margin:5px 0;">{sit_counts.get('Pago', 0)}</h2>
            </div>
            """, unsafe_allow_html=True)
        with col_s4:
            st.markdown(f"""
            <div class="metric-card">
                <h4 style="color:#0891b2; margin:0;">🚚 Entregue</h4>
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
                                item.data_atualizacao = datetime.datetime.now()
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
                                item.data_atualizacao = datetime.datetime.now()
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
        mes_selecionado = st.selectbox("Mes", list(MESES.keys()), format_func=lambda x: MESES[x], index=datetime.datetime.now().month - 1, key="novo_mes")
    with col_ano:
        ano_selecionado = st.selectbox("Ano", ANOS, index=ANOS.index(str(datetime.datetime.now().year)) if str(datetime.datetime.now().year) in ANOS else 0, key="novo_ano")

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
                agora = datetime.datetime.now()

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
                    agora = datetime.datetime.now()

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
                <p>Documento gerado em {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
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
            if st.button("➕ Adicionar Cliente", key="btn_add_cliente"):
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
        session = get_session()
        try:
            filtro_ativo_c = st.selectbox("Filtro", ["Ativos", "Inativos", "Todos"], key="filtro_cliente_ativo")
            query_c = session.query(Cliente)
            if filtro_ativo_c == "Ativos":
                query_c = query_c.filter_by(ativo=True)
            elif filtro_ativo_c == "Inativos":
                query_c = query_c.filter_by(ativo=False)
            clientes = query_c.order_by(Cliente.nome).all()

            if clientes:
                for c in clientes:
                    status_icon = "✅" if c.ativo else "❌"
                    with st.expander(f"{status_icon} {c.nome}"):
                        col_c1, col_c2 = st.columns(2)
                        with col_c1:
                            if c.ativo:
                                if st.button(f"🔴 Desativar", key=f"desat_cliente_{c.id}"):
                                    c.ativo = False
                                    session.commit()
                                    st.success(f"Cliente '{c.nome}' desativado.")
                                    st.rerun()
                            else:
                                if st.button(f"🟢 Reativar", key=f"reat_cliente_{c.id}"):
                                    c.ativo = True
                                    session.commit()
                                    st.success(f"Cliente '{c.nome}' reativado.")
                                    st.rerun()
                        with col_c2:
                            novo_nome_c = st.text_input("Novo Nome", value=c.nome, key=f"ren_cliente_{c.id}")
                            if st.button(f"✏️ Renomear", key=f"btn_ren_cliente_{c.id}"):
                                if novo_nome_c.strip() and novo_nome_c.strip().upper() != c.nome:
                                    c.nome = novo_nome_c.strip().upper()
                                    session.commit()
                                    st.success("Nome atualizado!")
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
                        status_icon = "✅" if m.ativo else "❌"
                        tipo_label = "Limpeza" if m.tipo == "material" else "EPI"
                        with st.expander(f"{status_icon} {m.nome} ({tipo_label})"):
                            col_m1, col_m2, col_m3 = st.columns(3)
                            with col_m1:
                                if m.ativo:
                                    if st.button(f"🔴 Desativar", key=f"desat_mat_{m.id}"):
                                        m.ativo = False
                                        session.commit()
                                        st.success("Material desativado.")
                                        st.rerun()
                                else:
                                    if st.button(f"🟢 Reativar", key=f"reat_mat_{m.id}"):
                                        m.ativo = True
                                        session.commit()
                                        st.success("Material reativado.")
                                        st.rerun()
                            with col_m2:
                                novo_grupo_m = st.text_input("Novo Grupo", value=m.grupo or "", key=f"edit_grupo_mat_{m.id}")
                                if st.button(f"✏️ Alterar Grupo", key=f"btn_alt_grupo_{m.id}"):
                                    m.grupo = novo_grupo_m.strip().upper() if novo_grupo_m.strip() else "OUTROS"
                                    session.commit()
                                    st.success("Grupo atualizado!")
                                    st.rerun()
                            with col_m3:
                                st.info(f"Tipo: {tipo_label}")
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
                        item.data_atualizacao = datetime.datetime.now()

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
def main():
    # Pagina padrao
    if "pagina_atual" not in st.session_state:
        st.session_state["pagina_atual"] = "Dashboard"

    with st.sidebar:
        st.markdown("## 🛒 Sistema de Compras")
        st.markdown("---")

        pagina = st.radio(
            "Navegacao",
            ["Dashboard", "Orcamentos", "Novo Orcamento", "Editar Orcamento", "Editar Item", "Imprimir", "Cadastros"],
            index=["Dashboard", "Orcamentos", "Novo Orcamento", "Editar Orcamento", "Editar Item", "Imprimir", "Cadastros"].index(
                st.session_state["pagina_atual"]
            ) if st.session_state["pagina_atual"] in ["Dashboard", "Orcamentos", "Novo Orcamento", "Editar Orcamento", "Editar Item", "Imprimir", "Cadastros"] else 0,
            key="nav_radio",
        )

        if pagina != st.session_state["pagina_atual"]:
            st.session_state["pagina_atual"] = pagina
            st.rerun()

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
