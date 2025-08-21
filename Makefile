# Makefile per CV Generator - Versione Build Directory
# Uso: make [target] [STYLE=academic|european]

# Configurazione
YAML_FILE = cv_data.yaml
PYTHON_SCRIPT = generate_cv.py
STYLES_DIR = styles
BUILD_DIR = build
MAIN_TEX = CV_GIULIO_DE_MATTIA.tex
DATA_TEX = cv_data.tex
OUTPUT_PDF = CV_GIULIO_DE_MATTIA.pdf

# Percorsi completi nella build directory
BUILD_MAIN_TEX = $(BUILD_DIR)/$(MAIN_TEX)
BUILD_DATA_TEX = $(BUILD_DIR)/$(DATA_TEX)
BUILD_OUTPUT_PDF = $(BUILD_DIR)/$(OUTPUT_PDF)

# Stile predefinito
STYLE ?= european

# Compilatore LaTeX
LATEX = xelatex
LATEX_FLAGS = -interaction=nonstopmode -halt-on-error -output-directory=$(BUILD_DIR)

# File temporanei generati da LaTeX (nella build directory)
LATEX_AUX_FILES = $(BUILD_DIR)/*.aux $(BUILD_DIR)/*.log $(BUILD_DIR)/*.out $(BUILD_DIR)/*.toc $(BUILD_DIR)/*.fdb_latexmk $(BUILD_DIR)/*.fls $(BUILD_DIR)/*.synctex.gz $(BUILD_DIR)/*.nav $(BUILD_DIR)/*.snm $(BUILD_DIR)/*.vrb

# Colori per output
GREEN = \033[0;32m
YELLOW = \033[1;33m
RED = \033[0;31m
NC = \033[0m # No Color

.PHONY: all european academic generate clean clean-all help

# Target predefinito
all: european

# Crea directory build se non esistente
$(BUILD_DIR):
	@mkdir -p $(BUILD_DIR)

# Genera CV stile europeo
european: $(BUILD_DIR)
	@echo "$(GREEN)📄 Generando CV stile europeo...$(NC)"
	@$(MAKE) generate STYLE=european
	@$(MAKE) compile

# Genera CV stile accademico  
academic: $(BUILD_DIR)
	@echo "$(GREEN)📄 Generando CV stile accademico...$(NC)"
	@$(MAKE) generate STYLE=academic
	@$(MAKE) compile

# Genera file LaTeX dal YAML (nella build directory)
generate: $(BUILD_DIR)
	@echo "$(YELLOW)🔄 Processando $(YAML_FILE) → file LaTeX in $(BUILD_DIR)/...$(NC)"
	@python3.11 $(PYTHON_SCRIPT) $(YAML_FILE) --style $(STYLE) --styles-dir ../$(STYLES_DIR) --output $(BUILD_DIR)
	@echo "$(GREEN)✅ File LaTeX generati in $(BUILD_DIR)/$(NC)"

# Compila LaTeX → PDF
compile: $(BUILD_OUTPUT_PDF)

$(BUILD_OUTPUT_PDF): $(BUILD_MAIN_TEX) $(BUILD_DATA_TEX)
	@echo "$(YELLOW)🔨 Compilando LaTeX → PDF in $(BUILD_DIR)/...$(NC)"
	@cd $(BUILD_DIR) && $(LATEX) $(LATEX_FLAGS) $(MAIN_TEX)
	@echo "$(GREEN)✅ PDF generato: $(BUILD_OUTPUT_PDF)$(NC)"

# Versione alternativa che compila dalla directory principale
compile-alt: $(BUILD_MAIN_TEX) $(BUILD_DATA_TEX)
	@echo "$(YELLOW)🔨 Compilando LaTeX → PDF...$(NC)"
	@$(LATEX) -output-directory=$(BUILD_DIR) $(BUILD_MAIN_TEX)
	@echo "$(GREEN)✅ PDF generato: $(BUILD_OUTPUT_PDF)$(NC)"

# Compila entrambi gli stili
both: $(BUILD_DIR)
	@echo "$(GREEN)📄 Generando entrambi gli stili...$(NC)"
	@$(MAKE) european
	@cp $(BUILD_OUTPUT_PDF) $(BUILD_DIR)/CV_GIULIO_DE_MATTIA_european.pdf
	@$(MAKE) academic  
	@cp $(BUILD_OUTPUT_PDF) $(BUILD_DIR)/CV_GIULIO_DE_MATTIA_academic.pdf
	@echo "$(GREEN)✅ Generati: $(BUILD_DIR)/CV_GIULIO_DE_MATTIA_european.pdf, $(BUILD_DIR)/CV_GIULIO_DE_MATTIA_academic.pdf$(NC)"

# Compila con output dettagliato (debug)
debug: $(BUILD_DIR)
	@echo "$(YELLOW)🛠 Compilazione debug...$(NC)"
	@echo "$(YELLOW)📁 Verificando file di stile...$(NC)"
	@test -f $(STYLES_DIR)/style_$(STYLE).sty || (echo "$(RED)❌ File style_$(STYLE).sty mancante$(NC)" && exit 1)
	@echo "$(GREEN)✅ File di stile trovato$(NC)"
	@$(MAKE) generate STYLE=$(STYLE)
	@echo "$(YELLOW)📝 Contenuto generato in $(BUILD_DATA_TEX):$(NC)"
	@head -10 $(BUILD_DATA_TEX)
	@echo "$(YELLOW)🔧 Compilando con output completo...$(NC)"
	@cd $(BUILD_DIR) && xelatex -interaction=errorstopmode -file-line-error $(MAIN_TEX)

# Compila automaticamente quando cambia il YAML
watch: $(BUILD_DIR)
	@echo "$(GREEN)👀 Modalità watch attiva. Premi Ctrl+C per uscire.$(NC)"
	@while true; do \
		$(MAKE) generate STYLE=$(STYLE) > /dev/null 2>&1; \
		$(MAKE) compile > /dev/null 2>&1; \
		echo "$(GREEN)✅ CV aggiornato ($(STYLE)) - $(shell date +%H:%M:%S)$(NC)"; \
		sleep 2; \
	done

# Pulizia file temporanei LaTeX
clean:
	@echo "$(YELLOW)🧹 Rimuovendo file temporanei LaTeX...$(NC)"
	@rm -f $(LATEX_AUX_FILES) 2>/dev/null || true
	@echo "$(GREEN)✅ File temporanei rimossi$(NC)"

# Pulizia completa (include file generati)
clean-all: clean
	@echo "$(YELLOW)🧹 Rimozione completa...$(NC)"
	@rm -rf $(BUILD_DIR)
	@echo "$(GREEN)✅ Pulizia completa completata$(NC)"

# Controllo dipendenze
check:
	@echo "$(YELLOW)🔍 Controllo dipendenze...$(NC)"
	@python3.11 --version || (echo "$(RED)❌ Python3 non trovato$(NC)" && exit 1)
	@python3.11 -c "import yaml" || (echo "$(RED)❌ PyYAML non installato. Installa con: pip install PyYAML$(NC)" && exit 1)
	@$(LATEX) --version > /dev/null || (echo "$(RED)❌ XeLaTeX non trovato$(NC)" && exit 1)
	@test -f $(YAML_FILE) || (echo "$(RED)❌ File $(YAML_FILE) non trovato$(NC)" && exit 1)
	@test -f $(PYTHON_SCRIPT) || (echo "$(RED)❌ Script $(PYTHON_SCRIPT) non trovato$(NC)" && exit 1)
	@echo "$(GREEN)✅ Tutte le dipendenze sono soddisfatte$(NC)"

# Installa dipendenze Python
install-deps:
	@echo "$(YELLOW)📦 Installando dipendenze Python...$(NC)"
	@pip install PyYAML
	@echo "$(GREEN)✅ Dipendenze installate$(NC)"

# Apri PDF generato
open: $(BUILD_OUTPUT_PDF)
	@echo "$(GREEN)👀 Aprendo $(BUILD_OUTPUT_PDF)...$(NC)"
	@if command -v xdg-open > /dev/null; then \
		xdg-open $(BUILD_OUTPUT_PDF); \
	elif command -v open > /dev/null; then \
		open $(BUILD_OUTPUT_PDF); \
	else \
		echo "$(YELLOW)⚠️  Non riesco ad aprire il PDF automaticamente$(NC)"; \
	fi

# Informazioni sui file generati
info:
	@echo "$(GREEN)📊 Informazioni file:$(NC)"
	@echo "YAML fonte: $(YAML_FILE) $(shell test -f $(YAML_FILE) && echo '✅' || echo '❌')"
	@echo "Script Python: $(PYTHON_SCRIPT) $(shell test -f $(PYTHON_SCRIPT) && echo '✅' || echo '❌')"
	@echo "File LaTeX: $(BUILD_MAIN_TEX) $(shell test -f $(BUILD_MAIN_TEX) && echo '✅' || echo '❌')"
	@echo "Dati LaTeX: $(BUILD_DATA_TEX) $(shell test -f $(BUILD_DATA_TEX) && echo '✅' || echo '❌')"
	@echo "PDF finale: $(BUILD_OUTPUT_PDF) $(shell test -f $(BUILD_OUTPUT_PDF) && echo '✅' || echo '❌')"
	@echo "Stile corrente: $(STYLE)"
	@echo "Build directory: $(BUILD_DIR)/"

# Copia file dalla build alla directory principale (se necessario)
export:
	@echo "$(GREEN)📤 Copiando file dalla build directory...$(NC)"
	@test -f $(BUILD_OUTPUT_PDF) && cp $(BUILD_OUTPUT_PDF) . && echo "✅ $(OUTPUT_PDF) copiato" || echo "❌ Nessun PDF da copiare"

# Help
help:
	@echo "$(GREEN)📖 CV Generator - Comandi disponibili:$(NC)"
	@echo ""
	@echo "$(YELLOW)Generazione:$(NC)"
	@echo "  make european    - Genera CV stile europeo (default)"
	@echo "  make academic    - Genera CV stile accademico" 
	@echo "  make both        - Genera entrambi gli stili"
	@echo ""
	@echo "$(YELLOW)Compilazione:$(NC)"
	@echo "  make compile     - Compila LaTeX → PDF"
	@echo "  make debug       - Compila con output dettagliato"
	@echo "  make watch       - Ricompila automaticamente"
	@echo ""
	@echo "$(YELLOW)Utilità:$(NC)"
	@echo "  make clean       - Rimuove file temporanei LaTeX"
	@echo "  make clean-all   - Rimozione completa (elimina build/)"
	@echo "  make check       - Controlla dipendenze"
	@echo "  make install-deps- Installa dipendenze Python"
	@echo "  make open        - Apri PDF generato"
	@echo "  make info        - Mostra stato file"
	@echo "  make export      - Copia PDF dalla build/ alla directory principale"
	@echo ""
	@echo "$(YELLOW)Opzioni:$(NC)"
	@echo "  STYLE=academic   - Forza stile accademico"
	@echo "  STYLE=european   - Forza stile europeo"
	@echo ""
	@echo "$(YELLOW)Esempi:$(NC)"
	@echo "  make academic    # Genera CV accademico"
	@echo "  make STYLE=academic compile  # Compila stile specifico"
	@echo "  make export      # Copia PDF finale nella directory principale"