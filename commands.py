import discord
from discord.utils import get
from discord.ext import commands

from streamer import StreamerMapper
from whitelist import JsonDatasourceHandler, NotFoundException


class CommandsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.datasource = JsonDatasourceHandler()

    @commands.command(name='add_streamer', pass_context=True)
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def add_streamer(self, ctx, user: discord.User, username: str, *roles: discord.Role) -> None:
        """
        Adds a streamer to the datasource / whitelist

        Args:
            ctx: Represents the :class:`.Context`
            user (discord.User): The discord user to add
            username (str): The twitch username to add
            *roles (discord.Role): A list of any discord roles to tag

        Returns:
            None
        """

        try:
            self.datasource.add_streamer(user.id, username)
        except ValueError:
            await ctx.send(f"{user.mention} is already in the approved streamer list")
            return None

        await ctx.send(f"{user.mention} has been added to the whitelist for twitch.tv/{username}")

        if len(roles) < 1:
            return None

        for role in roles:
            try:
                self.datasource.add_role_to_streamer(user.id, role.id, role.name)
            except ValueError:
                continue

    @commands.command(name='remove_streamer', pass_context=True)
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def remove_streamer(self, ctx, user: discord.User):
        try:
            self.datasource.delete_streamer(user.id)
        except NotFoundException:
            await ctx.send(f"{user.mention} cannot be removed as they are not in the streamer list")
            return None

        await ctx.send(f"{user.mention} has been removed from the streamer list.")

    @commands.command(name='add_roles', pass_context=True)
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def add_roles(self, ctx, user: discord.User, *roles: discord.Role):
        if len(roles) < 1:
            await ctx.send("You must specify at least one role to add to the streamer")
            return None

        for role in roles:
            try:
                self.datasource.add_role_to_streamer(user.id, role.id, role.name)
            except ValueError:
                continue

    @commands.command(name='remove_roles', pass_context=True)
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def remove_roles(self, ctx, user: discord.User, *roles: discord.Role):
        if len(roles) < 1:
            await ctx.send("You must specify at least one role to remove from the streamer")
            return None

        for role in roles:
            try:
                self.datasource.delete_role_from_streamer(user.id, role.id)
            except ValueError:
                continue

    @commands.command(name='list_streamers', pass_context=True)
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def list_streamers(self, ctx):
        streamerMapper = StreamerMapper()
        streamers = streamerMapper.map()

        for idx, streamer in enumerate(streamers):
            user = await self.bot.fetch_user(streamer.get_id())
            print(user)
            embed = discord.Embed(title=streamer.get_username(), description=f"You can follow {user.mention} on twitch at https://twitch.tv/{streamer.get_username()}")
            embed.set_thumbnail(url=user.avatar_url)

            role_list = "Subscribe to the following roles to be alerted when they're next live:\n "
            for role in streamer.get_roles():
                roleTag = get(ctx.guild.roles, id=role.get_id())
                role_list += f"{roleTag.mention}, "

            embed.add_field(name="Roles", value=role_list)
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(CommandsCog(bot))
