import discord
from discord.ext import commands
from discord.utils import get
from streamer import StreamerMapper
from whitelist import JsonDatasourceHandler, NotFoundException


class CommandsCog(commands.Cog):
    """
    Commands which enable an admin to maintain the streamer whitelist
    """

    def __init__(self, bot):
        """
        Initialize the command cog

        Args:
            bot: The discord bot
        """
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
    async def remove_streamer(self, ctx, user: discord.User) -> None:
        """
        Remove a streamer from the datasource / whitelist

        Args:
            ctx: Represents the :class:`.Context`
            user (discord.User): The user to remove

        Returns:
            None
        """

        try:
            self.datasource.delete_streamer(user.id)
        except NotFoundException:
            await ctx.send(f"{user.mention} cannot be removed as they are not in the streamer list")
            return None

        await ctx.send(f"{user.mention} has been removed from the streamer list.")

    @commands.command(name='add_roles', pass_context=True)
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def add_roles(self, ctx, user: discord.User, *roles: discord.Role) -> None:
        """
        Add roles to an existing streamer

        Args:
            ctx: Represents the :class:`.Context`
            user (discord.User): The streamer
            *roles (discord.Role): A list of discord roles

        Returns:
            None
        """

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
    async def remove_roles(self, ctx, user: discord.User, *roles: discord.Role) -> None:
        """
        Remove roles from a streamer

        Args:
            ctx: Represents the :class:`.Context`
            user (discord.User): The discord user
            *roles (discord.Role): The list of roles to remove

        Returns:
            None
        """

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
    async def list_streamers(self, ctx) -> None:
        """
        Produces a list of all the streamers and their associated roles

        Args:
            ctx: Represents the :class:`.Context`

        Returns:
            None
        """

        streamerMapper = StreamerMapper(self.datasource)
        streamers = streamerMapper.map()

        for idx, streamer in enumerate(streamers):
            user = await self.bot.fetch_user(streamer.id)
            embed = discord.Embed(
                title=streamer.username,
                description=f"You can follow {user.mention} on twitch at https://twitch.tv/{streamer.username}"
            )
            embed.set_thumbnail(url=user.avatar_url)
            role_list = "Subscribe to the following roles to be alerted when they're next live:\n "

            for role in streamer.roles:
                roleTag = get(ctx.guild.roles, id=role.id)
                role_list += f"{roleTag.mention}, "

            embed.add_field(name="Roles", value=role_list)
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(CommandsCog(bot))
