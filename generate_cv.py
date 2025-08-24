#!/usr/bin/env python3
"""
CV Generator - Genera file LaTeX da dati YAML
Uso: python generate_cv.py [--style academic|european] [--output filename]
"""

import yaml
import argparse
from pathlib import Path
from typing import Dict, Any, List
import re


class CVGenerator:
    def __init__(self, yaml_file: str):
        """Inizializza il generatore con i dati dal file YAML"""
        with open(yaml_file, 'r', encoding='utf-8') as f:
            self.data = yaml.safe_load(f)
        
    def latex_escape(self, text: str) -> str:
        """Escape dei caratteri speciali LaTeX, ignorando le espressioni matematiche $...$"""
        if not text:
            return ""
        
        # Dizionario dei caratteri da escapare
        latex_special_chars = {
            '&': r'\&',
            '%': r'\%',
            '$': r'\$',
            '#': r'\#',
            '^': r'\^{}',
            '_': r'\_',
            '{': r'\{',
            '}': r'\}',
            '~': r'\~{}',
            '\\': r'\textbackslash{}'
        }

        # Funzione per fare l'escape del testo normale
        def escape_text(t):
            for char, esc in latex_special_chars.items():
                t = t.replace(char, esc)
            return t

        # Split del testo in parti "normale" e "matematica"
        parts = re.split(r'(\$.*?\$)', text)  # mantiene anche i delimitatori $
        escaped_parts = []
        for part in parts:
            if part.startswith('$') and part.endswith('$'):
                # È un'espressione matematica: non fare escape
                escaped_parts.append(part)
            else:
                # Testo normale: fare escape
                escaped_parts.append(escape_text(part))
        
        return ''.join(escaped_parts)


    def generate_personal_data(self) -> str:
        """Genera i comandi LaTeX per i dati personali"""
        personal = self.data['dati_personali']
        
        latex = f"% --- Dati personali ---\n"
        latex += f"\\name{{{self.latex_escape(personal['nome'])}}}\n"
        latex += f"\\role{{{self.latex_escape(personal['ruolo'])}}}\n"
        latex += f"\\contacts{{{self.latex_escape(personal['citta'])}}}{{{personal['telefono']}}}{{{personal['email']}}}{{{personal['portfolio']}}}\n"
        
        if 'foto' in personal:
            latex += f"\\photo{{{personal['foto']}}}\n"
        
        return latex + "\n"
    
    def generate_summary(self) -> str:
        """Genera il summary professionale"""
        if 'summary' not in self.data:
            return ""
        
        summary_text = self.latex_escape(self.data['summary'])
        return f"% --- Summary ---\n\\summary{{{summary_text}}}\n\n"
    
    def generate_skills(self) -> str:
        """Genera la sezione competenze"""
        if 'tool_digitali' not in self.data:
            return ""
        
        tools = self.data['tool_digitali']
        latex = "% --- Competenze ---\n\\section*{Competenze Tecniche}\n\\skills{\n"
        
        if 'competenze_audio' in tools:
            for skill in tools['competenze_audio']:
                # IMPORTANTE: Applica l'escape LaTeX qui
                escaped_skill = self.latex_escape(skill)
                latex += f"  \\item {escaped_skill}\n"
        
        latex += "}\n\n"
        return latex
    
    def generate_experiences(self) -> str:
        """Genera le esperienze professionali"""
        if 'esperienze_professionali' not in self.data:
            return ""
        
        latex = "% --- Esperienze ---\n\\section*{Esperienza Professionale}\n"
        
        for exp in self.data['esperienze_professionali']:
            # Escape delle mansioni
            mansioni_escaped = []
            for mansione in exp['mansioni']:
                mansioni_escaped.append(f"  \\item {self.latex_escape(mansione)}")
            mansioni = '\n'.join(mansioni_escaped)
            
            latex += f"\\experience{{{exp['periodo']}}}{{{self.latex_escape(exp['organizzazione'])}}}{{{self.latex_escape(exp['ruolo'])}}}{{\n"
            latex += f"{mansioni}\n"
            latex += "}\n\n"
        
        return latex
    
    def generate_education(self) -> str:
        """Genera la sezione istruzione"""
        if 'istruzione' not in self.data:
            return ""
        
        latex = "% --- Formazione ---\n\\section*{Formazione}\n"
        
        for edu in self.data['istruzione']:
            voto_dettagli = f" ({edu['voto']})" if 'voto' in edu else ""
            dettagli = self.latex_escape(edu.get('dettagli', ''))
            
            latex += f"\\education{{{edu['anno']}}}{{{self.latex_escape(edu['istituto'])}}}{{{self.latex_escape(edu['titolo'])}{voto_dettagli}}}{{{dettagli}}}\n\n"
        
        return latex
    
    def generate_artistic_events(self) -> str:
        """Genera gli eventi artistici"""
        if 'attivita_concertistica' not in self.data:
            return ""
        
        latex = "% --- Attività Concertistica ---\n\\section*{Attività Concertistica}\n"
        
        for event in self.data['attivita_concertistica']:
            # Gestisce eventi con programma multiplo
            if 'programma' in event:
                # Evento con più brani (es. Generazioni Elettroacustiche)
                for brano in event['programma']:
                    latex += f"\\artisticevent{{{event['data']}}}{{{self.latex_escape(event['venue'])}}}{{{self.latex_escape(event['organizzatore'])}}}{{{self.latex_escape(brano['titolo'])}}}{{{self.latex_escape(brano['organico'])}}}{{{self.latex_escape(brano.get('note', brano['ruolo']))}}}\n\n"
            else:
                # Evento singolo
                organico = event.get('organico', '')
                if 'collaboratori' in event:
                    organico += f" (con {event['collaboratori']})" if organico else f"Con {event['collaboratori']}"
                
                programma = event.get('note', f"{event['tipo']} - {event['ruolo']}")
                if 'compositore' in event and event['compositore'] != event.get('ruolo'):
                    programma = f"Opera di {event['compositore']} - {programma}"
                
                titolo = event.get('titolo', event.get('evento', ''))
                
                latex += (
                    f"\\artisticevent"
                    f"{{{event['data']}}}"  # #1 data
                    f"{{{self.latex_escape(event['venue'])}}}"  # #2 venue
                    f"{{{self.latex_escape(event['organizzatore'])}}}"  # #3 organizzatore
                    f"{{{self.latex_escape(titolo)}}}"  # #4 titolo
                    f"{{{self.latex_escape(organico)}}}"  # #5 organico
                    f"{{{self.latex_escape(event.get('ruolo', ''))}}}"  # #6 ruolo (nuovo)
                    f"{{{self.latex_escape(programma)}}}"  # #7 programma/note
                    "\n\n"
                )
        
        return latex
    
    def generate_languages(self) -> str:
        """Genera le lingue come itemize usando il comando \languageitem"""
        if 'lingue' not in self.data:
            return ""
        
        latex = "% --- Lingue ---\n\\section*{Lingue}\n"
        latex += "\\begin{itemize}[leftmargin=*, topsep=2pt, itemsep=1pt]\n"
        
        for lang in self.data['lingue']:
            for nome, livello in lang.items():
                nome_clean = self.latex_escape(nome).replace('\n', ' ').strip()
                livello_clean = self.latex_escape(livello).replace('\n', ' ').strip()
                latex += f"  \\languageitem{{{nome_clean}}}{{{livello_clean}}}\n"
        
        latex += "\\end{itemize}\n\n"
        return latex

    
    def generate_gdpr(self) -> str:
        """Genera la sezione consenso GDPR"""
        return "% --- Consenso GDPR ---\n\\section*{Consenso}\nAutorizzo il trattamento dei miei dati personali ai sensi del Decreto Legislativo 196 del 30 giugno 2003 e dell'art. 13 del GDPR (Regolamento UE 2016/679) ai fini della ricerca e selezione del personale.\n"

    def generate_teaching(self) -> str:
        """Genera la sezione insegnamento"""
        if 'insegnamento' not in self.data:
            return ""
        
        latex = "% --- Didattica ---\n\\section*{Attività Didattica}\n"
        
        for teaching in self.data['insegnamento']:
            # Estrae i dati dal dizionario con valori di default sicuri
            periodo = teaching.get('periodo', '')
            istituto = self.latex_escape(teaching.get('istituto', ''))
            titolo_progetto = self.latex_escape(teaching.get('titolo_progetto', teaching.get('tipo', '')))
            
            # Costruisce la lista dei dettagli come itemize
            dettagli_items = []
            
            # Target (obbligatorio nel tuo esempio)
            if 'target' in teaching:
                dettagli_items.append(f"  \\item Target: {self.latex_escape(teaching['target'])}")
            
            # Numero partecipanti
            if 'partecipanti' in teaching:
                dettagli_items.append(f"  \\item Partecipanti: {self.latex_escape(str(teaching['partecipanti']))}")
            
            # Bando vinto (opzionale)
            if 'bando_vinto' in teaching and teaching['bando_vinto'].strip():
                dettagli_items.append(f"  \\item Bando: {self.latex_escape(teaching['bando_vinto'])}")
            
            # Focus
            if 'focus' in teaching:
                dettagli_items.append(f"  \\item Focus: {self.latex_escape(teaching['focus'])}")
            
            # Metodologia
            if 'metodologia' in teaching:
                dettagli_items.append(f"  \\item Metodologia: {self.latex_escape(teaching['metodologia'])}")
            
            # Genera il comando LaTeX usando il formato \experience esistente
            # \experience{periodo}{organizzazione}{ruolo}{mansioni_itemize}
            latex += f"\\experience{{{periodo}}}{{{istituto}}}{{{titolo_progetto}}}{{\n"
            
            # Aggiunge tutti gli item dei dettagli
            latex += '\n'.join(dettagli_items)
            
            latex += "\n}\n\n"
        
        return latex

    def generate_projects(self) -> str:
        """Genera la sezione progetti"""
        if 'pubblicazioni' not in self.data:
            return ""
        
        latex = "% --- Progetti ---\n\\section*{Progetti e Collaborazioni}\n"
        
        # Progetti personali
        if 'progetti_personali' in self.data['pubblicazioni']:
            for progetto in self.data['pubblicazioni']['progetti_personali']:
                latex += f"\\experience{{{progetto.get('periodo', 'In corso')}}}{{{self.latex_escape(progetto.get('sede', progetto.get('sedi', '')))}}}{{{self.latex_escape(progetto['nome'])}}}{{\n"
                
                if 'descrizione' in progetto:
                    latex += f"  \\item {self.latex_escape(progetto['descrizione'])}\n"
                if 'focus' in progetto:
                    latex += f"  \\item Focus: {self.latex_escape(progetto['focus'])}\n"
                if 'metodologia' in progetto:
                    latex += f"  \\item Metodologia: {self.latex_escape(progetto['metodologia'])}\n"
                if 'obiettivi' in progetto:
                    latex += f"  \\item Obiettivi: {self.latex_escape(progetto['obiettivi'])}\n"
                
                latex += "}\n\n"
        
        # Competenze relazionali (progetti di coordinamento)
        if 'competenze_relazionali' in self.data['pubblicazioni']:
            for competenza in self.data['pubblicazioni']['competenze_relazionali']:
                latex += f"\\experience{{{competenza.get('periodo', 'Coordinamento')}}}{{{self.latex_escape(competenza.get('sede', ''))}}}{{{self.latex_escape(competenza['progetto'])}}}{{\n"
                
                if 'team' in competenza:
                    latex += f"  \\item Team: {self.latex_escape(competenza['team'])}\n"
                if 'competenze' in competenza:
                    latex += f"  \\item Competenze: {self.latex_escape(competenza['competenze'])}\n"
                
                latex += "}\n\n"
        
        return latex

    def generate_latex_data(self) -> str:
        """Genera il file cv_data.tex completo"""
        latex = "% File: cv_data.tex (generato automaticamente)\n\n"
        
        latex += self.generate_personal_data()
        latex += "\\makeheader\n\n"
        latex += self.generate_summary()  # Il summary va dopo i dati personali
        latex += self.generate_education()
        latex += self.generate_languages()
        latex += self.generate_skills()
        latex += self.generate_experiences()
        latex += self.generate_teaching() 
        latex += self.generate_artistic_events()
        latex += self.generate_projects()
        latex += self.generate_gdpr()
        
        return latex
    
    def generate_main_tex(self, style: str = "european", styles_dir: str = "styles") -> str:
        """Genera il file principale LaTeX"""
        latex = f"""%!TEX root = CV_GIULIO_DE_MATTIA.tex
%!TEX TS-program = xelatex
%!TEX encoding = UTF-8 Unicode

\\documentclass[a4paper,10pt]{{article}}

% Carica direttamente il file di stile dal path relativo
\\usepackage{{{styles_dir}/style_{style}}}

\\begin{{document}}

% PRIMA definisci i dati
\\input{{cv_data.tex}}

\\end{{document}}
"""
        return latex
    
    def save_files(self, output_dir: str = ".", style: str = "european", styles_dir: str = "styles"):
        """Salva i file generati"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Genera cv_data.tex
        data_content = self.generate_latex_data()
        (output_path / "cv_data.tex").write_text(data_content, encoding='utf-8')
        
        # Genera file principale
        main_content = self.generate_main_tex(style, styles_dir)
        (output_path / "CV_GIULIO_DE_MATTIA.tex").write_text(main_content, encoding='utf-8')
        
        print(f"✅ File generati in {output_path}:")
        print(f"   - cv_data.tex")
        print(f"   - CV_GIULIO_DE_MATTIA.tex (stile: {style})")
        print(f"   - Cerca file .sty in: {styles_dir}/")



def main():
    parser = argparse.ArgumentParser(description="Genera CV LaTeX da dati YAML")
    parser.add_argument("yaml_file", help="File YAML con i dati del CV")
    parser.add_argument("--style", choices=["academic", "european"], 
                       default="european", help="Stile del CV")
    parser.add_argument("--styles-dir", default="styles", 
                       help="Cartella contenente i file .sty")
    parser.add_argument("--output", "-o", default=".", 
                       help="Directory di output")
    
    args = parser.parse_args()
    
    try:
        generator = CVGenerator(args.yaml_file)
        generator.save_files(args.output, args.style, args.styles_dir)
        
        print(f"\n🚀 Per compilare:")
        print(f"   cd {args.output}")
        print(f"   xelatex CV_GIULIO_DE_MATTIA.tex")
        
    except FileNotFoundError:
        print(f"❌ Errore: File {args.yaml_file} non trovato")
    except yaml.YAMLError as e:
        print(f"❌ Errore nel parsing YAML: {e}")
    except Exception as e:
        print(f"❌ Errore: {e}")


if __name__ == "__main__":
    main()