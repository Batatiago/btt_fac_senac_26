#!/usr/bin/env bash
set -euo pipefail

# Script para automatizar a instalação e a personalização do terminal.
# Ele instala Zsh, Oh My Zsh, plugins, o tema awesomepanda, a fonte Fira Code Nerd Font
# e, quando executado no WSL, também instala o Python 3.14.
# A ideia é evitar repetir o mesmo processo manualmente depois de formatar o sistema.

readonly OH_MY_ZSH_DIR="${HOME}/.oh-my-zsh"
readonly CUSTOM_DIR="${ZSH_CUSTOM:-${OH_MY_ZSH_DIR}/custom}"
readonly FONT_DIR="${HOME}/.local/share/fonts"
readonly AUTOSUGGESTIONS_DIR="${CUSTOM_DIR}/plugins/zsh-autosuggestions"
readonly SYNTAX_HIGHLIGHTING_DIR="${CUSTOM_DIR}/plugins/zsh-syntax-highlighting"
readonly ZSHRC_FILE="${HOME}/.zshrc"
readonly ZSHRC_BACKUP="${HOME}/.zshrc.backup-before-terminal-script"
readonly FIRACODE_ARCHIVE_URL="https://github.com/ryanoasis/nerd-fonts/releases/latest/download/FiraCode.zip"
readonly PYTHON314_VERSION="3.14.3"
readonly PYTHON314_TARBALL_URL="https://www.python.org/ftp/python/${PYTHON314_VERSION}/Python-${PYTHON314_VERSION}.tgz"
readonly PYTHON314_PREFIX="/opt/python-${PYTHON314_VERSION}"
readonly PYTHON314_BIN="${PYTHON314_PREFIX}/bin/python3.14"

log() {
  printf '\n[INFO] %s\n' "$1"
}

warn() {
  printf '\n[AVISO] %s\n' "$1"
}

error() {
  printf '\n[ERRO] %s\n' "$1" >&2
}

require_command() {
  local cmd="$1"
  if ! command -v "$cmd" >/dev/null 2>&1; then
    error "Comando obrigatório não encontrado: $cmd"
    exit 1
  fi
}

run_as_root() {
  if [[ "${EUID}" -eq 0 ]]; then
    "$@"
  else
    sudo "$@"
  fi
}

package_manager() {
  if command -v apt-get >/dev/null 2>&1; then
    printf 'apt'
  elif command -v dnf >/dev/null 2>&1; then
    printf 'dnf'
  elif command -v pacman >/dev/null 2>&1; then
    printf 'pacman'
  elif command -v zypper >/dev/null 2>&1; then
    printf 'zypper'
  elif command -v apk >/dev/null 2>&1; then
    printf 'apk'
  else
    error 'Nenhum gerenciador de pacotes suportado foi encontrado.'
    exit 1
  fi
}

is_wsl() {
  if [[ -r /proc/sys/kernel/osrelease ]] && grep -qiE '(microsoft|wsl)' /proc/sys/kernel/osrelease; then
    return 0
  fi

  if [[ -r /proc/version ]] && grep -qi microsoft /proc/version; then
    return 0
  fi

  return 1
}

install_packages() {
  local manager
  manager="$(package_manager)"

  log "Instalando dependências com $manager"

  case "$manager" in
    apt)
      run_as_root apt-get update
      run_as_root apt-get install -y zsh git curl wget unzip fontconfig
      ;;
    dnf)
      run_as_root dnf install -y zsh git curl wget unzip fontconfig
      ;;
    pacman)
      run_as_root pacman -Sy --noconfirm zsh git curl wget unzip fontconfig
      ;;
    zypper)
      run_as_root zypper --non-interactive install zsh git curl wget unzip fontconfig
      ;;
    apk)
      run_as_root apk add --no-cache zsh git curl wget unzip fontconfig
      ;;
  esac
}

install_python314_build_dependencies() {
  local manager
  manager="$(package_manager)"

  log "Instalando dependências de compilação do Python ${PYTHON314_VERSION} com $manager"

  case "$manager" in
    apt)
      run_as_root apt-get install -y \
        build-essential \
        libssl-dev \
        zlib1g-dev \
        libbz2-dev \
        libreadline-dev \
        libsqlite3-dev \
        libffi-dev \
        liblzma-dev \
        tk-dev \
        uuid-dev \
        libgdbm-dev \
        libncursesw5-dev \
        xz-utils
      ;;
    dnf)
      run_as_root dnf install -y \
        gcc \
        make \
        openssl-devel \
        zlib-devel \
        bzip2-devel \
        readline-devel \
        sqlite-devel \
        libffi-devel \
        xz-devel \
        tk-devel \
        gdbm-devel \
        ncurses-devel \
        libuuid-devel
      ;;
    pacman)
      run_as_root pacman -Sy --noconfirm \
        base-devel \
        openssl \
        zlib \
        bzip2 \
        readline \
        sqlite \
        libffi \
        xz \
        tk \
        gdbm \
        ncurses \
        util-linux-libs
      ;;
    zypper)
      run_as_root zypper --non-interactive install \
        gcc \
        make \
        openssl-devel \
        zlib-devel \
        libbz2-devel \
        readline-devel \
        sqlite3-devel \
        libffi-devel \
        xz-devel \
        tk-devel \
        gdbm-devel \
        ncurses-devel \
        libuuid-devel
      ;;
    apk)
      run_as_root apk add --no-cache \
        build-base \
        openssl-dev \
        zlib-dev \
        bzip2-dev \
        readline-dev \
        sqlite-dev \
        libffi-dev \
        xz-dev \
        tk-dev \
        gdbm-dev \
        ncurses-dev \
        util-linux-dev
      ;;
  esac
}

