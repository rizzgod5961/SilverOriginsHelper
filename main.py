from interactions import Client, Intents, listen, slash_command, SlashContext
from interactions import slash_option, OptionType, Embed
import json
import os

bot = Client(intents=Intents.DEFAULT)

@listen()
async def on_ready():
    print(f"Ready {bot.owner}")

@slash_command(name="addplayer", description="Adds a player to the data.")
@slash_option(
    name="discordusername",
    description="Discord username",
    required=True,
    opt_type=OptionType.STRING
)
@slash_option(
    name="minecraftusername",
    description="Minecraft username",
    required=True,
    opt_type=OptionType.STRING
)
async def addplayer(ctx: SlashContext, discordusername: str, minecraftusername: str):
    data = {}
    filename = "testingData.txt"
    
    if os.path.exists(filename):
       with open(filename, 'r') as file:
            data = json.load(file)

    if discordusername in data:
        await ctx.send(embed=Embed(title="**Error**", description=f'```{discordusername} already exists.```'))
        return

    data[discordusername] = minecraftusername
    
    with open(filename, 'w') as file:
        json.dump(data, file)

    await ctx.send(embed=Embed(title="**Success**", description=f'```Data added successfully. "{discordusername}": "{minecraftusername}"```'))

@slash_command(name="removeplayer", description="Removes a player from the data.")
@slash_option(
    name="discordusername",
    description="Discord username",
    required=True,
    opt_type=OptionType.STRING
)
async def removeplayer(ctx: SlashContext, discordusername: str):
    data = {}
    filename = "testingData.txt"
    
    if os.path.exists(filename):
       with open(filename, 'r') as file:
            data = json.load(file)

    try:
        data[discordusername]
    except:
        await ctx.send(embed=Embed(title="**Error**", description=f'```{discordusername} doesn\'t exist.```'))
        return

    del data[discordusername]

    with open(filename, 'w') as file:
        json.dump(data, file)
        
    await ctx.send(embed=Embed(title="**Success**", description=f'```Data removed successfully. "{discordusername}"```'))

@slash_command(name="returnminecraftusername", description="Returns the minecraft username of the discord user.")
@slash_option(
    name="discordusername",
    description="Discord username",
    required=True,
    opt_type=OptionType.STRING
)
async def returninecraftusername(ctx: SlashContext, discordusername: str):
    with open('testingData.txt', 'r') as f:
        data = json.load(f)

    if discordusername in data:
        await ctx.send(embed=Embed(title="**Success**", description=f'```{data.get(discordusername)}```'))
    else:
        await ctx.send(embed=Embed(title="**Error**", description=f'```{discordusername} was not found in the data file!```'))

@slash_command(name="returndiscordusername", description="Returns the discord username of the minecraft player.")
@slash_option(
    name="minecraftusername",
    description="Minecraft username",
    required=True,
    opt_type=OptionType.STRING
)
async def returndiscordusername(ctx: SlashContext, minecraftusername: str):
    with open('testingData.txt', 'r') as f:
        data = json.load(f)

    values = list(data.values())
    keys = list(data.keys())

    try:
        index = values.index(minecraftusername)
        await ctx.send(embed=Embed(title="**Success**", description=f'```{keys[index]}```'))
    except:
        await ctx.send(content=f'```{minecraftusername} was not found in the data file!```')
        await ctx.send(embed=Embed(title="**Error**", description=f'```{minecraftusername} was not found in the data file!```'))

@slash_command(name="returnallplayers", description="Returns all players.")
async def returnallusers(ctx: SlashContext):
    with open('testingData.txt', 'r') as f:
        data = json.load(f)

    users = ""

    for user in data:
        users += user + ": " + data.get(user) + "\n"
    users = users.rstrip("| ")
    if users != "":
        await ctx.send(embed=Embed(title="**Success**", description=f'''Users returned.```
{users}
```\n`<discord username>: <minecraft username>`'''))
    else:
        await ctx.send(embed=Embed(title="**Error**", description=f'```Players returned unsuccessfully. No indexes were found!```'))

bot.start("")
