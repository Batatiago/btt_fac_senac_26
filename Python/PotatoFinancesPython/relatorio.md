# 📄 Relatório do Projeto — Potato Finances

## 1. Visão Geral do Projeto

O **Potato Finances** é um sistema desktop de gestão financeira pessoal desenvolvido em **Python**. Ele permite ao usuário registrar, visualizar, editar e excluir transações financeiras (receitas, despesas e investimentos), com um painel visual (dashboard) que exibe saldo, totais por categoria e um gráfico de evolução mensal.

### Tecnologias Utilizadas

| Tecnologia | Função no Projeto |
|---|---|
| **Python 3** | Linguagem de programação principal |
| **CustomTkinter** | Biblioteca para criar a interface gráfica (GUI) com visual moderno e tema escuro |
| **MySQL** | Banco de dados relacional que armazena as transações |
| **mysql-connector-python** | Conector que permite o Python se comunicar com o MySQL |
| **Pandas** | Biblioteca de manipulação de dados, usada para organizar as transações em tabelas (DataFrames) |
| **Matplotlib** | Biblioteca de gráficos, usada para desenhar o gráfico de linhas no dashboard |
| **Pillow (PIL)** | Biblioteca de processamento de imagens, usada para carregar e exibir o logo do app |

---

## 2. Estrutura de Arquivos do Projeto

```
PotatoFinancesPython/
├── main.py          → Interface gráfica (telas, botões, gráfico, tabela)
├── database.py      → Comunicação com o banco de dados MySQL (CRUD)
├── logo.png         → Imagem do logo exibida no topo da aplicação
└── relatorio.md     → Este relatório
```

| Arquivo | Responsabilidade |
|---|---|
| `main.py` | Contém toda a **interface gráfica** do sistema: a janela principal, os cards de resumo (saldo, receitas, despesas, investimentos), o gráfico, a lista de transações, e o popup de criação/edição. |
| `database.py` | Contém as **funções de acesso ao banco de dados** — as 4 operações do CRUD (Create, Read, Update, Delete). Isola toda a lógica de SQL do resto do programa. |
| `logo.png` | Imagem PNG usada como logotipo no canto superior esquerdo da aplicação. |

> **Nota sobre separação de responsabilidades:** O projeto segue uma boa prática chamada **separação de camadas**. O arquivo `database.py` cuida exclusivamente de ler/escrever dados no MySQL, enquanto `main.py` cuida exclusivamente da interface. Isso facilita manutenção e testes.

---

## 3. Arquivo `database.py` — Camada de Dados

### 3.1 Imports

```python
import mysql.connector
import pandas as pd
```

| Import | O que faz | Como é usado |
|---|---|---|
| `mysql.connector` | É o **conector oficial** do MySQL para Python. Ele fornece funções para abrir conexões, executar comandos SQL e receber resultados. | Usado para conectar ao banco, inserir, ler, atualizar e deletar registros da tabela `transacoes`. |
| `pandas as pd` | **Pandas** é uma biblioteca de análise de dados. O alias `pd` é uma convenção da comunidade Python. | Usado na função `ler_transacoes()` para transformar o resultado de uma query SQL diretamente em um **DataFrame** — uma tabela em memória fácil de manipular. |

---

### 3.2 Funções

#### `conectar()`

```python
def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",         
        password="S3nh@mySQL", 
        database="potato_finances"
    )
```

- **O que faz:** Cria e retorna uma **conexão** com o banco de dados MySQL.
- **Como faz:** Chama `mysql.connector.connect()` passando os dados de acesso: o endereço do servidor (`localhost` = máquina local), o usuário (`root`), a senha e o nome do banco (`potato_finances`).
- **Retorna:** Um **objeto de conexão** que as outras funções usam para executar SQLs.
- **Por que é separada:** Evita repetir os dados de conexão em cada função — todas chamam `conectar()`.

---

#### `inserir_transacao(tipo, descricao, valor, data, categoria, forma_pagamento)`

