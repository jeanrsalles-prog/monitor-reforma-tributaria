# Rodar o monitor de forma agendada

A skill funciona sob demanda (você pede, ela roda). Se quiser que ela rode sozinha
em intervalos regulares, há duas formas, conforme a ferramenta que você usa.

## No Claude (Cowork / desktop) — tarefa agendada

Se o seu ambiente tiver agendamento de tarefas, crie uma tarefa que rode o monitor
na cadência desejada (por exemplo, toda segunda de manhã). O prompt da tarefa pode
ser simples:

```
Rodar o monitor da Reforma Tributária. Buscar novidades das últimas duas semanas
nas fontes oficiais, comparar com o meu registro de acompanhamento e reportar o
que mudou, com classificação de impacto. Não atualizar nenhum arquivo sem a minha
confirmação.
```

Sugestão de cadência: semanal ou quinzenal. A transição da reforma tem janelas em
que muita coisa sai de uma vez (períodos de regulamentação) e janelas calmas.

## Onde houver conector de e-mail

Se o ambiente tiver um conector de e-mail, dá para pedir que a tarefa agendada
deixe um **rascunho** de resumo na sua caixa, em vez de enviar sozinha. Assim você
revisa antes de qualquer coisa sair. Peça explicitamente "deixe como rascunho, não
envie".

## Cuidado de segurança

A tarefa agendada deve fazer só o acompanhamento normativo. Não configure a
automação para tocar em bases de clientes, nem para enviar nada automaticamente
sem revisão. O objetivo é te poupar a varredura manual, não automatizar decisão.
