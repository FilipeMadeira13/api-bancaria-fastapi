# Guia de Contribuição

Obrigado por considerar contribuir para a API Bancária! Este documento procura tornar o processo de contribuição claro e sem problemas.

## Código de Conduta

Este projeto adota um Código de Conduta que esperamos que todos os colaboradores sigam. Por favor, leia o arquivo [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) para entender as expectativas.

## Como Contribuir

### Reportando Bugs

Antes de criar relatórios de bugs, verifique a lista de issues pois você pode descobrir que não precisa criar um novo. Ao criar um relatório de bug, inclua o máximo de detalhes possível:

* **Use um título descritivo** para identificar o problema
* **Descreva os passos exatos** que reproduzem o problema
* **Forneça exemplos específicos** para demonstrar os passos
* **Descreva o comportamento observado** e **o que esperava ver**
* **Inclua screenshots e GIFs** se possível
* **Mencione sua versão Python e sistema operacional**

### Sugerindo Enhancements

Sugestões de melhorias são sempre bem-vindas! Ao sugerir um enhancement:

* **Use um título descritivo** para a sugestão
* **Forneça uma descrição passo-a-passo** da funcionalidade sugerida
* **Forneça exemplos específicos** para demonstrar a funcionalidade
* **Descreva o comportamento atual** e **o que espera**
* **Explique por quê essa mudança seria benéfica**

### Pull Requests

* Preencha o template de PR quando criar um novo PR
* Siga o guia de estilo Python [PEP 8](https://www.python.org/dev/peps/pep-0008/)
* Inclua testes adequados no seu PR
* Mantenha a cobertura de testes acima de 80%
* Use commits semânticos (feat:, fix:, docs:, etc)

## Processo de Desenvolvimento

### Configurar o Ambiente

```bash
# Clone o repositório
git clone https://github.com/FilipeMadeira13/api-bancaria-fastapi.git
cd api-bancaria-fastapi

# Crie um ambiente virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instale as dependências de desenvolvimento
pip install poetry
poetry install

# Instale pre-commit hooks
pip install pre-commit
pre-commit install
```

### Criar uma Branch

```bash
# Sempre crie uma branch para sua funcionalidade
git checkout -b feature/minha-feature
# ou para bug fix
git checkout -b fix/meu-bug
```

### Fazer Commits

Siga o padrão de commits semânticos:

```
feat: Adiciona nova funcionalidade
fix: Corrige um bug
docs: Altera documentação
style: Altera formatação (sem mudanças de lógica)
refactor: Refatora código (sem alterar funcionalidade)
perf: Melhora de performance
test: Adiciona ou altera testes
chore: Altera build ou ferramentas
```

Exemplo:

```bash
git commit -m "feat: adiciona validação de email ao registro"
```

### Rodar Testes

```bash
# Rode todos os testes
poetry run pytest -v

# Com cobertura
poetry run pytest --cov=app --cov-report=html

# Teste específico
poetry run pytest tests/test_auth.py::test_register_user -v
```

### Verificar Qualidade de Código

```bash
# Formatação com Black
poetry run black app/ tests/

# Lint com Flake8
poetry run flake8 app/ tests/

# Type checking com Mypy (opcional)
poetry run mypy app/

# Todos de uma vez
poetry run pre-commit run --all-files
```

### Enviar seu PR

1. Push sua branch para o repositório
2. Crie um Pull Request no GitHub
3. Preencha o template de PR com informações detalhadas
4. Aguarde feedback dos maintainers

## Padrões de Código

### Python

- Siga [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use [Black](https://github.com/psf/black) para formatted
- Máximo de 88 caracteres por linha
- Type hints quando possível
- Docstrings em formato Google/NumPy

### Exemplo:

```python
def calcular_juros(principal: float, taxa: float, periodo: int) -> float:
    """
    Calcula juros simples.
    
    Args:
        principal: Valor principal em reais
        taxa: Taxa de juros em percentual
        periodo: Período em meses
    
    Returns:
        Valor total com juros
    """
    juros = principal * (taxa / 100) * (periodo / 12)
    return principal + juros
```

### Tests

- Um arquivo de test por módulo
- Nome: `test_<module_name>.py`
- Use fixtures do pytest
- Mocke dependências externas
- Mantenha testes simples e focados

## Estrutura de Testes

```python
def test_sucesso_criar_conta(client):
    """Test: Criar conta com sucesso"""
    # Arrange
    headers = register_and_login(client)
    
    # Act
    response = client.post("/account/", headers=headers)
    
    # Assert
    assert response.status_code == 201
    assert response.json()["balance"] == 0.0
```

## Dúvidas?

Sinta-se livre para abrir uma issue com o label `question` ou me contatar:

- 📧 Email: cfilipemadeira@gmail.com
- 💼 LinkedIn: [Carlos Filipe](https://linkedin.com/in/carlos-filipe-madeira-de-souza-16211922a)

## Obrigado! 🙏

Sua contribuição é muito valiosa! Mesmo correções pequenas, melhorias na documentação ou novos testes são bem-vindos.

---

**Made with ❤️**
