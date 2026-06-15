---
name: monitor-reforma-tributaria
metadata:
  version: "1.0"
  owner: "Equipe que instalou a skill"
  review: "Revisar a cada mudança normativa relevante ou semestralmente"
description: >-
  Monitor de atualizações normativas da Reforma Tributária brasileira (CBS, IBS,
  Imposto Seletivo). Faz uma varredura nas fontes oficiais (Diário Oficial da
  União, Receita Federal, Comitê Gestor do IBS, Planalto, Ministério da Fazenda),
  compara com o registro de acompanhamento do usuário e reporta o que mudou, com
  classificação de impacto e próximos prazos. Use sempre que o usuário pedir para
  "rodar o monitor da reforma", "checar novidades da CBS/IBS", "atualização
  normativa", "o que mudou na reforma tributária", "saiu alguma resolução do
  CGIBS", "monitorar a reforma", ou quiser uma rodada periódica de acompanhamento
  legislativo da EC 132/2023 e da LC 214/2025. Funciona para qualquer advogado,
  contador ou empresa que precise acompanhar a transição 2026–2033.
---

# Monitor da Reforma Tributária — buscador de atualizações normativas

Esta skill executa um protocolo de varredura das fontes oficiais da Reforma
Tributária brasileira e devolve um relatório do que mudou desde a última rodada.
Ela serve a quem precisa acompanhar a transição sem ter de visitar dezenas de
sites a cada semana: o assistente faz as buscas, cruza com o seu histórico e te
diz o que é ruído e o que exige ação.

O objetivo é separar **norma publicada** (que muda premissa e cálculo) de
**notícia e análise** (que ajuda a entender, mas não decide nada). Por isso o
protocolo prioriza o Diário Oficial e os portais `gov.br`, e trata portais
especializados como apoio interpretativo, sempre a confirmar na fonte primária.

## Quando disparar

Sempre que o usuário quiser saber o que mudou na Reforma Tributária, pedir uma
rodada de monitoramento, perguntar sobre uma resolução/portaria recente, ou
montar um acompanhamento periódico. Não há input obrigatório. O usuário pode,
opcionalmente, informar:

- **Data de referência** (padrão: hoje).
- **Foco específico** (ex.: "só IBS", "só Simples Nacional", "só Imposto Seletivo").
- **Registro de acompanhamento** (um arquivo de changelog que ele já mantenha).
  Se não houver, a skill ajuda a criar um a partir do modelo em
  `references/changelog_modelo.md`.

## Dado sensível: o que esta skill NÃO faz

Este é um monitor de **informação pública**. Ele lê normas e atos oficiais, que
são públicos por natureza. Para que o fluxo seja seguro de compartilhar e de
rodar em qualquer máquina:

- **Não processa dados de clientes.** Nomes, CNPJs, faturamento, SPED, DRE ou
  qualquer dado de empresa não entram neste fluxo. Se o usuário pedir análise de
  um cliente, isso é outra tarefa — esta skill só acompanha a legislação.
- **Não guarda segredos.** Não pede nem armazena senhas, tokens ou credenciais.
  As buscas são em fontes abertas, sem login.
- **O registro de acompanhamento só contém norma.** O changelog que a skill
  mantém registra atos normativos e datas — nunca dados identificáveis de
  terceiros.

Se em algum momento o usuário colar dados de cliente no contexto, não os escreva
no changelog nem em nenhum arquivo desta skill. Apenas siga com o monitoramento
normativo.

---

## Fluxo de trabalho

### Passo 1 — Buscar nas fontes oficiais

Rodar buscas web nas fontes abaixo, nesta ordem de prioridade. A lista completa,
com os links e o que procurar em cada uma, está em `references/fontes_oficiais.md`
— leia esse arquivo se precisar dos endereços ou quiser ampliar a cobertura.

**Fontes primárias (`gov.br` — confiança alta):**

