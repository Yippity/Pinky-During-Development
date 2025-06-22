# Pinky During Development
Codebase for Discord bot Pinky throughout various stages of development for a collegiate capstone project. For an up-to-date version of Pinky, visit https://github.com/Yippity/Pinky

Legacy codebase: earliest version of the code that still exists. Originally developed around 2020-2021, likely had minor changes made since. Each enhancement progressively built upon the legacy codebase.

Enhancement 1: involved converting the legacy code from PyCord to Nextcord. Also introduced the use of slash commands, replacing the command prefix model previously used.

Enhancement 2: inclusion of the language filtration algorithm. Pinky's language filter uses regular expressions that are procedurally built from each phrase contained in a .txt file, allowing for the list of offensive phrases to be expanded upon seamlessly.

Enhancement 3: overhaul of reaction role feature. Converted storage of data necessary to reaction role functionality from JSON format to SQLite. Using a database improves the features speed and scalability greatly.

Final Enhancements: loose collection of further enhancements made beyond the scope of the original project guidelines. Includes password-based protection of Pinky's now encrypted token, audio streaming (WIP), and improvements to the language filtration algorithm
