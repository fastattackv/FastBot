import random
import os
import discord
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv
import pickle
from datetime import date

load_dotenv(dotenv_path="config")

default_intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=default_intents)

# load variables pickle
with open("save channels jeu bot", "rb") as f:
    dico_serv_jeu = pickle.load(f)
with open("save channels arrivées", "rb") as g:
    dico_serv_arrivees = pickle.load(g)
with open("classement devine", "rb") as h:
    dico_classement = pickle.load(h)
with open("save channels règles", "rb") as j:
    dico_serv_regles = pickle.load(j)
with open("save channels discu", "rb") as k:
    dico_serv_discu = pickle.load(k)
with open("save channels admin", "rb") as l:
    dico_serv_admin = pickle.load(l)
with open("monnaie FastBot", "rb") as m:
    dico_monnaie = pickle.load(m)
with open("save roles vip", "rb") as w:
    dico_role_vip = pickle.load(w)


var_jeu = False
joueur1 = False
var_annul_argent = False
var_annul_classement = False
annul_a = None
annul_c = None
# variables de batons
var_batons = False
var_j2_batons = True
var_batons_j1 = False
var_batons_j2 = False
nombre_batons = 24
joueur1_batons = False
joueur2_batons = False
id_joueur1_batons = False
id_joueur2_batons = False
# variables de devine
joueur1_devine = False
joueur2_devine = False
id_joueur1_devine = False
id_joueur2_devine = False
var_devine = False
var_devine_j1 = False
var_devine_j2 = False
nombre_a_d = 1
points = 0
liste_points = []


@bot.event
async def on_ready():
    print("Le bot est connecté.")


@bot.event
async def on_member_join(membre):
    channel_join = bot.get_channel(dico_serv_arrivees[str(membre.guild)])
    message_accueil_embed = discord.Embed(title="Nouveau membre !", description=f"Bienvenue à <@{membre.id}> !", color=0x0000ff)
    message_accueil_embed.add_field(name="N'oublie pas d'aller lire les règles", value=f"<#{dico_serv_regles[str(membre.guild)]}>", inline=False)
    message_accueil_embed.add_field(name="Commence par dire bonjour", value=f"<#{dico_serv_discu[str(membre.guild)]}>", inline=False)
    await channel_join.send(embed=message_accueil_embed)


@bot.event
async def on_guild_update(serveur_av, serveur_ap):
    if serveur_av.name != serveur_ap.name:
        if str(serveur_av) in dico_serv_jeu:
            dico_serv_jeu[str(serveur_ap)] = dico_serv_jeu.pop(str(serveur_av))
            with open("save channels jeu bot", "wb") as f:
                pickle.dump(dico_serv_jeu, f)
        if str(serveur_av) in dico_serv_arrivees:
            dico_serv_arrivees[str(serveur_ap)] = dico_serv_arrivees.pop(str(serveur_av))
            with open("save channels arrivées", "wb") as g:
                pickle.dump(dico_serv_arrivees, g)
        if str(serveur_av) in dico_serv_regles:
            dico_serv_regles[str(serveur_ap)] = dico_serv_regles.pop(str(serveur_av))
            with open("save channels règles", "wb") as j:
                pickle.dump(dico_serv_regles, j)
        if str(serveur_av) in dico_serv_discu:
            dico_serv_discu[str(serveur_ap)] = dico_serv_discu.pop(str(serveur_av))
            with open("save channels discu", "wb") as k:
                pickle.dump(dico_serv_discu, k)
        if str(serveur_av) in dico_role_vip:
            dico_role_vip[str(serveur_ap)] = dico_role_vip.pop(str(serveur_av))
            with open("save roles vip", "wb") as w:
                pickle.dump(dico_role_vip, w)
        if str(serveur_av) in dico_serv_admin:
            dico_serv_admin[str(serveur_ap)] = dico_serv_admin.pop(str(serveur_av))
            with open("save channels admin", "wb") as l:
                pickle.dump(dico_serv_admin, l)
            channel_admin: discord.TextChannel = bot.get_channel(int(dico_serv_admin[str(serveur_ap)]))
            await channel_admin.send("le nouveau nom du serveur a été pris en compte par FastBot")
    print(f"    Changement de nom du serveur {serveur_av} en {serveur_ap}")


