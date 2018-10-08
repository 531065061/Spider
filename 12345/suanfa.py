def suanfa1():
    n = int(input('输入参数'))
    sum = 0
    i = 1
    while i <= n:
        i += 1
        j = 1
        while j <= n:
            j += 1
            sum = sum + i * j
            print(sum)


# suanfa1()


def suanfa2():
    num = input('输入数组')
    x = int(input('输入数组中某个参数'))
    array = [int(array) for array in num.split()]
    n = len(array)
    pos = -1
    print(array)
    a = list(range(n))
    print(a)
    for i in a:
        while array[i] == x:
            pos = i
            print(pos)
    return print(pos)


# suanfa2()

def guess_number(list, item):
    low = 0
    high = len(list) - 1
    while low < high:
        mid = (low + high) // 2
        gusee = list[mid]
        print(gusee)
        if gusee == item:
            return mid
        if gusee > item:
            high = mid - 1
        else:
            low = mid + 1
    return None


def findSmallest(arr):
    smallest = arr[0]
    smallest_index = 0
    for i in range(1, len(arr)):
        if arr[i] < smallest:
            smallest = arr[i]
            smallest_index = i
            print(i)
    return smallest_index


def selectionSort(arr):
    newArr = []
    for i in range(len(arr)):
        smallest = findSmallest(arr)
        newArr.append(arr.pop(smallest))
        # print(newArr)
    return newArr


def sum(list):
    if list == []:
        return 0
    else:
        return list[0] + sum(list[1:])


def commit(list):
    if list == []:
        return 0
    else:
        return 1 + commit(list[1:])


def max(list):
    if len(list) == 2:
        return list[0] if list[0] > list[1] else list[1]
    sub_max = max(list[1:])
    return list[0] if list[0] > sub_max else sub_max


def quicksort(array):
    if len(array) < 2:
        return array
    else:
        pivot = array[0]
        less = [i for i in array[1:] if i <= pivot]
        greater = [i for i in array[1:] if i > pivot]
        return quicksort(less) + [pivot] + quicksort(greater)

from collections import deque
graph={}
graph["you"]=["alice","bob","claire"]
graph["bob"]=["anuj","peggy"]
graph["alice"]=["peggy"]
graph["claire"]=["thom","jonny"]
graph["anuj"]=[]
graph["peggy"]=[]
graph["thom"]=[]
graph["jonny"]=[]
def search(name):
    search_queue=deque()
    search_queue+=graph[name]
    searched=[]
    while search_queue:
        person=search_queue.popleft()
        if person not in searched:
            if person_is_seller(person):
                print(person+" is a mango seller!")
                return True
            else:
                search_queue+=graph[person]
                searched.append(person)
    return False
def person_is_seller(name):
    return name[-1]=='m'



def find_lowest_cost_node(costs):
    lowest_cost=float("inf")
    lowest_cost_node=None
    for node in costs:
        cost=costs[node]
        if cost<lowest_cost and node not in processed:
            lowest_cost=cost
            lowest_cost_node=node
    return lowest_cost_node
graph["start"]={}
graph["start"]["a"]=6
graph["start"]["b"]=2
graph["a"]={}
graph["a"]["fin"]=1
graph["b"]={}
graph["b"]["a"]=3
graph["b"]["fin"]=5
graph["fin"]={}
infinity=float("inf")
costs={}
costs["a"]=6
costs["b"]=2
costs["fin"]=infinity
parents={}
parents["a"]="start"
parents["b"]="start"
parents["fin"]=None
processed=[]
node=find_lowest_cost_node(costs)
while node is not None:
    cost=costs[node]
    neighbors=graph[node]
    for n in neighbors.keys():
        new_cost=cost+neighbors[n]
        if costs[n]>new_cost:
            costs[n]=new_cost
            parents[n]=node
    processed.append(node)
    node=find_lowest_cost_node(costs)










# if __name__ == '__main__':
    # suanfa1()

    # my_list = list(range(100))
    # print(my_list)
    # print(guess_number(my_list, 10))

    # print(selectionSort([5,3,6,2,10]))

    # print(sum([2,3,4]))

    # print(commit([1,2,3]))

    # search("you")

    # print(max([5,3,2]))

    # print(quicksort([10,5,1,3]))
