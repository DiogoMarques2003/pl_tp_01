import json
import sys

afnd = None
graphviz = False
graphvizPath = ''
caminhoAFD = ''

# Ignorar o nome do arquivo dos args e ler os outros parametros
for i, arg in enumerate(sys.argv[1:], start=1):
    if arg == '-help':
        print('Forma de usar:')
        print('python afnd_main.py [afnd.json] -output \'string\'')
        print('python afnd_main.py [afnd.json] -graphviz')
        print('python afnd_main.py [afnd.json] -graphviz \'string\'')
        exit(0)
    elif arg.endswith('.json') and afnd is None:
        with open(arg, "r", encoding="utf-8") as f:
            afnd = json.load(f)
    elif arg == '-graphviz':
        graphviz = True
    elif sys.argv[i - 1] == '-graphviz' and not arg.startswith('-'):
        graphvizPath = arg
    elif sys.argv[i - 1] == '-output' and (not arg.startswith('-') and arg.endswith('.json')):
        caminhoAFD = arg

if afnd is None:
    print("Não passasste o arquivo do afnd como argumento")
    exit(-1)

if graphviz == False and caminhoAFD == '':
    print("Tens de passar o parametro -output \'string\' ou -graphviz")
    exit(-1)

# definição do Autómato Finito não determinísto
#    AF=(V,Q,delta,q0,F) tal que:
V = set(afnd["V"])
Q = set(afnd["Q"])
delta = afnd["delta"]
q0 = afnd["q0"]
F = set(afnd["F"])


# Converter o AFND para AFD
def convertAFNDtoAFD(caminho: str):
    # Iniciar as variáveis
    simbolos = V
    estadoInicial = q0
    estados = [estadoInicial]
    transicoes = {}
    estadosFinais = []

    # Adicionar o estado inicial a fila
    fila = [estadoInicial]

    # Enquanto a fila tiver dados continuar o loop
    while len(fila) != 0:
        # Pegar no 1º dado da fila
        estadoAtual = fila.pop()

        for simbolo in simbolos:
            novoEstado = set()
            estadosVerificar = estadoAtual.split(',')

            # Verificar se os estados estão nas transições do AFND, se tiver adicionar ao novoEstado o simbolo
            for estado in estadosVerificar:
                if estado in delta and simbolo in delta[estado]:
                    novoEstado.update(delta[estado][simbolo])

            # Gerar o novo estado juntando as todos os simbolos por ","
            novoEstado = ','.join(sorted(novoEstado))
            # Se existir novoEstado e o mesmo não estiver nos estados adicionar a fila e aos estados
            if novoEstado and novoEstado not in estados:
                estados.append(novoEstado)
                fila.append(novoEstado)

            # Se o estado atual não estiver nas transições criar um json vazio para esse estado
            if estadoAtual not in transicoes:
                transicoes[estadoAtual] = {}
            # Adicionar o novo estado ao simbolo
            transicoes[estadoAtual][simbolo] = novoEstado

            # Se o novo estado for um estado final e ainda não tiver no array de estados finais adicionar
            if any(estadoFinal in novoEstado for estadoFinal in F):
                if novoEstado not in estadosFinais:
                    estadosFinais.append(novoEstado)

    # Gerar o json do AFD
    afd = {
        "V": list(simbolos),
        "Q": estados,
        "delta": transicoes,
        "q0": estadoInicial,
        "F": estadosFinais
    }

    # Salvar o arquivo
    f = open(caminho, "w")
    json.dump(afd, f, indent=4)
    f.close()
    print("Arquivo gerado com sucesso!")


# Gerar o grafico graphviz
def graphviz_gen(caminho: str):
    # Defenir a estrutura inicial
    graphviz_str = "digraph {\n"
    graphviz_str += "\tnode [shape = doublecircle]; " + " ".join(F) + ";\n"  # Pontos onde o diagrama termina acho
    graphviz_str += "\tnode [shape = point]; initial;\n"  # Iniciar o diagrama com um ponto
    graphviz_str += "\tnode [shape = circle];\n\n"  # O formato dos pontos deve ser um circulo
    graphviz_str += "\tinitial -> " + q0 + ";\n"  # Defenir o ponto inicial

    # Percorrer os itens do delta e adicionar
    for estado, transicoes in delta.items():
        graphviz_str += "\t"
        for simbolo, estadosDestino in transicoes.items():
            for estadoDestino in estadosDestino:
                graphviz_str += "" + estado + " -> " + estadoDestino + " [label=\"" + simbolo + "\"]; "
        graphviz_str += "\n"

    # Fechar arquivo
    graphviz_str += "}"

    if caminho == '':
        print(graphviz_str)
    else:
        f = open(graphvizPath, "w")
        f.write(graphviz_str)
        f.close()
        print("Arquivo gerado com sucesso!")


if graphviz == True:
    graphviz_gen(graphvizPath)

if caminhoAFD != '':
    convertAFNDtoAFD(caminhoAFD)
