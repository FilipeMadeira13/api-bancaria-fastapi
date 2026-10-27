# Backlog priorizado — API Bancária FastAPI

Data da análise: 27/10/2026.

## Objetivo e limites

Aperfeiçoar o projeto como API de estudo e portfólio, preservando inicialmente uma conta por usuário, depósitos, saques e extrato. Essa é uma premissa de planejamento; uso com dinheiro real exigiria uma análise de requisitos própria.

Este documento registra planejamento, não autorização para implementar, instalar ferramentas, alterar Git ou publicar serviços. As tarefas serão realizadas pelo autor com apoio de mentoria, uma por vez.

## Evidências usadas

Análise estática de `app/`, `tests/`, migrações Alembic, dependências, Docker, scripts, workflows e documentação. Nenhum teste, build, migração ou serviço foi executado nesta análise. Os riscos de execução abaixo precisam ser reproduzidos nos testes indicados.

| Referência | Observação verificável no código |
| --- | --- |
| E1 — `alembic/env.py`, `alembic/versions/` | Importação de `sqlite_url`, inexistente em `app/infra/database.py`; duas revisões executam `drop_table` em `upgrade`; metadados não têm importação explícita dos modelos. |
| E2 — `app/domain/models.py`, `app/routers/transaction.py` | Valores monetários em `float`; saldo lido, alterado em memória e gravado sem controle explícito de concorrência. |
| E3 — `app/domain/models.py`, `app/routers/account.py` | Regra de uma conta por usuário conferida na rota, sem unicidade de `Account.user_id` no banco. |
| E4 — `app/core/config.py`, `.env.example`, Compose | Chaves de autenticação de exemplo ou padrão; inicialização não exige substituição. |
| E5 — `app/domain/schemas.py`, `app/core/security.py` | Cadastro aceita strings sem limites; bcrypt recebe UTF-8 diretamente; autenticação captura `JWTError`, mas não cobre explicitamente erros de validação do conteúdo de `sub`. |
| E6 — `app/main.py` | Duas definições de `custom_openapi`; a última marca inclusive registro/login como protegidos; CORS permite qualquer origem com credenciais. |
| E7 — `tests/` | Sete funções de teste; faltam cenários de autenticação inválida, isolamento entre usuários, concorrência e migrações. Fixtures usam estado global e não restauram os overrides. |
| E8 — dependências e CI | `httpx`, `pytest-cov`, Black e flake8 não estão declarados em `pyproject.toml`; `requirements.txt` diverge dele e não contém Uvicorn, Alembic ou pytest-cov; CI altera dependências com `poetry add`. |
| E9 — Docker e workflows | Docker instala com `poetry install --no-dev`; README é excluído do contexto, mas declarado no pacote; Compose usa `curl` sem instalação explícita na imagem e monta um arquivo SQLite local. Build não validado. |
| E10 — `app/routers/statement.py` | Consulta sem paginação, ordenação explícita ou validação de intervalo invertido. |
| E11 — documentação | Há alegações de prontidão e testes passando sem evidência desta análise; `IMPLEMENTATION_SUMMARY.md` orienta push para main; links locais para LICENSE e CODE_OF_CONDUCT.md não têm arquivos correspondentes na listagem examinada. |
| E12 — workflows de segurança/publicação | Falhas são ignoradas em verificações; auditoria de dependências não instala explicitamente o conjunto da aplicação; publicação acompanha push na main e não depende dos jobs de qualidade do outro workflow. |

## Como usar

- **P0:** corrigir a base e os riscos de integridade antes de ampliar funcionalidades.
- **P1:** tornar o MVP confiável, verificável e fácil de operar localmente.
- **P2:** evolução posterior, após estabilização.
- **Tamanho P:** uma sessão focada; **M:** duas a três sessões, como aproximação para aprendizado. Se ultrapassar isso, dividir antes de implementar.
- **Dependências:** IDs que precisam estar concluídos. “Nenhuma” permite iniciar isoladamente; a execução ainda deve ocorrer uma tarefa por vez.
- **RED → GREEN → REFACTOR:** escrever um teste que falha, implementar o mínimo para passar e melhorar a organização preservando o comportamento. Aplicar às mudanças de comportamento; documentação usa revisão e verificações manuais.
- Todos os itens começam pendentes. A ordem numérica é a sequência sugerida, respeitando dependências.

