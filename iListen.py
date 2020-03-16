client = commands.Bot(command_prefix= '!')


# Get all users in all servers the bot is connected to


@client.command(pass_context=True)
async def listen(ctx):
    channel = ctx.message.author.voice.channel
    if not channel:
        await ctx.send("You are not connected to a voice channel")
        return
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    source = FFmpegPCMAudio('1.m4a')
    player = voice.play(source)
