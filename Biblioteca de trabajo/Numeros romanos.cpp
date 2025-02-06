#include <stdio.h>

void convertirARomanos(int numero) {
    int valores[] = {1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1};
    char *simbolos[] = {"M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"};

    printf("El número en romano es: ");
    for (int i = 0; i < 13; i++) {
        while (numero >= valores[i]) {
            printf("%s", simbolos[i]);
            numero -= valores[i];
        }
    }
    printf("\n");
}

int main() {
    int numero;

    printf("Ingrese un número entero (1-3999): ");
    scanf("%d", &numero);

    if (numero < 1 || numero > 3999) {
        printf("Error: El número debe estar en el rango de 1 a 3999.\n");
    } else {
        convertirARomanos(numero);
    }

    return 0;
}

