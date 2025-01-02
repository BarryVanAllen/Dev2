from classes.Character import Character
from classes.Player import Player
from classes.NPC import NPC
from classes.Item import Item
import classes.Location
import classes.TextLibrary

visited_places = {
    "salle_buffet": False,
    "cuisine": False,
    "bibli": False,
    "couloir": False,
    "cave": False,
    "couloirCaverne": False
}


def NaratorFunc(input_text, **kwargs):
    """
    Process input text and return the corresponding narrative or action response.

    Args:
        input_text (str): The input command or text from the user.
        kwargs: Additional parameters for dynamic text generation.

    Returns:
        str: The narrative text or error message based on input_text.
    """
    narratives = {
        "hello": "Hello There",
        "intro": (
            "Bienvenue dans le Jeu d'Aventure !"
            "Vous êtes un aventurier audacieux, qui s'est aventuré dans un vieux château abandonné en pleine forêt."
            "Le château a été laissé à l'abandon depuis des siècles, et des rumeurs parlent de trésors cachés et de secrets oubliés."
            "Alors que vous explorez le château, vous vous retrouvez perdu dans ses couloirs sombres et labyrinthiques. "
            "Test"
        ),
        "name_prompt": "Entrez votre nom : ",
        "good_luck": "Bonne chance, {name}. Vous allez en avoir besoin.",
        "blocked_entrance": "L'entrée du château est bloquée, il faut trouver un autre moyen de sortir !",
        "salle_buffet": (
            "Vous entrez dans une salle opulente, ornée de lustres étincelants et de longues tables chargées de vaisselle dorée.\n"
            "Chaque coin de la pièce semble suinter la richesse, mais un étrange silence règne, presque oppressant."
        ),
        "retourne_buffet" : "\nVous quittez la cuisine et retournez dans la salle du buffet.",
        "found_potion": (
            "Votre regard est attiré par une fiole posée négligemment sur une table.\n"
            "Un liquide rouge y tourbillonne mystérieusement. Vous avez trouvé une potion de vie ! Elle pourrait vous être utile plus tard."
        ),
        "action_options": "Que voulez-vous faire ? Options: {options}",
        "invalid_input": "Veuillez entrer une option valide.",
        "combat_start": (
            "Une tension palpable emplit l'air. {enemy_name} se dresse devant vous, prêt à en découdre.\n"
            "{enemy_name}: {enemy_health} PV | Vous: {player_health} PV\n"
            "Que le combat commence !"
        ),
        "combat_victory": "Vous avez vaincu {enemy_name} ! Son corps s'effondre dans un bruit sourd.",
        "combat_defeat": "Vous avez été vaincu par {enemy_name}. L'obscurité vous enveloppe...",
        "inventory_empty": "Votre inventaire est vide. Peut-être devriez-vous explorer davantage...",
        "inventory_items": "Vous ouvrez votre sac et inspectez vos possessions :\n{items}",
        "regarder_inventaire_valide" : "Vous ouvrez votre sac et inspectez vos possessions :",
        "regarder_inventaire_invalide" : "Votre inventaire est vide. Peut-être devriez-vous explorer davantage...",
        "visited_cuisine" : "Vous retournez dans la cuisine. Elle est désormais silencieuse et vide. \nLe sol est encore marqué par les traces du combat précédent.",
        "scène_cuisine": (
            "Vous poussez une porte grinçante et entrez dans ce qui semble être une cuisine."
            "L'odeur de nourriture rance flotte dans l'air, mélangée à celle de bois brûlé."
            "Des étagères croulent sous des ustensiles rouillés, et un chaudron abandonné repose au centre."
            "Alors que vous vous avancez prudemment, une ombre furtive surgit !"
            "Un gobelin malingre, armé d'un couteau de cuisine rouillé, vous bloque le passage."
            "Le gobelin montre les crocs et crie : 'Personne ne vole MES provisions !'"
        ),
        "combat_victory_cuisine": "Après un combat acharné, le gobelin s'effondre en grognant. Le calme revient dans la pièce.\nVous explorez rapidement la cuisine et trouvez des provisions et un couteau de cuisine.\nVous ajoutez les provisions et le couteau à votre inventaire.",
        "scène_couloir" : (
            "Vous entrez dans un couloir sombre et lugubre. Les murs sont ornés de portraits anciens, mais quelque chose cloche."
            "Les tableaux sont mal alignés et un étrange frisson parcourt votre échine."
            "Alors que vous avancez prudemment, vous remarquez un vieux livre posé à terre. La couverture semble usée, mais le titre est encore lisible : *'L'Ordre des Âges'.*"
            "Vous ramassez le livre et l'ouvrez. Une phrase attire votre attention :"
            "\"Dans le grand cycle, l'enfant vient avant le guerrier, mais après le vieillard. Le roi se tient toujours entre eux.\""
            "En levant les yeux, vous remarquez que les tableaux représentent :"
            "1. Un enfant avec un jouet"
            "2. Un roi en pleine gloire"
            "3. Un vieillard tenant une canne"
            "4. Un guerrier avec une épée"
        ),
        "scène_couloir_visited" : "Juste le couloir vide ou vous avez résolu les énigmes",
        "question_tableau" : "Voulez-vous regarder de plus près les tableaux? (oui/non) > ",
        "tableau_sensation" : "Vous sentez que réaligner les tableaux dans le bon ordre pourrait révéler quelque chose de caché.",
        "demande_enigme" : "Voulez-vous regarder de plus près les tableaux? (oui/non) > ",
        "enigme_non" : (
            "Vous décidez de ne pas résoudre l'énigme pour le moment."
            "Vous continuez à avancer dans le couloir, en ignorant les tableaux mal alignés."
            "Vous sentez une légère brise venant d'un autre passage. Vous décidez de vous y diriger."
        ),
        "equip_item" : "Quel objet voulez-vous équiper ?",
        "item_equiper" : "{item.name} est maintenant équipé !",
        "combat1" : "\nUne tension palpable emplit l'air. {enemy.name} se dresse devant vous, prêt à en découdre.",
        "combat2" : "\n{enemy.name}: {enemy.health} PV | Vous: {player.health} PV",
        "combat_commence" : "\nQue le combat commence !",
        "attaque_joueur" : "\nVous préparez votre attaque...",
        "ennemie_vaincu" : "\nVous avez vaincu {enemy.name} ! Son corps s'effondre dans un bruit sourd.",
        "contre_attaque" : "\n{enemy.name} riposte avec rage !",
        "etat_des_perso" : "\nVotre état : {player}\n{enemy}",
        "action_fuirouContinuer" : "\nQue voulez-vous faire ? (continuer/fuir) ",
        "fuir" : "\nVous tournez les talons et fuyez, le cœur battant.",
        "desequiper" : "Vous réfléchissez à déséquiper un objet, mais rien ne semble pertinent pour l'instant.",
        "utiliser" : "Vous vous demandez quel objet pourrait être utile...",
        "quitter" : "Vous refermez votre sac et vous préparez à continuer l'aventure.",
        "battre_retraite" : "\nVous battez en retraite, laissant la cuisine derrière vous.",
        "tableau_etat" : "\nVoici les tableaux dans leur état actuel :",
        "tableau_realigner" : "\nDans quel ordre voulez-vous réaligner les tableaux ? (Entrez les numéros séparés par des espaces, ex: '3 1 4 2')",
        "valueError" : "Veuillez entrer uniquement des chiffres.",
        "solution_enigme1" : "\nVous réalignez les tableaux dans le bon ordre. Un clic mécanique résonne, et une partie du mur coulisse lentement pour révéler un coffre secret.",
        "solution_enigme2" : "Vous avez résolu l'énigme en {tentatives} tentatives !",
        "coffre_epee" : "Vous ouvrez le coffre et découvrez une épée!",
        "tableau_rater" : "\nVous n'avez pas aligné tous les tableaux.",
        "ordre_incorrect" : "\nL'ordre semble incorrect. Les tableaux restent désalignés.",
        "tentative_5" : "\nVous commencez à vous demander si vous n'avez pas manqué un indice quelque part.",
        "avance_prudament" : "\nVous avancez prudemment dans le couloir...",
        "bibli" : (
            "\nVous poussez lentement la porte en bois massive de la bibliothèque. L'air à l'intérieur est lourd et poussiéreux."
            "Des rayonnages immenses s'étendent à perte de vue, remplis de livres anciens, certains à peine lisibles à cause de l'usure du temps."
            "L'odeur du vieux papier et du bois vieilli emplit vos narines. La pièce semble abandonnée depuis des siècles."
            "\nSoudain, un frisson vous parcourt l'échine. Vous apercevez une silhouette translucide, presque éthérée, flottant devant une étagère."
            "C'est un fantôme, un esprit qui semble perdu dans le temps. Il vous regarde, comme s'il vous attendait."
            "\nLe fantôme se tourne vers vous et, d'une voix grave mais douce, il commence à parler :"
            "\"Je suis l'âme du dernier propriétaire de ce château, un érudit obsédé par la connaissance. Jadis, je suis mort ici, seul et oublié, pris au piège des ombres de ce lieu maudit.\""
            "Le fantôme s'approche lentement, ses traits se précisant, et vous pouvez presque voir des larmes briller dans ses yeux."
            "\"Je suis resté prisonnier de ces murs, piégé par mes erreurs. Ne fais pas la même chose, aventurier. Ne meurs pas ici comme moi. Ce château te réclame, mais il est aussi une prison.\""
            "Il semble profondément triste, mais continue :"
            "\"Il y a une issue, mais elle est bien cachée. Prends le chemin à droite, et lorsque tu arriveras au portrait du roi, tourne à droite. Suis ce chemin avec prudence, car des pièges se cachent dans l'ombre.\""
            "\"Va, vite, et échappe à ce destin funeste. Le temps est compté.\""
            "\nLe fantôme disparaît lentement dans un éclat de lumière pâle, laissant derrière lui un silence lourd."
            "Vous sentez que l'atmosphère de la bibliothèque a changé, mais un lourd pressentiment demeure."
        ),
        "bibli_sans_fantome" : "La bibliothèque semble si calme sans le fantôme",
        "cave_visite" : (
                        "vous pouvez voir le trou géant qui vous a emmené dans la grotte"
                        "voulez-vous aller dans la grotte"
        ),
        "cave" : (
            "Vous entrez dans une cave sombre et mystérieuse. Devant vous se dresse une statue imposante d'un sphinx."
            "Son regard perçant semble suivre chacun de vos mouvements."
            "\nSoudain, une voix grave résonne dans l'air :"
            '"Où allez-vous en cette heure si tardive ?"\n'
            "Vous ne voyez pas d'où provient la voix, mais elle dégage une telle autorité que vous en tremblez."
            '"Si vous souhaitez avancer, vous devez répondre à mes trois énigmes."\n'
        ),
        "reponse_ok_sphinx" : (
            "\nBonne réponse !"
            enigme["effet"]
        ),
        "reponse_mauvaise_sphinx" : (
            "\nMauvaise réponse..."
            "La statue reste immobile, mais vous sentez la tension monter dans l'air."
            "Vous devez retenter votre chance pour continuer."
        ),
        "effet_cave" : (
            "\nVotre réponse semble déclencher quelque chose d'irréversible. Les murs tremblent, puis s’effondrent brusquement. "
            "\nUne masse d’eau vive jaillit des décombres et vous emporte avec une force inouïe. Incapable de lutter, vous êtes propulsé dans une grotte sombre et profonde. "
            "\nLes remous violents vous poussent contre les parois rocheuses, et vous vous retrouvez haletant sur une plage de sable noir, à l'intérieur de cette mystérieuse caverne."
            "\nUn seul chemins s'offrent à vous :"
            "Un passage éclairé par une faible lumière."
        ),
        "couloirCaverne_visite" : (
            "vous arpenter les couloirs sombres de la caverne, celle-ci à l'air bien calme sans l'immense araignée "
            "\nVous avancez dans les couloirs sombres de la grotte. L'air est lourd, et une odeur nauséabonde vous prend à la gorge."
            "Soudain, un bruit inquiétant résonne. Vous levez les yeux et apercevez une énorme araignée suspendue au plafond."
            "Elle descend lentement sur sa toile, ses yeux multiples brillant dans l'obscurité."
            "\nC'est un combat à mort ! Préparez-vous !\n"
        ),
        "combat_araigne_gagne" : (
            "Après un combat long et éprouvant, vous parvenez finalement à terrasser la bête monstrueuse. L'araignée géante s'effondre dans un dernier spasme, ses immenses pattes se repliant sur elles-mêmes."
            "Vous respirez profondément, le cœur battant à tout rompre, et une pensée ironique traverse votre esprit :"
            "\"Elle ne semble plus si redoutable maintenant qu'elle est morte.\""
            "\nMais alors que vous vous détendez un instant, une vision terrifiante vous glace le sang."
            "Le corps de l'araignée commence à se décomposer à une vitesse anormale. Sa carapace se fissure, et soudain, elle explose en une myriade de petites araignées grouillantes."
            "Les créatures minuscules se déversent en une vague noire et chaotique, envahissant le sol autour de vous. Elles se dispersent dans toutes les directions, disparaissant dans les ombres."
            "\nAu centre de ce chaos grouillant, quelque chose brille faiblement dans l'obscurité."
            "En vous approchant avec précaution, vous découvrez une clé étrange posée sur le sol, là où la bête avait rendu son dernier souffle."
            "La clé est froide au toucher, ornée de motifs arachnéens gravés dans le métal noirci. Elle semble presque vivante, pulsant légèrement comme si elle portait encore un fragment de l'araignée."
            "\nVous savez que cet objet a une importance cruciale, mais une part de vous ne peut s’empêcher de frissonner en la tenant dans vos mains."
        ),


    }


    # Handle dynamic input
    input_text = input_text.strip().lower()

    if input_text in narratives:
        # Retrieve predefined narrative
        text = narratives[input_text]
    else:
        # Handle unknown inputs
        text = "Commande inconnue. Veuillez essayer une autre commande."

    # Format the text if there are additional keyword arguments
    if kwargs:
        text = text.format(**kwargs)

    return text


# Example utility function to handle inventory formatting
def format_inventory(items):
    if not items:
        return NaratorFunc("inventory_empty")
    formatted_items = "\n".join(f"- {item}" for item in items)
    return NaratorFunc("inventory_items", items=formatted_items)
