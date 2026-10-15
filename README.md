# VerificarSite — Consulta de informações sobre sites

Aplicação web construída com **Python, Flask e Selenium** para consultar informações sobre uma URL em um serviço externo e exibir o resultado em uma interface simples.

> **Importante:** esta aplicação não realiza uma auditoria independente de segurança nem garante que um site seja confiável. As informações vêm de um serviço de terceiros e podem estar indisponíveis ou desatualizadas.

## Tecnologias

- **Python** — lógica e execução da aplicação.
- **Flask** — servidor web local e renderização da interface.
- **Selenium + Google Chrome** — automação de navegador e consulta ao serviço.
- **HTML e CSS** — formulário e exibição dos resultados.

## Como funciona

1. O usuário informa uma URL na interface local.
2. O servidor Flask inicia o Chrome com Selenium.
3. O navegador automatizado acessa o serviço externo `siteconfiavel.com.br` e envia a URL.
4. A aplicação tenta extrair o texto apresentado e exibi-lo na página.

O projeto depende da estrutura HTML desse serviço externo. **Mudanças na página podem quebrar a consulta**, mesmo que o servidor Flask continue funcionando.

## Executar localmente

### 1. Pré-requisitos

- Python 3 instalado.
- Google Chrome instalado.
- Acesso à Internet para a consulta externa.
- Um ChromeDriver compatível com o Chrome, quando a configuração do Selenium exigir um driver disponível localmente.

### 2. Clonar o repositório

```bash
git clone https://github.com/DanielHSec/VerificarSite.git
cd VerificarSite
```

### 3. Criar ambiente virtual

**Windows (PowerShell):**

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

**Linux/macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

### 4. Iniciar

```bash
python app.py
```

Depois, acesse **http://localhost:5000** e informe uma URL para consulta.

O servidor atual usa `0.0.0.0:5000`, o que pode disponibilizar a aplicação na rede local. **Use apenas em ambiente de desenvolvimento confiável; não publique essa versão diretamente na Internet.**

## Estrutura do projeto

```text
VerificarSite/
├── app.py                 # Aplicação Flask + automação Selenium
├── requirements.txt       # Dependências Python instaláveis
├── requiriments.txt       # Arquivo legado; prefira requirements.txt
├── templates/
│   └── index.html         # Formulário e apresentação do resultado
└── static/
    └── style.css          # Estilização
```

## Limitações conhecidas

- A aplicação consulta **um serviço de terceiros**, sem garantia de disponibilidade, precisão ou permanência da interface.
- A extração usa um caminho XPath específico e uma espera fixa; por isso, podem ocorrer resultados vazios ou erros.
- O tempo de resposta depende do navegador, da rede e do serviço consultado.
- O projeto não fornece API pública, análise de malware, varredura de vulnerabilidades nem classificação verificável de risco.
- URLs maliciosas devem ser avaliadas com cuidado; **não use o resultado como única base para decidir se um endereço é seguro**.

## Possíveis melhorias

- Validar e normalizar a URL informada.
- Tratar tempo limite, falhas da consulta e mudanças no HTML com mensagens específicas.
- Substituir a espera fixa por condições explícitas do Selenium.
- Criar testes automatizados de componentes independentes do serviço externo.
- Separar automação, lógica e interface em módulos menores.

## Autor

Desenvolvido por **Daniel Abreu**.

[GitHub](https://github.com/DanielHSec) · [Portfólio](https://daniel-abreu.vercel.app/) · [LinkedIn](https://www.linkedin.com/in/danielhenrique-cybersecurity/)
