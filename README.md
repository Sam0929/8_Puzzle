# Puzzle Game

Este é um jogo de quebra-cabeça implementado em Python usando a biblioteca `Tkinter` para a interface gráfica e três algoritmos de resolução clássicos: **BFS (Busca em Largura)**, **DFS (Busca em Profundidade)** e **A* (A-estrela)**. O objetivo é reorganizar as peças do tabuleiro até atingir o estado final correto.

## Funcionalidades

- Interface gráfica amigável para manipulação do quebra-cabeça.
- Controle via botões e teclas (`W`, `A`, `S`, `D`).
- Três métodos de resolução automática: BFS, DFS e A*.
- Exibição do número de movimentos e estados visitados durante a resolução.
- Reinício do jogo a qualquer momento.
- Resolução automática com controle de velocidade.

## Instalação

Para rodar este projeto localmente, siga os passos abaixo:

1. Clone o repositório para sua máquina local:

    ```bash
    git clone https://github.com/Sam0929/8_Puzzle.git
    ```

2. Certifique-se de ter o Python instalado. Caso não tenha, faça o download [aqui](https://www.python.org/downloads/).

3. Instale a biblioteca `Tkinter` (se necessário). No Windows, ela já vem instalada com o Python, mas em outras plataformas você pode instalá-la com:

    ```bash
    sudo apt-get install python3-tk  # para Ubuntu/Debian
    ```

4. Navegue até o diretório do projeto e execute o arquivo principal:

    ```bash
    cd 8_Puzzle
    python main.py
    ```

## Como Jogar

1. Ao iniciar o jogo, um tabuleiro embaralhado será exibido. Seu objetivo é reorganizar as peças para atingir o estado final, movendo a peça vazia (representada como um espaço vazio).

2. Você pode mover as peças de quatro maneiras:
   - Usando os botões `Cima`, `Baixo`, `Esquerda` e `Direita`.
   - Ou usando as teclas `W`, `S`, `A`, `D` do teclado para movimentar a peça vazia.

3. Caso esteja com dificuldades, pode selecionar um dos métodos de solução no dropdown (BFS, DFS ou A*) para resolver o quebra-cabeça automaticamente. Você pode ajustar a velocidade da animação da solução com o slider.

4. O jogo também oferece um botão de "Reiniciar" para gerar um novo tabuleiro embaralhado e começar de novo.

## Algoritmos de Resolução

- **BFS (Busca em Largura)**: Explora todos os nós na mesma profundidade antes de avançar para a próxima, garantindo a solução com o menor número de movimentos.
- **DFS (Busca em Profundidade)**: Explora o caminho até o fim antes de voltar, podendo encontrar soluções mais rapidamente, mas nem sempre as mais curtas.
- **A* (A-estrela)**: Um algoritmo heurístico que prioriza os caminhos que parecem mais promissores, buscando um equilíbrio entre velocidade e eficiência.

## Heurística

Para o algoritmo A*, escolhemos a heurística da **Distância de Manhattan**. Essa heurística calcula a soma das distâncias verticais e horizontais de cada peça até sua posição correta no tabuleiro.

### Como Funciona a Distância de Manhattan

A Distância de Manhattan entre dois pontos $\((x_1, y_1)\)$ e $\((x_2, y_2)\)$ em um espaço bidimensional é dada pela fórmula:

$\text{Distância de Manhattan} = |x_1 - x_2| + |y_1 - y_2|$

No contexto do nosso jogo, isso significa que, para cada peça do quebra-cabeça, calculamos a distância até a posição que ela deve ocupar. A soma dessas distâncias para todas as peças fornece uma estimativa da "distância" total que ainda precisamos percorrer para resolver o quebra-cabeça. Essa estimativa ajuda o algoritmo A* a priorizar movimentos que se aproximam mais rapidamente da solução final, tornando a busca mais eficiente.

Dessa forma, a heurística da Distância de Manhattan contribui para encontrar a solução do quebra-cabeça com um menor número de movimentos possíveis.

## Requisito de Implementação

Para a implementação dos algoritmos de busca, estabelecemos o seguinte requisito:

### Estruturas de Dados e Implementação Iterativa

A implementação deve utilizar estruturas de dados e ser iterativa, ou seja, sem o uso de recursão. O seguinte laço deve ser seguido:

1. **Adicionar estado na estrutura**
2. **Enquanto a estrutura não estiver vazia:**
   - Remover o próximo estado da estrutura.
   - Avaliar o estado.
   - **Se o estado for o estado final:** mostrar a solução e encerrar o programa.
   - Adicionar os estados seguintes à estrutura.
3. **Retornar "Sem solução"** se não houver um estado final encontrado após a avaliação de todos os estados possíveis.

Esse requisito garante que o algoritmo de busca opere de maneira eficiente e controlada, evitando o consumo excessivo de memória que pode ocorrer com a recursão. Além disso, promove uma melhor compreensão do fluxo de execução e da lógica de busca, permitindo um gerenciamento mais claro dos estados explorados no quebra-cabeça.

## Contribuindo

Se você quiser contribuir com melhorias ou correções, siga os seguintes passos:

1. Faça um fork do repositório.
2. Crie um branch para sua modificação: `git checkout -b minha-modificacao`.
3. Faça suas alterações e commit: `git commit -m 'Minha modificação'`.
4. Envie o branch para o GitHub: `git push origin minha-modificacao`.
5. Abra um Pull Request no repositório original.

## Licença

Este projeto é distribuído sob a licença MIT. Para mais informações, consulte o arquivo [LICENSE](LICENSE).

---

Divirta-se jogando e aprimorando suas habilidades de resolução de problemas com este clássico jogo de quebra-cabeça!
