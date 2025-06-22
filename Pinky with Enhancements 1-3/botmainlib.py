# Contains many functions used in main.py to make the bot function properly
# Pinky's signature color is #D179F1 (0xD179F1 in most places in code due to syntax)

import nextcord
import asyncio
import requests
import json
import random
import sqlite_interface
from datetime import datetime
from cmd_master_list import ALL_COMMANDS

data = None


async def pinkylog(client, message):  # Sends log messages direct to a Discord text channel, none specified currently
    # logchannel = await client.fetch_channel(None)
    # try:
    #     await logchannel.send('%s' % message)
    # except:
    #     pass
    print('%s' % message)


##########################################################
##########################################################


def getQuote():  # Use ZenQuotes' API to return inspirational quote
    quote = requests.get('https://zenquotes.io/api/random')
    jsonData = json.loads(quote.text)
    quote = [jsonData[0]['q'],
             jsonData[0]['a']]  # q represents quote, a represents author
    embeddedquote = nextcord.Embed(title='\"**%s**\"' % quote[0],
                                   color=0xD179F1)
    embeddedquote.add_field(name='** **', value='*- %s*' % quote[1])
    return embeddedquote


##########################################################
##########################################################


async def pfpSteal(
        client, cmd,
        target
):  # Sends profile picure of user(s) mentioned in command
    try:
        pfpembed = nextcord.Embed(title='**%s\'s profile picture**' %
                                        target.name,
                                  color=0xD179F1)
        if (target.id != 983212810907553803):
            pfpembed.set_image(target.avatar.url)
            await cmd.send(embed=pfpembed)
        else:
            pfp = nextcord.File('pinky-pfp.png', filename='pinky-pfp.png')
            pfpembed.set_image('attachment://pinky-pfp.png')
            pfpembed.add_field(
                name='*Disclaimer:*',
                value=
                '*Pinky\'s profile picture was created using the following link: https://www.neka.cc/composer/10350*'
            )
            await cmd.send(file=pfp, embed=pfpembed)

    except:
        await cmd.send(
            'Please enter a valid Discord member or user ID as the target.')


##########################################################
##########################################################


async def nukeChannel(
        cmd
):  # Erase all messages in given channel (if user is admin)
    try:

        if (cmd.user.guild_permissions.administrator == True):
            initiationtime = datetime.now()
            await cmd.send('Nuking messages...')
            await asyncio.sleep(2)
            await cmd.channel.purge(limit=1000, bulk=True)
            notice = nextcord.Embed(
                title='Pinky has completed a message purge', color=0xD179F1)
            notice.add_field(name=initiationtime.strftime("%d/%m/%Y %H:%M:%S"),
                             value='Initiated by %s' % cmd.user)
            await cmd.channel.send(embed=notice)
            return 0  # Returns 0 only if the use of the command is successful

        else:
            await cmd.send(
                'You need admin privileges to use the \"/nuke\" command.',
                ephemeral=True)
            return 1  # Returns 1 for non-admin user attempting command

    except:
        await cmd.send('An error occurred while deleting messages.',
                       ephemeral=True)
        return 2  # Returns 2 only if user is admin and the command still failed


##########################################################
##########################################################


async def coinFlip(
        cmd
):  # Just flips a coin, either heads or tails nothing special
    if (random.randint(0, 1) == 0):
        await cmd.send('Heads')
    else:
        await cmd.send('Tails')


##########################################################
##########################################################


async def announce(
        cmd,
        msg=None,
        embed=None,
        title=None
):  # The bot takes user's desired message and creates an announcement out of it that is then sent by Pinky in the specified channel
    try:
        if (
                cmd.user.guild_permissions.administrator == False
        ):
            await cmd.send('You are not authorized to use this command.',
                           ephemeral=True)
            return 1

        finalembed = None
        if (embed != None or title != None):
            finalembed = nextcord.Embed(title=title, description=embed, color=0xD179F1)

        await cmd.channel.send(content=msg, embed=finalembed)
        await cmd.send('Message sent successfully.', ephemeral=True)
        return 0

    except:
        await cmd.send(
            'Something went wrong with your command. Please try again.',
            ephemeral=True)
        return 2


##########################################################
##########################################################


