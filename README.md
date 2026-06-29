# Conferência Automática de Recebimentos Médicos (Promédica)

Aplicativo macOS para comparação automática de agendas médicas e demonstrativos de pagamentos, gerando agendas conferidas com marcação de procedimentos pagos.

## Funcionalidades

- ✅ Parser especializado para PDFs de agendas Promédica
- ✅ Extração de dados de demonstrativos de pagamento
- ✅ Correspondência inteligente de pacientes e procedimentos
- ✅ Normalização e fuzzy matching de nomes
- ✅ Marcação de PDFs com riscos em procedimentos pagos
- ✅ Interface moderna com CustomTkinter
- ✅ Relatórios em Excel (resultado e não encontrados)
- ✅ Logs detalhados em tempo real

## Requisitos

- macOS 11.0+
- Python 3.12+
- Apple Silicon ou Intel

## Instalação

```bash
git clone https://github.com/yuricostaf-hue/conferencia-recebimentos.git
cd conferencia-recebimentos
pip install -r requirements.txt
```

## Uso

```bash
python app.py
```

## Build para macOS

```bash
pyinstaller pyinstaller.spec
```

O aplicativo será gerado em `dist/ConferenciaRecebimentos.app`

## Estrutura do Projeto

```
conferencia/
├── app.py                 # Ponto de entrada
├── core/
│   ├── agenda_parser.py     # Parser das agendas
│   ├── demonstrativo_parser.py  # Parser dos demonstrativos
│   ├── matcher.py           # Correspondência de dados
│   ├── pdf_marker.py        # Marcação dos PDFs
│   ├── normalizer.py        # Normalização de dados
│   ├── models.py            # Dataclasses
│   └── logger.py            # Sistema de logs
├── gui/
│   ├── main_window.py       # Janela principal
│   ├── worker.py            # Worker para processamento
│   └── settings.py          # Configurações da GUI
├── assets/                  # Ícones e recursos
├── tests/                   # Testes unitários
├── requirements.txt         # Dependências
├── pyproject.toml          # Configuração do projeto
└── pyinstaller.spec        # Configuração PyInstaller
```

## Documentação

Ver documentação completa em `docs/` (em desenvolvimento).

## Testes

```bash
pytest tests/
```

## Licença

Proprietário - Promédica
