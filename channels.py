import discord

from discord.ext import commands

# ID владельца

OWNER_ID = 'Ваш айди аккаунта/роли'

# Разрешенные специальные символы

ALLOWED_SYMBOLS = [

    '『', '』', '【', '】', '⌈', '⌋', '⌊', '⌉',

    '《', '》', '〈', '〉', '⸨', '⸩', '〔', '〕',

    '⟦', '⟧', '⦑', '⦒', '⟬', '⟭',

    '➤', '➜', '➠', '➥', '➩', '➪', '➲', '➵', '⮕', '⭆',

    '↠', '↣', '⟶', '⟿', '⭢', '⇨'

]

class ChannelCommands(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

    def is_valid_name(self, name):

        """Проверяет имя на наличие запрещенных символов"""

        return all(char.isalnum() or char in ALLOWED_SYMBOLS or char in [' ', '-', '_'] for char in name)

    async def is_owner_or_has_perms(self, ctx):

        """Проверка: владелец или есть права"""

        if ctx.author.id == OWNER_ID:

            return True

        return discord.utils.get(ctx.author.roles, name="manage_bot_channels") is not None

    @commands.command(name="create_channels")

    async def create_channels(self, ctx, category_id: int, *channel_names):

        """Создает текстовые каналы в категории"""

        if not await self.is_owner_or_has_perms(ctx):

            return await ctx.send("❌ Недостаточно прав!")

        

        category = discord.utils.get(ctx.guild.categories, id=category_id)

        if not category:

            return await ctx.send("❌ Категория не найдена!")

        

        created_channels = []

        for name in channel_names:

            if not self.is_valid_name(name):

                await ctx.send(f"❌ Имя канала содержит запрещенные символы: {name}")

                continue

            

            channel = await category.create_text_channel(name)

            created_channels.append(channel.mention)

        

        if created_channels:

            await ctx.send(f"✅ Созданы каналы: {', '.join(created_channels)}")

    @commands.command(name="create_forum")

    async def create_forum(self, ctx, category_id: int, forum_name: str):

        """Создает форум в категории"""

        if not await self.is_owner_or_has_perms(ctx):

            return await ctx.send("❌ Недостаточно прав!")

        

        if not self.is_valid_name(forum_name):

            return await ctx.send("❌ Имя форума содержит запрещенные символы!")

        

        category = discord.utils.get(ctx.guild.categories, id=category_id)

        if not category:

            return await ctx.send("❌ Категория не найдена!")

        

        forum = await category.create_forum(forum_name)

        await ctx.send(f"✅ Создан форум: {forum.mention}")

    @commands.command(name="create_forum_thread")

    async def create_forum_thread(self, ctx, forum_id: int, thread_name: str):

        """Создает ветку в форуме (без описания) с возможностью прикрепления фото"""

        if not await self.is_owner_or_has_perms(ctx):

            return await ctx.send("❌ Недостаточно прав!")

        

        forum = discord.utils.get(ctx.guild.forums, id=forum_id)

        if not forum:

            return await ctx.send("❌ Форум не найден!")

        

        files = []

        if ctx.message.attachments:

            for attachment in ctx.message.attachments:

                if attachment.filename.lower().endswith(('png', 'jpg', 'jpeg', 'gif')):

                    files.append(await attachment.to_file())

        

        thread = await forum.create_thread(

            name=thread_name,

            content=None,  # Без описания

            files=files

        )

        

        await ctx.send(f"✅ Создана ветка: {thread.thread.mention}")

    @commands.command(name="delete_channel")

    async def delete_channel(self, ctx, channel_name: str):

        """Удаляет канал по названию"""

        if not await self.is_owner_or_has_perms(ctx):

            return await ctx.send("❌ Недостаточно прав!")

        

        channel = discord.utils.get(ctx.guild.channels, name=channel_name)

        if not channel:

            return await ctx.send("❌ Канал не найден!")

        

        await channel.delete()

        await ctx.send(f"✅ Канал `{channel_name}` удален!")

    @commands.command(name="rename_channel")

    async def rename_channel(self, ctx, old_name: str, new_name: str):

        """Переименовывает канал"""

        if not await self.is_owner_or_has_perms(ctx):

            return await ctx.send("❌ Недостаточно прав!")

        

        if not self.is_valid_name(new_name):

            return await ctx.send("❌ Новое имя содержит запрещенные символы!")

        

        channel = discord.utils.get(ctx.guild.channels, name=old_name)

        if not channel:

            return await ctx.send("❌ Канал не найден!")

        

        await channel.edit(name=new_name)

        await ctx.send(f"✅ Канал `{old_name}` переименован в `{new_name}`!")

    @commands.command(name="give_channel_perms")

    @commands.has_permissions(administrator=True)

    async def give_perms(self, ctx, member: discord.Member):

        """Выдает роль с правами на управление командами"""

        role = discord.utils.get(ctx.guild.roles, name="manage_bot_channels")

        if not role:

            role = await ctx.guild.create_role(name="manage_bot_channels")

        

        await member.add_roles(role)

        await ctx.send(f"✅ Пользователь {member.mention} получил права!")

async def setup(bot):

    await bot.add_cog(ChannelCommands(bot))