```python
def inserir_transacao(tipo, descricao, valor, data, categoria, forma_pagamento):
    conexao = conectar()
    cursor = conexao.cursor()
    sql = """INSERT INTO transacoes (tipo, descricao, valor, data_transacao, categoria, forma_pagamento) 
             VALUES (%s, %s, %s, %s, %s, %s)"""
    cursor.execute(sql, valores)
    conexao.commit()
```

- **O que faz:** **C (Create)** do CRUD — insere uma nova transação no banco.
- **Parâmetros:**
  - `tipo` → `"Receita"`, `"Despesa"` ou `"Investimento"`
  - `descricao` → texto livre (ex: `"Salário de junho"`)
  - `valor` → número decimal (ex: `1500.00`)
  - `data` → data no formato MySQL `"YYYY-MM-DD"` (ex: `"2026-06-26"`)
  - `categoria` → ex: `"Alimentação"`, `"Transporte"`, `"Salário"`
  - `forma_pagamento` → ex: `"Pix"`, `"Cartão de Crédito"`
- **Como faz:**
  1. Abre uma conexão chamando `conectar()`.
  2. Cria um **cursor** (objeto que executa comandos SQL).
  3. Monta um `INSERT INTO` com **placeholders** `%s` para segurança (evita SQL Injection).
  4. Executa o SQL com os valores passados como parâmetros.
  5. Chama `conexao.commit()` para confirmar a gravação no banco.
- **Tratamento de erro:** Usa `try/except/finally` — se houver erro, imprime uma mensagem e retorna `False`. O `finally` garante que a conexão e o cursor são sempre fechados, mesmo em caso de erro.

---

#### `ler_transacoes()`

```python
def ler_transacoes():
    conexao = conectar()
    df = pd.read_sql("SELECT * FROM transacoes", conexao)
    return df
```

- **O que faz:** **R (Read)** do CRUD — lê todas as transações do banco.
- **Como faz:**
  1. Abre uma conexão.
  2. Usa `pd.read_sql()` do Pandas — essa função executa a query SQL e retorna o resultado diretamente como um **DataFrame** (tabela com colunas e linhas nomeadas).
  3. Se houver erro, retorna um DataFrame vazio (`pd.DataFrame()`).
- **Retorna:** Um DataFrame do Pandas contendo todas as transações.

---

#### `atualizar_transacao(id_transacao, tipo, descricao, valor, data, categoria, forma_pagamento)`

```python
def atualizar_transacao(id_transacao, tipo, descricao, valor, data, categoria, forma_pagamento):
    sql = """UPDATE transacoes 
             SET tipo=%s, descricao=%s, valor=%s, data_transacao=%s, categoria=%s, forma_pagamento=%s 
             WHERE id=%s"""
```

- **O que faz:** **U (Update)** do CRUD — atualiza uma transação existente.
- **Como faz:**
  1. Monta um `UPDATE ... SET ... WHERE id=%s` que altera todos os campos da transação cujo `id` é o informado.
  2. Usa placeholders `%s` para evitar SQL Injection.
  3. Confirma com `commit()`.
- **Diferença para `inserir_transacao`:** Recebe o `id_transacao` como primeiro parâmetro e usa `WHERE id=%s` para modificar apenas o registro correto.

---

#### `deletar_transacao(id_transacao)`

```python
def deletar_transacao(id_transacao):
    sql = "DELETE FROM transacoes WHERE id = %s"
    cursor.execute(sql, (id_transacao,))
```

- **O que faz:** **D (Delete)** do CRUD — remove permanentemente uma transação.
- **Como faz:** Executa `DELETE FROM transacoes WHERE id = %s` com o ID da transação a excluir.
- **Detalhe importante:** `(id_transacao,)` com a vírgula cria uma **tupla de um elemento** — isso é obrigatório porque `cursor.execute()` espera uma sequência, não um valor solto.

---

## 4. Arquivo `main.py` — Interface Gráfica

### 4.1 Imports

```python
import customtkinter as ctk
import database
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image
import os
```

