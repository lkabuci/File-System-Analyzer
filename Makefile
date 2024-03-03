# Makefile for managing project tasks

# Colors for terminal output
GREEN = \033[0;32m
YELLOW = \033[1;33m
RESET = \033[0m

# Define virtual environment variables
VENV = .env
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip

# Directories to be cleaned
CLEAN_DIRS = __pycache__ .pytest_cache

# Target: run
# Run the main application
run: $(VENV)/bin/activate
	@echo "$(GREEN)Running the main application...$(RESET)"
	@$(PYTHON) main.py .

# Target: test
# Build and run test using Docker
test: $(VENV)/bin/activate
	@echo "$(YELLOW)Running tests using Docker...$(RESET)"
	@docker compose up --build

# Target: venv
# Create virtual environment and install dependencies
venv: $(VENV)/bin/activate
	@echo "$(GREEN)Virtual environment created and dependencies installed.$(RESET)"

# Target: $(VENV)/bin/activate
# Create virtual environment and install dependencies
$(VENV)/bin/activate: requirements.txt
	@echo "$(GREEN)Setting up virtual environment...$(RESET)"
	@python3 -m venv $(VENV)
	@$(PIP) install --upgrade pip
	@$(PIP) install -r requirements.txt

# Target: clean
# Remove generated files and virtual environment
clean:
	@echo "$(YELLOW)Cleaning up...$(RESET)"
	@for dir in $(CLEAN_DIRS); do find . -type d -name "$$dir" -exec rm -rf {} \; 2> /dev/null; done
	@rm -rf $(VENV)
	@echo "$(GREEN)Cleanup complete.$(RESET)"

# Target: help
# Display help information about available targets
help:
	@echo "$(YELLOW)Available targets:$(RESET)"
	@echo "  $(GREEN)run$(RESET)         - Run the main application"
	@echo "  $(GREEN)test$(RESET)        - Build and run tests using Docker"
	@echo "  $(GREEN)venv$(RESET)        - Create virtual environment and install dependencies"
	@echo "  $(GREEN)clean$(RESET)       - Remove generated files and virtual environment"
	@echo "  $(GREEN)help$(RESET)        - Display this help message"

# Target: .PHONY
# Define phony targets to avoid conflicts with file names
.PHONY: run test venv clean
