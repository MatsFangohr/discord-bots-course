# image manipulation?
# run on replit?
import os
import enum
import random
import discord
import datetime
import stundenplan as plan

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

guild_id = 956666111989010533
guild_ids = [guild_id]
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
    add_commands()
    await tree.sync(guild=guild_object)
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


def add_commands():
    for command in [ping, Abstimmung(), farbe, sarkasmus, stundenplan, info, code, projekte, echo, überraschung]:
        tree.add_command(command, guild=guild_object)


@discord.app_commands.command(
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


class Abstimmung(discord.app_commands.Group):
    @discord.app_commands.command(
        name="einfach",
        description="Erstellt eine einfache Abstimmung.",
    )
    @discord.app_commands.describe(frage="frage")
    @discord.app_commands.describe(antworta="antworta")
    @discord.app_commands.describe(antwortb="antwortb")
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

    @discord.app_commands.command(
        name="ja_nein",
        description="Erstellt eine Ja / Nein Abstimmung.",
    )
    @discord.app_commands.describe(frage="frage")
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


@discord.app_commands.command(
    name="farbe",
    description="Ändert deine Farbrolle auf Discord.",
)
@discord.app_commands.describe(farbe="Deine gewünschte Farbe.")
async def farbe(interaction: discord.Interaction, farbe: Farbe):
    color_roles = [
        964163492317917255,
        964164753515753522,
        964164766895575041,
        964164788731146261,
        964164805659349033,
        964164826370826261,
        964164840077791323,
        964164867680505856,
        964164880305385503,
    ]
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
    for role in color_roles:
        if role in [r.id for r in member.roles] and role != farbe_int:
            await member.remove_roles(guild.get_role(role))
    if farbe_int != 0:
        await interaction.response.send_message("Neue Farbe erfolgreich ausgewählt.")
        print(f"{format_name(interaction.user)} hat nun die Farbe {farbe.name}.")
    else:
        await interaction.response.send_message("Farbe erfolgreich entfernt.")
        print(f"{format_name(interaction.user)} hat nun keine Farbe.")


@discord.app_commands.command(
    name="sarkasmus", description="Macht den angegebenen Text 'sArKasTiSCh'."
)
@discord.app_commands.describe(text="Der zu verändernde Text.")
async def sarkasmus(interaction: discord.Interaction, text: str):
    await interaction.response.send_message(
        "".join([random.choice([char.upper(), char.lower()]) for char in list(text)])
    )
    print(
        f"""{format_name(interaction.user)} hat den Text '{text if len(text) <= 30 else f"{text[:30]}..."}' sarkastisch machen lassen."""
    )


@discord.app_commands.command(
    name="stundenplan", description="Zeigt Mats' Studenplan an."
)
async def stundenplan(interaction: discord.Interaction):
    await interaction.response.send_message(plan.mats_stundenplan.show_week())
    print("Stundenplan angezeigt.")


@discord.app_commands.command(name="münzwurf", description="Würft eine Münze.")
async def münzwurf(interaction: discord.Interaction):
    result = random.choice(["Kopf!", "Zahl!"])
    await interaction.response.send_message(result)
    print(f"{format_name(interaction.user)} hat eine Münze geworfen, es war {result}.")


@discord.app_commands.command(
    name="info", description="Gibt dir verschiedene Informationen über einen Benutzer."
)
@discord.app_commands.describe(member="Nutzer")
async def info(interaction: discord.Interaction, member: discord.Member):
    embed = discord.Embed(
        title=member.name,
        description=f"[Profilbild]({get_avatar_url(member)})",
        color=discord.Color.random(),
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
    await interaction.response.send_message("", embed=embed)
    print(f"Info-Nachricht für {format_name(member)} abgeschickt.")


@discord.app_commands.command(
    name="code", description="Gibt dir einen Link zu meinem Code!"
)
async def code(interaction: discord.Interaction):
    await interaction.response.send_message(
        "https://github.com/MatsFangohr/discord-bots-course/tree/main/beispiel-bot"
    )


@discord.app_commands.command(
    name="projekte", description="Andere Projeckte, an denen ich gearbeitet habe."
)
async def projekte(interaction: discord.Interaction):
    await interaction.response.send_message(
        "<https://github.com/MatsFangohr/discord-bots-course> - Ein Kurs, um in einer Woche das Programmieren von Discord-Bots zu lernen.\n<https://github.com/Anuken/Mindustry> - Ein 2d open-world tower defence Spiel."
    )


@discord.app_commands.command(
    name="echo", description="Bringt den Bot dazu, etwas zu sagen."
)
@discord.app_commands.describe(channel="Welcher Kanal?")
@discord.app_commands.describe(message="Welche Nachricht")
async def echo(
    interaction: discord.Interaction, channel: discord.TextChannel, message: str
):
    await channel.send(message)
    await interaction.response.send_message(
        "Fertig!",
        ephemeral=True
    )


client.run(os.getenv("TOKEN"))
