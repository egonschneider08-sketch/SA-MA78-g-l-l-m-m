"""
main.py — menu interativo para navegar e consultar o banco LuxeVoyage.

Rode a partir da pasta raiz do projeto:

    python main.py

Funciona em cima dos mesmos módulos de CRUD (um por tabela, organizados por
domínio nas pastas geografia/, parceiros/, catalogo/, clientes/, crm/,
comercial/, operacional/, auditoria/) e do utils.execute_query() para
consultas SQL livres.
"""

from utils import execute_query

from geografia import estado, municipio
from parceiros import parceiro, cobertura_parceiro, servico_parceiro, avaliacao_parceiro
from catalogo import pacote, temporada, modulo_pacote, preco_sazonal, destaque_sazonal
from clientes import cliente, interesse_cliente, consentimento_lgpd
from crm import usuario_interno, oportunidade_crm, historico_interacao, solicitacao_sla
from comercial import cotacao_personalizada, item_cotacao, proposta_comercial, contrato_digital
from operacional import viagem, pagamento_contrato
from auditoria import log_acesso


# ---------------------------------------------------------------------------
# Registro central: domínio -> tabelas -> metadados (módulo, pk, colunas...)
# É esse dicionário que o menu usa pra saber quais funções chamar.
# ---------------------------------------------------------------------------
REGISTRO = {
    "Geografia": {
        "Estado": dict(mod=estado, entidade="estado", plural="estados",
                        pk="id_estado",
                        cols=["sigla", "nome", "regiao_nome", "timezone"]),
        "Municipio": dict(mod=municipio, entidade="municipio", plural="municipios",
                           pk="id_municipio",
                           cols=["id_estado", "nome", "categoria"]),
    },
    "Parceiros": {
        "Parceiros": dict(mod=parceiro, entidade="parceiro", plural="parceiros",
                           pk="id_parceiro",
                           cols=["razao_social", "tipo_parceiro", "status"]),
        "Cobertura_Parceiros": dict(mod=cobertura_parceiro, entidade="cobertura", plural="coberturas",
                                     pk="id_cobertura",
                                     cols=["id_parceiro", "id_municipio", "status"]),
        "Servicos_Parceiros": dict(mod=servico_parceiro, entidade="servico", plural="servicos",
                                    pk="id_servico_parceiro",
                                    cols=["id_parceiro", "categoria_servico", "nome_servico"]),
        "Avaliacoes_Parceiros": dict(mod=avaliacao_parceiro, entidade="avaliacao", plural="avaliacoes",
                                      pk="id_avaliacao",
                                      cols=["id_parceiro", "id_usuario_interno", "nota", "comentarios"]),
    },
    "Catalogo": {
        "Pacote": dict(mod=pacote, entidade="pacote", plural="pacotes",
                        pk="id_pacote",
                        cols=["nome_pacote", "id_municipio_destino", "status"]),
        "Temporada": dict(mod=temporada, entidade="temporada", plural="temporadas",
                           pk="id_temporada",
                           cols=["nome", "data_inicio", "data_fim"]),
        "Modulos_Pacote": dict(mod=modulo_pacote, entidade="modulo", plural="modulos",
                                pk="id_modulo",
                                cols=["id_pacote", "id_servico_parceiro", "obrigatorio"]),
        "Preco_Sazonal": dict(mod=preco_sazonal, entidade="preco", plural="precos",
                               pk="id_preco",
                               cols=["id_modulo", "id_temporada", "valor_sugerido"]),
        "Destaques_Sazonais": dict(mod=destaque_sazonal, entidade="destaque", plural="destaques",
                                    pk="id_destaque",
                                    cols=["id_municipio", "data_inicio", "data_fim", "classificacao"]),
    },
    "Clientes": {
        "Cliente": dict(mod=cliente, entidade="cliente", plural="clientes",
                         pk="id_cliente",
                         cols=["nome", "cpf_criptografado", "email_criptografado",
                               "telefone_criptografado", "cep", "id_municipio_origem"]),
        "Interesses_Cliente": dict(mod=interesse_cliente, entidade="interesse", plural="interesses",
                                    pk="id_interesse",
                                    cols=["id_cliente", "id_municipio_destino", "status"]),
        "Consentimentos_LGPD": dict(mod=consentimento_lgpd, entidade="consentimento", plural="consentimentos",
                                     pk="id_consentimento",
                                     cols=["id_cliente", "tipo_consentimento", "status"]),
    },
    "CRM": {
        "Usuario_Interno": dict(mod=usuario_interno, entidade="usuario", plural="usuarios",
                                 pk="id_usuario_interno",
                                 cols=["nome", "cargo", "email_corporativo", "nivel_acesso"]),
        "Oportunidade_CRM": dict(mod=oportunidade_crm, entidade="oportunidade", plural="oportunidades",
                                  pk="id_oportunidade",
                                  cols=["id_cliente", "id_usuario_interno", "estagio_funil", "valor_estimado"]),
        "Historico_Interacoes": dict(mod=historico_interacao, entidade="interacao", plural="interacoes",
                                      pk="id_interacao",
                                      cols=["id_oportunidade", "id_cliente", "id_usuario_interno",
                                            "tipo_interacao", "data_interacao"]),
        "Solicitacao_SLA": dict(mod=solicitacao_sla, entidade="solicitacao", plural="solicitacoes",
                                 pk="id_solicitacao",
                                 cols=["id_oportunidade", "id_parceiro", "data_envio", "status"]),
    },
    "Comercial": {
        "Cotacao_Personalizadas": dict(mod=cotacao_personalizada, entidade="cotacao", plural="cotacoes",
                                        pk="id_cotacao",
                                        cols=["id_oportunidade", "id_pacote", "valor_total_calculado", "status"]),
        "Item_Cotacao": dict(mod=item_cotacao, entidade="item", plural="itens",
                              pk="id_item_cotacao",
                              cols=["id_cotacao", "id_modulo", "valor_aplicado"]),
        "Propostas_Comerciais": dict(mod=proposta_comercial, entidade="proposta", plural="propostas",
                                      pk="id_proposta",
                                      cols=["id_cotacao", "versao", "status"]),
        "Contrato_Digital": dict(mod=contrato_digital, entidade="contrato", plural="contratos",
                                  pk="id_contrato",
                                  cols=["id_proposta", "timestamp_aceite", "ip_aceite",
                                        "hash_integridade", "status"]),
    },
    "Operacional": {
        "Viagem": dict(mod=viagem, entidade="viagem", plural="viagens",
                        pk="id_viagem",
                        cols=["id_contrato", "data_embarque", "data_retorno", "status_viagem"]),
        "Pagamento_Contrato": dict(mod=pagamento_contrato, entidade="pagamento", plural="pagamentos",
                                    pk="id_pagamento",
                                    cols=["id_contrato", "metodo_pagamento", "valor_total",
                                          "numero_parcela", "total_parcelas", "status_transacao"]),
    },
    "Auditoria": {
        "Log_Acesso": dict(mod=log_acesso, entidade="log", plural="logs",
                            pk="id_log",
                            cols=["id_usuario_interno", "id_cliente", "tipo_operacao", "data_acesso"]),
    },
}


