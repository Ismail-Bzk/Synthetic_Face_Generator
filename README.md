# Rapport Technique - Migration Blender 3.5 (Synthetic Face Generator)

1️⃣ Résumé exécutif

Objectif de la migration
- Mettre à jour tous les scripts Python du projet pour une compatibilité Blender 3.5.x en mode `--background`, sans perdre de fonctionnalités (textures tête/yeux, HDRI, gaze, caméras, rendu, metadata CSV).

Risques majeurs identifiés
- Parsing `sys.argv` fragile en mode background (décalage des arguments).
- Opérateurs KeenTools non disponibles ou signatures variables.
- Sockets du Principled BSDF indexés (fragiles si l’ordre change).
- `World`/nodes absents en scène, causant des erreurs lors du rendu.
- Accès `bpy.ops` contextuel (non déterministe en `--background`).
- Fuites mémoire via `to_mesh()` sans `to_mesh_clear()`.
- `background_images` caméra non garanti selon contexte.

Bénéfices globaux après migration
- Exécution CLI plus stable, erreurs mieux diagnostiquées.
- Pipeline de rendu robuste, même en batch/background.
- Moins de fuites mémoire, meilleure stabilité sur longues séries.
- Compatibilité Blender 3.5 renforcée sans régression fonctionnelle.

Version Blender cible exacte (3.5.x)
- Blender 3.5.x (test recommandé: 3.5.1).

2️⃣ Vue d’ensemble des changements Blender 3.3 → 3.5

API Python (bpy)
- Certaines propriétés et sockets de nodes deviennent moins fiables par index; préférer les noms.
- Les opérateurs sont plus stricts sur le contexte (mode background).

Contexte et overrides
- `bpy.ops` nécessite un contexte actif (objet sélectionné/actif). En background, l’API data est plus sûre.

Rendu (Cycles / Eevee)
- Les devices GPU nécessitent souvent `prefs.get_devices()` avant usage.
- Le denoising peut être accessible via `view_layer` selon la version.

Python embarqué
- Blender 3.5 est basé sur Python 3.10; éviter `eval` et conversions implicites.

Modules dépréciés ou remplacés
- Import OBJ: `wm.obj_import` existe en 3.5, mais fallback requis pour compatibilité.

3️⃣ Analyse fichier par fichier (OBLIGATOIRE)

Launch.py
- Rôle: point d’entrée CLI Blender, orchestration du pipeline (modèle, scène, animation, rendu).
- Problèmes identifiés en 3.5: `sys.argv` indexé fragile; Cycles denoising pas toujours sur `scene`.
- Modifications appliquées: parsing robuste des 13 args après `--`; conversions typées; fallback denoising; passage d’arguments explicites aux classes.
- Justification technique: Blender injecte des arguments internes en background; parsing robuste évite erreurs silencieuses.
- Impact: automatisation plus fiable; fonctionnalités inchangées.

model.py
- Rôle: setup FaceBuilder, textures tête/yeux, HDRI, création et pose des yeux.
- Problèmes identifiés en 3.5: opérateurs KeenTools non garantis; `World`/nodes absents; sockets Principled indexés; `sys.argv` direct; fuite mémoire `to_mesh()`.
- Modifications appliquées: wrappers KeenTools (`_try_keentools_op`, `_pickmode_starter`); création sécurisée de `World` et nodes; sockets nommés; `start(texture_id)`; `to_mesh_clear()`.
- Justification technique: ops manquantes = crash; sockets indexés fragiles; `World` absent casse le rendu; `to_mesh_clear` évite fuites.
- Impact: stabilité accrue, rendu identique, compat 3.5 renforcée.

MyScene.py
- Rôle: caméra, lumière, DoF, background.
- Problèmes identifiés en 3.5: contraintes via `bpy.ops` instables en background; `World`/nodes non garantis.
- Modifications appliquées: contraintes via API data (`constraints.new`); création/liaison sûre du `World`.
- Justification technique: éviter dépendance à `bpy.context` en mode background.
- Impact: robustesse améliorée, rendu identique.

AnimGaze.py
- Rôle: animation des yeux et tête.
- Problèmes identifiés en 3.5: `eval(fixed)` dangereux et non déterministe.
- Modifications appliquées: parsing booléen explicite (`_parse_bool`).
- Justification technique: éviter exécution arbitraire et erreurs de type.
- Impact: animation inchangée, stabilité améliorée.

