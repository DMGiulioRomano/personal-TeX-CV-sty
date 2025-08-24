# Makefile semplificato per CV Generator

# Configurazione
YAML_FILE = cv_data.yaml
PYTHON_SCRIPT = generate_cv.py
MAIN_TEX = CV_GIULIO_DE_MATTIA.tex
DATA_TEX = cv_data.tex
OUTPUT_PDF = CV_GIULIO_DE_MATTIA.pdf

# Stile predefinito
STYLE ?= european

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

# Compila tutto (Python + LaTeX)
european:
	@$(MAKE) generate STYLE=european
	@$(MAKE) latex

academic:
	@$(MAKE) generate STYLE=academic  
	@$(MAKE) latex

# Pulizia completa
clean:
	@echo "$(YELLOW)🧹 Pulizia file generati...$(NC)"
	@rm -f $(MAIN_TEX) $(DATA_TEX) $(OUTPUT_PDF)
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
	@echo "  make european    - CV stile europeo (completo)"
	@echo "  make academic    - CV stile accademico (completo)"
	@echo ""
	@echo "$(YELLOW)Utilità:$(NC)"
	@echo "  make clean       - Elimina tutti i file generati"
	@echo "  make check       - Controlla dipendenze"
	@echo "  make open        - Apri PDF generato"
	@echo "  make help        - Mostra questo aiuto"
	@echo ""
	@echo "$(YELLOW)Esempi:$(NC)"
	@echo "  make european              # Genera CV europeo"
	@echo "  make STYLE=academic all    # Genera CV accademico"
	@echo "  make generate latex        # Due step separati"