import os
import csv
from PIL import Image
import tkinter as tk
from tkinter import filedialog, messagebox
from transformers import BlipProcessor, BlipForConditionalGeneration
from deep_translator import GoogleTranslator

# === Boîte de dialogue pour sélectionner le dossier ===
root = tk.Tk()
root.withdraw()
image_dir = filedialog.askdirectory(title="Sélectionnez le dossier contenant les images")
if not image_dir:
    messagebox.showinfo("Information", "Aucun dossier sélectionné. Fin du script.")
    exit()

# === Chargement du modèle BLIP ===
print("🔄 Chargement du modèle BLIP...")
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
print("✅ Modèle chargé.\n")

# === Fonction de génération de description ALT en anglais ===
def generate_alt_text_en(image_path):
    try:
        image = Image.open(image_path).convert('RGB')
        inputs = processor(image, return_tensors="pt")
        out = model.generate(**inputs)
        return processor.decode(out[0], skip_special_tokens=True)
    except Exception as e:
        return f"[Erreur BLIP : {e}]"

# === Traduction automatique vers le français ===
def translate_to_french(text):
    try:
        return GoogleTranslator(source='auto', target='fr').translate(text)
    except Exception as e:
        return f"[Erreur de traduction : {e}]"

# === Coupe propre à 150 caractères max ===
# DESACTIVEE POUR L'INSTANT
def truncate_rgaa(text, limit=150):
    if len(text) <= limit:
        return text
    return text[:limit].rsplit(' ', 1)[0].rstrip('.,;:!?') + "…"

# === Traitement ===
results = []
print(f"📂 Traitement des images dans : {image_dir}\n")
fichiers = sorted(os.listdir(image_dir))

for i, filename in enumerate(fichiers, 1):
    if filename.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
        path = os.path.join(image_dir, filename)
        print(f"[{i}] {filename}")
        alt_en = generate_alt_text_en(path)
        alt_fr = translate_to_french(alt_en)
        # alt_fr_tronque inutilisé (incertitude si RGAA limite à 150 caractères)
        alt_fr_tronque = truncate_rgaa(alt_fr)
        # alt_fr à remplacer par alt_fr_tronque si on veut tronquer à 150 caractères)
        results.append((filename, alt_fr))
    else:
        print(f"[{i}] Ignoré : {filename}")

# === Export CSV ===
csv_path = os.path.join(image_dir, "descriptions_alt_fr.csv")
with open(csv_path, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["fichier", "description_alt_fr"])
    writer.writerows(results)

print(f"\n✅ Export terminé : {csv_path}")
messagebox.showinfo("Terminé", f"Descriptions générées en français dans :\n{csv_path}")

# === Génération d'une page HTML d'aperçu ===
html_path = os.path.join(image_dir, "aperçu_alt.html")

with open(html_path, "w", encoding="utf-8") as f:
    f.write("<!DOCTYPE html>\n<html lang='fr'>\n<head>\n")
    f.write("<meta charset='UTF-8'>\n<title>Aperçu des balises ALT</title>\n")
    f.write("<style>\ntable { width: 100%; border-collapse: collapse; }\n")
    f.write("td, th { border: 1px solid #ccc; padding: 8px; vertical-align: top; }\n")
    f.write("img { max-width: 300px; height: auto; }\n")
    f.write("</style>\n</head>\n<body>\n")
    f.write("<h1>Aperçu des balises ALT générées</h1>\n")
    f.write("<table>\n<tr><th>Image (avec balise ALT)</th><th>Texte ALT</th></tr>\n")

    for filename, alt_text in results:
        relative_path = os.path.basename(filename)  # image dans le même dossier
        f.write(f"<tr><td><img src='{relative_path}' alt='{alt_text}'></td><td>{alt_text}</td></tr>\n")

    f.write("</table>\n</body>\n</html>")

print(f"🌐 Fichier HTML généré : {html_path}")