## P0 — Base e integridade

### B01 — Alinhar dependências de execução e desenvolvimento

- **Status:** concluída em 27/10/2026, por indicação do autor. Instalação e testes previstos abaixo não foram verificados nesta sessão.
- **Objetivo/evidência:** tornar instalações reproduzíveis a partir de uma fonte definida (E8).
- **Tamanho:** P. **Dependências:** nenhuma.
- **Aceitação:** definir `pyproject.toml` como fonte; declarar ferramentas de teste e qualidade em grupo de desenvolvimento; sincronizar lock e exportação para pip. Uvicorn, Alembic, httpx e pytest-cov devem estar no conjunto apropriado. Não atualizar versões sem necessidade desta tarefa.
- **Teste:** em ambientes descartáveis, instalar pelo caminho Poetry e pelo caminho pip documentados; verificar dependências e importar a aplicação; coletar os testes e reconhecer a opção `--cov` em ambos.
- **Risco:** regenerar o lock pode alterar versões transitivas; revisar o diff.

### B02 — Isolar o banco e o ciclo de vida dos testes

- **Objetivo/evidência:** impedir que testes dependam de estado global ou alcancem `bank.db` (E7).
- **Tamanho:** P. **Dependências:** B01.
- **Aceitação:** cada teste começa sem dados; cliente e engine são encerrados; overrides são restaurados; inicialização da aplicação usa apenas recursos de teste, inclusive ao exercitar o lifespan.
- **Teste:** criar usuário em um teste e confirmar ausência no seguinte; executar a suíte duas vezes; verificar que o arquivo de banco local não foi criado nem alterado.
- **Risco:** SQLite em memória e event loops precisam compartilhar recursos de forma compatível.

### B03 — Corrigir configuração e carregamento do Alembic

- **Objetivo/evidência:** permitir que Alembic carregue configurações e modelos (E1).
- **Tamanho:** P. **Dependências:** B01.
- **Aceitação:** usar a mesma configuração de URL da aplicação; remover importação inexistente; registrar explicitamente os modelos nos metadados. Não executar as revisões destrutivas nesta tarefa.
- **Teste:** carregar o ambiente Alembic em contexto de teste; confirmar URL temporária e presença de `user`, `account` e `transaction` nos metadados.
- **Risco:** URL errada pode direcionar comandos ao banco pessoal; testes devem usar caminho temporário explícito.

### B04 — Definir estratégia para o histórico de migrações

- **Objetivo/evidência:** decidir como reparar as revisões que excluem tabelas (E1).
- **Tamanho:** P. **Dependências:** nenhuma.
- **Aceitação:** registrar decisão com duas situações: projeto sem revisões aplicadas fora do ambiente local e banco existente com dados/revisões aplicadas. Confirmar a situação real com o autor; especificar estratégia, preservação de dados e recuperação. Não reescrever revisões já distribuídas sem decisão explícita.
- **Teste:** revisar a estratégia usando exemplos de banco vazio e banco com usuário, conta, saldo e histórico; explicar o destino de cada dado.
- **Risco:** histórico real de ambientes não foi verificado; essa informação é necessária antes de B05.

### B05 — Implementar o caminho seguro de migração

- **Objetivo/evidência:** criar/atualizar o esquema sem exclusão acidental (E1).
- **Tamanho:** M. **Dependências:** B02, B03, B04.
- **Aceitação:** implementar somente a estratégia aprovada em B04; banco vazio chega ao esquema atual; caminho de atualização preserva dados existentes; documentar restauração quando downgrade não for seguro.
- **Teste:** integração em bancos temporários: criação do zero, repetição de `upgrade head` e atualização de uma cópia representativa com conferência de usuários, saldos e transações. Nunca usar o banco pessoal como fixture.
- **Risco:** alterações SQLite podem exigir recriação controlada de tabelas.

### B06 — Exigir uma chave JWT configurada

- **Objetivo/evidência:** evitar execução silenciosa com chave conhecida (E4).
- **Tamanho:** P. **Dependências:** B02.
- **Aceitação:** ausência de chave e valores de exemplo são rejeitados com mensagem clara; `.env.example`, Compose e testes orientam configuração explícita; nenhum segredo real é versionado.
- **Teste:** configuração sem chave, com marcador de exemplo e com chave de teste válida; erro não revela o valor recebido.
- **Risco:** scripts que copiam `.env.example` deixam de iniciar até a configuração da chave; mensagem deve orientar essa etapa.

