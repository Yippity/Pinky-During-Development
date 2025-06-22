# Pinky#5049's source code
# Developed solely by Yippity#2030 on Discord

import nextcord
from typing import Optional
import botmainlib as bot  # Bot-specific functions
from cmd_master_list import ALL_COMMANDS
import offensive_lang_detect


client = nextcord.Client(intents=nextcord.Intents.all())  # Client connection to Discord
LANG_FILTER_FILEPATH = "lang_filter.txt"
LANG_FILTER_PATTERNS = offensive_lang_detect.fileToReference(LANG_FILTER_FILEPATH)


@client.event
async def on_ready():  # Everything in on_ready is executed each time Pinky comes online properly
    await bot.pinkylog(client, 'Log:\n\n- Logged in as {0.user}'.format(client))
    act = nextcord.Activity(type=nextcord.ActivityType.listening, name="the screams of the damned")
    await client.change_presence(status=nextcord.Status.online, activity=act)


@client.slash_command(description=ALL_COMMANDS.get('quote')[1], force_global=True,
                      dm_permission=True)  # Sends inspirational quote; Disclaimer: I do not claim to own any of these quotes, nor do I personally endorse any quote or its author that a user may come across when using this command
async def quote(interaction: nextcord.Interaction):
    await interaction.response.send_message(embed=bot.getQuote())
    await bot.pinkylog(client, '- Quote generated and sent')


##########################################################

@client.slash_command(dm_permission=True, description=ALL_COMMANDS.get('pfp')[1],
                      force_global=True)  # Sends a mentioned user's PFP
async def pfp(
    cmd: nextcord.Interaction,
    member: Optional[nextcord.Mentionable] = nextcord.SlashOption(required=True, choices=ALL_COMMANDS.keys(),
                                                                  description='Member whose PFP you wish to acquire')
):
    await bot.pfpSteal(client, cmd, member)
    await bot.pinkylog(client, '- Profile picture steal executed')


##########################################################

@client.slash_command(dm_permission=True, description=ALL_COMMANDS.get('reactionrole')[1],
                      force_global=True)  # Creates reaction roles on given message
async def reactionrole(
        cmd: nextcord.Interaction,
        roles: Optional[str] = nextcord.SlashOption(required=True,
                                                    description='All roles that will be assigned through reactions (in order)'),
        reactions: Optional[str] = nextcord.SlashOption(required=True,
                                                        description='All emojis that will be used for reaction roles (in order)'),
        message_id: Optional[str] = nextcord.SlashOption(required=True,
                                                         description='ID of message that reaction roles will be added to')
):
    await bot.addreactionrole(cmd, roles, reactions, message_id)
    await bot.pinkylog(client, '- Reaction role creation executed')


##########################################################

@client.slash_command(dm_permission=True, description=ALL_COMMANDS.get('announce')[1],
                      force_global=True)  # Sends message as if originating from Pinky
async def announce(
        cmd: nextcord.Interaction,
        msg: Optional[str] = nextcord.SlashOption(required=False, description='Message for Pinky to send'),
        embed: Optional[str] = nextcord.SlashOption(required=False, description='Message for Pinky to embed'),
        title: Optional[str] = nextcord.SlashOption(required=False, description='Title of embed')
):
    if ((msg == None or msg == '') and (embed == None or embed == '') and (title == None or title == '')):
        await cmd.send('Message cannot be empty.', ephemeral=True)
        return
    result = await bot.announce(cmd, msg=msg, embed=embed, title=title)
    if (result == 0):
        await bot.pinkylog(client, '- Announcement made successfully')
    elif (result == 1):
        await bot.pinkylog(client, '- Announcement failed, user is not authorized to use this command')
    else:
        await bot.pinkylog(client, '- Announcement failed, an error occurred')


##########################################################

@client.slash_command(dm_permission=True, description=ALL_COMMANDS.get('flipcoin')[1], force_global=True)
async def flipcoin(
        cmd: nextcord.Interaction
):
    await bot.coinFlip(cmd)
    await bot.pinkylog(client, '- Coin flipped')


##########################################################
@client.slash_command(dm_permission=True, description=ALL_COMMANDS.get('nuke')[1], force_global=True)
async def nuke(
        cmd: nextcord.Interaction
):  # Erase all (kinda) messages in given channel (only if user is admin); Warning: can be a little slow, and cannot be undone
    clearresult = await bot.nukeChannel(cmd)
    if (clearresult == 1):
        await bot.pinkylog(client, '- Request to nuke messages in %s denied' % str(cmd.channel))
    elif (clearresult == 0):
        await bot.pinkylog(client, '- Messages nuked in #%s' % str(cmd.channel))
    else:
        await bot.pinkylog(client, '- An error occurred during message purge in %s' % str(cmd.channel))


