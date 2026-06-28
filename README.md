# trabalho-livro-ofertas

Este é o repositório do trabalho da disciplina SME0827 - Estrutura de Dados: Simulador de Livro de Ofertas e Performance de Estruturas

1. **Estrutura do repositório**
- .gitignore: define quais arquivos o Git não deve acompanhar (*track*);
- LICENSE: arquivo padrão de licença;
- main.py: apresenta o motor de match e a lógica principal da solução;
- performance_report.ipynb: relatório de performance, incluindo a análise de custo para inserção/busca em listas encadeadas e a análise empírica com visualizações de dados comparando o tempo de processamento conforme o volume de ordens cresce;
- README.md: arquivo com a documentação da solução;
- structs.py: script com a implementação das estruturas de dados solicitadas no trabalho - **lista encadeada**, **fila (_queue_)** e **pilha (_stack_)**;
- visualization.py: arquivo extra para visualização da solução em interface gráfica

2. **Esquema de branches**
Usamos branches de features por componente a ser desenvolvido por cada integrante do time. Após o desenvolvimento de cada funcionalidade, há o merge com a branch principal, que contém a solução final do trabalho.

3. **Dependências externas**
A utilização de dependências externas (PyQt6) e a necessidade de instalação de bibliotecas estão restritas **apenas** ao script extra. A solução principal do trabalho não necessita de nenhuma configuração ou instalação específica, basta apenas rodar os scripts e o notebook. As estruturas de dados foram implementadas "do zero" usando código Python "puro".

4. **Reprodutibilidade**
Além do presente repositório, a entrega final no Moodle inclui um arquivo compactado (.zip), contendo o presente repositório