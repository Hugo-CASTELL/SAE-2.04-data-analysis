#%%
import cx_Oracle, numpy as np, matplotlib.pyplot as plt

dsn = cx_Oracle.makedsn(host='oracle.iut-blagnac.fr', port=1521, sid='db11g')

connection = cx_Oracle.connect(user="SAEBD39",
                               password="hugoLUCAhehehe",
                               dsn=dsn,
                               encoding="UTF-8")

cursor = connection.cursor()

#%%
request =(   "SELECT e.codetypetva, SUM(d.quantitelivree * tv.prixvente)"
+           " FROM client c, etiquette e, commande co, detail_commande d, tarif_vente tv"
+           " WHERE c.codeetiquette = e.codeetiquette"
+           " AND co.numclient = c.numclient"
+           " AND d.numcommande = co.numcommande"
+           " AND tv.numarticle = d.numarticle"
+           " GROUP BY e.codetypetva")

print(request)

zone = [0, 0]
country = ["France", "Etranger"]
for res in cursor.execute(request):
    if(res[0] == 1):
        zone[0] += res[1]
    else:
        zone[1] += res[1]

plt.pie(np.array(zone), labels=country)

centre_circle = plt.Circle((0,0),0.70,fc='white', alpha=1)
fig = plt.gcf()
fig.gca().add_artist(centre_circle)

plt.show
# %%
request =(   "SELECT e.codetypetva, COUNT(l.numcommande)"
+           " FROM client c, etiquette e, VLivraison_PB l"
            " WHERE c.numclient = l.numclient"
            " AND c.codeetiquette = e.codeetiquette"
            " GROUP BY e.codetypetva")

print(request)

zone = [0, 0]
country = ["France", "Etranger"]
total = 0
for res in cursor.execute(request):
    if(res[0] == 1):
        zone[0] += res[1]
    else:
        zone[1] += res[1]

for somme in zone:
    total += somme

print(zone)

plt.rcdefaults()
fig, ax = plt.subplots()

plt.barh([0, 1], zone, tick_label=country)
ax.set_xlabel('Problèmes de livraisons')
ax.set_title('Nombre de problèmes de livraison par zone')

plt.show
# %%
nb_clients = 5
request = ( "SELECT *"
+           " FROM VClient_Commande_CA"
+          f" WHERE ROWNUM <= {nb_clients}")

meilleurs_clients_noms = []
meilleurs_clients_ca_rapporte = []

print(request)

for res in cursor.execute(request):
    meilleurs_clients_noms.append(res[0])
    meilleurs_clients_ca_rapporte.append(res[1])

print(meilleurs_clients_noms, " ", meilleurs_clients_ca_rapporte)

plt.rcdefaults()
fig, ax = plt.subplots()

fig = plt.figure()
ax.bar(meilleurs_clients_noms, meilleurs_clients_ca_rapporte, width=0.8)

plt.show

# %%
