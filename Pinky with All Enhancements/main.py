# Pinky's source code
# Developed solely by @yippity on Discord

# Begin by ensuring all necessary packages are installed
import os
os.system("pip install -r requirements.txt")

import nextcord
from typing import Optional
import botmainlib as bot  # Bot-specific functions
from cmd_master_list import ALL_COMMANDS  # Dictionary containing information on bot commands
import offensive_lang_detect  # Algorithm for filtering offensive language
import aes_handling  # Used for accessing token via password
from getpass import getpass  # Masks password when entered
import audio_player  # Enables streaming .wav audio from host machine in a Discord voice channel

# Important constants:
CLIENT = nextcord.Client(intents=nextcord.Intents.all())  # Client connection to Discord
LANG_FILTER_FILEPATH = "lang_filter.txt"  # Language filter parameters
LANG_FILTER_PATTERNS = offensive_lang_detect.fileToReference(LANG_FILTER_FILEPATH)  # Language filter patterns
TOKEN_FILEPATH = "token.txt"  # File containing Pinky's encrypted auth token




@CLIENT.event
async def on_ready():  # Everything in on_ready is executed each time Pinky comes online properly
    await bot.pinkylog(CLIENT, '\nLog:\n\n- Logged in as {0.user}'.format(CLIENT))
    act = nextcord.Activity(type=nextcord.ActivityType.listening, name="the screams of the damned")
    await CLIENT.change_presence(status=nextcord.Status.online, activity=act)

##########################################################
##########################################################
##########################################################

# Slash command initialization

##########################################################
##########################################################
##########################################################

@CLIENT.slash_command(description=ALL_COMMANDS.get('quote')[1], force_global=True)  # Sends inspirational quote; Disclaimer: I do not claim to own any of these quotes, nor do I personally endorse any quote or its author that a user may come across when using this command
async def quote(interaction: nextcord.Interaction):
    await interaction.response.send_message(embed=bot.getQuote())
    await bot.pinkylog(CLIENT, '- Quote generated and sent')


##########################################################

@CLIENT.slash_command(description=ALL_COMMANDS.get('pfp')[1],
                      force_global=True)  # Sends a mentioned user's PFP
async def pfp(
    cmd: nextcord.Interaction,
    member: Optional[nextcord.Mentionable] = nextcord.SlashOption(required=True, choices=ALL_COMMANDS.keys(),
                                                                  description='Member whose PFP you wish to acquire')
):
    await bot.pfpSteal(CLIENT, cmd, member)
    await bot.pinkylog(CLIENT, '- Profile picture steal executed')


##########################################################

