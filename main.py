import random
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import pickle

load_dotenv(dotenv_path="config")

default_intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=default_intents)

serv_non_def = "pas de serv"
with open("save serveurs bot", "rb") as f:
    dico_serv = pickle.load(f)

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
async def on_guild_join(serveur):
    global serv_non_def
    serv_non_def = serveur
    return serv_non_def


@bot.event
async def on_member_join(membre):
    channel_join = bot.get_channel(774651919167389767)
    message_accueil_embed = discord.Embed(title="Nouveau membre !", description=f"bienvenue à {membre.id}", color=0x0000ff)
    message_accueil_embed.add_field(name="N'oublie pas d'aller lire les règles", value="<#841388167956791306>", inline=False)
    message_accueil_embed.add_field(name="Commence par dire bonjour", value="<#779687107878715392>", inline=False)
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
    channel_jeu = dico_serv[str(message.guild)]
    if message.author.name == "FastBot":
        pass
    else:
        print(message.author)
        print(message.channel)
        print(message.content)
    if message.content.lower() == "ping" and str(message.channel) == channel_jeu:
        await message.channel.send("pong")
    # début devine
    elif str(message.channel) == channel_jeu and message.content.lower() == "je veux jouer" and var_devine == False:
        joueur1 = message.author
        id_joueur1 = message.author.id
        var_devine = True
        await message.channel.send("à quoi ?")
    elif var_devine and str(message.channel) == channel_jeu and message.author == joueur1 and message.content.lower() == "à devine":
        await message.channel.send(f"qui joue avec {joueur1} ?")
    elif var_devine and str(message.channel) == channel_jeu and message.content.lower() == "moi":
        joueur2 = message.author
        id_joueur2 = message.author.id
        await message.channel.send(f"<@{id_joueur1}> devine (le nombre entre 1 et 99)")
        var_devine_j1 = True
        nombre_a_d = random.randint(1, 99)
    elif var_devine and str(message.channel) == channel_jeu:
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
                    await message.channel.send(f"le gagnant est <@{gagnant}>")
                elif liste_points[0] < liste_points[1]:
                    gagnant = id_joueur1
                    await message.channel.send(f"le gagnant est <@{gagnant}>")
                elif liste_points[0] == liste_points[1]:
                    await message.channel.send("il y a égalité")
                var_devine_j2 = False
                var_devine = False
                joueur1 = False
                joueur2 = False
                points = 0
                liste_points = []
            elif nombre_d < nombre_a_d:
                await message.channel.send("plus")
                points += 1
            elif nombre_d > nombre_a_d:
                await message.channel.send("moins")
                points += 1
    elif message.content == "<@1037734637285421197> .channel.jeu" and message.author.guild_permissions.administrator:
        dico_serv[str(message.guild)] = str(message.channel)
        with open("save serveurs bot", "wb") as f:
            pickle.dump(dico_serv, f)
        await message.channel.send(f"le salon de jeu est <#{message.channel.id}>")
    elif message.content  == "<@1037734637285421197> .channel.jeu" and message.author.guild_permissions.administrator == False:
        await message.channel.send("tu n'es pas admin")

bot.run(os.getenv("TOKEN"))
