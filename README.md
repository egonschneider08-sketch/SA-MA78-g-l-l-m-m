# ✈️ Luxe Voyage — Sistema de Expansão Nacional


> Reestruturação do modelo de dados para operação em escala nacional, 100% remota e digital.

![Status](https://img.shields.io/badge/status-em%20desenvolvimento-blue)
![Versão](https://img.shields.io/badge/versão-1.0-green)
![Banco](https://img.shields.io/badge/banco-MySQL-4479A1)

---

## Sobre o projeto

A **Luxe Voyage** é uma agência de viagens que operava exclusivamente no litoral Sul e Sudeste. Este projeto reestrutura o sistema de dados para suportar uma operação nacional cobrindo todos os **26 estados e o Distrito Federal**, sem abertura de filiais físicas.

A expansão é sustentada por quatro pilares estruturais que guiam toda a modelagem do banco de dados e as funcionalidades do sistema.

| Métrica | Valor |
|---|---|
| Requisitos funcionais | 22 |
| Requisitos não funcionais | 7 |
| Estados cobertos | 27 (26 UFs + DF) |
| Sessões de entrega | 3 |

---

## Pilares do sistema

### P1 — Hierarquia geográfica nacional
Malha geográfica completa com estados e municípios categorizados entre **capitais** e **cidades turísticas principais**. Filtros regionais por Norte, Nordeste, Centro-Oeste, Sudeste e Sul. Marcação de destinos sazonais por período.

### P2 — Rede de parceiros terceirizados
Cadastro de **Operadoras Nacionais** e **Receptivos Locais/DMCs** com área de cobertura mapeada por município. Vínculo automático entre parceiro e destino no momento da criação de pacotes.

### P3 — Pacotes modulares de viagem
Composição dinâmica de pacotes por módulos independentes (hotel, passeio, transfer, aéreo). Precificação automática por sazonalidade regional (baixa, média, alta). Geração de cotação personalizada em PDF.

### P4 — Rastreabilidade de clientes
Base de clientes interestadual com **UF de origem obrigatória**, histórico completo de interações, envio de proposta 100% digital e contrato com **aceite eletrônico** (timestamp + registro de IP).

---

## Tecnologias

### Banco de dados
- MySQL 8.0+
- Particionamento de tabelas por UF e por data (`PARTITION BY LIST` e `RANGE`)
- Índices compostos para buscas regionais
- Criptografia AES-256 via `AES_ENCRYPT()` em dados sensíveis
- Engine InnoDB (suporte a transações e chaves estrangeiras)

### Back-end
- Node.js ou Python (a definir na Sessão 2)
- REST API
- Autenticação JWT
- Geração automática de PDF para cotações e contratos

### Infraestrutura
- Arquitetura com escalabilidade horizontal
- Backup incremental a cada hora + backup completo diário
- Retenção de 30 dias | RPO máximo de 1 hora
- HTTPS obrigatório
- SLA mínimo de 99,5% de uptime

---

## Estrutura do banco de dados

```
luxe_voyage/
├── geografia/
│   ├── estados          → 27 registros (26 UFs + DF)
│   └── municipios       → particionado por estado
├── parceiros/
│   ├── parceiros        → tipo: operadora_nacional | receptivo_local
│   └── cobertura        → vínculo N:N parceiro ↔ município
├── pacotes/
│   ├── pacotes          → particionado por estado/destino
│   ├── modulos          → hotel | passeio | transfer | aereo
│   └── sazonalidade     → baixa | media | alta por destino
└── clientes/
    ├── clientes         → particionado por UF de origem
    ├── interacoes       → particionado por mês (histórico)
    └── contratos        → imutável + hash de integridade
```

### Estratégias de particionamento

| Tabela | Critério | Tipo MySQL | Motivo |
|---|---|---|---|
| `clientes` | UF de origem | `PARTITION BY LIST` | Consultas regionais não varrem o banco inteiro |
| `pacotes` | Estado/destino | `PARTITION BY LIST` | Filtros por região sem full scan |
| `interacoes` | Mês/ano | `PARTITION BY RANGE` | Histórico cresce indefinidamente; acesso recente é mais frequente |

---

## Requisitos funcionais (resumo)

| Pilar | IDs | Quantidade |
|---|---|---|
| Hierarquia geográfica | RF-01 a RF-05 | 5 |
| Rede de parceiros | RF-06 a RF-10 | 5 |
| Pacotes modulares | RF-11 a RF-16 | 6 |
| Rastreabilidade de clientes | RF-17 a RF-22 | 6 |

---

## Requisitos não funcionais (resumo)

| ID | Categoria | Meta |
|---|---|---|
| RNF-01 | Tempo de resposta | < 2 segundos para buscas e filtros |
| RNF-02 | Escalabilidade horizontal | Novas instâncias sem reescrever o sistema |
| RNF-03 | Sharding e particionamento | Tabelas particionadas por UF, destino e data |
| RNF-04 | Criptografia e mascaramento | AES-256 + exibição mascarada para agentes |
| RNF-05 | LGPD | Consentimento, anonimização e exclusão a pedido |
| RNF-06 | Backups automáticos | Incremental/hora + completo/dia, retenção 30 dias |
| RNF-07 | Alta disponibilidade | SLA 99,5%, resistência a picos em feriados |

---

## Cronograma

```
Sessão 1 — Qua 18/06 · 19h30
  └── Planejamento, requisitos, stakeholders e diagrama conceitual

Sessão 2 — Qua 25/06 · 14h45–17h00
  └── Criação do banco de dados (DDL completo) + início da programação

Sessão 3 — Qui 03/07 · 14h45–17h00
  └── Testes, ajustes e entrega final com demo do fluxo completo
```

---

## Segurança e conformidade (LGPD)

- CPF, telefone e e-mail armazenados com criptografia AES-256
- Mascaramento parcial na exibição para agentes (ex: `123.***.***-00`)
- Contratos digitais em armazenamento imutável com hash de integridade
- Consentimento de uso registrado no momento do cadastro
- Logs de acesso a dados sensíveis mantidos por 12 meses
- Clientes podem solicitar exclusão ou anonimização a qualquer momento

---

## Stakeholders

### Internos
| Nome | Papel | Prioridade no projeto |
|---|---|---|
| Ricardo Almeida | Sócio fundador e diretor geral | Manter qualidade do atendimento na migração |
| Patrícia Costa | Sócia e diretora comercial | Painel de gestão centralizado por região |
| Fernando Matos | Sócio e responsável financeiro | Controle de custos de infraestrutura |

### Externos (clientes)
| Nome | Perfil | Necessidade |
|---|---|---|
| Ana Souza, 36 — Porto Alegre | Cliente fiel | Histórico e cotação self-service pelo celular |
| Thiago Ribeiro, 44 — Goiânia | Cliente potencial | Preço estimado visível sem entrar em contato |
| Juliana Lima, 29 — Recife | Cliente potencial | Contrato digital sem papel |

---

*Luxe Voyage · Projeto de expansão nacional · v1.0 · Iniciado em junho de 2025*
