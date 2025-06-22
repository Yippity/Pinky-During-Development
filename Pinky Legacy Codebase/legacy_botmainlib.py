# Contains many functions used in main.py to make the bot function properly
# Pinky's signature color is D179F1

import discord
import time
import requests
import json
import random
from cmd_master_list import ALL_COMMANDS # ALL_COMMANDS is a dictionary that holds information regarding each of Pinky's commands
from replit import db

##########################################################
##########################################################

def getQuote(): # Use ZenQuotes' API to return inspirational quote
  quote=requests.get('https://zenquotes.io/api/random')
  jsonData=json.loads(quote.text)
  quote=[jsonData[0]['q'],jsonData[0]['a']] # q represents quote, a represents author
  embeddedquote=discord.Embed(title='\"**%s**\"'%quote[0],color=0xD179F1)
  embeddedquote.add_field(name='** **',value='*- %s*'%quote[1])
  return embeddedquote

##########################################################
##########################################################

async def pfpSteal(cmd,client): # Sends profile picure of user(s) mentioned in command
  if(len(cmd.mentions)==1):
    output='Here\'s a link to their PFP:\n'
    for target in cmd.mentions:
      output+=str(target.avatar.url)
  elif(len(cmd.mentions)>1):
    output='Here\'s a link for every PFP: '
    for target in cmd.mentions:
      output+='\n\n%s: %s'%(target.name,str(target.avatar.url))
  else:
    try:
      targets=cmd.content.split(' ')
      if(len(targets)==2):
        output='Here\'s a link to their PFP:\n'
        target=await client.fetch_user(int(targets[1]))
        print('check3')
        output+=str(target.avatar.url)
      else:
        output='Here\'s a link for every PFP: '
        for n in range(len(targets)-1):
          target=await client.fetch_user(int(targets[n+1]))
          output+='\n\n%s: %s'%(target.name,str(target.avatar.url))
    except:
      output='You need to mention a user to obtain their PFP.'
  await cmd.channel.send(output)

##########################################################
##########################################################

async def clearChannel(cmd): # Erase all messages in given channel (if user is admin)
  if(cmd.author.guild_permissions.administrator):

    try:
      await cmd.channel.send('Nuking messages...')
      time.sleep(2)
      await cmd.channel.purge(limit=1000,bulk=True)
      notif=await cmd.channel.send('Done!')
      time.sleep(2)
      await notif.delete()

      return 0 # Returns 0 only if the use of the command is successful

    except:
      await cmd.channel.send('An error occurred while deleting messages.')
      return 2 # Returns 2 only if user is admin and the command still failed

  else:
    await cmd.channel.send('You need admin privileges to use the \"nuke\" command.')
    return 1 # Returns 1 for non-admin user attempting command

##########################################################
##########################################################

async def kenobi(chan): # "chan" here means channel, totally not me endearingly referring to Obi Wan as if he was a cute anime character...
  with open('hello-there-general-kenobi.gif','rb') as f:
    picture=discord.File(f)
    await chan.send(file=picture)

##########################################################
##########################################################

async def coinFlip(chan): # Just flips a coin, either heads or tails nothing special
  if(random.randint(0,1)==0):
    await chan.send('Heads')
  else:
    await chan.send('Tails')

##########################################################
##########################################################

async def announce(msg): # The bot takes user's desired message and creates an announcement out of it that is then sent by Pinky in the specified channel
  try:
    if(msg.author.id!=982521654536179773 and msg.author.guild_permissions.administrator==False):
      await msg.channel.send('You are not authorized to use this command.')
      return 1

    fullcommand=msg.content
    cmd=fullcommand.split(' ')

    chanid=int(cmd[1][2:].replace('>',''))
    announcementchannel=discord.utils.get(msg.guild.channels,id=chanid)

    newannouncement=fullcommand[11+len(cmd[1]):]
    files=[]
    for x in msg.attachments:
      with open(x.url,'rb') as f:
        file=discord.File(f)
      files.append(file)
      
    await msg.delete()
    await announcementchannel.send(newannouncement,files=files)
    return 0

  except:
    await msg.channel.send('Something went wrong with your command. Please try again.')
    return 2

##########################################################
##########################################################

