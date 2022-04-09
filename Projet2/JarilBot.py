
import discord
import random
from operations_package import operations_modules
from oui_non_package import oui_non_modules
from discord.ext import commands
from discord.utils import get

bot = commands.Bot(command_prefix="bj/", description="Nouveau Bot de Jaril")
token = "OTU3MjQyODEwNTAxODI4Njcw.Yj771g.EwWmXNWSmqhM2MoUfBDvzWdtifU"

# listes pour on_message()
liste_quoi=["Feuse", "Feur", "Fure", "Chi", "Driceps", "Drilatère", "D", "Drupède", 
            "Tuor", "Druplé", "De neuf", "Ffage", "Artz", "Rterback", "Dragénaire",
            "Drilataire", "Druple", "Dricolore", "Ffé", "Drillion", "Drisyllabe", "Drireacteur"]
liste_re=["Nard","Quin"]

# on_ready() pour vérifier si le bot est connecté
@bot.event
async def on_ready():
    await bot.change_presence(afk=False, status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.playing, name="."))
    connexion="Le bot est prêt!"
    print(connexion)

# on_message() pour le délire des syllabes
@bot.event
async def on_message(message):
    roulette_message = random.choice(liste_quoi)

    with open("quoi.txt", "r",encoding="utf-8") as myfile:
        myfile_received = [line.strip() for line in myfile]

        if message.content in myfile_received:
            await message.reply(roulette_message)
    
    if message.content=="Ping":
        await message.reply("Pong, PC")
    if message.content=="Ping MP":
        await message.reply("Pong, Téléphone")

    await bot.process_commands(message)

# on_raw_reaction_add
@bot.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    if message_id == 962339998378647564:  #ID depends on message
        guild = await bot.fetch_guild(payload.guild_id)

        if payload.emoji.name == 'wexxed':
            role = get(guild.roles, name="xxxx")
        elif payload.emoji.name == 'xxxx':
            role = get(guild.roles, name="xxx")
        else:
            role = get(guild.roles, name = payload.emoji.name)
        
        if role is not None:
            member = payload.member
            if member is not None:
                await member.add_roles(role,reason=f"Le rôle '{role.name}' a été ajouté !")
                embed = discord.Embed(title="Ajout de rôle",description=f"Le rôle {role.name} dans le serveur {guild.name} a été ajouté!",color=discord.Colour.dark_green())
                await member.send(embed=embed)
                print("rôle ajouté")
            else:
                print("member not found")
        else:
            print("role not found.")

# on_raw_reaction_remove
async def on_raw_reaction_remove(payload):
    message_id = payload.message_id
    if message_id == 962339998378647564:  #ID depends on message
        guild = await bot.fetch_guild(payload.guild_id)

        if payload.emoji.name == 'wexxed':
            role = get(guild.roles, name="xxxx")
        elif payload.emoji.name == 'xxxx':
            role = get(guild.roles, name="xxx")
        else:
            role = get(guild.roles, name = payload.emoji.name)
        
        if role is not None:
            member = get(guild.members, id=payload.user_id)
            if member is not None:
                await member.remove_roles(role)
                print("done")
            else:
                print("member not found")
        else:
            print("role not found.")

# bj/clear
@bot.command()
async def clear(ctx, nombre:int):
    messages = await ctx.channel.history(limit=nombre+1).flatten()

    for i in messages:
        await i.delete()

