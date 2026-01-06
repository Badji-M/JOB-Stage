import pandas as pd
import os

# Load data
base_score_indicateur = pd.read_stata('base_score_indicateur.dta')
base_score_final = pd.read_stata('base_score_final.dta')

print("Colonnes disponibles:")
print(base_score_indicateur.columns.tolist())
print("\nAperçu des données:")
print(base_score_indicateur.head())

# Generate LaTeX tables for each ODD
output = []

for odd_num in range(1, 18):
    odd_str = f'ODD{odd_num}'
    
    try:
        # Get global score
        odd_global = base_score_final[base_score_final['ODD'] == odd_str]['score'].values[0]
        
        # Get indicators sorted by score
        odd_indicators = base_score_indicateur[base_score_indicateur['ODD'] == odd_str].copy()
        odd_indicators = odd_indicators.sort_values('score')
        
        num_indicators = len(odd_indicators)
        
        # Start LaTeX section
        latex = f"\n\\section*{{Synthèse de la performance - {odd_str}}}\n\n"
        latex += f"Sur la base des indicateurs disponibles, l'évaluation de la performance du Sénégal par rapport aux objectifs de l'{odd_str} produit un \\textbf{{score global de {odd_global*100:.2f}\\%}}, reflétant une situation modérément favorable.\n\n"
        
        latex += f"\\subsection*{{Performance par Indicateur}}\n\n"
        
        latex += f"\\begin{{figure}}[H]\n"
        latex += f"\t\\centering\n"
        latex += f"\t\\includegraphics[width=0.95\\textwidth]{{Pictures/graphs/{odd_str}_scores.png}}\n"
        latex += f"\t\\caption{{Performance par indicateur - {odd_str} (Score global: {odd_global*100:.2f}\\%)}}\n"
        latex += f"\t\\label{{fig:{odd_str.lower()}_scores}}\n"
        latex += f"\\end{{figure}}\n\n"
        
        # Table
        latex += f"\\begin{{table}}[H]\n"
        latex += f"\t\\caption{{Détails des indicateurs - {odd_str}}}\n"
        latex += f"\t\\centering\n"
        latex += f"\t\\small\n"
        latex += f"\t\\renewcommand{{\\arraystretch}}{{1.4}}\n"
        latex += f"\t\\begin{{tabularx}}{{0.85\\textwidth}}{{l l c c c}}\n"
        latex += f"\t\t\\rowcolor[HTML]{{003D82}}\n"
        latex += f"\t\t\\color{{white}}\\textbf{{Code}} & \\color{{white}}\\textbf{{Indicateur}} & \\color{{white}}\\textbf{{Valeur}} & \\color{{white}}\\textbf{{Cible}} & \\color{{white}}\\textbf{{Score}} \\\\\n"
        
        # Alternate row colors
        colors = ['F5F8FC', 'E8F0FF']
        for idx, (_, row) in enumerate(odd_indicators.iterrows()):
            code = row['code_ODD2'] if pd.notna(row['code_ODD2']) else ''
            description = row['description'] if pd.notna(row['description']) else ''
            valeur = f"{row['valeuractuelle']:.2f}" if pd.notna(row['valeuractuelle']) else ''
            cible = f"{row['CibleInternational']:.2f}" if pd.notna(row['CibleInternational']) else ''
            score = f"{row['score']:.2f}" if pd.notna(row['score']) else ''
            
            color = colors[idx % 2]
            latex += f"\t\t\\rowcolor[HTML]{{{color}}}\n"
            latex += f"\t\t{code} & {description} & {valeur} & {cible} & {score} \\\\\n"
        
        latex += f"\t\\end{{tabularx}}\n"
        latex += f"\t\\label{{tab:{odd_str.lower()}_detailed}}\n"
        latex += f"\\end{{table}}\n\n"
        
        # Analysis text
        latex += f"L'analyse du {odd_str} révèle un score global de {odd_global:.4f}, basé sur {num_indicators} indicateur(s). Les performances varient de {odd_indicators['score'].min():.2f} à {odd_indicators['score'].max():.2f}, montrant une certaine disparité dans la mise en oeuvre des cibles.\n\n"
        
        output.append(latex)
        print(f"[OK] {odd_str}: {num_indicators} indicateurs, score={odd_global:.4f}")
        
    except Exception as e:
        print(f"[ERROR] {odd_str}: {e}")

# Write to file
with open('odd_tables_latex.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output))

print("\nLaTeX tables generated in odd_tables_latex.txt")
