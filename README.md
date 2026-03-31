<<<<<<< HEAD
# 🤖 Agente Inteligente com Algoritmo A* (A-Estrela)

Sistema de navegação inteligente usando busca heurística A* para coleta de esferas em mapa 42×42.

---

## 📋 Descrição

Agente autônomo que:
- 🗺️ Navega em mapa com terrenos de diferentes custos
- 📡 Detecta esferas via radar de alcance limitado
- 🎯 Usa algoritmo A* para planejamento ótimo de rotas
- 🔄 Alterna entre exploração, coleta e retorno à base

---

## 🚀 Como Usar

### Execução
```bash
python agente_aestrela.py
```

O programa carrega automaticamente o mapa de `mapa.txt`.

### Editar Mapa
1. Abra `mapa.txt` em qualquer editor de texto
2. Modifique os valores:
   - `0` = Grama (custo 1) - Fácil de atravessar
   - `1` = Água (custo 10) - Custo médio
   - `2` = Montanha (custo 60) - Difícil de atravessar
3. Salve e execute novamente

---

## 📝 Formato do mapa.txt

Matriz 42×42 com valores separados por vírgulas:

```
0,0,0,1,1,1,0,0,2,2,0,...  (42 valores)
0,0,1,1,1,1,1,0,0,2,0,...  (42 valores)
0,0,0,0,0,0,0,0,0,0,0,...  (42 valores)
...
(42 linhas total)
```

---

## ⌨️ Controles

| Tecla | Ação |
|-------|------|
| **ESPAÇO** | Pausar/Retomar |
| **↑** | Acelerar simulação |
| **↓** | Desacelerar simulação |
| **ESC** | Sair |

---

## 🎨 Legenda Visual

| Cor | Elemento |
|-----|----------|
| 🟩 Verde escuro | Grama (custo 1) |
| 🟦 Azul | Água (custo 10) |
| ⬛ Cinza | Montanha (custo 60) |
| 🟨 Dourado | Agente |
| 🟣 Roxo pulsante | Esferas detectadas |
| 🟢 Verde claro | Esferas coletadas |
| 🔴 Vermelho | Base/Início |
| 🟡 Amarelo | Rastro do agente |

---

## 🧠 Algoritmo A*

### Heurística
- **Distância de Manhattan**: `h = |x₁ - x₂| + |y₁ - y₂|`
- **Admissível**: Nunca superestima o custo real

### Custo Total
- **f(n) = g(n) + h(n)**
  - `g(n)` = Custo acumulado do início até n
  - `h(n)` = Estimativa de custo de n até o objetivo

### Estrutura de Dados
- **Lista aberta**: Min-heap (heapq) - O(log n)
- **Lista fechada**: Set Python - O(1) para verificação

---

## 📊 Estatísticas

### Mapa Atual (mapa.txt)
- **Total**: 1764 células (42×42)
- **Grama**: 1053 células (~59.7%)
- **Água**: 599 células (~34.0%)
- **Montanha**: 112 células (~6.3%)

### Agente
- **Posição inicial**: (21, 21) - Centro do mapa
- **Radar**: Alcance 3 células (Manhattan)
- **Esferas**: 7 no total
- **Estados**: Explorando → Coletando → Retornando → Concluído

---

## 🛠️ Requisitos

### Instalação
```bash
pip install pygame
```

### Verificação
```bash
python -c "import pygame; print('Pygame OK!')"
```

---

## 📁 Estrutura de Arquivos

```
projetos/python/
├── agente_aestrela.py            # Ponto de entrada (main)
├── constantes.py                 # Constantes globais
├── nucleo_aestrela.py            # Algoritmo A* e utilitários de busca
├── util_mapa.py                  # Carregamento e validação do mapa
├── util_esferas.py               # Geração/validação das esferas
├── tela_menu.py                  # Tela inicial de configuração
├── logica_agente.py              # Lógica do agente inteligente
├── visualizador.py               # Renderização e painel com Pygame
├── mapa.txt                      # Mapa editável
└── README.md                     # Este arquivo
```

---

## 🎓 Conceitos de IA Implementados

### 1. Busca Heurística
- Algoritmo A* com heurística admissível
- Garantia de caminho ótimo

### 2. Conhecimento Parcial
- Agente não conhece posições das esferas
- Detecção via radar limitado
- Simulação de percepção sensorial

### 3. Planejamento Dinâmico
- Reavalia objetivos conforme detecta esferas
- Escolhe sempre a esfera de menor custo
- Adapta comportamento ao contexto

### 4. Estados e Transições
- **Explorando**: Varredura sistemática do mapa
- **Coletando**: Navegação otimizada até esferas
- **Retornando**: Caminho ótimo de volta à base

---

## 🔍 Detalhes Técnicos

### Custo de Movimento
```
Grama: 1 unidade
Água: 10 unidades (10× mais lento)
Montanha: 60 unidades (60× mais lento)
```

### Radar
- **Alcance**: 3 células (distância de Manhattan ≤ 3)
- **Cobertura**: ~37 células ao redor do agente
- **Atualização**: A cada passo

### Exploração
- **Padrão**: Varredura em serpentina
- **Passo**: 2×RADAR-1 (sem sobreposição excessiva)
- **Cobertura**: 100% do mapa

