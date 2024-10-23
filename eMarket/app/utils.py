# Sort Function using QuickSort
def partition(a,low,high):
    pivot = a[high]
    i = low - 1
    for j in range(low,high):
        if a[j] <= pivot:
            i += 1
            (a[i],a[j]) = (a[j],a[i])
    (a[i+1],a[high]) = (a[high],a[i+1])
    return i+1

# Search Function using largest common substring with 2D memoization
def lcs(s1,s2,m,n,memo):
    if m == 0 or n == 0:
        return 0
    if memo[m][n] != -1:
        return memo[m][n]
    if s1[m-1] == s2[n-1]:
        memo[m][n] = 1 + lcs(s1,s2,m-1,n-1,memo)
        return memo[m][n]
    else:
        memo[m][n] =  max(lcs(s1,s2,m,n-1,memo),lcs(s1,s2,m-1,n,memo))
        return memo[m][n]

# Modifies a and sorts
def sort(a,low=0,high=-1):
    if high < 0:
        high = len(a)-1
    if low < high:
        partition_index = partition(a,low,high)
        sort(a,low,partition_index-1)
        sort(a,partition_index+1,high)

# Returns a new array weighted by the similarity of the product to the input
# Array form = [[productIndex,similarity],[productIndex2,similarity2]...]
def search(searchInput,productList):
    searchResults = []
    maxNameLength = 50 # Replace with max_value of Product name in the future
    for i in range(len(productList)):
        product = productList[i].lower()
        m = len(searchInput)
        n = len(product)
        memo = [[-1]*maxNameLength]*maxNameLength
        similarity = lcs(searchInput,product,m,n,memo)
        if similarity > m: similarity = m # Weird bug I couldn't figure out, caused values > m which would freak out the sorting
        if min(3,n) <= similarity:
            searchResults.append([i,similarity])
            for j in range(len(searchResults)-1,0,-1):
                if searchResults[j-1][1] < searchResults[j][1]: (searchResults[j-1],searchResults[j]) = (searchResults[j],searchResults[j-1])
    return searchResults