#%%
import cx_Oracle, numpy as np, matplotlib.pyplot as plt
from matplotlib import transforms

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

percentage = round(zone[1] * 100 / (zone[0] + zone[1]))

plt.pie(np.array(zone), labels=country)

centre_circle = plt.Circle((0,0),0.70,fc='white', alpha=1)
fig = plt.gcf()
fig.gca().add_artist(centre_circle)

plt.text(0, 0, f"{percentage} %", dict(size=20), va='center', ha='center')
plt.text(0, 0, f"\n\n\nà l'étranger", dict(size=9), va='center', ha='center')



plt.show

#%%
request =(   "SELECT COUNT(*) FROM Commande co")
request2=(   "SELECT COUNT(*) FROM VLivraison_PB")

print(request, " ", request2)

zone = [0, 0]
labels = ["Livraisons complètes", "Livraisons problématiques"]
for res in cursor.execute(request):
    zone[0] = res[0]
for res in cursor.execute(request2):
    zone[1] = res[0]
zone[0]-=zone[1]

percentage = round(zone[1] * 100 / (zone[0] + zone[1]))

print(percentage, zone)

plt.pie(np.array(zone), labels=labels)

centre_circle = plt.Circle((0,0),0.70,fc='white', alpha=1)
fig = plt.gcf()
fig.gca().add_artist(centre_circle)
plt.text(0, 0, f"{percentage} %", dict(size=20), va='center', ha='center')

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

plt.barh([i for i in range(0, nb_clients)], meilleurs_clients_ca_rapporte, tick_label=meilleurs_clients_noms)
    
plt.show

# %%
request = """SELECT ROUND(AVG(co.montantttc), 2) AS MOY
             FROM client c, etiquette e, commande co
             WHERE c.codeetiquette = e.codeetiquette
             AND co.numclient = c.numclient"""
print(request)

for res in cursor.execute(request):
    final = round(res[0], 2)

plt.pie([final, 0])
centre_circle = plt.Circle((0,0),0.65,fc='white', alpha=1)
fig = plt.gcf()
fig.gca().add_artist(centre_circle)

plt.text(0, 0, f"{final} €", dict(size=20), va='center', ha='center')
plt.text(0, 0, f"\n\n\ntous pays confondus", dict(size=9), va='center', ha='center')
    
plt.show

#%%
#%%
nb_produits = 5
request =f"""SELECT *
             FROM (  SELECT A.nomArticle, SUM(d.quantitecommandee * tv.prixvente) as ventes
             FROM Detail_Commande D, Article A, tarif_vente tv
             WHERE D.numarticle=A.numArticle
             AND tv.numarticle = d.numarticle
             GROUP BY A.nomArticle
             ORDER BY ventes DESC
             )
             WHERE ROWNUM <= {nb_produits}
            """
            
request2= """SELECT SUM(ventes)
             FROM (  SELECT A.nomArticle, SUM(d.quantitecommandee * tv.prixvente) as ventes
                     FROM Detail_Commande D, Article A, tarif_vente tv
                     WHERE D.numarticle=A.numArticle
                     AND tv.numarticle = d.numarticle
                     GROUP BY A.nomArticle
                     ORDER BY ventes DESC
)"""

print(request, "\n", request2)

prix = [int(0) for i in range(nb_produits + 1)]
produits = ["" for i in range(nb_produits)]
produits.append("Autres")
i = 0
for res in cursor.execute(request):
    produits[i] = res[0]
    prix[i] = res[1]
    print(i)
    i+=1
for res in cursor.execute(request2):
    prix[i] = res[0]

plt.pie(np.array(prix), labels=produits, autopct='%1.2f%%', pctdistance=0.85)

centre_circle = plt.Circle((0,0),0.70,fc='white', alpha=1)
fig = plt.gcf()
fig.gca().add_artist(centre_circle)


plt.show

# %%
request = """SELECT cat.libellecategorie, c.cat1, c.commandes
                 FROM (  SELECT c.numcatpere, c.libellecategorie AS CAT1, COUNT(co.numcommande) AS COMMANDES
                         FROM Categorie C, article a, commande co, detail_commande d
                         WHERE c.numcategorie = a.numcategorie
                         AND co.numcommande = d.numcommande
                         AND d.numarticle = a.numarticle
                         GROUP BY c.numcatpere, c.libellecategorie
                    ) C, Categorie cat
                 WHERE c.numcatpere = cat.numcategorie
                 ORDER BY c.commandes DESC"""
                 
noms = []
nb_commandes = []
cmd = 0
print(request)

for res in cursor.execute(request):
    noms.append(res[0] + " : " + res[1])
    nb_commandes.append(res[2])
    cmd+=1

plt.barh([i for i in range(0, cmd)], nb_commandes, tick_label=noms)
    
plt.show