from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
import json
import matplotlib.pyplot as plt
import numpy as np
from ONEFactureScript import api_text_request

# Your JSON data
json_string = [
    """
{
  "heures_de_pointes": {
    "puissance_appelee": 55,
    "difference": 4971,
    "consommation_kWh": 5193,
    "prix_unitaire_HT_DH": 1.24185,
    "montant_DH_HT": 6448.93
  },
  "heures_pleines": {
    "puissance_appelee": 75,
    "difference": 17854,
    "consommation_kWh": 18684,
    "prix_unitaire_HT_DH": 0.880606,
    "montant_DH_HT": 16471.64
  },
  "heures_creuses": {
    "puissance_appelee": 75,
    "difference": 7298,
    "consommation_kWh": 7630,
    "prix_unitaire_HT_DH": 0.64895,
    "montant_DH_HT": 4951.49
},
  "Total_HT": 32516.87,
  "TVA": {
    "7%": 13.09,
    "10%": 6.6,
    "14%": 4471.21,
    "20%": 65.2
 },
    "Puissance_Installe": 100,
    "Puissance_a_vide": 0.3,
    "Mois_de_Consomation": "SEP 2023",
    "Total_a_regler": 37073.03,
    "Destinataire": "SOCIÉTÉ DOMAINES ROYAUX",
    "N_Client": 1000000293,
    "Type_compteur": "Electronique",
    "Option_Tarifiaire": "MT Général",
    "Energie_active": {
        "nouveau": 339744,
        "ancien": 334773,
        "difference": 4971
    },
    "Energie_reactive": {
        "nouveau": 18758,
        "ancien": 18124,
        "difference": 634
    },
    "CosPhi": 0.921,
    "Puissance_Souscrite": {
        "quantite": 48,
        "prix_unitaire": 674.51,
        "montant": 1799.68
    },
    "Depassement_Puissance": 2023.52,
    "Redevance_comptage": {
        "location": 187,
        "entretien": 326
    }
}
    """,
    """
    {
  "heures_de_pointes": {
    "puissance_appelee": 55,
    "difference": 4971,
    "consommation_kWh": 5193,
    "prix_unitaire_HT_DH": 1.24185,
    "montant_DH_HT": 6448.93
  },
  "heures_pleines": {
    "puissance_appelee": 75,
    "difference": 17854,
    "consommation_kWh": 18684,
    "prix_unitaire_HT_DH": 0.880606,
    "montant_DH_HT": 16471.64
  },
  "heures_creuses": {
    "puissance_appelee": 75,
    "difference": 7298,
    "consommation_kWh": 7630,
    "prix_unitaire_HT_DH": 0.64895,
    "montant_DH_HT": 4951.49
},
  "Total_HT": 32516.87,
  "TVA": {
    "7%": 13.09,
    "10%": 6.6,
    "14%": 4471.21,
    "20%": 65.2
 },
    "Puissance_Installe": 100,
    "Puissance_a_vide": 0.3,
    "Mois_de_Consomation": "OCT 2023",
    "Total_a_regler": 37073.03,
    "Destinataire": "SOCIÉTÉ DOMAINES ROYAUX",
    "N_Client": 1000000293,
    "Type_compteur": "Electronique",
    "Option_Tarifiaire": "MT Général",
    "Energie_active": {
        "nouveau": 339744,
        "ancien": 334773,
        "difference": 4971
    },
    "Energie_reactive": {
        "nouveau": 18758,
        "ancien": 18124,
        "difference": 634
    },
    "CosPhi": 0.934,
    "Puissance_Souscrite": {
        "quantite": 48,
        "prix_unitaire": 674.51,
        "montant": 1799.68
    },
    "Depassement_Puissance": 2023.52,
    "Redevance_comptage": {
        "location": 187,
        "entretien": 326
    }
}
    """,
    """
    {
  "heures_de_pointes": {
    "puissance_appelee": 55, 
    "difference": 4971,
    "consommation_kWh": 5193,
    "prix_unitaire_HT_DH": 1.24185,
    "montant_DH_HT": 6448.93
  },
  "heures_pleines": {
    "puissance_appelee": 75,
    "difference": 17854,
    "consommation_kWh": 18684,
    "prix_unitaire_HT_DH": 0.880606,
    "montant_DH_HT": 16471.64
  },
  "heures_creuses": {
    "puissance_appelee": 75,
    "difference": 7298,
    "consommation_kWh": 7630,
    "prix_unitaire_HT_DH": 0.64895,
    "montant_DH_HT": 4951.49
},
  "Total_HT": 32516.87,
  "TVA": {
    "7%": 13.09,
    "10%": 6.6,
    "16%": 4472.21,
    "20%": 65.2
 },
    "Puissance_Installe": 100,
    "Puissance_a_vide": 0.3,
    "Mois_de_Consomation": "NOV 2023",
    "Total_a_regler": 37073.03,
    "Destinataire": "SOCIÉTÉ DOMAINES ROYAUX",
    "N_Client": 1000000293,
    "Type_compteur": "Electronique",
    "Option_Tarifiaire": "MT Général",
    "Energie_active": {
        "nouveau": 339744,
        "ancien": 334773,
        "difference": 4971
    },
    "Energie_reactive": {
        "nouveau": 18758,
        "ancien": 18124,
        "difference": 634
    },
    "CosPhi": 0.926,
    "Puissance_Souscrite": {
        "quantite": 48,
        "prix_unitaire": 674.51,
        "montant": 1799.68
    },
    "Depassement_Puissance": 2023.52,
    "Redevance_comptage": {
        "location": 187,
        "entretien": 326
    }
}
    """
]

