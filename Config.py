# Board Colors
LIGHT_COLOR = (255, 178, 102)
DARK_COLOR = (255, 204, 153)

# How many moves in advance Craig will look
DEPTH = 3   # Anything more than 3 takes forever, dont change this

# Craig's personality
AGRESSIVENESS = 0.1   # Controls how much Craig cares about board management
DEFENSE = 1    # Controls how much Craig cares about piece values
PAWNLOVE = 0.5  # Controls how much Craig cares about isolated, doubled, and blocked pawns
POSITIONING = 0.1   # Controls how much Craig cares about piece positioning