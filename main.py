#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Universal Media Downloader
Spotify ve YouTube için birleşik indirici
"""

import sys
import os
import argparse

# Windows encoding fix
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
    os.environ['PYTHONIOENCODING'] = 'utf-8'

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich import box
from rich.text import Text

from functions.spotify_downloader import SpotifyDownloader
from functions.youtube_downloader import YouTubeDownloader
from functions.ffmpeg_installer import FFmpegInstaller

console = Console()


def show_main_banner():
    """Ana banner'ı göster"""
    banner = Text()
    banner.append("🎵 ", style="bold green")
    banner.append("Universal Media Downloader", style="bold cyan")
    banner.append(" 🎵", style="bold green")
    banner.append("\n\n", style="")
    banner.append("Spotify & YouTube Downloader", style="dim white")
    
    panel = Panel(
        banner,
        box=box.DOUBLE,
        border_style="bright_magenta",
        padding=(1, 2)
    )
    console.print(panel)
    console.print()


def detect_platform(url: str) -> str:
    """URL'den platformu otomatik algıla"""
    if "spotify.com" in url:
        return "spotify"
    elif "youtube.com" in url or "youtu.be" in url:
        return "youtube"
    else:
        return "unknown"


def interactive_mode():
    """İnteraktif mod - otomatik platform algılama"""
    show_main_banner()
    
    # FFmpeg kontrolü
    ffmpeg_installer = FFmpegInstaller()
    if not ffmpeg_installer.check_ffmpeg():
        console.print("[yellow]⚠ FFmpeg bulunamadi[/yellow]")
        console.print("[dim]FFmpeg ses/video donusturme icin gereklidir.[/dim]\n")
        
        # Kurulum seçenekleri tablosu
        options_table = Table(show_header=True, box=box.SIMPLE)
        options_table.add_column("Secenek", style="cyan", justify="center", width=10)
        options_table.add_column("Aciklama", style="white", width=50)
        options_table.add_row("1", "Otomatik kurulum (onerilir)")
        options_table.add_row("2", "Manuel kurulum talimatlarini goster")
        options_table.add_row("3", "Simdilik atla (bazi ozellikler calismayabilir)")
        
        console.print(options_table)
        console.print()
        
        choice = Prompt.ask(
            "[yellow]Seciminiz[/yellow]",
            choices=["1", "2", "3"],
            default="1"
        )
        
        console.print()
        
        if choice == "1":
            if not ffmpeg_installer.install():
                console.print("\n[yellow]Otomatik kurulum basarisiz oldu.[/yellow]")
                console.print("[cyan]Manuel kurulum:[/cyan]")
                console.print("  Windows: [white]winget install FFmpeg[/white]")
                console.print("  Veya: [white]https://ffmpeg.org/download.html[/white]\n")
        elif choice == "2":
            console.print("[cyan]Manuel Kurulum Talimatlari:[/cyan]\n")
            console.print("[bold]Windows:[/bold]")
            console.print("  1. Komut satirini ac (CMD veya PowerShell)")
            console.print("  2. Su komutu calistir: [white]winget install FFmpeg[/white]")
            console.print("  3. Veya: https://ffmpeg.org/download.html adresinden indir\n")
            console.print("[bold]Linux:[/bold]")
            console.print("  Ubuntu/Debian: [white]sudo apt install ffmpeg[/white]")
            console.print("  Fedora: [white]sudo dnf install ffmpeg[/white]\n")
            console.print("[bold]macOS:[/bold]")
            console.print("  [white]brew install ffmpeg[/white]\n")
            
            input("[dim]Devam etmek icin Enter'a basin...[/dim]")
            console.print()
        else:
            console.print("[yellow]FFmpeg olmadan devam ediliyor.[/yellow]")
            console.print("[dim]Not: Bazi format donusturmeleri calismayabilir.[/dim]\n")
    
    # Desteklenen platformları göster
    info_table = Table(show_header=True, box=box.ROUNDED, border_style="cyan")
    info_table.add_column("Platform", style="bold cyan", width=15)
    info_table.add_column("Desteklenen", style="white", width=50)
    
    info_table.add_row("♫ Spotify", "Sarki, Album, Playlist, Sanatci")
    info_table.add_row("▶ YouTube", "Video, Playlist, Canli Yayin")
    
    console.print(info_table)
    console.print()
    
    # URL al - otomatik algılama
    url = Prompt.ask(
        "[yellow]URL'yi girin[/yellow]\n"
        "[dim](Spotify veya YouTube linki - otomatik algilanacak)[/dim]"
    )
    
    if not url:
        console.print("[red]URL gerekli![/red]")
        return
    
    console.print()
    
    # Platform algıla
    platform = detect_platform(url)
    
    if platform == "spotify":
        console.print("[green]✓[/green] Spotify linki algilandi!\n")
        downloader = SpotifyDownloader()
        
        if not downloader.check_spotdl():
            if Confirm.ask("[yellow]spotdl yuklu degil. Yuklemek ister misiniz?[/yellow]"):
                if not downloader.install_spotdl():
                    console.print("[red]Program sonlandiriliyor.[/red]")
                    return
            else:
                console.print("[red]spotdl gerekli. Program sonlandiriliyor.[/red]")
                return
        
        # Spotify interactive mode
        downloader.interactive_mode_with_url(url)
        
    elif platform == "youtube":
        console.print("[green]✓[/green] YouTube linki algilandi!\n")
        downloader = YouTubeDownloader()
        
        if not downloader.check_ytdlp():
            if Confirm.ask("[yellow]yt-dlp yuklu degil. Yuklemek ister misiniz?[/yellow]"):
                if not downloader.install_ytdlp():
                    console.print("[red]Program sonlandiriliyor.[/red]")
                    return
            else:
                console.print("[red]yt-dlp gerekli. Program sonlandiriliyor.[/red]")
                return
        else:
            # yt-dlp güncel mi kontrol et
            if Confirm.ask("[yellow]yt-dlp'yi guncellemek ister misiniz? (Onerilir)[/yellow]", default=True):
                downloader.update_ytdlp()
        
        # YouTube interactive mode
        downloader.interactive_mode_with_url(url)
        
    else:
        console.print("[red]X[/red] Gecersiz URL! Spotify veya YouTube linki girin.")