| Import | O que faz | Como é usado no projeto |
|---|---|---|
| `customtkinter as ctk` | Versão moderna e estilizada do Tkinter. Fornece widgets (botões, labels, janelas) com visual dark/light profissional. | Cria **todos** os elementos visuais: janela, botões, labels, frames, popups, campos de texto, menus. |
| `import database` | Importa o **nosso próprio arquivo** `database.py` como um módulo. | Permite chamar as funções CRUD: `database.inserir_transacao()`, `database.ler_transacoes()`, etc. |
| `pandas as pd` | Biblioteca de manipulação de dados tabulares. | Usado para processar e agrupar transações por mês antes de desenhar o gráfico, e para formatar datas. |
| `from datetime import datetime` | Importa a **classe** `datetime` do **módulo** `datetime` (nomes iguais). | Usada para obter a data de hoje (`datetime.today()`) e para converter formatos de data (`strptime` e `strftime`). |
| `matplotlib.pyplot as plt` | Sub-módulo do Matplotlib para criação de gráficos em estilo procedural. | Cria a **figura** e os **eixos** (`fig, ax`) do gráfico de linhas da visão anual. |
| `FigureCanvasTkAgg` | Classe que permite **embutir um gráfico Matplotlib dentro de uma janela Tkinter**. | Renderiza o gráfico como um widget nativo da interface, dentro do `frame_grafico`. |
| `from PIL import Image` | Classe do **Pillow** para abrir e manipular imagens. | Abre o arquivo `logo.png` para exibi-lo no topo da janela. |
| `import os` | Módulo padrão do Python para operações de sistema de arquivos. | Usado para construir o caminho absoluto até o arquivo `logo.png`, independente do diretório de execução. |

---

### 4.2 Configuração Inicial

```python
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

janela = ctk.CTk()
janela.title("Potato Finances")
janela.geometry("1000x800")
```

- `set_appearance_mode("dark")` → Define o tema visual como **escuro** (fundo escuro, textos claros).
- `set_default_color_theme("blue")` → Define azul como cor padrão dos widgets.
- `ctk.CTk()` → Cria a **janela principal** da aplicação.
- `janela.geometry("1000x800")` → Define o tamanho da janela em pixels (largura × altura).

### 4.3 Variáveis Globais

```python
lbl_saldo_valor = None
lbl_receitas_valor = None
lbl_despesas_valor = None
lbl_investimentos_valor = None
```

Essas variáveis guardam **referências** aos labels dos cards do dashboard. São inicializadas como `None` e depois recebem os widgets reais quando os cards são criados. Isso permite que a função `atualizar_dashboard()` atualize os textos desses labels.

```python
CATEGORIAS = ["Geral", "Alimentação", "Transporte", "Moradia", "Lazer", "Saúde", "Educação", "Salário", "Freelance", "Investimento"]
FORMAS_PAGAMENTO = ["Pix", "Cartão de Crédito", "Cartão de Débito", "Dinheiro", "Boleto", "Transferência"]
```

Listas constantes usadas como opções nos menus dropdown do popup de transação.

---

### 4.4 Funções

#### `desenhar_grafico()`

- **O que faz:** Cria o **gráfico de linhas** "Visão Anual" que mostra a evolução de receitas, despesas e investimentos por mês.
- **Como faz, passo a passo:**
  1. **Limpa o frame:** Remove todos os widgets filhos de `frame_grafico` para evitar sobreposição.
  2. **Cria a figura:** `plt.subplots()` cria uma figura Matplotlib com fundo na cor `#2A2D3E` (cinza escuro).
  3. **Configura a aparência:** Define cores dos eixos, bordas e ticks para combinar com o tema escuro.
  4. **Busca os dados:** Chama `database.ler_transacoes()` para obter todas as transações.
  5. **Se não houver dados:** Exibe o texto "Sem transações" centralizado.
  6. **Se houver dados:**
     - Converte a coluna `data_transacao` para o tipo datetime do Pandas.
     - Filtra apenas Receitas, Despesas e Investimentos.
     - Cria uma coluna `mes_ano` formatada como `"MM/YYYY"`.
     - Agrupa por `mes_ano` e `tipo`, somando os valores — usa `unstack()` para pivotar os tipos em colunas.
     - Plota uma **linha** para cada tipo com cores diferentes: verde (receita), vermelho (despesa), roxo (investimento).
     - Adiciona uma **legenda**.
  7. **Embutir na interface:** Usa `FigureCanvasTkAgg` para renderizar o gráfico como widget Tkinter dentro de `frame_grafico`.

