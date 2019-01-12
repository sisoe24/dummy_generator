# Installazione ed utilizzo
I primi step sono per lanciare lo script tramite la GUI. nel caso dovessero fallire, allora continua con gli altri step per farlo partire dal terminale.

------
## GUI

1. Apri il terminale e scrivi:

        python -m tkinter

    Dovrebbe farti vedere una finestra di un app con qualche testo random \.
    Se invece ti dice un errore del tipo: `blabla python3.7: No module named tkinter`,
    allora sempre sul terminale scrivi (ti chiedera la password):

        sudo apt-get install python3-tk

2. Per lanciare lo script (_come al solito_) scrivi sul terminale python,
poi trascina lo script `dummy_gui.py` accanto (_ricorda lo spazio_) e premi invio:

        python /home/blabla/dummy_gui.py

![alt text](gui.png)

> Lo screenshot è stato fatto sul mac, su linux è leggermente diverso, ma comunque dovrebbe essere abbastanza intuitivo a capire cosa devi fare.
* **Select directory** - selezioni la cartella che vuoi copiare in questo caso la cartella "genitore" dove salvate i podcast.
* spunta **Zip Dummy folder** e **Include invisible file**.
* controlla che il percorso è giusto nella cassella grande dove scritto **Selected directory**.
* poi premi **Conferm and proceed**.

3. Se tutto ha funzionato secondo i piani, dovresti avere un file zip `SEND_ME.zip` nella stessa cartella dove ce il `dummy_gui.py`.
    * per sicurezza puoi aprire il send_me e controllare che combacia con la cartella
4. Fine
-----
## Command line

1. Per lanciare lo script (_come al solito_) scrivi sul terminale python
e poi trascina lo script `dummy_generator.py` accanto (_ricorda lo spazio_).
**NON PREMERE ANCORA INVIO**

        python /home/blabla/dummy_gui.py

2. Per abilitare le opzioni (zip file e include invisibile files) devi scrivere i seguenti argomenti
dopo il nome del file (_ricorda lo spazio_): `-z` (per zippare la cartella), `-i` (per includere i file invisibili).  **NON PREMERE ANCORA INVIO**

        python /home/blabla/dummy_gui.py -zi

> scrivere `-zi` o `-z -i` è uguale
3. Trascina la cartella che vuoi copiare in questo caso la cartella "genitore" dove salvate i podcast (_ricorda lo spazio_) e premi invio

         python /home/blabla/dummy_gui.py -zi /home/blabla/Desktop/Podcast

> se scrivi il percorso manualmente invece di trascinarlo, è importante scrivere
> fare attenzione se il nome è scritto con lettera maiuscola.
> desktop non è uguale a Desktop
4. Se tutto ha funzionato secondo i piani, dovresti avere un file zip `SEND_ME.zip` nella stessa cartella dove ce il `dummy_generator.py`.
    * per sicurezza puoi aprire il send_me e controllare che combacia con la cartella
5. Fine