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
def search(searchInput, productList):
    searchResults = []
    searchInput = searchInput.lower()  # Ensure the search term is in lowercase
    m = len(searchInput)
    
    # Only proceed if the search input is exactly 1 character
    if m == 1:
        for i in range(len(productList)):
            product = productList[i].lower()  # Ensure product name is in lowercase
            # Check if the single character exists in the product name
            if searchInput in product:
                # If found, add the product index and a score of 1
                searchResults.append([i, 1])
    else:
        for i in range(len(productList)):
            product = productList[i].lower()  # Ensure product name is in lowercase
            n = len(product)
            
            # Initialize memoization table for LCS calculation
            memo = [[-1 for _ in range(n + 1)] for _ in range(m + 1)]
            
            # Calculate similarity score using LCS for subsequence
            similarity = lcs(searchInput, product, m, n, memo)
            
            # Set a proportional threshold (e.g., 60% of the search term length)
            min_similarity_threshold = max(2, int(0.6 * m))
            
            # Only include results that meet or exceed the proportional threshold
            if similarity >= min_similarity_threshold:
                searchResults.append([i, similarity])
    
    # Sort results by similarity score in descending order
    searchResults.sort(key=lambda x: x[1], reverse=True)
    return searchResults