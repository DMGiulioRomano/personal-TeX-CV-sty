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
        """Escape dei caratteri speciali LaTeX"""
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
        
        # Applica l'escape
        for char, escape in latex_special_chars.items():
            text = text.replace(char, escape)
        
        return text
    
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
        latex = "% --- Competenze ---\n\\skills{\n"
        
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
        
        latex = "% --- Esperienze ---\n"
        
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
        
        latex = "% --- Istruzione ---\n"
        
        for edu in self.data['istruzione']:
            voto_dettagli = f" ({edu['voto']})" if 'voto' in edu else ""
            dettagli = self.latex_escape(edu.get('dettagli', ''))
            
            latex += f"\\education{{{edu['anno']}}}{{{self.latex_escape(edu['istituto'])}}}{{{self.latex_escape(edu['titolo'])}{voto_dettagli}}}{{{dettagli}}}\n\n"
        
        return latex
    
    def generate_artistic_events(self) -> str:
        """Genera gli eventi artistici"""
        if 'attivita_concertistica' not in self.data:
            return ""
        
        latex = "% --- Attività selezionate ---\n"
        
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
                
                latex += f"\\artisticevent{{{event['data']}}}{{{self.latex_escape(event['venue'])}}}{{{self.latex_escape(event['organizzatore'])}}}{{{self.latex_escape(titolo)}}}{{{self.latex_escape(organico)}}}{{{self.latex_escape(programma)}}}\n\n"
        
        return latex
    
    def generate_languages(self) -> str:
        """Genera la sezione lingue"""
        if 'lingue' not in self.data:
            return ""
        
        latex = "% --- Lingue ---\n\\section*{Lingue}\n"
        
        lang_strings = []
        for lang in self.data['lingue']:
            lang_strings.append(f"{self.latex_escape(lang['nome'])}: {self.latex_escape(lang['livello'])}")
        
        latex += " \\\\\\\\ ".join(lang_strings) + "\n\n"
        return latex
    
    def generate_gdpr(self) -> str:
        """Genera la sezione consenso GDPR"""
        return "% --- Consenso GDPR ---\n\\section*{Consenso}\nAutorizzo il trattamento dei dati ai sensi del Reg. UE 2016/679.\n"
    
    def generate_latex_data(self) -> str:
        """Genera il file cv_data.tex completo"""
        latex = "% File: cv_data.tex (generato automaticamente)\n\n"
        
        latex += self.generate_personal_data()
        latex += f"\\makeheader"
        latex += self.generate_summary()  # Il summary va dopo i dati personali
        latex += self.generate_skills()
        latex += self.generate_experiences()
        latex += self.generate_education()
        latex += self.generate_artistic_events()
        latex += self.generate_languages()
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