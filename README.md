# Gêmeo Digital da Biblioteca (Projeto 3D)

Este projeto é um sistema de gerenciamento de acervo 3D integrado ao Streamlit. Ele permite visualizar a estante de livros em um ambiente tridimensional e realizar buscas inteligentes com destaque visual no modelo 3D.

## Funcionalidades
- **Visualização 3D:** Renderização da estante utilizando `model-viewer`.
- **Busca Inteligente:** Autocompletar para Título e Autor, com destaque visual em tempo real.
- **Destaque Dinâmico:** Os livros filtrados mudam de cor (vermelho para selecionado, azul para os demais) diretamente no modelo GLB.

## Como rodar
1. Instale as dependências:
   ```bash
   pip install -r requirements.txt

   Notas Técnicas (Modelo 3D)

O modelo 3D foi desenvolvido no Blender.
A estrutura foi otimizada com a aplicação de materiais únicos para cada componente (forma da estante, prateleiras individuais 
e livros (com materiais diferentes para capas e espinhas),
permitindo que o sistema identifique cada livro individualmente para a aplicação de filtros dinâmicos via model-viewer.

   Execute o projeto:

Bash
streamlit run app3d.py
Estrutura
app3d.py: Script principal.

static/: Contém o arquivo estante.glb.

Biblioteca Crounel - Página1.csv: Base de dados.
