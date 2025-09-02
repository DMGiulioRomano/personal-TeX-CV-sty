# Makefile semplificato per CV Generator

# Configurazione
YAML_FILE = cv_data.yaml
PYTHON_SCRIPT = generate_cv.py
DATA_TEX = cv_data.tex

# Stile predefinito
STYLE ?= europass

# File generati dinamicamente basati sullo stile
MAIN_TEX = CV_GIULIO_DE_MATTIA-$(STYLE).tex
OUTPUT_PDF = CV_GIULIO_DE_MATTIA-$(STYLE).pdf

# Colori
GREEN = \033[0;32m
YELLOW = \033[1;33m
RED = \033[0;31m
NC = \033[0m

.PHONY: all generate latex clean check help

# Target predefinito
all: generate latex

# Genera file LaTeX da YAML
generate:
	@echo "$(YELLOW)🔄 Generando file LaTeX...$(NC)"
	@python3.11 $(PYTHON_SCRIPT) $(YAML_FILE) --style $(STYLE) --output .
	@echo "$(GREEN)✅ File LaTeX generati$(NC)"

# Compila LaTeX → PDF
latex:
	@echo "$(YELLOW)🔨 Compilando PDF...$(NC)"
	@xelatex -interaction=nonstopmode $(MAIN_TEX)
	@echo "$(GREEN)✅ PDF generato: $(OUTPUT_PDF)$(NC)"

# Stili disponibili
creative:    # Stile artistico/creativo
	$(MAKE) generate STYLE=creative
	$(MAKE) latex STYLE=creative

europass:    # Stile Europass standard UE  
	@$(MAKE) generate STYLE=europass
	@$(MAKE) latex STYLE=europass

academic:    # Stile per pubblicazioni/ricerca
	@$(MAKE) generate STYLE=academic
	@$(MAKE) latex STYLE=academic

# Genera tutti gli stili
all-styles:
	@echo "$(YELLOW)🚀 Generando tutti gli stili...$(NC)"
	@$(MAKE) creative
	@$(MAKE) europass  
	@$(MAKE) academic
	@echo "$(GREEN)✅ Tutti gli stili generati:$(NC)"
	@echo "$(GREEN)   - CV_GIULIO_DE_MATTIA-creative.pdf$(NC)"
	@echo "$(GREEN)   - CV_GIULIO_DE_MATTIA-europass.pdf$(NC)"
	@echo "$(GREEN)   - CV_GIULIO_DE_MATTIA-academic.pdf$(NC)"

# Pulizia completa
clean:
	@echo "$(YELLOW)🧹 Pulizia file generati...$(NC)"
	@rm -f CV_GIULIO_DE_MATTIA-*.tex CV_GIULIO_DE_MATTIA-*.pdf
	@rm -f $(DATA_TEX)
	@rm -f *.aux *.log *.out *.toc *.fdb_latexmk *.fls *.synctex.gz
	@echo "$(GREEN)✅ Pulizia completata$(NC)"

# Controllo dipendenze
check:
	@echo "$(YELLOW)🔍 Controllo dipendenze...$(NC)"
	@python3.11 --version || (echo "$(RED)❌ Python3.11 non trovato$(NC)" && exit 1)
	@python3.11 -c "import yaml" || (echo "$(RED)❌ PyYAML mancante. Installa: pip install PyYAML$(NC)" && exit 1)
	@xelatex --version > /dev/null || (echo "$(RED)❌ XeLaTeX non trovato$(NC)" && exit 1)
	@test -f $(YAML_FILE) || (echo "$(RED)❌ File $(YAML_FILE) mancante$(NC)" && exit 1)
	@test -f $(PYTHON_SCRIPT) || (echo "$(RED)❌ Script $(PYTHON_SCRIPT) mancante$(NC)" && exit 1)
	@echo "$(GREEN)✅ Tutte le dipendenze OK$(NC)"

# Apri PDF
open:
	@echo "$(GREEN)👀 Aprendo $(OUTPUT_PDF)...$(NC)"
	@if command -v xdg-open > /dev/null; then \
		xdg-open $(OUTPUT_PDF); \
	elif command -v open > /dev/null; then \
		open $(OUTPUT_PDF); \
	else \
		echo "$(YELLOW)⚠️  Apri manualmente: $(OUTPUT_PDF)$(NC)"; \
	fi

# Help
help:
	@echo "$(GREEN)📖 Comandi disponibili:$(NC)"
	@echo ""
	@echo "$(YELLOW)Generazione:$(NC)"
	@echo "  make generate    - Genera file LaTeX da YAML"
	@echo "  make latex       - Compila LaTeX → PDF"
	@echo "  make europass    - CV stile Europass UE (completo)"
	@echo "  make creative    - CV stile artistico/creativo (completo)"
	@echo "  make academic    - CV stile accademico (completo)"
	@echo "  make all-styles  - Genera tutti gli stili"
	@echo ""
	@echo "$(YELLOW)Utilità:$(NC)"
	@echo "  make clean       - Elimina tutti i file generati"
	@echo "  make check       - Controlla dipendenze"
	@echo "  make open        - Apri PDF generato (per stile corrente)"
	@echo "  make help        - Mostra questo aiuto"
	@echo ""
	@echo "$(YELLOW)Esempi:$(NC)"
	@echo "  make europass                    # Genera CV_GIULIO_DE_MATTIA-europass.pdf"
	@echo "  make STYLE=creative all          # Genera CV_GIULIO_DE_MATTIA-creative.pdf"
	@echo "  make generate latex              # Due step separati"
	@echo ""
	@echo "$(YELLOW)File generati:$(NC)"
	@echo "  - CV_GIULIO_DE_MATTIA-europass.pdf"
	@echo "  - CV_GIULIO_DE_MATTIA-creative.pdf" 
	@echo "  - CV_GIULIO_DE_MATTIA-academic.pdf"