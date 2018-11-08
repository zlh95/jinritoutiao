#/usr/bin/python

def binary_search(lst,value,low,high):
    '''递归二分查找的原理：前提是有一个已经排好序列的列表。
    tips:可以使用list.index()的方法，返回元素的索引位置。
    1.首先获取查找范围，low必须小于high（两个值分别是索引值）。
    2.判断要查找的值是否大于或者小于该范围的中间值。
    3.使用递归缩小区间。

    '''
    if high < low:
        return -1
    mid = (low + high)//2
    if lst[mid] > value:
        return binary_search(lst,value,low,mid-1)
    if lst[mid] < value:
        return binary_search(lst,value,mid+1,high)
    else:
        return mid

print(binary_search([1,2,3,5,7,9,12,15,16],15,0,8))
