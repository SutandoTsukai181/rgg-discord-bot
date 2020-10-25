import os
import sys
import zlib
import zipfile
from io import BytesIO, StringIO
from math import ceil
from json import loads, dumps
import random

import requests

from discord import File, utils, DMChannel
from discord.ext import commands
from dotenv import load_dotenv

from help import *
from utils import *
from reARMP import reARMP
from gmt_converter.main import convert_from_url_bytes

load_dotenv()

MEME_CHANNELS = os.getenv('DISCORD_MEME_CHANNELS')
WORK_CHANNELS = os.getenv('DISCORD_WORK_CHANNELS')
CHANNELS = list(set().union(MEME_CHANNELS, WORK_CHANNELS))


def in_channel(ctx):
    return ctx.message.channel.name in CHANNELS if type(ctx.message.channel) is not DMChannel else True


def in_meme_channel(ctx):
    return ctx.message.channel.name in MEME_CHANNELS if type(ctx.message.channel) is not DMChannel else True


def in_work_channel(ctx):
    return ctx.message.channel.name in WORK_CHANNELS


"""
def has_files(ctx):
    if not len(ctx.message.attachments):
        content = [a.lstrip(' -') for a in ctx.message.content.lower().split(' ')]
        
        for m in ['h', 'help', 'd', 'dir']:
            if m in content:
                return True
        await ctx.send("No files were attached to the message. Aborting.")
        return False
    return True
"""


class Memes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(checks=[in_work_channel], brief="Prints all emotes")
    async def emotes(self, ctx):
        def check(reaction, user):
            return user == ctx.message.author

        content = ""
        for e in WORK_EMOTES.values():
            content += f"{e} "
        msg_in = await ctx.message.channel.send("React with the desired input game.")
        for e in WORK_EMOTES.values():
            await msg_in.add_reaction(e)
        reaction, user = await self.bot.wait_for('reaction_add', timeout=10.0, check=check)
        await ctx.message.channel.send(f"You reacted with {reaction}")
        # await ctx.message.channel.send("React with the desired input game.")

    @commands.command(checks=[in_meme_channel], brief="Es Cocaina")
    async def pruebala(self, ctx):
        await ctx.message.channel.send(f"es cocaina {EMOTES['Cocaine']}\n{COKE}")

    @commands.command(checks=[in_meme_channel], brief="Based on what?")
    async def based(self, ctx):
        await ctx.message.channel.send(f"Based? Based on what?\n{NAGOSHIBASED}")

    @commands.command(checks=[in_meme_channel], brief="...")
    async def stare(self, ctx):
        await ctx.message.channel.send(NAGOSHISTARE)

    @commands.command(checks=[in_meme_channel], brief="Professional beef bowl face")
    async def ichireal(self, ctx):
        await ctx.message.channel.send(FAKEICHIBAN)

    @commands.command(checks=[in_meme_channel], brief="Nagoshi sent you a dick pic")
    async def dickpic(self, ctx):
        if random.randrange(0, 100) > 50:
            pic = NAGOSHIPIC1
        else:
            pic = NAGOSHIPIC2
        await ctx.message.channel.send(f"I showed you my dick please respond\n{pic}")


class Tools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(checks=[in_work_channel], brief="Converts BIN files", help=HELP['bin'])
    async def bin(self, ctx):
        await ctx.message.channel.send("Unimplemented")

    @commands.command(checks=[in_work_channel], brief="Accesses reARMP tool", help=HELP['armp'])
    async def armp(self, ctx):
        def sender(msg):
            return msg.author == ctx.message.author

        sysout = sys.stdout
        result = StringIO()
        sys.stdout = result

        if not len(ctx.message.attachments):
            await ctx.send("No files were attached to the message. Aborting.")
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
                            file=data, mode='w', compression=zipfile.ZIP_DEFLATED, compresslevel=zlib.Z_BEST_COMPRESSION)
                        z.writestr(zinfo_or_arcname=name, data=new_file)
                        z.close()
                        new_file = BytesIO(data.getvalue())
                        name += '.zip'
                    if type(new_file) is not BytesIO:
                        new_file = BytesIO(new_file)
                    files.append(File(new_file, filename=name))

            except Exception as err:
                print(err)
                await ctx.send(content="Oopsie woopsie. Something went wrong. Post log?")
                msg = await ctx.bot.wait_for('message', check=sender, timeout=15.0)
                if 'y' in msg.content:
                    if len(result.getvalue()) < 500:
                        await ctx.send(content=f"```{result.getvalue()}```")
                    else:
                        await ctx.send(file=File(BytesIO(result.getvalue().encode()), filename='log.txt'))
                return

            if check_size(files) > 8_388_119:
                await ctx.send(content="Your files are too powerful. (heh)")
                await ctx.send(content="Bot's maximum upload limit is 8MB. Try uploading less files next time. Aborting.")
                return
            await ctx.send(content="Done!", file=files[0])
        sys.stdout = sysout

    @commands.command(checks=[in_work_channel], brief="Accesses the GMT converter tool", help=HELP['gmt'])
    async def gmt(self, ctx):
        def sender(msg):
            return msg.author == ctx.message.author

        def sender_has_files_or_links(msg):
            return msg.author == ctx.message.author and (len(msg.attachments) > 0 or DISCORD_LINK in msg.content)

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
                return

        sysout = sys.stdout
        result = StringIO()
        sys.stdout = result

        # Start typing...

        with ctx.typing():

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
                help1 = True
                if 'h' in args:
                    if len(args) > args.index('h') + 1:
                        if args[args.index('h') + 1] == '2':
                            help1 = False
                elif 'help' in args:
                    if len(args) > args.index('help') + 1:
                        if args[args.index('help') + 1] == '2':
                            help1 = False
                if help1:
                    await ctx.send(content=f"Showing help 1, use `.gmt -h 2` for the rest of the commands\n{GMT_HELP_1}")
                else:
                    await ctx.send(content=f"Showing help 2\n{GMT_HELP_2}")
                return

            if not 'ig' in args:
                # if 'i' in args:
                #    args[args.index('i')] = 'ig'
                await ctx.send(content="Provide input game with \'-ig\'. Aborting.")
                return

            if not 'og' in args:
                # if 'o' in args:
                #    args[args.index('o')] = 'og'
                await ctx.send(content="Provide output game with \'-og\'. Aborting.")
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
            print(args)
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
            print(args)
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
                await ctx.send(content="Oopsie woopsie. Something went wrong. Post log?")
                msg = await ctx.bot.wait_for('message', check=sender, timeout=15.0)
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

            i = 1
            if zipmode:
                data = BytesIO()
                z = zipfile.ZipFile(
                    file=data, mode='w', compression=zipfile.ZIP_DEFLATED, compresslevel=zlib.Z_BEST_COMPRESSION)
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
                        sub_files.append((zipfile.ZipFile(
                            file=data, mode='w', compression=zipfile.ZIP_DEFLATED, compresslevel=zlib.Z_BEST_COMPRESSION), data))
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
                            file=data, mode='w', compression=zipfile.ZIP_DEFLATED, compresslevel=zlib.Z_BEST_COMPRESSION)
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

        #result_string = result.getvalue()
        # print(result_string)
        sys.stdout = sysout


COGS = [Tools, Memes]
