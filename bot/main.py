import guilded
import random
from guilded.ext import commands
from dotenv import load_dotenv
from os import getenv
from scrape_nikke import Nikke
from novel_api import generate_image
from upload_image import upload_image

load_dotenv()

bot = commands.Bot(command_prefix="!", user_id=getenv("BOT_USER_ID"))


@bot.event
async def on_ready():
    print("Ready!")


@bot.event
async def on_message(message: guilded.Message):
    if message.author.bot:
        return

    if bot.user.id in map(lambda x: x.id, message.mentions):
        possibilites = [
            "Hi!",
            "Hello!",
            "Hey!",
            "Hi, how are you?",
            "Hello, how are you?",
        ]

        await message.channel.send(
            f"{random.choice(possibilites)}!", reply_to=[message]
        )

    await bot.process_commands(message)


@bot.command()
async def generate(ctx: commands.Context, size: str = "small", *input: str):
    if size.lower() not in ["small", "large"]:
        await ctx.send("Invalid size! Please use `small` or `large`.")
        return

    print(f"Generating image for {ctx.author.name} with input: {input}")

    message = await ctx.send("Generating image, please wait...")

    image = generate_image(" ".join(input), size.lower() == "large")
    if image:
        upload = upload_image(image)
        if upload:
            embed = guilded.Embed()
            embed.set_image(url=upload)
            embed.color = 0x00FF00

            await message.edit(embed=embed)
    else:
        await message.edit(content="Something went wrong! Please try again later.")


@bot.command()
async def roleplay(ctx: commands.Context, key: str, nikke_name: str, *input: str):
    if (key := key.lower()) not in ["perfil", "rp"]:
        await ctx.send("Invalid key! Please use `perfil` or `rp`.")
        return

    character = Nikke.from_name(nikke_name)
    if character is None:
        await ctx.send("Invalid Nikke name or something went wrong!")
        return

    embed = guilded.Embed()
    embed.title = character.name
    embed.color = random.randint(0, 16777215)
    if key == "perfil":
        # limit to 1024 characters, stop in the last space or newline
        if len(character.profile) > 1024:
            character.profile = character.profile[:1024].rsplit(maxsplit=1)[0]

        embed.add_field(name="Perfil", value=character.profile, inline=False)
        embed.set_footer(text=character.description)
        embed.description = character.backstory
        embed.set_image(url=character.image)
    elif key == "rp":
        embed.description = ctx.message.content.replace(
            f"!roleplay {key} {nikke_name}", ""
        )
        embed.set_thumbnail(url=character.portrait)
        await ctx.message.delete()

    await ctx.send(embed=embed)


bot.run(getenv("BOT_TOKEN"))
