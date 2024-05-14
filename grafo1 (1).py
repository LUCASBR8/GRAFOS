#!/usr/bin/env python
# coding: utf-8

# In[1]:


def ler_grafo2(nome_arquivo):
    grafo = {}
    vertices = set()
    with open(nome_arquivo, 'r') as arquivo:
        linhas = arquivo.readlines()
        for linha_num, linha in enumerate(linhas, start=1):
            valores = linha.split()
            if len(valores) == 3:
                origem, destino, distancia = valores
                if origem not in grafo:
                    grafo[origem] = {}
                if destino not in grafo:
                    grafo[destino] = {}
                # Removendo "km" dos valores de distância e convertendo para float
                distancia = float(distancia)
                grafo[origem][destino] = distancia
                grafo[destino][origem] = distancia
                vertices.add(origem)
                vertices.add(destino)
            else:
                print(f"Erro na linha {linha_num}: A linha '{linha.strip()}' não possui o formato esperado (origem destino distância).")

    return grafo


# In[2]:


def gerar_matriz_adjacencia(grafo):
    vertices = sorted(grafo.keys())
    tamanho = len(vertices)
    matriz = [[0] * tamanho for _ in range(tamanho)]

    indice_vertices = {v: i for i, v in enumerate(vertices)}

    for origem in grafo:
        for destino, distancia in grafo[origem].items():
            matriz[indice_vertices[origem]][indice_vertices[destino]] = distancia

    return matriz


# In[3]:


def mostrar_matriz(matriz):
    for linha in matriz:
        print(" ".join(map(str, linha)))


# In[4]:


def dfs(grafo, vertice, visitados):
    stack = [vertice]
    while stack:
        v = stack.pop()
        if v not in visitados:
            visitados.add(v)
            for vizinho in grafo[v]:
                if vizinho not in visitados:
                    stack.append(vizinho)


# In[5]:


def verificar_conectividade(grafo):
    visitados = set()
    num_componentes = 0
    
    for vertice in grafo:
        if vertice not in visitados:
            dfs(grafo, vertice, visitados)
            num_componentes += 1

    if num_componentes == 1:
        return "C1", "O grafo é conexo."
    else:
        return "C0", f"O grafo possui {num_componentes} componentes desconexos."


# In[6]:


def conectar_componentes(grafo):
    visitados = set()
    componentes = []

    # Encontra os componentes conectados
    for vertice in grafo:
        if vertice not in visitados:
            componente = set()
            dfs(grafo, vertice, componente)
            componentes.append(componente)
            visitados.update(componente)

    # Conecta os componentes desconexos
    for i in range(len(componentes) - 1):
        componente_atual = componentes[i]
        proximo_componente = componentes[i + 1]
        v1 = next(iter(componente_atual))
        v2 = next(iter(proximo_componente))
        grafo[v1][v2] = 1.0
        grafo[v2][v1] = 1.0

    return grafo


# In[7]:


def criar_grafo_reduzido(grafo):
    grafo_reduzido = {}
    mapeamento = {}
    novo_vertice = 1

    for origem in grafo:
        if origem not in mapeamento:
            mapeamento[origem] = novo_vertice
            novo_vertice += 1

        for destino in grafo[origem]:
            if destino not in mapeamento:
                mapeamento[destino] = novo_vertice
                novo_vertice += 1

            vertice_origem = mapeamento[origem]
            vertice_destino = mapeamento[destino]

            if vertice_origem not in grafo_reduzido:
                grafo_reduzido[vertice_origem] = {}

            if vertice_destino not in grafo_reduzido[vertice_origem]:
                grafo_reduzido[vertice_origem][vertice_destino] = grafo[origem][destino]
            else:
                grafo_reduzido[vertice_origem][vertice_destino] += grafo[origem][destino]

    # Adicionar vértices que não estão conectados a nenhuma aresta
    for vertice in mapeamento.values():
        if vertice not in grafo_reduzido:
            grafo_reduzido[vertice] = {}

    # Garantir conexão entre Cubatão, Capuava e Paulínia
    if 100 in grafo_reduzido and 200 in grafo_reduzido:
        grafo_reduzido[100][200] = 65.1
        grafo_reduzido[200][100] = 65.1

    if 200 in grafo_reduzido and 300 in grafo_reduzido:
        grafo_reduzido[200][300] = 155
        grafo_reduzido[300][200] = 155

    if 100 in grafo_reduzido and 300 in grafo_reduzido:
        grafo_reduzido[100][300] = 193
        grafo_reduzido[300][100] = 193

    return grafo_reduzido


# In[8]:


