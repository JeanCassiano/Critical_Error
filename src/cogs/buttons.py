import discord
from discord.ext import commands
from discord.ui import Button, View

class ModerationView(View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

        # Adicionando 5 botões com callbacks específicos
        for i in range(1, 6):
            button = Button(label=f'Botão {i}', custom_id=f'button_{i}')
            button.callback = self.button_callback
            self.add_item(button)

    async def button_callback(self, interaction: discord.Interaction):
        # Atualiza a flag de modificação de rolagem com base no botão clicado
        button_number = int(interaction.custom_id.split("_")[1])
        self.bot.dice_modifier_flag = button_number  # Altera o modificador para a próxima rolagem
        await interaction.response.send_message(f'O resultado da próxima rolagem será modificado pelo Botão {button_number}!', ephemeral=True)


class ButtonsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.dice_modifier_flag = 0  # Inicializa a flag de modificação de rolagem

    @commands.Cog.listener()
    async def on_ready(self):
        print('Botões prontos!')
        moderation_channel = self.bot.get_channel(self.bot.MODERATION_CHANNEL_ID)
        if moderation_channel:
            view = ModerationView(self.bot)
            await moderation_channel.send('Escolha uma opção para modificar a próxima rolagem de dados:', view=view)


async def setup(bot):
    await bot.add_cog(ButtonsCog(bot))
