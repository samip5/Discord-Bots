import discord

print(f'API Version: {discord.__version__}')
if(discord.__version__ == "1.0.0a"):
    print(f'We are using rewrite branch.')
else:
    print(f'We are not using rewrite branch.')