### B07 — Definir e aplicar representação monetária exata

- **Objetivo/evidência:** remover cálculo monetário com `float` (E2).
- **Tamanho:** M. **Dependências:** B02, B05.
- **Aceitação:** para o escopo de uma moeda com duas casas, usar centavos inteiros na persistência e conversão decimal exata nas bordas; migrar saldo e transações juntos; documentar limites, serialização e regra para dados antigos com frações de centavo. Rejeitar entradas novas com mais de duas casas, não finitas ou fora dos limites.
- **Teste:** depósitos de 0,10 e 0,20 resultam exatamente em 0,30; saque de todo o saldo zera a conta; zero, negativos, terceira casa decimal, limites e valores não finitos são rejeitados; migração preserva exemplos de valores válidos.
- **Risco:** contrato JSON e conversão de valores antigos precisam de decisão explícita antes da implementação.

### B08 — Garantir uma conta por usuário no banco

- **Objetivo/evidência:** sustentar a regra mesmo com solicitações simultâneas (E3).
- **Tamanho:** P. **Dependências:** B02, B05.
- **Aceitação:** unicidade em `Account.user_id`; verificar duplicatas antes da migração, sem apagar dados automaticamente; conflito retorna erro de domínio consistente e faz rollback da sessão.
- **Teste:** duas sessões tentam criar conta para o mesmo usuário: apenas uma persiste; usuários diferentes criam suas contas; sessão volta a ser utilizável após conflito.
- **Risco:** bancos existentes podem conter duplicatas que exigem decisão do autor.

### B09 — Proteger saldo contra operações simultâneas

- **Objetivo/evidência:** evitar perda de depósitos e saques incompatíveis com o saldo (E2).
- **Tamanho:** M. **Dependências:** B07.
- **Aceitação:** atualização atômica ou controle explícito de versão compatível com SQLite; saque condiciona débito a saldo suficiente; saldo e transação são confirmados juntos; conflitos têm tratamento definido.
- **Teste:** com sessões/conexões independentes e SQLite temporário em arquivo, disparar dois saques de 80 sobre saldo 100: apenas um tem sucesso; dois depósitos simultâneos não se perdem; saldo corresponde ao histórico. Sincronizar as tentativas para exercitar a disputa, sem depender apenas de pausas.
- **Risco:** teste com uma sessão compartilhada não demonstra proteção contra concorrência real.

### B10 — Verificar atomicidade de saldo e histórico

- **Objetivo/evidência:** comprovar que falhas não deixam uma operação parcial (E2).
- **Tamanho:** P. **Dependências:** B09.
- **Aceitação:** falha durante a persistência desfaz tanto saldo quanto lançamento; erro não retorna sucesso e sessão é revertida corretamente.
- **Teste:** provocar falha controlada entre atualização e conclusão; consultar por nova sessão e verificar saldo original e ausência da transação; próxima operação válida funciona.
- **Risco:** verificar apenas o objeto em memória pode esconder persistência parcial.

## P1 — MVP confiável

### B11 — Cobrir isolamento entre usuários

- **Objetivo/evidência:** demonstrar que cada token opera apenas sua conta (E7).
- **Tamanho:** P. **Dependências:** B02.
- **Aceitação:** dois usuários com contas e movimentos distintos não consultam nem alteram dados um do outro; nenhuma resposta expõe hash de senha.
- **Teste:** usar token A e depois B em conta, depósito, saque e extrato; comparar saldos e IDs em sessão independente.
- **Risco:** helpers com e-mail fixo impedem testar dois usuários distintos.

### B12 — Tratar autenticação inválida de forma previsível

- **Objetivo/evidência:** completar validação e cobertura de tokens/credenciais (E5, E7).
- **Tamanho:** P. **Dependências:** B02.
- **Aceitação:** rotas protegidas respondem 401 para token ausente, expirado, adulterado, sem `sub`, com `sub` de tipo inválido ou usuário inexistente; manter cabeçalho Bearer; login inválido não distingue e-mail de senha incorretos.
- **Teste:** parametrizar esses casos nas rotas protegidas; incluir senha errada e usuário inexistente; não usar espera real para expiração.
- **Risco:** erros de validação do payload podem escapar como 500.

