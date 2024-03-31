import json
import sys

er = None
arquivoSalvar = ''

# Ignorar o nome do arquivo dos args e ler os outros parametros
for i, arg in enumerate(sys.argv[1:], start=1):  #
    if arg == '-help':
        print('Forma de usar:')
        print('python er-main.py [er.json] --output \'string\'')
        exit(0)
    elif arg.endswith('.json') and er is None:
        with open(arg, "r", encoding="utf-8") as f:
            er = json.load(f)
    elif sys.argv[i - 1] == '--output':
        arquivoSalvar = arg


if er is None:
    print("Não passasste o arquivo da expressão regular como argumento")
    exit(-1)

if arquivoSalvar == '':
    print("Tens de passar o arquivo para salvar a conversão com o parametro --output \'string\'")
    exit(-1)
