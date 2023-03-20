import os
import discord
from discord_slash import SlashCommand
from discord_slash import SlashCommandOptionType as Option
import re

client = discord.Client(intents=discord.Intents.all())
slash = SlashCommand(client, sync_commands=True)


@client.event
async def on_ready():
	print(f'Logged in as {client.user}')


@slash.slash(name="create_role",
             description="Create a new role with the specified color",
             options=[{
              "name": "color",
              "description": "Hex color code for the role",
              "type": Option.STRING,
              "required": True
             }])
async def create_role_command(ctx, color: str):
	if ctx.author.id != client.owner_id:
		await ctx.send("You are not authorized to use this command.")
		return

	# Check if color is a valid hex color code
	if not re.match(r'^#(?:[0-9a-fA-F]{3}){1,2}$', color):
		await ctx.send('Please enter a valid hex color code (e.g. #FF0000)')
		return

	# Remove the # symbol from the beginning of the hex code
	color = color.lstrip('#')

	# Convert hex code to decimal RGB values
	r = int(color[0:2], 16)
	g = int(color[2:4], 16)
	b = int(color[4:6], 16)

	# Create the role with the specified color
	new_role = await ctx.guild.create_role(name=f"Color {color}",
	                                       color=discord.Color.from_rgb(r, g, b))

	await ctx.send(f"Role {new_role.name} with color {color} created successfully"
	               )


client.run(os.environ['TOKEN'])
