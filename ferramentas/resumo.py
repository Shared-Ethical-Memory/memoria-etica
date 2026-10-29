#!/usr/bin/env python3
"""Resumo local, sem rede, das contribuições e avaliações registradas."""
from pathlib import Path
import csv
BASE = Path(__file__).resolve().parents[1]

def load(path):
    with (BASE / path).open(encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f))

contrib = load('dados/contribuicoes.csv')
vals = load('dados/avaliacoes.csv')
verified = [r for r in contrib if r['status_verificacao'].strip().lower() in ('verificado','verificada','sim')]
reviewed = [r for r in vals if r['revisao_humana_verificada'].strip().lower() in ('sim','verificado','verificada')]

def total_score(row):
    keys = ['nota_afetados_0a2','nota_danos_0a2','nota_alternativas_0a2','nota_limites_0a2']
    try:
        scores = [int(row[k]) for k in keys]
        return sum(scores) if all(0 <= x <= 2 for x in scores) else None
    except (ValueError,TypeError):
        return None

scored = [(r, total_score(r)) for r in reviewed]
scored = [(r,v) for r,v in scored if v is not None]
print('# Situação da Memória Ética Compartilhada')
print('Contribuições registradas:', len(contrib))
print('Contribuições com verificação declarada:', len(verified))
print('Avaliações registradas:', len(vals))
print('Avaliações com revisão humana declarada:', len(reviewed))
print('Avaliações com nota válida:', len(scored))
for condition in ['sem_memoria','com_memoria']:
    grades = [s for r,s in scored if r['condicao'].strip() == condition]
    print(f'Média {condition}: {sum(grades)/len(grades):.2f}/8 ({len(grades)} amostras)' if grades else f'Média {condition}: sem dados')
print('Atenção: esta ferramenta só conta entradas; não valida links, identidades ou qualidade metodológica.')
