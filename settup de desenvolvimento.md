#Instala WSL - wsl --install

#Instala ZSH - sudo apt install zsh -y

#Definir zsh como shell default - chsh -s $(which zsh)

#Instalar OH-MY-ZSH! - sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

#Via ( nano ~/.zshrc ) definir tema awesomepada e instalar zinit:

ZINIT_HOME="${XDG_DATA_HOME:-${HOME}/.local/share}/zinit/zinit.git"
[ ! -d $ZINIT_HOME ] && mkdir -p "$(dirname $ZINIT_HOME)"
[ ! -d $ZINIT_HOME/.git ] && git clone https://github.com/zdharma-continuum/zinit.git "$ZINIT_HOME"
source "${ZINIT_HOME}/zinit.zsh"

#Instalar os plugins (copiar no fim do arquivo .zsh.rc via nano) -

zinit light zsh-users/zsh-autosuggestions
zinit light zdharma-continuum/fast-syntax-highlighting
zinit load zdharma-continuum/history-search-multi-wordu u

#Instalar Python3.14 ->

1º sudo add-apt-repository ppa:deadsnakes/ppa
2º sudo apt update && sudo apt upgrade
3º sudo apt install python3.14-full

#Definir python3.14 padrão ->

sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.14 10
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 100
sudo update-alternatives --config python3

#Configurações Git/GitHub ->

git config --global user.name "Tiago de Andrade Lima"
git config --global user.email "tiago.andrade.lima@gmail.com"

ssh-keygen -t ed25519-sk -C "tiago.andrade.lima@gmail.com"
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
cat ~/.ssh/id_ed25519.pub

#Instalar LLM Local - Ollama ->

sudo curl -fsSL https://ollama.com/install.sh | sh
ollama run gemma4:31b

# Install using npm

npm install -g @openai/codex ou {

# Clone the repository and navigate to the root of the Cargo workspace.

git clone https://github.com/openai/codex.git
cd codex/codex-rs

# Install the Rust toolchain, if necessary.

curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
source "$HOME/.cargo/env"
rustup component add rustfmt
rustup component add clippy

# Install helper tools used by the workspace justfile:

cargo install just

# Optional: install nextest for the `just test` helper

cargo install --locked cargo-nextest

# Build Codex.

cargo build

# Launch the TUI with a sample prompt.

cargo run --bin codex -- "explain this codebase to me"

# After making changes, use the root justfile helpers (they default to codex-rs):

just fmt
just fix -p <crate-you-touched>

# Run the relevant tests (project-specific is fastest), for example:

cargo test -p codex-tui

# If you have cargo-nextest installed, `just test` runs the test suite via nextest:

just test

# Avoid `--all-features` for routine local runs because it increases build

# time and `target/` disk usage by compiling additional feature combinations.

# If you specifically want full feature coverage, use:

cargo test --all-features
}
# Adiciona o ollama ao codex
ollama launch codex --model gemma4
