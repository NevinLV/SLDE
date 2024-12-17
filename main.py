def getI(n):
    """
    Получить единичную матрицу
    :param n: размерность матрицы
    """

    I = []

    for i in range(n):
        row = []
        for j in range(n):
            row.append(0)

        row[i] = 1
        I.append(row)

    return I


def getB(m, n, A):
    """
    Получить матрицу B
    :param m: Количество уравнений в системе
    :param n: Количество переменных
    :param A: Матрица коэффициентов системы уравнений
    """

    B = []
    I = getI(n)

    for a in A:
        B.append(a)

    for i in range(0, n):
        B.append(I[i])

    for i in range(m, m + n):
        B[i].append(0)

    return B


def inputSLDE():
    """
    Ввод данных о системе
    :return: N - число уравнений, M - число неизвестных, A - матрица коэффициентов
    """

    N, M = list(map(int, input().split()))
    A = []

    for n in range(N):
        row = list(map(int, input().split()))
        row[M] = -row[M]
        A.append(row)

    return N, M, A


def gcd(a, b):
    """
    НОД двух чисел
    """
    while b:
        a, b = b, a % b
    return a


def calculateGCDofRow(row):
    """
    НОД первых n элементов строки
    """
    current_gcd = row[0]
    for num in row[1:-1]:  # Проходим по всем элементам, кроме последнего
        current_gcd = gcd(current_gcd, num)
    return current_gcd


def checkSolveExisting(matrix):
    """
    Проверка существования решения в целых числах
    """
    for row in matrix:
        current_gcd = calculateGCDofRow(row)
        last_element = row[-1]

        if current_gcd != 0 and last_element % current_gcd == 0:
            pass
        else:
            return False

    return True


def checkRow(B_i):
    """
    Проверить, один ли ненулевой элемент остался в строке
    :param B_i:
    :return:
    """
    count = 0

    for B_j in B_i:
        if B_j != 0:
            count += 1

    if count == 1:
        return True
    else:
        return False


def getCol(matrix, j):
    """
    Получить столбец
    :param matrix: Матрица
    :param j: Индекс столбца
    """
    col = []
    for row in matrix:
        col.append(row[j])

    return col


def swapCols(matrix, col_1_index, col_2_index):
    """
    Поменять местами столбцы
    :param matrix: Матрица
    :param col_1_index: Индекс первого столбца
    :param col_2_index: Индекс второго столбца
    """

    col_1 = getCol(matrix, col_1_index)
    col_2 = getCol(matrix, col_2_index)

    i = 0
    for row in matrix:
        row[col_2_index] = col_1[i]
        row[col_1_index] = col_2[i]
        i += 1

    return matrix


def getMinBiIndex(matrix, current_row):
    """
    Получить минимальный ненулевой элемент в строке
    :param matrix:
    :param current_row:
    :return:
    """
    min_value = None
    min_index = None

    for index, value in enumerate(matrix[current_row]):
        if value != 0:
            if min_value is None or abs(value) < abs(min_value):
                min_value = value
                min_index = index

    return min_index


def getBjIndex(matrix, current_row, i):
    """
    Получить элемент Bj в текущей строке
    :param matrix:
    :param current_row:
    :param i:
    :return:
    """

    for j in range(current_row, len(matrix)):
        if matrix[current_row][j] != 0 and j != i:
            return j

    return None


def subCol(matrix, index_1, index_2, c):
    for row in matrix:
        row[index_1] -= row[index_2] * c

    return matrix


def addCol(matrix, index_1, index_2):
    for row in matrix:
        row[index_1] += row[index_2]

    return matrix


def getK(matrix, n, m):
    """
    Подсчёт количества свободных переменных
    """
    K = 0
    for i in reversed(range(n)):
        zero_count = 0
        for j in range(m):
            if matrix[j][i] == 0:
                zero_count += 1

        if zero_count == m:
            K += 1
        else:
            break
    return K


def transformB(m, n, B):
    """
    Преобразование матрицы B
    :param m: Количество доступных строк
    :param n: Количество доступных столбцов
    :param B: Матрица B
    """

    current_row = 0

    while current_row < m:
        B_i = B[current_row]
        count = 0

        while not checkRow(B_i):
            # Тут просто ограничение на количество итераций - если цикл делает много итераций,
            # значит не получается привести матрицу к нужному виду, а значит нет решения
            if count == 100:
                return None

            min_B_i_index = getMinBiIndex(B, current_row)
            if min_B_i_index is None:
                break

            B_j_index = getBjIndex(B, current_row, min_B_i_index)

            if B_j_index is None:
                break
            else:
                c = B[current_row][B_j_index] // B[current_row][min_B_i_index]
                B = subCol(B, B_j_index, min_B_i_index, c)

                if B[current_row][current_row] == 0:
                    if B[min_B_i_index][current_row] != 0:
                        return None
                    else:
                        B = addCol(B, current_row, min_B_i_index)

                count += 1

        d_index = B_i.index(max(B_i, key=abs))

        if B_i[d_index] == 0:
            B = swapCols(B, d_index, 0)

        if B[current_row][m] % B_i[d_index] != 0 and B[current_row][m] != 0:
            return None

        current_row += 1

    return B


def solve(m, n, B):
    """
    Решение системы диофантовых уравнений
    """

    newB = transformB(m, n, B)

    if newB is None:
        print("NO SOLUTIONS")
    else:
        K = getK(newB, n, m)

        print(K)

        for i in range(n):

            if K > 0:
                print(B[m + i][n], end=' ')

                for j in range(K - 1):
                    print(B[m + i][n - K + j], end=' ')
                print(B[m + i][n - 1])
            else:
                print(B[m + i][n])


def main():
    m, n, A = inputSLDE()
    if checkSolveExisting(A):
        B = getB(m, n, A)
        solve(m, n, B)
    else:
        print("NO SOLUTIONS")


if __name__ == '__main__':
    main()