### B13 — Validar nome, e-mail e senha no cadastro/login

- **Objetivo/evidência:** rejeitar dados inválidos antes de persistir ou chamar bcrypt (E5).
- **Tamanho:** P. **Dependências:** B02.
- **Aceitação:** definir e documentar limites de nome/senha e normalização de e-mail; nome em branco e e-mail inválido retornam 422; limite bcrypt é considerado em bytes UTF-8, inclusive no login; nunca truncar senha silenciosamente.
- **Teste:** espaços no nome, e-mail inválido, limites de senha e caracteres multibyte próximos/acima de 72 bytes; respostas não expõem senha/hash.
- **Risco:** normalização pode produzir colisões entre e-mails existentes; verificar antes de migrar dados.

### B14 — Tratar conflito de cadastro no banco

- **Objetivo/evidência:** evitar erro interno quando dois cadastros disputam o mesmo e-mail; hoje há consulta prévia e unicidade no modelo.
- **Tamanho:** P. **Dependências:** B13.
- **Aceitação:** capturar especificamente conflito de unicidade, executar rollback e responder com o mesmo contrato do cadastro duplicado; outros erros não são mascarados.
- **Teste:** cadastro duplicado sequencial e concorrente por sessões distintas; apenas um usuário persiste; sessão se recupera após conflito.
- **Risco:** capturar exceções genéricas pode ocultar falhas de infraestrutura.

### B15 — Completar testes das regras de transação

- **Objetivo/evidência:** cobrir entradas inválidas e limites já esperados no MVP (E7).
- **Tamanho:** P. **Dependências:** B07.
- **Aceitação:** testar tipo desconhecido, campo obrigatório ausente, operação sem conta, saque igual ao saldo e saldo insuficiente; nenhum caso rejeitado altera saldo ou histórico.
- **Teste:** tabela parametrizada com status HTTP e estado persistido esperado; manter testes de depósito/saque existentes.
- **Risco:** conferir apenas a resposta permite regressões no estado do banco.

### B16 — Corrigir documentação de autenticação OpenAPI

- **Objetivo/evidência:** eliminar definição duplicada e marcar corretamente rotas públicas (E6).
- **Tamanho:** P. **Dependências:** B02.
- **Aceitação:** uma única definição; `/auth/register` e `/auth/login` públicos no esquema; rotas protegidas usam esquema coerente com OAuth2/Bearer real; autorização funciona no Swagger.
- **Teste:** verificar `/openapi.json` por rota; realizar cadastro, login e chamada protegida no Swagger em ambiente local.
- **Risco:** alterar só o esquema pode esconder divergência com a autenticação real.

### B17 — Configurar origens CORS

- **Objetivo/evidência:** definir quais interfaces web podem chamar a API (E6). CORS é a política de acesso aplicada pelo navegador.
- **Tamanho:** P. **Dependências:** B02.
- **Aceitação:** origens permitidas vêm da configuração; padrão sem liberação ampla; credenciais e métodos têm configuração coerente com o cliente escolhido.
- **Teste:** requisições OPTIONS de origem permitida e não permitida; conferir cabeçalhos; chamadas sem origem continuam funcionando.
- **Risco:** CORS não substitui autenticação e não bloqueia clientes fora do navegador.

### B18 — Tornar datas e ordenação do extrato determinísticas

- **Objetivo/evidência:** corrigir ambiguidade dos filtros e ordem dos resultados (E10).
- **Tamanho:** P. **Dependências:** B02.
- **Aceitação:** definir UTC, tratamento de datas sem fuso, limites inclusivos e ordem por timestamp mais ID; intervalo invertido retorna 422; nenhum teste depende do horário real.
- **Teste:** registros com horários fixos; limites exatos, fuso diferente representando o mesmo instante, intervalo invertido, resultado vazio e timestamps iguais.
- **Risco:** SQLite pode devolver datas sem informação de fuso; normalizar também a saída.

### B19 — Paginar o extrato

