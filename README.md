# Monitor da Reforma Tributária

Skill para o Claude que acompanha as atualizações normativas da Reforma
Tributária brasileira (CBS, IBS, Imposto Seletivo). Em vez de visitar dezenas de
sites por semana, você pede uma rodada e o assistente faz a varredura nas fontes
oficiais, cruza com o seu histórico e reporta o que mudou, separando norma
publicada de notícia.

Pensada para advogados, contadores e empresas que precisam acompanhar a transição
2026–2033 sem virar a noite lendo Diário Oficial.

## O que ela faz

- Varre as fontes oficiais (Diário Oficial da União, Receita Federal, Comitê
  Gestor do IBS, Planalto, Ministério da Fazenda).
- Confere os parâmetros críticos (alíquotas de referência, cronograma, fatores
  setoriais, Imposto Seletivo, Split Payment, Simples Nacional).
- Classifica cada novidade em CRÍTICO, RELEVANTE ou INFORMATIVO.
- Mantém um registro datado das mudanças (changelog), só com informação pública.
- Pode rodar de forma agendada, semanal ou quinzenal.

## O que ela NÃO faz

- Não processa dados de clientes (nomes, CNPJs, faturamento, SPED, DRE).
- Não pede nem guarda senhas, tokens ou credenciais.
- Não dá parecer jurídico ou contábil, não afirma alíquota sem fonte e não
  promete economia.

## Como instalar

1. Baixe o arquivo `monitor-reforma-tributaria.skill` deste repositório.
2. No Claude (Cowork/desktop), use a opção de instalar skill e selecione o
   arquivo `.skill`. Como alternativa, copie a pasta da skill para o diretório de
   skills do seu ambiente.

Depois de instalada, é só pedir: "roda o monitor da reforma tributária".

## Estrutura

```
monitor-reforma-tributaria/
├── SKILL.md                         protocolo principal
├── references/
│   ├── fontes_oficiais.md           onde buscar
│   ├── parametros_criticos.md       o que monitorar
│   ├── changelog_modelo.md          modelo do registro
│   └── automacao_agendada.md        como agendar
├── README.md
└── LICENSE
```

## Privacidade e segurança

Esta skill trabalha só com informação pública (atos e normas oficiais). Ela não
coleta nem armazena dados pessoais ou de empresas, e o registro de acompanhamento
guarda apenas a legislação. Mantenha qualquer análise de cliente fora deste fluxo.

## Aviso

Ferramenta de apoio ao acompanhamento normativo. Não substitui parecer jurídico
ou contábil. A leitura da norma na fonte oficial e a decisão final são sempre do
profissional que a utiliza.

## Licença

MIT — veja o arquivo `LICENSE`. Sinta-se à vontade para usar, adaptar e
compartilhar.