async def addreactionrole(msg): # Takes a specified message and creates reaction role(s) for it, both target and command must be in same channel, works in conjunction with giverole and removerole
  if(msg.author.guild_permissions.administrator==False): # Only admins can make reaction roles
    await msg.channel.send('You are not authorized to use this command.')
    return 1

  try:
    await msg.delete()
    temp=await msg.channel.send('Processing...')

    elements=msg.content.split(' ')
    roles=[] # Stores role IDs to database
    emojis=[] # Stores emojis to database
    target=await msg.channel.fetch_message(int(elements[1]))

    for n in range(2,len(elements)): # Stores roles in list, emojis in separate list
      if(n%2==0):
        roles.append(elements[n])
      else:
        emojis.append(elements[n])

    if(len(roles)==0 or len(emojis)==0): # There must be at least one pair of a role and an emoji
      await temp.delete()
      temp=await msg.channel.send('There must be at least one role and one emoji provided. Please try again.')
      time.sleep(4)
      try:
        await temp.delete()
      except:
        pass

      return 3
    
    if(len(roles)!=len(emojis)): # Roles and emojis must have a 1:1 ratio
      await temp.delete()
      temp=await msg.channel.send('The number of roles listed must equal the number of emojis listed. Please try again.')
      time.sleep(4)
      try:
        await temp.delete()
      except:
        pass

      return 4

    for n in range(len(roles)): # Ascertain the ID of each role being made into a reaction role
      try:
        roles[n]=int(roles[n])
      except:
        roles[n]=int(roles[n][3:-1])

    for n in range(len(emojis)): # React to target message with each given emoji (in order of appearance in command)
      await target.add_reaction(emojis[n])
      
    db[str(target.id)]=[roles,emojis]

    await temp.delete()
    return 0

  except:
    await temp.delete()
    temp=await msg.channel.send('Something went wrong with your command. Please try again.')
    time.sleep(4)
    try:
      await temp.delete()
    except:
      pass
    return 2

##########################################################
##########################################################

async def giverole(reaction,client): # Target user is given specified role
  try:
    messagedata=db[str(reaction.message_id)] # Each key contains two lists

    emojis=[]

    for x in messagedata[1]: # Converts second list (contains emojis) to more readable form
      emojis.append(x)

    for x in range(len(emojis)): # Compares each emoji in list to emoji in reaction

      if(str(emojis[x])==str(reaction.emoji)):

        server=await client.fetch_guild(reaction.guild_id)
        role=server.get_role(messagedata[0][x]) # Fetches role object based on role ID listed in first list

        await reaction.member.add_roles(role,reason='Reaction role given')

        return True

    return False

  except:
    return False

##########################################################
##########################################################

async def removerole(reaction,client): # Target user has specified role removed
  try:
    messagedata=db[str(reaction.message_id)]

    emojis=[]

    for x in messagedata[1]:
      emojis.append(x)

    for x in range(len(emojis)):

      if(str(emojis[x])==str(reaction.emoji)):

        server=await client.fetch_guild(reaction.guild_id)
        role=server.get_role(messagedata[0][x])
        reactionmember=await server.fetch_member(reaction.user_id)

        try:
          await reactionmember.remove_roles(role,reason='Reaction role removed')
        except Exception as inst:
          print(inst)
        return True

    return False

  except:

    return False

##########################################################
##########################################################

async def help(msg,command=None): # When used with no specified command, returns list of commands; if a particular command is specified, the format of the command's proper usage will be given in addition to a description of its operations
  if(command!=None):
    specifiedcommand=True
    try: # Specified command must be in list of commands
      details=ALL_COMMANDS[command]
    except: # Send error message if requested command is invalid
      await msg.channel.send('The command \"%s\" does not exist. Please try again.'%command)
      print('- Unable to process help command, requested command does not exist')
      return
    helpembed=discord.Embed(title='**Help - %s**'%command,color=0xD179F1)
    helpembed.add_field(name='```%%%s```'%details[0],value='>>> ```%s```'%details[2])

  else: # When there is no specified command
    specifiedcommand=False
    helpembed=discord.Embed(title='**Help - Pinky**',color=0xD179F1)
    for x in ALL_COMMANDS.keys():

      helpembed.add_field(name='```%s:```'%x,value='>>> ```%s```'%ALL_COMMANDS[x][1])
    

  await msg.channel.send(embed=helpembed)

  if(specifiedcommand): # If command is specified
    print('- %s used the help command on %s'%(str(msg.author),command))
  else: # If no command is specified
    print('- %s used the generic help command'%str(msg.author))

##########################################################
##########################################################

async def delreactionroles(msg): # Upon deletion of a message attached to reaction roles, Pinky will clear up room in its database that held necessary data to the facilitation of the roles
  try:
    del db[str(msg.message_id)]
    return True
  except:
    return False
    
##########################################################
##########################################################
########### The below functions are incomplete ###########
########## but are planned for the near future. ##########
##########################################################
##########################################################

# # async def devmessage(msg): # Anonymously sends your message directly to the developer of Pinky via the bot's DMs; can be used for reporting bugs with the bot, suggesting a new feature, or just trolling me I guess... maybe this is a bad idea lol

# async def emotesteak(msg): # "Steal" a download link to all emotes in message (yes I am aware it says emoteSTEAK instead of emoteSTEAL and no I will not elaborate why >:3 )

##########################################################
################# Miscellaneous Thoughts #################
##########################################################
##########################################################

# Modify help so that you can receive detailed specifications of multiple commands; e.g. "%help reactionrole nuke announce" would have Pinky send three separate embeds, one for each requested command

# Allow replying to a message with reactionrole command to substitute for listing a particular message ID

# Allow the specification of a channel or multiple channels to purge with the nuke command

# Customizable bot command prefix

# Read in commands using some alternative method instead of if-elif-else statements

# Custom welcome messages/embeds