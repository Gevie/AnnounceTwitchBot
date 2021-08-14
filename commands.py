import discord
from discord.ext import commands
from whitelist import JsonDatasourceHandler


class CommandsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.datasource = JsonDatasourceHandler()

    @commands.command(name='add_streamer', pass_context=True)
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def add_streamer(self, ctx, user: discord.User, username: str, *roles: discord.Role):
        try:
            self.datasource.add_streamer(user.id, username)
        except ValueError:
            await ctx.send(f"{user.mention} is already in the approved streamer list")
            return

        await ctx.send(f"{user.mention} has been added to the whitelist for twitch.tv/{username}")

        for role in roles:
            try:
                self.datasource.add_role_to_streamer(user.id, role.id, role.name)
            except ValueError:
                await ctx.send(f"{role.mention} is already added to {user.mention} for twitch.tv/{username}")
                continue

            await ctx.send(f"{role.mention} has been added to {user.mention} for twitch.tv/{username}")


def setup(bot):
    bot.add_cog(CommandsCog(bot))