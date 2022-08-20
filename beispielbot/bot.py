# image manipulation?
import os
import enum
import random
import datetime
import stundenplan as plan

import discord
from discord import app_commands

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)
client.tree = app_commands.CommandTree(client)

guild_id = 956666111989010533
guild_object = discord.Object(id=guild_id)


def format_name(member: discord.Member):
    if member.nick is None:
        return member.name
    else:
        return f"{member.nick} ({member.name})"


def get_avatar_url(member: discord.Member):
    try:
        return member.avatar.url
    except AttributeError:
        return "https://cdn.discordapp.com/embed/avatars/0.png"


@client.event
async def on_ready():
    await client.tree.sync(guild=guild_object)
    print(f"Eingeloggt als {client.user}.")


@client.event
async def on_member_join(member: discord.Member):
    embed = discord.Embed(
        title=f"Hallo {member.name}!",
        description="Willkommen auf meinem Beispielserver für die Projektwoche!",
        color=discord.Color.random(),
    )
    embed.set_author(name=member.guild.name, icon_url=member.guild.icon.url)
    embed.set_thumbnail(url=get_avatar_url(member))
    embed.timestamp = datetime.datetime.utcnow()
    await client.get_channel(963592742049546280).send("", embed=embed)
    print(f"Welcome-Message für {member.name} abgeschickt!")


@client.event
async def setup_hook():
    client.tree.copy_global_to(guild=guild_object)
    await client.tree.sync(guild=guild_object)


@client.tree.command(
    name="ping",
    description="Gibt die Latenz zwischen Discord und dem Bot an.",
)
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(
        f"Pong! Die Latenz beträgt ~{round(client.latency * 1000)}ms."
    )
    print(
        f"Die Latenz wurde von {format_name(interaction.user)} abgefragt und beträgt ~{round(client.latency * 1000)}ms."
    )


class Abstimmung(app_commands.Group):
    @client.tree.command(
        name="einfach",
        description="Erstellt eine einfache Abstimmung.",
    )
    @app_commands.describe(frage="frage")
    @app_commands.describe(antworta="antworta")
    @app_commands.describe(antwortb="antwortb")
    async def einfach(
        self, interaction: discord.Interaction, frage: str, antworta: str, antwortb: str
    ):
        await interaction.response.send_message(
            f"<@{interaction.user.id}> fragt: {frage}\n\n:one:: {antworta}\n:two:: {antwortb}"
        )
        message = await interaction.original_message()
        await message.add_reaction("1️⃣")
        await message.add_reaction("2️⃣")
        print(
            f"Abstimmung '{frage}' (einfach) von {format_name(interaction.user)} erstellt."
        )

    @client.tree.command(
        name="ja_nein",
        description="Erstellt eine Ja / Nein Abstimmung.",
    )
    @app_commands.describe(frage="frage")
    async def abstimmung(self, interaction: discord.Interaction, frage: str):
        await interaction.response.send_message(
            f"<@{interaction.user.id}> fragt: {frage}"
        )
        message = await interaction.original_message()
        await message.add_reaction("✅")
        await message.add_reaction("❌")
        print(
            f"Abstimmung '{frage}' (ja / nein) von {format_name(interaction.user)} erstellt."
        )


class Farbe(enum.Enum):
    rot = "964163492317917255"
    orange = "964164753515753522"
    gelb = "964164766895575041"
    grün = "964164788731146261"
    dunkelgrün = "964164805659349033"
    blau = "964164826370826261"
    dunkelblau = "964164840077791323"
    pink = "964164867680505856"
    lila = "964164880305385503"
    keine = "0"


@client.tree.command(
    name="farbe",
    description="Ändert deine Farbrolle auf Discord.",
)
@app_commands.describe(farbe="Deine gewünschte Farbe.")
async def farbe(interaction: discord.Interaction, farbe: Farbe):
    farbe_int = int(farbe.value)
    guild = discord.utils.get(client.guilds, name="Projektwoche: Discord Bots")
    member = guild.get_member(interaction.user.id)
    for role in member.roles:
        if role.id == farbe_int:
            await interaction.response.send_message("Du hast die Farbe schon!")
            print(
                f"{format_name(interaction.user)} hat keine neue Farbe erhalten, da er / sie die Farbe {farbe.name} schon hat!"
            )
            return
    if farbe_int != 0:
        await member.add_roles(discord.utils.get(guild.roles, id=farbe_int))
    for role in [int(role_str.value) for role_str in Farbe]:
        if role in [r.id for r in member.roles] and role != farbe_int:
            await member.remove_roles(guild.get_role(role))
    if farbe_int != 0:
        await interaction.response.send_message("Neue Farbe erfolgreich ausgewählt.")
        print(f"{format_name(interaction.user)} hat nun die Farbe {farbe.name}.")
    else:
        await interaction.response.send_message("Farbe erfolgreich entfernt.")
        print(f"{format_name(interaction.user)} hat nun keine Farbe.")