# ---------------------------------------------------------------------------
# Helpers de exibição
# ---------------------------------------------------------------------------
def imprimir_registros(registros):
    """Imprime uma lista de dicts (linhas do banco) em formato de tabela simples."""
    if not registros:
        print("(nenhum registro encontrado)")
        return
    colunas = list(registros[0].keys())
    larguras = [max(len(str(c)), *(len(str(r.get(c, ""))) for r in registros)) for c in colunas]

    def linha(valores):
        return " | ".join(str(v).ljust(w) for v, w in zip(valores, larguras))

    print(linha(colunas))
    print("-+-".join("-" * w for w in larguras))
    for r in registros:
        print(linha([r.get(c, "") for c in colunas]))
    print(f"\n({len(registros)} registro(s))")


def ler_valor(campo, obrigatorio=True):
    """Lê um valor do terminal. Enter vazio vira None (útil pra update parcial)."""
    valor = input(f"  {campo}: ").strip()
    if valor == "":
        return None
    return valor


def pausa():
    input("\nPressione Enter para continuar...")


# ---------------------------------------------------------------------------
# Operações genéricas (funcionam para qualquer tabela do REGISTRO)
# ---------------------------------------------------------------------------
def op_criar(info):
    print(f"\n--- Criar novo registro ---")
    valores = [ler_valor(c) for c in info["cols"]]
    funcao = getattr(info["mod"], f"criar_{info['entidade']}")
    try:
        novo_id = funcao(*valores)
        print(f"\n✅ Registro criado com sucesso! id gerado: {novo_id}")
    except Exception as e:
        print(f"\n❌ Erro ao criar registro: {e}")


def op_buscar_por_id(info):
    print(f"\n--- Buscar por id ---")
    id_valor = input(f"  {info['pk']}: ").strip()
    funcao = getattr(info["mod"], f"buscar_{info['entidade']}_por_id")
    try:
        registro = funcao(id_valor)
        imprimir_registros([registro] if registro else [])
    except Exception as e:
        print(f"\n❌ Erro na busca: {e}")


def op_listar(info):
    print(f"\n--- Listar (paginado) ---")
    limit = input("  limite (Enter = 100): ").strip() or "100"
    offset = input("  offset (Enter = 0): ").strip() or "0"
    funcao = getattr(info["mod"], f"listar_{info['plural']}")
    try:
        registros = funcao(limit=int(limit), offset=int(offset))
        imprimir_registros(registros)
    except Exception as e:
        print(f"\n❌ Erro ao listar: {e}")


