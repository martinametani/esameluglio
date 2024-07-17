import datetime

class ExamException(Exception):
     pass

class CSVTimeSeriesFile:

    def __init__(self,name):
        self.name = name

    def get_data(self): #metodo per prendere i dati
        # lista da ritornare in caso di successo
        ret_list = []

        # questa la uso per caricare solo i timestamp..
        # la userò per vedere se è ordinata e se ci sono duplicati
        checklist = []

        #
        #   verifico se il file è leggibile e se esiste
        #
        try:
            my_file = open(self.name,"r")
            my_file.readline()
            my_file.close()
        except Exception as e:
            raise ExamException("File non trovato o illeggibile")

        #
        # inizio a leggere
        #
        with open(self.name,"r") as csv_file:

            for line in csv_file:
                elements = line.strip("\n").split(",")



                if elements[0] == "epoch": #se trovo epoch sono sull'int.
                        #sono sull'intestazione, skippo
                        print('skippo intestazione --> "{}" '.format(elements))
                        continue

                # controllo l'intestazione
                if len(elements) < 2:
                    print('manca almeno un parametro nella riga: --> "{}" - SKIP'.format(elements))
                    continue

                # posso assegnare alle variabili
                epoch = elements[0]
                temperature = elements[1]

                #controlla che la data sia valida --> se non int skippa
                try:
                    epoch_int = int(epoch)
                except Exception as e:
                    print("impossibile convertire la data --> {} - SKIP".format(elements[0]))
                    continue

                # controlla che la temperatura sia float (comprende int)
                try:
                    temperatura_float = float(temperature)
                except Exception as e:
                    print("impossibile convertire la temperatura --> {} - SKIP".format(temperature))
                    continue



                # aggiungo alla lista
                time_series = [epoch,temperature] #come è fatta la ts
                ret_list.append(time_series)
                checklist.append(epoch) #nella check list vogliamo solo gli epoch perchè sono loro che ordinano la ts

            # controllo se la lista è ordinata
            test_lista = checklist.copy()  #copio check list nel test lista
            test_lista.sort()

            if test_lista == checklist:
                #tutto ordinato
                print("La lista è ordinata")
            else:
                #non ordinata
                raise ExamException("la lista NON è ordinata")

            # controllo se la lista ha duplicati
            lunghezza_lista = len(checklist)
            lunghezza_set_lista = len(set(checklist))  #set toglie i duplicati

            if lunghezza_lista == lunghezza_set_lista:
                # non ci sono duplicati
                print("La lista non contiene duplicati")
            else:
                #duplicati... eccezione
                raise ExamException("La lista contiene dei duplicati")


        # fine, restituisco la lista (non checklist perchè era temporanea)
        return ret_list

def compute_daily_max_difference (time_series):

    ret = []  #inizializzo lista vuota di ritorno
    min = float('inf') #min = infinito
    max = 0
    # questo mi serve per sapere se sono al primo giorno in cui non ho giorni precedenti
    primogiorno = True #inizializzo come true il primo giorno perchè sono al 1 giorno

    for riga in time_series:

        epoch = riga[0]  #prima colonna
        temperatura = float(riga[1]) #seconda colonna

        if float(epoch) % 86400 == 0: #il resto fa 0 -> mezzanotte
            print ("Nuovo giorno")
            if primogiorno:
                # sto facendo il nuovo giorno quindi non ho valori dei giorni precedenti
                primogiorno = False #se supero il primo giorno poi diventa false --> se epoch % 86400 == 0 allora sono al giorno successivo
            else:  #sono dal secondo giorno in poi
                # scrivo la differenza del giorno precedente se sono al giorno dopo
                if (max - min) == 0:
                    ret.append(None)  #none se se ho unico dato nella giornata
                else:
                    
                    ret.append(round(max-min,2)) #round approssima a  cifre decimali
            min = temperatura
            max = temperatura #ora confronto temperature dei vari giorni

        if temperatura < min:
            min = temperatura
        if temperatura > max:
            max = temperatura

        print ("--> {} - {} {}".format(temperatura,min,max))

    # ultimo giorno
    ret.append(round(max-min,2))

    #finito, esco
    return ret

#main

time_series_file = CSVTimeSeriesFile(name='data.csv')
time_series = time_series_file.get_data()

print(compute_daily_max_difference (time_series))