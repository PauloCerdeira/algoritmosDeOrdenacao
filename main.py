import PySimpleGUI as sg
import random
from datetime import datetime

sg.theme('GrayGrayGray')

col = [
    [sg.Text('Algoritmos disponiveis: ')],

    [sg.Radio('Insert Sort', "algoritmos", default=True, key="Insert"),
    sg.Radio('Merge Sort', "algoritmos", default=False, key="Merge"),
    sg.Radio('Quick Sort', "algoritmos", default=False, key="Quick")],

    [sg.Text('DataSets disponiveis:')],

    [sg.Radio('Melhor caso (array já ordenado)', "DataSets", default=False, key="best")],
    [sg.Radio('Caso Médio (array em ordem aleatória)', "DataSets", default=True, key="medium")],
    [sg.Radio('Pior Caso (array em ordem decrescente)', "DataSets", default=False, key="worst")],

    [ sg.Text('Quantidade de elementos:'), sg.Input("50", size=(10,1), key='DataSetSize'), ],

    [sg.Checkbox("Mostrar array em ordem", default=False, key="showOrganizedArray")],
    [sg.Checkbox("Mostrar array reorganizado", default=False, key="showShuffledArray")],
    [sg.Checkbox("Mostrar array pós algoritmo", default=False, key="showReorganizedArray")],
    [sg.Checkbox("Mensagens minimas", default=False, key="minimalMsgs")],


    [sg.Button('Ordenar'), sg.Button('Fechar')]
]

layout = [
    [sg.Column(col), 
    sg.Multiline(default_text="------------------ Software iniciado ------------------\n", size=(40,22), disabled=True, autoscroll=True , key="output")
    ],
]

window = sg.Window('Algoritmos De Ordenação', layout)



def printM(text):
    window['output'].update(text + "\n", append=True)

def printArray(array):
    string = "["
    for e in array:
        string += str(e) + ", "
    printM(string[0:len(string) - 2] + "]")

def InsertionSort(array):
    for i in range(1, len(array)):
        aux = array[i]

        j = i-1
        while j >=0 and aux < array[j] :
                array[j+1] = array[j]
                j -= 1
        array[j+1] = aux

def merge(arr, l, m, r):
    n1 = m - l + 1
    n2 = r - m
 
    L = [0] * (n1)
    R = [0] * (n2)
 
    for i in range(0, n1):
        L[i] = arr[l + i]
 
    for j in range(0, n2):
        R[j] = arr[m + 1 + j]
 
   
    i = 0    
    j = 0     
    k = l 
 
    while i < n1 and j < n2:
        if L[i] <= R[j]:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1
 
    while i < n1:
        arr[k] = L[i]
        i += 1
        k += 1
 
    while j < n2:
        arr[k] = R[j]
        j += 1
        k += 1

def mergeSort(arr, l, r):
    if l < r:
 
        m = l+(r-l)//2
 
        mergeSort(arr, l, m)
        mergeSort(arr, m+1, r)
        merge(arr, l, m, r)

def partition(array, low, high):
 
    pivot = array[high]
 
    i = low - 1
 
    for j in range(low, high):
        if array[j] <= pivot:
 
            i = i + 1
 
            (array[i], array[j]) = (array[j], array[i])
 
    (array[i + 1], array[high]) = (array[high], array[i + 1])

    return i + 1

def quickSort(array, low, high):
    if low < high:
 
        pi = partition(array, low, high)
 
        quickSort(array, low, pi - 1)
 
        quickSort(array, pi + 1, high)

while True:  # Event Loop
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Fechar':
        break
    if event == 'Ordenar': 
        printM("")
        # validar tamanho do array
        try:
            int(values["DataSetSize"])
        except:
            printM("Quantidade de elementos \"" + values["DataSetSize"] + "\" inválida,\nusando quantidade padrão: 50")
            values["DataSetSize"] = "50"
            window['DataSetSize'].update("50")
        
        # gerar array
        if not values["minimalMsgs"]:
            printM("Gerando array de " + values["DataSetSize"] + " elementos...")
        array = []
        count = 0
        for x in range(int(values["DataSetSize"])):
            count += 1
            array.append(count)
        if values["showOrganizedArray"]:
            printArray(array)

        #randomizar ou inverter array
        _case = "Melhor caso"
        if values["medium"]:
            _case = "Caso medio"
            if not values["minimalMsgs"]:
                printM("Reordenando array...")
            random.shuffle(array)
        elif values["worst"]:
            _case = "Pior Caso"
            if not values["minimalMsgs"]:
                printM("Invertendo array...")
            array = array[::-1]
        if values["showShuffledArray"]:
            printArray(array)
            

        alg = ""
        tstart = datetime.now()
        if values["Insert"]:
            if not values["minimalMsgs"]:
                printM("Insertion sort  iniciado...")
            InsertionSort(array)
            alg = "Insertion sort"
        elif values["Merge"]:
            if not values["minimalMsgs"]:
                printM("Merge sort iniciado...")
            mergeSort(array, 0, len(array)-1)
            alg = "Merge sort"
        elif values["Quick"]:
            if not values["minimalMsgs"]:
                printM("Quick sort iniciado...")
            quickSort(array, 0, len(array) - 1)
            alg = "Quick sort"
        tend = datetime.now()

        if values["showReorganizedArray"]:
            printArray(array)

        if not values["minimalMsgs"]:
            printM(alg + " finalizado em " +    str(tend - tstart)[0:12])
        else:
            printM("QTD elementos: " + values["DataSetSize"] + " - " + _case)
            printM(alg + " - " +    str(tend - tstart)[0:12])

window.close()