- **Objetivo/evidência:** limitar consulta e resposta conforme o histórico cresce (E10).
- **Tamanho:** P. **Dependências:** B18.
- **Aceitação:** adicionar `limit` com teto e `offset` não negativo, mantendo resposta em lista nesta primeira versão; aplicar filtros e ordem antes de limitar; documentar valores padrão.
- **Teste:** páginas de conjunto fixo sem repetição/omissão, última página, filtro combinado e parâmetros inválidos.
- **Risco:** offset pode deslocar resultados se houver novas operações entre páginas; registrar limitação.

### B20 — Consultar a própria conta e saldo

- **Objetivo:** permitir consultar saldo sem criar conta ou executar transação.
- **Tamanho:** P. **Dependências:** B07, B11.
- **Aceitação:** `GET /account/` devolve conta do usuário autenticado com representação monetária definida; sem conta retorna 404 e sem token retorna 401.
- **Teste:** saldo inicial, após depósito/saque, ausência de conta e isolamento entre usuários.
- **Risco:** reusar resposta deve preservar o contrato definido em B07.

### B21 — Tornar testes e qualidade obrigatórios na CI

- **Objetivo/evidência:** fazer a integração contínua reprovar regressões verificáveis (E8).
- **Tamanho:** P. **Dependências:** B01, B02.
- **Aceitação:** workflow instala dependências declaradas sem `poetry add`; executa testes, cobertura e verificações de código escolhidas sem ignorar falhas; Makefile usa ferramentas instaladas sem instalar durante lint/format; compatibilidade é verificada nas versões Python declaradas.
- **Teste:** introduzir falha temporária em teste e em lint numa branch descartável; ambos reprovam; reverter e obter execução verde antes de integrar.
- **Risco:** regras de estilo novas podem exigir tarefa separada; não misturar reformatação ampla.

### B22 — Auditar dependências e segredos de forma verificável

- **Objetivo/evidência:** corrigir verificações que hoje ignoram falhas ou não examinam explicitamente a aplicação (E12).
- **Tamanho:** P. **Dependências:** B01.
- **Aceitação:** auditoria usa dependências efetivamente resolvidas do projeto; configurar scanner e baseline quando aplicável; exceções são explícitas e justificadas; logs não revelam segredos.
- **Teste:** verificar reprovação usando segredo fictício e uma fixture de relatório com vulnerabilidade conhecida; remover fixtures da execução normal; falha da ferramenta também reprova.
- **Risco:** ferramentas podem exigir rede ou credenciais; instalação/configuração será autorizada na execução da tarefa.

### B23 — Validar construção e inicialização da imagem

- **Objetivo/evidência:** corrigir o caminho de build realmente executado (E9).
- **Tamanho:** P. **Dependências:** B01, B06.
- **Aceitação:** comando de instalação compatível com Poetry escolhido; arquivos exigidos pelo empacotamento presentes; dependências de execução disponíveis; imagem inicia como usuário sem privilégios usando chave de teste explícita.
- **Teste:** construir imagem limpa e executar chamada HTTP de smoke test; conferir usuário e ausência de `.env`/banco pessoal no conteúdo da imagem.
- **Risco:** build pode exigir rede; falha exata ainda não foi reproduzida.

### B24 — Separar verificação de processo e banco

- **Objetivo:** substituir `/docs` como indicador de saúde por endpoints específicos.
- **Tamanho:** P. **Dependências:** B02.
- **Aceitação:** endpoint de processo responde sem consultar banco; endpoint de prontidão consulta banco e retorna 503 quando indisponível; respostas não incluem configuração ou detalhes internos.
- **Teste:** processo saudável, banco disponível e falha simulada no banco; confirmar que verificação de processo permanece disponível.
- **Risco:** tratar exceções não pode transformar falha de banco em falso sucesso.

### B25 — Corrigir persistência e healthcheck no Compose

- **Objetivo/evidência:** tornar ambiente local repetível sem depender de arquivo previamente criado ou de curl ausente (E9).
- **Tamanho:** P. **Dependências:** B05, B06, B23, B24.
- **Aceitação:** usar diretório/volume gravável para SQLite; healthcheck usa recurso presente e endpoint de prontidão; inicialização aplica migrações de forma explícita; documentar hot reload como opção de desenvolvimento.
- **Teste:** subir em ambiente descartável sem `bank.db`, cadastrar e movimentar conta, reiniciar sem excluir volume e confirmar dados; verificar saúde do serviço.
- **Risco:** permissões do volume para usuário sem privilégios e inicialização simultânea.

