# cliente_app.py
# Aplicação para consumir o Web Service de Gestão Ambiental (OGAS-API)

import requests
import json
import csv

BASE_URL = "http://127.0.0.1:5000"

def adicionar_indicador():
    """Adiciona um novo indicador ambiental."""
    print("\n--- Adicionar Novo Indicador ---")
    try:
        empresa = input("Nome da Empresa: ")
        ano = int(input("Ano de referência: "))
        consumo_agua = float(input("Consumo de água (m³): "))
        residuos = float(input("Geração de resíduos (ton): "))
        emissoes_co2 = float(input("Emissões de CO2 (ton): "))
        
        novo_indicador = {
            "empresa": empresa,
            "ano": ano,
            "consumo_agua_m3": consumo_agua,
            "residuos_ton": residuos,
            "emissoes_co2_ton": emissoes_co2
        }
        
        response = requests.post(f"{BASE_URL}/indicadores", json=novo_indicador)
        response.raise_for_status()
        print("Indicador adicionado com sucesso!")
        
    except (ValueError, requests.exceptions.RequestException) as e:
        print(f"Erro ao adicionar indicador: {e}")

def listar_indicadores():
    """Lista todos os indicadores cadastrados."""
    print("\n--- Lista de Indicadores ---")
    try:
        response = requests.get(f"{BASE_URL}/indicadores")
        response.raise_for_status()
        indicadores = response.json()
        
        for id, dados in indicadores.items():
            print(f"ID: {id} | Empresa: {dados['empresa']} | Ano: {dados['ano']}")
    
    except requests.exceptions.RequestException as e:
        print(f"Erro ao listar indicadores: {e}")

def buscar_indicador():
    """Busca e exibe um indicador específico."""
    print("\n--- Buscar Indicador por ID ---")
    try:
        id_busca = int(input("Digite o ID do indicador: "))
        response = requests.get(f"{BASE_URL}/indicadores/{id_busca}")
        response.raise_for_status()
        indicador = response.json()

        print(json.dumps(indicador, indent=2))

    except (ValueError, requests.exceptions.RequestException) as e:
        print(f"Erro ao buscar indicador: {e}")

def atualizar_indicador():
    """Atualiza os dados de um indicador."""
    print("\n--- Atualizar Indicador ---")
    try:
        id_atualiza = int(input("Digite o ID do indicador a ser atualizado: "))
        
        # Coleta dos novos dados
        novos_dados = {}
        novos_dados['empresa'] = input("Novo nome da empresa (deixe em branco para não alterar): ")
        novos_dados['ano'] = input("Novo ano (deixe em branco para não alterar): ")
        novos_dados['consumo_agua_m3'] = input("Novo consumo de água (deixe em branco para não alterar): ")
        novos_dados['residuos_ton'] = input("Nova geração de resíduos (deixe em branco para não alterar): ")
        novos_dados['emissoes_co2_ton'] = input("Novas emissões de CO2 (deixe em branco para não alterar): ")
        
        # Filtra e formata os dados
        payload = {k: (float(v) if k != 'empresa' and k != 'ano' else (int(v) if k == 'ano' else v)) for k, v in novos_dados.items() if v}
        
        if payload:
            response = requests.put(f"{BASE_URL}/indicadores/{id_atualiza}", json=payload)
            response.raise_for_status()
            print("Indicador atualizado com sucesso!")
        else:
            print("Nenhum dado fornecido para atualização.")
            
    except (ValueError, requests.exceptions.RequestException) as e:
        print(f"Erro ao atualizar indicador: {e}")


def deletar_indicador():
    """Deleta um indicador do sistema."""
    print("\n--- Deletar Indicador ---")
    try:
        id_deleta = int(input("Digite o ID do indicador a ser deletado: "))
        response = requests.delete(f"{BASE_URL}/indicadores/{id_deleta}")
        response.raise_for_status()
        print("Indicador deletado com sucesso!")
        
    except (ValueError, requests.exceptions.RequestException) as e:
        print(f"Erro ao deletar indicador: {e}")

def gerar_relatorio_csv():
    """Gera um relatório em formato CSV com todos os indicadores."""
    print("\n--- Gerando Relatório CSV ---")
    try:
        response = requests.get(f"{BASE_URL}/indicadores")
        response.raise_for_status()
        indicadores = response.json()
        
        with open('relatorio_ambiental.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'Empresa', 'Ano', 'Consumo de Água (m³)', 'Resíduos (ton)', 'Emissões de CO2 (ton)'])
            
            for id, dados in indicadores.items():
                writer.writerow([id, dados['empresa'], dados['ano'], dados['consumo_agua_m3'], dados['residuos_ton'], dados['emissoes_co2_ton']])
        
        print("Relatório 'relatorio_ambiental.csv' gerado com sucesso!")

    except requests.exceptions.RequestException as e:
        print(f"Erro ao gerar relatório: {e}")


def menu():
    """Exibe o menu principal e gerencia a entrada do usuário."""
    while True:
        print("\n===== Oficina de Gestão Ambiental Sustentável (OGAS) =====")
        print("1. Adicionar Indicador Ambiental")
        print("2. Listar Todos os Indicadores")
        print("3. Buscar Indicador por ID")
        print("4. Atualizar Indicador")
        print("5. Deletar Indicador")
        print("6. Gerar Relatório (CSV)")
        print("0. Sair")
        
        try:
            opcao = int(input("Escolha uma opção: "))
            
            if opcao == 1:
                adicionar_indicador()
            elif opcao == 2:
                listar_indicadores()
            elif opcao == 3:
                buscar_indicador()
            elif opcao == 4:
                atualizar_indicador()
            elif opcao == 5:
                deletar_indicador()
            elif opcao == 6:
                gerar_relatorio_csv()
            elif opcao == 0:
                break
            else:
                print("Opção inválida. Tente novamente.")
                
        except ValueError:
            print("Entrada inválida. Por favor, insira um número.")

if __name__ == "__main__":
    menu()