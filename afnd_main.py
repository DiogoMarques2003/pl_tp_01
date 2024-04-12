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
    # Iniciar as variáveis para construir o AFD
    simbolos = V # Símbolos do alfabeto
    estadoInicial = q0 # Estado inicial
    estados = [estadoInicial] # Listado dos estados
    transicoes = {} # Transições que constituem o AFD
    estadosFinais = [] # Lista dos estados finais

    # Usa uma fila para controlar os estados a serem processados
    fila = [estadoInicial]

    # Enquanto a fila tiver dados continuar o loop
    while len(fila) != 0:
        # Remove e retorna o primeiro estado da fila
        estadoAtual = fila.pop()

        # Para cada símbolo do alfabeto, tentar construir as transições do estado atual
        for simbolo in simbolos:
            # Conjunto para armazenar os estados utilizados pelo símbolo atual
            novoEstado = set()
            # Divide o estado atual nos seus componentes, por ex se tivermos o estado q1,q2 vamos ter os componentes q1 e q2
            estadosVerificar = estadoAtual.split('_')

            # Verifica as transições para cada componente do estado atual no AFND
            for estado in estadosVerificar:
                if estado in delta and simbolo in delta[estado]:
                    novoEstado.update(delta[estado][simbolo])

            # Gerar o novo estado juntando as todos os simbolos por ","
            novoEstado = '_'.join(sorted(novoEstado))

            # Se o novo estado for válido e ainda não estiver adicionado vai adicionar o mesmo a lista de estados e a fila para ser processado
            if novoEstado and novoEstado not in estados:
                estados.append(novoEstado)
                fila.append(novoEstado)

            # Se o estado atual não estiver nas transições criar um json vazio para esse estado
            if estadoAtual not in transicoes:
                transicoes[estadoAtual] = {}

            # Adiciona a transição do estado atual para o novo estado com símbolo atual
            transicoes[estadoAtual][simbolo] = novoEstado

            # Verifica se o novo estado contém algum estado final do AFND, se tiver adicionar o novo estado aos estados finais
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
    with open(caminho, "w") as f:
        json.dump(afd, f, indent=4)
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
