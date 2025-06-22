# Module for playing audio in Discord voice chats using .wav files
from typing import Optional

import nextcord
import os

##########################################################
##########################################################


async def joinvc(cmd: nextcord.Interaction):  # Join VC with command's user
    if cmd.user.voice:  # Check if user is in voice channel, join and return true; else, return false
        # connection = await cmd.user.voice.channel.connect()
        # return (True, connection)
        await cmd.user.voice.channel.connect()
        return True
    else:
        return False


##########################################################
##########################################################


async def leavevc(cmd: nextcord.Interaction, vcStatus: Optional[nextcord.VoiceClient]):  # Leave VC
    if vcStatus:
        await vcStatus.disconnect()
        return True
    else:  # If not in VC, do nothing
        return False


##########################################################
##########################################################


async def playwav(cmd: nextcord.Interaction, name: str):  # Plays named .wav if available
    currentDir = os.getcwd()
    wavName = name + ".wav"
    filepath = os.path.join(currentDir, "wavs", wavName)
    voiceClient = cmd.guild.voice_client

    if not voiceClient:
        return [False, "Cannot play music before joining a voice channel. Please join a VC and then use /joinvc."]

    elif not os.path.exists(filepath):  # Check if .wav exists
        return [False, "My library does not have a song by that name"]

    if voiceClient.is_playing:  # Stop any current audio
        voiceClient.stop()

    try:
        voiceClient.play(nextcord.FFmpegPCMAudio(source=filepath))  # Begin playing track
        return [True, "Streaming \"%s\" in %s" % (name, cmd.channel.name)]
    except Exception as e:
        print("Playback error: %s"%e)
        return [False]


##########################################################
##########################################################


async def audiostop(cmd: nextcord.Interaction):
    voiceClient = cmd.guild.voice_client
    if voiceClient is None:
        return False
    elif voiceClient.is_playing():  # Stop any current audio
        voiceClient.stop()
        return True
    else:
        return False