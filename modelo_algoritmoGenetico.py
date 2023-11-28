import timeit
import random

#generarmos soluciones iniciales

def generar_poblacion_inicial(n_individuos, longitud_individuo,n_tareas_validas):
    poblacion = []
    for i in range(n_individuos):
        n_tareas_realizadas = []
        individuo = ''.join(random.choice('01') for _ in range(longitud_individuo)) #Nos genera el individuo
        valido = True #Variable para saber si una tarea es valida
        for i in range(0,longitud_individuo,3):
            n_tarea_binaria = individuo[i:i+3] #Obtenemos la tarea
            if n_tarea_binaria not in n_tareas_validas or n_tarea_binaria in n_tareas_realizadas:
                valido = False
            else:
                n_tareas_realizadas.append(n_tarea_binaria)
        if valido:
            poblacion.append(individuo)
    
    return poblacion

#fitness_individuo =  sum(int(bit)*peso for bit, peso in zip(individuo, beneficios))


#ordenar poblacion en base a poblacion fitness
def ordenar_poblacion(poblacion):
    return {k: v for k, v in sorted(poblacion.items(), key=lambda item: item[1],reverse=True)}

def evaluar_factibilidad(individuo,longitud_individuo,n_tareas_validas):
    valido = True #Variable para saber si una tarea es valida
    n_tareas_realizadas = []
    for i in range(0,longitud_individuo,3):
        n_tarea_binaria = individuo[i:i+3] #Obtenemos la tarea
        if n_tarea_binaria not in n_tareas_validas or n_tarea_binaria in n_tareas_realizadas:
            valido = False
        else:
            n_tareas_realizadas.append(n_tarea_binaria)
    
    return valido


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
        
        poblacion[individuo] = f_o
    

    return ordenar_poblacion(poblacion)



def algoritmoGenetico_Tareas(poblacion,generaciones,longitud_individuo,n_tareas_validas,ti,di,hi,ci,factibilidad=True):

    p_cruce = 0.9 #probabilidad de cruce
    p_mutacion = 0.1 #probabilidad de mutacion

    #Iteramos sobre las generaciones
    for n in range(generaciones):
        #Generamos una probabilidad aleatoria de cruce
        cruce = random.random()
        if cruce < p_cruce:
            individuos = list(poblacion.keys())
            numero_padre1,numero_padre2 = random.sample(range(0, len(individuos)), 2) #numero de padre
            padre1 = individuos[numero_padre1]
            padre2 = individuos[numero_padre2]

            hijo1 = padre1[0:5] + padre2[5:10] + padre1[10:15] 
            hijo2 = padre2[0:5] + padre1[5:10] + padre2[10:15]

            #mutacion de cada hijo
            for i in range(0,len(hijo1)):
                mutacion = random.random()
                if mutacion < p_mutacion:
                    if hijo1[i] == '1':
                        hijo1[i] ==  '0'
                    else:
                        hijo1[i] == '1'

            for j in range(0,len(hijo2)):
                mutacion = random.random()
                if mutacion < p_mutacion:
                    if hijo2[j] == '1':
                        hijo2[j] ==  '0'
                    else:
                        hijo2[j] == '1'

            #Si queremos factibilidad checamos si el individuo cumple con ella
            nuevosIntegrantes = [hijo1,hijo2]
            integrantes_filtrados = []
            if factibilidad:
                for hijo in nuevosIntegrantes:
                    factible = evaluar_factibilidad(hijo,longitud_individuo,n_tareas_validas)
                    if factible == True and (hijo not in individuos):
                        integrantes_filtrados.append(hijo)
                    else:
                        continue


            #Si cualquiera de los hijos es factible, evaluamos su funcion fitness y decidimos si lo incluimos en la poblacion
            if integrantes_filtrados:
                subPoblacion = evaluarFuncionFitness(integrantes_filtrados,longitud_individuo,ti,di,hi,ci)
                poblacion_original_debiles = dict(list(poblacion.items())[:2])

                # Unimos los dos diccionarios
                poblacionMerge = {**subPoblacion, **poblacion_original_debiles}

                # Ordenamos el diccionario total por valor de forma ascendente
                poblacionMerge = dict(sorted(poblacionMerge.items(), key=lambda item: item[1]))
                # Creamos un nuevo diccionario con los dos primeros elementos del diccionario ordenado
                nuevaSubPoblacion = dict(list(poblacionMerge.items())[:2])

                nuevaSubPoblacion_ordenada = ordenar_poblacion(nuevaSubPoblacion)

                #Actualizamos los primeros dos elementos del diccionario original con los del subdiccionario
                #print(poblacionMerge)
                #print(nuevaSubPoblacion_ordenada)
                #print()                
                
                #Eliminamos los antiguos individuos y agregamos los nuevos
                oldIndividuals = individuos[:2]
                del poblacion[oldIndividuals[0]]
                del poblacion[oldIndividuals[1]]

                for newIndividual,fitness in nuevaSubPoblacion_ordenada.items():
                    poblacion[newIndividual] = fitness




            poblacion = ordenar_poblacion(poblacion)       
        

    return poblacion



#pasamos las cadenas binarias a
def mostrar_secuenciaDeTareas(poblacion_final,longitud_individuo):

    poblacion_final_secuencia = {}

    for individuo,fitness in poblacion_final.items():
        secuenciaTarea = []
        for i in range(0,longitud_individuo,3):
            n_tarea =  int(individuo[i:i+3],2) #Pasamos de cadena binaria a entero
            secuenciaTarea.append(str(n_tarea))

        secuenciaTarea_individuo = ' -> '.join(secuenciaTarea)
        poblacion_final_secuencia[secuenciaTarea_individuo] = fitness 

    return poblacion_final_secuencia   

                
#Parametros

ti = [10,8,6,7,4] #tiempo de procesamiento
di = [15,20,10,30,12] #fecha limite para ser realizada la tarea
hi =  [3,2,5,4,6]  #Costo de retencion por unidad de tiempo
ci = [10,22,10,8,15] #Costo de penalizacion por unidad de tiempo

n_tareas_validas = set(["000","001","010","011","100"]) #Tenemos 5 tareas solamente (Tarea 0 ~ 4)

start_time = timeit.default_timer()
generaracion_individuos= generar_poblacion_inicial(3000,15,n_tareas_validas)

poblacion_inicial = evaluarFuncionFitness(generaracion_individuos,15,ti,di,hi,ci)


poblacionFinal = algoritmoGenetico_Tareas(poblacion_inicial,10000,15,n_tareas_validas,ti,di,hi,ci,factibilidad=True)
poblacionFinal_secuencia = mostrar_secuenciaDeTareas(poblacionFinal,15)
end_time = timeit.default_timer()
execution_time =  end_time - start_time

print(poblacionFinal_secuencia)
print()
print(f'\n Tiempo de ejecucion del algoritmo: {execution_time}')