def main():
    """Ana program"""
    # FFmpeg kontrolü (sessiz)
    ffmpeg_installer = FFmpegInstaller()
    if not ffmpeg_installer.check_ffmpeg():
        console.print("[dim]FFmpeg bulunamadi. Otomatik kurulum icin -i modunu kullanin.[/dim]\n")
    
    parser = argparse.ArgumentParser(
        description="Universal Media Downloader - Spotify & YouTube",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ornekler:
  %(prog)s -u https://open.spotify.com/playlist/...
  %(prog)s -u https://www.youtube.com/watch?v=...
  %(prog)s -u https://www.youtube.com/playlist?list=... --audio
  %(prog)s -i  # Interaktif mod
        """
    )
    
    parser.add_argument(
        "-u", "--url",
        help="Spotify veya YouTube URL"
    )
    parser.add_argument(
        "-o", "--output",
        default="downloads",
        help="Cikti dizini (varsayilan: downloads)"
    )
    parser.add_argument(
        "-p", "--platform",
        choices=["spotify", "youtube", "auto"],
        default="auto",
        help="Platform secimi (varsayilan: auto)"
    )
    parser.add_argument(
        "--audio",
        action="store_true",
        help="Sadece ses olarak indir (YouTube icin)"
    )
    parser.add_argument(
        "-i", "--interactive",
        action="store_true",
        help="Interaktif mod"
    )
    
    args = parser.parse_args()
    
    # İnteraktif mod
    if args.interactive or not args.url:
        interactive_mode()
        return
    
    # Komut satırı modu
    show_main_banner()
    
    # Platform algılama
    if args.platform == "auto":
        platform = detect_platform(args.url)
    else:
        platform = args.platform
    
    if platform == "spotify":
        console.print("[green]✓[/green] Spotify modu\n")
        downloader = SpotifyDownloader(args.output)
        
        if not downloader.check_spotdl():
            console.print("[red]spotdl yuklu degil! Lutfen yukleyin: pip install spotdl[/red]")
            sys.exit(1)
        
        downloader.download(args.url)
        
    elif platform == "youtube":
        console.print("[green]✓[/green] YouTube modu\n")
        downloader = YouTubeDownloader(args.output)
        
        if not downloader.check_ytdlp():
            console.print("[red]yt-dlp yuklu degil! Lutfen yukleyin: pip install yt-dlp[/red]")
            sys.exit(1)
        
        downloader.download(args.url, audio_only=args.audio)
        
    else:
        console.print("[red]X[/red] Gecersiz URL veya platform!")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[yellow]Program sonlandirildi.[/yellow]")
        sys.exit(0)
