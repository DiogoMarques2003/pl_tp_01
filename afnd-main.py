import json
import sys

afnd = None
graphviz = False
graphvizPath = ''
caminhoAFD = ''

# Ignorar o nome do arquivo dos args e ler os outros parametros
for i, arg in enumerate(sys.argv[1:], start=1):  #
    if arg == '-help':
        print('Forma de usar:')
        print('python afnd-main.py [afnd.json] -output \'string\'')
        print('python afnd-main.py [afnd.json] -graphviz')
        print('python afnd-main.py [afnd.json] -graphviz \'string\'')
        exit(0)
    elif arg.endswith('.json') and afnd is None:
        with open(arg, "r", encoding="utf-8") as f:
            afnd = json.load(f)
    elif arg == '-graphviz':
        graphviz = True
    elif sys.argv[i - 1] == '-graphviz' and not arg.startswith('-'):
        graphvizPath = arg
    elif sys.argv[i - 1] == '-output':
        caminhoAFD = arg

if afnd is None:
    print("Não passasste o arquivo do afd como argumento")
    exit(-1)

if graphviz == False and caminhoAFD == '':
    print("Tens de passar o parametro -output \'string\' ou -graphviz")
    exit(-1)
