from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
import json
import matplotlib.pyplot as plt
import numpy as np
import os

# Your JSON data
json_string = [
    """
{
  "heures_de_pointes": {
    "nouveau": 339744,
    "ancien": 334773,
    "difference": 4971,
    "consommation_kWh": 5193,
    "prix_unitaire_HT_DH": 1.24185,
    "montant_DH_HT": 6448.93
  },
  "heures_pleines": {
    "nouveau": 1805712,
    "ancien": 1787858,
    "difference": 17854,
    "consommation_kWh": 18684,
    "prix_unitaire_HT_DH": 0.880606,
    "montant_DH_HT": 16471.64
  },
  "heures_creuses": {
    "nouveau": 659000,
    "ancien": 651702,
    "difference": 7298,
    "consommation_kWh": 7630,
    "prix_unitaire_HT_DH": 0.64895,
    "montant_DH_HT": 4951.49
},
  "Total_HT": 4556.16,
  "TVA": {
    "7%": 13.09,
    "10%": 6.6,
    "14%": 4471.21,
    "20%": 65.2
 },
    "Puissance_Installe": 0.3,
    "Puissance_a_vide": 0,
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
    "nouveau": 339744,
    "ancien": 334773,
    "difference": 4971,
    "consommation_kWh": 5193,
    "prix_unitaire_HT_DH": 1.24185,
    "montant_DH_HT": 6448.93
  },
  "heures_pleines": {
    "nouveau": 1805712,
    "ancien": 1787858,
    "difference": 17854,
    "consommation_kWh": 18684,
    "prix_unitaire_HT_DH": 0.880606,
    "montant_DH_HT": 16471.64
  },
  "heures_creuses": {
    "nouveau": 659000,
    "ancien": 651702,
    "difference": 7298,
    "consommation_kWh": 7630,
    "prix_unitaire_HT_DH": 0.64895,
    "montant_DH_HT": 4951.49
},
  "Total_HT": 4556.16,
  "TVA": {
    "7%": 13.09,
    "10%": 6.6,
    "14%": 4471.21,
    "20%": 65.2
 },
    "Puissance_Installe": 0.3,
    "Puissance_a_vide": 0,
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
    """
]

# Load the JSON data
data = [json.loads(json_str) for json_str in json_string]


# Define the path to your template and output
template_path = "template.docx"
output_path = "report.docx"

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



# Function to generate a report
def generate_report(data, template_path, output_path):
    # Load your docx file
    doc = DocxTemplate(template_path)

    # Create empty lists to store data for chart generation
    months = []
    energy_active_HPt = ()
    energy_active_HPL = ()
    energy_active_HCR = ()

    #variables init
    consommation_global = 0
    cout_consommation_seul = 0
    consommation_item = 0
    redevance_ps = 0
    Depassement_Puissance = 0
    Redevance_Comptage = 0

    # Create the context including the data array
    all_contexts = []
    for item in data:
        Redevance_Comptage += (item["Redevance_comptage"]["location"] + item["Redevance_comptage"]["entretien"])
        Depassement_Puissance += (item["Depassement_Puissance"])
        redevance_ps += (item["Puissance_Souscrite"]["montant"])
        consommation_global += (
                item["heures_de_pointes"]["consommation_kWh"] + item["heures_pleines"]["consommation_kWh"] + item["heures_creuses"]["consommation_kWh"]
        )
        cout_consommation_seul += (
                item["heures_de_pointes"]["montant_DH_HT"] + item["heures_pleines"]["montant_DH_HT"] + item["heures_creuses"][
            "montant_DH_HT"]
        )
        cout_global = consommation_global * 1.16

        # Add data to lists for chart generation
        months.append(item["Mois_de_Consomation"])
        energy_active_HPt += (item["heures_de_pointes"]["difference"],)
        energy_active_HPL += (item["heures_pleines"]["difference"],)
        energy_active_HCR += (item["heures_creuses"]["difference"],)

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
            "Consomation_global": consommation_global,
            "Cout_global": cout_global,
            "Cout_consommation_seul": cout_consommation_seul,
            "redevance_ps": redevance_ps,
            "Depassement_Puissance": Depassement_Puissance,
            "Redevance_Comptage": Redevance_Comptage,
        }
        all_contexts.append(context)

    # Generate the chart
    width = 0.1
    print(energy_active_HPL)
    print(energy_active_HPt)
    print(energy_active_HCR)
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

    all_contexts[-1]["chart_image"] = InlineImage(doc, chart_image_path, width=Mm(120))
    all_contexts[-1]["pie1"] = InlineImage(doc, pie1_path, width=Mm(60))


    # Replace placeholders with actual values and save the result
    doc.render({"data": all_contexts})  # Pass all contexts as a list under the key "data"
    doc.save(output_path)

# Generate the report
generate_report(data, template_path, output_path)