GenPupils.py
- Rôle: génération dataset (rendu + metadata + CSV).
- Problèmes identifiés en 3.5: `World`/nodes absents; `background_images` non garanti; `sys.argv` pour `run_id`; `to_mesh()` sans clear; `ray_cast` boolean; devices GPU non initialisés.
- Modifications appliquées: `run_id` explicite; `_ensure_world_nodes` + `_load_image`; guard `background_images`; `to_mesh_clear`; `os.makedirs`; `hit and ...`; `prefs.get_devices()`; `check_existing=True`.
- Justification technique: stabilité background + mémoire + reproductibilité.
- Impact: dataset inchangé; automation et stabilité améliorées.

synthetic_face_ui.py
- Rôle: UI Tkinter, lancement Blender CLI.
- Problèmes identifiés en 3.5: erreurs Blender masquées; fichiers images non fermés.
- Modifications appliquées: `Image.open` via context manager; `subprocess.run(check=True)`.
- Justification technique: meilleure gestion ressources + remontée d’erreurs Blender.
- Impact: UI stable, debugging facilité.

utils/Clothes1.py
- Rôle: import assets paramétrables (cheveux/vêtements/masques) + matériaux.
- Problèmes identifiés en 3.5: sockets Principled indexés; import OBJ variable; contraintes via ops; duplication images.
- Modifications appliquées: sockets nommés; fallback import OBJ; contraintes via data API; `check_existing=True`.
- Justification technique: sockets stables + robustesse en background.
- Impact: rendu identique, stabilité accrue.

utils/Hat1.py
- Rôle: import hats/masks paramétrables.
- Problèmes identifiés en 3.5: identiques à Clothes1.
- Modifications appliquées: mêmes patterns (sockets nommés, fallback import, contraintes data API).
- Justification technique: stabilité 3.5.
- Impact: inchangé fonctionnellement.

utils/Clothes.py
- Rôle: ancienne gestion d’assets (hair/clothes/mask).
- Problèmes identifiés en 3.5: import OBJ dépend de l’opérateur disponible.
- Modifications appliquées: fallback `import_obj`.
- Justification technique: compatibilité 3.5 avec différents importeurs.
- Impact: inchangé.

utils/Hat.py
- Rôle: ancienne gestion hats/masks/sunglasses/beard.
- Problèmes identifiés en 3.5: import OBJ non garanti.
- Modifications appliquées: fallback `import_obj`.
- Justification technique: compatibilité 3.5.
- Impact: inchangé.

utils/EyePupils.py
- Rôle: calcul pupilles + projection 2D.
- Problèmes identifiés en 3.5: fuite mémoire `to_mesh()`; bool `hit &`.
- Modifications appliquées: `to_mesh_clear`; `hit and`.
- Justification technique: stabilité mémoire + logique bool correcte.
- Impact: résultats identiques, stabilité améliorée.

utils/EarToCsv.py
- Rôle: génération CSV blendshapes/landmarks.
- Problèmes identifiés en 3.5: variables `scene/cam` non définies; fuite `to_mesh()`.
- Modifications appliquées: définition explicite `scene/cam`; `to_mesh_clear()`.
- Justification technique: éviter crash et fuite mémoire.
- Impact: inchangé.

utils/__init__.py
- Rôle: expose modules utils.
- Problèmes identifiés en 3.5: aucun.
- Modifications appliquées: aucune.
- Justification technique: N/A.
- Impact: inchangé.

WithoutTracking/3Dto2Dpixels.py
- Rôle: conversion 3D→2D hors tracking.
- Problèmes identifiés en 3.5: dépend d’objets nommés; non testé en background.
- Modifications appliquées: aucune.
- Justification technique: utilitaire hors pipeline principal.
- Impact: inchangé.

WithoutTracking/AnimationTaskNewWithoutTrack.py
- Rôle: animation alternative sans tracking.
- Problèmes identifiés en 3.5: dépend de `bpy.context.active_object`.
- Modifications appliquées: aucune.
- Justification technique: hors pipeline principal.
- Impact: inchangé.

WithoutTracking/csv_file.py
- Rôle: export CSV des objets sélectionnés.
- Problèmes identifiés en 3.5: dépend de sélection active.
- Modifications appliquées: aucune.
- Justification technique: utilitaire isolé.
- Impact: inchangé.

WithoutTracking/CreateWithoutTrack.py
- Rôle: création des yeux sans tracking.
- Problèmes identifiés en 3.5: usage intensif d’opérateurs contextuels.
- Modifications appliquées: aucune.
- Justification technique: hors pipeline principal.
- Impact: inchangé.

