#!/bin/bash
# ServerWatch Installation Script

set -e

# Configuration
INSTALL_PREFIX="${PREFIX:-/usr/local}"
BIN_DIR="${INSTALL_PREFIX}/bin"
LIB_DIR="${INSTALL_PREFIX}/lib/serverwatch"
VENV_DIR="${VENV_DIR:-/opt/venv}"
CONFIG_DIR="${CONFIG_DIR:-/etc/serverwatch}"
LOG_DIR="${LOG_DIR:-/var/log}"
SYSTEMD_DIR="${SYSTEMD_DIR:-/etc/systemd/system}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
check_root() {
    if [[ $EUID -ne 0 ]]; then
        log_error "This script must be run as root"
        exit 1
    fi
}

# Check dependencies
check_dependencies() {
    log_info "Checking system dependencies..."

    local missing_deps=()

    # Check for required system packages
    for cmd in python3 pip systemctl git; do
        if ! command -v "$cmd" &> /dev/null; then
            missing_deps+=("$cmd")
        fi
    done

    if [[ ${#missing_deps[@]} -gt 0 ]]; then
        log_error "Missing required dependencies: ${missing_deps[*]}"
        log_info "Please install the missing packages and try again"
        exit 1
    fi

    # Check Python version
    python_version=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
    required_version="3.8"

    if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
        log_error "Python ${required_version} or higher is required. Found: ${python_version}"
        exit 1
    fi

    log_info "All dependencies satisfied"
}

# Create directories
create_directories() {
    log_info "Creating installation directories..."

    mkdir -p "$BIN_DIR"
    mkdir -p "$LIB_DIR"
    mkdir -p "$CONFIG_DIR"
    mkdir -p "$LOG_DIR"

    # Create venv directory if it doesn't exist
    if [[ ! -d "$VENV_DIR" ]]; then
        mkdir -p "$VENV_DIR"
    fi
}

# Setup Python virtual environment
setup_python_env() {
    log_info "Setting up Python virtual environment..."

    if [[ ! -d "$VENV_DIR" ]]; then
        python3 -m venv "$VENV_DIR"
    fi

    # Activate virtual environment and install package
    # shellcheck disable=SC1091
    source "$VENV_DIR/bin/activate"

    # Upgrade pip
    "$VENV_DIR/bin/pip" install --upgrade pip

    # Install the serverwatch-analyzer package in development mode
    "$VENV_DIR/bin/pip" install -e .

    log_info "Python environment setup complete"
}

# Install serverwatch script
install_serverwatch() {
    log_info "Installing serverwatch script..."

    # Copy the main script
    cp "src/serverwatch" "$BIN_DIR/serverwatch"
    chmod +x "$BIN_DIR/serverwatch"

    # Update the Python path in the script
    sed -i "s|/opt/venv/bin/python3|${VENV_DIR}/bin/python3|g" "$BIN_DIR/serverwatch"

    log_info "ServerWatch script installed to $BIN_DIR/serverwatch"
}

# Setup configuration
setup_configuration() {
    log_info "Setting up configuration..."

    # Create default environment file if it doesn't exist
    if [[ ! -f "/root/.env.serverwatch" ]]; then
        cat > "/root/.env.serverwatch" << EOF
# ServerWatch Configuration
# OpenAI API Key for report analysis
OPENAI_API_KEY=your_openai_api_key_here

# Email settings
ALERT_RECIPIENT=admin@example.com
EMAIL_FROM=serverwatch@\$(hostname)

# Hostname (defaults to system hostname if not set)
HOSTNAME=\$(hostname)
EOF
        chmod 600 "/root/.env.serverwatch"
        log_warn "Created default configuration at /root/.env.serverwatch"
        log_warn "Please edit this file with your actual configuration"
    fi
}

# Setup systemd service (optional)
setup_systemd_service() {
    if [[ -d "$SYSTEMD_DIR" ]]; then
        log_info "Setting up systemd service..."

        cat > "$SYSTEMD_DIR/serverwatch.service" << EOF
[Unit]
Description=ServerWatch Daily Report
After=network.target

[Service]
Type=oneshot
ExecStart=${BIN_DIR}/serverwatch
User=root
Group=root

[Install]
WantedBy=multi-user.target
EOF

        cat > "$SYSTEMD_DIR/serverwatch.timer" << EOF
[Unit]
Description=Run ServerWatch daily at 6:00 AM
Requires=serverwatch.service

[Timer]
OnCalendar=daily
Persistent=true
RandomizedDelaySec=300

[Install]
WantedBy=timers.target
EOF

        systemctl daemon-reload
        log_info "SystemD service created. Enable with: systemctl enable --now serverwatch.timer"
    fi
}

# Run tests
run_tests() {
    if [[ "$RUN_TESTS" == "true" ]]; then
        log_info "Running tests..."
        # shellcheck disable=SC1091
        source "$VENV_DIR/bin/activate"

        # Install dev dependencies
        "$VENV_DIR/bin/pip" install -e ".[dev]"

        # Run tests
        "$VENV_DIR/bin/python" -m pytest tests/ -v --cov=serverwatch_analyzer

        log_info "Tests completed"
    fi
}

# Uninstall function
uninstall() {
    log_info "Uninstalling ServerWatch..."

    # Stop and disable systemd service
    if systemctl is-active --quiet serverwatch.timer; then
        systemctl stop serverwatch.timer
        systemctl disable serverwatch.timer
    fi

    # Remove files
    rm -f "$BIN_DIR/serverwatch"
    rm -f "$SYSTEMD_DIR/serverwatch.service"
    rm -f "$SYSTEMD_DIR/serverwatch.timer"
    rm -rf "$LIB_DIR"

    # Optionally remove virtual environment
    if [[ "$REMOVE_VENV" == "true" ]]; then
        rm -rf "$VENV_DIR"
    fi

    log_info "ServerWatch uninstalled"
}

# Show usage
usage() {
    cat << EOF
Usage: $0 [OPTIONS]

OPTIONS:
    install         Install ServerWatch (default)
    uninstall       Uninstall ServerWatch
    --prefix DIR    Installation prefix (default: /usr/local)
    --venv DIR      Virtual environment directory (default: /opt/venv)
    --test          Run tests after installation
    --help          Show this help message

ENVIRONMENT VARIABLES:
    PREFIX          Installation prefix
    VENV_DIR        Virtual environment directory
    CONFIG_DIR      Configuration directory
    LOG_DIR         Log directory
    SYSTEMD_DIR     SystemD service directory
    RUN_TESTS       Set to 'true' to run tests
    REMOVE_VENV     Set to 'true' to remove venv during uninstall

EXAMPLES:
    # Standard installation
    sudo $0

    # Install with custom prefix
    sudo PREFIX=/opt/serverwatch $0

    # Install and run tests
    sudo RUN_TESTS=true $0

    # Uninstall
    sudo $0 uninstall
EOF
}

# Main installation function
main() {
    local command="install"

    # Parse command line arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            install)
                command="install"
                shift
                ;;
            uninstall)
                command="uninstall"
                shift
                ;;
            --prefix)
                INSTALL_PREFIX="$2"
                BIN_DIR="${INSTALL_PREFIX}/bin"
                LIB_DIR="${INSTALL_PREFIX}/lib/serverwatch"
                shift 2
                ;;
            --venv)
                VENV_DIR="$2"
                shift 2
                ;;
            --test)
                RUN_TESTS="true"
                shift
                ;;
            --help|-h)
                usage
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
                usage
                exit 1
                ;;
        esac
    done

    case $command in
        install)
            log_info "Starting ServerWatch installation..."
            check_root
            check_dependencies
            create_directories
            setup_python_env
            install_serverwatch
            setup_configuration
            setup_systemd_service
            run_tests
            log_info "Installation completed successfully!"
            log_info "Don't forget to configure /root/.env.serverwatch"
            ;;
        uninstall)
            check_root
            uninstall
            ;;
        *)
            log_error "Invalid command: $command"
            usage
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"
