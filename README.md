# Générateur de balises ALT pour l’accessibilité des images

Ce script Python permet de générer automatiquement des **descriptions alternatives (balises `alt`)** en français pour un lot d’images (couvertures, illustrations, figures, etc.), afin de respecter les exigences du **RGAA** (Référentiel Général d'Amélioration de l'Accessibilité).

- Réalisé pour répondre à des besoins spécifiques des Presses universitaires de Rouen et du Havre (PURH)
- Licence MIT

Il utilise :
- Le modèle **BLIP** (Salesforce) pour analyser l’image,
- La **traduction automatique** via [deep-translator](https://pypi.org/project/deep-translator/) (Google Translate),
- Une interface simple avec **boîte de dialogue** pour choisir le dossier,
- Présence dans le code d'une fonction de **limite automatique à 256 caractères** pour conformité RGAA (fonction désactivée pour l'instant en raison des incertitudes de la RGAA sur ce point)
- Un **CSV exporté** avec les textes alternatifs,
- Un **aperçu HTML visuel** des images et de leurs balises ALT.

---

## Tutoriel
https://youtu.be/Zb2LoKAMums

## 🧰 Installation

Dans un terminal :

```bash
pip install transformers torch pillow deep-translator
