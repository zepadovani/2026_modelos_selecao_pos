# Este script gera o material em outro repositorio

import os
import subprocess
import shutil
import sys

def main():
    # Caminhos
    current_dir = os.getcwd()
    # O diretório onde está o script a ser executado: ../2026_ideias_novo_processoseletivo/
    target_project_relative_path = "../2026_PPGMUS_estudo_processoseletivo"
    target_project_dir = os.path.abspath(os.path.join(current_dir, target_project_relative_path))
    
    script_name = "03_html_slides.py"
    
    # O diretório fonte para cópia: ../2026_ideias_novo_processoseletivo/slides/html
    source_html_dir = os.path.join(target_project_dir, "slides", "html")
    
    # O diretório destino (raiz deste projeto)
    destination_dir = current_dir

    # 1. Executar o script no outro diretório
    print(f"--- Iniciando execução de {script_name} em {target_project_dir} ---")
    
    if not os.path.exists(target_project_dir):
        print(f"Erro: O diretório alvo não existe: {target_project_dir}")
        return

    try:
        # Executa o script python definindo o cwd como o diretório alvo
        result = subprocess.run(
            [sys.executable, script_name],
            cwd=target_project_dir,
            check=True,
            text=True
        )
        print("Script executado com sucesso.")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o script {script_name}: {e}")
        return
    except Exception as e:
        print(f"Erro inesperado ao tentar executar o script: {e}")
        return

    # 2. Copiar conteúdo para a raiz
    print(f"\n--- Copiando arquivos de {source_html_dir} para {destination_dir} ---")
    
    if not os.path.exists(source_html_dir):
        print(f"Erro: O diretório fonte de html não existe: {source_html_dir}")
        return

    try:
        # Itera sobre os itens no diretório fonte
        for item in os.listdir(source_html_dir):
            if item.startswith('.'):
                continue # Ignora arquivos ocultos se desejar, ou remova essa linha
                
            source_item = os.path.join(source_html_dir, item)
            dest_item = os.path.join(destination_dir, item)

            if os.path.isdir(source_item):
                # Se for diretório, copia recursivamente
                if os.path.exists(dest_item):
                    shutil.rmtree(dest_item)
                shutil.copytree(source_item, dest_item)
                print(f"Diretório copiado: {item}")
            else:
                # Se for arquivo, copia (sobrescreve se existir)
                shutil.copy2(source_item, dest_item)
                print(f"Arquivo copiado: {item}")
                
        print("Cópia concluída com sucesso.")

    except Exception as e:
        print(f"Erro durante a cópia dos arquivos: {e}")

    # 3. Copiar conf/version.json
    source_version_path = os.path.join(target_project_dir, "conf", "version.json")
    dest_version_path = os.path.join(destination_dir, "version.json")

    print(f"\n--- Copiando version.json ---")
    if os.path.exists(source_version_path):
        try:
            shutil.copy2(source_version_path, dest_version_path)
            print(f"Arquivo copiado com sucesso: version.json")
        except Exception as e:
            print(f"Erro ao copiar version.json: {e}")
    else:
        print(f"Aviso: Arquivo de versão não encontrado em {source_version_path}")

    # 4. Git operations: add, commit, push
    print(f"\n--- Executando comandos Git ---")
    try:
        # git add .
        subprocess.run(["git", "add", "."], check=True, cwd=destination_dir)
        print("Git add executado.")

        # git commit -m "Auto update: [Data]"
        # Verifica se há algo para commitar
        status_result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, cwd=destination_dir)
        if status_result.stdout.strip():
            commit_message = f"Auto update via script"
            subprocess.run(["git", "commit", "-m", commit_message], check=True, cwd=destination_dir)
            print(f"Git commit executado: {commit_message}")
            
            # git push
            # Assumindo que o remote 'origin' e branch padrão estão configurados
            subprocess.run(["git", "push"], check=True, cwd=destination_dir)
            print("Git push executado com sucesso para https://github.com/zepadovani/2026_modelos_selecao_pos")
        else:
            print("Nada para commitar (working tree clean).")

    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar comandos Git: {e}")
    except Exception as e:
        print(f"Erro inesperado no Git: {e}")

if __name__ == "__main__":
    main()