- `site:gov.br/receitafederal reforma tributária CBS IBS`
- `site:gov.br/fazenda reforma tributária nota`
- `site:in.gov.br CBS IBS "imposto seletivo"` (Diário Oficial da União)
- Comitê Gestor do IBS — resoluções e atos conjuntos
- Planalto — leis complementares e decretos do ano corrente

**Apoio interpretativo (confirmar sempre na fonte primária):**

- Portais especializados e imprensa jurídica, usados só para localizar o ato e
  depois conferir no Diário Oficial.

### Passo 2 — Conferir os parâmetros críticos

Para cada parâmetro, dizer se está **sem alteração**, **atualizado** ou
**pendente**. A tabela de referência com os valores e as fontes está em
`references/parametros_criticos.md`. Os pontos que mais se mexem na transição são
as alíquotas de referência de CBS e IBS, o cronograma 2026–2033, os fatores
setoriais, o Imposto Seletivo, o Split Payment e a regulamentação do Simples
Nacional.

Importante: alíquotas marcadas como **estimativa** não devem ser apresentadas
como valor fixo. Quando uma fonte trouxer um número novo, confirme na norma antes
de tratá-lo como definitivo.

### Passo 3 — Identificar novidades

Para cada ato encontrado, registrar:

- Nome do ato, data e fonte (Diário Oficial / portal oficial).
- Resumo do impacto em até três linhas.
- Classificação: **CRÍTICO** (altera cálculo ou premissa de alíquota) ·
  **RELEVANTE** (altera premissa qualitativa) · **INFORMATIVO**.
- Prazo sugerido de tratamento: CRÍTICO em 48h · RELEVANTE em 72h ·
  INFORMATIVO no próximo ciclo.

### Passo 4 — Propor atualização e pedir confirmação

Se houver novidade CRÍTICA ou RELEVANTE, apresentar ao usuário o que muda e onde,
e **perguntar antes de gravar qualquer coisa**: "Encontrei [N] novidade(s).
Quer que eu atualize o seu registro agora?". Só escrever após confirmação
explícita. Esse cuidado evita que uma leitura equivocada de uma notícia entre no
registro como se fosse norma.

### Passo 5 — Registrar no changelog

Após a confirmação, adicionar uma entrada datada ao registro de acompanhamento,
no formato de `references/changelog_modelo.md`:

```markdown
### DD/MM/AAAA — [Nome do ato] ⭐ NOVO
- **Fonte:** [Diário Oficial / portal oficial] | [data de publicação]
- **Escopo:** [resumo]
- **Classificação:** CRÍTICO | RELEVANTE | INFORMATIVO
- **Impacto:** [o que muda na prática]
- **A validar:** [o que ainda precisa de confirmação na fonte, se houver]
```

Sempre que um dado não estiver confirmado na fonte oficial, marque-o como
**a validar** e aponte onde conferir. É melhor um registro honesto sobre a
incerteza do que um número que aparenta firmeza que não tem.

---

## Formato do relatório final

Ao terminar, exibir um resumo enxuto:

```
📋 MONITOR DA REFORMA TRIBUTÁRIA — [data]
──────────────────────────────────────────
Fontes verificadas: [N]
Novidades: [N]  (CRÍTICO [N] · RELEVANTE [N] · INFORMATIVO [N])

Destaques:
  • [ato] — [uma linha]

Próximos eventos esperados:
  • [data]: [evento]

Próxima rodada sugerida: [data]
```

Depois do resumo, se houver novidades, liste-as com fonte e link para o usuário
conferir. Feche reforçando que o monitor é um apoio de acompanhamento e que a
decisão e a leitura da norma na íntegra continuam sendo do profissional.

## Rodar de forma agendada

Para deixar o monitor rodando sozinho toda semana (e, onde houver conector de
e-mail, deixar um rascunho de resumo), siga o guia em
`references/automacao_agendada.md`.

## Ressalva

Esta skill faz acompanhamento normativo de apoio. Não é parecer jurídico nem
contábil, não afirma alíquota sem fonte e não promete economia. A conferência da
norma na fonte oficial e a decisão final são sempre do profissional que a utiliza.
