# Turing Simulator
Simulatore di una macchina di turing a scopo didattico, scritta in python.


## Utilizzo

Il simulatore è utilizzabile con una versione di python >3.7.

<hr>

I programmi per questo simulatore devono essere scritti in un file con estensione `.tur`.
All'inizio di ogni programma dev'essere indicato lo stato di partenza (es. `0`) dopo il termine `#init`.

_Esempio:_
```
#init 0
```

<hr>

Ogni frase del programma ha una sintassi;
```
(stato, simbolo) > (nuovo_stato, nuovo_simbolo, movimento)
```
indicando in ogni posizione l'informazione relativa:
- **stato**     |   _Lo stato a cui appartiene la frase_
- **simbolo**   |   _Il simbolo (lettera) che la frase deve riconoscere_
- **nuovo_stato**   |   _Lo stato che il programma deve raggiungere se il simbolo viene riconosciuto sul nastro_
- **nuovo_simbolo** |   _Il simbolo utilizzato per la sostituzione nella casella_
- **movimento**     |   _Il movimento che la testina eseguirà a fine della frase (destra >, sinistra <, fermo -)_

<br>
<hr>

### Esempio di programma:
```
#init 0

(0,clc) > (1,C,<)
(1,clc) > (2,I,<)
(2,clc) > (3,A,<)
(3,clc) > (4,O,<)
```

_La scrittura `clc` indica il riconoscimento di una cella vuota (CLear Cell) sul nastro._

<hr>

Opzionalmente si può indicare uno stato finale, al cui raggiungimento la macchina si ferma.
```
#end 4
```

<br>

## Esecuzione di un programma

Per eseguire un programma, basta richiamare il file `turing.py` e fornire come argomento di linea di comando il nome del file del programma (es. `./examples/ciao.tur`).

Il file del programma deve trovarsi nella stessa cartella del file `turing.py` se non viene specificata la posizione del primo.

```
python turing.py ./esempi/ciao.tur
```

_Output:_

```
Stato finale del nastro:
| C | I | A | O |
```

<br>

## Inizializzazione con contenuto sul nastro

Se non indicato diversamente, la macchina comincia il suo funzionamento con il nastro vuoto.

Per indicare i contenuti da inserire nel nastro prima dell'esecuzione, è necessario specificarli singolarmente, spaziati tra uno e l'altro, con l'opzione da linea di comando `--tape` o, abbreviato `-t`.

```
python turing.py ./examples/divisori_5.tur --tape 1 2 3 4
```
_Questo comando inizializzerà la macchina con, all'interno del nastro:_
```python
[ '1', '2', '3', '4']
```

_Output:_
```
Stato finale del nastro:
| 1 | 2 | 3 | 4 | N |
```

<br>
<hr>

Nella cartella `examples` sono presenti alcuni programmi di esempio per far funzionare la macchina.