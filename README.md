# Teste Abstract - API de Relatórios

Este teste é o projeto de uma API desenvolvida em **Flask**. Ela processa e gera relatórios de insights de anúncios provenientes de diferentes plataformas pré-selecionadas. A API consome dados da API original, enviada no sumário do teste da **Stract**, padroniza as informações e gera relatórios em CSV.

## Tecnologias Utilizadas  

- **Python 3.12**
- **Flask**
- **Requests**
- **Poetry** (Gerenciamento de dependências)

## Estrutura do Projeto  

```
/api
 .. root
 ┣ api
 ┃ ┣  __init__.py
 ┃ ┣  config.py
 ┃ ┣  insights_processor.py
 ┃ ┣  routes.py
 ┃ ┣  services.py
 ┃ ┗  utils.py
 ┣ tests
 ┃ ┣  __init__.py
 ┃ ┣  test_routes.py
 ┃ ┣  test_services.py
 ┃ ┣  test_insights_processor.py
 ┃ ┗  test_utils.py
 ┣  main.py
 ┣  pyproject.toml
 ┣  .flaskenv
 ┣  .gitignore
 ┣  README.md
 ┗  poetry.lock

```

## Configuração  

### 1. Clonando o Repositório  
```sh
git clone https://github.com/pgpostit/api_test_stract
```

### 2. Instalando Dependências  
Certifique-se de ter **Poetry** instalado e execute:  
```sh
poetry install
```

### 3. (Opcional) Configurando Variáveis de Ambiente  
Crie um arquivo **.env** com as seguintes variáveis, caso queira escolher o host e a porta:  
```
HOST=127.0.0.1
PORT=5000
```

### 4. Rodando o Servidor  
```sh
poetry run python main.py
```
A API, por padrão, estará disponível em `http://127.0.0.1:5000/`.
Também pode-se utilizar:
```sh
flask run
```
Para rodar em modo de desenvolvimento

---

## API Original (Stract)  

A API consome dados da **API do Stract** (`https://sidebar.stract.to/api`), que fornece insights de anúncios em diversas plataformas. Algumas informações recebidas podem precisar de normalização e formatação, para serem salvas de forma agrupada.

**Atenção:** A API do Stract, em caso de erro, retorna um JSON com `"error": "invalid request"` e código **200**, mas a API deste projeto ajusta para **400**.

---

## Regras de Negócio  

- **Normalização de Campos:** Diferentes nomes de atributos, em endpoints que agrupam diferentes plataformas, são padronizados. Exemplo:
  - `"adName"` (GA4) → `"ad_name"`
  - `"cost_per_click"` (TikTok) → `"cpc"`
- **Preenchimento de Valores Faltantes:** Se o `"cpc"` não estiver disponível, ele será calculado como `spend / clicks`.
- **Colunas Unificadas:** Campos com o mesmo significado são agrupados na mesma coluna.
- **Soma de Valores para Relatórios Resumidos:** No `/geral/resumo`, valores numéricos são somados.

---

## **Rotas da API**  

### **Rota Principal**  
| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/` | Retorna informações sobre o desenvolvedor e as rotas disponíveis, como pedido no teste. |

Exemplo de resposta:
```json
{
    "developer": {
        "name": "Paulo S. Garcia",
        "email": "pgarcia2022@gmail.com",
        "linkedin": "https://linkedin.com/in/paulogarcia01"
    },
    "endpoints": {
        "general_data": "http://127.0.0.1:5000/geral",
        "general_summary": "http://127.0.0.1:5000/geral/resumo",
        "platform_data": "http://127.0.0.1:5000/<platform>",
        "platform_summary": "http://127.0.0.1:5000/<platform>/resumo"
    }
}
```

---

### **Rotas para Relatórios de Plataforma Específica**  

| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/<platform>` | Obtém os anúncios de uma plataforma específica |
| `GET` | `/<platform>/resumo` | Obtém um resumo de métricas por usuário da plataforma |

Exemplo:
```sh
GET http://127.0.0.1:5000/meta_ads
```

---

### **Rotas para Relatórios de Todas as Plataformas**  

| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/geral` | Obtém todos os anúncios de todas as plataformas |
| `GET` | `/geral/resumo` | Obtém um resumo de métricas por usuário de cada a plataforma |

Exemplo:
```sh
GET http://127.0.0.1:5000/geral
```

---

## **Testes Unitários**  

Os testes foram implementados para validar a API.  

### **Rodando os Testes**  
Para executar os testes:
```sh
pytest tests/
```

### **Exemplo de Teste** (`tests/test_services.py`)
```python
import pytest
from api.services import StractAPIService

@pytest.fixture
def service():
    return StractAPIService()

def test_fetch_platforms(service, requests_mock):
    mock_response = {"platforms": [{"name": "Meta Ads"}]}
    requests_mock.get(service.BASE_URL + "/platforms", json=mock_response)

    response = service.fetch_platforms()
    assert response == mock_response
```

---

## **Possíveis Melhorias Futuras**
 - Retornar na chamada da API ambos os formatos, CSV e JSON, talvez por escolha do usuário
 - Permitir ao usuário uma quantidade de itens retornados por chamada, enquanto a API trabalha, por baixo dos panos, no service, para obedecer esse limite ao buscar da API externa
 - Adicionar logs para melhor monitoramento das chamadas à API  
 - Implementar cache para otimizar requisições repetitivas  
 - Criar interface web para visualização dos relatórios  

---

## **Autor**  
Desenvolvido por **Paulo S. Garcia**  
 **Email:** pgarcia2022@gmail.com  
 **LinkedIn:** [linkedin.com/in/paulogarcia01](https://linkedin.com/in/paulogarcia01)  