@client.tree.command(
    name="sarkasmus", description="Macht den angegebenen Text 'sArKasTiSCh'."
)
@app_commands.describe(text="Der zu verändernde Text.")
async def sarkasmus(interaction: discord.Interaction, text: str):
    await interaction.response.send_message(
        "".join([random.choice([char.upper(), char.lower()]) for char in list(text)])
    )
    print(
        f"""{format_name(interaction.user)} hat den Text '{text if len(text) <= 30 else f"{text[:30]}..."}' sarkastisch machen lassen."""
    )


@client.tree.command(name="stundenplan", description="Zeigt Mats' Studenplan an.")
async def stundenplan(interaction: discord.Interaction):
    await interaction.response.send_message(plan.mats_stundenplan.show_week())
    print("Stundenplan angezeigt.")


@client.tree.command(name="münzwurf", description="Würft eine Münze.")
async def münzwurf(interaction: discord.Interaction):
    result = random.choice(["Kopf!", "Zahl!"])
    await interaction.response.send_message(result)
    print(f"{format_name(interaction.user)} hat eine Münze geworfen, es war {result}.")


async def get_user_info_embed(member: discord.Member) -> discord.Embed:
    embed = discord.Embed(
        title=member.name,
        description=f"[Profilbild]({get_avatar_url(member)})",
        color=member.roles[-1].color,
    )
    embed.set_author(name=member.guild.name, icon_url=member.guild.icon.url)
    embed.set_thumbnail(url=get_avatar_url(member))

    embed.add_field(
        name="Benutzer erstellt",
        value=f"<t:{round(member.created_at.timestamp())}>\n<t:{round(member.created_at.timestamp())}:R>",
        inline=True,
    )
    embed.add_field(
        name="Benutzer beigetreten",
        value=f"<t:{round(member.joined_at.timestamp())}>\n<t:{round(member.joined_at.timestamp())}:R>",
    )
    embed.set_footer(text=member.id)

    embed.timestamp = embed.timestamp = datetime.datetime.utcnow()
    return embed


@client.tree.context_menu(name="Info")
async def info(interaction: discord.Interaction, member: discord.Member):
    embed = await get_user_info_embed(member)
    await interaction.response.send_message("", embed=embed)
    print(f"Info-Nachricht für {format_name(member)} abgeschickt.")


@client.tree.command(name="code", description="Gibt dir einen Link zu meinem Code!")
async def code(interaction: discord.Interaction):
    await interaction.response.send_message(
        "https://github.com/MatsFangohr/discord-bots-course/tree/main/beispielbot"
    )


@client.tree.command(
    name="projekte", description="Andere Projeckte, an denen ich gearbeitet habe."
)
async def projekte(interaction: discord.Interaction):
    await interaction.response.send_message(
        "<https://github.com/MatsFangohr/discord-bots-course> - Ein Kurs, um in einer Woche das Programmieren von Discord-Bots zu lernen.\n<https://github.com/Anuken/Mindustry> - Ein 2d open-world tower defence Spiel.\nhttps://store.steampowered.com/app/1318690/shapez - Ein Automationsspiel auf Steam."
    )


@client.tree.command(name="echo", description="Bringt den Bot dazu, etwas zu sagen.")
@app_commands.describe(channel="Welcher Kanal?")
@app_commands.describe(message="Welche Nachricht")
async def echo(
    interaction: discord.Interaction, channel: discord.TextChannel, message: str
):
    await channel.send(message)
    await interaction.response.send_message("Fertig!", ephemeral=True)


@client.tree.command(name="würfel", description="Wirft eine Anzahl n-seitiger Würfel.")
@app_commands.describe(anzahl="Die Anzahl der Würfel.")
@app_commands.describe(seiten="Wie viele Seiten jeder Würfel hat.")
async def würfel(
    interaction: discord.Interaction,
    anzahl: app_commands.Range[int, 1, 300],
    seiten: app_commands.Range[int, 1, 1000],
):
    results = [random.randint(1, seiten) for _ in range(anzahl)]
    await interaction.response.send_message(
        " + ".join([str(r) for r in results]) + " = " + str(sum(results))
    )


@client.tree.command(name="hallo")
async def hallo(interaction: discord.Interaction):
    """Sagt Hallo!"""
    await interaction.response.send_message(f"Hallo {interaction.user.nick}!")


client.run(os.getenv("TOKEN"))
