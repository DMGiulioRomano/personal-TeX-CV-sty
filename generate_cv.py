#!/usr/bin/env python3
"""
CV Generator - Genera file LaTeX da dati YAML
Uso: python generate_cv.py [--style academic|european] [--output filename]
"""

import yaml
import argparse
from pathlib import Path
from typing import Dict, Any, List


class CVGenerator:
    def __init__(self, yaml_file: str):
        """Inizializza il generatore con i dati dal file YAML"""
        with open(yaml_file, 'r', encoding='utf-8') as f:
            self.data = yaml.safe_load(f)
    
    def generate_personal_data(self) -> str:
        """Genera i comandi LaTeX per i dati personali"""
        personal = self.data['dati_personali']
        
        latex = f"% --- Dati personali ---\n"
        latex += f"\\name{{{personal['nome']}}}\n"
        latex += f"\\role{{{personal['ruolo']}}}\n"
        latex += f"\\contacts{{{personal['citta']}}}{{{personal['telefono']}}}{{{personal['email']}}}{{{personal['portfolio']}}}\n"
        
        if 'foto' in personal:
            latex += f"\\photo{{{personal['foto']}}}\n"
        
        return latex + "\n"
    
    def generate_skills(self) -> str:
        """Genera la sezione competenze"""
        if 'tool_digitali' not in self.data:
            return ""
        
        tools = self.data['tool_digitali']
        latex = "% --- Competenze ---\n\\skills{\n"
        
        if 'competenze_audio' in tools:
            for skill in tools['competenze_audio']:
                latex += f"  \\item {skill}\n"
        
        latex += "}\n\n"
        return latex
    
    def generate_experiences(self) -> str:
        """Genera le esperienze professionali"""
        if 'esperienze_professionali' not in self.data:
            return ""
        
        latex = "% --- Esperienze ---\n"
        
        for exp in self.data['esperienze_professionali']:
            mansioni = '\n'.join([f"  \\item {m}" for m in exp['mansioni']])
            
            latex += f"\\experience{{{exp['periodo']}}}{{{exp['organizzazione']}}}{{{exp['ruolo']}}}{{\n"
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
            dettagli = edu.get('dettagli', '')
            
            latex += f"\\education{{{edu['anno']}}}{{{edu['istituto']}}}{{{edu['titolo']}{voto_dettagli}}}{{{dettagli}}}\n\n"
        
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
                    latex += f"\\artisticevent{{{event['data']}}}{{{event['venue']}}}{{{event['organizzatore']}}}{{{brano['titolo']}}}{{{brano['organico']}}}{{{brano.get('note', brano['ruolo'])}}}\n\n"
            else:
                # Evento singolo
                organico = event.get('organico', '')
                if 'collaboratori' in event:
                    organico += f" (con {event['collaboratori']})" if organico else f"Con {event['collaboratori']}"
                
                programma = event.get('note', f"{event['tipo']} - {event['ruolo']}")
                if 'compositore' in event and event['compositore'] != event.get('ruolo'):
                    programma = f"Opera di {event['compositore']} - {programma}"
                
                titolo = event.get('titolo', event.get('evento', ''))
                
                latex += f"\\artisticevent{{{event['data']}}}{{{event['venue']}}}{{{event['organizzatore']}}}{{{titolo}}}{{{organico}}}{{{programma}}}\n\n"
        
        return latex
    
    def generate_languages(self) -> str:
        """Genera la sezione lingue"""
        if 'lingue' not in self.data:
            return ""
        
        latex = "% --- Lingue ---\n\\section*{Lingue}\n"
        
        lang_strings = []
        for lang in self.data['lingue']:
            lang_strings.append(f"{lang['nome']}: {lang['livello']}")
        
        latex += " \\\\\\\\ ".join(lang_strings) + "\n\n"
        return latex
    
    def generate_gdpr(self) -> str:
        """Genera la sezione consenso GDPR"""
        return "% --- Consenso GDPR ---\n\\section*{Consenso}\nAutorizzo il trattamento dei dati ai sensi del Reg. UE 2016/679.\n"
    
    def generate_latex_data(self) -> str:
        """Genera il file cv_data.tex completo"""
        latex = "% File: cv_data.tex (generato automaticamente)\n\n"
        
        latex += self.generate_personal_data()
        latex += self.generate_skills()
        latex += self.generate_experiences()
        latex += self.generate_education()
        latex += self.generate_artistic_events()
        latex += self.generate_languages()
        latex += self.generate_gdpr()
        
        return latex
    
    def generate_main_tex(self, style: str = "european") -> str:
        """Genera il file principale LaTeX"""
        latex = f"""%!TEX root = CV_GIULIO_DE_MATTIA.tex
%!TEX TS-program = xelatex
%!TEX encoding = UTF-8 Unicode

\\documentclass[a4paper,10pt]{{article}}

% Stile scelto: {style}
\\usepackage{{style_{style}}}

\\begin{{document}}

% PRIMA definisci i dati
\\input{{cv_data.tex}}

% POI crea l'header
\\makeheader

\\end{{document}}
"""
        return latex
    
    def save_files(self, output_dir: str = ".", style: str = "european"):
        """Salva i file generati"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Genera cv_data.tex
        data_content = self.generate_latex_data()
        (output_path / "cv_data.tex").write_text(data_content, encoding='utf-8')
        
        # Genera file principale
        main_content = self.generate_main_tex(style)
        (output_path / "CV_GIULIO_DE_MATTIA.tex").write_text(main_content, encoding='utf-8')
        
        print(f"✅ File generati in {output_path}:")
        print(f"   - cv_data.tex")
        print(f"   - CV_GIULIO_DE_MATTIA.tex (stile: {style})")


def main():
    parser = argparse.ArgumentParser(description="Genera CV LaTeX da dati YAML")
    parser.add_argument("yaml_file", help="File YAML con i dati del CV")
    parser.add_argument("--style", choices=["academic", "european"], 
                       default="european", help="Stile del CV")
    parser.add_argument("--output", "-o", default=".", 
                       help="Directory di output")
    
    args = parser.parse_args()
    
    try:
        generator = CVGenerator(args.yaml_file)
        generator.save_files(args.output, args.style)
        
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