@bot.event
async def on_guild_remove(serveur_r):
    if serveur_r in dico_serv_jeu:
        del dico_serv_jeu[str(serveur_r)]
        with open("save channels jeu bot", "wb") as f:
            pickle.dump(dico_serv_jeu, f)
    if serveur_r in dico_serv_arrivees:
        del dico_serv_arrivees[str(serveur_r)]
        with open("save channels arrivées", "wb") as g:
            pickle.dump(dico_serv_arrivees, g)
    if serveur_r in dico_serv_regles:
        del dico_serv_regles[str(serveur_r)]
        with open("save channels règles", "wb") as j:
            pickle.dump(dico_serv_regles, j)
    if serveur_r in dico_serv_discu:
        del dico_serv_discu[str(serveur_r)]
        with open("save channels discu", "wb") as k:
            pickle.dump(dico_serv_discu, k)
    if serveur_r in dico_serv_admin:
        del dico_serv_admin[str(serveur_r)]
        with open("save channels admin", "wb") as l:
            pickle.dump(dico_serv_admin, l)
    if serveur_r in dico_role_vip:
        del dico_role_vip[str(serveur_r)]
        with open("save roles vip", "wb") as w:
            pickle.dump(dico_role_vip, w)
    print(f"    Serveur {serveur_r} retiré de FastBot")


@bot.event
async def on_guild_role_delete(role_s):
    if role_s in dico_role_vip:
        del dico_role_vip[str(role_s)]
        with open("save roles vip", "wb") as w:
            pickle.dump(dico_role_vip, w)