def dijkstra(grafo, origem):
    if origem not in grafo:
        raise ValueError(f"O vértice {origem} não existe no grafo.")
    
    distancias = {vertice: float('inf') for vertice in grafo}
    predecessores = {vertice: None for vertice in grafo}
    distancias[origem] = 0
    visitados = set()
    nao_visitados = set(grafo.keys())

    while nao_visitados:
        menor_vertice = min(nao_visitados, key=lambda vertice: distancias[vertice])
        visitados.add(menor_vertice)
        nao_visitados.remove(menor_vertice)

        for vizinho, distancia in grafo[menor_vertice].items():
            if vizinho not in visitados:
                nova_distancia = distancias[menor_vertice] + distancia
                if nova_distancia < distancias[vizinho]:
                    distancias[vizinho] = nova_distancia
                    predecessores[vizinho] = menor_vertice

    return distancias, predecessores


# In[9]:


def encontrar_caminho_minimo(origem, destino, predecessores):
    caminho = []
    atual = destino
    while atual != origem:
        caminho.insert(0, atual)
        atual = predecessores[atual]
    caminho.insert(0, origem)
    return caminho


# In[10]:


def menor_caminho(grafo, origem, destino):
    distancias, predecessores = dijkstra(grafo, origem)
    caminho_curto = encontrar_caminho_minimo(origem, destino, predecessores)

    if distancias[destino] == float('inf'):
        return float('inf'), []
    else:
        return distancias[destino], caminho_curto


# In[11]:


def colorir_vertices(grafo):
    cores = {}  # Dicionário para armazenar os vértices coloridos por cada cor
    cores_disponiveis = ['preto', 'amarelo', 'verde', 'roxo', 'vermelho']

    for vertice in grafo:
        vizinhos_coloridos = [cores.get(vizinho) for vizinho in grafo[vertice] if vizinho in cores]
        cor_disponivel = None

        for cor in cores_disponiveis:
            if cor not in vizinhos_coloridos:
                cor_disponivel = cor
                break

        if cor_disponivel is None:
            cor_disponivel = cores_disponiveis[0]

        cores[vertice] = cor_disponivel

    return cores


# In[12]:


def imprimir_cores(cores):
    cores_por_cor = {}
    for vertice, cor in cores.items():
        if cor not in cores_por_cor:
            cores_por_cor[cor] = []
        cores_por_cor[cor].append(vertice)
    
    print("\nVértices coloridos:")
    for cor, vertices in cores_por_cor.items():
        vertices_str = ", ".join(vertices)
        print(f"{cor} = {{{vertices_str}}}" if vertices else f"{cor} = {{}}")


# In[13]:


def calcular_graus(grafo):
    graus = {vertice: 0 for vertice in grafo}
    for vertice in grafo:
        graus[vertice] = len(grafo[vertice])
    return graus


# In[14]:


def imprimir_graus(graus):
    print("\nGraus dos vértices:")
    for vertice, grau in graus.items():
        print(f"Vértice {vertice}: Grau {grau}")


# In[15]:


def verificar_propriedades(grafo):
    euleriano = True
    hamiltoniano = True

    for vertice in grafo:
        if len(grafo[vertice]) % 2 != 0:
            euleriano = False

    grau_maximo = max(len(vizinhos) for vizinhos in grafo.values())
    if grau_maximo < len(grafo) - 1:
        hamiltoniano = False

    return euleriano, hamiltoniano


# In[16]:


def imprimir_propriedades(euleriano, hamiltoniano):
    if euleriano and hamiltoniano:
        print("O grafo é euleriano e hamiltoniano.")
    elif euleriano:
        print("O grafo é euleriano, mas não é hamiltoniano.")
    elif hamiltoniano:
        print("O grafo é hamiltoniano, mas não é euleriano.")
    else:
        print("O grafo não é euleriano nem hamiltoniano.")


# In[17]:


def mostrar_grafo2(grafo):
    for vertice, vizinhos in grafo.items():
        print(f"{vertice} -> {list(vizinhos.keys())}")


# In[18]:


def mostrar_grafo3(grafo):
    for vertice, vizinhos in grafo.items():
        vizinhos_formatados = [str(v) for v in vizinhos]
        print(f"{vertice} -> {', '.join(vizinhos_formatados)}")


# In[19]:


def mostrar_grafo4(grafo):
    for origem in grafo:
        for destino, peso in grafo[origem].items():
            print(f"{origem} -> {destino} : {peso}")


# In[20]:


def ler_grafo(arquivo):
    with open(arquivo, 'r') as f:
        conteudo = f.read().splitlines()
    grafo = {}
    for linha in conteudo:
        vertice, *arestas = linha.split()
        grafo[vertice] = arestas
    return grafo


# In[21]:


def gravar_grafo(arquivo, grafo):
    with open(arquivo, 'w') as f:
        for vertice, arestas in grafo.items():
            f.write(f"{vertice} {' '.join(arestas)}\n")


# In[22]:


def inserir_vertice(grafo, vertice):
    if vertice not in grafo:
        grafo[vertice] = []


# In[23]:


def inserir_aresta(grafo, inicio, fim):
    if inicio in grafo:
        grafo[inicio].append(fim)


# In[24]:


def remover_vertice(grafo, vertice):
    if vertice in grafo:
        del grafo[vertice]


# In[25]:


def remover_aresta(grafo, inicio, fim):
    if inicio in grafo:
        grafo[inicio].remove(fim)


# In[26]:


def mostrar_grafo(grafo):
    with open('grafo.txt', 'r') as f:
        for linha in f:
            print(linha.strip())  # strip() remove espaços em branco e quebras de linha extras


# In[27]:


def main():
    grafo = {}
    while True:
        print("\nMenu de opções:")
        print("a) Ler dados do arquivo grafo.txt")
        print("b) Gravar dados no arquivo grafo.txt")
        print("c) Inserir vértice")
        print("d) Inserir aresta")
        print("e) Remover vértice")
        print("f) Remover aresta")
        print("g) Mostrar conteúdo do arquivo")
        print("h) Mostrar grafo")
        print("i) Apresentar a conexidade do grafo")
        print("j) Encerrar a aplicação")
        print("1) Encontrar o menor caminho entre dois vértices")
        print("2) Coloração de vértices")
        print("3) Determinar grau dos vértices")
        print("4) Verificar se grafo é euleriano, hamiltoniano ou ambos")
        opcao = input("Escolha uma opção: ")

        if opcao == 'a':
            grafo = ler_grafo2('grafo.txt')
            print("Grafo lido do arquivo grafo.txt.")
        elif opcao == 'b':
            gravar_grafo('grafo.txt', grafo)
            print("Grafo gravado no arquivo grafo.txt.")
        elif opcao == 'c':
            vertice = input("Digite o vértice a ser inserido: ")
            inserir_vertice(grafo, vertice)
            print(f"Vértice {vertice} inserido com sucesso no grafo.")
        elif opcao == 'd':
            inicio = input("Digite o vértice de início da aresta: ")
            fim = input("Digite o vértice de fim da aresta: ")
            inserir_aresta(grafo, inicio, fim)
            print(f"Aresta de {inicio} para {fim} inserida com sucesso no grafo.")
        elif opcao == 'e':
            vertice = input("Digite o vértice a ser removido: ")
            remover_vertice(grafo, vertice)
            print(f"Vértice {vertice} removido com sucesso do grafo.")
        elif opcao == 'f':
            inicio = input("Digite o vértice de início da aresta a ser removida: ")
            fim = input("Digite o vértice de fim da aresta a ser removida: ")
            remover_aresta(grafo, inicio, fim)
            print(f"Aresta de {inicio} para {fim} removida com sucesso do grafo.")
        elif opcao == 'g':
            print("\nOs vértices que correspondem às refinarias são:")
            print("\n100 - Cubatão;")
            print("\n200 - Capuava;")
            print("\n300 - Paulínia")
            print('\n')
            mostrar_grafo(grafo)
        elif opcao == 'h':
            mostrar_grafo(grafo)
        elif opcao == 'i':
            nome_arquivo = "grafo.txt"
            grafo = ler_grafo2(nome_arquivo)
            categoria, comentario = verificar_conectividade(grafo)
            print(f"Categoria: {categoria}")
            print(f"Comentário: {comentario}")

            grafo_reduzido = criar_grafo_reduzido(grafo)
            print("\nOs vértices que correspondem às refinarias são:")
            print("\n100 - Cubatão;")
            print("\n200 - Capuava;")
            print("\n300 - Paulínia")
            print("\nGrafo Original:")
            mostrar_grafo4(grafo)
            print("\nGrafo Reduzido:")
            mostrar_grafo4(grafo_reduzido)
        elif opcao == 'j':
            print("Aplicação encerrada.")
            break
        elif opcao == '1':
            origem = input("Digite o vértice de origem: ")
            destino = input("Digite o vértice de destino: ")
            if origem in grafo and destino in grafo:
                distancia, caminho = menor_caminho(grafo, origem, destino)
                if distancia == float('infinity'):
                    print(f"Não há caminho entre {origem} e {destino}.")
                else:
                    print(f"Menor distância entre {origem} e {destino}: {distancia}")
                    print(f"Caminho: {' -> '.join(caminho)}")
            else:
                print("Um ou ambos os vértices não existem no grafo.")
        elif opcao == '2':
            cores = colorir_vertices(grafo)
            imprimir_cores(cores)
        elif opcao == '3':
            if grafo is None:
                print("Por favor, carregue um grafo primeiro.")
                continue
            graus = calcular_graus(grafo)
            imprimir_graus(graus)

        elif opcao == '4':
            if grafo is None:
                print("Carregue o grafo primeiro (opção 1).")
                continue

            graus = calcular_graus(grafo)

            euleriano, hamiltoniano = verificar_propriedades(grafo)
            imprimir_propriedades(euleriano, hamiltoniano)
        else:
            print("Opção inválida!")


# In[28]:


if __name__ == "__main__":
    main()


# In[ ]:



