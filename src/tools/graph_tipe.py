from typing import Literal,List,Tuple
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

Sig=Literal[1,-1]
Noeud=Tuple[int,Literal[1,-1]]
Tresse=List[Noeud]


def differentes_couleurs(n):
    """Génère n couleurs distinctes en utilisant l'espace HSV/TSV.
    Les teintes sont réparties uniformément, avec saturation et valeur élevées.
    Retourne une liste de triplets RGB."""
    tsv_couleurs = []
    for i in range(n):
        teinte = i / n
        saturation = 0.9
        valeur = 0.9
        tsv_couleurs.append((teinte, saturation, valeur))
    return [mcolors.hsv_to_rgb(tsv) for tsv in tsv_couleurs]

def decomposition(T):
    """Décompose une liste de tuples (a, b) en deux listes distinctes : [a1, a2, ...], [b1, b2, ...]
    Équivaut à la fonction zip(*L)"""
    return [a for a, _ in T], [b for _, b in T]

def index(L, val):
    """Renvoie l'indice de la première occurrence de val dans la liste L.
    Équivaut à L.index(val)"""
    for i in range(len(L)):
        if L[i] == val:
            return i

def nbr_brins(t: list) -> int:
    """Nombre de brins utiles de la tresse"""
    return max(list(t[i][0] for i in range(len(t)))) + 1

def trajectoires_croisements(L):
    """renvoie la liste des trajectoires associées aux croisement et la hauteur"""
    nb_brins = nbr_brins(L)
    ordre_brins = list(range(nb_brins))
    trajectoires = [[(pos, 0, False)] for pos in range(nb_brins)]
    y = 0
    if L==[]:
        for pos, brin in enumerate(ordre_brins):
            trajectoires[brin].append((pos, 1, False))
        return trajectoires, 1

    for croisement, signe in L:
        n_ordre = ordre_brins.copy()
        n_ordre[croisement - 1], n_ordre[croisement] = n_ordre[croisement], n_ordre[croisement - 1]
        brin_g = ordre_brins[croisement - 1]
        brin_d = ordre_brins[croisement]
        brin_dessous = brin_g if signe == 1 else brin_d
        for brin in ordre_brins:
            n_pos = n_ordre.index(brin)
            est_croisement = (brin == brin_dessous)
            trajectoires[brin][-1] = (trajectoires[brin][-1][0], trajectoires[brin][-1][1], est_croisement)
            trajectoires[brin].append((n_pos, y + 1, False))
        ordre_brins = n_ordre
        y += 1
    for pos, brin in enumerate(ordre_brins):
        trajectoires[brin].append((pos, y, False))
    return trajectoires, y

def affichage_tresse(trajectoires, couleurs, L):
    """afficher les tresses avec matplotlib"""
    nb_brins = len(trajectoires)
    _,y = trajectoires_croisements(L)

    fig, ax = plt.subplots(figsize=(max(5, nb_brins), y), facecolor='white')

    for brin in range(nb_brins):
        points = trajectoires[brin]
        x_p, y_p = decomposition([(x, y) for x, y, _ in points])

        for j in range(len(x_p) - 1):
            x0, x1 = x_p[j], x_p[j+1]
            y0, y1 = y_p[j], y_p[j+1]
            est_dessous = points[j][2]

            if est_dessous:
                frac = 0.1
                dx, dy = x1 - x0, y1 - y0
                x_a = x0 + dx * (0.5 - frac)
                y_a = y0 + dy * (0.5 - frac)
                x_b = x0 + dx * (0.5 + frac)
                y_b = y0 + dy * (0.5 + frac)
                ax.plot([x0, x_a], [y0, y_a], color=couleurs[brin], linewidth=2, zorder=1)
                ax.plot([x_b, x1], [y_b, y1], color=couleurs[brin], linewidth=2, zorder=1)
            else:
                ax.plot([x0, x1], [y0, y1], color=couleurs[brin], linewidth=2, zorder=2)

    sigma_labels = [fr'$\sigma_{{{i}}}^{{{s}}}$' for i, s in L]
    for label in sigma_labels:
        ax.plot([], [], label=label)

    ax.legend(loc='center left', bbox_to_anchor=(-0.02, 0.47), fontsize=14,
              frameon=False, handlelength=0, handletextpad=0, labelspacing=1.5)
    ax.set_xlim(-0.5, nb_brins - 0.5)
    ax.set_ylim(y, -0.8)
    for pos in range(nb_brins):
        ax.text(pos, -0.4, str(pos + 1), ha='center', va='bottom', fontsize=12)
    ax.text((nb_brins - 1) / 2, -1.4, f"Tresse à {nb_brins} brins", ha='center', va='top', fontsize=14)
    ax.axis('off')
    plt.show()

def tresses_n_brins(L: Tresse):
    """affiche la tresse"""
    couleurs = differentes_couleurs(nbr_brins(L))
    trajectoires,_ = trajectoires_croisements(L)
    affichage_tresse(trajectoires, couleurs, L)