---

#### `deletar_item(id_transacao)`

```python
def deletar_item(id_transacao):
    database.deletar_transacao(id_transacao)
    atualizar_dashboard()
```

- **O que faz:** Exclui uma transação e atualiza o dashboard.
- **Como faz:** Chama a função `deletar_transacao()` do `database.py` e depois chama `atualizar_dashboard()` para que os cards, gráfico e tabela reflitam a mudança.

---

#### `abrir_transacao(modo="novo", transacao_id=None, dados=None)`

- **O que faz:** Abre uma **janela popup** para criar uma nova transação ou editar uma existente.
- **Parâmetros:**
  - `modo` → `"novo"` para criar, `"editar"` para modificar uma transação existente.
  - `transacao_id` → O ID da transação a editar (só usado no modo editar).
  - `dados` → Os dados atuais da transação (para preencher os campos no modo editar).
- **Como faz, passo a passo:**
  1. **Cria o popup:** `ctk.CTkToplevel()` cria uma janela secundária acima da principal.
  2. **`popup.grab_set()`** → Torna o popup **modal** — o usuário não pode interagir com a janela principal enquanto o popup estiver aberto.
  3. **Campos do formulário:**
     - **Tipo:** Botão segmentado com opções "Despesa", "Receita", "Investimento".
     - **Descrição:** Campo de texto livre.
     - **Valor:** Campo numérico (aceita vírgula, convertida para ponto internamente).
     - **Data:** Campo de data no formato DD/MM/AAAA (pré-preenchido com a data de hoje se for novo).
     - **Categoria:** Menu dropdown com as opções da lista `CATEGORIAS`.
     - **Forma de Pagamento:** Menu dropdown com as opções da lista `FORMAS_PAGAMENTO`.
  4. **Pré-preenchimento:** Se `dados` não for `None` (modo editar), os campos já vêm preenchidos com os valores atuais.
  5. **Função interna `salvar()`:**
     - Coleta os valores de todos os campos.
     - Converte o valor para `float` (substituindo vírgula por ponto).
     - Converte a data de `DD/MM/AAAA` para `YYYY-MM-DD` (formato MySQL).
     - Se for modo `"novo"`, chama `database.inserir_transacao()`.
     - Se for modo `"editar"`, chama `database.atualizar_transacao()`.
     - Atualiza o dashboard e fecha o popup.

---

#### `desenhar_tabela()`

- **O que faz:** Renderiza a **lista de transações** no painel lateral direito.
- **Como faz:**
  1. **Limpa a lista:** Remove todos os widgets filhos de `frame_lista`.
  2. **Busca os dados:** Chama `database.ler_transacoes()`.
  3. **Ordena:** Ordena por data decrescente (transação mais recente no topo).
  4. **Para cada transação:** Cria uma "linha" visual (`CTkFrame`) contendo:
     - **Botão ✎** (editar) → Abre o popup no modo editar.
     - **Botão X** (excluir) → Chama `deletar_item()`.
     - **Data** formatada como DD/MM/AAAA.
     - **Descrição** do lançamento.
     - **Valor** formatado como `R$ X.XX`.
  5. **Detalhe de empacotamento:** Os botões são empacotados **primeiro** (`side="right"`) para garantir que sempre fiquem visíveis. Os labels são empacotados depois — se faltar espaço, o texto é truncado, mas os botões permanecem acessíveis.

---

#### `atualizar_dashboard()`

