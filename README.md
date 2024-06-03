# Ticket Tracker

Um dos problemas enfrentados por quem gosta de frequentar festas está na hora de competir com outras pessoas na hora de comprar o seu ingresso. As organizadoras de eventos costumam compartilhar em suas redes sociais quando os ingressos serão lançados, mas mesmo se antecipando não há garantia que você será mais rápido do que o outro. Um dos fatores determinantes para saber quem ganha essa corrida está na velocidade de se clicar nos botões - então por que não automatizar isso?

Esse projeto é um MVP de um serviço de automatização de compra de ingressos com dois arquivos com funções diferentes:

- `buy_ticket.py`: Dado informações de uma festa,faz a compra antes de outras pessoas, garantindo que se pegue os primeiros lotes (mais baratos)
- `track_tickets.ipynb`: A partir de informações de um site de festas cria um json com todas as festas com ingressos à venda

## Índice

- [Ticket Tracker](#ticket-tracker)
  - [Índice](#índice)
  - [Uso](#uso)
  - [`buy_ticket.py`](#buy_ticketpy)

## Uso

Em um ambiente virtual, baixe as dependências com o comando

```bash
pip install -r requirements.txt
```

Crie um arquivo `.env` seguindo as informações de `.env.example` (dados de login e senha da Blacktag)

## `buy_ticket.py`

Ao rodar o arquivo, é pedido do usuário que ele forneça as seguintes informações da festa de interesse:

1.  Nome do evento
2.  Data de abertura da venda dos ingressos
3.  Horário de abertura da venda dos ingressos

A partir disso, o programa espera até a hora de abertura de ingressos (menos um delta de tempo de segurança) e faz requests seguidos até o evento abrir para venda. Caso isso aconteça, o programa faz automaticamente a seleção de ingressos e o processo de autenticação até o momento de pedido do token por WhatsApp. Feito isso, é só copiar e colar o token que o seu ingresso já está garantido pela plataforma.

Limitações:

- Só funciona para a plataforma Blacktag
- Escolhe-se o primeiro ingresso disponível
- Compra de apenas um ingresso

Possíveis próximos passos:

- Integração com nuvem usando cronjob do script ao invés de usar sleep
- Programação da compra do ingresso com Telegram
- Usar uma maneira mais inteligente de selecionar o ingresso esecolhido (priorizar primeiro lote / promocional)
- Opção de escolha de número de ingressos comprados