# Load the JSON data
data = [json.loads(json_str) for json_str in json_string]


# Define the path to your template and output
template_path = "template.docx"
output_path = "report.docx"

#Chart of CosPhi changes
def cosPhiChart(months, cosPhi):

    plt.plot(months, cosPhi, marker='o', markerfacecolor='lightblue', markersize=7)
    plt.ylabel("FP CosPhi")
    plt.title("Evolution du Facteur de Puissance CosPhi")

    # Add the value of cosPhi on each point marker
    for i in range(len(months)):
        plt.text(months[i], cosPhi[i], str(cosPhi[i]), ha='center', va='bottom')

    chart_path = "./CosPhiChart.png"
    plt.savefig(chart_path)
    plt.close()

    return chart_path

def pie1(energy_active_HPt, energy_active_HPL, energy_active_HCR):
    total = [sum(energy_active_HCR), sum(energy_active_HPL), sum(energy_active_HPt)]
    labels = ['E. Active HCR', 'E. Active HPL', 'E. Active HPt']
    plt.pie(total, colors=['grey', 'lightgreen', 'lightblue'], autopct='%1.1f%%')

    # Add legend with labels
    plt.legend(labels, loc="lower left")
    plt.title('REPARTITION DE LA CONSOMMATION PAR TRANCHE HORAIRE')

    chart_image_path = "./pie1.png"
    plt.tight_layout()
    plt.savefig(chart_image_path)
    plt.close()

    return chart_image_path

def psaChart(months, psa_arr):
    pourcentages = ["0%", "10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%", "100"]
    plt.bar(months, psa_arr, color="lightgreen", width=0.2)
    plt.title("TAUX DE CHARGE GLOBAL TRANSFOS (%)")

    chart_image_path = "./psaChart.png"
    plt.tight_layout()
    plt.savefig(chart_image_path)
    plt.close()

    return chart_image_path


