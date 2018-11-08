
def selection_sort(lst):
    '''
    选择排序的原理：
    第一次循环，从列表的第一个数开始，依次与其他元素比较出最小的值，
    记录index值，然后与之交换。
    第二次循环，从列表的第二个数开始，一次与剩下的元素比较出最小值，
    记录index值，然后与之交换，其他次循环与此类似。
    '''
    for k in range(len(lst)):
        min_index = k #最小元素
        for j in range(k+1,len(lst)):
            if lst[min_index] > lst[j]:
                min_index = j
        lst[k],lst[min_index] = lst[min_index] ,lst[k]

num = [64,25,12,22,11]
selection_sort(num)
print(num)
