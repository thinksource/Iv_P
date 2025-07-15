def countingSort(arr):
    max_value = max(arr) if arr else 0
    count = [0] * (max_value + 1)
    for i in arr:
        count[i]+=1
    return count

if __name__ == '__main__':