def generarUsername(nombres, apellidos):
    primeraLetra = nombres[0]
    apellido = apellidos.split()[0]
    return primeraLetra + apellido
    