# Function to generate a report
def generate_report(data, template_path, output_path):
    # Load your docx file
    doc = DocxTemplate(template_path)

    # Create empty lists to store data for chart generation
    months = []
    energy_active_HPt = ()
    energy_active_HPL = ()
    energy_active_HCR = ()

    cosPhi = ()

    #variables init
    consommation_global = 0
    cout_consommation_seul = 0
    prix_moy_KWH_TTC = 0
    prix_moy_KWH_HT = 0
    redevance_ps = 0
    Depassement_Puissance = 0
    Redevance_Comptage = 0
    total_prix_moy_HT = 0
    total_prix_moy_TTC = 0
    majCosPhi = 0
    prix_moy_KWH_consommation_seule = 0
    tva = []
    psa_arr = ()

    for item in data:
        if "14%" in item["TVA"]:
            tva.append(1.14)
        elif "16%" in item["TVA"]:
            tva.append(1.16)




    min_prix_moy_TTC = 10000000
    min_prix_moy_HT = 10000000
    total_prix_moy_cons_seule = 0
    max_prix_moy_TTC = 0
    max_prix_moy_HT = 0
    prix_moy_min = 0
    prix_moy_max = 0
    min_month = ""
    max_month = ""


    i = 0
    # Create the context including the data array
    all_contexts = []
    for item in data:
        Redevance_Comptage += (item["Redevance_comptage"]["location"] + item["Redevance_comptage"]["entretien"]) * tva[i]
        Depassement_Puissance += (item["Depassement_Puissance"] * tva[i])
        redevance_ps += (item["Puissance_Souscrite"]["montant"] * tva[i])
        consommation_global += (
                item["heures_de_pointes"]["consommation_kWh"] + item["heures_pleines"]["consommation_kWh"] + item["heures_creuses"]["consommation_kWh"]
        )
        cout_consommation_seul += (
            (item["heures_de_pointes"]["montant_DH_HT"] + item["heures_pleines"]["montant_DH_HT"] + item["heures_creuses"][
            "montant_DH_HT"]) * tva[i]
        )
        cout_global = consommation_global * tva[i]

        prix_moy_KWH_TTC = round(item["Total_a_regler"] / (item["heures_de_pointes"]["consommation_kWh"] + item["heures_pleines"]["consommation_kWh"] + item["heures_creuses"]["consommation_kWh"]), 2)
        prix_moy_KWH_HT = round(prix_moy_KWH_TTC/tva[i], 2)
        prix_moy_KWH_consommation_seule = round((item["heures_de_pointes"]["montant_DH_HT"] + item["heures_pleines"]["montant_DH_HT"] + item["heures_creuses"][
            "montant_DH_HT"]) / (item["heures_de_pointes"]["consommation_kWh"] + item["heures_pleines"]["consommation_kWh"] + item["heures_creuses"]["consommation_kWh"]), 2)


        total_prix_moy_HT += prix_moy_KWH_HT
        total_prix_moy_TTC += prix_moy_KWH_TTC
        total_prix_moy_cons_seule += prix_moy_KWH_consommation_seule

        if prix_moy_KWH_TTC < min_prix_moy_TTC:
            min_prix_moy_HT = prix_moy_KWH_HT
            min_prix_moy_TTC = prix_moy_KWH_TTC
            prix_moy_min = prix_moy_KWH_consommation_seule
            min_month = item["Mois_de_Consomation"]
        elif prix_moy_KWH_TTC > max_prix_moy_HT:
            max_prix_moy_TTC = prix_moy_KWH_TTC
            max_prix_moy_HT = prix_moy_KWH_HT
            prix_moy_max = prix_moy_KWH_consommation_seule
            max_month = item["Mois_de_Consomation"]

        psa = (item["heures_pleines"]["puissance_appelee"], item["heures_de_pointes"]["puissance_appelee"], item["heures_creuses"]["puissance_appelee"])

        psa = (max(psa)*100/item["CosPhi"]/item["Puissance_Installe"])
        psa_arr += (psa,)

        # Add data to lists for chart generation
        months.append(item["Mois_de_Consomation"])
        energy_active_HPt += (item["heures_de_pointes"]["difference"],)
        energy_active_HPL += (item["heures_pleines"]["difference"],)
        energy_active_HCR += (item["heures_creuses"]["difference"],)

        cosPhi += (item["CosPhi"],)

        majCosPhi += 2 * (0.8 - item["CosPhi"]) * ((item["Redevance_comptage"]["entretien"]+item["Redevance_comptage"]["location"]) + item["Puissance_Souscrite"]["montant"] + item["Depassement_Puissance"]) * tva[i]


        context = {
            "Destinataire": item["Destinataire"],
            "N_Client": item["N_Client"],
            "Option_Tarifiaire": item["Option_Tarifiaire"],
            "Type_compteur": item["Type_compteur"],
            "Puissance_Installe": item["Puissance_Installe"],
            "Mois_de_Consomation": item["Mois_de_Consomation"],
            "heures_de_pointes": item["heures_de_pointes"],
            "heures_pleines": item["heures_pleines"],
            "heures_creuses": item["heures_creuses"],
            "Puissance_Souscrite": item["Puissance_Souscrite"],
            "Consomation_global": round(consommation_global, 2),
            "Cout_global": round(cout_global, 2),
            "Cout_consommation_seul": round(cout_consommation_seul, 2),
            "redevance_ps": round(redevance_ps, 2),
            "Depassement_Puissance": round(Depassement_Puissance, 2),
            "Redevance_Comptage": round(Redevance_Comptage, 2),
            "prix_moy_KWH_TTC": prix_moy_KWH_TTC,
            "prix_moy_KWH_HT": prix_moy_KWH_TTC/tva[i],
            "prix_moy_KWH_consommation_seule": prix_moy_KWH_consommation_seule,
            "total_prix_moy_HT": round(total_prix_moy_HT/(i+1), 2),
            "total_prix_moy_TTC": total_prix_moy_TTC/(i+1),
            "prix_moy_KWH_consommation_seule_total": total_prix_moy_cons_seule/(i+1),
            "min_prix_moy_HT": min_prix_moy_HT,
            "min_prix_moy_TTC": min_prix_moy_TTC,
            "max_prix_moy_HT": max_prix_moy_HT,
            "max_prix_moy_TTC": max_prix_moy_TTC,
            "prix_moy_min": prix_moy_min,
            "prix_moy_max": prix_moy_max,
            "min_month": min_month,
            "max_month": max_month,
            "min_CosPhi": min(cosPhi),
            "max_CosPhi": max(cosPhi),
            "average_CosPhi": sum(cosPhi)/len(cosPhi),
            "majCosPhi": round(majCosPhi, 2)

        }



        all_contexts.append(context)
        i += 1

    # Generate the chart
    width = 0.1
    xpos = np.arange(len(months))
    plt.figure(figsize=(10, 7))
    plt.bar(xpos, energy_active_HPt, color='lightblue', width=width, label='E. Active HPt')
    plt.bar(xpos+0.1, energy_active_HPL, color='lightgreen', width=width, label='E. Active HPL')
    plt.bar(xpos+0.2, energy_active_HCR, color='grey', width=width, label='E. Active HCR')

    plt.xlabel('Months')
    plt.ylabel('Energy (kWh)')
    plt.title('EVOLUTION CONSOMMATION (KWh) par Tranche Horaire')
    plt.xticks(xpos, months)
    plt.legend()

    # Save the chart as an image
    chart_image_path = "./chart.png"
    plt.tight_layout()
    plt.savefig(chart_image_path)
    plt.close()

    pie1_path = pie1(energy_active_HPt, energy_active_HPL, energy_active_HCR)
    cosPhi_chart_path = cosPhiChart(months, cosPhi)

    psaChart_path = psaChart(months, psa_arr)

    response = api_text_request(all_contexts)

    all_contexts[-1]["chart_image"] = InlineImage(doc, chart_image_path, width=Mm(120))
    all_contexts[-1]["pie1"] = InlineImage(doc, pie1_path, width=Mm(60))
    all_contexts[-1]["cosPhiChart"] = InlineImage(doc, cosPhi_chart_path, width=Mm(150))
    all_contexts[-1]["psaChart"] = InlineImage(doc, psaChart_path, width=Mm(150))

    # Replace placeholders with actual values and save the result
    doc.render({"data": all_contexts})  # Pass all contexts as a list under the key "data"
    doc.save(output_path)

# Generate the report
#generate_report(data, template_path, output_path)