install_python314_on_wsl() {
  local temp_dir

  if ! is_wsl; then
    return
  fi

  if command -v python3.14 >/dev/null 2>&1; then
    warn 'Python 3.14 já está disponível no PATH. Pulando esta etapa.'
    return
  fi

  if [[ -x "$PYTHON314_BIN" ]]; then
    warn "Python ${PYTHON314_VERSION} já foi instalado em ${PYTHON314_PREFIX}."
  else
    install_python314_build_dependencies

    temp_dir="$(mktemp -d)"
    trap 'rm -rf "$temp_dir"' RETURN

    log "Baixando o código-fonte do Python ${PYTHON314_VERSION}"
    curl -fL "$PYTHON314_TARBALL_URL" -o "$temp_dir/Python-${PYTHON314_VERSION}.tgz"

    log "Compilando e instalando o Python ${PYTHON314_VERSION} em ${PYTHON314_PREFIX}"
    tar -xzf "$temp_dir/Python-${PYTHON314_VERSION}.tgz" -C "$temp_dir"
    (
      cd "$temp_dir/Python-${PYTHON314_VERSION}"
      ./configure --prefix="$PYTHON314_PREFIX" --enable-optimizations
      make -j"$(nproc)"
      run_as_root make altinstall
    )
  fi

  mkdir -p "${HOME}/.local/bin"
  ln -sfn "$PYTHON314_BIN" "${HOME}/.local/bin/python3.14"

  if [[ ":${PATH}:" != *":${HOME}/.local/bin:"* ]]; then
    warn 'Adicione $HOME/.local/bin ao PATH para usar python3.14 sem informar o caminho completo.'
  fi
}

install_oh_my_zsh() {
  if [[ -d "$OH_MY_ZSH_DIR" ]]; then
    warn 'Oh My Zsh já está instalado. Pulando esta etapa.'
    return
  fi

  log 'Instalando Oh My Zsh em modo não interativo'
  RUNZSH=no CHSH=no KEEP_ZSHRC=yes \
    sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
}

clone_or_update() {
  local repo_url="$1"
  local destination="$2"

  if [[ -d "$destination/.git" ]]; then
    log "Atualizando $(basename "$destination")"
    git -C "$destination" pull --ff-only
  else
    log "Clonando $(basename "$destination")"
    git clone --depth=1 "$repo_url" "$destination"
  fi
}

install_plugins() {
  mkdir -p "$CUSTOM_DIR/plugins"

  clone_or_update https://github.com/zsh-users/zsh-autosuggestions "$AUTOSUGGESTIONS_DIR"
  clone_or_update https://github.com/zsh-users/zsh-syntax-highlighting "$SYNTAX_HIGHLIGHTING_DIR"
}

install_fonts() {
  local temp_dir
  temp_dir="$(mktemp -d)"
  mkdir -p "$FONT_DIR"

  log 'Baixando Fira Code Nerd Font'
  curl -fL "$FIRACODE_ARCHIVE_URL" -o "$temp_dir/FiraCode.zip"

  log 'Extraindo Fira Code Nerd Font'
  unzip -o "$temp_dir/FiraCode.zip" -d "$FONT_DIR" >/dev/null
  rm -rf "$temp_dir"

  if command -v fc-cache >/dev/null 2>&1; then
    log 'Atualizando cache de fontes'
    fc-cache -f "$FONT_DIR"
  else
    warn 'fc-cache não foi encontrado. Talvez seja preciso reiniciar a sessão para detectar as fontes.'
  fi
}

backup_zshrc() {
  if [[ -f "$ZSHRC_FILE" && ! -f "$ZSHRC_BACKUP" ]]; then
    cp "$ZSHRC_FILE" "$ZSHRC_BACKUP"
    log "Backup criado em $ZSHRC_BACKUP"
  fi
}

write_zshrc() {
  backup_zshrc

  log 'Escrevendo configuração padrão do .zshrc'
  cat > "$ZSHRC_FILE" <<'ZSHRC'
export ZSH="$HOME/.oh-my-zsh"

ZSH_THEME="awesomepanda"

plugins=(
  git
  colored-man-pages
  zsh-autosuggestions
  zsh-syntax-highlighting
)

export PATH="$HOME/.local/bin:$PATH"

source "$ZSH/oh-my-zsh.sh"

# Aliases úteis para o dia a dia.
alias ll='ls -lah'
alias gs='git status'
alias gc='git commit'
alias gp='git push'
ZSHRC
}

change_default_shell() {
  local zsh_path
  zsh_path="$(command -v zsh)"

  if [[ "${SHELL:-}" == "$zsh_path" ]]; then
    warn 'Zsh já é o shell padrão deste usuário.'
    return
  fi

  log "Definindo $zsh_path como shell padrão"
  chsh -s "$zsh_path"
}

show_next_steps() {
  cat <<MESSAGE

Configuração finalizada.

Próximos passos:
1. Feche e abra o terminal novamente.
2. No emulador de terminal, selecione a fonte "FiraCode Nerd Font" ou "FiraCode Nerd Font Mono".
3. Se estiver no WSL, confirme se o Windows Terminal também está configurado para usar a Fira Code Nerd Font.
4. O Python ${PYTHON314_VERSION} fica disponível em ${PYTHON314_BIN} quando a instalação ocorre no WSL.
5. Se quiser personalizar mais, edite o arquivo ~/.zshrc.
MESSAGE
}

main() {
  install_packages

  require_command git
  require_command curl
  require_command tar
  require_command unzip

  install_python314_on_wsl
  install_oh_my_zsh
  install_plugins
  install_fonts
  write_zshrc
  change_default_shell
  show_next_steps
}

main "$@"