def op_buscar_por_campo(info):
    print(f"\n--- Buscar por campo ---")
    print("  Colunas disponíveis:", ", ".join([info["pk"]] + info["cols"]))
    campo = input("  campo: ").strip()
    valor = input("  valor: ").strip()
    funcao = getattr(info["mod"], f"buscar_{info['plural']}_por_campo")
    try:
        registros = funcao(campo, valor)
        imprimir_registros(registros)
    except Exception as e:
        print(f"\n❌ Erro na busca: {e}")


def op_atualizar(info):
    print(f"\n--- Atualizar registro ---")
    id_valor = input(f"  {info['pk']}: ").strip()
    print("  Deixe em branco para não alterar um campo.")
    campos = {}
    for c in info["cols"]:
        valor = ler_valor(c, obrigatorio=False)
        if valor is not None:
            campos[c] = valor
    if not campos:
        print("\nNenhum campo informado, nada foi alterado.")
        return
    funcao = getattr(info["mod"], f"atualizar_{info['entidade']}")
    try:
        linhas = funcao(id_valor, **campos)
        print(f"\n✅ Atualização concluída. Linhas afetadas: {linhas}")
    except Exception as e:
        print(f"\n❌ Erro ao atualizar: {e}")


def op_deletar(info):
    print(f"\n--- Deletar registro ---")
    id_valor = input(f"  {info['pk']}: ").strip()
    confirmar = input(f"  Confirma a exclusão do id {id_valor}? (s/n): ").strip().lower()
    if confirmar != "s":
        print("Cancelado.")
        return
    funcao = getattr(info["mod"], f"deletar_{info['entidade']}")
    try:
        linhas = funcao(id_valor)
        print(f"\n✅ Exclusão concluída. Linhas afetadas: {linhas}")
    except Exception as e:
        print(f"\n❌ Erro ao deletar: {e}")


def op_sql_livre():
    print("\n--- Consulta SQL livre (somente SELECT) ---")
    query = input("  SQL> ").strip()
    if not query.lower().startswith("select"):
        print("Por segurança, esse modo aceita apenas comandos SELECT.")
        return
    try:
        registros = execute_query(query, fetch="all")
        imprimir_registros(registros)
    except Exception as e:
        print(f"\n❌ Erro na consulta: {e}")


OPERACOES = {
    "1": ("Criar", op_criar),
    "2": ("Buscar por id", op_buscar_por_id),
    "3": ("Listar (paginado)", op_listar),
    "4": ("Buscar por campo", op_buscar_por_campo),
    "5": ("Atualizar", op_atualizar),
    "6": ("Deletar", op_deletar),
}


# ---------------------------------------------------------------------------
# Menus de navegação
# ---------------------------------------------------------------------------
def menu_tabela(nome_tabela, info):
    while True:
        print(f"\n=== {nome_tabela} ===")
        for chave, (rotulo, _) in OPERACOES.items():
            print(f"  {chave}. {rotulo}")
        print("  0. Voltar")
        escolha = input("Escolha uma opção: ").strip()

        if escolha == "0":
            return
        if escolha in OPERACOES:
            _, funcao = OPERACOES[escolha]
            funcao(info)
            pausa()
        else:
            print("Opção inválida.")


def menu_dominio(nome_dominio, tabelas):
    while True:
        print(f"\n=== {nome_dominio} ===")
        nomes = list(tabelas.keys())
        for i, nome in enumerate(nomes, start=1):
            print(f"  {i}. {nome}")
        print("  0. Voltar")
        escolha = input("Escolha uma tabela: ").strip()

        if escolha == "0":
            return
        if escolha.isdigit() and 1 <= int(escolha) <= len(nomes):
            nome_tabela = nomes[int(escolha) - 1]
            menu_tabela(nome_tabela, tabelas[nome_tabela])
        else:
            print("Opção inválida.")


def menu_principal():
    while True:
        print("\n############################################")
        print("#        LuxeVoyage — Menu Principal        #")
        print("############################################")
        nomes = list(REGISTRO.keys())
        for i, nome in enumerate(nomes, start=1):
            print(f"  {i}. {nome}")
        print("  9. Consulta SQL livre (SELECT)")
        print("  0. Sair")
        escolha = input("Escolha um domínio: ").strip()

        if escolha == "0":
            print("Até logo!")
            break
        if escolha == "9":
            op_sql_livre()
            pausa()
        elif escolha.isdigit() and 1 <= int(escolha) <= len(nomes):
            nome_dominio = nomes[int(escolha) - 1]
            menu_dominio(nome_dominio, REGISTRO[nome_dominio])
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    menu_principal()