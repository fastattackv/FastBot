import random
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import pickle

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

# variables de devine
joueur1 = False
joueur2 = False
id_joueur1 = False
id_joueur2 = False
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
    message_accueil_embed.add_field(name="N'oublie pas d'aller lire les règles", value= f"<#{dico_serv_regles[str(membre.guild)]}>", inline=False)
    message_accueil_embed.add_field(name="Commence par dire bonjour", value=f"<#{dico_serv_discu[str(membre.guild)]}>", inline=False)
    await channel_join.send(embed=message_accueil_embed)


@bot.event
async def on_message(message):
    global joueur1
    global joueur2
    global id_joueur1
    global id_joueur2
    global var_devine
    global var_devine_j1
    global var_devine_j2
    global nombre_a_d
    global points
    global liste_points
    global dico_classement
    channel_jeu = dico_serv_jeu[str(message.guild)]
    if message.author.name == "FastBot":
        pass
    else:
        print(message.author)
        print(f"{message.guild}, {message.channel}")
        print(message.content)
    if message.content.lower() == "ping" and str(message.channel) == channel_jeu:
        await message.channel.send("pong")
    # devine
    elif str(message.channel.id) == channel_jeu and message.content.lower() == "je veux jouer" and var_devine == False:
        joueur1 = message.author
        print(joueur1)
        id_joueur1 = message.author.id
        var_devine = True
        await message.channel.send("à quoi ?")
    elif var_devine and str(message.channel.id) == channel_jeu and message.author == joueur1 and message.content.lower() == "à devine":
        await message.channel.send(f"qui joue avec {joueur1} ?")
    elif var_devine and str(message.channel.id) == channel_jeu and message.content.lower() == "moi":
        joueur2 = message.author
        id_joueur2 = message.author.id
        if joueur1 in dico_classement == False:
            dico_classement[joueur1] = 0
        elif joueur2 in dico_classement == False:
            dico_classement[joueur2] = 0
        if joueur1 == joueur2:
            await message.channel.send("Tricheur !")
            await message.channel.send("On ne joue pas avec soi-même")
            joueur1 = False
            joueur2 = False
            id_joueur1 = False
            id_joueur2 = False
            var_devine = False
            var_devine_j1 = False
            var_devine_j2 = False
        else:
            await message.channel.send(f"<@{id_joueur1}> devine (le nombre entre 1 et 99)")
            var_devine_j1 = True
            nombre_a_d = random.randint(1, 99)
    elif var_devine and str(message.channel.id) == channel_jeu:
        if var_devine_j1 and message.author == joueur1:
            nombre_d = int(message.content)
            if nombre_d == nombre_a_d:
                await message.channel.send("bonne réponse")
                points += 1
                liste_points.append(points)
                await message.channel.send(f"<@{id_joueur2}> devine (le nombre entre 1 et 99)")
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
        elif var_devine_j2 and message.author == joueur2:
            nombre_d = int(message.content)
            if nombre_d == nombre_a_d:
                await message.channel.send("bonne réponse")
                points += 1
                liste_points.append(points)
                await message.channel.send(f"<@{id_joueur1}> a trouvé en {liste_points[0]}")
                await message.channel.send(f"<@{id_joueur2}> a trouvé en {liste_points[1]}")
                if liste_points[0] > liste_points[1]:
                    gagnant = id_joueur2
                    dico_classement[str(joueur2)] = dico_classement[str(joueur2)] + 1
                    await message.channel.send(f"le gagnant est <@{gagnant}>")
                elif liste_points[0] < liste_points[1]:
                    gagnant = id_joueur1
                    dico_classement[str(joueur1)] = dico_classement[str(joueur1)] + 1
                    await message.channel.send(f"le gagnant est <@{gagnant}>")
                elif liste_points[0] == liste_points[1]:
                    await message.channel.send("il y a égalité")
                var_devine_j2 = False
                var_devine = False
                joueur1 = False
                joueur2 = False
                points = 0
                liste_points = []
                with open("classement devine", "wb") as h:
                    pickle.dump(dico_classement, h)
            elif nombre_d < nombre_a_d:
                await message.channel.send("plus")
                points += 1
            elif nombre_d > nombre_a_d:
                await message.channel.send("moins")
                points += 1
    elif message.content == "<@1037734637285421197> quel est le classement ?" and str(message.channel.id) == channel_jeu:
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
    elif message.content == "<@1037734637285421197> .channels":
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


bot.run(os.getenv("TOKEN"))
