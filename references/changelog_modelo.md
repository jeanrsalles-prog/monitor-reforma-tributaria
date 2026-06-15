# Modelo de registro de acompanhamento (changelog normativo)

Copie este modelo para um arquivo seu (por exemplo, `CHANGELOG_NORMATIVO.md`) na
pasta onde quiser manter o histórico. A skill acrescenta entradas novas no topo,
preservando as antigas. O registro guarda **apenas informação normativa pública**
— nunca dados de clientes.

---

```markdown
# Registro de acompanhamento — Reforma Tributária

> Histórico cronológico das normas e atos que impactam o acompanhamento.
> Atualizar a cada rodada do monitor.

## 2026

### DD/MM/AAAA — [Nome do ato] ⭐ NOVO
- **Fonte:** [Diário Oficial / portal oficial] | [data de publicação]
- **Escopo:** [resumo em uma ou duas linhas]
- **Classificação:** CRÍTICO | RELEVANTE | INFORMATIVO
- **Impacto:** [o que muda na prática]
- **A validar:** [o que ainda precisa de confirmação na fonte, se houver]

---
```

## Boas práticas

- **Mais recente no topo.** Cada rodada acrescenta a entrada nova logo abaixo do
  cabeçalho do ano, sem apagar as anteriores.
- **Uma entrada por ato.** Se uma rodada encontrar três atos, são três entradas.
- **Honestidade sobre a incerteza.** Use o campo "A validar" sempre que o dado não
  estiver confirmado na fonte oficial. É melhor registrar a dúvida do que um
  número que aparenta firmeza que não tem.
- **Sem dado de terceiro.** O registro acompanha a legislação, não casos. Não
  inclua nomes, CNPJs ou números de clientes.
