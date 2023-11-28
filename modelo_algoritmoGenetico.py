import timeit
import random

#generarmos soluciones iniciales

def generar_poblacion_inicial(n_individuos, longitud_individuo,n_tareas_validas):
    poblacion = []
    for i in range(n_individuos):
        individuo = ''.join(random.choice('01') for _ in range(longitud_individuo)) #Nos genera el individuo
        valido = True #Variable para saber si una tarea es valida
        for i in range(0,longitud_individuo,3):
            n_tarea = individuo[i:i+3] #Obtenemos la tarea
            if n_tarea not in n_tareas_validas:
                valido = False
        if valido:
            poblacion.append(individuo)
    
    return poblacion

#fitness_individuo =  sum(int(bit)*peso for bit, peso in zip(individuo, beneficios))


#ordenar poblacion en base a poblacion fitness
def ordenar_poblacion(poblacion):
    return {k: v for k, v in sorted(poblacion.items(), key=lambda item: item[1])}

#evaluar funcionFitness
def evaluarFuncionFitness(generacion_poblacion,longitud_individuos,ti,di,hi,ci):
    poblacion = {}
    for individuo in generacion_poblacion:
        xi = 0 #tiempo total de realizacion de tareas
        f_o = 0 #funcion objetivo
        for i in range(0,longitud_individuos,3):
            n_tarea = int(individuo[i:i+3],2)
            ai = max(0,di[n_tarea] - xi - ti[n_tarea]) #tiempo de retencion
            bi = max(0,xi + ti[n_tarea] - di[n_tarea]) #tiempo de penalizacion
            f_o += ai * hi[n_tarea]  + bi * ci[n_tarea]
            xi += ti[n_tarea]
        
        poblacion[individuo] = 1 / f_o
    

    return ordenar_poblacion(poblacion)



def algoritmoGenetico_Tareas(poblacion,generaciones,longitud_individuos,ti,di,hi,ci):

    return 0





#Parametros

ti = [10,8,6,7,4] #tiempo de procesamiento
di = [15,20,10,30,12] #fecha limite para ser realizada la tarea
hi =  [3,2,5,4,6]  #Costo de retencion por unidad de tiempo
ci = [10,22,10,8,15] #Costo de penalizacion por unidad de tiempo

n_tareas_validas = set(["000","001","010","011","100"]) #Tenemos 5 tareas solamente (Tarea 0 ~ 4)

generaracion_poblacion_inicial = generar_poblacion_inicial(1024,15,n_tareas_validas)


print(generaracion_poblacion_inicial)
print()


individuo = '001001010000100'
n_primera_tarea = int(individuo[0:3],2) 
print(n_primera_tarea)

print()

poblacion = {}
xi = 0 #tiempo total de realizacion de tareas
f_o = 0 #funcion objetivo
for i in range(0,15,3):
    n_tarea = int(individuo[i:i+3],2)
    ai = max(0,di[n_tarea] - xi - ti[n_tarea]) #tiempo de retencion
    bi = max(0,xi + ti[n_tarea] - di[n_tarea]) #tiempo de penalizacion
    f_o += ai * hi[n_tarea]  + bi * ci[n_tarea]
    xi += ti[n_tarea]

poblacion[individuo] = 1 / f_o

print(poblacion)

print()

poblacion_inicial =  evaluarFuncionFitness(generaracion_poblacion_inicial,15,ti,di,hi,ci)
print(poblacion_inicial)