@CLIENT.slash_command(description=ALL_COMMANDS.get('reactionrole')[1],
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
    result = await bot.addreactionrole(cmd, roles, reactions, message_id)
    if (result == 0):
        await bot.pinkylog(CLIENT, '- Reaction role creation executed')
    else:
        await bot.pinkylog(CLIENT, '- Reaction role creation failed, code %i'%result)


##########################################################

@CLIENT.slash_command(description=ALL_COMMANDS.get('announce')[1],
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
        await bot.pinkylog(CLIENT, '- Announcement made successfully')
    elif (result == 1):
        await bot.pinkylog(CLIENT, '- Announcement failed, user is not authorized to use this command')
    else:
        await bot.pinkylog(CLIENT, '- Announcement failed, an error occurred')


##########################################################

@CLIENT.slash_command(description=ALL_COMMANDS.get('flipcoin')[1], force_global=True)
async def flipcoin(
        cmd: nextcord.Interaction
):
    await bot.coinFlip(cmd)
    await bot.pinkylog(CLIENT, '- Coin flipped')


##########################################################

@CLIENT.slash_command(description=ALL_COMMANDS.get('nuke')[1], force_global=True)
async def nuke(
        cmd: nextcord.Interaction
):  # Erase all (kinda) messages in given channel (only if user is admin); Warning: can be a little slow, and cannot be undone
    clearresult = await bot.nukeChannel(cmd)
    if (clearresult == 1):
        await bot.pinkylog(CLIENT, '- Request to nuke messages in %s denied' % str(cmd.channel))
    elif (clearresult == 0):
        await bot.pinkylog(CLIENT, '- Messages nuked in #%s' % str(cmd.channel))
    else:
        await bot.pinkylog(CLIENT, '- An error occurred during message purge in %s' % str(cmd.channel))


##########################################################

@CLIENT.slash_command(description='Access information on all of Pinky\'s commands',
                      force_global=True)  # Gives list of all commands and brief overview of each one if no particular command is specified
async def help(
        interaction: nextcord.Interaction,
        command: Optional[str] = nextcord.SlashOption(required=False, choices=ALL_COMMANDS.keys(),
                                                      description='Find more details on a specific command. Sends command list if left empty.')
):
    if (command != None):
        await bot.help(interaction, CLIENT, command=command)
    else:
        await bot.help(interaction, CLIENT)


##########################################################

@CLIENT.slash_command(description='Change target user for Pinky\'s DMs.', guild_ids=[
    None])  # Enables Pinky to DM specific user; currently beyond the intended scope of this project
async def dmuser(
        interaction: nextcord.Interaction,
        id: Optional[str] = nextcord.SlashOption(required=True, description='Target user\'s ID.')
):
    try:
        target = await CLIENT.fetch_user(int(id))
        with open('target.txt', 'w') as file:
            file.write(id)
            await interaction.send("Target user set to %s" % str(target))
    except:
        await interaction.send('Target ID is invalid.')


##########################################################

@CLIENT.slash_command(description=ALL_COMMANDS.get('joinvc')[1], force_global=True)  # Join same vc as user
async def joinvc(interaction: nextcord.Interaction):
    joined = await audio_player.joinvc(interaction)
    if joined:
        try:
            await interaction.send("Joined voice channel")
        except Exception as e:
            print("Error joinvc executed: %s" % e)
        await bot.pinkylog(CLIENT, '- Joined %s for audio streaming' % interaction.user.name)
    else:
        try:
            await interaction.send("I can only join a voice channel that you are in")
        except Exception as e:
            print("Error when joinvc failed: %s" % e)
        await bot.pinkylog(CLIENT, '- Could not join %s' % interaction.user.name)


##########################################################

@CLIENT.slash_command(description=ALL_COMMANDS.get('leavevc')[1], force_global=True)  # Leave vc if present in one in guild
async def leavevc(interaction: nextcord.Interaction):
    vcStatus = interaction.guild.voice_client
    if await audio_player.leavevc(interaction, vcStatus):
        await interaction.send("Left voice channel")
        await bot.pinkylog(CLIENT, '- Left voice chat in %s' % interaction.guild.name)
    else:
        await interaction.send("I am not in a voice channel")
        await bot.pinkylog(CLIENT, '- Did not leave any voice channel')


##########################################################

@CLIENT.slash_command(description=ALL_COMMANDS.get('audiostop')[1], force_global=True)  # If streaming audio in vc, stop
async def audiostop(interaction: nextcord.Interaction):
    status = await audio_player.audiostop(interaction)
    if status:
        await interaction.send("Stopped streaming audio")
        await bot.pinkylog(CLIENT, '- Stopped streaming audio')
    else:
        await interaction.send("There is no audio stream to stop")
        await bot.pinkylog(CLIENT, '- No audio stream to stop')


##########################################################

@CLIENT.slash_command(description=ALL_COMMANDS.get('playwav')[1], force_global=True)  # Begin streaming selected audio if in vc
async def playwav(interaction: nextcord.Interaction, name: str):
    status = await audio_player.playwav(interaction, name)
    print("- " + status[1])
    if status[0]:
        await interaction.send("Now streaming \"%s\""%name)
        await bot.pinkylog(CLIENT, '- Streaming %s.wav' % name)
    else:
        await interaction.send("My library does not have a song by that name")
        await bot.pinkylog(CLIENT, '- %s does not exist'%(name + ".wav"))


##########################################################
##########################################################
##########################################################

# Standard Discord message processing

##########################################################
##########################################################
##########################################################

@CLIENT.event
async def on_message(msg):
    if (msg.author.bot):  # If msg is from a bot, including Pinky itself, ignore it
        return
    elif (offensive_lang_detect.containsOffensiveLanguage(msg.content, LANG_FILTER_PATTERNS)): # Language filter call
        try:
            await msg.delete()
            await msg.channel.send('<@%i> Your message was deleted because it triggered an offensive language filter.'%msg.author.id)  # Ping user and notify them that they trigger the language filter
            await bot.pinkylog(CLIENT, '- Message in channel %s from %s deleted after triggering language filter' % (msg.channel, msg.author))
        except:
            await bot.pinkylog(CLIENT, '- Message in channel %s from %s triggered language filter, but could not be deleted' % (msg.channel, msg.author))
    elif (msg.channel.id == None): # This specific elif is beyond the scope of this project, enables Pinky to send DMs by forwarding my messages from specific channel
        with open('target.txt', 'r') as file:
            target_id = int(file.read())
            try:
                target = await CLIENT.fetch_user(target_id)
            except:
                await msg.channel.send(
                    'User with entered ID could not be found. Either the user with the given ID does not exist or has deleted their account.')
            try:
                await target.send(msg.content)
                await bot.pinkylog(CLIENT, '- Message sent to %s' % str(target))
            except:
                await msg.channel.send(
                    'Message failed to send to %s. They likely do not share a server with me.' % target)
    if (str(msg.channel.type) == 'private'): # For handling DMs to Pinky and forwarding them to another channel, intended for interactions with friends; this is beyond the scope of this project
        await bot.pinkylog(CLIENT, '- Message received in DMs')
        embed = nextcord.Embed(title='**%s**' % str(msg.author), color=0xD179F1)
        if (msg.content == ''):
            embed.add_field(name='*No string to display.*', value='Message likely contains inaccessible attachments.')
        else:
            embed.add_field(name='*Full message:*', value='%s' % msg.content)
        chan = await CLIENT.fetch_channel(None)
        await chan.send(embed=embed)


##########################################################
##########################################################
##########################################################

# Reaction handling

##########################################################
##########################################################
##########################################################

@CLIENT.event  # Reaction roles!
async def on_raw_reaction_add(reaction):
    if (reaction.member.bot):  # This if statement prevents Pinky from giving bots, including itself, reaction roles
        return

    if (await bot.giverole(reaction, CLIENT) == True):
        await bot.pinkylog(CLIENT, '- Gave reaction role to %s' % str(await CLIENT.fetch_user(reaction.user_id)))
    else:
        await bot.pinkylog(CLIENT, '- %s has made an edit to reactions on a message; no actions taken' % str(
            await CLIENT.fetch_user(reaction.user_id)))


@CLIENT.event  # Remove reaction role when user removes their reaction emoji from the message
async def on_raw_reaction_remove(reaction):
    if (await bot.removerole(reaction, CLIENT) == True):
        await bot.pinkylog(CLIENT, '- Removed reaction role from %s' % str(await CLIENT.fetch_user(reaction.user_id)))
    else:
        await bot.pinkylog(CLIENT, '- %s has made an edit to reactions on a message; no actions taken' % str(
            await CLIENT.fetch_user(reaction.user_id)))


@CLIENT.event  # Deletes data associated with any reaction role message that is deleted
async def on_raw_message_delete(msg):
    if (await bot.delreactionroles(msg)):
        await bot.pinkylog(CLIENT, '- Reaction role data associated with message #%i has been purged' % msg.message_id)


##########################################################
##########################################################
##########################################################

# Client start-up

##########################################################
##########################################################
##########################################################

# Terminal clear is executed reduce screen clutter
# For Windows
if os.name == 'nt':
    os.system('cls')
# For Linux and macOS
else:
    os.system('clear')

# Pinky's token is only decrypted at runtime via a password; the design is such that the token is not stored in
# plaintext and the password from which the AES decryption key is derived is not stored in any form at all


gettingPassword = True
passwordPrompt = "Please enter password to start bot application: "

while gettingPassword:  # If password yields improper auth token, prompt again
    try:
        password = getpass(passwordPrompt)
        key = aes_handling.passwordToKey(password)
        token = aes_handling.getToken(TOKEN_FILEPATH, key)
        CLIENT.run(token)
        gettingPassword = False
    except:
        passwordPrompt = "\nPassword failed, please try again: "
