# Grafos - Rede de Disciplinas e Pré-requisitos (Educação)
Projeto em Python que modela uma rede de disciplinas e pré-requisitos de um curso, com visualização em grafo.

Este projeto modela a grade curricular de um curso usando **grafos direcionados**.

Cada disciplina é um **vértice**, e cada relação de pré-requisito é uma **aresta**.

## 🧠 Funcionalidades

- Adicionar/remover disciplinas e pré-requisitos  
- Consultar pré-requisitos de uma disciplina  
- Verificar dependências entre duas matérias  
- Detectar ciclos (pré-requisitos inválidos)  
- Gerar a ordem de disciplinas (ordenação topológica)  
- Visualizar o grafo com layout hierárquico (sem cruzamento de arestas)

## 📂 Arquivo principal

**`grafo_disciplinas.py`**

Contém toda a implementação da classe `CurriculumGraph` e exemplos de uso.

## 📊 Visualização

Para gerar o grafo, e necessario instalar o Graphviz e o Matplotlib networkx:
pip install pygraphviz
pip install matplotlib networkx
