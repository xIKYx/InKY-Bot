import discord
import random
import time
from discord.ext import commands
from pytz import timezone

class Information(commands.Cog):

    def __innit__(self, client):
        self.client = client
    
    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot is Online!')
    
    # Commands
    @commands.command()
    async def ping(self, ctx, arg=None):
        """- Check Bots Ping"""
        if arg == "pong":
            return await ctx.send("Congratulation, you just ponged yourself lol")

        else:
            start = time.perf_counter()
            message = await ctx.send("Ping...")
            end = time.perf_counter()
            duration = (end - start) * 1000
            await message.edit(content='Pong! {:.2f}ms'.format(duration))

    @commands.command(aliases=["bi", "about", "info",])
    async def botinfo(self, ctx):
        """- Show bot information."""
        bot_ver = "1.0.0"
        embed = discord.Embed(
            title="About InKY Bot",
            colour=discord.Colour(0xFFFFF0),
            timestamp=ctx.message.created_at,
        )
        embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/783159643126890517/06e9f5496357fc24b6037dc92c159971.webp?size=1024')
        embed.add_field(name="Author", value="IKY#5948")
        embed.add_field(
            name="discord.py",
            value=f"[{discord.__version__}-modified](https://github.com/xIKYx/InKY-Bot)",
        )
        embed.add_field(
            name="About",
            value="**InKY Bot** is an open source bot, "
            + "a fork of [mcbeDiscordBot](https://github.com/AnInternetTroll/mcbeDiscordBot) "
            + "(Steve the Bot) created by [AnInternetTroll](https://github.com/AnInternetTroll), "
            + "and from [ZiRO-Bot](https://github.com/ZiRO-Bot/ziBot) (ziBot) created by "
            + "[null2264](https://github.com/null2264), "
            + f"but rewritten a bit.\n\n**Bot Version**: {bot_ver}",
            inline=False,
        )
        embed.set_footer(
            text=f"Requested by {ctx.message.author.name}#{ctx.message.author.discriminator}"
        )
        await ctx.send(embed=embed)

    @commands.command(aliases=["ui"], usage="[member]")
    async def userinfo(self, ctx, *, user: discord.Member = None):
        """- Show user information."""
        member = user or ctx.message.author

        def stat(x):
            return {
                "offline": "<:status_offline:747799247243575469>",
                "idle": "<:status_idle:747799258316668948>",
                "dnd": "<:status_dnd:747799292592259204>",
                "online": "<:status_online:747799234828435587>",
                "streaming": "<:status_streaming:747799228054765599>",
            }.get(str(x), "None")

        def badge(x):
            return {
                "UserFlags.hypesquad_balance": "<:balance:747802468586356736>",
                "UserFlags.hypesquad_brilliance": "<:brilliance:747802490241810443>",
                "UserFlags.hypesquad_bravery": "<:bravery:747802479533490238>",
                "UserFlags.bug_hunter": "<:bughunter:747802510663745628>",
                "UserFlags.booster": "<:booster:747802502677659668>",
                "UserFlags.hypesquad": "<:hypesquad:747802519085776917>",
                "UserFlags.partner": "<:partner:747802528594526218>",
                "UserFlags.owner": "<:owner:747802537402564758>",
                "UserFlags.staff": "<:stafftools:747802548391379064>",
                "UserFlags.early_supporter": "<:earlysupport:747802555689730150>",
                "UserFlags.verified": "<:verified:747802457798869084>",
                "UserFlags.verified_bot": "<:verified:747802457798869084>",
                "UserFlags.verified_bot_developer": "<:verified_bot_developer:748090768237002792>",
            }.get(x, "🚫")

        def activity(x):
            return {
                "playing": "Playing ",
                "watching": "Watching ",
                "listening": "Listening to ",
                "streaming": "Streaming ",
                "custom": "",
            }.get(x, "None ")

        badges = []
        for x in list(member.public_flags.all()):
            x = str(x)
            if member == ctx.guild.owner:
                badges.append(badge("UserFlags.owner"))
            badges.append(badge(x))

        roles = []
        if member:
            for role in member.roles:
                if role.name != "@everyone":
                    roles.append(role.mention)

        jakarta = timezone("Asia/Jakarta")

        if member:
            status = member.status
            statEmoji = stat(member.status)
        else:
            status = "Unknown"
            statEmoji = "❓"
        embed = discord.Embed(
            description=f"{statEmoji}({status})\n"
            + (
                "<:activity:748091280227041281>"
                + activity(str(member.activity.type).replace("ActivityType.", ""))
                + f"**{member.activity.name}**"
                if member and member.activity
                else ""
            ),
            colour=member.colour if member else discord.Colour(0x000000),
            timestamp=ctx.message.created_at,
        )
        embed.set_author(
            name=f"{member}", icon_url=member.avatar_url
        )
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name="ID", value=member.id)
        embed.add_field(name="Guild name", value=member.display_name)
        embed.add_field(
            name="Badges", value=" ".join(badges) if badges else "No badge."
        )
        embed.add_field(
            name="Created on",
            value=member.created_at.replace(tzinfo=timezone("UTC"))
            .astimezone(jakarta)
            .strftime("%a, %#d %B %Y, %H:%M WIB"),
        )
        embed.add_field(
            name="Joined on",
            value=member.joined_at.replace(tzinfo=timezone("UTC"))
            .astimezone(jakarta)
            .strftime("%a, %#d %B %Y, %H:%M WIB")
            if member
            else "Not a member.",
        )
        if len(", ".join(roles)) <= 1024:
            embed.add_field(
                name=f"Roles ({len(roles)})",
                value=", ".join(roles) or "No roles.",
                inline=False,
            )
        else:
            embed.add_field(name=f"Roles", value=f"{len(roles)}", inline=False)
        embed.set_footer(
            text=f"Requested by {ctx.message.author.name}#{ctx.message.author.discriminator}"
        )
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Information(client))