##########################################################

@client.slash_command(dm_permission=True, description='Access full list of Pinky\'s commands',
                      force_global=True)  # Gives list of all commands and brief overview of each one if no particular command is specified
async def help(
        interaction: nextcord.Interaction,
        command: Optional[str] = nextcord.SlashOption(required=False, choices=ALL_COMMANDS.keys(),
                                                      description='Find more details on a specific command. Sends command list if left empty.')
):
    if (command != None):
        await bot.help(interaction, client, command=command)
    else:
        await bot.help(interaction, client)


##########################################################

@client.slash_command(description='Change target user for Pinky\'s DMs.', guild_ids=[
    None])  # Enables Pinky to DM specific user; currently beyond the intended scope of this project
async def dmuser(
        interaction: nextcord.Interaction,
        id: Optional[str] = nextcord.SlashOption(required=True, description='Target user\'s ID.')
):
    try:
        target = await client.fetch_user(int(id))
        with open('target.txt', 'w') as file:
            file.write(id)
            await interaction.send("Target user set to %s" % str(target))
    except:
        await interaction.send('Target ID is invalid.')


##########################################################

@client.event
async def on_message(msg):
    if (msg.author.bot):  # If msg is from a bot, including Pinky itself, ignore it
        return
    elif (offensive_lang_detect.containsOffensiveLanguage(msg.content, LANG_FILTER_PATTERNS)): # Language filter call
        try:
            await msg.delete()
            response = await msg.channel.send('Your message was deleted because it triggered an offensive language filter.')
            await response.delete(delay=3)
            await bot.pinkylog(client, '- Message in channel %s from %s deleted after triggering language filter' % (msg.channel, msg.author))
        except:
            await bot.pinkylog(client, '- Message in channel %s from %s triggered language filter, but could not be deleted' % (msg.channel, msg.author))
    elif (msg.channel.id == None): # This specific elif is beyond the scope of this project, enables Pinky to send DMs by forwarding my messages from specific channel
        with open('target.txt', 'r') as file:
            target_id = int(file.read())
            try:
                target = await client.fetch_user(target_id)
            except:
                await msg.channel.send(
                    'User with entered ID could not be found. Either the user with the given ID does not exist or has deleted their account.')
            try:
                await target.send(msg.content)
                await bot.pinkylog(client, '- Message sent to %s' % str(target))
            except:
                await msg.channel.send(
                    'Message failed to send to %s. They likely do not share a server with me.' % target)
    if (str(msg.channel.type) == 'private'): # For handling DMs to Pinky and forwarding them to another channel, intended for interactions with friends and beyond the scope of this project
        await bot.pinkylog(client, '- Message received in DMs')
        embed = nextcord.Embed(title='**%s**' % str(msg.author), color=0xD179F1)
        if (msg.content == ''):
            embed.add_field(name='*No string to display.*', value='Message likely contains inaccessible attachments.')
        else:
            embed.add_field(name='*Full message:*', value='%s' % msg.content)
        chan = await client.fetch_channel(None)
        await chan.send(embed=embed)


##########################################################
##########################################################
##########################################################

# Reaction handling

##########################################################
##########################################################
##########################################################

@client.event  # Reaction roles!
async def on_raw_reaction_add(reaction):
    if (reaction.member.bot):  # This if statement prevents Pinky from giving bots, including itself, reaction roles
        return

    if (await bot.giverole(reaction, client) == True):
        await bot.pinkylog(client, '- Gave reaction role to %s' % str(await client.fetch_user(reaction.user_id)))
    else:
        await bot.pinkylog(client, '- %s has made an edit to reactions on a message; no actions taken' % str(
            await client.fetch_user(reaction.user_id)))


@client.event  # Remove reaction role when user removes their reaction emoji from the message
async def on_raw_reaction_remove(reaction):
    if (await bot.removerole(reaction, client) == True):
        await bot.pinkylog(client, '- Removed reaction role from %s' % str(await client.fetch_user(reaction.user_id)))
    else:
        await bot.pinkylog(client, '- %s has made an edit to reactions on a message; no actions taken' % str(
            await client.fetch_user(reaction.user_id)))


@client.event  # Deletes data associated with any reaction role message that is deleted
async def on_raw_message_delete(msg):
    if (await bot.delreactionroles(msg)):
        await bot.pinkylog(client, '- Reaction role data associated with message #%i has been purged' % msg.message_id)


# Will implement a slightly more secure method of accessing the bot at later date; provided the host system is not hacked, the token is safe for now
with open('token.txt', 'r') as token:
    client.run(token.read())
