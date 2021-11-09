"""The commands file of the announce twitch bot module"""

import discord
from discord.ext import commands, tasks
from discord.utils import get
from streamer import StreamerMapper
from twitch_api import TwitchHandler
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

    @tasks.loop(minutes=5)
    async def check_streamers(self):
        """
        Checks twitch streamers every interval to be able to announce go lives

        Returns:
            None
        """
        streamer_mapper = StreamerMapper(self.datasource)
        streamers = streamer_mapper.map()
        twitch_handler = TwitchHandler()
        live_streams = twitch_handler.get_streams(streamers)

        if len(live_streams) > 0:
            streamers = self.mark_as_online(streamers, live_streams)

        self.mark_as_offline(streamers)

    def mark_as_online(self, streamers: list, live_streams: dict) -> list:
        """
        Flags any streamers as live and remove them from the list

        Args:
            streamers (list): A list of Streamer objects
            live_streams (dict): A dict of streams

        Returns:
            List: The remaining streamers
        """
        for index, streamer in enumerate(streamers):
            if streamer.username in live_streams:
                # self.datasource.mark_as_online(streamer)
                print('todo: mark as online')
                streamers.pop(index)

        return streamers

    def mark_as_offline(self, streamers: list) -> None:
        """
        Flags any streamers as offline

        Args:
            streamers (list): A list of streamer objects

        Returns:
            None
        """
        for streamer in streamers:
            if streamer.is_live():
                # self.datasource.mark_as_offline(streamer)
                print('todo: mark as offline')

    @commands.Cog.listener()
    async def on_ready(self):
        """
        Executed on ready, currently used to start the check streamers task

        Returns:
            None
        """

        self.check_streamers.start()

    @commands.command(name='add_streamer', pass_context=True)
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def add_streamer(
        self,
        ctx,
        user: discord.User,
        username: str,
        *roles: discord.Role
    ) -> None:
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

    @commands.command(name='enable_announcements', pass_context=True)
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def enable_announcements(self, ctx) -> None:
        """
        Used to enable the check streamers task

        Args:
            ctx: Represents the :class:`.Context`

        Returns:
            None
        """

        self.check_streamers.start()
        await ctx.send('I am now actively checking twitch streams')

    @commands.command(name='disable_announcements', pass_context=True)
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def disable_announcements(self, ctx) -> None:
        """
        Used to disable the check streamers task

        Args:
            ctx: Represents the :class:`.Context`

        Returns:
            None
        """

        self.check_streamers.stop()
        await ctx.send('I will no longer check twitch streams')

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

        streamer_mapper = StreamerMapper(self.datasource, TwitchHandler())
        streamers = streamer_mapper.map()

        for streamer in streamers:
            user = await self.bot.fetch_user(streamer.id)
            embed = discord.Embed(
                title=streamer.username,
                description=f"You can follow {user.mention} on twitch at"
                            f" https://twitch.tv/{streamer.username}"
            )
            embed.set_thumbnail(url=user.avatar_url)
            role_list = "Subscribe to the following roles to be alerted when they're next live:\n "

            for role in streamer.roles:
                role_tag = get(ctx.guild.roles, id=role.id)
                role_list += f"{role_tag.mention}, "

            embed.add_field(name="Roles", value=role_list)
            await ctx.send(embed=embed)


def setup(bot):
    """Sets up the bot by adding the commands cog"""

    bot.add_cog(CommandsCog(bot))
