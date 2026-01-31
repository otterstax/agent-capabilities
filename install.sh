#!/bin/bash
#
# OtterStax Skills Installer for Claude Code
# https://github.com/otterstax/claude-skills
#

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_DIR="${HOME}/.claude"
COMMANDS_DIR="${CLAUDE_DIR}/commands"
SKILLS_DIR="${CLAUDE_DIR}/skills"
CONFIG_DIR="${HOME}/.otterstax"

echo -e "${BLUE}"
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║           OtterStax Skills for Claude Code                ║"
echo "║                    Installer v1.0.0                       ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check if Claude Code is available
check_claude() {
    if command -v claude &> /dev/null; then
        echo -e "${GREEN}✓${NC} Claude Code CLI found"
        return 0
    else
        echo -e "${YELLOW}⚠${NC} Claude Code CLI not found in PATH"
        echo "  Commands will be installed but may require Claude Code to use"
        return 0
    fi
}

# Create directories
create_dirs() {
    echo -e "\n${BLUE}Creating directories...${NC}"

    mkdir -p "${COMMANDS_DIR}/data"
    mkdir -p "${COMMANDS_DIR}/infra"
    mkdir -p "${COMMANDS_DIR}/dev"
    mkdir -p "${SKILLS_DIR}/otterstax"
    mkdir -p "${CONFIG_DIR}"

    echo -e "${GREEN}✓${NC} Directories created"
}

# Install commands
install_commands() {
    echo -e "\n${BLUE}Installing commands...${NC}"

    # Data commands
    if [ -d "${SCRIPT_DIR}/commands/data" ]; then
        cp -r "${SCRIPT_DIR}/commands/data/"* "${COMMANDS_DIR}/data/" 2>/dev/null || true
        echo -e "${GREEN}✓${NC} Data commands installed"
    fi

    # Infra commands
    if [ -d "${SCRIPT_DIR}/commands/infra" ]; then
        cp -r "${SCRIPT_DIR}/commands/infra/"* "${COMMANDS_DIR}/infra/" 2>/dev/null || true
        echo -e "${GREEN}✓${NC} Infrastructure commands installed"
    fi

    # Dev commands
    if [ -d "${SCRIPT_DIR}/commands/dev" ]; then
        cp -r "${SCRIPT_DIR}/commands/dev/"* "${COMMANDS_DIR}/dev/" 2>/dev/null || true
        echo -e "${GREEN}✓${NC} Development commands installed"
    fi
}

# Install skills
install_skills() {
    echo -e "\n${BLUE}Installing skills...${NC}"

    if [ -d "${SCRIPT_DIR}/skills/otterstax" ]; then
        cp -r "${SCRIPT_DIR}/skills/otterstax/"* "${SKILLS_DIR}/otterstax/" 2>/dev/null || true
        echo -e "${GREEN}✓${NC} OtterStax skill installed"
    fi
}

# Install Python client
install_client() {
    echo -e "\n${BLUE}Installing Python client...${NC}"

    if [ -f "${SCRIPT_DIR}/scripts/otterstax_client.py" ]; then
        cp "${SCRIPT_DIR}/scripts/otterstax_client.py" "${CONFIG_DIR}/"
        chmod +x "${CONFIG_DIR}/otterstax_client.py"
        echo -e "${GREEN}✓${NC} Python client installed to ${CONFIG_DIR}"
    fi
}

# Create default config
create_config() {
    local config_file="${CONFIG_DIR}/config.json"

    if [ ! -f "${config_file}" ]; then
        echo -e "\n${BLUE}Creating default configuration...${NC}"

        cat > "${config_file}" << 'EOF'
{
  "environments": {
    "local": {
      "host": "0.0.0.0",
      "mysql_port": 8816,
      "http_port": 8085,
      "user": "testuser",
      "password": "testpass"
    },
    "docker": {
      "host": "localhost",
      "mysql_port": 8816,
      "http_port": 8085,
      "user": "testuser",
      "password": "testpass",
      "container": "otterstax"
    },
    "k8s": {
      "namespace": "otterstax",
      "service": "otterstax-server",
      "mysql_port": 8816,
      "http_port": 8085,
      "user": "testuser",
      "password": "testpass"
    }
  },
  "current_environment": "local",
  "data_sources": []
}
EOF
        echo -e "${GREEN}✓${NC} Configuration created at ${config_file}"
    else
        echo -e "${YELLOW}⚠${NC} Configuration already exists, skipping"
    fi
}

# Show summary
show_summary() {
    echo -e "\n${GREEN}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}Installation complete!${NC}"
    echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"

    echo -e "\n${BLUE}Installed commands:${NC}"
    echo "  /data:query        - Execute SQL queries"
    echo "  /data:schema       - Explore database schema"
    echo "  /data:analyze      - Analyze data"
    echo "  /data:federated    - Federated queries"
    echo "  /infra:connect     - Connect to OtterStax"
    echo "  /infra:deploy      - Deploy OtterStax"
    echo "  /infra:status      - Check status"
    echo "  /infra:add-source  - Add data source"

    echo -e "\n${BLUE}Quick start:${NC}"
    echo "  1. Start OtterStax server"
    echo "  2. Run: /infra:connect local"
    echo "  3. Run: /data:query SELECT 1"

    echo -e "\n${BLUE}Configuration:${NC}"
    echo "  ${CONFIG_DIR}/config.json"

    echo -e "\n${BLUE}Documentation:${NC}"
    echo "  https://github.com/otterstax/claude-skills"
    echo ""
}

# Uninstall function
uninstall() {
    echo -e "${YELLOW}Uninstalling OtterStax Skills...${NC}"

    rm -rf "${COMMANDS_DIR}/data"
    rm -rf "${COMMANDS_DIR}/infra"
    rm -rf "${COMMANDS_DIR}/dev"
    rm -rf "${SKILLS_DIR}/otterstax"

    echo -e "${GREEN}✓${NC} OtterStax Skills uninstalled"
    echo -e "${YELLOW}Note:${NC} Configuration at ${CONFIG_DIR} was preserved"
}

# Main
main() {
    case "${1:-}" in
        --uninstall|-u)
            uninstall
            exit 0
            ;;
        --help|-h)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --uninstall, -u  Remove installed commands and skills"
            echo "  --help, -h       Show this help message"
            exit 0
            ;;
    esac

    check_claude
    create_dirs
    install_commands
    install_skills
    install_client
    create_config
    show_summary
}

main "$@"
