#Importar librerías
import json

#Abre el archivo json
jsonFile = open('Sudokus.json')

#Lee el archivo json
dataOfJson = json.load(jsonFile)
gameBoard = dataOfJson["Raw-Sudoku3"][4]

def getGameBoardSize(gameBoard):
    return len(gameBoard)

size = getGameBoardSize(gameBoard)#Se obtiene el tamaño del sudoku

#Se chequean todos los numeros que hay en dicha fila
def checkRow(gameBoard, row):
    listImpossibleNumbers = []
    for indexColumn in range(size):
        if gameBoard[row][indexColumn] != 0:
            listImpossibleNumbers.append(gameBoard[row][indexColumn])
    return listImpossibleNumbers

#Se chequean todos los números que hay en dicha columna
def checkColumn(gameBoard, column):
    listImpossibleNumbers = []
    for indexRow in range(size):
        if gameBoard[indexRow][column] != 0:
            listImpossibleNumbers.append(gameBoard[indexRow][column])
    return listImpossibleNumbers

#Se chequean todos los números que hay en la subregión
def checkSquareSubRegion(gameBoard, row, column):
    listImpossibleNumbers = []
    # Determina las coordenadas de la esquina superior izquierda de la subregión dadas las coordenadas iniciales
    subRegionSize = int (size ** 0.5)
    startRow = (row // subRegionSize) * subRegionSize
    startColumn = (column // subRegionSize) * subRegionSize
    for indexRow in range(subRegionSize):
        for indexColumn in range(subRegionSize):
            actualRow = startRow + indexRow
            actualColumn = startColumn + indexColumn
            if gameBoard[actualRow][actualColumn] != 0:
                listImpossibleNumbers.append(gameBoard[actualRow][actualColumn])
    return listImpossibleNumbers

#Recibe las tres listas generadas por cada función de checking
#y las une en una sola lista sin elementos repetidos

def listsOfCheckingUnion(list1, list2, list3):
    return list(set(list1) | set(list2) | set(list3))

#Recibe la lista de los números imposibles y de una lista de 1 a 9
#filtra los que no estan en la lista de los números imposibles

def possibleNumbers(listWithImpossibleNumbers):
    return [x for x in range(1,size + 1) if x not in listWithImpossibleNumbers]


#Funcion que recorre todo el tablero checkeando los valores posibles de las celdas vacías
#y asigna el valor si solo hay uno posible

def checkAllCells(gameBoard):
    for row in range(size):
        for column in range(size):
            if gameBoard[row][column] == 0:
                listImpossibleNumbers = listsOfCheckingUnion(checkRow(gameBoard, row), 
                                                             checkColumn(gameBoard, column), 
                                                             checkSquareSubRegion(gameBoard, row, column))
                if len(possibleNumbers(listImpossibleNumbers)) == 1:
                    gameBoard[row][column] = possibleNumbers(listImpossibleNumbers)[0]
                    checkAllCells(gameBoard)#Llamado recursivo para seguir buscando celdas vacías en el tablero actualizado
    return gameBoard

#---------------------------------------------------------------------------------------
        
#Comienza la tecnica de backtracking para sudokus dificiles y de varias soluciones
def checkAllSolutions(gameBoard):
    if findEmptyLocation(gameBoard) is False:
        # Si no hay más celdas vacías, significa que hemos encontrado una solución
        return True
    
    row, column = findEmptyLocation(gameBoard)
    listWithImpossibleNumbers = listsOfCheckingUnion(checkRow(gameBoard, row), 
                                                    checkColumn(gameBoard, column),
                                                    checkSquareSubRegion(gameBoard, row, column))
    possible_numbers = possibleNumbers(listWithImpossibleNumbers)
    
    for number in possible_numbers:
        # Intentar asignar cada número posible a la celda vacía
        gameBoard[row][column] = number
        # Llamar recursivamente a checkAllSolutions con el nuevo tablero
        if checkAllSolutions(gameBoard):
            return True  # Si se encuentra una solución, retornar True
        
    # Si ninguna de las opciones funciona, retroceder (backtrack)
    gameBoard[row][column] = 0
    return False
        

#Funcion que encuentra las celdas vacías del tablero
def findEmptyLocation(gameBoard):
    for row in range(size):
        for column in range(size):
            if gameBoard[row][column] == 0:
                return (row, column)  # Devuelve la posición de la celda vacía como una tupla
    return False  # Devuelve False si no hay celdas vacías


#Funcion que verifica si el sudoku ya está resuelto

def verifyIfSudokuIsSolved(gameBoard):
    for row in range(size):
        for column in range(size):
            if gameBoard[row][column] == 0:
                return False
    return True #Si no hay celdas vacías, el sudoku está resuelto

#Funcion que imprime de manera ordenada, el tablero resuelto
def printSolvedSudoku(gameBoard):
    for row in gameBoard:
        print(row)


def finalSolution(gameBoard):
    if verifyIfSudokuIsSolved(gameBoard) == False:
        checkAllSolutions(gameBoard)
    printSolvedSudoku(gameBoard)




finalSolution(gameBoard)


jsonFile.close()