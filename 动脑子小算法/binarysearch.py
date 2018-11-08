
def binarysearch(lst,value):
    start = 0
    end = len(lst) - 1
    while start <= end :
        mid = (start + end ) // 2
        if lst[mid] < value:
            start = mid + 1
        elif lst[mid] > value:
            end = mid - 1
        else:
            return mid

print(binarysearch([1,2,3,4,5,6,7,8,9],4))
