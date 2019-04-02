# Nome: Emulador TTA (Transport Triggered Architecture)
# Criado por: Carlo Henrique FR
# Data: 30/03/2019
# Última revisão: 01/04/2019
# Versão: 0.4


# LISTA DE ENDEREÇOS INTERNOS.
# FFF0 - Registrador A.
# FFF1 - Registrador B.
# FFF2 - Registrador A+B (soma dos valores contidos em A e em B).
# FFF3 - Registrador /A (inverso de A).
# FFF4 - NDA
# FFF5 - NDA
# FFF6 - NDA
# FFF7 - NDA
# FFF8 - NDA
# FFF9 - NDA
# FFFA - NDA
# FFFB - NDA
# FFFC - Jump (mover qualquer valor para este endereço e o programa continua apartir desse endereço).
# FFFD - SIZ (skip if zero - Pula a proxima instruçao se o conteudo do regTemp for zero).
# FFFE - Out (sai com uma valor na tela).
# FFFF - Halt (para a execução do programa).



# EXEMPLO DE PROGRAMA. - Somador - 
# 0000:BBB7:    - Fonte da primeria instrução BBB7 na memória.
# 0001:FFF0:    - Destino do valor contido em BBB7, neste caso o destino é o registrador A.
# 0002:BBB8:    - Fonte da segunda instrução BBB8 na memória.
# 0003:FFF1:    - Destino do valor contido em BBB8, neste caso o destino é o registrador B.
# 0004:FFF2:    - Fonte da terceira instrução FFF2 registrador AB (A + B)
# 0005:FFFE:    - Destino do valor contido em FFF2, neste caso o destino é o registrador de saida.
# 0006:BBB9:    - Fonte da quarta instrução BBB9 na memória.
# 0007:FFFF:    - Destino do valor contido em BBB9, neste caso é o resistrador de parada.
# BBB7:5AB1:    - Valor armazenado em BBB7.
# BBB8:4AE4:    - Valor armazenado em BBB8.
# BBB9:FFFF:    - Valor armazenado em BBB9.


import time


FFFF = "0000"              # Endereço que para a execução do programa se for diferente de "0000h".
contadorPrograma = "0000"  # Endereço inicial do contador de programa sera em "0000h" (Será utilizado para buscar na memoria)
regFD = "0000"             # Registrador de fonte destino. 
regTemp = "0000"           # Registrador temporario de informaçoes.
memoria = {"FFF0":"0000","FFF1":"0000","FFF2":"0000"} # Memoria de dados e programa. Registradores já inicializados NÃO MODIFICAR.




# Buscando o programa no txt e salvando na memoria -- SÓ IRA EXECUTAR O PROGRAMA SE ESTIVER NO MESMO DIRETORIO --      
nomeArquivo = input("Digite o nome do arquivo que está o programa seguido de \".txt\": ")
try:
    arquivo = open(nomeArquivo, "r")      # Abre o arquivo como o nome especificado pelo usuario.
    listaPrograma = arquivo.readlines()   # Coloca o texto lido em uma lista, cada elemento é uma linha.
    for linha in listaPrograma:
        enderecoValor = linha.split(":")  # Ira separar os elementos pelo ":" -- FORMATO DE INSTRUÇAO => 0000:0001: --
        endereco = enderecoValor[0]       # Retirando o endereço a ser armazenado o valor.
        valor = enderecoValor[1]          # Retirando o valor a ser armazenado na memoria.
        memoria[endereco] = valor         # Salvando o valor no endereço especificado.

except:
    print("Arquivo não encontrado.")      # Caso o arquivo não exista encerre o programa.
    FFFF = "0001"
      
finally:
    arquivo.close()                       # De qualquer forma feche o arquivo txt.


# Criando atrasos para melhor apresentação.
time.sleep(2)
print("Valor carregado na memoria.")
time.sleep(2)
print("Preparando para executar.")
time.sleep(2)
print("Pronto.")
time.sleep(2)
print()