---

## 💡 Dicas de Uso

### Criar Desafios
- Use montanhas (2) para criar labirintos
- Use água (1) para simular rios e lagos
- Deixe grama (0) para áreas abertas

### Testar Performance
- Mapas com mais obstáculos = mais complexo
- Compare custo total em diferentes configurações
- Observe número de passos necessários

### Debugging
- Use ESPAÇO para pausar
- Observe o log de eventos no painel
- Verifique estatísticas finais no terminal

---

## 🐛 Solução de Problemas

### Erro: "Arquivo não encontrado: mapa.txt"
```
Solução: Verifique se mapa.txt está na mesma pasta que agente_aestrela.py
```

### Erro: "Número de linhas incorreto"
```
Solução: O arquivo deve ter exatamente 42 linhas
```

### Erro: "Linha X tem Y colunas"
```
Solução: Cada linha deve ter exatamente 42 valores separados por vírgulas
```

### Erro: "Valor inválido"
```
Solução: Use apenas 0, 1 ou 2 (sem espaços extras)
```

---

## 📚 Referências Acadêmicas

### Algoritmo A*
- Hart, P. E., Nilsson, N. J., & Raphael, B. (1968). "A Formal Basis for the Heuristic Determination of Minimum Cost Paths". IEEE Transactions on Systems Science and Cybernetics.

### Busca Heurística
- Russell, S., & Norvig, P. (2020). "Artificial Intelligence: A Modern Approach" (4th ed.). Pearson.

---

## 🎯 Objetivos de Aprendizado

Ao usar este projeto, você aprenderá:

✓ Implementação prática do algoritmo A*
✓ Uso de heurísticas admissíveis
✓ Estruturas de dados para busca eficiente
✓ Planejamento de agentes inteligentes
✓ Conhecimento parcial e exploração
✓ Visualização de algoritmos de IA

---

## 📄 Licença

Projeto educacional - Livre para uso acadêmico

---

## 👤 Autor

Desenvolvido para disciplina de Inteligência Artificial

---

**Versão**: 1.0 (Simplificada)
**Última atualização**: 25/03/2026
=======

---

## 🗺️ Estrutura do Mapa

O mapa é uma grade `42x42`, onde cada célula representa um tipo de terreno:

| Terreno   | Código | Custo |
|----------|--------|------|
| Grama    | 0      | 1    |
| Água     | 1      | 10   |
| Montanha | 2      | 60   |

---

## 🧭 Algoritmo A*

O A* é responsável por encontrar o melhor caminho entre dois pontos.

### Função de custo:


f(n) = g(n) + h(n)


- `g(n)` → custo do caminho até o nó
- `h(n)` → heurística (distância de Manhattan)

### Heurística utilizada:


h = |x1 - x2| + |y1 - y2|


---

## ⚙️ Estrutura do Código

### 🔹 Classe `Node`

Representa um nó da busca A*:

- posição `(linha, coluna)`
- custo acumulado `g`
- heurística `h`
- custo total `f`
- ponteiro para o pai

---

### 🔹 Funções principais

#### `manhattan_distance(a, b)`
Calcula a heurística entre dois pontos.

---

#### `get_neighbors(pos, game_map)`
Retorna vizinhos válidos (cima, baixo, esquerda, direita).

---

#### `astar(start, goal, game_map)`
Implementa o algoritmo A*:

- Usa fila de prioridade (`heapq`)
- Mantém lista aberta e fechada
- Calcula o menor custo até o objetivo
- Reconstrói o caminho ao final

---

#### `load_map_from_txt(file_path)`
Carrega o mapa de um arquivo `.txt`.

Suporta:
- formato com vírgula: `0,1,2`
- formato direto: `012`

---

#### `validate_map(game_map)`
Valida se o mapa tem dimensão correta (42x42).

---

#### `generate_spheres()`
Gera esferas aleatórias no mapa.

---

#### `generate_spheres_fixed()`
Permite definir posições fixas manualmente.

---

## 📡 Sistema de Radar

O agente possui um radar com alcance:


RADAR_RANGE = 3


Ele utiliza isso para:

- Planejar a varredura do mapa
- Definir pontos estratégicos (waypoints)
- Garantir cobertura eficiente

---

## 🔄 Estratégia de Varredura

O agente percorre o mapa em padrão **zig-zag (lawn mower)**:

- Vai linha por linha
- Alterna direção (direita ↔ esquerda)
- Usa espaçamento baseado no radar

Isso reduz o custo total da exploração.

---

## 🖥️ Interface Gráfica

O projeto usa **Pygame** para visualização:

- Mapa colorido por terreno
- Agente animado
- Radar visível
- Esferas destacadas
- Painel lateral com informações

---

## 🎮 Menu Interativo

Antes da execução, o usuário pode escolher:

- 🔀 Modo aleatório (esferas aleatórias)
- 📍 Modo fixo (definir posições manualmente)

---

## ▶️ Como Executar

### 1. Instalar dependências

```bash
pip install pygame
2. Executar o programa
python astar_agent.py
>>>>>>> 93be8690ece60e96a156c823da0b7d2499be1218
