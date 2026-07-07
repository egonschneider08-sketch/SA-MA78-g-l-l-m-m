# LuxeVoyage CRUD (Python modularizado)

CRUD completo, um módulo por tabela, para as 25 tabelas do banco `LuxeVoyage`,
organizado em pastas por domínio.

## Estrutura

```
database.py               -> conexão com o banco (preencha suas credenciais)
utils.py                  -> execute_query() e build_update_clause() (usados por todos os módulos)
main.py                   -> exemplos de uso
requirements.txt

geografia/
    estado.py
    municipio.py

parceiros/
    parceiro.py               -> tabela Parceiros
    cobertura_parceiro.py     -> tabela Cobertura_Parceiros
    servico_parceiro.py       -> tabela Servicos_Parceiros
    avaliacao_parceiro.py     -> tabela Avaliacoes_Parceiros

catalogo/
    pacote.py
    temporada.py
    modulo_pacote.py          -> tabela Modulos_Pacote
    preco_sazonal.py
    destaque_sazonal.py       -> tabela Destaques_Sazonais

clientes/
    cliente.py
    interesse_cliente.py      -> tabela Interesses_Cliente
    consentimento_lgpd.py     -> tabela Consentimentos_LGPD

crm/
    usuario_interno.py
    oportunidade_crm.py
    historico_interacao.py    -> tabela Historico_Interacoes
    solicitacao_sla.py

comercial/
    cotacao_personalizada.py  -> tabela Cotacao_Personalizadas
    item_cotacao.py
    proposta_comercial.py     -> tabela Propostas_Comerciais
    contrato_digital.py

operacional/
    viagem.py
    pagamento_contrato.py

auditoria/
    log_acesso.py
```

Cada pasta é um pacote Python (tem `__init__.py`), agrupando tabelas do mesmo
domínio de negócio. `database.py` e `utils.py` ficam na raiz porque são
compartilhados por todos os domínios.

## Padrão de cada módulo

Todos os 25 módulos de tabela seguem exatamente o mesmo padrão de funções:

```python
criar_<entidade>(coluna1, coluna2, ...)          # INSERT -> retorna o id gerado
buscar_<entidade>_por_id(id)                     # SELECT * WHERE pk = id -> dict ou None
listar_<entidades>(limit=100, offset=0)          # SELECT * paginado -> lista de dicts
buscar_<entidades>_por_campo(campo, valor)       # SELECT * WHERE <campo> = valor
atualizar_<entidade>(id, **campos)               # UPDATE dinâmico (só os campos passados)
deletar_<entidade>(id)                           # DELETE WHERE pk = id
```

## Como importar

```python
from clientes import cliente
from catalogo import pacote
from operacional import viagem

novo_id = cliente.criar_cliente(
    nome="Fulano de Tal",
    cpf_criptografado="CPF_HASH_XYZ",
    email_criptografado="EMAIL_HASH_XYZ",
    telefone_criptografado="TEL_HASH_XYZ",
    cep="88000-000",
    id_municipio_origem=24,
)

c = cliente.buscar_cliente_por_id(novo_id)
cliente.atualizar_cliente(novo_id, cep="88010-000")
cliente.deletar_cliente(novo_id)
```

⚠️ **Importante:** rode os scripts sempre a partir da pasta raiz do projeto
(ex: `python main.py`), pois é isso que garante que `database.py` e
`utils.py` sejam encontrados pelos módulos dentro das subpastas.

## Conexão

`database.py` só tem a função `get_connection()` com placeholders — como você
disse que vai cuidar da conexão, é só preencher ali (ou usar as variáveis de
ambiente `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME` que já
estão previstas no arquivo).

## Instalação

```bash
pip install -r requirements.txt
```
