import math
import time

N = 8
INF = 99999

NOMBRES = ["Almacen","C1","C2","C3","C4","C5","C6","C7"]

X = [0,2,5,3,7,9,6,1]
Y = [0,4,2,7,5,2,9,9]

H_INI = [0,8,9,8,10,11,9,8]
H_FIN = [24,14,15,14,16,17,15,14]

VEH = ["Moto","Auto","Camioneta"]
CAP = [20,60,150]
VEL = [40,60,80]

ARISTAS = [
    (0,1),(0,2),(1,3),(1,7),
    (2,4),(2,5),(3,6),
    (3,7),(4,5),(4,6),(5,6)
]

mejor_ruta = []
mejor_dist = INF

def distancia(a,b):
    return math.sqrt((X[a]-X[b])**2 + (Y[a]-Y[b])**2)

def floyd():
    d = [[INF]*N for _ in range(N)]
    for i in range(N):
        d[i][i] = 0
    for a,b in ARISTAS:
        d[a][b] = distancia(a,b)
        d[b][a] = d[a][b]
    for k in range(N):
        for i in range(N):
            for j in range(N):
                d[i][j] = min(d[i][j],d[i][k]+d[k][j])
    return d

def distancia_ruta(ruta,d):
    total = d[0][ruta[0]]
    for i in range(len(ruta)-1):
        total += d[ruta[i]][ruta[i+1]]
    return total + d[ruta[-1]][0]

def backtrack(nodo,ruta,visitados,d,pesos,cap,vel,tiempo,peso,dist):
    global mejor_ruta, mejor_dist

    if len(ruta) == N-1:
        total = dist+d[nodo][0]
        if total < mejor_dist:
            mejor_dist = total
            mejor_ruta = ruta[:]
        return

    for c in range(1,N):
        if not visitados[c]:
            llegada = tiempo+d[nodo][c]/vel
            nuevo_peso = peso+pesos[c]
            nueva_dist = dist+d[nodo][c]

            if (nuevo_peso <= cap 
                and llegada <= H_FIN[c]
                and nueva_dist < mejor_dist):

                visitados[c] = True
                ruta.append(c)

                backtrack(
                    c,ruta,visitados,d,
                    pesos,cap,vel,
                    max(llegada,H_INI[c]),
                    nuevo_peso,
                    nueva_dist
                )

                ruta.pop()
                visitados[c] = False

def mostrar(ruta):
    if not ruta:
        print("No se encontro una ruta factible con las restricciones.")
        return
        
    print(
        " -> ".join(
            ["Almacen"]+
            [NOMBRES[i] for i in ruta]+
            ["Almacen"]
        )
    )

def main():
    global mejor_ruta, mejor_dist
    pesos = [0]*N

    print("\nSISTEMA DE RUTAS - METODO BACKTRACKING")
    print("-"*40)

    for i in range(1, N):
        while True:
            entrada = input(f"Peso pedido {NOMBRES[i]}: ")
            if entrada == "":
                print("Cantidad inválida")
                continue
            try:
                peso = float(entrada)
                if peso <= 0:
                    print("Cantidad inválida")
                    continue
                pesos[i] = peso
                break
            except ValueError:
                print("Cantidad inválida")

    total = sum(pesos)
    print(f"\nPeso total: {total}")

    print("\nVehiculos disponibles:")
    for i in range(3):
        print(f"{i+1} {VEH[i]} {CAP[i]} kg")

    while True:
        try:
            op = int(input("Seleccione vehículo (1-3): "))
            if op < 1 or op > 3:
                print("Opción inválida")
                continue
            if total <= CAP[op - 1]:
                break
            print("Capacidad insuficiente")
        except ValueError:
            print("Opción inválida")

    cap = CAP[op-1]
    vel = VEL[op-1]

    d = floyd()

    print("\n--- CALCULANDO RUTA OPTIMA (BACKTRACKING) ---")
    
    mejor_ruta = []
    mejor_dist = INF
    visitados = [False]*N
    visitados[0] = True

    inicio = time.time()
    
    backtrack(
        0,[],visitados,d,
        pesos,cap,vel,
        8,0,0
    )

    tb = (time.time()-inicio)*1000
    rb = mejor_ruta
    db = distancia_ruta(rb,d) if rb else INF

    print(f"\nClientes visitados: {len(rb)}/{N-1}")
    if db != INF:
        print(f"Distancia optima: {db:.2f} km")
    print(f"Tiempo de ejecucion: {tb:.5f} ms")
    print("\nMejor ruta encontrada:")
    mostrar(rb)

if __name__ == "__main__":
    main()