@bot.event
async def on_message(message):
    global var_jeu, joueur1, var_annul_argent, var_annul_classement, annul_a, annul_c
    global var_batons,var_j2_batons, var_batons_j1, var_batons_j2, joueur1_batons, joueur2_batons, id_joueur1_batons, id_joueur2_batons, nombre_batons
    global joueur1_devine, joueur2_devine, id_joueur1_devine, id_joueur2_devine, var_devine, var_devine_j1, var_devine_j2, nombre_a_d, points, liste_points
    global dico_classement
    global dico_role_vip
    channel_jeu = 0
    if str(message.guild) in dico_serv_jeu:
        channel_jeu = dico_serv_jeu[str(message.guild)]
    if message.author.name == "FastBot":
        pass
    else:
        print(message.author)
        print(f"{message.guild}, {message.channel}")
        print(message.content)
    if message.content.lower() == "ping" and str(message.channel) == channel_jeu:
        await message.channel.send("pong")
    elif str(message.channel.id) == channel_jeu and message.content.lower() == "je veux jouer" and var_devine == False:
        joueur1 = message.author
        var_jeu = True
        await message.channel.send("à quoi ?")
    elif var_jeu and str(message.channel.id) == channel_jeu and message.author == joueur1:
        if message.content.lower() == "à devine":
            joueur1_devine = message.author
            id_joueur1_devine = message.author.id
            joueur1 = False
            await message.channel.send(f"qui joue à devine avec <@{id_joueur1_devine}> ?")
            var_jeu = False
            var_devine = True
        elif message.content.lower() == "aux batons":
            joueur1_batons = message.author
            id_joueur1_batons = message.author.id
            joueur1 = False
            await message.channel.send(f"qui joue aux bâtons avec <@{id_joueur1_batons}> ?")
            var_jeu = False
            var_batons = True
    # batons
    if var_batons and str(message.channel.id) == channel_jeu:
        nombre_e = int(message.content)
        aff = ""
        if message.content.lower() == "moi" and var_j2_batons:
            joueur2_batons = message.author
            id_joueur2_batons = message.author.id
            var_j2_batons = False
            if joueur1_batons == joueur2_batons:
                await message.channel.send("Tricheur !")
                await message.channel.send("On ne joue pas avec soi-même")
                joueur1_batons = False
                id_joueur1_batons = False
                joueur2_batons = False
                id_joueur2_batons = False
                var_batons = False
                var_j2_batons = True
            else:
                await bot.change_presence(activity=discord.Activity(type=0, name=f"bâtons avec {joueur1_batons} et {joueur2_batons}"))
                await message.channel.send(". :french_bread: :french_bread: :french_bread: :french_bread: :french_bread: :french_bread: :french_bread: :french_bread: :french_bread: :french_bread: :french_bread: :french_bread: :french_bread: :french_bread: :french_bread: :french_bread: :french_bread: :french_bread: :french_bread: :french_bread: :french_bread: :french_bread: :french_bread: :french_bread:")
                await message.channel.send(f"<@{id_joueur1_batons}> prends entre 1 et 3 bâtons")
                var_batons_j1 = True
        else:
            if nombre_e <= 1 and nombre_e >= 3:
                nombre_batons -= nombre_e
                for x in range(nombre_batons):
                    aff += " :french_bread:"
                await message.channel.send(f". {aff}")
                aff = ""

    # devine
    if var_devine and str(message.channel.id) == channel_jeu and message.content.lower() == "moi":
        joueur2_devine = message.author
        id_joueur2_devine = message.author.id
        if str(joueur1_devine) not in dico_classement:
            dico_classement[str(joueur1)] = 0
            print(f"    ajout de {joueur1_devine} dans dico_classement")
            with open("classement devine", "wb") as h:
                pickle.dump(dico_classement, h)
        elif str(joueur2_devine) not in dico_classement:
            dico_classement[str(joueur2_devine)] = 0
            print(f"    ajout de {joueur2_devine} dans dico_classement")
            with open("classement devine", "wb") as h:
                pickle.dump(dico_classement, h)
        if joueur1_devine == joueur2_devine:
            await message.channel.send("Tricheur !")
            await message.channel.send("On ne joue pas avec soi-même")
            joueur1_devine = False
            joueur2_devine = False
            id_joueur1_devine = False
            id_joueur2_devine = False
            var_devine = False
            var_devine_j1 = False
            var_devine_j2 = False
        else:
            await bot.change_presence(activity=discord.Activity(type=0, name=f"devine avec {joueur1_devine} et {joueur2_devine}"))
            await message.channel.send(f"<@{id_joueur1_devine}> devine (le nombre entre 1 et 99)")
            var_devine_j1 = True
            nombre_a_d = random.randint(1, 99)
    if var_devine and str(message.channel.id) == channel_jeu:
        if var_devine_j1 and message.author == joueur1_devine:
            nombre_d = int(message.content)
            if nombre_d == nombre_a_d:
                await message.channel.send("bonne réponse")
                points += 1
                liste_points.append(points)
                await message.channel.send(f"<@{id_joueur2_devine}> devine (le nombre entre 1 et 99)")
                var_devine_j1 = False
                var_devine_j2 = True
                nombre_a_d = random.randint(1, 99)
                points = 0
            elif nombre_d < nombre_a_d:
                await message.channel.send("plus")
                points += 1
            elif nombre_d > nombre_a_d:
                await message.channel.send("moins")
                points += 1
        elif var_devine_j2 and message.author == joueur2_devine:
            nombre_d = int(message.content)
            if nombre_d == nombre_a_d:
                await message.channel.send("bonne réponse")
                points += 1
                liste_points.append(points)
                await message.channel.send(f"<@{id_joueur1_devine}> a trouvé en {liste_points[0]}")
                await message.channel.send(f"<@{id_joueur2_devine}> a trouvé en {liste_points[1]}")
                monnaie_gagnee = 0
                if id_joueur1_devine not in dico_monnaie:
                    dico_monnaie[str(id_joueur1_devine)] = ["0", 0]
                if id_joueur2_devine not in dico_monnaie:
                    dico_monnaie[str(id_joueur2_devine)] = ["0", 0]
                if liste_points[0] > liste_points[1]:
                    gagnant = id_joueur2_devine
                    dico_classement[str(joueur2_devine)] = dico_classement[str(joueur2_devine)] + 1
                    monnaie_gagnee = random.randint(25, 50)
                    infos_auteur = dico_monnaie[str(id_joueur2_devine)]
                    dico_monnaie[str(joueur2_devine)] = [infos_auteur[0], infos_auteur[1]+monnaie_gagnee]
                    await message.channel.send(f"le gagnant est <@{gagnant}>")
                    await message.channel.send(f"<@{id_joueur2_devine}> a gagné {monnaie_gagnee} pièces")
                elif liste_points[0] < liste_points[1]:
                    gagnant = id_joueur1_devine
                    dico_classement[str(joueur1_devine)] = dico_classement[str(joueur1_devine)] + 1
                    monnaie_gagnee = random.randint(25, 50)
                    infos_auteur = dico_monnaie[str(id_joueur1_devine)]
                    dico_monnaie[str(joueur1_devine)] = [infos_auteur[0], infos_auteur[1]+monnaie_gagnee]
                    await message.channel.send(f"le gagnant est <@{gagnant}>")
                    await message.channel.send(f"<@{id_joueur1_devine}> a gagné {monnaie_gagnee} pièces")
                elif liste_points[0] == liste_points[1]:
                    await message.channel.send("il y a égalité")
                    monnaie_gagnee = random.randint(10, 20)
                    infos_auteur = dico_monnaie[str(id_joueur1_devine)]
                    dico_monnaie[str(id_joueur1_devine)] = [infos_auteur[0], infos_auteur[1]+monnaie_gagnee]
                    infos_auteur = dico_monnaie[str(id_joueur2_devine)]
                    dico_monnaie[str(id_joueur2_devine)] = [infos_auteur[0], infos_auteur[1]+monnaie_gagnee]
                    await message.channel.send(f"<@{id_joueur1_devine}> et <@{id_joueur2_devine}> ont gagné {monnaie_gagnee} pièces")
                with open("monnaie FastBot", "wb") as m:
                    pickle.dump(dico_monnaie, m)
                var_devine_j2 = False
                var_devine = False
                joueur1_devine = False
                joueur2_devine = False
                points = 0
                liste_points = []
                await bot.change_presence(activity=discord.Activity(type=0, name=None))
                with open("classement devine", "wb") as h:
                    pickle.dump(dico_classement, h)
            elif nombre_d < nombre_a_d:
                await message.channel.send("plus")
                points += 1
            elif nombre_d > nombre_a_d:
                await message.channel.send("moins")
                points += 1
    # fin jeux
    if message.content == "<@1037734637285421197> quel est le classement ?" and str(message.channel.id) == channel_jeu:
        classement_sorted = sorted(dico_classement, key=dico_classement.get, reverse=True)
        premier = classement_sorted[0]
        deuxieme = classement_sorted[1]
        troisieme = classement_sorted[2]
        points_1 = dico_classement[str(premier)]
        points_2 = dico_classement[str(deuxieme)]
        points_3 = dico_classement[str(troisieme)]
        await message.channel.send("Le classement de devine est :")
        await message.channel.send(f"1er : {premier} avec {points_1} points")
        await message.channel.send(f"2eme : {deuxieme} avec {points_2} points")
        await message.channel.send(f"3eme : {troisieme} avec {points_3} points")
    # definitions des salons du bot
    elif message.content == "<@1037734637285421197> .channel.jeu":
        if message.author.guild_permissions.administrator:
            dico_serv_jeu[str(message.guild)] = str(message.channel.id)
            with open("save channels jeu bot", "wb") as f:
                pickle.dump(dico_serv_jeu, f)
            await message.channel.send(f"le salon de jeu est <#{dico_serv_jeu[str(message.guild)]}>")
        else:
            await message.channel.send("tu n'es pas admin")
    elif message.content == "<@1037734637285421197> .channel.arrivées":
        if message.author.guild_permissions.administrator:
            dico_serv_arrivees[str(message.guild)] = str(message.channel.id)
            with open("save channels arrivées", "wb") as g:
                pickle.dump(dico_serv_arrivees, g)
            await message.channel.send(f"le salon des arrivées est <#{dico_serv_arrivees[str(message.guild)]}>")
        else:
            await message.channel.send("tu n'es pas admin")
    elif message.content == "<@1037734637285421197> .channel.règles":
        if message.author.guild_permissions.administrator:
            dico_serv_regles[str(message.guild)] = str(message.channel.id)
            with open("save channels règles", "wb") as j:
                pickle.dump(dico_serv_regles, j)
            await message.channel.send(f"le salon des règles est <#{dico_serv_regles[str(message.guild)]}>")
        else:
            await message.channel.send("tu n'es pas admin")
    elif message.content == "<@1037734637285421197> .channel.discution":
        if message.author.guild_permissions.administrator:
            dico_serv_discu[str(message.guild)] = str(message.channel.id)
            with open("save channels discu", "wb") as k:
                pickle.dump(dico_serv_discu, k)
            await message.channel.send(f"le salon de discution est <#{dico_serv_discu[str(message.guild)]}>")
        else:
            await message.channel.send("tu n'es pas admin")
    elif message.content == "<@1037734637285421197> .channel.messages_FastBot":
        if message.author.guild_permissions.administrator:
            dico_serv_admin[str(message.guild)] = str(message.channel.id)
            with open("save channels admin", "wb") as l:
                pickle.dump(dico_serv_admin, l)
            await message.channel.send(f"le salon des messages pour les admins de FastBot est <#{dico_serv_admin[str(message.guild)]}>")
        else:
            await message.channel.send("tu n'es pas admin")
    elif message.content.startswith("<@1037734637285421197> .role_VIP"):
        mess_split = str(message.content.split()[2])
        mess_split = mess_split.replace("<", "")
        mess_split = mess_split.replace("@", "")
        mess_split = mess_split.replace("&", "")
        mess_split = mess_split.replace(">", "")
        dico_role_vip[str(message.guild)] = mess_split
        with open("save roles vip", "wb") as w:
            pickle.dump(dico_role_vip, w)
        await message.channel.send(f"Le rôle VIP de {message.guild} est <@&{dico_role_vip[str(message.guild)]}>")
    elif message.content == "<@1037734637285421197> .channels" and message.author.guild_permissions.administrator:
        serveur = str(message.guild)
        await message.channel.send("Les salons de <@1037734637285421197> de ce serveur sont :")
        if serveur in dico_serv_jeu:
            await message.channel.send(f"Jeu : <#{dico_serv_jeu[str(serveur)]}>")
        else:
            await message.channel.send("Jeu : Pas défini")
        if serveur in dico_serv_arrivees:
            await message.channel.send(f"Arrivées : <#{dico_serv_arrivees[str(serveur)]}>")
        else:
            await message.channel.send("Arrivées : Pas défini")
        if serveur in dico_serv_regles:
            await message.channel.send(f"Règles : <#{dico_serv_regles[str(serveur)]}>")
        else:
            await message.channel.send("Règles : Pas défini")
        if serveur in dico_serv_discu:
            await message.channel.send(f"Discution : <#{dico_serv_discu[str(serveur)]}>")
        else:
            await message.channel.send("Discution : Pas défini")
        if serveur in dico_serv_admin:
            await message.channel.send(f"Messages pour admins : <#{dico_serv_admin[str(serveur)]}>")
        else:
            await message.channel.send("Messages pour admins : Pas défini")
    elif message.content == "<@1037734637285421197> .roles":
        serveur = str(message.guild)
        if serveur in dico_role_vip:
            await message.channel.send(f"Role VIP : <@&{dico_role_vip[str(serveur)]}>")
        else:
            await message.channel.send("Role VIP : Pas défini")
    elif message.content == "<@1037734637285421197> .récompense" and str(message.channel.id) == channel_jeu:
        auteur = str(message.author.id)
        if str(auteur) not in dico_monnaie:
            dico_monnaie[str(message.author.id)] = ["0", 0]
        infos_auteur = dico_monnaie[str(auteur)]
        if str(date.today()) != infos_auteur[0]:
            pieces = 0
            nombre_1 = random.randint(1, 3)
            if nombre_1 == 1:
                pieces = random.randint(1, 40)
            elif nombre_1 == 2 or nombre_1 == 3:
                pieces = random.randint(41, 99)
            total_pieces = infos_auteur[1] + pieces
            if total_pieces > 10000:
                total_pieces = 10000
                await message.channel.send("Attention, ton porte monnaie est plein, si tu gagnes de nouvelles pièces, elles seront supprimées")
            dico_monnaie[str(auteur)] = [str(date.today()), int(total_pieces)]
            await message.channel.send(f"Tu as récupéré {pieces} pièces aujourd'hui, ton total est de {total_pieces} pièces")
            with open("monnaie FastBot", "wb") as m:
                pickle.dump(dico_monnaie, m)
        elif str(date.today()) == infos_auteur[0]:
            await message.channel.send("tu as déjà récupéré tes récompenses aujourd'hui")
    elif message.content == "<@1037734637285421197> .monnaie" and str(message.channel.id) == channel_jeu:
        if str(message.author.id) not in dico_monnaie:
            dico_monnaie[str(message.author.id)] = ["0", 0]
        infos_auteur = dico_monnaie[str(message.author.id)]
        await message.channel.send(f"<@{message.author.id}> possède {infos_auteur[1]} pièces")
    elif message.content == "<@1037734637285421197> .boutique" and str(message.channel.id) == channel_jeu:
        message_boutique_embed = discord.Embed(title="Boutique", description="Attention pas de remboursement", color=0x0000ff)
        message_boutique_embed.add_field(name="1_ Rôle VIP (permet d'accéder à des channels VIP)", value="Prix : 1000 pièces", inline=False)
        message_boutique_embed.add_field(name="2_", value="Prix : 2500 pièces", inline=False)
        await message.channel.send(embed=message_boutique_embed)
    elif message.content.startswith("<@1037734637285421197> .acheter") and str(message.channel.id) == channel_jeu:
        if str(message.author.id) not in dico_monnaie:
            dico_monnaie[str(message.author.id)] = ["0", 0]
        infos_auteur = dico_monnaie[str(message.author.id)]
        item = int(message.content.split()[2])
        role = get(message.guild.roles, id=int(dico_role_vip[str(message.guild)]))
        if item == 1:
            if str(message.guild) in dico_role_vip:
                if role in message.author.roles:
                    await message.channel.send(f"Tu as déjà le rôle <@&{dico_role_vip[str(message.guild)]}> de {message.guild}")
                elif infos_auteur[1] >= 1000:
                    dico_monnaie[str(message.author.id)] = [infos_auteur[0], infos_auteur[1]-1000]
                    await message.author.add_roles(role, atomic=True)
                    await message.channel.send(f"Le rôle <@&1059409263975469107> a été attribué à <@{message.author.id}>")
                    await message.channel.send(f"Il reste {infos_auteur}")
                    with open("monnaie FastBot", "wb") as m:
                        pickle.dump(dico_monnaie, m)
                elif infos_auteur[1] < 1000:
                    await message.channel.send(f"Tu n'as pas assez de pièces : {infos_auteur[1]} sur 1000")
            else:
                await message.channel.send(f"Le rôle VIP n'existe pas sur {message.guild}")
        elif item == 2:
            print("pas fait lol")
        elif item > 2:
            await message.channel.send(f"L'item numéro {item} n'existe pas")
    elif message.content.startswith("<@1037734637285421197> .reset_argent") and str(message.author) == "fastattack#7170":
        mess_split_a = str(message.content.split()[2])
        mess_split_a = mess_split_a.replace("<", "")
        mess_split_a = mess_split_a.replace("@", "")
        mess_split_a = mess_split_a.replace(">", "")
        if mess_split_a in dico_monnaie:
            infos_auteur = dico_monnaie[str(mess_split_a)]
            dico_monnaie[mess_split_a] = [str(date.today()), 0]
            await message.channel.send(f"l'argent de <@{mess_split_a}> a été remis à 0")
            var_annul_argent = True
            annul_a = [str(mess_split_a), infos_auteur[0], infos_auteur[1]]
            await message.channel.send("annulation disponible avec <@1037734637285421197> .annulation.argent")
            with open("monnaie FastBot", "wb") as m:
                pickle.dump(dico_monnaie, m)
        else:
            await message.channel.send("L'utilisateur n'a pas été trouvé")
    elif message.content.startswith("<@1037734637285421197> .reset_classement") and str(message.author) == "fastattack#7170":
        mess_split_c = str(message.content.split()[2])
        mess_split_c = mess_split_c.replace("<", "")
        mess_split_c = mess_split_c.replace("@", "")
        mess_split_c = mess_split_c.replace(">", "")
        nom = await bot.fetch_user(int(mess_split_c))
        nom = str(nom)
        if nom in dico_classement:
            annul_c = [str(nom), dico_classement[nom]]
            dico_classement[nom] = 0
            await message.channel.send(f"le classement de <@{mess_split_c}> a été remis à 0")
            var_annul_classement = True
            await message.channel.send("annulation disponible avec <@1037734637285421197> .annulation.classement")
            with open("classement devine", "wb") as h:
                pickle.dump(dico_classement, h)
        else:
            await message.channel.send("L'utilisateur n'a pas été trouvé")
    elif message.content == "<@1037734637285421197> .annulation.argent" and var_annul_argent and str(message.author) == "fastattack#7170":
        dico_monnaie[str(annul_a[0])] = [annul_a[1], annul_a[2]]
        with open("monnaie FastBot", "wb") as m:
            pickle.dump(dico_monnaie, m)
        await message.channel.send(f"le reset d'argent de <@{annul_a[0]}> a été annulé : il possède {annul_a[2]} pièces")
        var_annul_argent = False
        annul_a = None
    elif message.content == "<@1037734637285421197> .annulation.classement" and var_annul_classement and str(message.author) == "fastattack#7170":
        dico_classement[str(annul_c[0])] = annul_c[1]
        with open("classement devine", "wb") as h:
            pickle.dump(dico_classement, h)
        await message.channel.send(f"le reset du classement de {annul_c[0]} a été annulé : il possède {annul_c[1]} victoires")
        var_annul_classement = False
        annul_c = None


bot.run(os.getenv("TOKEN"))
