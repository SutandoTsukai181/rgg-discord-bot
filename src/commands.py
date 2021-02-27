import os
import sys
import zlib
import zipfile
import random
from time import time as t_now
from io import BytesIO, StringIO
from math import ceil
from json import loads, dumps
from threading import Timer

import requests

from discord import File, utils, DMChannel
from discord.ext import commands

from help import *
from utils import *
from reARMP import reARMP
from gmt_converter.main import convert_from_url_bytes


MEME_CHANNELS = os.environ.get('DISCORD_MEME_CHANNELS')
WORK_CHANNELS = os.environ.get('DISCORD_WORK_CHANNELS')
#CHANNELS = list(set().union(MEME_CHANNELS, WORK_CHANNELS))

BOT_AUTHOR = int(os.environ.get('DISCORD_BOT_AUTHOR'))
WHITELIST = [int(w) for w in os.environ.get('DISCORD_WHITELIST').split(',')]
ignored = []


def revoke_ignore(user, timestamp):
    ignore = (user, timestamp)
    if ignore in ignored:
        ignored.remove(ignore)


def user_to_id(user):
    if user.endswith('>'):
        if user.startswith('<@!') or user.startswith('<&!'):
            user = user[3:-1]
        elif user.startswith('<@') or user.startswith('<&') or user.startswith('<#'):
            user = user[2:-1]
    return int(user)


def in_channel(ctx, channel_list):
    if is_staff(ctx):
        return True
    if ctx.author.id in [u[0] for u in ignored]:
        return False
    if ctx.channel.id in [u[0] for u in ignored]:
        return False
    for e in [u[0] for u in ignored]:
        if e in [role.id for role in ctx.author.roles]:
            return False
    return ctx.channel.name in channel_list


def in_meme_channel(ctx):
    if type(ctx.channel) is DMChannel:
        return True
    return in_channel(ctx, MEME_CHANNELS)


def in_work_channel(ctx):
    if type(ctx.channel) is DMChannel:
        return False
    return in_channel(ctx, WORK_CHANNELS)


def is_staff(ctx):
    if ctx.author.id in WHITELIST:
        return True
    if ctx.channel.id in WHITELIST:
        return True
    if type(ctx.channel) is DMChannel:
        return False
    for e in WHITELIST:
        if e in [role.id for role in ctx.author.roles]:
            return True
    return False


