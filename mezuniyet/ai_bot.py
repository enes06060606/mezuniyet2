import discord  # Discord kütüphanesi
from discord.ext import commands  # Komut sistemi
import os  # Dosya işlemleri
from model import get_class  # Modelden sınıflandırma fonksiyonu

# Bot izinlerini ayarla
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True

# Botu oluştur
bot = commands.Bot(command_prefix="!", intents=intents)

# Görsellerin kaydedileceği klasör
IMAGE_DIR = "images"
os.makedirs(IMAGE_DIR, exist_ok=True)

@bot.command()
async def check(ctx):
    if not ctx.message.attachments:
        await ctx.send("⚠️ Görsel yüklemeyi unuttun!")
        return
    
    for attachment in ctx.message.attachments:
        file_name = attachment.filename
        file_path = os.path.join(IMAGE_DIR, file_name)
        
        try:
            await attachment.save(file_path)
            await ctx.send(f"✅ Görsel başarıyla kaydedildi: `{file_name}`")
            class_name, confidence_score = get_class(file_path)

            await ctx.send(f" Sınıflandırma sonucu: `{class_name}`\n Güven skoru: `{confidence_score:.2f}`")

            cikarimlar={
                "donusebilir":"Bu atık geri dönüştürülebilir, lütfen geri dönüşüm kutusuna atın.",
                "donusemeyenler":"BU atık dönüşemez bu yüzden geri dönüşüm kutusuna atılmalıdır. Lütfen çöpe atın.",
            }

            cikarim=cikarimlar.get(class_name, "Bu sınıf için bir çıkarım bulunamadı.")
            await ctx.send(f"🔍 Çıkarım: `{cikarim}`")

        except Exception as e:
            await ctx.send(f"❌ Görsel kaydedilemedi: `{file_name}`\n Hata: {str(e)}")
    return
bot.run("TOKEN")  # Botun tokenini buraya ekleyin
# Not: Gerçek tokeninizi paylaşmayın, bu güvenlik açığına neden olabilir