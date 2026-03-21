# Repositorio de Exercícios

Meu repo de exercícios da Faculdade-Senac.

## Script para instalar e customizar o terminal Linux

Se você quer evitar reinstalar manualmente o seu ambiente sempre que formatar o sistema, este repositório agora inclui um script Bash que automatiza a configuração básica do terminal.

### O que o script faz

O arquivo `scripts/install-zsh-terminal.sh`:

- instala `zsh`, `git`, `curl`, `wget`, `unzip` e `fontconfig`;
- detecta quando está sendo executado no **WSL**;
- instala o **Python 3.14.3** no WSL a partir do código-fonte oficial do Python;
- instala o **Oh My Zsh** em modo não interativo;
- ativa os plugins `git`, `colored-man-pages`, `zsh-autosuggestions` e `zsh-syntax-highlighting`;
- ativa o tema **awesomepanda** do próprio Oh My Zsh;
- baixa e instala a fonte **FiraCode Nerd Font**;
- cria backup do `~/.zshrc` antes de sobrescrever a configuração;
- define o `zsh` como shell padrão do usuário.

### Como usar

```bash
chmod +x scripts/install-zsh-terminal.sh
./scripts/install-zsh-terminal.sh
```

### Como estudar e adaptar o script

A melhor forma de aprender é dividir o arquivo em blocos:

1. **Detecção do sistema:** as funções `package_manager` e `is_wsl` identificam o ambiente e o gerenciador de pacotes disponível.
2. **Instalação de dependências:** a função `install_packages` instala os pacotes básicos usados pelo restante da automação.
3. **Python no WSL:** as funções `install_python314_build_dependencies` e `install_python314_on_wsl` instalam as bibliotecas de compilação e fazem o build do Python 3.14.3 a partir do fonte oficial.
4. **Automação do Oh My Zsh:** a função `install_oh_my_zsh` executa a instalação sem abrir shell interativo.
5. **Plugins:** a função `install_plugins` faz clone ou atualização dos plugins desejados.
6. **Fontes:** a função `install_fonts` baixa e extrai a Fira Code Nerd Font.
7. **Configuração do Zsh:** a função `write_zshrc` escreve um `~/.zshrc` inicial com o tema `awesomepanda`, os plugins pedidos e `$HOME/.local/bin` no `PATH`.

### Dicas de personalização

Você pode adaptar esse script para o seu gosto alterando:

- os plugins no bloco `plugins=(...)` dentro do `.zshrc`;
- o valor de `ZSH_THEME`;
- os aliases criados automaticamente;
- a versão configurada em `PYTHON314_VERSION`;
- a URL da fonte baixada em `FIRACODE_ARCHIVE_URL`;
- os pacotes extras que você usa no dia a dia, como `fzf`, `bat`, `eza` ou `tmux`.

### Importante

- O script pode pedir sua senha de `sudo` para instalar pacotes e para o `make altinstall` do Python no WSL.
- Em alguns terminais, a fonte precisa ser selecionada manualmente após a instalação.
- Depois de executar o script no WSL, escolha `FiraCode Nerd Font` nas preferências do **Windows Terminal**.
- O Python 3.14.3 instalado no WSL fica em `/opt/python-3.14.3/bin/python3.14` e um link simbólico é criado em `~/.local/bin/python3.14`.
- Se você já tiver um `~/.zshrc`, o backup será salvo como `~/.zshrc.backup-before-terminal-script`.