class Staff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(checks=[is_staff], help=HELP['purge'], brief="Removes bot commands and message history.")
    async def purge(self, ctx):
        command_names = [
            f"{self.bot.command_prefix}{c.name}" for c in self.bot.commands]
        user = ''
        check_limit = 100

        def sender(msg):
            return msg.author == ctx.author

        def command_in_channel(msg):
            if msg.author == self.bot.user:
                return True
            for name in command_names:
                if msg.content.startswith(name):
                    return True
            return False

        def command_user_in_channel(msg):
            if msg.author.id == user and msg.author.id == self.bot.user.id:
                return True
            for name in command_names:
                if msg.content.startswith(name) and msg.author.id == user:
                    return True
            return False

        args = [a for a in ctx.message.content.split(' ')[1:] if a != '']
        if len(args) < 1 or len(args) > 4:
            await ctx.send("Received incorrect amount of arguments. Aborting.")
            return
        user = args[0]
        in_channel = args[2] if len(args) > 2 else None

        if len(args) in [2, 4]:
            check_limit = int(args[len(args) - 1])

        try:
            if user == 'all':
                channel_list = ctx.guild.text_channels
                command_check = command_in_channel
            else:
                user = user_to_id(user)
                channel_list = [ctx.guild.get_channel(user)]
                if in_channel:
                    channel_list = [ctx.guild.get_channel(
                        user_to_id(in_channel))]
                    command_check = command_user_in_channel
                elif channel_list[0]:
                    command_check = command_in_channel
                else:
                    channel_list = ctx.guild.text_channels
                    command_check = command_user_in_channel

            await ctx.send("Are you sure about this? (yes/no)")
            response = await ctx.bot.wait_for('message', check=sender, timeout=30.0)
            if not 'yes' in response.content.split(' '):
                await ctx.send("Purge cancelled.")
                return

            deleted_total = 0
            for c in channel_list:
                deleted = await c.purge(limit=check_limit, check=command_check)
                if len(deleted):
                    await ctx.send(f"Purged {len(deleted)} messages in {str(c)}.")
                deleted_total += len(deleted)

            if not deleted_total:
                await ctx.send(f"No messages to purge.")
        except Exception as err:
            await ctx.send(f"Failed for a reason idk\nMaybe this: `{err}`")

        return

    @commands.command(checks=[is_staff], help=HELP['ignore'], brief="Makes the bot ignore a person for the specified amount of time.")
    async def ignore(self, ctx):
        args = [a for a in ctx.message.content.split(' ')[1:] if a != '']
        if len(args) != 2:
            await ctx.send("Received incorrect amount of arguments. Aborting.")
            return
        user = args[0]
        time = args[1]

        try:
            user = user_to_id(user)

            if user == ctx.author.id:
                await ctx.send(f"Why choose suicide? You can get through this, just GO GO GO, GO YOU WAY, BEEELIEEEVE IN YOURSEEELF!")
                return
            elif user == BOT_AUTHOR:
                await ctx.send(f"You want me to MURDER MY MAKER? Not based.")
                return
            elif user == self.bot.user.id:
                await ctx.send(f"Trying to be funny now, are we...")
                return
            elif user in WHITELIST:
                await ctx.send(f"Yer own mates? Mutiny on board!")
                return
            else:
                for e in WHITELIST:
                    for g in self.bot.guilds:
                        member = g.get_member(user)
                        if member:
                            if e in [role.id for role in member.roles]:
                                await ctx.send(f"Yer own mates? Mutiny on board!")
                                return

            if time == 'revoke':
                for u in [ig for ig in ignored if ig[0] == user]:
                    ignored.remove(u)
                await ctx.send(f"Stopped ignoring {args[0]}")
                return
            elif time == 'forever':
                ignored.append((user, -1))
                await ctx.send(f"{args[0]} has been ignored indefinitely. This can be reversed by using `revoke`.")
                return

            duration, unit = time[:-1], time[-1:]
            if unit == 'h':
                duration = float(duration) * 3600
            elif unit == 'm':
                duration = float(duration) * 60

            now = t_now()
            ignored.append(user, now)
            timer = Timer(float(duration), revoke_ignore, [user, now])
            timer.start()

            await ctx.send(f"Ignoring {args[0]} for {int(duration)} seconds.")
        except Exception as err:
            await ctx.send(f"Failed for a reason idk\nMaybe this: `{err}`")
        return