- **O que faz:** **Função central** que recalcula todos os valores e redesenha toda a interface.
- **Como faz:**
  1. Chama `database.ler_transacoes()` para obter os dados atualizados.
  2. Calcula os totais:
     - `total_rec` → soma de todas as transações do tipo "Receita".
     - `total_desp` → soma de todas as transações do tipo "Despesa".
     - `total_inv` → soma de todas as transações do tipo "Investimento".
  3. Atualiza os textos dos 4 cards:
     - **Saldo** = Receitas − Despesas − Investimentos.
     - **Receitas**, **Despesas** e **Investimentos** mostram seus totais.
  4. Chama `desenhar_grafico()` para redesenhar o gráfico.
  5. Chama `desenhar_tabela()` para redesenhar a lista de transações.
- **Quando é chamada:** Sempre que uma transação é criada, editada ou excluída.

---

#### `criar_card(pai, titulo, cor)`

```python
def criar_card(pai, titulo, cor):
    card = ctk.CTkFrame(pai, height=100, corner_radius=15, fg_color="#2A2D3E")
    card.pack(side="left", padx=10, expand=True, fill="both")
    ctk.CTkLabel(card, text=titulo).pack(pady=10)
    lbl = ctk.CTkLabel(card, text="R$ 0,00", font=("Arial", 20, "bold"), text_color=cor)
    lbl.pack(pady=10)
    return lbl
```

- **O que faz:** Cria um **card visual** (caixa arredondada) com título e valor.
- **Parâmetros:**
  - `pai` → O frame "pai" onde o card será colocado.
  - `titulo` → Texto do título (ex: "Saldo", "Receitas").
  - `cor` → Cor do texto do valor (verde, vermelho ou roxo).
- **Retorna:** O **label do valor** — para que a função `atualizar_dashboard()` possa atualizar o texto depois.

---

### 4.5 Layout Principal (Montagem da Tela)

O layout é montado de **cima para baixo** usando o gerenciador `pack()`:

```
┌──────────────────────────────────────────────────┐
│  🥔 Potato Finances                  [+ Nova]    │  ← frame_topo
├──────────────────────────────────────────────────┤
│  Saldo  │  Receitas  │  Despesas  │ Investimentos│  ← frame_cards
├────────────────────────┬─────────────────────────┤
│                        │  Data  Descrição  Valor │
│      📈 Gráfico       │  ✎  X   26/06   Salário │  ← area_inferior
│     (Visão Anual)      │  ✎  X   25/06   Aluguel│
│                        │  ✎  X   24/06   Comida │
│   frame_grafico        │     frame_historico     │
└────────────────────────┴─────────────────────────┘
```

#### Carregamento do Logo

```python
logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo.png")
logo_pil = Image.open(logo_path)
logo_ratio = logo_pil.width / logo_pil.height
logo_height = 40
logo_image = ctk.CTkImage(light_image=logo_pil, dark_image=logo_pil, size=(int(logo_height * logo_ratio), logo_height))
```

1. `os.path.abspath(__file__)` → Obtém o caminho absoluto do arquivo `main.py`.
2. `os.path.dirname(...)` → Pega só a pasta (sem o nome do arquivo).
3. `os.path.join(..., "logo.png")` → Junta o caminho da pasta com o nome do arquivo.
4. `Image.open(logo_path)` → Abre a imagem com Pillow.
5. Calcula a proporção (aspect ratio) para não distorcer a imagem ao redimensionar.
6. `ctk.CTkImage(...)` → Converte para o formato que o CustomTkinter aceita, definindo o tamanho final.

---

## 5. Fluxo de Funcionamento

