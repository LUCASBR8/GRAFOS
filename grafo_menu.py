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
                distancia = float(distancia[:-2]) if len(distancia) >= 2 else 0.0
                grafo[origem][destino] = distancia
                vertices.add(origem)
                vertices.add(destino)
            else:
                print(
                    f"Erro na linha {linha_num}: A linha '{linha.strip()}' não possui o formato esperado (origem destino distância).")

    # Adiciona as arestas ausentes
    for v in vertices:
        if v not in grafo:
            grafo[v] = {}

    return grafo


def gerar_matriz_adjacencia(grafo):
    vertices = sorted(grafo.keys())
    tamanho = len(vertices)
    matriz = [[0] * tamanho for _ in range(tamanho)]

    indice_vertices = {v: i for i, v in enumerate(vertices)}

    for origem in grafo:
        for destino, distancia in grafo[origem].items():
            matriz[indice_vertices[origem]][indice_vertices[destino]] = distancia

    return matriz

def mostrar_matriz(matriz):
    for linha in matriz:
        print(" ".join(map(str, linha)))

def dfs(grafo, vertice, visitados):
    visitados.add(vertice)
    for vizinho in grafo[vertice]:
        if vizinho not in visitados:
            dfs(grafo, vizinho, visitados)

def verificar_conectividade(grafo):
    visitados = set()
    num_componentes = 0
    for vertice in grafo:
        if vertice not in visitados:
            dfs(grafo, vertice, visitados)
            num_componentes += 1

    if num_componentes == 1:
        return "C0", "O grafo não é conexo."
    elif num_componentes == 2:
        return "C1", "O grafo possui 2 componentes conexos."
    elif num_componentes == 3:
        return "C2", "O grafo possui 3 componentes conexos."
    else:
        return "C3", "O grafo possui mais de 3 componentes conexos."


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

    return grafo_reduzido

def mostrar_grafo2(grafo):
    for vertice, vizinhos in grafo.items():
        print(f"{vertice} -> {list(vizinhos.keys())}")

def mostrar_grafo3(grafo):
    for vertice, vizinhos in grafo.items():
        vizinhos_formatados = [str(v) for v in vizinhos]
        print(f"{vertice} -> {', '.join(vizinhos_formatados)}")
def mostrar_grafo4(grafo):
    for origem in grafo:
        for destino, peso in grafo[origem].items():
            print(f"{origem} -> {destino} : {peso}")

def ler_grafo(arquivo):
    with open(arquivo, 'r') as f:
        conteudo = f.read().splitlines()
    grafo = {}
    for linha in conteudo:
        vertice, *arestas = linha.split()
        grafo[vertice] = arestas
    return grafo

def gravar_grafo(arquivo, grafo):
    with open(arquivo, 'w') as f:
        for vertice, arestas in grafo.items():
            f.write(f"{vertice} {' '.join(arestas)}\n")

def inserir_vertice(grafo, vertice):
    if vertice not in grafo:
        grafo[vertice] = []

def inserir_aresta(grafo, inicio, fim):
    if inicio in grafo:
        grafo[inicio].append(fim)

def remover_vertice(grafo, vertice):
    if vertice in grafo:
        del grafo[vertice]

def remover_aresta(grafo, inicio, fim):
    if inicio in grafo:
        grafo[inicio].remove(fim)

def mostrar_grafo(grafo):
    with open('grafo.txt', 'r') as f:
        for linha in f:
            print(linha.strip())  # strip() remove espaços em branco e quebras de linha extras

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
        opcao = input("Escolha uma opção: ")

        if opcao == 'a':
            grafo = ler_grafo('grafo.txt')
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
            mostrar_grafo(grafo)
        elif opcao == 'h':
            mostrar_grafo(grafo)
        elif opcao == 'i':
            # Aqui você pode implementar a lógica para verificar a conexidade do grafo e apresentar o grafo reduzido

            nome_arquivo = "grafo.txt"
            grafo = ler_grafo2(nome_arquivo)
            matriz_adjacencia = gerar_matriz_adjacencia(grafo)
            mostrar_matriz(matriz_adjacencia)
            categoria, comentario = verificar_conectividade(grafo)
            print(f"Categoria: {categoria}")
            print(f"Comentário: {comentario}")
            grafo_reduzido = criar_grafo_reduzido(grafo)
            print("Grafo Original:")
            mostrar_grafo4(grafo)
            print("\nGrafo Reduzido:")
            print("\nNo código que estamos utilizando, o tipo de redução de grafo realizado é a contração de vértices. ")
            print("\nNa contração de vértices, os vértices que estão conectados por uma")
            print("\naresta no grafo original são combinados em um único vértice no grafo reduzido. ")
            print("\nIsso reduz o número de vértices no grafo e simplifica sua estrutura, ")
            print("\nmas mantém a conectividade entre os vértices.")
            #Na implementação que estamos fazendo,
            # a função contrair_grafo realiza a contração de vértices para
            # criar o grafo reduzido a partir do grafo original.
            # Ela percorre todas as arestas do grafo original e combina
            # os vértices conectados em um novo grafo reduzido,
            # mantendo as informações sobre os pesos das arestas.



            mostrar_grafo4(grafo_reduzido)

            pass
        elif opcao == 'j':
            print("Aplicação encerrada.")
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()