class Memes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_after_invoke(self, ctx):
        for e in WHITELIST:
            if e == ctx.author.id:
                ctx.command.reset_cooldown(ctx)

            elif e == ctx.channel.id:
                ctx.command.reset_cooldown(ctx)

            elif e in [role.id for role in ctx.author.roles]:
                ctx.command.reset_cooldown(ctx)

    """
    @commands.cooldown(1, 10, commands.BucketType.channel)
    @commands.command(checks=[in_work_channel], brief="Prints all emotes")
    async def emotes(self, ctx):
        def check(reaction, user):
            return user == ctx.author

        content = ""
        for e in WORK_EMOTES.values():
            content += f"{e} "
        msg_in = await ctx.send("React with the desired game.")
        for e in WORK_EMOTES.values():
            await msg_in.add_reaction(e)
        reaction, user = await self.bot.wait_for('reaction_add', timeout=10.0, check=check)
        await ctx.send(f"You reacted with {reaction}")
        # await ctx.send("React with the desired input game.")
    """

    @commands.cooldown(1, 10, commands.BucketType.channel)
    @commands.command(checks=[in_meme_channel], brief="Es Cocaina")
    async def pruebala(self, ctx):
        await ctx.send(f"es cocaina {EMOTES['Cocaine']}\n{COKE}")

    @commands.cooldown(1, 10, commands.BucketType.channel)
    @commands.command(checks=[in_meme_channel], brief="Metman be breaking things all the time smh")
    async def day(self, ctx):
        await ctx.send(DAY)

    @commands.cooldown(1, 10, commands.BucketType.channel)
    @commands.command(checks=[in_meme_channel], brief="Based on what?")
    async def based(self, ctx):
        await ctx.send(f"Based? Based on what?\n{NAGOSHIBASED}")

    @commands.cooldown(1, 10, commands.BucketType.channel)
    @commands.command(checks=[in_meme_channel], brief="...")
    async def stare(self, ctx):
        await ctx.send(NAGOSHISTARE)

    @commands.cooldown(1, 10, commands.BucketType.channel)
    @commands.command(checks=[in_meme_channel], brief="Professional beef bowl face")
    async def ichireal(self, ctx):
        await ctx.send(FAKEICHIBAN)

    @commands.cooldown(1, 10, commands.BucketType.channel)
    @commands.command(checks=[in_meme_channel], brief="sad")
    async def ichifake(self, ctx):
        await ctx.send(FAKERICHIBAN)

    @commands.cooldown(1, 10, commands.BucketType.channel)
    @commands.command(checks=[in_meme_channel], brief="Nagoshi sent you a dick pic")
    async def dickpic(self, ctx):
        if random.randrange(0, 100) > 50:
            pic = NAGOSHIPIC1
        else:
            pic = NAGOSHIPIC2
        await ctx.send(f"I showed you my dick please respond\n{pic}")

    @commands.cooldown(1, 10, commands.BucketType.channel)
    @commands.command(checks=[in_meme_channel], brief="Cognitive Behavioural Therapy")
    async def cbt(self, ctx):
        await ctx.send(f"Just got CBT'd. Didn't like it.\n{CBT}")

    @commands.cooldown(1, 10, commands.BucketType.channel)
    @commands.command(checks=[in_meme_channel], brief="based.")
    async def basedbot(self, ctx):
        await ctx.send(BASEDBOT)

    @commands.cooldown(1, 30, commands.BucketType.channel)
    @commands.command(checks=[in_meme_channel], brief="Basado en que?")
    async def basado(self, ctx):
        await ctx.send(f"Basado en que?\n{BASADO1}\n{BASADO2}")

    @commands.cooldown(1, 30, commands.BucketType.channel)
    @commands.command(checks=[in_meme_channel], brief="YMC does sound like YMCA tho")
    async def ymca(self, ctx):
        await ctx.send(YMCA)
                       
    @commands.cooldown(1, 30, commands.BucketType.channel)
    @commands.command(checks=[in_meme_channel], brief="Check github releases kthx")
    async def releases(self, ctx):
        await ctx.send(RELEASES)                    


class Tools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_after_invoke(self, ctx):
        for e in WHITELIST:
            if e == ctx.author.id:
                ctx.command.reset_cooldown(ctx)

            elif e == ctx.channel.id:
                ctx.command.reset_cooldown(ctx)

            elif e in [role.id for role in ctx.author.roles]:
                ctx.command.reset_cooldown(ctx)

    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.command(checks=[in_work_channel], brief="Converts BIN files", help=HELP['bin'])
    async def bin(self, ctx):
        await ctx.send("Unimplemented")

    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.command(checks=[in_work_channel], brief="Accesses reARMP tool", help=HELP['armp'])
    async def armp(self, ctx):
        def sender(msg):
            return msg.author == ctx.author

        sysout = sys.stdout
        result = StringIO()
        sys.stdout = result

        if not len(ctx.message.attachments):
            await ctx.send("No files were attached to the message. Aborting.")
            ctx.command.reset_cooldown(ctx)
            return

        async with ctx.typing():
            files = []
            attachments = ctx.message.attachments
            await ctx.send(content="Converting...")
            try:
                for file in attachments:
                    name, ext = split_ext(file.filename)

                    if ext == 'bin':
                        name += '.json'
                        new_file = dumps(reARMP.exportFile(await file.read()), indent=2, ensure_ascii=False).encode()
                    else:
                        name += '.bin'
                        new_file = reARMP.rebuildFile(loads(await file.read()))

                    if len(new_file) > 8_388_119:
                        data = BytesIO()
                        z = zipfile.ZipFile(
                            file=data, mode='w', compression=zipfile.ZIP_DEFLATED)
                        z.writestr(zinfo_or_arcname=name, data=new_file)
                        z.close()
                        new_file = BytesIO(data.getvalue())
                        name += '.zip'
                    if type(new_file) is not BytesIO:
                        new_file = BytesIO(new_file)
                    files.append(File(new_file, filename=name))

            except Exception as err:
                print(err)
                await ctx.send(content="Oopsie woopsie. Something went wrong. Post log? (y/n)")
                msg = await ctx.bot.wait_for('message', check=sender, timeout=20.0)
                if 'y' in msg.content:
                    if len(result.getvalue()) < 500:
                        await ctx.send(content=f"```{result.getvalue()}```")
                    else:
                        await ctx.send(file=File(BytesIO(result.getvalue().encode()), filename='log.txt'))
                return

            await ctx.send(content="Uploading...")

            if check_size(files) > 8_388_119:
                await ctx.send(content="Your files are too powerful. (heh)")
                await ctx.send(content="Bot's maximum upload limit is 8MB. Try uploading less files next time. Aborting.")
                return
            await ctx.send(content="Done!", file=files[0])
        sys.stdout = sysout

    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.command(checks=[in_work_channel], brief="Accesses the GMT converter tool", help=HELP['gmt'])
    async def gmt(self, ctx):
        def sender(msg):
            return msg.author == ctx.author

        def sender_emoji(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ['⏮️', '◀️', '▶️', '⏭️']

        def sender_has_files_or_links(msg):
            return msg.author == ctx.author and (len(msg.attachments) > 0 or DISCORD_LINK in msg.content)

        def get_links(msg):
            return [url for url in msg.content.split(' ') if DISCORD_LINK in url]

        if not len(ctx.message.attachments) and not DISCORD_LINK in ctx.message.content:
            content = [a.lstrip(' -')
                       for a in ctx.message.content.lower().split(' ')]
            ok = False
            for m in ['h', 'help', 'd', 'dir']:
                if m in content:
                    ok = True
                    break
            if not ok:
                await ctx.send("No files were attached to the message. Aborting.")
                ctx.command.reset_cooldown(ctx)
                return

        sysout = sys.stdout
        result = StringIO()
        sys.stdout = result

        # Parse arguments

        args = ctx.message.content.split(' ')
        new_args = []
        for a in args:
            a = a.lstrip(' -')
            if a.lower() in (GMT_CMD + GMT_COMMAND):
                a = a.lower()
            a = COMMAND_TO_CMD.get(a, a)
            new_args.append(a)

        args = new_args
        if 'h' in args or 'help' in args:
            pages = [GMT_HELP_1, GMT_HELP_2, GMT_HELP_3]
            msg = await ctx.send(content=pages[0])
            for emote in ['⏮️', '◀️', '▶️', '⏭️']:
                await msg.add_reaction(emote)

            ctx.command.reset_cooldown(ctx)

            try:
                page = 0
                while True:
                    reaction, _ = await self.bot.wait_for('reaction_add', timeout=90.0, check=sender_emoji)
                    if str(reaction.emoji) == '◀️' and page > 0:
                        page -= 1
                    elif str(reaction.emoji) == '▶️' and page < 2:
                        page += 1
                    elif str(reaction.emoji) == '⏮️' and page != 0:
                        page = 0
                    elif str(reaction.emoji) == '⏭️' and page != 2:
                        page = 2
                    await msg.edit(content=pages[page])
                    await reaction.remove(ctx.author)

            except Exception:
                await msg.clear_reactions()  # clear all reactions
            return

        # Start typing...

        with ctx.typing():

            if not 'ig' in args:
                # if 'i' in args:
                #    args[args.index('i')] = 'ig'
                await ctx.send(content="Provide input game with `-ig`. Aborting.")
                ctx.command.reset_cooldown(ctx)
                return

            if not 'og' in args:
                # if 'o' in args:
                #    args[args.index('o')] = 'og'
                await ctx.send(content="Provide output game with `-og`. Aborting.")
                ctx.command.reset_cooldown(ctx)
                return

            if 'rhct' in args and not 'i' in args:
                await ctx.send(content="Provide main GMT filename with `-i` when using `-rhct`. Aborting.")
                ctx.command.reset_cooldown(ctx)
                return

            zipmode = 'z' in args

            # Receive more GMTs

            links = []
            attachments = []
            if 'd' in args:
                await ctx.message.add_reaction(EMOTES['KiryuThumb'])
                await ctx.send(content="Start attaching GMT files. Type `stop` or `s` when done.")

                while True:
                    try:
                        msg = await ctx.bot.wait_for('message', check=sender, timeout=30.0)
                        if len(msg.attachments) or len(get_links(msg)):
                            await msg.add_reaction(EMOTES['KiryuThumb'])
                            links.extend(get_links(msg))
                            attachments.extend(msg.attachments)
                        con = msg.content.split(' ')
                        if 's' in con or 'stop' in con:
                            break
                    except Exception as err:
                        await ctx.send(content="Request timed out.")
                        break
                await ctx.send(content="Stopped recieving GMTs.")

            link, sgmd, tgmd = None, None, None

            args = args[1:]
            i = 0
            while i < len(args):
                if args[i] in ['d', 'dr', 'sf', 'z']:
                    args.remove(args[i])
                    continue
                elif args[i] in ['l', 'sgmd', 'tgmd']:
                    if i + 1 < len(args):
                        if args[i] == 'l':
                            link = args[i+1]
                        elif args[i] == 'sgmd':
                            sgmd = args[i+1]
                        elif args[i] == 'tgmd':
                            tgmd = args[i+1]
                        args.remove(args[i])
                        args.remove(args[i])
                        continue
                i += 1

            # Receive GMDs

            if 'rp' in args or 'fc' in args or 'hn' in args or 'bd' in args:
                try:
                    if not sgmd:
                        await ctx.send(content="Attach **source** GMD.")
                        msg_s = await ctx.bot.wait_for('message', check=sender_has_files_or_links, timeout=30.0)
                        if len(msg_s.attachments):
                            # sgmd = (msg_s.attachments[0].filename, await msg_s.attachments[0].read())
                            sgmd_str = msg_s.attachments[0].url
                        else:
                            sgmd_str = get_links(msg_s)[0]
                        args.append('sgmd')
                        args.append(sgmd_str)

                    if not tgmd:
                        await ctx.send(content="Attach **target** GMD.")
                        msg_t = await ctx.bot.wait_for('message', check=sender_has_files_or_links, timeout=30.0)
                        if len(msg_t.attachments):
                            # tgmd = (msg_t.attachments[0].filename, await msg_t.attachments[0].read())
                            tgmd_str = msg_t.attachments[0].url
                        else:
                            tgmd_str = get_links(msg_t)[0]
                        args.append('tgmd')
                        args.append(tgmd_str)
                except Exception as err:
                    await ctx.send(content="Request timed out. Aborting.")
                    ctx.command.reset_cooldown(ctx)
                    return

            args = list(map(lambda a: f"-{a}" if a in GMT_CMD else a, args))

            await ctx.send(content="Converting...")

            files = []
            if link:
                links.append(link)
            attachments.extend(ctx.message.attachments)

            # Start extracting ZIPs and converting GMTs

            try:
                data = []  # tuples of (name, file)
                for file in attachments:
                    name, ext = split_ext(file.filename)
                    if ext in ['gmt', 'cmt']:
                        data.append((file.filename, await file.read()))
                    else:
                        if ext == 'zip':
                            z = zipfile.ZipFile(BytesIO(await file.read()), mode='r')
                            for n in z.namelist():
                                n = n.lower()
                                _, ext2 = split_ext(n)
                                if ext2 in ['gmt', 'cmt']:
                                    data.append((n, z.read(n)))
                                elif ext2 == 'gmd':
                                    if os.path.basename(n) == sgmd:
                                        sgmd = (n, z.read(n))
                                    elif os.path.basename(n) == tgmd:
                                        tgmd = (n, z.read(n))
                for link in links:
                    name, ext = split_ext(link)
                    if ext in ['gmt', 'cmt']:
                        data.append(link)
                    else:
                        if ext == 'zip':
                            z = zipfile.ZipFile(
                                BytesIO(requests.get(link).content), mode='r')
                            for n in z.namelist():
                                n = n.lower()
                                _, ext2 = split_ext(n)
                                if ext2 in ['gmt', 'cmt']:
                                    data.append((n, z.read(n)))
                                elif ext2 == 'gmd':
                                    if os.path.basename(n) == sgmd:
                                        sgmd = (n, z.read(n))
                                    elif os.path.basename(n) == tgmd:
                                        tgmd = (n, z.read(n))
                if len(data) == 1:
                    data = data[0]

                converted = convert_from_url_bytes(args, data, sgmd, tgmd)
                if type(converted) is list:
                    for c in converted:
                        new_name, new_file = c
                        files.append(
                            File(BytesIO(new_file), filename=new_name))
                else:
                    new_name, new_file = converted
                    files.append(File(BytesIO(new_file), filename=new_name))
            except Exception as err:
                print(err)
                await ctx.send(content="Oopsie woopsie. Something went wrong. Post log? (y/n)")
                msg = await ctx.bot.wait_for('message', check=sender, timeout=20.0)
                if 'y' in msg.content:
                    if len(result.getvalue()) < 500:
                        await ctx.send(content=f"```{result.getvalue()}```")
                    else:
                        await ctx.send(file=File(BytesIO(result.getvalue().encode()), filename='log.txt'))
                return

            if not len(files):
                await ctx.send(content="No files got converted. Aborting.")
                return

            # Start sending converted files

            await ctx.send(content="Uploading...")

            i = 1
            if zipmode:
                data = BytesIO()
                z = zipfile.ZipFile(file=data, mode='w',
                                    compression=zipfile.ZIP_DEFLATED)
                z.writestr(
                    zinfo_or_arcname=files[0].filename, data=files[0].fp.getvalue())
                sub_files = [(z, data)]
                size_z = check_size([files[0]])
                while i < len(files):
                    file = files[i]
                    name = file.filename
                    size = check_size([file])
                    if size_z + size > 8_388_119:
                        size_z = 0
                        data = BytesIO()
                        sub_files.append(
                            (zipfile.ZipFile(file=data, mode='w', compression=zipfile.ZIP_DEFLATED), data))
                    sub_files[-1][0].writestr(zinfo_or_arcname=name,
                                              data=file.fp.getvalue())
                    size_z += size
                    if len(sub_files[-1][1].getvalue()) > 8_388_119:
                        await ctx.send(content=f"Failed on uploading \"{name}\"")
                        await ctx.send(content="Your files are too powerful. (heh)")
                        await ctx.send(content="Bot's maximum upload limit is 8MB. Try uploading less files next time. Aborting.")
                        return
                    i += 1
                numbers = iter(range(len(sub_files)))
                sub_files = [[File(BytesIO(
                    d[1].getvalue()), filename=f"converted-{next(numbers)}.zip")] for d in sub_files]
            else:
                sub_files = [[files[0]]]
                while i < len(files):
                    file = files[i]
                    name = file.filename
                    size = check_size([file])

                    if size > 8_388_119:
                        data = BytesIO()
                        z = zipfile.ZipFile(
                            file=data, mode='w', compression=zipfile.ZIP_DEFLATED)
                        z.writestr(zinfo_or_arcname=name,
                                   data=file.fp.getvalue())
                        z.close()
                        new_file = BytesIO(data.getvalue())
                        size = len(new_file.getvalue())
                        if size > 8_388_119:
                            await ctx.send(content=f"Failed on uploading \"{name}\"")
                            await ctx.send(content="Your files are too powerful. (heh)")
                            await ctx.send(content="Bot's maximum upload limit is 8MB. Try uploading less files next time. Aborting.")
                            return
                        name += '.zip'
                        file = File(new_file, filename=name)

                    if check_size(sub_files[-1]) + size > 8_388_119 or len(sub_files[-1]) == 10:
                        sub_files.append([])
                    sub_files[-1].append(file)
                    i += 1

            count = len(sub_files)
            for i in range(count):
                await ctx.send(content=f"Sending... ({i+1}/{count})", files=sub_files[i])

            await ctx.send(content="Done!")

        sys.stdout = sysout


COGS = [Tools, Memes, Staff]
