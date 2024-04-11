import discord
import random
from discord.ext import commands
from discord import app_commands
import openai
import insultes
import time


openai.api_key = "clé open ai ici"


intents = discord.Intents.default()
client = commands.Bot(command_prefix='!', intents=intents, description="Petit projet pour apprendre python , donner moi des idées pour le bot")
intents.message_content = True



client.remove_command('help')
@client.command()
async def help(ctx):
    await ctx.send("En cours de rédaction")

       


#bot connecter sur console 
@client.event
async def on_ready():
    activity_name = "!help pour les commandes 👀"
    activity = discord.Activity(type=discord.ActivityType.watching, name=activity_name)
    await client.change_presence(status=discord.Status.online, activity=activity)
    print('Bot connecté en tant que', client.user.name)
    try:
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)


@client.command()
async def dm(ctx, user: discord.User = None, *, value = None):
  if user == ctx.message.author:
    await ctx.send("tu ne peux pas te dm")
  else:
    await ctx.message.delete()
    if user == None:
      await ctx.send(f'**{ctx.message.author},** Choisis une personne a mentionner.')
    else:
      if value == None:
        await ctx.send(f'**{ctx.message.author},** Choisis un message a envoyer.')
      else:
        await user.send(value)



@client.tree.command(name = "hello", description= "commande test salut")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message (f"salut {interaction.user.mention}")



@client.command()
async def gpt(ctx,*, question):
    if question == None:
         await ctx.send(f'**{ctx.message.author},** Choisis une question a poser.')
    else:
#la partie chatgpt
        prompt = question
        model = "gpt-3.5-turbo"
        response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
            ],
        max_tokens=2000,
        temperature=0.7
        )
        generated_text = response.choices[0].message['content']
#la partie embed
        embed=discord.Embed(
            title="Amogus GPT",
            url=None,
            description="Poser une question a Amogus GPT",
            color=discord.Color.red())
        embed.add_field(name="**Votre question**", value= question)
        embed.add_field(name= "**Votre réponse**", value= generated_text)
        await ctx.send(embed=embed)






#commande MOT
@client.command()
async def mot(ctx,* , reponse):
    await ctx.message.delete()
    await ctx.send(reponse)



#commande sur les mots
@client.event
async def on_message(message):
    print(time.ctime(),":","{0}: {1}".format(message.author, str(message.content)))
        
    if message.content  in insultes.insultes :
        await message.delete()
        await message.channel.send("Interdiction d'insulter")
    await client.process_commands(message)


# Dictionnaire pour stocker le nombre de crédits de chaque utilisateur
user_credits = {}


# Commande pour obtenir le nombre de crédits d'un utilisateur
def get_user_credits(user_id):
    return user_credits.get(user_id, 0)

# Commande pour attribuer des crédits à un utilisateur
def give_user_credits(user_id, amount):
    current_credits = get_user_credits(user_id)
    user_credits[user_id] = current_credits + amount

# Commande pour donner des crédits à un utilisateur
@client.command()
async def give_credits(ctx, amount: int):
    user_id = ctx.author.id
    give_user_credits(user_id, amount)
    await ctx.send(f"Vous avez reçu {amount} crédits !")

# Commande pour vérifier le nombre de crédits de l'utilisateur
@client.command()
async def check_credits(ctx):
    user_id = ctx.author.id
    credits = get_user_credits(user_id)
    await ctx.send(f"Vous avez {credits} crédits.")
    
    

#commande PING
@client.command()
async def ping(ctx):
    start_time = time.time()
    message = await ctx.send("Ping...")
    end_time = time.time()

    # Calculer le temps de réponse en millisecondes
    latency = (end_time - start_time) * 1000
    await message.edit(content=f"Pong! Latence: {int(latency)}ms")

client.run("token ici")



