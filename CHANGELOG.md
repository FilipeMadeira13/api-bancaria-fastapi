# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
e este projeto segue [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-04-06

### Added
- ✅ Autenticação JWT com registro e login
- ✅ Gerenciamento de contas bancárias
- ✅ Transações (depósitos e saques)
- ✅ Extrato com filtros por tipo e data
- ✅ Validações de saldo e valores
- ✅ API assíncrona com FastAPI
- ✅ Banco SQLite com async support
- ✅ Testes automatizados (7 testes)
- ✅ Documentação Swagger/OpenAPI
- ✅ Docker e docker-compose
- ✅ CI/CD com GitHub Actions
- ✅ Estrutura de projeto com clean architecture
- ✅ Type hints e Pydantic v2
- ✅ Alembic para migrações

### Changed

### Deprecated

### Removed

### Fixed

### Security
- Senhas com bcrypt (hash seguro)
- JWT token com expiração configurável
- CORS middleware (permitindo todas as origens por padrão - alterar em produção)
- Validação de entrada com Pydantic

---

## Planejamento de Versões Futuras

### v1.1.0 (Próximo)
- [ ] Suporte a múltiplas contas por usuário
- [ ] Rate limiting nos endpoints
- [ ] Paginação avançada no extrato
- [ ] Webhook para notificações
- [ ] PostgreSQL como opção de banco

### v2.0.0
- [ ] Dashboard com dados agregados
- [ ] Gráficos e relatórios
- [ ] API para terceiros (OAuth2)
- [ ] Mobile App support
- [ ] Observabilidade (Prometheus/Grafana)

---

**[Unreleased]** - Changes since last release
**[1.0.0]** - 2026-04-06 - Initial Release