WithoutTracking/camera-matrix-from-blender-camera.py
- Rôle: extraction matrices caméra.
- Problèmes identifiés en 3.5: dépend du nom caméra.
- Modifications appliquées: aucune.
- Justification technique: utilitaire isolé.
- Impact: inchangé.

WithoutTracking/AnimJaw_Mouth.py
- Rôle: animation bouche/yeux.
- Problèmes identifiés en 3.5: dépend de noms de KeyBlocks.
- Modifications appliquées: aucune.
- Justification technique: hors pipeline principal.
- Impact: inchangé.

4️⃣ Changements transversaux (cross-files)

Gestion du contexte
- Migration de `bpy.ops` vers l’API data pour constraints/modifiers.

Sélection / activation d’objets
- Réduction de dépendance à `bpy.context.view_layer.objects.active`.

Gestion des scènes et collections
- Création systématique du `World` si absent.

Accès aux matériaux, textures, nodes
- Utilisation de sockets nommés du Principled BSDF.
- Chargement d’images avec `check_existing=True`.

Rendu automatisé (Cycles settings)
- Initialisation `prefs.get_devices()` avant GPU.
- Fallback denoising `view_layer`.

Logging et gestion d’erreurs
- Warnings explicites pour opérateurs KeenTools absents.
- Exceptions propagées via `subprocess.run(check=True)`.

5️⃣ Tableau récapitulatif des changements API

| API Blender 3.3 | Problème en 3.5 | Solution adoptée | Fichier(s) |
|---|---|---|---|
| `bpy.ops.wm.obj_import` uniquement | importeur OBJ variable | fallback `import_scene.obj` | `utils/Clothes.py`, `utils/Hat.py`, `utils/Clothes1.py`, `utils/Hat1.py` |
| Sockets Principled indexés | indices fragiles | sockets nommés (`Specular`, `Normal`) | `model.py`, `utils/Clothes1.py`, `utils/Hat1.py` |
| `bpy.context.scene.world` implicite | `World` peut être None | création explicite + `use_nodes` | `model.py`, `MyScene.py`, `GenPupils.py` |
| `cam.data.background_images` direct | non garanti | guard `hasattr` | `GenPupils.py` |
| `scene.cycles.use_denoising` | propriété variable | fallback `view_layer.cycles` | `Launch.py` |
| `bpy.ops.object.constraint_add` | dépend contexte | `constraints.new` | `model.py`, `MyScene.py`, `utils/Clothes1.py`, `utils/Hat1.py` |
| `to_mesh()` sans clear | fuite mémoire | `to_mesh_clear()` | `model.py`, `GenPupils.py`, `utils/EyePupils.py`, `utils/EarToCsv.py` |
| `sys.argv` indexé | args décalés | parsing structuré | `Launch.py`, `GenPupils.py`, `model.py` |

6️⃣ Problèmes évités grâce à la migration
- Crash en background dû à `bpy.ops` sans contexte actif.
- Rendus noirs si `World`/nodes absents.
- Textures incorrectes via sockets Principled indexés.
- Fuites mémoire cumulées lors de longs rendus.
- Arguments CLI mal interprétés (gaze/rendu incohérents).
- Duplications d’images en mémoire.

7️⃣ Bonnes pratiques Blender 3.5 intégrées
- API data privilégiée pour contraintes et modifiers.
- Guards explicites sur l’existence d’objets/nodes.
- Fonctions utilitaires (`_ensure_world_nodes`, `_load_image`, `_try_keentools_op`).
- Parsing CLI robuste et typé.
- Code plus maintenable et prévisible en mode `--background`.

8️⃣ Checklist de validation finale
- Blender 3.5.x installé.
- Lancement CLI testé:
  - `blender --background model_v1/Model_Normal.blend --python Launch.py -- <head_texture> <camera_mode> <directory_name> <light_power> <gaze_yaw_range> <gaze_pitch_range> <images_nb> <head_fixed> <clothes_choice> <hat_choice> <mask_choice> <hair_choice> <run_id>`
- Rendu OK (au moins 2–3 frames).
- UI Tkinter OK (`python synthetic_face_ui.py`).
- CSV + metadata générés.
- Aucun warning critique dans la console (hors logs KeenTools).

9️⃣ Conclusion
- Le projet est désormais compatible Blender 3.5.x avec stabilité accrue en batch.
- Structure robuste pour migration future vers 3.6 LTS et 4.x (sockets nommés, guards, parsing CLI).
- Recommandations long terme: centraliser helpers (`import_obj`, `ensure_world_nodes`), ajouter un test minimal de rendu sur 1–2 frames.