async def addreactionrole(
        cmd, temproles, tempemojis, target
):  # Takes a specified message and creates reaction role(s) for it, both target and command must be in same channel, works in conjunction with giverole and removerole
    if (cmd.user.guild_permissions.administrator == False
    ):  # Only admins can make reaction roles
        await cmd.send('You are not authorized to use this command.',
                       ephemeral=True)
        return 1

    try:
        target = await cmd.channel.fetch_message(target)
    except:
        await cmd.send(
            'Message not found. Please enter a valid message ID and execute the command in the same channel.',
            ephemeral=True)
        return 5

    try:

        temproles = temproles.split(' ')

        roles = []
        emojis = []

        for role in temproles:  # Stores roles in list, emojis in separate list
            if (role != None):
                roles.append(role)
        for emoji in tempemojis:
            if (emoji != None and emoji != ' '):
                emojis.append(emoji)

        if (len(roles) == 0 or len(emojis) == 0
        ):  # There must be at least one pair of a role and an emoji
            await cmd.send(
                'There must be at least one role and one emoji provided. Please try again.', ephemeral=True
            )
            return 3

        if (len(roles) !=
                len(emojis)):  # Roles and emojis must have a 1:1 ratio
            await cmd.send(
                'The number of roles listed must equal the number of emojis listed. Please try again.',
                ephemeral=True)

            return 4

        for n in range(
                len(roles)
        ):  # Ascertain the ID of each role being made into a reaction role
            try:
                roles[n] = int(roles[n])
            except:
                roles[n] = int(roles[n][3:-1])

        for n in range(
                len(emojis)
        ):  # React to target message with each given emoji (in order of appearance in command)
            await target.add_reaction(emojis[n])

        #with open('data.json', 'r') as datafile:
        #    data = json.load(datafile)
        #with open('data.json', 'w') as datafile:
        #    data[str(target.id)] = [roles, emojis]
        #    json.dump(data, datafile)

        sqlite_interface.setEntry(target.id, roles, emojis)

        await cmd.send('Reaction roles added!', ephemeral=True)
        return 0

    except:
        await cmd.send(
            'Something went wrong with your command. Please try again.',
            ephemeral=True)
        return 2


##########################################################
##########################################################


async def giverole(
        reaction,
        client
):  # Target user is given specified role
    try:
        #messagedata = None
        #with open('data.json', 'r') as datafile:
        #    data = json.load(datafile)
        #    messagedata = data[str(reaction.message_id)]  # Each key references two lists

        rrData = sqlite_interface.getEntry(reaction.message_id)  # Retrieve [roles, emojis] from database
        roles = rrData[0]
        emojis = rrData[1]

        #emojis = []

        #for x in messagedata[
        #    1]:  # Converts second list (contains emojis) to more readable form
        #    emojis.append(x)

        for x in range(len(
                emojis)):  # Compares each emoji in list to emoji in reaction

            if (str(emojis[x]) == str(reaction.emoji)):
                server = await client.fetch_guild(reaction.guild_id)
                role = server.get_role(
                    #messagedata[0][x]
                    roles[x]
                )  # Fetches role object based on role ID

                await reaction.member.add_roles(role,
                                                reason='Reaction role given')

                return True

        return False

    except:
        return False


##########################################################
##########################################################


async def removerole(
        reaction,
        client
):  # Target user's specified role is removed
    try:
        #messagedata = None
        #with open('data.json', 'r') as datafile:
        #    data = json.load(datafile)
        #    messagedata = data[str(reaction.message_id)]

        #emojis = []

        #for x in messagedata[1]:
        #    emojis.append(x)

        rrData = sqlite_interface.getEntry(reaction.message_id)  # Retrieve [roles, emojis] from database
        roles = rrData[0]
        emojis = rrData[1]

        for x in range(len(emojis)):
            if (str(emojis[x]) == str(reaction.emoji)):

                server = await client.fetch_guild(reaction.guild_id)
                role = server.get_role(roles[x])
                reactionmember = await server.fetch_member(reaction.user_id)

                try:
                    await reactionmember.remove_roles(
                        role, reason='Reaction role removed')
                except Exception as inst:
                    print(inst)
                return True

        return False

    except:

        return False


##########################################################
##########################################################


async def help(
        cmd,
        client,
        command=None
):  # When used with no specified command, returns list of commands; if a particular command is specified, the format of the command's proper usage will be given in addition to a description of its operations
    if (command != None):
        specifiedcommand = True
        try:  # Specified command must be in list of commands
            details = ALL_COMMANDS[command]
        except:  # Send error message if requested command is invalid
            await cmd.send(
                'The command \"%s\" does not exist. Please try again.' %
                command)
            await pinkylog(client, '- Unable to process help command, requested command does not exist')
            return
        helpembed = nextcord.Embed(title='**Help - %s**' % command,
                                   color=0xD179F1)
        helpembed.add_field(name='```/%s```' % details[0],
                            value='>>> ```%s```' % details[2])

    else:  # When there is no specified command
        specifiedcommand = False
        helpembed = nextcord.Embed(title='**Help - Pinky**', color=0xD179F1)
        for x in ALL_COMMANDS.keys():
            helpembed.add_field(name='```%s:```' % x,
                                value='>>> ```%s```' % ALL_COMMANDS[x][1])

    await cmd.send(embed=helpembed)

    if (specifiedcommand):  # If command is specified
        await pinkylog(client, '- %s used the help command on %s' %
                       (str(cmd.user), command))
    else:  # If no command is specified
        await pinkylog(client, '- %s used the generic help command' % str(cmd.user))


##########################################################
##########################################################


async def delreactionroles(
        msg
):  # Upon deletion of a message attached to reaction roles, Pinky will clear up room in its database that held necessary data to the facilitation of the roles
    try:
        #with open('data.json', 'r') as datafile:
        #    data = json.load(datafile)
        #with open('data.json', 'w') as datafile:
        #    data.pop(str(msg.message_id))
        #    json.dump(data, datafile)
        #return True
        sqlite_interface.deleteEntry(msg.message_id)
        return True

    except:
        return False

##########################################################
##########################################################
