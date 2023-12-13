from functools import cmp_to_key
from spin_http import Response
from json import dumps, loads
from operator import itemgetter


def handle_request(request):

    if request.method != "POST":
        return Response(405)
    
    if request.body == None:
        return Response(405)

    r = loads(request.body)
    kids = r.get("kids")
    if kids == None:
        return Response(400)
    weight = r.get("weight")
    if weight == None:
        return Response(400)
    capacity = r.get("capacity")
    if capacity == None:
        return Response(400)    

    result = calculate(kids, weight, capacity)

    return Response(200, 
                    {"content-type": "application/json"},
                    bytes(dumps({"kids": result}), "utf-8"))

def compare(a,b) :
    if a[0] == b[0]:
        return a[1] - b[1]
    else:
        return a[0] - b[0]

def calculate(kids, weight, capacity):
    pairs = [i for i in zip(kids, weight)]
    pairs.sort(key = cmp_to_key(compare), reverse = True)
    
    i = 0
    total = 0
    total_kids = 0
    while i < len(pairs) and total + pairs[i][1] < capacity:
        total += pairs[i][1]
        total_kids += pairs[i][0]
        i += 1
    return total_kids
