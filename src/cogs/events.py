import re
from discord.ext import commands
from .dice import roll_dice  # Importa a função de rolagem de dados do arquivo dice.py

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        # Impedir que o bot responda a si mesmo
        if message.author == self.bot.user:
            return

        content = message.content.strip()
        author = message.author

        # Comando "ola bot"
        if content.lower() == "ola bot":
            await message.channel.send(f"Olá, {message.author.display_name}!")
        
        # Verifique se a mensagem é um comando para rolar dados no formato xdy
        elif re.match(r'^\d+d\d+$', content):
            try:
                num_rolls_command, sides = map(int, content.split('d'))
                if num_rolls_command <= 0 or sides <= 0:
                    await message.channel.send('Número de rolagens e lados do dado devem ser maiores que zero.')
                    return

                # Chama a função de rolagem de dados
                rolls = roll_dice(num_rolls_command, sides)
                sum_rolls = sum(rolls)

                # Responder a rolagem no canal apropriado
                if message.channel.id == self.bot.ROLEPLAY_CHANNEL_ID:
                    # Apenas responde a mensagem no mesmo canal de roleplay
                    await message.reply(f'{sum_rolls} ⟵ {rolls} ⟵ {content}')
                else:
                    # Transferir a mensagem original para o canal de roleplay
                    roleplay_channel = self.bot.get_channel(self.bot.ROLEPLAY_CHANNEL_ID)
                    bot_message = await roleplay_channel.send(f'{message.author.mention}: {content}')

                    # Excluir a mensagem original
                    await message.delete()

                    # Enviar a resposta como reply na mensagem do bot no canal de roleplay
                    await bot_message.reply(f'{sum_rolls} ⟵ {rolls} ⟵ {content}')
            
            except ValueError:
                await message.channel.send('Erro ao processar a rolagem de dados.')

async def setup(bot):
    await bot.add_cog(Events(bot))
