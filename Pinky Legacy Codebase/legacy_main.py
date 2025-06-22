# Pinky Discord bot source code
# Developed solely by @yippity on Discord

import discord
import asyncio
import requests
import json
import random
from datetime import datetime
import wavelink
from wavelink.ext import spotify
import os
from cmd_master_list import ALL_COMMANDS # ALL_COMMANDS is a dictionary that holds information regarding each of Pinky's commands
from replit import db
import os
import time
import pprint
from typing import Optional
import legacy_botmainlib as bot # Bot-specific functions

print('Ready')
# Everything in this file is legacy code and should be used as reference only

client=discord.Client(intents=discord.Intents.all()) # Client connection to Discord

print('Now running Pinky, a general-purpose bot for Discord developed by Fulcrum#6643\n\nIn order to add Pinky to a server, use this link:\nhttps://discord.com/api/oauth2/authorize?client_id=983212810907553803&permissions=8&scope=bot\n\nWhen the bot joins your server, use the \"%help\" command to see what it can do.\n\nPinky should be running shortly!\n\n')

@client.event
async def on_ready(): # Everything in on_ready is executed each time Pinky comes online properly
  print('Log:\n\n- Logged in as {0.user}'.format(client))
  act=discord.Activity(type=discord.ActivityType.listening,name="the screams of the damned")
  await client.change_presence(status=discord.Status.online, activity=act)


@client.event
async def on_message(msg):

  if(msg.author.bot): # If msg is from a bot, including Pinky itself, ignore it
    return

  if(msg.content.startswith('%')): # Command prefix is "%"
    if(msg.content[1:6]=='quote'): # Sends inspirational quote; Disclaimer: I do not claim to own any of these quotes, nor do I personally endorse any quote or its author that a user may come across when using this command
      await msg.channel.send(embed=bot.getQuote())
      print('- Quote generated and sent')
##########################################################

    elif(msg.content[1:4]=='pfp'): # Sends links to all mentioned users' PFPs
      await bot.pfpSteal(msg,client)
      print('- Profile picture steal executed')
##########################################################

    elif(msg.content[1:]=='nuke'): # Erase all (kinda) messages in given channel (only if user is admin); Warning: can be a little slow, and cannot be undone
      clearresult=await bot.clearChannel(msg)
      if(clearresult==1):
        print('- Request to nuke messages in %s denied'%str(msg.channel))
      elif(clearresult==0):
        print('- Messages nuked in #%s'%str(msg.channel))
      else:
        print('- An error occurred during message purge in %s'%str(msg.channel))
##########################################################

    elif(msg.content[1:]=='flipcoin'): # Flips coin
      await bot.coinFlip(msg.channel)
      print('- Coin flipped')
##########################################################

    elif(msg.content[1:9]=='announce'): # Sends announcement (message is element 3) from bot in specified channel (element 2)
      result=await bot.announce(msg)
      if(result==0):
        print('- Announcement made successfully')
      elif(result==1):
        print('- Announcement failed, user is not authorized to use this command')
      else:
        print('- Announcement failed, an error occurred')
##########################################################

    elif(msg.content[1:]=='count'):
      for x in range(1000000):
        await msg.channel.send(x+1)
##########################################################

    elif(msg.content[1:13]=='reactionrole' or msg.content[1:3]=='rr'): # Adds reaction role(s) to specified message
      result=await bot.addreactionrole(msg)
      if(result==0):
        print('- Successfully added reaction role(s) to message')
      elif(result==1):
        print('- User attempted to use reactionrole command, but did not have permission')
      else:
        print('- Adding reaction role(s) failed, an error occurred')
##########################################################

    elif(msg.content[1:5]=='help'): # Gives list of all commands and brief overview of each one if no particular command is specified
      cmd=msg.content.split(' ')
      if(len(cmd)>1):
        await bot.help(msg,command=cmd[1])
      else:
        await bot.help(msg)
##########################################################
    else: # Sends if no real command is specified or format is not understood
      error=await msg.channel.send('Sorry, but I don\'t understand the command you sent. Try sending \"%help\" to view the details of each command you can use with Pinky.')
      print('- Command received, but could not be interpreted')
      time.sleep(7)
      await error.delete()
##########################################################

  elif(msg.content.startswith('H') or msg.content.startswith('h')): #  G E N E R A L   K E N O B I
    if(msg.content[1:11]=='ello there' or msg.content[1:11]=='ELLO THERE'):
      await bot.kenobi(msg.channel)
      print('- \"Hello there\" responded to')
##########################################################


@client.event # Reaction roles!
async def on_raw_reaction_add(reaction):

  if(reaction.member.id!=983212810907553803): # This if statement prevents Pinky from giving itself reaction roles
    if(await bot.giverole(reaction,client)==True):
      print('- Gave reaction role to %s'%str(await client.fetch_user(reaction.user_id)))
    else:
      print('- %s has made an edit to reactions on a message; no actions taken'%str(await client.fetch_user(reaction.user_id)))


@client.event # Remove reaction role when user removes their reaction emoji from the message
async def on_raw_reaction_remove(reaction):

  if(await bot.removerole(reaction,client)==True):
    print('- Removed reaction role from %s'%str(await client.fetch_user(reaction.user_id)))
  else:
    print('- %s has made an edit to reactions on a message; no actions taken'%str(await client.fetch_user(reaction.user_id)))


@client.event # Deletes data associated with any reaction role message that is deleted
async def on_raw_message_delete(msg):

  if(await bot.delreactionroles(msg)):
    print('- Reaction role data associated with message #%i has been purged'%msg.message_id)

running=False
while(running==False):
  try:
    client.run(os.getenv('TOKEN'))
    running=True
  except HTTPException as ratelimiterror:
    print(f'Pinky has been rate-limited!\n\n{ratelimiterror.resonse}\n\n{ratelimiterror.data}')
    time.sleep(200)