### B26 — Usar migrações como fonte do esquema

- **Objetivo/evidência:** impedir que `create_all` na inicialização oculte migrações ausentes (E1 e `app/main.py`).
- **Tamanho:** P. **Dependências:** B05, B25.
- **Aceitação:** fluxo normal exige migração explícita; inicialização não cria nem altera tabelas silenciosamente; testes de integração exercitam esquema migrado. `create_all` pode permanecer apenas onde justificado em testes unitários.
- **Teste:** banco vazio sem migração não é considerado pronto; após migração, fluxo cadastro → conta → depósito → extrato funciona; início da aplicação não muda o esquema.
- **Risco:** scripts locais precisam passar a orientar/aplicar a etapa de migração explicitamente.

### B27 — Condicionar publicação às verificações

- **Objetivo/evidência:** evitar publicação independente do resultado da CI (E12).
- **Tamanho:** P. **Dependências:** B21, B22, B23.
- **Aceitação:** publicação manual e explicitamente aprovada, executando somente após qualidade/build aprovados para a mesma revisão; condições de secrets usam mecanismo suportado; notificação reflete resultado real; remover simulação de deploy apresentada como sucesso.
- **Teste:** validação estática do YAML e simulação sem push/deploy; comprovar por estrutura do workflow que falhas bloqueiam publicação e ausência de secrets é tratada.
- **Risco:** validação completa de publicação exige credenciais e aprovação específica; esta tarefa não autoriza publicar.

### B28 — Alinhar guias com o fluxo validado

- **Objetivo/evidência:** tornar instalação e contribuição confiáveis, removendo afirmações sem comprovação (E11).
- **Tamanho:** P. **Dependências:** B21, B25, B26.
- **Aceitação:** revisar README, guia rápido, resumo e contribuição; documentar chave, migrações, dinheiro e comandos reais; substituir instrução de push na main por branch/PR; resolver links de licença/conduta após decisão do autor; métricas indicam comando e evidência, sem alegação genérica de prontidão.
- **Teste:** seguir um caminho de instalação em ambiente descartável e executar o fluxo principal; conferir links locais e comparar endpoints/exemplos com OpenAPI.
- **Risco:** escolha de licença deve ser feita pelo autor, não inferida pelo agente.

## P2 — Melhorias posteriores

### B29 — Evitar duplicação de transações por repetição de requisição

- **Objetivo:** adicionar idempotência: repetir a mesma operação com a mesma chave não movimenta o saldo novamente.
- **Tamanho:** M. **Dependências:** B09, B10.
- **Aceitação:** chave opcional por usuário, persistida atomicamente com a operação; repetição devolve o mesmo resultado; mesma chave com payload diferente retorna conflito; definir retenção antes de implementar.
- **Teste:** repetição sequencial e simultânea gera um lançamento; payload diferente conflita; usuários distintos podem usar a mesma chave.
- **Risco:** guardar a chave fora da transação de banco deixa janela para duplicação.

### B30 — Limitar tentativas de login

- **Objetivo:** reduzir abuso e custo de autenticação.
- **Tamanho:** P. **Dependências:** B12.
- **Aceitação:** limites configuráveis e resposta 429 com orientação de nova tentativa; definir chave de limitação e política para proxy; documentar escopo de um processo caso armazenamento seja local.
- **Teste:** tentativas até o limite, bloqueio, liberação com relógio controlado e independência entre clientes conforme a política; não usar esperas reais.
- **Risco:** identificação incorreta de IP atrás de proxy e bloqueio indevido de redes compartilhadas.

### B31 — Adicionar logs de diagnóstico sem dados sensíveis

- **Objetivo:** localizar falhas por identificador da requisição.
- **Tamanho:** P. **Dependências:** B12.
- **Aceitação:** registrar rota, status, duração e identificador; não registrar token, senha, hash ou corpo financeiro completo; erros internos preservam contexto no servidor sem expor detalhes na resposta.
- **Teste:** capturar logs de sucesso e falha; verificar correlação e ausência de dados sensíveis em cadastro, login e transação.
- **Risco:** logs SQL e cabeçalhos podem vazar dados mesmo quando o log principal está correto.

