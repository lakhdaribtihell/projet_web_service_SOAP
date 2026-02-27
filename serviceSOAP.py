from flask import Flask, request, Response
import xml.etree.ElementTree as ET

from database import get_city_from_vol, get_suggestions_from_db, insert_suggestion
from geo_service import get_places

app = Flask(__name__)

@app.route("/soap", methods=["POST"])
def soap_service():

    try:
        xml_data = request.data
        root = ET.fromstring(xml_data)

        vol_id = int(root.find("vol_id").text)
        type_lieu = root.find("type").text.lower()

    except:
        return Response("XML invalide", status=400)

    # 🔹 récupérer ville
    city = get_city_from_vol(vol_id)

    if not city:
        return Response("Vol non trouvé", status=404)

    # 🔹 vérifier si déjà en base
    db_results = get_suggestions_from_db(city, type_lieu)

    if db_results:
        results = [(desc, nom, type_, ville) for nom, desc, type_, ville in db_results]
    else:
        # 🔹 appeler API
        results = get_places(city, type_lieu)

        # 🔹 insérer en base
        for description, nom, type_, ville in results:
            insert_suggestion(description, nom, type_, ville)

    # 🔹 construire XML
    response_xml = "<suggestions>"

    for description, nom, type_, ville in results:
        response_xml += f"""
        <suggestion>
            <nom>{nom}</nom>
            <description>{description}</description>
            <type>{type_}</type>
            <ville>{ville}</ville>
        </suggestion>
        """

    response_xml += "</suggestions>"

    return Response(response_xml, mimetype="text/xml")


if __name__ == "__main__":
    print("SOAP Service running at http://127.0.0.1:5000/soap")
    app.run(debug=True)