# Parte principal do programa, irá buscar as instrucões e malipular os dados 
while FFFF == "0000":

    # Somando automaticamente o endereço FFF0 + FFF1 colocando resultado em FFF2
    num1Hex = memoria["FFF0"]
    num2Hex = memoria["FFF1"]
    num1Dec = int(num1Hex, 16)
    num2Dec = int(num2Hex, 16)
    somaDec = num1Dec + num2Dec
    somaHex = format(somaDec, "04x").upper()
    memoria["FFF2"] = somaHex

    # Invertendo automaticamente o endereço FFF0 colocando resultado em FFF3.
    string = memoria["FFF0"]
    tabelainver = {"0":"F",
                   "1":"E",
                   "2":"D",
                   "3":"C",
                   "4":"B",
                   "5":"A",
                   "6":"9",
                   "7":"8",
                   "8":"7",
                   "9":"6",
                   "A":"5",
                   "B":"4",
                   "C":"3",
                   "D":"2",
                   "E":"1",
                   "F":"0"}

    stringInv = ""

    for elementos in string:
        elementoInv = tabelainver[elementos]    # Procurando na tabela o seu inverso.
        stringInv += elementoInv                # Contatenando os valores para formar a palavra.

    memoria["FFF3"] = stringInv                 # Salvando o resultado inverso no endereço (FFF3)


    # Recebe um valor em hexadecimal converte para inteiro incrementa 1 e e retorna o valor novamente em hexadecimal
    def contadorProgramaInc (ContadorHex):
        contadorProgramaDec = int(ContadorHex, 16)
        contadorProgramaDec += 1
        contadorProgramaProx = format(contadorProgramaDec, "04x").upper()
        return contadorProgramaProx
    

    print("-"*50)

    #-------------------------------------- PROCURANDO O DADO A SER MOVIDO ------------------------------------------#

    # Procura na memoria o valor no endereço passado pelo contadorPrograma então salva na variavel regFD.
    regFD = memoria[contadorPrograma]

    print("Contador de programa: ", contadorPrograma)

    print("Registrador de fonte e destino: ", regFD)

    # Incrementa o contadorPrograma chamando a função e passando como parametro seu proprio valor.
    contadorPrograma = contadorProgramaInc(contadorPrograma)
    
    # Procura na memoria o endereço informado por regFD e salva o dado em regTemp. 
    regTemp = memoria[regFD]

    print("registrador temporario: ", regTemp)
    

    #-------------------------------------- MOVENDO O DADO PARA O DESTINO --------------------------------------------#

    # Procurando o endereço de destino, salva então na variavel regFD. 
    regFD = memoria[contadorPrograma]

    print("Contador de programa: ", contadorPrograma)

    print("Registrador de fonte e destino: ", regFD)
    
    # Incrementa o contadorPrograma chamando a função e passando como parametro seu proprio valor.
    contadorPrograma = contadorProgramaInc(contadorPrograma)
    
    
    # Checando se o endereço de destino é o contador de programa (Executa JUMP para qualquer valor contido no regTemp)
    if regFD == "FFFC":
        contadorPrograma = regTemp

    # Checando se o endereço de destino é o pulo condicional (Pule a próxima instrução se regTemp for zero)
    elif regFD == "FFFD":
        if regTemp == "0000":
            # Incrementando duas vezes para que ele pule a fonte e o destino da proxima instrução.
            contadorPrograma = contadorProgramaInc(contadorPrograma) 
            contadorPrograma = contadorProgramaInc(contadorPrograma)
        else:
            pass

    # Checando se o endereço de destino é o registrador de saida.
    elif regFD == "FFFE":
        print("Saida : ", regTemp)

    # Checando se o endereço de destino é o registrador de parada.
    elif regFD == "FFFF":
        print("-"*50)
        print()
        FFFF = "0001"

    # Se o endereço de destino nao pertence a nenhum dos endereços acima entao salve na memoria.
    else:
        memoria[regFD] = regTemp
