import random
import time
import hashlib
from django.core.mail import send_mail 
import re
import unicodedata


def nettoyer_caracteres_speciaux(texte: str, mode: str = "remplacer") -> str:
    """
    Nettoie une chaîne de caractères pour éviter les problèmes d'insertion en base
    
    Modes disponibles:
    - "supprimer"    → enlève tout ce qui n'est pas alphanumérique + espaces
    - "remplacer"    → remplace accents et caractères spéciaux par leur version ASCII proche
    - "minimal"      → garde accents mais enlève caractères très exotiques / contrôles
    """
    if not texte:
        return ""

    # Étape 1 : normalisation Unicode (très important pour les accents)
    texte = unicodedata.normalize('NFD', texte)

    if mode == "supprimer":
        # Ne garde que lettres, chiffres, espaces et tirets
        texte = re.sub(r'[^a-zA-Z0-9\s-]', '', texte)
    
    elif mode == "remplacer":
        # Remplace les accents par leur lettre de base (é → e, ç → c, ñ → n, etc.)
        texte = ''.join(
            c for c in texte
            if unicodedata.category(c) != 'Mn'  # enlève les diacritiques
        )
        # Optionnel : remplacer quelques caractères spéciaux courants
        remplacements = {
            'æ': 'ae', 'œ': 'oe', 'ß': 'ss',
            'ø': 'o', 'å': 'a', 'ł': 'l',
            'đ': 'd', 'ħ': 'h', 'ŧ': 't',
        }
        for ancien, nouveau in remplacements.items():
            texte = texte.replace(ancien, nouveau)
    
    elif mode == "minimal":
        # Garde les accents mais supprime les caractères de contrôle et très exotiques
        texte = re.sub(r'[\x00-\x1F\x7F-\x9F]', '', texte)  # contrôle
        texte = re.sub(r'[^\w\sÀ-ž\-\'’]', '', texte)       # garde lettres latines étendues

    # Nettoyage final : espaces multiples → un seul
    texte = re.sub(r'\s+', ' ', texte).strip()

    return texte

def send_email(subject, message, recipient_list):
    send_mail(
        subject,
        message,
        'mfrelyon@gmail.com',
        recipient_list,
        fail_silently=False,
    )
    try:
        send_mail(
            subject=subject,
            message=message, 
            from_email="service@richbook.net",
            recipient_list=recipient_list, 
            fail_silently=False,
        )
        return True
    except Exception as e:
        # Optionnel : logger l'erreur
        print(f"Erreur envoi email : {e}")
       
        raise
        # return False


def generate_code(string):
    return "".join( random.sample(string,len(string)) )+str(int(time.time()));
    
def compute_duration(start, end):
    start = start.split(":")
    start = (int(start[0])* 3600 ) + (int(start[1]) * 60 ) + int(start[2])
    end = end.split(":")
    end = (int(end[0]) * 3600 ) + (int(end[1]) * 60 ) + int(end[2])
    
    return int( end - start );

def compute_sha1(string):
    return hashlib.sha256(bytes(string,"utf-8")).hexdigest()
  