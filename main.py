import discord
from discord import app_commands
from discord.ext import commands

# Configuração dos Intents
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# E-mail cadastrado como Administrador Supremo
ADMIN_EMAIL = "jcodogn@gmail.com"

# Lista de todos os planos disponíveis no sistema
TODOS_OS_PLANOS = ["Free", "Silver", "Gold", "Platinum", "Ônix (VIP)"]

# Simulação de Banco de Dados na memória
# Formato: { discord_id: {"email": str, "cargo": str, "planos": list} }
database_usuarios = {}

@bot.event
async def on_ready():
    print(f"Bot conectado como: {bot.user.name}")
    try:
        # Sincroniza os comandos de barra (Slash Commands) com o Discord
        synced = await bot.tree.sync()
        print(f"Sincronizados {len(synced)} comandos de barra.")
    except Exception as e:
        print(f"Erro ao sincronizar comandos: {e}")

# -------------------------------------------------------------
# Comando de Barra: /autenticar
# -------------------------------------------------------------
@bot.tree.command(name="autenticar", description="Autentique seu e-mail no sistema")
@app_commands.describe(email="Digite o seu e-mail cadastrado")
async def autenticar(interaction: discord.Interaction, email: str):
    user_id = interaction.user.id
    email_limpo = email.strip().lower()

    # Checa se o e-mail é o do Admin
    if email_limpo == ADMIN_EMAIL.lower():
        database_usuarios[user_id] = {
            "email": email_limpo,
            "cargo": "Administrador",
            "planos": TODOS_OS_PLANOS # Acesso a todos os planos vitalícios
        }
        
        embed = discord.Embed(
            title="⚡ Autenticação de Administrador",
            description="Bem-vindo de volta, **Admin**!",
            color=discord.Color.gold()
        )
        embed.add_field(name="E-mail", value=email_limpo, inline=False)
        embed.add_field(name="Cargo", value="👑 Administrador", inline=True)
        embed.add_field(name="Acesso concedido", value="Vitalício a **TODOS** os planos (Free até Ônix)", inline=False)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

    else:
        # Usuário comum (Cliente)
        database_usuarios[user_id] = {
            "email": email_limpo,
            "cargo": "Cliente",
            "planos": ["Free"] # Plano básico inicial
        }

        embed = discord.Embed(
            title="✅ Autenticação Concluída",
            description="Você entrou como **Cliente**.",
            color=discord.Color.green()
        )
        embed.add_field(name="E-mail", value=email_limpo, inline=False)
        embed.add_field(name="Cargo", value="👤 Cliente", inline=True)
        embed.add_field(name="Plano Atual", value="Free (Vitalício)", inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)

# -------------------------------------------------------------
# Comando de Barra: /meu_plano
# -------------------------------------------------------------
@bot.tree.command(name="meu_plano", description="Verifique seus acessos e plano atual")
async def meu_plano(interaction: discord.Interaction):
    user_id = interaction.user.id

    if user_id not in database_usuarios:
        await interaction.response.send_message(
            "❌ Você ainda não fez a autenticação! Use `/autenticar <seu_email>`.",
            ephemeral=True
        )
        return

    dados = database_usuarios[user_id]
    planos_formatados = "\n".join([f"• {plano}" for plano in dados["planos"]])

    embed = discord.Embed(
        title="📋 Informações da Conta",
        color=discord.Color.blue()
    )
    embed.add_field(name="Usuário", value=interaction.user.mention, inline=True)
    embed.add_field(name="Cargo", value=dados["cargo"], inline=True)
    embed.add_field(name="E-mail Registrado", value=dados["email"], inline=False)
    embed.add_field(name="Planos Liberados", value=planos_formatados, inline=False)

    await interaction.response.send_message(embed=embed, ephemeral=True)

# Substitua 'SEU_TOKEN_AQUI' pelo token do seu bot obtido no Discord Developer Portal
bot.run("SEU_TOKEN_AQUI")