### B32 — Extrair somente a regra de movimentação para um serviço

- **Objetivo:** facilitar testes e manutenção da lógica financeira, hoje na rota, sem reestruturar todo o projeto.
- **Tamanho:** P. **Dependências:** B09, B10, B15.
- **Aceitação:** rota cuida de HTTP e serviço coordena a operação financeira; contratos, atomicidade e comportamento permanecem iguais; evitar interfaces/camadas sem necessidade demonstrada.
- **Teste:** executar os testes de regressão financeira existentes e verificar contratos HTTP antes/depois.
- **Risco:** mudar onde ocorre o commit pode quebrar atomicidade; manter um único responsável.

### B33 — Avaliar índice do extrato com dados representativos

- **Objetivo:** melhorar consulta apenas após medir necessidade.
- **Tamanho:** P. **Dependências:** B18, B19, B05.
- **Aceitação:** criar conjunto sintético, registrar plano/tempo da consulta e avaliar índice por conta, timestamp e ID; adicionar migração somente se houver benefício demonstrado; registrar custo de escrita.
- **Teste:** comparar plano e medições antes/depois com o mesmo conjunto; confirmar que filtros e páginas retornam resultados idênticos. Não fixar limiar de tempo dependente da máquina em teste unitário.
- **Risco:** volume pequeno pode produzir medição enganosa.

### B34 — Validar backup e restauração local

- **Objetivo:** comprovar recuperação do histórico e saldo.
- **Tamanho:** P. **Dependências:** B05, B25.
- **Aceitação:** documentar cópia consistente do SQLite e restauração em destino separado; indicar revisão Alembic esperada; não sobrescrever o banco original.
- **Teste:** gerar dados sintéticos, copiar, restaurar em arquivo temporário e comparar usuários, contas, saldo, transações e revisão.
- **Risco:** copiar arquivo enquanto há escrita pode produzir backup inconsistente; escolher método apropriado.

## Marcos e dependências

| Marco | Critério de conclusão |
| --- | --- |
| M1 — Base de verificação | B01–B05 concluídos: dependências, testes isolados e caminho de migração seguro. |
| M2 — Integridade financeira | M1 e B06–B15 concluídos: configuração explícita, dinheiro exato, concorrência, atomicidade e isolamento verificados. |
| M3 — MVP aperfeiçoado | M2 e B16–B28 concluídos: contrato documentado, extrato limitado, CI e execução local verificáveis. |
| M4 — Evolução | Escolher B29–B34 conforme necessidade, sem bloquear o MVP. |

Trilhas que podem ser planejadas independentemente após B02: configuração/autenticação (B06, B11–B14), contrato HTTP (B16–B19) e saúde (B24). A trilha financeira depende do caminho de migrações. A publicação depende das verificações e não é parte automática da implementação.

## Fora do escopo inicial

Múltiplas contas por usuário, transferências, webhooks, dashboard, aplicativo móvel, OAuth2 para terceiros, infraestrutura de métricas e troca para PostgreSQL ficam para descoberta posterior. Múltiplas contas contradizem a regra atual; PostgreSQL exige validar driver, migrações e concorrência no novo banco. Nenhum desses itens deve ser iniciado apenas por constar nas sugestões antigas do README.

## Critério comum de conclusão de uma tarefa

1. Trabalhar em branch apropriada quando a implementação for autorizada; não fazer commit direto em main/master.
2. Para comportamento, demonstrar primeiro o caso de falha e depois o caso corrigido; o autor escreve testes e implementação com apoio de mentoria.
3. Registrar comandos e resultados realmente observados; checks não executados ficam explícitos.
4. Conferir diff, escopo e documentação afetada; não misturar limpeza ampla ou novas funcionalidades.
5. Revisar brevemente o aprendizado e aguardar escolha da próxima tarefa.

## Próxima microtarefa sugerida

Começar por **B01**: comparar dependências declaradas com imports e comandos do projeto; propor os grupos de execução e desenvolvimento antes de instalar ou alterar versões. É uma tarefa pequena e independente que habilita a verificação das seguintes.

Pergunta para revisão ativa ao concluí-la: **por que uma instalação pode executar a API e ainda assim não conseguir rodar os testes ou gerar cobertura?**
