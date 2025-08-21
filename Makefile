# Makefile per CV Generator
# Uso: make [target] [STYLE=academic|european]

# Configurazione
YAML_FILE = cv_data.yaml
PYTHON_SCRIPT = generate_cv.py
MAIN_TEX = CV_GIULIO_DE_MATTIA.tex
DATA_TEX = cv_data.tex
OUTPUT_PDF = CV_GIULIO_DE_MATTIA.pdf

# Stile predefinito
STYLE ?= european

# Compilatore LaTeX
LATEX = xelatex
LATEX_FLAGS = -interaction=nonstopmode -halt-on-error

# File temporanei generati da LaTeX
LATEX_AUX_FILES = *.aux *.log *.out *.toc *.fdb_latexmk *.fls *.synctex.gz *.nav *.snm *.vrb

# Colori per output
GREEN = \033[0;32m
YELLOW = \033[1;33m
RED = \033[0;31m
NC = \033[0m # No Color

.PHONY: all european academic generate clean clean-all help

# Target predefinito
all: european

# Genera CV stile europeo
european:
	@echo "$(GREEN) Generando CV stile europeo...$(NC)"
	@$(MAKE) generate STYLE=european
	@$(MAKE) compile

# Genera CV stile accademico  
academic:
	@echo "$(GREEN) Generando CV stile accademico...$(NC)"
	@$(MAKE) generate STYLE=academic
	@$(MAKE) compile

# Genera file LaTeX dal YAML
generate:
	@echo "$(YELLOW) Processando $(YAML_FILE) → file LaTeX...$(NC)"
	@python3 $(PYTHON_SCRIPT) $(YAML_FILE) --style $(STYLE)

# Compila LaTeX → PDF
compile: $(OUTPUT_PDF)

$(OUTPUT_PDF): $(MAIN_TEX) $(DATA_TEX)
	@echo "$(YELLOW) Compilando LaTeX → PDF...$(NC)"
	@$(LATEX) $(LATEX_FLAGS) $(MAIN_TEX)
	@echo "$(GREEN) PDF generato: $(OUTPUT_PDF)$(NC)"

# Compila entrambi gli stili
both:
	@echo "$(GREEN) Generando entrambi gli stili...$(NC)"
	@$(MAKE) european
	@cp $(OUTPUT_PDF) CV_GIULIO_DE_MATTIA_european.pdf
	@$(MAKE) academic  
	@cp $(OUTPUT_PDF) CV_GIULIO_DE_MATTIA_academic.pdf
	@echo "$(GREEN) Generati: CV_GIULIO_DE_MATTIA_european.pdf, CV_GIULIO_DE_MATTIA_academic.pdf$(NC)"

# Compila con output dettagliato (debug)
debug:
	@echo "$(YELLOW) Compilazione debug...$(NC)"
	@$(MAKE) generate STYLE=$(STYLE)
	@$(LATEX) -interaction=errorstopmode $(MAIN_TEX)

# Compila automaticamente quando cambia il YAML
watch:
	@echo "$(GREEN) Modalità watch attiva. Premi Ctrl+C per uscire.$(NC)"
	@while true; do \
		$(MAKE) generate STYLE=$(STYLE) > /dev/null 2>&1; \
		$(MAKE) compile > /dev/null 2>&1; \
		echo "$(GREEN) CV aggiornato ($(STYLE)) - $(shell date +%H:%M:%S)$(NC)"; \
		sleep 2; \
	done

# Pulizia file temporanei LaTeX
clean:
	@echo "$(YELLOW) Rimuovendo file temporanei LaTeX...$(NC)"
	@rm -f $(LATEX_AUX_FILES)
	@echo "$(GREEN) File temporanei rimossi$(NC)"

# Pulizia completa (include file generati)
clean-all: clean
	@echo "$(YELLOW) Rimozione completa...$(NC)"
	@rm -f $(DATA_TEX) $(OUTPUT_PDF)
	@rm -f CV_GIULIO_DE_MATTIA_*.pdf
	@echo "$(GREEN) Pulizia completa completata$(NC)"

# Controllo dipendenze
check:
	@echo "$(YELLOW) Controllo dipendenze...$(NC)"
	@python3 --version || (echo "$(RED)❌ Python3 non trovato$(NC)" && exit 1)
	@python3 -c "import yaml" || (echo "$(RED)❌ PyYAML non installato. Installa con: pip install PyYAML$(NC)" && exit 1)
	@$(LATEX) --version > /dev/null || (echo "$(RED)❌ XeLaTeX non trovato$(NC)" && exit 1)
	@test -f $(YAML_FILE) || (echo "$(RED)❌ File $(YAML_FILE) non trovato$(NC)" && exit 1)
	@test -f $(PYTHON_SCRIPT) || (echo "$(RED)❌ Script $(PYTHON_SCRIPT) non trovato$(NC)" && exit 1)
	@echo "$(GREEN) Tutte le dipendenze sono soddisfatte$(NC)"

# Installa dipendenze Python
install-deps:
	@echo "$(YELLOW) Installando dipendenze Python...$(NC)"
	@pip install PyYAML
	@echo "$(GREEN) Dipendenze installate$(NC)"

# Apri PDF generato
open: $(OUTPUT_PDF)
	@echo "$(GREEN) Aprendo $(OUTPUT_PDF)...$(NC)"
	@if command -v xdg-open > /dev/null; then \
		xdg-open $(OUTPUT_PDF); \
	elif command -v open > /dev/null; then \
		open $(OUTPUT_PDF); \
	else \
		echo "$(YELLOW)  Non riesco ad aprire il PDF automaticamente$(NC)"; \
	fi

# Help
help:
	@echo "$(GREEN) CV Generator - Comandi disponibili:$(NC)"
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
	@echo "  make clean-all   - Rimozione completa"
	@echo "  make check       - Controlla dipendenze"
	@echo "  make install-deps- Installa dipendenze Python"
	@echo "  make open        - Apri PDF generato"
	@echo ""
	@echo "$(YELLOW)Opzioni:$(NC)"
	@echo "  STYLE=academic   - Forza stile accademico"
	@echo "  STYLE=european   - Forza stile europeo"
	@echo ""
	@echo "$(YELLOW)Esempi:$(NC)"
	@echo "  make academic    # Genera CV accademico"
	@echo "  make STYLE=academic compile  # Compila stile specifico"