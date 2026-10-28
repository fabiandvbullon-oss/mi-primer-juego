import random

print("¡Bienvenido al juego en la nube de GitHub!")
numero_secreto = random.randint(1, 10)
intentos = 3

print("He pensado en un número del 1 al 10. Tienes 3 intentos para adivinarlo.")

while intentos > 0:
    intento = input("¿Qué número crees que es? ")
    
    if intento.isdigit() and int(intento) == numero_secreto:
        print("¡MAGIA! ¡Adivinaste el número!")
        break
    else:
        intentos -= 1
        print(f"Uy, incorrecto. Te quedan {intentos} intentos.")

if intentos == 0:
    print(f"¡Oh no! Te quedaste sin intentos. El número era el {numero_secreto}.")
