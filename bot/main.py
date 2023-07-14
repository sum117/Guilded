import guilded
import random
from guilded.ext import commands
from dotenv import load_dotenv
from os import getenv
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


@bot.command(name="generate")
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


bot.run(getenv("BOT_TOKEN"))
