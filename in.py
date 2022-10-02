import matplotlib.pyplot as plt
import numpy as np

def check(B, y, x):
    #если мы в пределах картинки и в соседе объект, то возвращаем True
    if not 0 <= x < B.shape[1]: 
        return False
    if not 0 <= y < B.shape[0]:
        return False
    if B[y, x] != 0:
        return True
    return False

def neighbors2(B, y, x):
    left = y, x-1 #сосед слева
    top = y - 1, x #сосед сверху
    
    #присваиваем None если не прошли проверку на наличие объекта
    if not check(B, *left):  
        left = None
    if not check(B, *top):
        top = None
    return left, top #возвращаем соседа

def exists(neighbors):
    return not all([n is None for n in neighbors])

def find(label, linked):
    j = label
    # print(linked, linked[j], j)
    while linked[j] != 0:
        j = linked[j]
    
    # print(j)
    return j

def union(label1, label2, linked):
    j = find(label1, linked)
    k = find(label2, linked)
    if j != k:
        # print(linked[k], j)
        linked[k] = j


def two_pass_labeling(B):
    B = (B.copy() * - 1).astype("int") #изображение, где объекты помечены как -1
    linked = np.zeros(len(B), dtype="uint") #связи объектов
    #print(linked, len(B))
    labels = np.zeros_like(B) #выходной результат
    label = 1 #метка
    
    #первый проход
    for row in range(B.shape[0]): 
        for col in range(B.shape[1]):
            if B[row, col] != 0: #если находим объект
                n = neighbors2(B, row, col) #получаем соседей сверху и слева
                if not exists(n): #если соседей нет, значит, мы нашли начало нового объекта
                    m = label #присваиваем label временной переменной
                    label += 1 #увеличиваем метку на единицу
                else:
                    lbs = [labels[i] for i in n if i is not None] #получаем существующих соседей
                    #print(lbs)
                    m = min(lbs) #получаем минимальную метку
                labels[row, col] = m #присваиваем точке минимальную метку
                for i in n: #идем по соседям
                    if i is not None: #если сосед существует
                        lb = labels[i] #берем соседа
                        if lb != m: #если его метка не является минимальной, то ищем родительскую метку и соединяем
                            union(m, lb, linked)
                            # print(m, lb, linked)   
    #print(linked)
    new_linked = np.zeros(label, dtype='int')
    new_label = 1
    
    # for row in range(B.shape[0]):
    #     for col in range(B.shape[1]):
    #         if B[row, col] != 0:
    #             new_label = find(labels[row, col], linked)
    #             if new_label != labels[row, col]:
    #                 labels[row, col] = new_label    
    
    for lb in range(1, label):
        if (linked[lb] == 0):
            new_linked[lb] = new_label
            new_label += 1
        else: 
            new_linked[lb] = new_linked[linked[lb]]    
            
    #print(new_linked)
    
    for y in range(B.shape[0]):
        for x in range(B.shape[1]):
            if (B[y, x] != 0):
                labels[y, x] = new_linked[labels[y][x]]
                
        


    return labels

if __name__ == "__main__":
    image = np.zeros((20, 20), dtype='int32')
    
    image[1:-1, -2] = 1
    
    image[1, 1:5] = 1
    image[1, 7:12] = 1
    image[2, 1:3] = 1
    image[2, 6:8] = 1
    image[3:4, 1:7] = 1
    
    image[7:11, 11] = 1
    image[7:11, 14] = 1
    image[10:15, 10:15] = 1
    
    image[5:10, 5] = 1
    image[5:10, 6] = 1

    labeled_image = two_pass_labeling(image)
    
    plt.figure(figsize=(12, 5))
    plt.subplot(121)
    plt.imshow(image)
    plt.subplot(122)
    plt.imshow(labeled_image.astype("uint8"))
    plt.show()