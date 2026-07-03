import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import os
import json

# 1. Configuração da página do Streamlit
st.set_page_config(page_title="Gêmeo Digital - Biblioteca", layout="wide")

st.title("Gerenciamento de Acervo 3D - Biblioteca")

# 2. Carregar a planilha de dados da biblioteca
@st.cache_data
def carregar_dados():
    try:
        df = pd.read_csv("Biblioteca Crounel - Página1.csv")
        df.columns = df.columns.str.strip()
        colunas_texto = ['Autor', 'Titulo', 'PalavrasChaves', 'ID_Livro']
        for col in colunas_texto:
            if col in df.columns:
                df[col] = df[col].fillna("").astype(str)
        return df
    except Exception as e:
        st.error(f"Erro ao carregar o CSV: {e}")
        return pd.DataFrame()

df_livros = carregar_dados()

if not df_livros.empty:
    # 3. Filtros na Barra Lateral com Sugestões Automáticas (Autocompletar)
    st.sidebar.header("Busca por Conteúdo")
    
    # Criamos listas exclusivas com valores únicos para as sugestões, adicionando uma opção vazia no início
    lista_titulos = [""] + sorted(list(df_livros['Titulo'].unique()))
    lista_autores = [""] + sorted(list(df_livros['Autor'].unique()))
    
    # O selectbox permite que o usuário digite para achar o nome semelhante
    busca_titulo = st.sidebar.selectbox("Título do Livro (Digite para sugerir):", options=lista_titulos, index=0)
    busca_autor = st.sidebar.selectbox("Nome do Autor (Digite para sugerir):", options=lista_autores, index=0)

    df_filtrado = df_livros.copy()
    if busca_titulo:
        df_filtrado = df_filtrado[df_filtrado['Titulo'] == busca_titulo]
    if busca_autor:
        df_filtrado = df_filtrado[df_filtrado['Autor'] == busca_autor]

    # 4. Exibição da Tabela
    st.subheader(f"Livros Encontrados ({len(df_filtrado)})")
    st.dataframe(df_filtrado, use_container_width=True)

    st.markdown("---")

    # 5. Visualizador 3D com Destaque em Vermelho e Fundo em Azul
    st.subheader("Visualização 3D da Estante")
    
    busca_ativa = 1 if (busca_titulo or busca_autor) else 0

    json_ativos = json.dumps(df_filtrado['ID_Livro'].tolist())
    json_todos = json.dumps(df_livros['ID_Livro'].tolist())

    gltf_path = os.path.join("static", "estante.glb")
    if os.path.exists(gltf_path):
        html_code = f"""
        <script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/3.5.0/model-viewer.min.js"></script>
        
        <model-viewer 
            id="biblioteca-3d"
            src="app/static/estante.glb" 
            camera-controls 
            touch-action="pan-y" 
            camera-orbit="90deg 75deg 105%" 
            field-of-view="30deg"
            style="width: 100%; height: 550px; background-color: #f0f2f6; border-radius: 10px;"
            shadow-intensity="1">
        </model-viewer>

        <script>
            const modelViewer = document.querySelector('#biblioteca-3d');
            
            const ativos = {json_ativos}.map(id => id.trim().toUpperCase());
            const todos = {json_todos}.map(id => id.trim().toUpperCase());
            const buscaAtiva = {busca_ativa};

            const ultimaOrbita = localStorage.getItem('camera_orbit_estante');
            if (ultimaOrbita) {{
                modelViewer.cameraOrbit = ultimaOrbita;
            }}

            modelViewer.addEventListener('camera-change', () => {{
                const orbitaAtual = modelViewer.getCameraOrbit();
                const orbitaString = `${{Math.round(orbitaAtual.theta * (180 / Math.PI))}}deg ${{Math.round(orbitaAtual.phi * (180 / Math.PI))}}deg ${{Math.round(orbitaAtual.radius * 100)}}%`;
                localStorage.setItem('camera_orbit_estante', orbitaString);
            }});

            function aplicarFiltroNos() {{
                const model = modelViewer.model;
                if (!model) return;

                const corEstanteLateral = [0.36, 0.25, 0.20, 1.0]; 
                const corPrateleiras    = [0.10, 0.10, 0.10, 1.0]; 
                
                const azulEscuroColuna    = [0.05, 0.25, 0.50, 1.0]; 
                const azulClaroLateral    = [0.55, 0.75, 0.95, 1.0]; 
                
                const vermelhoEscuroCol   = [0.55, 0.00, 0.00, 1.0]; 
                const vermelhoClaroLat    = [1.00, 0.40, 0.40, 1.0]; 

                model.materials.forEach((material) => {{
                    const nomeMat = material.name.trim().toUpperCase();
                    
                    if (nomeMat === "E1") {{
                        material.pbrMetallicRoughness.setBaseColorFactor(corEstanteLateral);
                        material.pbrMetallicRoughness.setRoughnessFactor(0.6);
                        return;
                    }}

                    if (nomeMat.startsWith("E1_P")) {{
                        material.pbrMetallicRoughness.setBaseColorFactor(corPrateleiras);
                        material.pbrMetallicRoughness.setRoughnessFactor(0.4);
                        return;
                    }}

                    const ehLateralPagina = nomeMat.includes("PAG");
                    const idCorrespondente = todos.find(id => nomeMat.includes(id));
                    
                    if (idCorrespondente) {{
                        if (buscaAtiva === 1) {{
                            const estaAtivo = ativos.includes(idCorrespondente);
                            
                            if (estaAtivo) {{
                                if (ehLateralPagina) {{
                                    material.pbrMetallicRoughness.setBaseColorFactor(vermelhoClaroLat);
                                }} else {{
                                    material.pbrMetallicRoughness.setBaseColorFactor(vermelhoEscuroCol);
                                }}
                            }} else {{
                                if (ehLateralPagina) {{
                                    material.pbrMetallicRoughness.setBaseColorFactor(azulClaroLateral);
                                }} else {{
                                    material.pbrMetallicRoughness.setBaseColorFactor(azulEscuroColuna);
                                }}
                            }}
                        }} else {{
                            if (ehLateralPagina) {{
                                material.pbrMetallicRoughness.setBaseColorFactor(azulClaroLateral);
                            }} else {{
                                material.pbrMetallicRoughness.setBaseColorFactor(azulEscuroColuna);
                            }}
                        }}
                    }}
                }});
            }}

            modelViewer.addEventListener('load', aplicarFiltroNos);
            setTimeout(aplicarFiltroNos, 500);
        </script>
        """
        components.html(html_code, height=570)
    else:
        st.error("Arquivo 'estante.glb' não encontrado na pasta 'static'.")
else:
    st.warning("Aguardando carregamento da base de dados CSV.")