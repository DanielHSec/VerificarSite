# VerificarSite

**Consulta experimental de informações sobre sites · Python · Flask · Selenium**

[![Python checks](https://github.com/DanielHSec/VerificarSite/actions/workflows/python-checks.yml/badge.svg)](https://github.com/DanielHSec/VerificarSite/actions/workflows/python-checks.yml)
[![MIT License](https://img.shields.io/badge/License-MIT-bd97ff.svg)](LICENSE)

Aplicação web local que envia uma URL pública ao serviço de terceiros [Site Confiável](https://www.siteconfiavel.com.br/) usando automação do Google Chrome e exibe as informações retornadas. Interface redesenhada em preto/violeta e tratamento de falhas mais claro.

> **Atenção:** o projeto **não** executa auditoria de segurança, scanner antimalware ou certificação de confiabilidade. Dados externos podem estar errados, indisponíveis ou desatualizados. **Não use como única fonte para decidir se um endereço é seguro.**

## Recursos

- Formulário responsivo com validação básica de URLs públicas HTTP/HTTPS.
- Bloqueio de entradas com credenciais, esquemas perigosos e endereços internos/reservados.
- Esperas condicionais do Selenium (sem pausa fixa de 10 segundos) e mensagens de erro amigáveis.
- Chrome iniciado apenas durante a consulta; encerramento do driver mesmo em falhas.
- Servidor Flask vinculado a `127.0.0.1` por padrão, sem exposição automática na rede.
- Testes offline de validação de URLs via `unittest` e workflow de checagem no GitHub.

## Instalação

Requer **Python 3.10+**, **Google Chrome** e acesso à Internet. A instalação atual do Selenium pode gerenciar o driver compatível automaticamente; em alguns ambientes é necessário configurá-lo.

```bash
git clone https://github.com/DanielHSec/VerificarSite.git
cd VerificarSite
python -m venv .venv
```

**Windows (PowerShell)**

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

**Linux/macOS**

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

Abra **http://127.0.0.1:5000**.

### Opções de ambiente

| Variável | Padrão | Finalidade |
| :--- | :--- | :--- |
| `VERIFICARSITE_HOST` | `127.0.0.1` | Interface de escuta do Flask. Evite `0.0.0.0` fora de rede confiável. |
| `VERIFICARSITE_PORT` | `5000` | Porta HTTP local. |
| `VERIFICARSITE_HEADLESS` | `0` | Use `1` para tentar o Chrome sem janela gráfica. |

## Como funciona

1. A aplicação normaliza e verifica sintaticamente a URL informada.
2. O Selenium abre exclusivamente o serviço externo de consulta.
3. A URL é enviada ao formulário do serviço de terceiros, que realiza o processamento.
4. O conteúdo textual da página de resultado é exibido ao usuário.

**Privacidade:** não envie URLs com tokens, caminhos privados ou dados confidenciais. A URL é compartilhada com o serviço externo. A validação local é uma proteção básica e não identifica phishing ou malware.

## Testes e qualidade

```bash
python -m unittest discover -s tests -v
python -m compileall -q app.py url_validation.py tests
```

O workflow `.github/workflows/python-checks.yml` automatiza essas verificações em pushes e pull requests. Esses testes **não** acessam nem homologam o serviço externo.

## Organização

```text
app.py                         Flask e integração Selenium
url_validation.py              Normalização e restrições básicas de URL
templates/index.html           Interface acessível em português
static/style.css               Tema responsivo preto/violeta
tests/test_url_validation.py   Testes independentes da rede
.github/workflows/             Verificações automatizadas
requirements.txt               Dependências
```

## Limitações conhecidas

- O serviço consultado é externo e sua estrutura HTML pode mudar sem aviso.
- A disponibilidade do Chrome e da rede afeta o resultado.
- Alguns sites e provedores bloqueiam automação.
- Não há histórico persistido, API pública, autenticação ou garantia de resultado.
- O servidor Flask embutido é para desenvolvimento, não para publicação direta na Internet.

## Autor

**Daniel Abreu** · [Portfólio](https://daniel-abreu.vercel.app/) · [GitHub](https://github.com/DanielHSec)

Licença: [MIT](LICENSE) (mantido o aviso de direitos autorais original).
