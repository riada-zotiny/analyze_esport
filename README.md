# Stage sur Esport
Le code qui était écrite durant le stage de fin d'année de Master Informatique. Dans ce git, nous avons tout le code qui était ecrite durant le stage concernatn l'analyse des données d'Esport

## Code mouvement Souris 
Le code qui détecte le mouvement de sourise et du clavier étant inspiré de cet auteur https://github.com/biohacker0/maCrow/tree/main. Ce code permet d'enregistrer ces mouvements en format JSON. Cela va être utile plus tard pour l'analyse des données obtenues.

### Usage
Pour le moment le code se lance en ligne des commandes en terminal avec la commande suivant pour play :
bash
```
python recordMouseKeyboardMovement.py record --file mouse_actions.json
```

### Interface graphique 

En supplément, j'ai pu developpé une interface graphique à l'aide de bibliotheque tkinter

![image](https://github.com/user-attachments/assets/bdc37cc6-888f-42df-ad88-900490856bc1)

## Interaction avec les lunettes Tobii Pro Glasses 3

Pour pouvoir connecter avec les lunettes, nous aurons utiliser la librairie https://tobiipro.github.io/g3pylib/g3pylib.html
