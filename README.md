# Cálculo de Horas Extras a partir de PDFs

## Descrição

Este projeto foi desenvolvido para calcular as horas extras trabalhadas a partir de registros de ponto armazenados em arquivos PDF. A necessidade surgiu devido à dificuldade de calcular manualmente as horas extras a partir de múltiplos PDFs contendo os registros de ponto.

## Funcionalidades

- Extração de dados de registros de ponto a partir de arquivos PDF.
- Cálculo de horas trabalhadas e horas extras com base nos registros extraídos.
- Geração de um relatório em formato Excel contendo os registros de ponto e as horas extras calculadas.

## Estrutura do Projeto

- `main.py`: Script principal que realiza a extração dos dados, cálculo das horas extras e geração do relatório.
- `FERIADOS`: Lista de feriados que são considerados no cálculo das horas extras.
- Funções principais:
  - `extrair_data_horarios(texto)`: Extrai a data e os horários do texto extraído dos PDFs.
  - `calcular_jornada_diaria(data)`: Define a jornada diária com base no dia da semana e feriados.
  - `calcular_tempo_almoco(horarios)`: Calcula o tempo de almoço com base nos horários de saída e volta.
  - `calcular_horas_extras(horarios_por_dia)`: Calcula as horas extras por dia.
  - `processar_pdf(pdf_path)`: Processa um único PDF e retorna os horários por dia.
  - `main(diretorio)`: Função principal que lista todos os PDFs no diretório, processa cada um e gera o relatório final.

## Como Usar

1. **Pré-requisitos**:
   - Python 3.11 ou superior.
   - Bibliotecas `pdfplumber` e `pandas` instaladas. Você pode instalá-las usando o comando:
     ```bash
     pip install pdfplumber pandas
     ```

2. **Configuração**:
   - Coloque todos os arquivos PDF contendo os registros de ponto em um diretório específico.
   - Atualize o caminho do diretório no script [main.py](http://_vscodecontentref_/0) na linha:
     ```python
     diretorio = r"C:\pontos"  # Substitua pelo caminho do diretório com os PDFs
     ```

3. **Execução**:
   - Execute o script [main.py](http://_vscodecontentref_/1):
     ```bash
     python main.py
     ```
   - O script irá processar todos os PDFs no diretório especificado, calcular as horas extras e gerar um arquivo Excel `registros_ponto.xlsx` com os registros de ponto e as horas extras calculadas.

## Exemplo de Uso

```python
if __name__ == "__main__":
    diretorio = r"C:\pontos"  # Substitua pelo caminho do diretório com os PDFs
    main(diretorio)