# bj/operations
@bot.command()
async def operations(ctx):
    auteur=ctx.author
    channel=ctx.channel
    nombre1=0
    nombre2=0
    
    # fonctions pour bj/operations

    # verifier difficultés, arguments: string, return: un entier booléen (entre 1 et 5)
    async def difficiultés(reaction:str):
        if reaction.emoji == "1️⃣":
            return 1
        if reaction.emoji == "2️⃣":
            return 2
        if reaction.emoji == "3️⃣":
            return 3
        if reaction.emoji == "4️⃣":
            return 4
        if reaction.emoji == "5️⃣":
            return 5
    
    # verifier opération, arguments: nb1, nb2, string, return: int (le résultat Ordinateur)
    async def operations(reaction:str, nb1:int,nb2:int):
        if reaction.emoji == "➕":
            await ctx.send("Donnez le résultat de " + format(nb1) + " + " + format(nb2))
            return nb1 + nb2
        if reaction.emoji == "➖":
            await ctx.send("Donnez le résultat de " + format(nb1) + " - " + format(nb2))
            return nb1 - nb2
        if reaction.emoji == "✖️":
            await ctx.send("Donnez le résultat de " + format(nb1) + " * " + format(nb2))
            return nb1 * nb2
        if reaction.emoji == "➗":
            await ctx.send("Donnez le résultat de " + format(nb1) + " // " + format(nb2))
            return nb1 // nb2
        if reaction.emoji == "💯":
            await ctx.send("Donnez le résultat de " + format(nb1) + " % " + format(nb2))
            return nb1 % nb2

    # afficher résultats, arguments: 2 entiers, appel: await nécessaire
    async def resultats(userAnswer:int, Answer:int):
        if userAnswer == Answer:
            message = await ctx.reply("C'est la bonne réponse! ***Réponse:*** " + f"({Answer})")
            await message.add_reaction("✅")
        else:
            message = await ctx.reply("C'est la mauvaise réponse! ***Réponse:*** "  + f"({Answer})")
            await message.add_reaction("❌")
    
    await ctx.reply(f"Salut <@{auteur.id}>! Es-tu venu.e pour tester tes capacités en calcul?!\nVous aurez 1 minute pour trouver le résultat!\n")
    message= await ctx.send("Veuillez choisir votre niveau de difficulté(intervalles):\n:one: 1 à 101\n:two: 1 à 201\n:three: 1 à 301\n:four: 1 à 401\n:five: 1 à 501")
    await message.add_reaction("1️⃣")
    await message.add_reaction("2️⃣")
    await message.add_reaction("3️⃣")
    await message.add_reaction("4️⃣")
    await message.add_reaction("5️⃣")

    # check emoji, arguments: reaction et user
    def checkEmoji(reaction,user):
        return ctx.message.author == user and message.id == reaction.message.id and (str(reaction.emoji)=="1️⃣" or str(reaction.emoji)=="2️⃣" or str(reaction.emoji)=="3️⃣" or str(reaction.emoji)=="4️⃣" or str(reaction.emoji)=="5️⃣")

    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=60,check=checkEmoji)
        # choix_difficultés prend 1 ou 2 ou 3 ou 4 ou 5
        await ctx.send("Votre choix a été pris en compte!")
        choix_difficultés = await difficiultés(reaction)
        nombre1 = operations_modules.affection(nombre1,choix_difficultés)
        nombre2 = operations_modules.affection(nombre2,choix_difficultés)
    except:
        await ctx.send("60 secondes se sont écoulées! Il fallait être plus rapide que ça!")

    message= await ctx.send("Veuillez choisir votre opération:\n:heavy_plus_sign: Addition\n:heavy_minus_sign: Soustraction\n:heavy_multiplication_x: Multiplication\n:heavy_division_sign: Division\n:100: Opération Super Difficile")
    await message.add_reaction("➕")
    await message.add_reaction("➖")
    await message.add_reaction("✖️")
    await message.add_reaction("➗")
    await message.add_reaction("💯")
    
    # check emoji, arguments: reaction et user
    def checkEmoji2(reaction,user):
        return ctx.message.author == user and message.id == reaction.message.id and (str(reaction.emoji)=="➕" or str(reaction.emoji)=="➖" or str(reaction.emoji)=="✖️" or str(reaction.emoji)=="➗" or str(reaction.emoji)=="💯")
    
    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=60,check=checkEmoji2)
        await ctx.send("Votre choix a été pris en compte!")
        resultatOrdi = await operations(reaction,nombre1,nombre2)
        await ctx.send("L'ordinateur a déjà calculé l'opération, à vous de retrouver le résultat!")
    except:
        await ctx.send("60 secondes se sont écoulées! Il fallait être plus rapide que ça!")
    
    # check message, arguments: message
    def checkMessage(message):
        return message.author == auteur and message.channel == channel
    
    await ctx.send("Votre réponse ?")
    try:
        message = await bot.wait_for("message", timeout=60, check=checkMessage)
        if message.content.isnumeric():
            resultatHumain=int(message.content)
            await resultats(resultatHumain,resultatOrdi)
        else:
            await ctx.send("Il ne faut pas discuter durant le jeu! Recommencez svp!")
            return

    except:
        await ctx.send("60 secondes se sont écoulées! Il fallait être plus rapide que ça!")
        await resultats(0,resultatOrdi)

