import pdfplumber
from datetime import datetime
import os
import pandas as pd

# Lista de feriados (adicione os feriados relevantes)
FERIADOS = [
    "01/01/2024",  # Ano Novo
    "12/02/2024",  # Carnaval
    "25/12/2024",  # Natal
    # Adicione outros feriados conforme necessário
]

def extrair_data_horarios(texto):
    # Extrai a data e os horários do texto
    linhas = texto.split('\n')
    horarios_por_dia = {}
    
    for linha in linhas:
        if "Registro de Ponto:" in linha:
            partes = linha.split()
            print(f"Partes da linha: {partes}")  # Adiciona o print das partes da linha
            
            # Ajuste para o formato: "Registro de Ponto: 12:30 - 17/02/2025"
            if len(partes) >= 6:  # Garante que a linha tem o formato esperado
                horario = partes[3]  # Horário (HH:MM)
                data_str = partes[5]  # Data (DD/MM/AAAA)
                
                try:
                    data = datetime.strptime(data_str, "%d/%m/%Y").date()
                    # Verifica se o horário é válido
                    datetime.strptime(horario, "%H:%M")
                except ValueError:
                    continue
                
                if data not in horarios_por_dia:
                    horarios_por_dia[data] = []
                horarios_por_dia[data].append(horario)
    
    print(f"Horários extraídos: {horarios_por_dia}")  # Adiciona o print dos horários extraídos
    return horarios_por_dia

def calcular_jornada_diaria(data):
    # Define a jornada diária com base no dia da semana e feriados
    if data.strftime("%d/%m/%Y") in FERIADOS or data.weekday() == 6:  # Domingo ou feriado
        return 8
    elif data.weekday() == 4:  # Sexta-feira
        return 8
    else:  # Segunda a quinta
        return 9

def calcular_tempo_almoco(horarios):
    # Calcula o tempo de almoço com base nos horários de saída e volta
    if len(horarios) == 4:  # Entrada, saída almoço, volta almoço, saída
        saida_almoco = datetime.strptime(horarios[1], "%H:%M")
        volta_almoco = datetime.strptime(horarios[2], "%H:%M")
        return (volta_almoco - saida_almoco).seconds / 3600  # Converte para horas
    return 1  # Assume 1 hora de almoço se não houver 4 registros

def calcular_horas_extras(horarios_por_dia):
    # Calcula as horas extras por dia
    horas_extras_totais = 0
    registros = []  # Lista para armazenar os registros de ponto
    
    for data, horarios in horarios_por_dia.items():
        if len(horarios) >= 2:  # Precisa ter pelo menos entrada e saída
            entrada = min(horarios)  # Horário mais cedo (entrada)
            saida = max(horarios)     # Horário mais tarde (saída)
            
            # Converte para objetos datetime
            entrada_time = datetime.strptime(entrada, "%H:%M").time()
            saida_time = datetime.strptime(saida, "%H:%M").time()
            
            # Calcula a diferença de horas
            horas_trabalhadas = (
                datetime.combine(data, saida_time) - datetime.combine(data, entrada_time)
            )
            horas_trabalhadas = horas_trabalhadas.seconds / 3600  # Converte para horas
            
            # Subtrai o tempo de almoço
            tempo_almoco = calcular_tempo_almoco(horarios)
            horas_trabalhadas -= tempo_almoco
            
            # Calcula horas extras
            jornada_diaria = calcular_jornada_diaria(data)
            horas_extras = max(horas_trabalhadas - jornada_diaria, 0)
            horas_extras_totais += horas_extras
            
            # Adiciona os registros à lista
            registros.append({
                "Data": data.strftime("%d/%m/%Y"),
                "Entrada": entrada,
                "Saída": saida,
                "Horas Trabalhadas": f"{horas_trabalhadas:.2f}",
                "Horas Extras": f"{horas_extras:.2f}"
            })
    
    return horas_extras_totais, registros

def processar_pdf(pdf_path):
    # Processa um único PDF e retorna os horários por dia
    with pdfplumber.open(pdf_path) as pdf:
        texto = ''
        for page in pdf.pages:
            texto += page.extract_text()
    
    print(f"Texto extraído do PDF {pdf_path}:\n{texto}\n")  # Adiciona o print do texto extraído
    
    horarios_por_dia = extrair_data_horarios(texto)
    return horarios_por_dia

def main(diretorio):
    # Lista todos os PDFs no diretório e processa cada um
    horarios_por_dia = {}  # Dicionário para agrupar horários por dia
    todos_registros = []    # Lista para armazenar todos os registros
    
    print("PDFs encontrados no diretório:")
    for arquivo in os.listdir(diretorio):
        if arquivo.endswith(".pdf"):
            print(f"- {arquivo}")  # Exibe o nome do PDF
            caminho_completo = os.path.join(diretorio, arquivo)
            horarios_por_dia_pdf = processar_pdf(caminho_completo)
            
            for data, horarios in horarios_por_dia_pdf.items():
                if data not in horarios_por_dia:
                    horarios_por_dia[data] = []
                horarios_por_dia[data].extend(horarios)
    
    print(f"Horários por dia: {horarios_por_dia}")  # Adiciona o print dos horários por dia
    
    # Calcula as horas extras totais e obtém os registros
    horas_extras, registros = calcular_horas_extras(horarios_por_dia)
    print(f"Registros: {registros}")  # Adiciona o print dos registros
    todos_registros.extend(registros)
    
    # Cria um DataFrame com os registros
    df = pd.DataFrame(todos_registros)
    
    # Salva o DataFrame em um arquivo Excel
    excel_path = os.path.join(diretorio, "registros_ponto.xlsx")
    df.to_excel(excel_path, index=False)
    
    print(f"\nTotal de horas extras: {horas_extras:.2f} horas")
    print(f"Registros salvos em: {excel_path}")

if __name__ == "__main__":
    diretorio = r"C:\pontos"  # Substitua pelo caminho do diretório com os PDFs
    main(diretorio)