```
INICIALIZAÇÃO
     │
     ▼
 main.py carrega
     │
     ├─ Cria a janela (CTk)
     ├─ Monta o layout (frames, cards, gráfico, lista)
     ├─ Chama atualizar_dashboard()
     │      │
     │      ├─ database.ler_transacoes()
     │      │      └─ Conecta ao MySQL → SELECT * → Retorna DataFrame
     │      │
     │      ├─ Atualiza os valores dos 4 cards
     │      ├─ Chama desenhar_grafico()
     │      └─ Chama desenhar_tabela()
     │
     └─ janela.mainloop()  ← Fica aguardando interações do usuário


USUÁRIO CLICA "+ Nova transação"
     │
     ▼
 abrir_transacao(modo="novo")
     │
     ├─ Abre popup com formulário
     └─ Ao clicar "Salvar":
            ├─ database.inserir_transacao(...)
            │      └─ Conecta ao MySQL → INSERT INTO → commit
            ├─ atualizar_dashboard()  ← Redesenha tudo
            └─ Fecha o popup


USUÁRIO CLICA "✎" (editar)
     │
     ▼
 abrir_transacao(modo="editar", transacao_id=..., dados=...)
     │
     ├─ Abre popup com campos pré-preenchidos
     └─ Ao clicar "Salvar":
            ├─ database.atualizar_transacao(...)
            │      └─ Conecta ao MySQL → UPDATE → commit
            ├─ atualizar_dashboard()
            └─ Fecha o popup


USUÁRIO CLICA "X" (excluir)
     │
     ▼
 deletar_item(id_transacao)
     │
     ├─ database.deletar_transacao(...)
     │      └─ Conecta ao MySQL → DELETE → commit
     └─ atualizar_dashboard()
```

---

## 6. Banco de Dados — Estrutura da Tabela

A tabela `transacoes` no MySQL possui a seguinte estrutura:

| Coluna | Tipo | Descrição |
|---|---|---|
| `id` | INT (PK, AUTO_INCREMENT) | Identificador único de cada transação |
| `tipo` | VARCHAR | "Receita", "Despesa" ou "Investimento" |
| `descricao` | VARCHAR | Descrição livre da transação |
| `valor` | DECIMAL | Valor monetário da transação |
| `data_transacao` | DATE | Data em que a transação ocorreu |
| `categoria` | VARCHAR | Categoria da transação (ex: Alimentação, Salário) |
| `forma_pagamento` | VARCHAR | Forma de pagamento (ex: Pix, Cartão de Crédito) |

---

## 7. Conceitos Importantes Usados no Projeto

### CRUD
O acrônimo CRUD significa as 4 operações básicas de persistência de dados:
- **C**reate → `inserir_transacao()` → `INSERT INTO`
- **R**ead → `ler_transacoes()` → `SELECT *`
- **U**pdate → `atualizar_transacao()` → `UPDATE ... SET`
- **D**elete → `deletar_transacao()` → `DELETE FROM`

### Separação de Camadas
O projeto separa **interface** (`main.py`) e **dados** (`database.py`). Isso significa que poderíamos trocar o MySQL por outro banco (SQLite, PostgreSQL) apenas alterando `database.py`, sem mexer na interface.

### Janela Modal
O `popup.grab_set()` torna o popup "modal", ou seja, bloqueia a interação com a janela principal até que o popup seja fechado. Isso evita conflitos e garante que o usuário complete a ação antes de voltar ao dashboard.

### Tratamento de Erros (try/except/finally)
Todas as funções do `database.py` usam:
- `try` → Tenta executar a operação.
- `except` → Se der erro, captura a exceção e imprime uma mensagem.
- `finally` → **Sempre** executa, mesmo com erro — garante que a conexão com o banco seja fechada, evitando vazamento de recursos.

### SQL Injection — Prevenção
O projeto usa **placeholders** (`%s`) em vez de concatenar strings no SQL. Isso impede que um usuário mal-intencionado injete comandos SQL maliciosos nos campos de texto.

---

## 8. Como Executar o Projeto

### Pré-requisitos
1. **Python 3** instalado.
2. **MySQL** instalado e rodando.
3. Banco de dados `potato_finances` criado com a tabela `transacoes`.
4. Bibliotecas Python instaladas:
   ```
   pip install customtkinter mysql-connector-python pandas matplotlib pillow
   ```

### Execução
```
python main.py
```

---

*Relatório gerado para o projeto Potato Finances — Sistema de Gestão Financeira Pessoal.*
