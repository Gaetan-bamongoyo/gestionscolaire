# repartition_frais = [
#     {"frais":20, "tranche":"Inscription", "paye":0},
#     {"frais":70, "tranche":"Premier", "paye": 0},
#     {"frais":80, "tranche":"Deuxiement", "paye":0}
# ]

# montant = 180
# paiement = []

# for repartition in repartition_frais:
#     for i in range(len(repartition)):
#         reste = repartition["frais"] - repartition["paye"]
#         print(i)
#         if reste <= 0:
#             continue
#         if montant <= 0:
#             break
#         if montant >= reste:
#             repartition["paye"] += reste
#             montant -= reste
#             paiement.append({
#                 "frais": reste,
#                 "tranche": repartition["tranche"],
#                 "nom": "Gaetan"
#             })
#         else:
#             repartition["paye"] += montant
#             paiement.append({
#                 "frais": montant,
#                 "tranche": repartition["tranche"],
#                 "nom": "Gaetan"
#             })
#             montant = 0
# print(repartition_frais)
# print(paiement)

repartitions = [
    {"id": 1, "tranche": "Inscription", "frais": 20},
    {"id": 2, "tranche": "Premier", "frais": 70},
    {"id": 3, "tranche": "Deuxieme", "frais": 80},
]

paiements = [
    {"eleve_id": 1, "repartition_id": 1, "montant": 20},
    {"eleve_id": 1, "repartition_id": 2, "montant": 30},
    {"eleve_id": 2, "repartition_id": 1, "montant": 10},
]

eleve_id = 1
nouveau_paiement = 140

paiements_eleve = [p for p in paiements if p["eleve_id"] == eleve_id]

deja_paye = {}

for p in paiements_eleve:
    rid = p["repartition_id"]
    deja_paye[rid] = deja_paye.get(rid, 0) + p["montant"]

paiements_generes = []
montant = nouveau_paiement

for rep in repartitions:

    rep_id = rep["id"]
    frais = rep["frais"]
    paye = deja_paye.get(rep_id, 0)

    reste = frais - paye

    if reste <= 0: 
        continue

    if montant <= 0:
        break

    if montant >= reste:
        montant_utilise = reste
    else:
        montant_utilise = montant

    paiements_generes.append({
        "eleve_id": eleve_id,
        "repartition_id": rep_id,
        "montant": montant_utilise
    })

    montant -= montant_utilise

print(paiements_generes)