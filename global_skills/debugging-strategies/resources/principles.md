# Principios y Mentalidad de Depuración

## 1. El Método Científico
1. **Observar**: Identifica exactamente qué está pasando frente a qué debería pasar.
2. **Formular Hipótesis**: Elabora teorías sobre qué parte del sistema está fallando.
3. **Experimentar**: Realiza cambios o pruebas pequeñas para aislar la causa.
4. **Analizar**: ¿El experimento confirmó o refutó la teoría?
5. **Repetir**: Itera hasta llegar a la causa raíz.

## 2. Reglas de Oro
- **No supongas**: "No puede ser X" es la frase más peligrosa. Todo es sospechoso.
- **Reproduce consistentemente**: Si no puedes reproducirlo a voluntad, no puedes estar seguro de haberlo arreglado.
- **Aislar el problema**: Elimina el ruido y el código no relacionado hasta que solo quede el problema.
- **Toma notas**: Documenta qué has probado para no dar vueltas en círculos.

## 3. Rubber Ducking (El Patito de Goma)
Explica el problema y la lógica del código en voz alta. El proceso de forzar a tu cerebro a estructurar la explicación para "alguien más" suele revelar el error lógico de forma casi mágica.