# bj/userinfo
@bot.command()
async def userinfo(ctx, member:discord.Member):
    roles = member.roles
    roles = [i.mention for i in roles]

    embed=discord.Embed(title="Informations de l'utilisateur:",description=f"La personne que vous stalkez actuellement est: {member.mention}",color=discord.Colour.dark_green())
    embed.set_thumbnail(url=member.avatar_url) #afficher l'avatar
    embed.set_footer(text=f"{ctx.author.display_name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url) #message en bas de page
    embed.add_field(name="Nom#Tag: ",value=f"{member.display_name}#{member.discriminator}",inline=True) #field 1 inline=true
    embed.add_field(name="ID de l'utilisateur demandée: ",value=f"{member.id}",inline=True) #field 2 inline=true
    
    embed.add_field(name="Lien vers l'avatar: ",value=f"{member.avatar_url}",inline=False) #field 3 inline=false
    
    embed.add_field(name="Le compte discord a été crée le: ",value=f"{member.created_at}",inline=True) #field 4 inline=true
    embed.add_field(name="L'utilisateur a rejoint le: ",value=f"{member.joined_at}",inline=True) #field 5 inline=true
    
    embed.add_field(name="Les rôles de l'utilisateur: ",value=f"{','.join(roles)}",inline=False) #field 6 inline=False
    embed.add_field(name="Serveurs: ",value=f"{member.guild}",inline=True) #field 7 inline=False
    await ctx.send(embed=embed)

# bj/oui_non 
@bot.command()
async def oui_non(ctx):
    booloui= False # True = il a dit oui / non, False= il est toujours en course
    boolouais= False # True = il a dit ouais / nah , False= il est toujours en course

    # liste de questions pour bj/oui_non
    liste_questions=[]

    # ouverture en utf-8, lecture ligne par ligne, fermeture
    with open("questions.txt", "r", encoding="utf-8") as infile:
        liste_questions= infile.readlines()

        # le coeur du jeu, les arguments sont claqués, obligés d'en mettre! 
        async def main_game(booloui:str,boolouais:str):
            compteurActuel=1
            compteurMax=10
            gagner= False # True= il a gagné sur 10 questions, False= il continue à répondre ou a perdu avant les 10 questions!
            while booloui==False and gagner==False:
                roulette_message= random.choice(liste_questions)
                embed= discord.Embed(description=f"{roulette_message}",color=discord.Color.dark_gold())
                embed.set_footer(text = f"Question actuelle: {compteurActuel} / {compteurMax}", icon_url=ctx.guild.icon_url)
                await ctx.send(embed=embed)
            
                message = await bot.wait_for("message",timeout=60, check=checkMessage)
                
                booloui= await oui_non_modules.oui_non(str(message.content))
                boolouais = await oui_non_modules.ouais_nan(str(message.content))
                
                while boolouais == True and booloui==False:
                    await ctx.send("La réponse attendue n'est pas acceptée! En attente d'une nouvelle réponse! :gear:")
                    message = await bot.wait_for("message",timeout=60,check=checkMessage)
                    booloui= await oui_non_modules.oui_non(str(message.content))                
                    boolouais= await oui_non_modules.ouais_nan(str(message.content))
            
                if compteurActuel==compteurMax:
                    gagner=True
                    break
                if gagner==False and booloui==True:
                    compteurActuel = compteurActuel - 1
                    break
                else:
                    compteurActuel = compteurActuel + 1

            if booloui == True and gagner==False:
                embed=discord.Embed(title="Allez hop perdu !",description=f"Bonnes réponses: {compteurActuel} / {compteurMax}",color=discord.Colour.dark_red())
                embed.set_footer(text=f"{ctx.author.display_name}#{ctx.author.discriminator}",icon_url=ctx.author.avatar_url)
                message = await ctx.send(embed=embed)                
                await message.add_reaction("❌")
                return
            if booloui == False and gagner==True:
                embed=discord.Embed(title="Game Won !",description=f"Bonnes réponses: {compteurActuel} / {compteurMax}",color=discord.Colour.dark_green())
                embed.set_footer(text=f"{ctx.author.display_name}#{ctx.author.discriminator}",icon_url=ctx.author.avatar_url)
                message = await ctx.send(embed=embed)                
                await message.add_reaction("✅")
                return

    # ligne 295 check message
    def checkMessage(message):
        return message.author == ctx.author and message.channel == ctx.channel
        
    embed=discord.Embed(title="Ni OUI - Ni NON",description=f"Bienvenue <@{ctx.author.id}> ! Comme on peut le voir dans le titre, c'est le jeu populaire: Ni OUI-Ni NON !",color=discord.Colour.dark_green())
    embed.set_footer(text = "Pour commencer, réagissez avec ✅ ou ❌(vous avez 60 secondes pour réagir !)", icon_url=ctx.guild.icon_url)
    message = await ctx.reply(embed=embed)
    await message.add_reaction("✅")
    await message.add_reaction("❌")

    # ligne 305 check emoji
    def checkEmoji(reaction,user):
        return ctx.message.author == user and message.id == reaction.message.id and (str(reaction.emoji)=="❌" or str(reaction.emoji)=="✅")
    
    try:
        reaction,user = await bot.wait_for("reaction_add",timeout=60,check=checkEmoji)
        if str(reaction.emoji) == "✅":
            await ctx.send("Le jeu va commencer ... :gear:")
            await main_game(booloui,boolouais)
        elif str(reaction.emoji)== "❌":
            await ctx.send("Dommage! à la prochaine!")
            return
    except:
        await ctx.send("60 secondes se sont écoulées! Il fallait être plus rapide que ça!")

# bj/surprises
@bot.command()
async def surprises(ctx):
    # ouverture en utf-8, lecture ligne par ligne, fermeture
    liste_dadjokes=[]
    with open("dad_jokes.txt","r", encoding="utf-8") as infile:
        liste_dadjokes=infile.readlines()
        roulette_message = random.choice(liste_dadjokes)
        embed=discord.Embed(title="You requested for a dad joke!", description=f"{roulette_message}", color= discord.Colour.dark_magenta())
        await ctx.author.send(embed=embed)

# bj/reglements
@bot.command()
async def reglements(ctx):

    # ouverture les fichiers et les fichiers se ferment automatiquement. complexité en temps : je ne sais pas
    with open("entente.txt","r",encoding="utf-8") as entente:
        with open("adequation.txt","r",encoding="utf-8") as adequation:
            with open("exterieur.txt","r",encoding="utf-8") as exterieur:
                with open("moderation.txt","r",encoding="utf-8") as moderation:
                    entente_read=entente.read()
                    adequation_read=adequation.read()
                    exterieur_read=exterieur.read()
                    moderation_read=moderation.read()

                    embed=discord.Embed(title="RÈGLEMENTS",description="", color= discord.Colour.dark_blue())
                    embed.add_field(name="ENTENTE:", value=f"{entente_read}",inline=False)
                    embed.add_field(name="ADEQUATION:", value=f"{adequation_read}",inline=False)
                    embed.add_field(name="EXTERIEUR:", value=f"{exterieur_read}",inline=False)
                    embed.add_field(name="MODERATION:", value=f"{moderation_read}",inline=False)
                    embed.set_footer(text="Cordialement, le Bureau Des Licences",icon_url=f"{ctx.guild.icon_url}")
                    message = await ctx.send(embed=embed)
                    await message.add_reaction("✅")

# bj/strawpolls
@bot.command()
async def strawpolls(ctx):
    with open("strawpoll.txt","r",encoding="utf-8") as strawpolls:
        strawpolls_read=strawpolls.read()
        embed=discord.Embed(title="VOTE À L'UNANIMITÉ", description="Votez pour le futur nom du bot", color=discord.Colour.dark_green())
        embed.add_field(name="Les choix proposés par des personnes:",value=f"{strawpolls_read}",inline=False)
        embed.set_footer(text="Veuillez réagir pour voter!",icon_url=f"{ctx.guild.icon_url}")
        message = await ctx.send(embed=embed)
        await message.add_reaction("1️⃣")
        await message.add_reaction("2️⃣")
        await message.add_reaction("3️⃣")
        await message.add_reaction("4️⃣")
        await message.add_reaction("5️⃣")
        await message.add_reaction("6️⃣")
        await message.add_reaction("7️⃣")
        await message.add_reaction("8️⃣")
        await message.add_reaction("9️⃣")
        await message.add_reaction("🔟")
        await message.add_reaction("⏸️")

bot.run(token)

# objectif à faire:
# 447-202 = 245 lignes pour l'ancien jeu operations
# 192-68 = 124 lignes pour le nouveau jeu operations

# on_ready() = 5 lignes
# on_message() = 30 lignes
# bj/clear = 6 lignes
# bj/operations = 125 lignes
# bj/userinfo = 21 lignes
# bj/oui_non = 87 lignes