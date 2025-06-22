ALL_COMMANDS={ # Dictionary giving specifications on all commands in alphabetical order; format is "'<command name>':['<proper usage format>','<surface-level explanation>','<in-depth explanation>']

  ####################
  ### announce
  ####################

  'announce':['announce [channel] [announcement]','(Administrator only) Sends a custom announcement/message from Pinky','Requires administrator privileges. Pinky will send a custom announcement/message in the channel you mention.The message will include everything after the mentioned channel in your command (e.g. send \"%announce #announcements {Everything inside the braces is the message Pinky will send.}\")'],

  ####################
  ### nuke
  ####################

  'nuke':['nuke','(Administrator only) Bulk deletes messages in channel','Requires administrator privileges. Deletes up to ~1000 messages in the channel it is used in.'],

  ####################
  ### flipcoin
  ####################

  'flipcoin':['flipcoin','Flips a coin','Flips a coin. The result is always either heads or tails.'],

  ####################
  ### pfp
  ####################
  
  'pfp':['pfp [mentioned user(s)]','Steals PFPs lol','Sends a link to the PFP of each user mentioned in the command. Can substitute mentioning a user or users for each user\'s ID number.'],
  
  ####################
  ### quote
  ####################
  
  'quote':['quote','Gives a random quote and cites the author','Gives a random quote and cites the author. The quote is generated at https://zenquotes.io/api/random. Pinky does not endorse any particular author or quote; the command is merely for entertainment.'],

  ####################
  ### reactionrole
  ####################
  
  'reactionrole':['reactionrole [message ID] [role 1] [emoji 1] [role 2] [emoji 2]...','Adds reaction roles to the given message; equivalent to \"rr\" command','First, Pinky identifies what message will have reaction roles added to it by the message\'s ID (you need to have Discord\'s Developer Mode enabled in Settings to obtain this ID). Then, you can add as many or as few roles and their corresponding emojis to that message as you want. Each role must be followed by its corresponding emoji. This command and \"rr\" perform the exact same task.'],

  ####################
  ### rr
  ####################

  'rr':['rr [message ID] [role 1] [emoji 1] [role 2] [emoji 2]...','Adds reaction roles to the given message; equivalent to \"reactionrole\" command','First, Pinky identifies what message will have reaction roles added to it by the message\'s ID (you need to have Discord\'s Developer Mode enabled in Settings to obtain this ID). Then, you can add as many or as few roles and their corresponding emojis to that message as you want. Each role must be followed by its corresponding emoji. This command and \"reactionrole\" perform the exact same task.']
}